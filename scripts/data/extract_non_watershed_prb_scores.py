#!/usr/bin/env python3
"""Extract and reconcile January 2026 PRB score components for the 69 non-Watershed analytical projects."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import unicodedata
from dataclasses import asdict, dataclass
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"

DEFAULT_REGISTRY_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "metadata"
    / "source_registry.csv"
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

CATEGORY_PATHS = {
    "Transportation": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "transportation.json"
    ),
    "Parks & Open Space": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "parks.json"
    ),
    "Community Facilities": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "community_facilities.json"
    ),
}

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "non_watershed_prb_scores.csv"
)

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Community Facilities": 38,
}

EXPECTED_RECORD_COUNT = 69

EXPECTED_PAGE_COUNTS = {
    5: 19,
    6: 29,
    7: 21,
}

EXPECTED_HALF_POINT_PROJECTS = {
    "community-facilities/ems/station-03",
    "community-facilities/ems/station-14",
    "community-facilities/fleet/consolidated-service-center",
}

PHYSICAL_PDF_PAGES = (5, 6, 7)

CSV_COLUMNS = (
    "source_id",
    "source_pdf_page",
    "source_table_row_order",
    "decision_unit_id",
    "presentation_category",
    "january_source_name",
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
    "grand_total",
)

NUMBER = r"\d+(?:\.\d+)?"

ROW_SUFFIX_PATTERN = re.compile(
    rf"^\s+"
    rf"(?P<requirement>yes|no|n/a)\s+"
    rf"(?P<city_owned>yes|no|n/a)\s+"
    rf"(?P<strategic_alignment>{NUMBER})\s+"
    rf"(?P<critical_asset>{NUMBER})\s+"
    rf"(?P<community_consideration>{NUMBER})\s+"
    rf"(?P<efficiency>{NUMBER})\s+"
    rf"(?P<timeliness_readiness>{NUMBER})\s+"
    rf"(?P<climate_resilience>{NUMBER})\s+"
    rf"(?P<grand_total>{NUMBER})\s+"
    rf"(?P<om_impact>yes|no|n/a)\b"
)

COMPONENT_FIELDS = (
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
)

CHECKSUM_PATTERN = re.compile(
    r"^sha256:[0-9a-f]{64}$"
)


class ExtractionError(RuntimeError):
    """Raised when deterministic extraction cannot proceed."""


class DerivedArtifactConflictError(ExtractionError):
    """Raised when a differing derived artifact already exists."""


@dataclass(frozen=True)
class PrbScoreRecord:
    source_id: str
    source_pdf_page: int
    source_table_row_order: int
    decision_unit_id: str
    presentation_category: str
    january_source_name: str
    strategic_alignment: Decimal
    critical_asset: Decimal
    community_consideration: Decimal
    efficiency: Decimal
    timeliness_readiness: Decimal
    climate_resilience: Decimal
    grand_total: Decimal


def normalize(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD",
        value,
    )

    value = value.replace("&", " and ")
    value = value.replace("–", "-")
    value = value.replace("—", "-")
    value = value.lower()

    value = re.sub(
        r"[^a-z0-9.$]+",
        " ",
        value,
    )

    return " ".join(value.split())


def sha256_checksum(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as source_file:
        for chunk in iter(
            lambda: source_file.read(
                1024 * 1024
            ),
            b"",
        ):
            digest.update(chunk)

    return "sha256:" + digest.hexdigest()


def load_registered_source(
    registry_path: Path,
) -> dict[str, str]:
    with registry_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as registry_file:
        rows = [
            row
            for row in csv.DictReader(
                registry_file
            )
            if row.get("source_id")
            == SOURCE_ID
        ]

    if len(rows) != 1:
        raise ExtractionError(
            "Expected exactly one January "
            "source registry row."
        )

    source = rows[0]

    if source.get("format") != "PDF":
        raise ExtractionError(
            "January PRB source must remain PDF."
        )

    if source.get("historical_fit") != "valid":
        raise ExtractionError(
            "January PRB source must remain "
            "historically valid."
        )

    # Preserve the field-level authority boundary.
    # The PDF contains analytical PRB scoring evidence
    # plus the historical recommendation outcome.
    if source.get("analytical_role") != "benchmark":
        raise ExtractionError(
            "January source analytical_role "
            "changed unexpectedly."
        )

    checksum = source.get(
        "checksum",
        "",
    )

    if not CHECKSUM_PATTERN.fullmatch(
        checksum
    ):
        raise ExtractionError(
            "January source does not have a "
            "valid registered SHA-256 checksum."
        )

    return source


def validate_source_checksum(
    source_path: Path,
    registry_path: Path,
) -> str:
    source = load_registered_source(
        registry_path
    )

    actual = sha256_checksum(
        source_path
    )

    expected = source["checksum"]

    if actual != expected:
        raise ExtractionError(
            "Source checksum mismatch: "
            f"expected {expected}; "
            f"found {actual}."
        )

    return actual


def load_governed_projects() -> dict[
    str,
    dict[str, object],
]:
    governed = {}

    for (
        presentation_category,
        path,
    ) in CATEGORY_PATHS.items():

        rows = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        projects = [
            row
            for row in rows
            if (
                row[
                    "analytical_unit_type"
                ]
                == "ANALYTICAL_PROJECT"
            )
        ]

        expected_count = (
            EXPECTED_CATEGORY_COUNTS[
                presentation_category
            ]
        )

        if len(projects) != expected_count:
            raise ExtractionError(
                f"{presentation_category}: "
                f"expected {expected_count} "
                "analytical projects; "
                f"found {len(projects)}."
            )

        for project in projects:
            decision_unit_id = project[
                "decision_unit_id"
            ]

            if decision_unit_id in governed:
                raise ExtractionError(
                    "Duplicate decision_unit_id: "
                    f"{decision_unit_id}"
                )

            if project["prb_scored"] is not True:
                raise ExtractionError(
                    f"{decision_unit_id} must "
                    "remain PRB-scored."
                )

            if project["prb_score"] is None:
                raise ExtractionError(
                    f"{decision_unit_id} has "
                    "no governed PRB score."
                )

            request = project[
                "department_request_dollars"
            ]

            if (
                request is None
                or request <= 0
            ):
                raise ExtractionError(
                    f"{decision_unit_id} has "
                    "no usable request amount."
                )

            january_versions = [
                version
                for version in project[
                    "source_versions"
                ]
                if (
                    version["source_id"]
                    == SOURCE_ID
                )
            ]

            if len(january_versions) != 1:
                raise ExtractionError(
                    f"{decision_unit_id} must "
                    "have exactly one January "
                    "source version."
                )

            january = january_versions[0]

            january_name = january.get(
                "source_name"
            )

            if not january_name:
                raise ExtractionError(
                    f"{decision_unit_id} has "
                    "no January source name."
                )

            if (
                january.get("prb_score")
                != project["prb_score"]
            ):
                raise ExtractionError(
                    f"{decision_unit_id} "
                    "January PRB score does not "
                    "match governed PRB score."
                )

            governed[decision_unit_id] = {
                "decision_unit_id": (
                    decision_unit_id
                ),
                "presentation_category": (
                    presentation_category
                ),
                "january_source_name": (
                    january_name
                ),
                "grand_total": Decimal(
                    str(
                        project[
                            "prb_score"
                        ]
                    )
                ),
            }

    if len(governed) != EXPECTED_RECORD_COUNT:
        raise ExtractionError(
            f"Expected {EXPECTED_RECORD_COUNT} "
            "governed non-Watershed projects; "
            f"found {len(governed)}."
        )

    names = [
        record["january_source_name"]
        for record in governed.values()
    ]

    if len(names) != len(set(names)):
        raise ExtractionError(
            "Governed January project names "
            "are not unique."
        )

    return governed


def is_half_point(
    value: Decimal,
) -> bool:
    doubled = value * Decimal("2")

    return (
        doubled
        == doubled.to_integral_value()
        and value
        != value.to_integral_value()
    )


def validate_half_point_increment(
    value: Decimal,
    field: str,
    decision_unit_id: str,
) -> None:
    doubled = value * Decimal("2")

    if (
        doubled
        != doubled.to_integral_value()
    ):
        raise ExtractionError(
            f"{decision_unit_id} {field} "
            "does not use a whole- or "
            "half-point increment."
        )


def extract_score_rows(
    source_path: Path,
    governed: dict[
        str,
        dict[str, object],
    ],
) -> tuple[PrbScoreRecord, ...]:

    reader = PdfReader(
        source_path
    )

    if (
        len(reader.pages)
        < max(PHYSICAL_PDF_PAGES)
    ):
        raise ExtractionError(
            "Source PDF does not contain "
            "physical pages 5-7."
        )

    page_text = {}

    for physical_page in (
        PHYSICAL_PDF_PAGES
    ):
        raw = (
            reader.pages[
                physical_page - 1
            ].extract_text()
            or ""
        )

        page_text[
            physical_page
        ] = normalize(raw)

    extracted = []

    for governed_record in (
        governed.values()
    ):
        name = str(
            governed_record[
                "january_source_name"
            ]
        )

        normalized_name = normalize(
            name
        )

        occurrences = []

        for (
            physical_page,
            text,
        ) in page_text.items():
            count = text.count(
                normalized_name
            )

            if count:
                start = text.find(
                    normalized_name
                )

                occurrences.append(
                    (
                        physical_page,
                        start,
                        count,
                    )
                )

        if len(occurrences) != 1:
            raise ExtractionError(
                f"{name!r} must occur on "
                "exactly one PRB page; "
                f"found {occurrences}."
            )

        (
            physical_page,
            start,
            count,
        ) = occurrences[0]

        if count != 1:
            raise ExtractionError(
                f"{name!r} occurs {count} "
                "times on physical page "
                f"{physical_page}."
            )

        text = page_text[
            physical_page
        ]

        suffix_start = (
            start
            + len(
                normalized_name
            )
        )

        suffix = text[
            suffix_start:
        ]

        match = (
            ROW_SUFFIX_PATTERN.match(
                suffix
            )
        )

        if match is None:
            raise ExtractionError(
                "Could not parse PRB score "
                f"suffix for {name!r} on "
                f"physical page "
                f"{physical_page}."
            )

        raw_scores = (
            match.groupdict()
        )

        scores = {
            field: Decimal(
                raw_scores[field]
            )
            for field in (
                *COMPONENT_FIELDS,
                "grand_total",
            )
        }

        for (
            field,
            value,
        ) in scores.items():
            validate_half_point_increment(
                value,
                field,
                str(
                    governed_record[
                        "decision_unit_id"
                    ]
                ),
            )

        component_sum = sum(
            (
                scores[field]
                for field in (
                    COMPONENT_FIELDS
                )
            ),
            Decimal("0"),
        )

        if (
            component_sum
            != scores["grand_total"]
        ):
            raise ExtractionError(
                "Component sum mismatch for "
                f"{name!r}: "
                f"{component_sum} != "
                f"{scores['grand_total']}"
            )

        if (
            scores["grand_total"]
            != governed_record[
                "grand_total"
            ]
        ):
            raise ExtractionError(
                "Governed Grand Total mismatch "
                f"for {name!r}: "
                f"PDF={scores['grand_total']} "
                "governed="
                f"{governed_record['grand_total']}"
            )

        extracted.append(
            {
                "physical_page": (
                    physical_page
                ),
                "source_position": start,
                "governed": (
                    governed_record
                ),
                "scores": scores,
            }
        )

    if (
        len(extracted)
        != EXPECTED_RECORD_COUNT
    ):
        raise ExtractionError(
            f"Expected {EXPECTED_RECORD_COUNT} "
            "score rows; extracted "
            f"{len(extracted)}."
        )

    extracted.sort(
        key=lambda row: (
            row["physical_page"],
            row["source_position"],
        )
    )

    page_counts = {}

    for row in extracted:
        page = row[
            "physical_page"
        ]

        page_counts[page] = (
            page_counts.get(
                page,
                0,
            )
            + 1
        )

    if (
        page_counts
        != EXPECTED_PAGE_COUNTS
    ):
        raise ExtractionError(
            "Physical-page extraction counts "
            "changed unexpectedly: "
            f"{page_counts}"
        )

    records = []

    for (
        row_order,
        extracted_row,
    ) in enumerate(
        extracted,
        start=1,
    ):
        governed_record = (
            extracted_row[
                "governed"
            ]
        )

        scores = (
            extracted_row[
                "scores"
            ]
        )

        records.append(
            PrbScoreRecord(
                source_id=SOURCE_ID,
                source_pdf_page=int(
                    extracted_row[
                        "physical_page"
                    ]
                ),
                source_table_row_order=(
                    row_order
                ),
                decision_unit_id=str(
                    governed_record[
                        "decision_unit_id"
                    ]
                ),
                presentation_category=str(
                    governed_record[
                        "presentation_category"
                    ]
                ),
                january_source_name=str(
                    governed_record[
                        "january_source_name"
                    ]
                ),
                strategic_alignment=scores[
                    "strategic_alignment"
                ],
                critical_asset=scores[
                    "critical_asset"
                ],
                community_consideration=scores[
                    "community_consideration"
                ],
                efficiency=scores[
                    "efficiency"
                ],
                timeliness_readiness=scores[
                    "timeliness_readiness"
                ],
                climate_resilience=scores[
                    "climate_resilience"
                ],
                grand_total=scores[
                    "grand_total"
                ],
            )
        )

    ids = [
        record.decision_unit_id
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise ExtractionError(
            "Extracted decision-unit IDs "
            "are not unique."
        )

    half_point_ids = {
        record.decision_unit_id
        for record in records
        if any(
            is_half_point(value)
            for value in (
                record.strategic_alignment,
                record.critical_asset,
                record.community_consideration,
                record.efficiency,
                record.timeliness_readiness,
                record.climate_resilience,
                record.grand_total,
            )
        )
    }

    if (
        half_point_ids
        != EXPECTED_HALF_POINT_PROJECTS
    ):
        raise ExtractionError(
            "Half-point project set changed "
            "unexpectedly: "
            f"{sorted(half_point_ids)}"
        )

    return tuple(records)


def render_csv(
    records: tuple[
        PrbScoreRecord,
        ...,
    ],
) -> bytes:
    buffer = io.StringIO(
        newline=""
    )

    writer = csv.DictWriter(
        buffer,
        fieldnames=CSV_COLUMNS,
        lineterminator="\n",
    )

    writer.writeheader()

    for record in records:
        writer.writerow(
            asdict(record)
        )

    return (
        buffer.getvalue()
        .encode("utf-8")
    )


def write_artifact(
    output_path: Path,
    records: tuple[
        PrbScoreRecord,
        ...,
    ],
) -> str:
    content = render_csv(
        records
    )

    if output_path.exists():
        existing = (
            output_path.read_bytes()
        )

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite "
            "differing derived artifact: "
            f"{output_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_bytes(
        content
    )

    return "created"


def parse_args() -> argparse.Namespace:
    parser = (
        argparse.ArgumentParser()
    )

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

    checksum = (
        validate_source_checksum(
            args.source_path,
            args.registry_path,
        )
    )

    governed = (
        load_governed_projects()
    )

    records = extract_score_rows(
        args.source_path,
        governed,
    )

    print(
        "Verified source checksum: "
        f"{checksum}"
    )

    print(
        "Extracted non-Watershed "
        "analytical projects: "
        f"{len(records)}"
    )

    print(
        "Unique decision_unit_ids: "
        f"{len({r.decision_unit_id for r in records})}"
    )

    print(
        "Page 5 rows: "
        f"{sum(r.source_pdf_page == 5 for r in records)}"
    )

    print(
        "Page 6 rows: "
        f"{sum(r.source_pdf_page == 6 for r in records)}"
    )

    print(
        "Page 7 rows: "
        f"{sum(r.source_pdf_page == 7 for r in records)}"
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
        "Component-sum mismatches: "
        f"{mismatch_count}"
    )

    half_point_ids = {
        record.decision_unit_id
        for record in records
        if any(
            is_half_point(value)
            for value in (
                record.strategic_alignment,
                record.critical_asset,
                record.community_consideration,
                record.efficiency,
                record.timeliness_readiness,
                record.climate_resilience,
                record.grand_total,
            )
        )
    }

    print(
        "Projects containing "
        "half-point values: "
        f"{len(half_point_ids)}"
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
        "Derived artifact: "
        f"{result}: "
        f"{args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())