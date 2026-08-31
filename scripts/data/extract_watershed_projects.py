#!/usr/bin/env python3
"""Extract the governed November 2025 Watershed project source universe."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError as error:  # pragma: no cover - exercised by the CLI environment.
    PdfReader = None  # type: ignore[assignment,misc]
    PdfReadError = Exception  # type: ignore[assignment,misc]
    PYPDF_IMPORT_ERROR: ImportError | None = error
else:
    PYPDF_IMPORT_ERROR = None


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
DEFAULT_REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
DEFAULT_SOURCE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "staging"
    / "raw"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "source.pdf"
)
DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "projects.csv"
)

CSV_COLUMNS = (
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

EXPECTED_RECORD_COUNT = 37
TABLE_PAGE_MARKERS = ("Table - Page 1 of 2", "Table - Page 2 of 2")
TABLE_TITLE = "2026 Bond Austin Watershed Protection Potential Projects"
EXPECTED_TABLE_HEADER = (
    "Map Label Subproject ID Project Name Current Funding Request Estimate "
    "Council District"
)
MEMO_PROGRAM_ANCHOR = (
    "Strategic Plan Identified Drainage & Stormwater Infrastructure Projects"
)
MEMO_NEXT_PROGRAM_ANCHOR = "Stormwater Resilience Program"

CURRENCY_PATTERN_TEXT = r"\$[0-9]{1,3}(?:,[0-9]{3})+"
CURRENCY_PATTERN = re.compile(CURRENCY_PATTERN_TEXT)
CHECKSUM_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
ROW_START_PATTERN = re.compile(
    r"(?m)^(?P<map_label>[A-Z]{1,2})[ \t]+"
    r"(?P<subproject_id>[0-9]+\.[0-9]{3})[ \t]+"
)
ROW_PATTERN = re.compile(
    rf"^(?P<map_label>[A-Z]{{1,2}}) "
    rf"(?P<subproject_id>[0-9]+\.[0-9]{{3}}) "
    rf"(?P<project_name>.+?) "
    rf"(?P<currency>{CURRENCY_PATTERN_TEXT}) "
    rf"(?P<council_districts>[0-9]+(?:,[0-9]+)*)$"
)


class ExtractionError(RuntimeError):
    """Raised when source extraction cannot proceed without guessing."""


class DerivedArtifactConflictError(ExtractionError):
    """Raised when a differing derived artifact would be overwritten."""


@dataclass(frozen=True)
class PdfPageText:
    """Extracted text paired with its 1-based physical PDF page number."""

    physical_page_number: int
    text: str


@dataclass(frozen=True)
class ProjectRecord:
    source_id: str
    source_pdf_page: int
    source_table_row_order: int
    map_label: str
    subproject_id: str
    project_name: str
    current_funding_request_estimate_source: str
    current_funding_request_estimate_dollars: int
    council_districts_source: str


@dataclass(frozen=True)
class ExtractionResult:
    records: tuple[ProjectRecord, ...]
    table_total_dollars: int
    memo_program_request_dollars: int


@dataclass(frozen=True)
class ParsedTableRow:
    source_pdf_page: int
    map_label: str
    subproject_id: str
    project_name: str
    funding_source: str
    funding_dollars: int
    council_districts_source: str


def _normalize_extracted_whitespace(value: str) -> str:
    """Collapse only PDF-extraction whitespace; preserve all visible characters."""

    return re.sub(r"\s+", " ", value).strip()


def _sha256_checksum(path: Path) -> str:
    digest = hashlib.sha256()
    try:
        with path.open("rb") as source_file:
            for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError as error:
        raise ExtractionError(f"Unable to read source PDF {path}: {error}") from error
    return "sha256:" + digest.hexdigest()


def _load_registered_source(registry_path: Path) -> dict[str, str]:
    try:
        with registry_path.open("r", encoding="utf-8", newline="") as registry_file:
            reader = csv.DictReader(registry_file)
            required_columns = {
                "source_id",
                "checksum",
                "format",
                "historical_fit",
                "analytical_role",
            }
            columns = set(reader.fieldnames or ())
            missing = sorted(required_columns - columns)
            if missing:
                raise ExtractionError(
                    f"Source registry {registry_path} is missing required columns: "
                    + ", ".join(missing)
                )
            matches = [row for row in reader if row.get("source_id") == SOURCE_ID]
    except OSError as error:
        raise ExtractionError(
            f"Unable to read source registry {registry_path}: {error}"
        ) from error

    if len(matches) != 1:
        raise ExtractionError(
            f"Expected exactly one registry row for {SOURCE_ID!r}; found {len(matches)}."
        )

    source = matches[0]
    if source["format"] != "PDF":
        raise ExtractionError(
            f"Registered source {SOURCE_ID!r} must have format 'PDF'; "
            f"found {source['format']!r}."
        )
    if source["historical_fit"] != "valid":
        raise ExtractionError(
            f"Registered source {SOURCE_ID!r} must have historical_fit 'valid'; "
            f"found {source['historical_fit']!r}."
        )
    if source["analytical_role"] != "analytical":
        raise ExtractionError(
            f"Registered source {SOURCE_ID!r} must have analytical_role "
            f"'analytical'; found {source['analytical_role']!r}."
        )
    if not CHECKSUM_PATTERN.fullmatch(source["checksum"]):
        raise ExtractionError(
            f"Registered source {SOURCE_ID!r} has no valid SHA-256 checksum."
        )
    return source


def validate_source_checksum(
    source_path: Path, registry_path: Path = DEFAULT_REGISTRY_PATH
) -> str:
    """Require the local PDF bytes to match the registered governed snapshot."""

    source = _load_registered_source(registry_path)
    actual = _sha256_checksum(source_path)
    expected = source["checksum"]
    if actual != expected:
        raise ExtractionError(
            f"Source checksum does not match the registry for {SOURCE_ID!r}: "
            f"expected {expected}; found {actual}. Extraction stopped."
        )
    return actual


def read_pdf_pages(source_path: Path) -> tuple[PdfPageText, ...]:
    """Extract every page's text and retain 1-based physical page numbers."""

    if PYPDF_IMPORT_ERROR is not None or PdfReader is None:
        raise ExtractionError(
            "pypdf is required for source extraction. Install requirements-data.txt "
            "in an isolated local environment."
        ) from PYPDF_IMPORT_ERROR

    try:
        reader = PdfReader(source_path)
        pages = tuple(
            PdfPageText(
                physical_page_number=index,
                text=page.extract_text() or "",
            )
            for index, page in enumerate(reader.pages, start=1)
        )
    except (OSError, PdfReadError) as error:
        raise ExtractionError(f"Unable to parse source PDF {source_path}: {error}") from error

    if not pages:
        raise ExtractionError(f"Source PDF {source_path} contains no pages.")
    if any(not page.text.strip() for page in pages):
        empty_pages = [
            str(page.physical_page_number) for page in pages if not page.text.strip()
        ]
        raise ExtractionError(
            "Source PDF contains page(s) without extractable text: "
            + ", ".join(empty_pages)
            + ". Extraction stopped rather than guessing or using OCR."
        )
    return pages


def _find_unique_page(
    pages: Sequence[PdfPageText], marker: str
) -> PdfPageText:
    matches = [page for page in pages if marker in page.text]
    if len(matches) != 1:
        raise ExtractionError(
            f"Required table anchor {marker!r} must occur on exactly one PDF page; "
            f"found {len(matches)}."
        )
    return matches[0]


def _parse_currency(currency: str, context: str) -> int:
    if not CURRENCY_PATTERN.fullmatch(currency):
        raise ExtractionError(
            f"{context}: currency value {currency!r} is not losslessly parseable."
        )
    return int(currency.removeprefix("$").replace(",", ""))


def _parse_memo_program_request(pages: Sequence[PdfPageText]) -> int:
    first_page = next(
        (page for page in pages if page.physical_page_number == 1), None
    )
    if first_page is None:
        raise ExtractionError("Required physical PDF page 1 is absent.")

    text = _normalize_extracted_whitespace(first_page.text)
    start = text.find(MEMO_PROGRAM_ANCHOR)
    end = text.find(MEMO_NEXT_PROGRAM_ANCHOR, start + len(MEMO_PROGRAM_ANCHOR))
    if start < 0 or end < 0:
        raise ExtractionError(
            "Required memorandum program anchors are absent; the program request "
            "cannot be reconciled safely."
        )
    segment = text[start:end]
    currencies = CURRENCY_PATTERN.findall(segment)
    if len(currencies) != 1:
        raise ExtractionError(
            "The memorandum program request could not be identified unambiguously; "
            f"found {len(currencies)} currency values in the anchored program block."
        )
    return _parse_currency(currencies[0], "Memorandum program request")


def _require_expected_columns(page: PdfPageText, table_page: int) -> None:
    normalized = _normalize_extracted_whitespace(page.text)
    if EXPECTED_TABLE_HEADER not in normalized:
        raise ExtractionError(
            f"Table page {table_page} on physical PDF page "
            f"{page.physical_page_number} does not contain the expected table "
            "columns in an identifiable order."
        )


def _parse_table_total(table_page_two: PdfPageText) -> int:
    pattern = re.compile(
        rf"(?m)^Total[ \t]+(?P<currency>{CURRENCY_PATTERN_TEXT})[ \t]*$"
    )
    matches = list(pattern.finditer(table_page_two.text))
    if len(matches) != 1:
        raise ExtractionError(
            "The table total could not be independently parsed exactly once from "
            f"physical PDF page {table_page_two.physical_page_number}; "
            f"found {len(matches)} matches."
        )
    return _parse_currency(matches[0].group("currency"), "Table total")


def _table_body(page: PdfPageText, table_page: int) -> str:
    starts = list(ROW_START_PATTERN.finditer(page.text))
    if not starts:
        raise ExtractionError(
            f"Table page {table_page} on physical PDF page "
            f"{page.physical_page_number} contains no identifiable project rows."
        )
    start = starts[0].start()
    if table_page == 1:
        end = page.text.find("\nDate:", start)
        if end < 0:
            raise ExtractionError(
                "Required table-page footer anchor is absent from physical PDF "
                f"page {page.physical_page_number}."
            )
    else:
        total_match = re.search(r"(?m)^Total[ \t]+", page.text[start:])
        if total_match is None:
            raise ExtractionError(
                "The table total boundary is absent from physical PDF page "
                f"{page.physical_page_number}."
            )
        end = start + total_match.start()
    return page.text[start:end].strip()


def _parse_table_rows(page: PdfPageText, table_page: int) -> list[ParsedTableRow]:
    body = _table_body(page, table_page)
    row_starts = list(ROW_START_PATTERN.finditer(body))
    parsed: list[ParsedTableRow] = []

    for index, row_start in enumerate(row_starts):
        block_end = (
            row_starts[index + 1].start()
            if index + 1 < len(row_starts)
            else len(body)
        )
        block = _normalize_extracted_whitespace(body[row_start.start() : block_end])
        currencies = CURRENCY_PATTERN.findall(block)
        match = ROW_PATTERN.fullmatch(block)
        if len(currencies) != 1 or match is None:
            label = row_start.group("map_label")
            subproject_id = row_start.group("subproject_id")
            raise ExtractionError(
                f"Project row {label} / {subproject_id} on physical PDF page "
                f"{page.physical_page_number} could not be parsed losslessly; "
                "extraction stopped before associating fields across rows."
            )

        funding_source = match.group("currency")
        parsed.append(
            ParsedTableRow(
                source_pdf_page=page.physical_page_number,
                map_label=match.group("map_label"),
                subproject_id=match.group("subproject_id"),
                project_name=match.group("project_name"),
                funding_source=funding_source,
                funding_dollars=_parse_currency(
                    funding_source,
                    f"Project row {match.group('map_label')}",
                ),
                council_districts_source=match.group("council_districts"),
            )
        )
    return parsed


def _spreadsheet_label(one_based_index: int) -> str:
    label = ""
    value = one_based_index
    while value:
        value, remainder = divmod(value - 1, 26)
        label = chr(ord("A") + remainder) + label
    return label


def _validate_records(records: Sequence[ProjectRecord]) -> None:
    if len(records) != EXPECTED_RECORD_COUNT:
        raise ExtractionError(
            f"Expected {EXPECTED_RECORD_COUNT} independently verified source rows; "
            f"extracted {len(records)}."
        )

    labels = [record.map_label for record in records]
    expected_labels = [
        _spreadsheet_label(index) for index in range(1, EXPECTED_RECORD_COUNT + 1)
    ]
    if labels != expected_labels:
        raise ExtractionError(
            "Map labels do not match the independently verified published A–AK "
            "source sequence."
        )
    if len(set(labels)) != len(labels):
        raise ExtractionError("Extracted map labels are not unique.")

    subproject_ids = [record.subproject_id for record in records]
    if len(set(subproject_ids)) != len(subproject_ids):
        raise ExtractionError("Extracted subproject IDs are not unique.")
    if any(not isinstance(subproject_id, str) for subproject_id in subproject_ids):
        raise ExtractionError("Every official subproject ID must remain a string.")

    for record in records:
        districts = record.council_districts_source.split(",")
        if len(districts) != len(set(districts)):
            raise ExtractionError(
                f"Project row {record.map_label} repeats a council district."
            )
        if any(not district.isdigit() or not 1 <= int(district) <= 10 for district in districts):
            raise ExtractionError(
                f"Project row {record.map_label} has an invalid council-district "
                f"source value {record.council_districts_source!r}."
            )
        if record.current_funding_request_estimate_dollars <= 0:
            raise ExtractionError(
                f"Project row {record.map_label} has a non-positive funding request."
            )


def parse_source_pages(pages: Sequence[PdfPageText]) -> ExtractionResult:
    """Parse and reconcile the source universe from extracted PDF page text."""

    table_page_one = _find_unique_page(pages, TABLE_PAGE_MARKERS[0])
    table_page_two = _find_unique_page(pages, TABLE_PAGE_MARKERS[1])
    if table_page_one.physical_page_number >= table_page_two.physical_page_number:
        raise ExtractionError("Required table pages are not in published source order.")
    if TABLE_TITLE not in table_page_one.text:
        raise ExtractionError(
            f"Required table anchor {TABLE_TITLE!r} is absent from table page 1."
        )

    _require_expected_columns(table_page_one, table_page=1)
    _require_expected_columns(table_page_two, table_page=2)
    table_total = _parse_table_total(table_page_two)
    memo_program_request = _parse_memo_program_request(pages)

    parsed_rows = [
        *_parse_table_rows(table_page_one, table_page=1),
        *_parse_table_rows(table_page_two, table_page=2),
    ]
    records = tuple(
        ProjectRecord(
            source_id=SOURCE_ID,
            source_pdf_page=row.source_pdf_page,
            source_table_row_order=index,
            map_label=row.map_label,
            subproject_id=row.subproject_id,
            project_name=row.project_name,
            current_funding_request_estimate_source=row.funding_source,
            current_funding_request_estimate_dollars=row.funding_dollars,
            council_districts_source=row.council_districts_source,
        )
        for index, row in enumerate(parsed_rows, start=1)
    )
    _validate_records(records)

    calculated_total = sum(
        record.current_funding_request_estimate_dollars for record in records
    )
    if calculated_total != table_total:
        raise ExtractionError(
            "Extracted project requests do not reconcile to the independently "
            f"parsed table total: rows sum to ${calculated_total:,}; table states "
            f"${table_total:,}."
        )
    if table_total != memo_program_request:
        raise ExtractionError(
            "The table total does not reconcile to the memorandum program request: "
            f"table states ${table_total:,}; memorandum states "
            f"${memo_program_request:,}."
        )

    return ExtractionResult(
        records=records,
        table_total_dollars=table_total,
        memo_program_request_dollars=memo_program_request,
    )


def extract_source_universe(
    source_path: Path = DEFAULT_SOURCE_PATH,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
) -> ExtractionResult:
    """Verify the governed source snapshot, then parse its project universe."""

    validate_source_checksum(source_path, registry_path)
    return parse_source_pages(read_pdf_pages(source_path))


def render_csv(records: Sequence[ProjectRecord]) -> bytes:
    """Render deterministic UTF-8 CSV bytes in the governed schema order."""

    output = io.StringIO(newline="")
    writer = csv.DictWriter(
        output,
        fieldnames=list(CSV_COLUMNS),
        lineterminator="\n",
    )
    writer.writeheader()
    for record in records:
        writer.writerow(asdict(record))
    return output.getvalue().encode("utf-8")


def write_extraction(destination: Path, records: Sequence[ProjectRecord]) -> str:
    """Create a derived artifact once, or report identical existing bytes."""

    content = render_csv(records)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        existing = destination.read_bytes()
        if existing == content:
            return "identical"
        raise DerivedArtifactConflictError(
            f"Derived artifact already exists with different bytes: {destination}. "
            "The existing artifact was not overwritten."
        )

    temporary_path = destination.with_name(destination.name + ".tmp")
    try:
        with temporary_path.open("xb") as temporary_file:
            temporary_file.write(content)
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        try:
            os.link(temporary_path, destination)
        except FileExistsError:
            existing = destination.read_bytes()
            if existing == content:
                return "identical"
            raise DerivedArtifactConflictError(
                f"Derived artifact appeared with different bytes: {destination}. "
                "The existing artifact was not overwritten."
            )
        except OSError as error:
            raise ExtractionError(
                f"Unable to finalize derived artifact {destination}: {error}"
            ) from error
    except FileExistsError as error:
        raise ExtractionError(
            f"Temporary extraction path already exists: {temporary_path}. "
            "Inspect or remove the stale file before retrying."
        ) from error
    except OSError as error:
        raise ExtractionError(
            f"Unable to write derived artifact {destination}: {error}"
        ) from error
    finally:
        if temporary_path.exists():
            temporary_path.unlink()
    return "created"


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path)


def _build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Extract the checksum-governed November 2025 Austin Watershed "
            "project source universe into deterministic CSV."
        )
    )
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE_PATH)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT_PATH)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_argument_parser().parse_args(argv)
    try:
        result = extract_source_universe(
            source_path=args.source,
            registry_path=args.registry,
        )
        artifact_status = write_extraction(args.output, result.records)
    except ExtractionError as error:
        print("FAILURE: Watershed project source-universe extraction", file=sys.stderr)
        print(f"  {error}", file=sys.stderr)
        return 1

    print("SUCCESS: Watershed project source-universe extraction")
    print(f"  Source ID: {SOURCE_ID}")
    print(f"  Source PDF: {_display_path(args.source)}")
    print(f"  Output CSV: {_display_path(args.output)}")
    print(f"  Artifact status: {artifact_status}")
    print(f"  Project rows: {len(result.records)}")
    print(f"  Reconciled total: ${result.table_total_dollars:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
