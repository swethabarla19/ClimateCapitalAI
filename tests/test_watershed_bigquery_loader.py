from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from google.api_core.exceptions import NotFound
from google.cloud import bigquery

from scripts.data import load_watershed_projects_bigquery as loader


EXPECTED_SCHEMA = (
    ("source_id", "STRING", "REQUIRED"),
    ("source_pdf_page", "INTEGER", "REQUIRED"),
    ("source_table_row_order", "INTEGER", "REQUIRED"),
    ("map_label", "STRING", "REQUIRED"),
    ("subproject_id", "STRING", "REQUIRED"),
    ("project_name", "STRING", "REQUIRED"),
    ("current_funding_request_estimate_source", "STRING", "REQUIRED"),
    ("current_funding_request_estimate_dollars", "INTEGER", "REQUIRED"),
    ("council_districts_source", "STRING", "REQUIRED"),
)


class SourceCsvPreflightTests(unittest.TestCase):
    def test_governed_source_artifact_passes_exact_preflight(self) -> None:
        summary = loader.validate_source_csv()

        self.assertEqual(summary.checksum, loader.EXPECTED_CSV_SHA256)
        self.assertEqual(summary.row_count, 37)
        self.assertEqual(summary.funding_total_dollars, 327_970_000)
        self.assertTrue(loader.CSV_PATH.is_absolute())
        self.assertTrue(loader.CSV_PATH.is_relative_to(loader.REPOSITORY_ROOT))

    def test_wrong_header_order_fails_before_any_cloud_call(self) -> None:
        content = loader.CSV_PATH.read_bytes().replace(
            b"source_id,source_pdf_page",
            b"source_pdf_page,source_id",
            1,
        )

        with self.assertRaisesRegex(loader.LoadValidationError, "schema order"):
            loader.validate_csv_content(content)

    def test_non_utf8_source_fails_clearly(self) -> None:
        with self.assertRaisesRegex(loader.LoadValidationError, "valid UTF-8"):
            loader.validate_csv_content(b"\xff")

    def test_differing_historical_artifact_checksum_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_source = Path(temporary_directory) / "projects.csv"
            changed_source.write_bytes(loader.CSV_PATH.read_bytes() + b"\n")

            with self.assertRaisesRegex(
                loader.LoadValidationError,
                "checksum does not match",
            ):
                loader.validate_source_csv(changed_source)


class LoadContractTests(unittest.TestCase):
    def test_target_and_schema_match_the_governed_contract(self) -> None:
        self.assertEqual(loader.PROJECT_ID, "climatecapital-ai")
        self.assertEqual(loader.DATASET_ID, "raw")
        self.assertEqual(loader.TABLE_ID, "watershed_projects_2025_11_21")
        self.assertEqual(loader.LOCATION, "us-central1")
        self.assertEqual(loader.FULL_TABLE_ID, "climatecapital-ai.raw.watershed_projects_2025_11_21")
        self.assertEqual(
            tuple(
                (field.name, field.field_type, field.mode)
                for field in loader.SCHEMA
            ),
            EXPECTED_SCHEMA,
        )

    def test_load_job_config_is_explicit_utf8_and_overwrite_safe(self) -> None:
        config = loader.build_load_job_config()

        self.assertEqual(config.source_format, bigquery.SourceFormat.CSV)
        self.assertEqual(config.skip_leading_rows, 1)
        self.assertEqual(
            config.write_disposition,
            bigquery.WriteDisposition.WRITE_EMPTY,
        )
        self.assertEqual(
            config.create_disposition,
            bigquery.CreateDisposition.CREATE_IF_NEEDED,
        )
        self.assertEqual(config.encoding, "UTF-8")
        self.assertEqual(config.field_delimiter, ",")
        self.assertEqual(config.quote_character, '"')
        self.assertFalse(config.allow_quoted_newlines)
        self.assertFalse(config.ignore_unknown_values)
        self.assertEqual(config.max_bad_records, 0)
        self.assertFalse(config.autodetect)

    def test_existing_historical_table_is_refused_before_load_submission(self) -> None:
        class ExistingTableClient:
            load_called = False

            @staticmethod
            def get_dataset(_dataset_id: str) -> SimpleNamespace:
                return SimpleNamespace(location="us-central1")

            @staticmethod
            def get_table(_table_id: str) -> SimpleNamespace:
                return SimpleNamespace()

            def load_table_from_file(self, *_args: object, **_kwargs: object) -> None:
                self.load_called = True

        client = ExistingTableClient()
        with self.assertRaisesRegex(loader.LoadValidationError, "already exists"):
            loader.load_source_universe(client=client)  # type: ignore[arg-type]

        self.assertFalse(client.load_called)

    def test_absent_table_preflight_does_not_hide_other_api_errors(self) -> None:
        class MissingTableClient:
            @staticmethod
            def get_table(_table_id: str) -> None:
                raise NotFound("table is absent")

        loader.require_target_absent(MissingTableClient())  # type: ignore[arg-type]

    def test_dataset_location_mismatch_is_refused(self) -> None:
        class WrongLocationClient:
            @staticmethod
            def get_dataset(_dataset_id: str) -> SimpleNamespace:
                return SimpleNamespace(location="US")

        with self.assertRaisesRegex(loader.LoadValidationError, "no load was started"):
            loader.require_dataset_location(WrongLocationClient())  # type: ignore[arg-type]

    def test_loaded_table_metadata_must_match_schema_location_and_count(self) -> None:
        valid_table = SimpleNamespace(
            schema=loader.SCHEMA,
            location="us-central1",
            num_rows=37,
        )
        loader.validate_loaded_table(valid_table)  # type: ignore[arg-type]

        wrong_schema = SimpleNamespace(
            schema=[bigquery.SchemaField("subproject_id", "FLOAT")],
            location="us-central1",
            num_rows=37,
        )
        with self.assertRaisesRegex(loader.LoadValidationError, "schema differs"):
            loader.validate_loaded_table(wrong_schema)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
