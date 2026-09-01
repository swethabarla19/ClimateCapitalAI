#!/usr/bin/env python3
"""Create the immutable raw BigQuery copy of the Watershed source universe."""

from __future__ import annotations

import csv
import hashlib
import io
import re
import sys
from dataclasses import dataclass
from pathlib import Path

from google.api_core.exceptions import GoogleAPIError, NotFound
from google.cloud import bigquery


PROJECT_ID = "climatecapital-ai"
DATASET_ID = "raw"
TABLE_ID = "watershed_projects_2025_11_21"
LOCATION = "us-central1"
SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
EXPECTED_ROW_COUNT = 37
EXPECTED_FUNDING_TOTAL = 327_970_000
EXPECTED_CSV_SHA256 = (
    "sha256:051735b15dca7333a03d7f1b61edd24c2f306935c841e564492100d4d9c5afba"
)

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CSV_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "projects.csv"
)
FULL_TABLE_ID = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"

SCHEMA = [
    bigquery.SchemaField("source_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("source_pdf_page", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("source_table_row_order", "INTEGER", mode="REQUIRED"),
    bigquery.SchemaField("map_label", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("subproject_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("project_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField(
        "current_funding_request_estimate_source",
        "STRING",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "current_funding_request_estimate_dollars",
        "INTEGER",
        mode="REQUIRED",
    ),
    bigquery.SchemaField(
        "council_districts_source",
        "STRING",
        mode="REQUIRED",
    ),
]
CSV_COLUMNS = tuple(field.name for field in SCHEMA)
EXPECTED_MAP_LABELS = tuple(
    [chr(ord("A") + index) for index in range(26)]
    + ["A" + chr(ord("A") + index) for index in range(11)]
)
FUNDING_SOURCE_PATTERN = re.compile(r"^\$[0-9]{1,3}(?:,[0-9]{3})+$")
COUNCIL_DISTRICTS_PATTERN = re.compile(r"^(?:[1-9]|10)(?:,(?:[1-9]|10))*$")


class LoadValidationError(RuntimeError):
    """Raised when a safe, source-faithful load cannot be guaranteed."""


@dataclass(frozen=True)
class SourceCsvSummary:
    checksum: str
    row_count: int
    funding_total_dollars: int


def _sha256_bytes(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _parse_required_integer(row: dict[str, str], field: str, row_number: int) -> int:
    value = row[field]
    if not value.isdigit():
        raise LoadValidationError(
            f"CSV row {row_number} field {field!r} is not an unsigned integer: "
            f"{value!r}."
        )
    return int(value)


def validate_csv_content(content: bytes) -> SourceCsvSummary:
    """Validate the governed CSV contract before any BigQuery API call."""

    checksum = _sha256_bytes(content)
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise LoadValidationError("Source artifact is not valid UTF-8.") from error

    try:
        reader = csv.DictReader(io.StringIO(text, newline=""))
        if tuple(reader.fieldnames or ()) != CSV_COLUMNS:
            raise LoadValidationError(
                "Source artifact columns do not match the governed schema order: "
                f"expected {CSV_COLUMNS!r}; found {tuple(reader.fieldnames or ())!r}."
            )
        rows = list(reader)
    except csv.Error as error:
        raise LoadValidationError(f"Source artifact is not valid CSV: {error}") from error

    if len(rows) != EXPECTED_ROW_COUNT:
        raise LoadValidationError(
            f"Expected {EXPECTED_ROW_COUNT} source rows; found {len(rows)}."
        )

    row_orders: list[int] = []
    map_labels: list[str] = []
    subproject_ids: list[str] = []
    pages: list[int] = []
    funding_total = 0

    for row_number, row in enumerate(rows, start=2):
        if None in row:
            raise LoadValidationError(
                f"CSV row {row_number} has more fields than the governed header."
            )
        empty_fields = [field for field in CSV_COLUMNS if not row.get(field)]
        if empty_fields:
            raise LoadValidationError(
                f"CSV row {row_number} has empty governed fields: "
                + ", ".join(empty_fields)
            )
        if row["source_id"] != SOURCE_ID:
            raise LoadValidationError(
                f"CSV row {row_number} has unexpected source_id "
                f"{row['source_id']!r}."
            )

        page = _parse_required_integer(row, "source_pdf_page", row_number)
        row_order = _parse_required_integer(
            row, "source_table_row_order", row_number
        )
        funding_dollars = _parse_required_integer(
            row, "current_funding_request_estimate_dollars", row_number
        )
        funding_source = row["current_funding_request_estimate_source"]
        if not FUNDING_SOURCE_PATTERN.fullmatch(funding_source):
            raise LoadValidationError(
                f"CSV row {row_number} has invalid source currency text "
                f"{funding_source!r}."
            )
        parsed_source_dollars = int(funding_source[1:].replace(",", ""))
        if parsed_source_dollars != funding_dollars:
            raise LoadValidationError(
                f"CSV row {row_number} source currency text does not reconcile "
                "to its normalized dollar value."
            )
        districts = row["council_districts_source"]
        if not COUNCIL_DISTRICTS_PATTERN.fullmatch(districts):
            raise LoadValidationError(
                f"CSV row {row_number} has invalid council-district source text "
                f"{districts!r}."
            )

        pages.append(page)
        row_orders.append(row_order)
        map_labels.append(row["map_label"])
        subproject_ids.append(row["subproject_id"])
        funding_total += funding_dollars

    if row_orders != list(range(1, EXPECTED_ROW_COUNT + 1)):
        raise LoadValidationError(
            "source_table_row_order must be the contiguous published order 1–37."
        )
    if tuple(map_labels) != EXPECTED_MAP_LABELS:
        raise LoadValidationError("map_label must preserve the published A–AK order.")
    if len(set(subproject_ids)) != EXPECTED_ROW_COUNT:
        raise LoadValidationError("subproject_id values must be unique strings.")
    if pages.count(4) != 19 or pages.count(5) != 18 or set(pages) != {4, 5}:
        raise LoadValidationError(
            "source_pdf_page must contain 19 rows from page 4 and 18 from page 5."
        )
    if funding_total != EXPECTED_FUNDING_TOTAL:
        raise LoadValidationError(
            "Normalized funding requests do not reconcile to the governed total: "
            f"expected ${EXPECTED_FUNDING_TOTAL:,}; found ${funding_total:,}."
        )

    return SourceCsvSummary(
        checksum=checksum,
        row_count=len(rows),
        funding_total_dollars=funding_total,
    )


def validate_source_csv(path: Path = CSV_PATH) -> SourceCsvSummary:
    """Require the exact reviewed historical CSV before loading it."""

    try:
        content = path.read_bytes()
    except OSError as error:
        raise LoadValidationError(f"Unable to read source artifact {path}: {error}") from error

    summary = validate_csv_content(content)
    if summary.checksum != EXPECTED_CSV_SHA256:
        raise LoadValidationError(
            "Source artifact checksum does not match the reviewed historical CSV: "
            f"expected {EXPECTED_CSV_SHA256}; found {summary.checksum}."
        )
    return summary


def build_load_job_config() -> bigquery.LoadJobConfig:
    """Return the explicit, create-only CSV load contract."""

    return bigquery.LoadJobConfig(
        schema=SCHEMA,
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition=bigquery.WriteDisposition.WRITE_EMPTY,
        create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
        encoding="UTF-8",
        field_delimiter=",",
        quote_character='"',
        allow_quoted_newlines=False,
        ignore_unknown_values=False,
        max_bad_records=0,
        autodetect=False,
    )


def require_dataset_location(client: bigquery.Client) -> None:
    dataset = client.get_dataset(f"{PROJECT_ID}.{DATASET_ID}")
    if dataset.location.lower() != LOCATION.lower():
        raise LoadValidationError(
            f"Dataset {PROJECT_ID}.{DATASET_ID} is in {dataset.location!r}, not "
            f"the required {LOCATION!r}; no load was started."
        )


def require_target_absent(client: bigquery.Client) -> None:
    """Refuse a rerun before submitting a load; WRITE_EMPTY closes the race window."""

    try:
        client.get_table(FULL_TABLE_ID)
    except NotFound:
        return
    raise LoadValidationError(
        f"Target table {FULL_TABLE_ID} already exists; no load was started. "
        "Validate the existing historical table instead of overwriting it."
    )


def validate_loaded_table(table: bigquery.Table) -> None:
    expected_schema = [
        (field.name, field.field_type, field.mode) for field in SCHEMA
    ]
    actual_schema = [
        (field.name, field.field_type, field.mode) for field in table.schema
    ]
    if actual_schema != expected_schema:
        raise LoadValidationError(
            "Created table schema differs from the governed schema: "
            f"expected {expected_schema!r}; found {actual_schema!r}."
        )
    if table.location.lower() != LOCATION.lower():
        raise LoadValidationError(
            f"Created table is in {table.location!r}, not {LOCATION!r}."
        )
    if table.num_rows != EXPECTED_ROW_COUNT:
        raise LoadValidationError(
            f"Created table has {table.num_rows} rows; expected {EXPECTED_ROW_COUNT}."
        )


def load_source_universe(
    client: bigquery.Client | None = None,
    csv_path: Path = CSV_PATH,
) -> tuple[SourceCsvSummary, bigquery.Table]:
    """Validate locally, then create and verify the immutable raw table."""

    summary = validate_source_csv(csv_path)
    client = client or bigquery.Client(project=PROJECT_ID)
    require_dataset_location(client)
    require_target_absent(client)

    with csv_path.open("rb") as source_file:
        load_job = client.load_table_from_file(
            source_file,
            FULL_TABLE_ID,
            job_config=build_load_job_config(),
            location=LOCATION,
        )
    load_job.result()

    table = client.get_table(FULL_TABLE_ID)
    validate_loaded_table(table)
    return summary, table


def main() -> int:
    try:
        summary, table = load_source_universe()
    except (LoadValidationError, GoogleAPIError, OSError) as error:
        print("FAILURE: Watershed raw BigQuery load", file=sys.stderr)
        print(f"  {error}", file=sys.stderr)
        return 1

    print("SUCCESS: Watershed raw BigQuery load")
    print(f"  Loaded table: {FULL_TABLE_ID}")
    print(f"  Location: {table.location}")
    print(f"  Rows: {table.num_rows}")
    print(f"  Funding total validated before load: ${summary.funding_total_dollars:,}")
    print(f"  Source artifact checksum: {summary.checksum}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
