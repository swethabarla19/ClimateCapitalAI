from __future__ import annotations

import csv
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

from climatecapital.contracts.versions import GOVERNED_PROJECT_IDS
from scripts.data import extract_watershed_prb_scores


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

SOURCE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "staging"
    / "raw"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "source.pdf"
)

REGISTRY_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "metadata"
    / "source_registry.csv"
)

WATERSHED_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "source_rows"
    / "watershed.json"
)

OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "watershed_prb_scores.csv"
)

EXPECTED_CHECKSUM = (
    "sha256:"
    "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359"
)

EXPECTED_COLUMNS = (
    "source_id",
    "source_pdf_page",
    "source_table_row_order",
    "canonical_project_id",
    "january_source_name",
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
    "grand_total",
)


# These score vectors were independently checked against the rendered
# January 21, 2026 PRB scoring table before this persistent test was created.
SOURCE_VERIFIED_SPOT_CHECKS = {
    1: {
        "source_pdf_page": 8,
        "canonical_project_id": "5282.134",
        "january_source_name": (
            "Walnut Creek - Tannehill Creek Bartholomew Park "
            "Stormwater Retrofit"
        ),
        "strategic_alignment": 8,
        "critical_asset": 6,
        "community_consideration": 16,
        "efficiency": 14,
        "timeliness_readiness": 18,
        "climate_resilience": 12,
        "grand_total": 74,
    },
    8: {
        "source_pdf_page": 8,
        "canonical_project_id": "5282.162",
        "january_source_name": "CapEx",
        "strategic_alignment": 8,
        "critical_asset": 7,
        "community_consideration": 12,
        "efficiency": 16,
        "timeliness_readiness": 13,
        "climate_resilience": 12,
        "grand_total": 68,
    },
    14: {
        "source_pdf_page": 9,
        "canonical_project_id": "4015.001",
        "january_source_name": (
            "Country Club Creek Metcalf & Oltorf Wastewater Improvements"
        ),
        "strategic_alignment": 8,
        "critical_asset": 6,
        "community_consideration": 16,
        "efficiency": 13,
        "timeliness_readiness": 12,
        "climate_resilience": 11,
        "grand_total": 66,
    },
    28: {
        "source_pdf_page": 9,
        "canonical_project_id": "5789.150",
        "january_source_name": "City Storm Drain Renewal Downtown",
        "strategic_alignment": 8,
        "critical_asset": 5,
        "community_consideration": 16,
        "efficiency": 12,
        "timeliness_readiness": 14,
        "climate_resilience": 5,
        "grand_total": 60,
    },
    37: {
        "source_pdf_page": 10,
        "canonical_project_id": "5848.070",
        "january_source_name": (
            "Shoal Creek - Grover Channel Stabilization"
        ),
        "strategic_alignment": 8,
        "critical_asset": 5,
        "community_consideration": 10,
        "efficiency": 8,
        "timeliness_readiness": 11,
        "climate_resilience": 10,
        "grand_total": 52,
    },
}


class WatershedPrbScoreExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.checksum = (
            extract_watershed_prb_scores.validate_source_checksum(
                SOURCE_PATH,
                REGISTRY_PATH,
            )
        )

        cls.governed_overlay = (
            extract_watershed_prb_scores.load_governed_january_overlay(
                WATERSHED_PATH
            )
        )

        cls.records = extract_watershed_prb_scores.extract_score_rows(
            SOURCE_PATH,
            cls.governed_overlay,
        )

    def test_source_checksum_is_exact_registered_snapshot(self) -> None:
        self.assertEqual(
            self.checksum,
            EXPECTED_CHECKSUM,
        )

    def test_exact_37_project_reconciliation(self) -> None:
        self.assertEqual(
            extract_watershed_prb_scores.CSV_COLUMNS,
            EXPECTED_COLUMNS,
        )

        self.assertEqual(
            len(self.records),
            37,
        )

        self.assertEqual(
            [record.source_table_row_order for record in self.records],
            list(range(1, 38)),
        )

        self.assertEqual(
            Counter(
                record.source_pdf_page
                for record in self.records
            ),
            {
                8: 12,
                9: 16,
                10: 9,
            },
        )

        canonical_ids = [
            record.canonical_project_id
            for record in self.records
        ]

        self.assertEqual(
            len(canonical_ids),
            len(set(canonical_ids)),
        )

        self.assertEqual(
            set(canonical_ids),
            set(GOVERNED_PROJECT_IDS),
        )

        self.assertEqual(
            len(
                {
                    record.january_source_name
                    for record in self.records
                }
            ),
            37,
        )

    def test_every_component_vector_sums_to_grand_total(self) -> None:
        for record in self.records:
            with self.subTest(
                canonical_project_id=record.canonical_project_id
            ):
                component_sum = (
                    record.strategic_alignment
                    + record.critical_asset
                    + record.community_consideration
                    + record.efficiency
                    + record.timeliness_readiness
                    + record.climate_resilience
                )

                self.assertEqual(
                    component_sum,
                    record.grand_total,
                )

    def test_every_grand_total_matches_existing_m3_6_overlay(self) -> None:
        for record in self.records:
            governed = self.governed_overlay[
                record.january_source_name
            ]

            with self.subTest(
                canonical_project_id=record.canonical_project_id
            ):
                self.assertEqual(
                    record.grand_total,
                    governed["grand_total"],
                )

                self.assertEqual(
                    record.canonical_project_id,
                    governed["canonical_project_id"],
                )

    def test_source_verified_spot_checks_preserve_row_associations(
        self,
    ) -> None:
        records_by_order = {
            record.source_table_row_order: record
            for record in self.records
        }

        for row_order, expected in SOURCE_VERIFIED_SPOT_CHECKS.items():
            with self.subTest(
                source_table_row_order=row_order
            ):
                record = records_by_order[row_order]

                for field, expected_value in expected.items():
                    self.assertEqual(
                        getattr(record, field),
                        expected_value,
                    )

    def test_committed_csv_is_deterministic_source_render(
        self,
    ) -> None:
        expected_bytes = (
            extract_watershed_prb_scores.render_csv(
                self.records
            )
        )

        self.assertEqual(
            OUTPUT_PATH.read_bytes(),
            expected_bytes,
        )

        with OUTPUT_PATH.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as output_file:
            reader = csv.DictReader(output_file)

            self.assertEqual(
                tuple(reader.fieldnames or ()),
                EXPECTED_COLUMNS,
            )

            rows = list(reader)

        self.assertEqual(
            len(rows),
            37,
        )

        self.assertEqual(
            rows[0]["canonical_project_id"],
            "5282.134",
        )

        self.assertEqual(
            rows[-1]["canonical_project_id"],
            "5848.070",
        )


class WatershedPrbScoreFailClosedTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.governed_overlay = (
            extract_watershed_prb_scores.load_governed_january_overlay(
                WATERSHED_PATH
            )
        )

        cls.records = extract_watershed_prb_scores.extract_score_rows(
            SOURCE_PATH,
            cls.governed_overlay,
        )

    def test_changed_source_bytes_fail_checksum_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_source = (
                Path(temporary_directory)
                / "source.pdf"
            )

            changed_source.write_bytes(
                SOURCE_PATH.read_bytes()
                + b"\nchanged"
            )

            with self.assertRaisesRegex(
                extract_watershed_prb_scores.ExtractionError,
                "Source checksum mismatch",
            ):
                extract_watershed_prb_scores.validate_source_checksum(
                    changed_source,
                    REGISTRY_PATH,
                )

    def test_source_role_change_fails_m3_7a_authority_boundary(
        self,
    ) -> None:
        with REGISTRY_PATH.open(
            "r",
            encoding="utf-8",
            newline="",
        ) as registry_file:
            reader = csv.DictReader(registry_file)
            fieldnames = list(reader.fieldnames or ())
            rows = list(reader)

        for row in rows:
            if row["source_id"] == extract_watershed_prb_scores.SOURCE_ID:
                row["analytical_role"] = "analytical"

        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_registry = (
                Path(temporary_directory)
                / "source_registry.csv"
            )

            with changed_registry.open(
                "w",
                encoding="utf-8",
                newline="",
            ) as output_file:
                writer = csv.DictWriter(
                    output_file,
                    fieldnames=fieldnames,
                )
                writer.writeheader()
                writer.writerows(rows)

            with self.assertRaisesRegex(
                extract_watershed_prb_scores.ExtractionError,
                "analytical_role changed unexpectedly",
            ):
                extract_watershed_prb_scores.load_registered_source(
                    changed_registry
                )

    def test_governed_grand_total_conflict_fails_reconciliation(
        self,
    ) -> None:
        rows = json.loads(
            WATERSHED_PATH.read_text(
                encoding="utf-8"
            )
        )

        target = next(
            row
            for row in rows
            if row.get("canonical_project_id") == "5282.134"
        )

        target["prb_score"] = 73

        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_watershed = (
                Path(temporary_directory)
                / "watershed.json"
            )

            changed_watershed.write_text(
                json.dumps(rows),
                encoding="utf-8",
            )

            changed_overlay = (
                extract_watershed_prb_scores.load_governed_january_overlay(
                    changed_watershed
                )
            )

            with self.assertRaisesRegex(
                extract_watershed_prb_scores.ExtractionError,
                "Grand Total mismatch",
            ):
                extract_watershed_prb_scores.extract_score_rows(
                    SOURCE_PATH,
                    changed_overlay,
                )

    def test_different_existing_artifact_is_not_overwritten(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = (
                Path(temporary_directory)
                / "watershed_prb_scores.csv"
            )

            original = b"different derived artifact\n"

            output_path.write_bytes(original)

            with self.assertRaisesRegex(
                extract_watershed_prb_scores.DerivedArtifactConflictError,
                "Refusing to overwrite differing derived artifact",
            ):
                extract_watershed_prb_scores.write_artifact(
                    output_path,
                    self.records,
                )

            self.assertEqual(
                output_path.read_bytes(),
                original,
            )


if __name__ == "__main__":
    unittest.main()
