from __future__ import annotations

import csv
import io
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from scripts.data import extract_watershed_projects


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "staging"
    / "raw"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "source.pdf"
)
REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "projects.csv"
)

EXPECTED_COLUMNS = (
    "source_id",
    "source_pdf_page",
    "source_table_row_order",
    "map_label",
    "subproject_id",
    "project_name",
    "current_funding_request_estimate_source",
    "current_funding_request_estimate_dollars",
    "council_districts_source",
)

# These expectations were transcribed from visual inspection of the rendered
# source table, independently of the extraction implementation.
SOURCE_VERIFIED_SPOT_CHECKS = {
    1: {
        "source_pdf_page": 4,
        "map_label": "A",
        "subproject_id": "4015.001",
        "project_name": (
            "Country Club Creek (Between Metcalfe & Oltorf) "
            "Wastewater Improvements"
        ),
        "current_funding_request_estimate_source": "$5,470,000",
        "current_funding_request_estimate_dollars": 5_470_000,
        "council_districts_source": "3",
    },
    19: {
        "source_pdf_page": 4,
        "map_label": "S",
        "subproject_id": "5789.141",
        "project_name": "Boggy Creek - Oakwood Cemetery Storm Drain Improvements",
        "current_funding_request_estimate_source": "$7,350,000",
        "current_funding_request_estimate_dollars": 7_350_000,
        "council_districts_source": "1",
    },
    20: {
        "source_pdf_page": 5,
        "map_label": "T",
        "subproject_id": "5789.150",
        "project_name": (
            "Lady Bird Lake – Citywide Storm Drain Renewal Program – Phase 1"
        ),
        "current_funding_request_estimate_source": "$3,000,000",
        "current_funding_request_estimate_dollars": 3_000_000,
        "council_districts_source": "9",
    },
    29: {
        "source_pdf_page": 5,
        "map_label": "AC",
        "subproject_id": "6039.109",
        "project_name": "Shoal Creek - Brentwood Integrated Drainage Improvements",
        "current_funding_request_estimate_source": "$33,500,000",
        "current_funding_request_estimate_dollars": 33_500_000,
        "council_districts_source": "4,7,9",
    },
    37: {
        "source_pdf_page": 5,
        "map_label": "AK",
        "subproject_id": "11889.004",
        "project_name": (
            "William Cannon Drive Corridor - US 290 to East of Brodie Ln"
        ),
        "current_funding_request_estimate_source": "$2,625,000",
        "current_funding_request_estimate_dollars": 2_625_000,
        "council_districts_source": "5,8",
    },
}


class CanonicalSourceUniverseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = extract_watershed_projects.extract_source_universe(
            source_path=SOURCE_PATH,
            registry_path=REGISTRY_PATH,
        )

    def test_schema_count_and_independently_reconciled_total(self) -> None:
        self.assertEqual(extract_watershed_projects.CSV_COLUMNS, EXPECTED_COLUMNS)
        self.assertEqual(len(self.result.records), 37)
        self.assertEqual(
            sum(
                record.current_funding_request_estimate_dollars
                for record in self.result.records
            ),
            327_970_000,
        )
        self.assertEqual(self.result.table_total_dollars, 327_970_000)
        self.assertEqual(self.result.memo_program_request_dollars, 327_970_000)
        self.assertEqual(
            [record.source_table_row_order for record in self.result.records],
            list(range(1, 38)),
        )
        self.assertEqual(
            {record.source_pdf_page for record in self.result.records},
            {4, 5},
        )
        self.assertEqual(
            len({record.map_label for record in self.result.records}),
            37,
        )
        self.assertEqual(
            len({record.subproject_id for record in self.result.records}),
            37,
        )
        self.assertTrue(
            all(isinstance(record.subproject_id, str) for record in self.result.records)
        )
        for record in self.result.records:
            source_dollars = int(
                record.current_funding_request_estimate_source.removeprefix("$").replace(
                    ",", ""
                )
            )
            self.assertEqual(
                source_dollars,
                record.current_funding_request_estimate_dollars,
            )

    def test_source_verified_spot_checks_preserve_row_associations(self) -> None:
        records_by_order = {
            record.source_table_row_order: record for record in self.result.records
        }

        for row_order, expected in SOURCE_VERIFIED_SPOT_CHECKS.items():
            with self.subTest(source_table_row_order=row_order):
                record = records_by_order[row_order]
                for field, value in expected.items():
                    self.assertEqual(getattr(record, field), value)

    def test_source_order_anomaly_is_preserved_without_sorting(self) -> None:
        observed = [
            (record.source_table_row_order, record.map_label, record.subproject_id)
            for record in self.result.records[19:22]
        ]
        self.assertEqual(
            observed,
            [
                (20, "T", "5789.150"),
                (21, "U", "5789.145"),
                (22, "V", "5789.146"),
            ],
        )

    def test_committed_csv_is_a_deterministic_render_of_the_source(self) -> None:
        expected_bytes = extract_watershed_projects.render_csv(self.result.records)
        self.assertEqual(OUTPUT_PATH.read_bytes(), expected_bytes)

        with OUTPUT_PATH.open("r", encoding="utf-8", newline="") as output_file:
            reader = csv.DictReader(output_file)
            self.assertEqual(tuple(reader.fieldnames or ()), EXPECTED_COLUMNS)
            rows = list(reader)

        self.assertEqual(len(rows), 37)
        self.assertEqual(rows[0]["subproject_id"], "4015.001")
        self.assertEqual(rows[-1]["subproject_id"], "11889.004")


class FailClosedExtractionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.pages = extract_watershed_projects.read_pdf_pages(SOURCE_PATH)

    def _replace_page_text(
        self, physical_page_number: int, old: str, new: str
    ) -> tuple[extract_watershed_projects.PdfPageText, ...]:
        changed = []
        for page in self.pages:
            if page.physical_page_number == physical_page_number:
                self.assertIn(old, page.text)
                page = replace(page, text=page.text.replace(old, new, 1))
            changed.append(page)
        return tuple(changed)

    def test_registered_checksum_mismatch_fails_before_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            changed_source = Path(temporary_directory) / "source.pdf"
            changed_source.write_bytes(SOURCE_PATH.read_bytes() + b"\nchanged")

            with self.assertRaisesRegex(
                extract_watershed_projects.ExtractionError,
                "checksum does not match",
            ):
                extract_watershed_projects.extract_source_universe(
                    source_path=changed_source,
                    registry_path=REGISTRY_PATH,
                )

    def test_missing_required_table_anchor_fails_clearly(self) -> None:
        pages = self._replace_page_text(
            4,
            "Table - Page 1 of 2",
            "Table page marker unavailable",
        )
        with self.assertRaisesRegex(
            extract_watershed_projects.ExtractionError,
            "(?i)required table anchor",
        ):
            extract_watershed_projects.parse_source_pages(pages)

    def test_unidentified_expected_columns_fail_clearly(self) -> None:
        pages = self._replace_page_text(4, "Council \nDistrict", "Council \nArea")
        with self.assertRaisesRegex(
            extract_watershed_projects.ExtractionError,
            "expected table columns",
        ):
            extract_watershed_projects.parse_source_pages(pages)

    def test_unparseable_row_fails_without_cross_row_association(self) -> None:
        pages = self._replace_page_text(4, "$5,470,000 3", "$5,470,000 unknown")
        with self.assertRaisesRegex(
            extract_watershed_projects.ExtractionError,
            "could not be parsed losslessly",
        ):
            extract_watershed_projects.parse_source_pages(pages)

    def test_missing_table_total_fails_clearly(self) -> None:
        pages = self._replace_page_text(
            5,
            "Total $327,970,000",
            "Aggregate $327,970,000",
        )
        with self.assertRaisesRegex(
            extract_watershed_projects.ExtractionError,
            "table total",
        ):
            extract_watershed_projects.parse_source_pages(pages)

    def test_existing_different_derived_artifact_is_not_overwritten(self) -> None:
        records = extract_watershed_projects.parse_source_pages(self.pages).records
        with tempfile.TemporaryDirectory() as temporary_directory:
            output_path = Path(temporary_directory) / "projects.csv"
            original = b"different derived artifact\n"
            output_path.write_bytes(original)

            with self.assertRaisesRegex(
                extract_watershed_projects.DerivedArtifactConflictError,
                "different bytes",
            ):
                extract_watershed_projects.write_extraction(output_path, records)

            self.assertEqual(output_path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
