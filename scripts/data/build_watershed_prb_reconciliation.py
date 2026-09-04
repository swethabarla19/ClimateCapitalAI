#!/usr/bin/env python3
"""Build the governed M3.7A Watershed PRB reconciliation artifact."""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

NOV_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"

DEFAULT_WATERSHED_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "source_rows"
    / "watershed.json"
)

DEFAULT_PRB_SCORE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "watershed_prb_scores.csv"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "watershed-prb-reconciliation.json"
)

EXPECTED_PROJECT_COUNT = 37
EXPECTED_NOVEMBER_REQUEST_TOTAL = 327_970_000
EXPECTED_JANUARY_REQUEST_TOTAL = 328_095_000
EXPECTED_JANUARY_RECOMMENDATION_TOTAL = 125_000_000
EXPECTED_NAME_DIFFERENCE_COUNT = 30
EXPECTED_REQUEST_CONFLICT_IDS = {"5754.149"}

ARTIFACT_VERSION = "m3.7a-watershed-prb-reconciliation/1.0.0"


class ReconciliationError(RuntimeError):
    """Raised when M3.7A reconciliation cannot proceed without guessing."""


class DerivedArtifactConflictError(ReconciliationError):
    """Raised when a differing governed artifact would be overwritten."""


@dataclass(frozen=True)
class ReconciliationRecord:
    canonical_project_id: str

    canonical_november_name: str
    january_source_name: str

    reconciliation_status: str
    name_version_difference: bool

    november_request_dollars: int
    january_request_dollars: int
    january_recommendation_dollars: int | None
    request_version_conflict: bool

    strategic_alignment: int
    critical_asset: int
    community_consideration: int
    efficiency: int
    timeliness_readiness: int
    climate_resilience: int
    prb_grand_total: int

    canonical_identity_source_id: str
    prb_scoring_source_id: str
    prb_source_pdf_page: int
    prb_source_table_row_order: int


def load_watershed_projects(
    path: Path,
) -> list[dict[str, object]]:
    rows = json.loads(path.read_text(encoding="utf-8"))

    projects = [
        row
        for row in rows
        if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
    ]

    if len(projects) != EXPECTED_PROJECT_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_PROJECT_COUNT} Watershed analytical "
            f"projects; found {len(projects)}."
        )

    ids = [
        str(project["canonical_project_id"])
        for project in projects
    ]

    if len(ids) != len(set(ids)):
        raise ReconciliationError(
            "Canonical Watershed project IDs must be unique."
        )

    return projects


def load_prb_scores(
    path: Path,
) -> dict[str, dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as input_file:
        rows = list(csv.DictReader(input_file))

    if len(rows) != EXPECTED_PROJECT_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_PROJECT_COUNT} PRB score rows; "
            f"found {len(rows)}."
        )

    by_id: dict[str, dict[str, str]] = {}

    for row in rows:
        canonical_project_id = row["canonical_project_id"]

        if canonical_project_id in by_id:
            raise ReconciliationError(
                f"Duplicate PRB score canonical ID "
                f"{canonical_project_id!r}."
            )

        by_id[canonical_project_id] = row

    return by_id


def source_version(
    project: dict[str, object],
    source_id: str,
) -> dict[str, object]:
    versions = [
        version
        for version in project["source_versions"]
        if version["source_id"] == source_id
    ]

    if len(versions) != 1:
        raise ReconciliationError(
            f"{project['canonical_project_id']} must contain exactly "
            f"one source version for {source_id!r}."
        )

    return versions[0]


def build_records(
    projects: list[dict[str, object]],
    prb_scores: dict[str, dict[str, str]],
) -> tuple[ReconciliationRecord, ...]:
    project_ids = {
        str(project["canonical_project_id"])
        for project in projects
    }

    score_ids = set(prb_scores)

    if project_ids != score_ids:
        raise ReconciliationError(
            "Canonical project IDs and PRB score IDs do not reconcile. "
            f"Missing scores={sorted(project_ids - score_ids)}; "
            f"unexpected scores={sorted(score_ids - project_ids)}"
        )

    records: list[ReconciliationRecord] = []

    for project in projects:
        canonical_id = str(
            project["canonical_project_id"]
        )

        november = source_version(
            project,
            NOV_SOURCE_ID,
        )

        january = source_version(
            project,
            JAN_SOURCE_ID,
        )

        score = prb_scores[canonical_id]

        november_name = str(
            november["source_name"]
        )

        january_name = str(
            january["source_name"]
        )

        if score["january_source_name"] != january_name:
            raise ReconciliationError(
                f"January source-name mismatch for {canonical_id}: "
                f"score artifact={score['january_source_name']!r}; "
                f"governed overlay={january_name!r}"
            )

        name_difference = (
            november_name != january_name
        )

        reconciliation_status = (
            "EXACT_NAME_MATCH"
            if not name_difference
            else "GOVERNED_SOURCE_VERSION_MATCH"
        )

        november_request = november.get(
            "department_request_dollars"
        )

        january_request = january.get(
            "department_request_dollars"
        )

        january_recommendation = january.get(
            "historical_recommendation_amount_dollars"
        )

        if november_request is None:
            raise ReconciliationError(
                f"{canonical_id} has no November request amount."
            )

        if january_request is None:
            raise ReconciliationError(
                f"{canonical_id} has no January request amount."
            )

        request_conflict = (
            int(november_request)
            != int(january_request)
        )

        strategic_alignment = int(
            score["strategic_alignment"]
        )
        critical_asset = int(
            score["critical_asset"]
        )
        community_consideration = int(
            score["community_consideration"]
        )
        efficiency = int(
            score["efficiency"]
        )
        timeliness_readiness = int(
            score["timeliness_readiness"]
        )
        climate_resilience = int(
            score["climate_resilience"]
        )
        grand_total = int(
            score["grand_total"]
        )

        component_sum = (
            strategic_alignment
            + critical_asset
            + community_consideration
            + efficiency
            + timeliness_readiness
            + climate_resilience
        )

        if component_sum != grand_total:
            raise ReconciliationError(
                f"PRB component sum mismatch for {canonical_id}: "
                f"{component_sum} != {grand_total}"
            )

        if grand_total != project["prb_score"]:
            raise ReconciliationError(
                f"PRB Grand Total mismatch for {canonical_id}: "
                f"score artifact={grand_total}; "
                f"M3.6={project['prb_score']}"
            )

        records.append(
            ReconciliationRecord(
                canonical_project_id=canonical_id,
                canonical_november_name=november_name,
                january_source_name=january_name,
                reconciliation_status=reconciliation_status,
                name_version_difference=name_difference,
                november_request_dollars=int(
                    november_request
                ),
                january_request_dollars=int(
                    january_request
                ),
                january_recommendation_dollars=(
                    int(january_recommendation)
                    if january_recommendation is not None
                    else None
                ),
                request_version_conflict=request_conflict,
                strategic_alignment=strategic_alignment,
                critical_asset=critical_asset,
                community_consideration=community_consideration,
                efficiency=efficiency,
                timeliness_readiness=timeliness_readiness,
                climate_resilience=climate_resilience,
                prb_grand_total=grand_total,
                canonical_identity_source_id=NOV_SOURCE_ID,
                prb_scoring_source_id=JAN_SOURCE_ID,
                prb_source_pdf_page=int(
                    score["source_pdf_page"]
                ),
                prb_source_table_row_order=int(
                    score["source_table_row_order"]
                ),
            )
        )

    return tuple(records)


def validate_records(
    records: tuple[ReconciliationRecord, ...],
) -> dict[str, int]:
    if len(records) != EXPECTED_PROJECT_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_PROJECT_COUNT} reconciliation "
            f"records; found {len(records)}."
        )

    ids = [
        record.canonical_project_id
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise ReconciliationError(
            "Reconciliation canonical IDs are not unique."
        )

    november_total = sum(
        record.november_request_dollars
        for record in records
    )

    january_total = sum(
        record.january_request_dollars
        for record in records
    )

    recommendation_total = sum(
        record.january_recommendation_dollars or 0
        for record in records
    )

    name_difference_count = sum(
        record.name_version_difference
        for record in records
    )

    request_conflict_ids = {
        record.canonical_project_id
        for record in records
        if record.request_version_conflict
    }

    exact_name_count = sum(
        record.reconciliation_status
        == "EXACT_NAME_MATCH"
        for record in records
    )

    governed_version_match_count = sum(
        record.reconciliation_status
        == "GOVERNED_SOURCE_VERSION_MATCH"
        for record in records
    )

    if november_total != EXPECTED_NOVEMBER_REQUEST_TOTAL:
        raise ReconciliationError(
            f"November request total changed: "
            f"{november_total:,}"
        )

    if january_total != EXPECTED_JANUARY_REQUEST_TOTAL:
        raise ReconciliationError(
            f"January request total changed: "
            f"{january_total:,}"
        )

    if (
        recommendation_total
        != EXPECTED_JANUARY_RECOMMENDATION_TOTAL
    ):
        raise ReconciliationError(
            f"January recommendation total changed: "
            f"{recommendation_total:,}"
        )

    if (
        name_difference_count
        != EXPECTED_NAME_DIFFERENCE_COUNT
    ):
        raise ReconciliationError(
            f"Expected {EXPECTED_NAME_DIFFERENCE_COUNT} "
            f"name-version differences; "
            f"found {name_difference_count}."
        )

    if (
        request_conflict_ids
        != EXPECTED_REQUEST_CONFLICT_IDS
    ):
        raise ReconciliationError(
            "Request-version conflict set changed: "
            f"{sorted(request_conflict_ids)}"
        )

    if exact_name_count + governed_version_match_count != 37:
        raise ReconciliationError(
            "Every project must have a governed reconciliation status."
        )

    return {
        "project_count": len(records),
        "exact_name_match_count": exact_name_count,
        "governed_source_version_match_count": (
            governed_version_match_count
        ),
        "name_version_difference_count": (
            name_difference_count
        ),
        "request_version_conflict_count": len(
            request_conflict_ids
        ),
        "november_request_total_dollars": (
            november_total
        ),
        "january_request_total_dollars": (
            january_total
        ),
        "january_recommendation_total_dollars": (
            recommendation_total
        ),
        "complete_prb_component_vector_count": len(
            records
        ),
        "valid_prb_grand_total_count": len(
            records
        ),
    }


def render_artifact(
    records: tuple[ReconciliationRecord, ...],
    summary: dict[str, int],
) -> bytes:
    artifact = {
        "artifact_version": ARTIFACT_VERSION,
        "governance_checkpoint": "M3.7A",
        "historical_decision_snapshot_date": "2026-01-21",
        "canonical_identity_source_id": NOV_SOURCE_ID,
        "prb_scoring_source_id": JAN_SOURCE_ID,
        "summary": summary,
        "records": [
            asdict(record)
            for record in records
        ],
    }

    return (
        json.dumps(
            artifact,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def write_artifact(
    output_path: Path,
    content: bytes,
) -> str:
    if output_path.exists():
        existing = output_path.read_bytes()

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite differing governed "
            f"reconciliation artifact: {output_path}"
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
        "--watershed-path",
        type=Path,
        default=DEFAULT_WATERSHED_PATH,
    )

    parser.add_argument(
        "--prb-score-path",
        type=Path,
        default=DEFAULT_PRB_SCORE_PATH,
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

    projects = load_watershed_projects(
        args.watershed_path
    )

    scores = load_prb_scores(
        args.prb_score_path
    )

    records = build_records(
        projects,
        scores,
    )

    summary = validate_records(
        records
    )

    print("M3.7A Watershed PRB reconciliation")
    print(
        f"Projects reconciled: "
        f"{summary['project_count']}/37"
    )
    print(
        "Exact Nov/Jan name matches: "
        f"{summary['exact_name_match_count']}"
    )
    print(
        "Governed source-version name matches: "
        f"{summary['governed_source_version_match_count']}"
    )
    print(
        "Request-version conflicts: "
        f"{summary['request_version_conflict_count']}"
    )
    print(
        "Complete PRB component vectors: "
        f"{summary['complete_prb_component_vector_count']}/37"
    )
    print(
        "Valid PRB Grand Totals: "
        f"{summary['valid_prb_grand_total_count']}/37"
    )
    print(
        "November request total: "
        f"${summary['november_request_total_dollars']:,}"
    )
    print(
        "January request total: "
        f"${summary['january_request_total_dollars']:,}"
    )
    print(
        "January recommendation total: "
        f"${summary['january_recommendation_total_dollars']:,}"
    )

    if args.verify_only:
        print(
            "Verify-only mode: "
            "no governed reconciliation artifact written."
        )
        return 0

    content = render_artifact(
        records,
        summary,
    )

    result = write_artifact(
        args.output_path,
        content,
    )

    print(
        f"Governed reconciliation artifact: "
        f"{result}: {args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
