#!/usr/bin/env python3
"""Extract and reconcile the January 2026 Watershed PRB score components."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

from pypdf import PdfReader


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
JAN_SOURCE_ID = SOURCE_ID

DEFAULT_REGISTRY_PATH = (
    REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
)

DEFAULT_SOURCE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "staging"
    / "raw"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "source.pdf"
)

DEFAULT_WATERSHED_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "source_rows"
    / "watershed.json"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "watershed_prb_scores.csv"
)

EXPECTED_RECORD_COUNT = 37
PHYSICAL_PDF_PAGES = (8, 9, 10)

CSV_COLUMNS = (
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

PROJECT_PREFIX = (
    r"Watershed Protection "
    r"Strategic Plan Identified Drainage & "
    r"Stormwater Infrastructure Projects - "
)

PROJECT_PATTERN = re.compile(
    PROJECT_PREFIX
    + r"(?P<name>.+?) "
    + r"(?P<requirement>Yes|No) "
    + r"(?P<city_owned>Yes|No) "
    + r"(?P<strategic_alignment>\d+) "
    + r"(?P<critical_asset>\d+) "
    + r"(?P<community_consideration>\d+) "
    + r"(?P<efficiency>\d+) "
    + r"(?P<timeliness_readiness>\d+) "
    + r"(?P<climate_resilience>\d+) "
    + r"(?P<grand_total>\d+) "
    + r"No "
)

CHECKSUM_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")


class ExtractionError(RuntimeError):
    """Raised when deterministic extraction or reconciliation cannot proceed."""


class DerivedArtifactConflictError(ExtractionError):
    """Raised when a differing derived artifact would be overwritten."""


@dataclass(frozen=True)
class PrbScoreRecord:
    source_id: str
    source_pdf_page: int
    source_table_row_order: int
    canonical_project_id: str
    january_source_name: str
    strategic_alignment: int
    critical_asset: int
    community_consideration: int
    efficiency: int
    timeliness_readiness: int
    climate_resilience: int
    grand_total: int


def normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def sha256_checksum(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)

    return "sha256:" + digest.hexdigest()


def load_registered_source(registry_path: Path) -> dict[str, str]:
    with registry_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as registry_file:
        rows = [
            row
            for row in csv.DictReader(registry_file)
            if row.get("source_id") == SOURCE_ID
        ]

    if len(rows) != 1:
        raise ExtractionError(
            f"Expected exactly one source registry row for {SOURCE_ID!r}; "
            f"found {len(rows)}."
        )

    source = rows[0]

    if source.get("format") != "PDF":
        raise ExtractionError(
            "January PRB source must be registered as PDF."
        )

    if source.get("historical_fit") != "valid":
        raise ExtractionError(
            "January PRB source must remain historically valid."
        )

    # Preserve the existing M3.6 authority boundary.
    #
    # M3.7A extracts source-governed PRB evidence but does not yet
    # promote the entire January source from benchmark authority to
    # analytical authority. The Initial Recommendation outcome must
    # remain isolated from future analytical inputs.
    if source.get("analytical_role") != "benchmark":
        raise ExtractionError(
            "January PRB source analytical_role changed unexpectedly; "
            "M3.7A expects the existing benchmark registration."
        )

    checksum = source.get("checksum", "")

    if not CHECKSUM_PATTERN.fullmatch(checksum):
        raise ExtractionError(
            "January PRB source does not have a valid registered "
            "SHA-256 checksum."
        )

    return source


def validate_source_checksum(
    source_path: Path,
    registry_path: Path,
) -> str:
    source = load_registered_source(registry_path)

    actual = sha256_checksum(source_path)
    expected = source["checksum"]

    if actual != expected:
        raise ExtractionError(
            f"Source checksum mismatch: expected {expected}; "
            f"found {actual}."
        )

    return actual


def load_governed_january_overlay(
    watershed_path: Path,
) -> dict[str, dict[str, object]]:
    rows = json.loads(
        watershed_path.read_text(encoding="utf-8")
    )

    projects = [
        row
        for row in rows
        if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
    ]

    if len(projects) != EXPECTED_RECORD_COUNT:
        raise ExtractionError(
            f"Expected {EXPECTED_RECORD_COUNT} governed Watershed "
            f"projects; found {len(projects)}."
        )

    overlay: dict[str, dict[str, object]] = {}

    for project in projects:
        january_versions = [
            version
            for version in project["source_versions"]
            if version["source_id"] == JAN_SOURCE_ID
        ]

        if len(january_versions) != 1:
            raise ExtractionError(
                f"{project['canonical_project_id']} must have exactly "
                "one January source version."
            )

        january = january_versions[0]
        january_name = january.get("source_name")

        if not january_name:
            raise ExtractionError(
                f"{project['canonical_project_id']} has no January "
                "source name."
            )

        if january_name in overlay:
            raise ExtractionError(
                f"Duplicate governed January source name: "
                f"{january_name!r}"
            )

        overlay[january_name] = {
            "canonical_project_id": project["canonical_project_id"],
            "grand_total": project["prb_score"],
        }

    if len(overlay) != EXPECTED_RECORD_COUNT:
        raise ExtractionError(
            "Governed January overlay does not contain 37 unique "
            "project names."
        )

    return overlay


def extract_score_rows(
    source_path: Path,
    governed_overlay: dict[str, dict[str, object]],
) -> tuple[PrbScoreRecord, ...]:
    reader = PdfReader(source_path)

    if len(reader.pages) < max(PHYSICAL_PDF_PAGES):
        raise ExtractionError(
            f"Source PDF has only {len(reader.pages)} pages; "
            "expected Watershed scoring on physical pages 8-10."
        )

    extracted: list[tuple[int, dict[str, str]]] = []

    for physical_page in PHYSICAL_PDF_PAGES:
        text = reader.pages[
            physical_page - 1
        ].extract_text() or ""

        normalized = normalize_whitespace(text)

        for match in PROJECT_PATTERN.finditer(normalized):
            extracted.append(
                (physical_page, match.groupdict())
            )

    if len(extracted) != EXPECTED_RECORD_COUNT:
        raise ExtractionError(
            f"Expected {EXPECTED_RECORD_COUNT} Watershed project "
            f"score rows; extracted {len(extracted)}."
        )

    extracted_names = [
        row["name"]
        for _, row in extracted
    ]

    if len(extracted_names) != len(set(extracted_names)):
        raise ExtractionError(
            "Extracted January project names are not unique."
        )

    governed_names = set(governed_overlay)
    extracted_name_set = set(extracted_names)

    missing = sorted(
        governed_names - extracted_name_set
    )

    unexpected = sorted(
        extracted_name_set - governed_names
    )

    if missing or unexpected:
        raise ExtractionError(
            "January project-name reconciliation failed. "
            f"Missing={missing}; unexpected={unexpected}"
        )

    records: list[PrbScoreRecord] = []

    for row_order, (
        physical_page,
        raw,
    ) in enumerate(extracted, start=1):
        numeric = {
            key: int(raw[key])
            for key in (
                "strategic_alignment",
                "critical_asset",
                "community_consideration",
                "efficiency",
                "timeliness_readiness",
                "climate_resilience",
                "grand_total",
            )
        }

        component_sum = (
            numeric["strategic_alignment"]
            + numeric["critical_asset"]
            + numeric["community_consideration"]
            + numeric["efficiency"]
            + numeric["timeliness_readiness"]
            + numeric["climate_resilience"]
        )

        if component_sum != numeric["grand_total"]:
            raise ExtractionError(
                f"Component sum mismatch for {raw['name']!r}: "
                f"{component_sum} != {numeric['grand_total']}"
            )

        governed = governed_overlay[raw["name"]]

        if (
            numeric["grand_total"]
            != governed["grand_total"]
        ):
            raise ExtractionError(
                f"Grand Total mismatch for {raw['name']!r}: "
                f"PDF={numeric['grand_total']} "
                f"governed={governed['grand_total']}"
            )

        records.append(
            PrbScoreRecord(
                source_id=SOURCE_ID,
                source_pdf_page=physical_page,
                source_table_row_order=row_order,
                canonical_project_id=str(
                    governed["canonical_project_id"]
                ),
                january_source_name=raw["name"],
                strategic_alignment=numeric[
                    "strategic_alignment"
                ],
                critical_asset=numeric[
                    "critical_asset"
                ],
                community_consideration=numeric[
                    "community_consideration"
                ],
                efficiency=numeric["efficiency"],
                timeliness_readiness=numeric[
                    "timeliness_readiness"
                ],
                climate_resilience=numeric[
                    "climate_resilience"
                ],
                grand_total=numeric["grand_total"],
            )
        )

    canonical_ids = [
        record.canonical_project_id
        for record in records
    ]

    if len(canonical_ids) != len(set(canonical_ids)):
        raise ExtractionError(
            "Canonical project IDs are not unique after "
            "reconciliation."
        )

    return tuple(records)


def render_csv(
    records: tuple[PrbScoreRecord, ...],
) -> bytes:
    buffer = io.StringIO(newline="")

    writer = csv.DictWriter(
        buffer,
        fieldnames=CSV_COLUMNS,
        lineterminator="\n",
    )

    writer.writeheader()

    for record in records:
        writer.writerow(asdict(record))

    return buffer.getvalue().encode("utf-8")


def write_artifact(
    output_path: Path,
    records: tuple[PrbScoreRecord, ...],
) -> str:
    content = render_csv(records)

    if output_path.exists():
        existing = output_path.read_bytes()

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite differing derived artifact: "
            f"{output_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_bytes(content)

    return "created"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--source-path",
        type=Path,
        default=DEFAULT_SOURCE_PATH,
    )

    parser.add_argument(
        "--registry-path",
        type=Path,
        default=DEFAULT_REGISTRY_PATH,
    )

    parser.add_argument(
        "--watershed-path",
        type=Path,
        default=DEFAULT_WATERSHED_PATH,
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
    )

    parser.add_argument(
        "--verify-only",
        action="store_true",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    checksum = validate_source_checksum(
        args.source_path,
        args.registry_path,
    )

    governed_overlay = load_governed_january_overlay(
        args.watershed_path
    )

    records = extract_score_rows(
        args.source_path,
        governed_overlay,
    )

    print(
        f"Verified source checksum: {checksum}"
    )

    print(
        f"Extracted Watershed PRB projects: "
        f"{len(records)}"
    )

    print(
        "Unique canonical project IDs: "
        f"{len({record.canonical_project_id for record in records})}"
    )

    mismatch_count = sum(
        (
            record.strategic_alignment
            + record.critical_asset
            + record.community_consideration
            + record.efficiency
            + record.timeliness_readiness
            + record.climate_resilience
        )
        != record.grand_total
        for record in records
    )

    print(
        f"Component-sum mismatches: "
        f"{mismatch_count}"
    )

    if args.verify_only:
        print(
            "Verify-only mode: "
            "no derived artifact written."
        )
        return 0

    result = write_artifact(
        args.output_path,
        records,
    )

    print(
        f"Derived artifact: "
        f"{result}: {args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
