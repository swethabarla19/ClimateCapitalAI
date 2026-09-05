#!/usr/bin/env python3
"""Build the governed M3.7C Watershed PRB Funding Priority overlay."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

MODEL_SCOPE = "WATERSHED_PRB_PROJECT_MODEL"
ARTIFACT_VERSION = "m3.7c-watershed-prb-funding-priority/1.0.0"

EXPECTED_PROJECT_COUNT = 37
EXPECTED_UNIQUE_SCORE_COUNT = 17
EXPECTED_TIE_GROUP_COUNT = 12
EXPECTED_TIED_PROJECT_COUNT = 32
EXPECTED_MAX_SCORE = 74
EXPECTED_MIN_SCORE = 52

DEFAULT_ELIGIBILITY_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "watershed-prb-model-eligibility.json"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "watershed-prb-funding-priority.json"
)


class FundingPriorityError(RuntimeError):
    """Raised when Funding Priority cannot be built without guessing."""


class DerivedArtifactConflictError(FundingPriorityError):
    """Raised when a differing governed artifact already exists."""


def load_eligibility(path: Path) -> dict[str, object]:
    artifact = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(artifact, dict):
        raise FundingPriorityError(
            "M3.7B eligibility artifact must be a JSON object."
        )

    if artifact.get("governance_checkpoint") != "M3.7B":
        raise FundingPriorityError(
            "M3.7C requires the governed M3.7B eligibility artifact."
        )

    if artifact.get("model_scope") != MODEL_SCOPE:
        raise FundingPriorityError(
            "M3.7B model scope does not match the Watershed PRB project model."
        )

    if artifact.get("runtime_integration_authorized") is not False:
        raise FundingPriorityError(
            "M3.7C requires runtime integration to remain unauthorized."
        )

    return artifact


def load_eligible_records(
    eligibility_path: Path,
) -> tuple[dict[str, object], ...]:
    artifact = load_eligibility(eligibility_path)

    records = artifact.get("records")

    if not isinstance(records, list):
        raise FundingPriorityError(
            "M3.7B eligibility artifact has no record list."
        )

    if len(records) != EXPECTED_PROJECT_COUNT:
        raise FundingPriorityError(
            f"Expected {EXPECTED_PROJECT_COUNT} M3.7B records; "
            f"found {len(records)}."
        )

    project_ids: list[str] = []

    for record in records:
        if record.get("model_scope") != MODEL_SCOPE:
            raise FundingPriorityError(
                "Eligibility record has unexpected model scope."
            )

        if record.get("evidence_feasibility_status") != "FEASIBLE":
            raise FundingPriorityError(
                "M3.7C cannot rank an evidence-infeasible project."
            )

        if record.get("model_eligible") is not True:
            raise FundingPriorityError(
                "M3.7C cannot rank a model-ineligible project."
            )

        if record.get("blocking_reason_codes") != []:
            raise FundingPriorityError(
                "Eligible ranking cohort must have no blocking reason codes."
            )

        project_id = record.get("canonical_project_id")
        score = record.get("prb_grand_total")

        if not isinstance(project_id, str) or not project_id:
            raise FundingPriorityError(
                "Eligible project is missing canonical_project_id."
            )

        if (
            not isinstance(score, int)
            or isinstance(score, bool)
        ):
            raise FundingPriorityError(
                "PRB Grand Total must be an integer."
            )

        if not 0 <= score <= 100:
            raise FundingPriorityError(
                "PRB Grand Total must be between 0 and 100."
            )

        project_ids.append(project_id)

    if len(project_ids) != len(set(project_ids)):
        raise FundingPriorityError(
            "Canonical project IDs must be unique."
        )

    return tuple(records)


def build_ranking_records(
    eligible_records: tuple[dict[str, object], ...],
) -> tuple[dict[str, object], ...]:
    ordered = sorted(
        eligible_records,
        key=lambda record: (
            -int(record["prb_grand_total"]),
            str(record["canonical_project_id"]),
        ),
    )

    score_counts = Counter(
        int(record["prb_grand_total"])
        for record in ordered
    )

    display_positions: dict[int, int] = {}

    output: list[dict[str, object]] = []

    previous_score: int | None = None
    current_rank: int | None = None

    for position, record in enumerate(ordered, start=1):
        score = int(record["prb_grand_total"])

        if score != previous_score:
            current_rank = position
            previous_score = score

        if current_rank is None:
            raise FundingPriorityError(
                "Competition rank failed to initialize."
            )

        display_positions[score] = (
            display_positions.get(score, 0) + 1
        )

        output.append(
            {
                "canonical_project_id": str(
                    record["canonical_project_id"]
                ),
                "model_scope": MODEL_SCOPE,
                "funding_priority_score": score,
                "funding_priority_rank": current_rank,
                "is_tied": score_counts[score] > 1,
                "tie_group_size": score_counts[score],
                "display_order_within_tie": (
                    display_positions[score]
                ),
                "display_tiebreak_has_analytical_meaning": False,
            }
        )

    return tuple(output)


def validate_ranking_records(
    records: tuple[dict[str, object], ...],
) -> dict[str, int]:
    if len(records) != EXPECTED_PROJECT_COUNT:
        raise FundingPriorityError(
            f"Expected {EXPECTED_PROJECT_COUNT} ranking records; "
            f"found {len(records)}."
        )

    project_ids = [
        str(record["canonical_project_id"])
        for record in records
    ]

    if len(project_ids) != len(set(project_ids)):
        raise FundingPriorityError(
            "Ranking project IDs must be unique."
        )

    scores = [
        int(record["funding_priority_score"])
        for record in records
    ]

    score_counts = Counter(scores)

    unique_score_count = len(score_counts)

    tied_score_group_count = sum(
        1
        for count in score_counts.values()
        if count > 1
    )

    tied_project_count = sum(
        count
        for count in score_counts.values()
        if count > 1
    )

    maximum_score = max(scores)
    minimum_score = min(scores)

    if unique_score_count != EXPECTED_UNIQUE_SCORE_COUNT:
        raise FundingPriorityError(
            "Unique PRB Grand Total count changed unexpectedly."
        )

    if tied_score_group_count != EXPECTED_TIE_GROUP_COUNT:
        raise FundingPriorityError(
            "Tied PRB score-group count changed unexpectedly."
        )

    if tied_project_count != EXPECTED_TIED_PROJECT_COUNT:
        raise FundingPriorityError(
            "Tied project count changed unexpectedly."
        )

    if (
        maximum_score != EXPECTED_MAX_SCORE
        or minimum_score != EXPECTED_MIN_SCORE
    ):
        raise FundingPriorityError(
            "PRB score range changed unexpectedly."
        )

    # Verify descending competition ranking.
    previous_score: int | None = None
    expected_rank: int | None = None

    for position, record in enumerate(records, start=1):
        score = int(record["funding_priority_score"])

        if score != previous_score:
            expected_rank = position
            previous_score = score

        if record["funding_priority_rank"] != expected_rank:
            raise FundingPriorityError(
                "Funding Priority rank is not deterministic "
                "competition ranking."
            )

    # Verify canonical project ID ordering only within equal-score groups.
    for score in score_counts:
        group = [
            record
            for record in records
            if record["funding_priority_score"] == score
        ]

        ids = [
            str(record["canonical_project_id"])
            for record in group
        ]

        if ids != sorted(ids):
            raise FundingPriorityError(
                "Tie display order is not canonical project ID ascending."
            )

        expected_positions = list(
            range(1, len(group) + 1)
        )

        actual_positions = [
            int(record["display_order_within_tie"])
            for record in group
        ]

        if actual_positions != expected_positions:
            raise FundingPriorityError(
                "Tie display positions are not deterministic."
            )

        if any(
            record["display_tiebreak_has_analytical_meaning"]
            is not False
            for record in group
        ):
            raise FundingPriorityError(
                "Display tiebreak must have no analytical meaning."
            )

    return {
        "analytical_project_count": len(records),
        "unique_funding_priority_score_count": (
            unique_score_count
        ),
        "tied_score_group_count": tied_score_group_count,
        "projects_in_tied_score_groups": tied_project_count,
        "maximum_funding_priority_score": maximum_score,
        "minimum_funding_priority_score": minimum_score,
    }


def render_artifact(
    records: tuple[dict[str, object], ...],
    summary: dict[str, int],
) -> bytes:
    artifact = {
        "artifact_version": ARTIFACT_VERSION,
        "governance_checkpoint": "M3.7C",
        "historical_decision_snapshot_date": "2026-01-21",
        "model_scope": MODEL_SCOPE,
        "portfolio_selection_authorized": False,
        "runtime_integration_authorized": False,
        "source_artifacts": {
            "model_eligibility": (
                "data/governed/cross_category/"
                "model_eligibility/"
                "watershed-prb-model-eligibility.json"
            ),
        },
        "ranking_policy": {
            "funding_priority_score_authority": (
                "OFFICIAL_PRB_GRAND_TOTAL"
            ),
            "direction": "HIGHER_IS_HIGHER_PRIORITY",
            "rank_method": (
                "COMPETITION_RANK_DESCENDING"
            ),
            "tie_policy": "SHARED_SUBSTANTIVE_RANK",
            "display_tiebreak": (
                "CANONICAL_PROJECT_ID_ASCENDING"
            ),
            "display_tiebreak_has_analytical_meaning": False,
            "forbidden_analytical_tiebreakers": [
                "PROJECT_COST",
                "JANUARY_INITIAL_RECOMMENDATION",
                "INDIVIDUAL_PRB_COMPONENT",
                "RNA_GEOMETRY",
                "FEMA_FLOODPLAIN_CONTEXT",
                "EAZ_2021_CONTEXT",
                "WATERSHED_PROBLEM_SCORE_CONTEXT",
                "SOURCE_TABLE_ROW_ORDER",
                "PROJECT_NAME",
            ],
        },
        "summary": summary,
        "records": list(records),
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
            f"Funding Priority artifact: {output_path}"
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
        "--eligibility-path",
        type=Path,
        default=DEFAULT_ELIGIBILITY_PATH,
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

    eligible_records = load_eligible_records(
        args.eligibility_path
    )

    ranking_records = build_ranking_records(
        eligible_records
    )

    summary = validate_ranking_records(
        ranking_records
    )

    print("M3.7C Watershed PRB Funding Priority")
    print(
        "Analytical projects: "
        f"{summary['analytical_project_count']}"
    )
    print(
        "Unique PRB Grand Totals: "
        f"{summary['unique_funding_priority_score_count']}"
    )
    print(
        "Tied score groups: "
        f"{summary['tied_score_group_count']}"
    )
    print(
        "Projects in tied score groups: "
        f"{summary['projects_in_tied_score_groups']}"
    )
    print(
        "Score range: "
        f"{summary['minimum_funding_priority_score']}-"
        f"{summary['maximum_funding_priority_score']}"
    )
    print(
        "Rank method: COMPETITION_RANK_DESCENDING"
    )
    print(
        "Tie policy: SHARED_SUBSTANTIVE_RANK"
    )
    print(
        "Display tiebreak: "
        "CANONICAL_PROJECT_ID_ASCENDING (non-analytical)"
    )
    print(
        "Portfolio selection authorized: false"
    )
    print(
        "Runtime integration authorized: false"
    )

    if args.verify_only:
        print(
            "Verify-only mode: no governed "
            "Funding Priority artifact written."
        )
        return 0

    content = render_artifact(
        ranking_records,
        summary,
    )

    result = write_artifact(
        args.output_path,
        content,
    )

    print(
        "Governed Funding Priority artifact: "
        f"{result}: {args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())