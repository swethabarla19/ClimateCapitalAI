#!/usr/bin/env python3
"""Build governed M3.7F cross-category PRB Funding Priority."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader

if __package__:
    from . import audit_cross_category_prb_baseline_criteria as baseline_audit
else:
    import audit_cross_category_prb_baseline_criteria as baseline_audit


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

MODEL_SCOPE = "CROSS_CATEGORY_PRB_PROJECT_MODEL"

ARTIFACT_VERSION = (
    "m3.7f-cross-category-prb-funding-priority/1.0.0"
)

EXPECTED_PROJECT_COUNT = 106

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}

EXPECTED_UNIQUE_SCORE_COUNT = 35
EXPECTED_TIE_GROUP_COUNT = 24
EXPECTED_TIED_PROJECT_COUNT = 95

EXPECTED_MAX_SCORE = Decimal("83")
EXPECTED_MIN_SCORE = Decimal("40")

EXPECTED_HALF_POINT_SCORES = {
    Decimal("54.5"),
    Decimal("53.5"),
    Decimal("50.5"),
}

DEFAULT_ELIGIBILITY_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "cross-category-prb-model-eligibility.json"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "cross-category-prb-funding-priority.json"
)


class FundingPriorityError(RuntimeError):
    """Raised when Funding Priority cannot be built without guessing."""


class DerivedArtifactConflictError(FundingPriorityError):
    """Raised when a differing governed artifact already exists."""


def decimal_score(value: object) -> Decimal:
    if isinstance(value, bool):
        raise FundingPriorityError(
            "PRB Grand Total cannot be boolean."
        )

    if not isinstance(
        value,
        (int, float),
    ):
        raise FundingPriorityError(
            "PRB Grand Total must be numeric."
        )

    score = Decimal(str(value))

    if score < 0 or score > 100:
        raise FundingPriorityError(
            "PRB Grand Total must be between 0 and 100."
        )

    doubled = score * Decimal("2")

    if doubled != doubled.to_integral_value():
        raise FundingPriorityError(
            "PRB Grand Total must use whole- or half-point increments."
        )

    return score


def json_score(score: Decimal) -> int | float:
    if score == score.to_integral_value():
        return int(score)

    return float(score)


def load_eligibility(
    path: Path,
) -> dict[str, object]:
    artifact = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        artifact,
        dict,
    ):
        raise FundingPriorityError(
            "M3.7E-B eligibility artifact must be a JSON object."
        )

    if (
        artifact.get(
            "governance_checkpoint"
        )
        != "M3.7E-B"
    ):
        raise FundingPriorityError(
            "M3.7F requires the governed M3.7E-B eligibility artifact."
        )

    if (
        artifact.get("model_scope")
        != MODEL_SCOPE
    ):
        raise FundingPriorityError(
            "M3.7E-B model scope does not match the "
            "cross-category PRB project model."
        )

    if (
        artifact.get(
            "cross_category_ranking_authorized"
        )
        is not False
    ):
        raise FundingPriorityError(
            "M3.7F expects the predecessor artifact "
            "to leave ranking unauthorized."
        )

    if (
        artifact.get(
            "portfolio_selection_authorized"
        )
        is not False
    ):
        raise FundingPriorityError(
            "Portfolio selection must remain unauthorized."
        )

    if (
        artifact.get(
            "runtime_integration_authorized"
        )
        is not False
    ):
        raise FundingPriorityError(
            "Runtime integration must remain unauthorized."
        )

    return artifact


def validate_baseline_prerequisite() -> None:
    checksum = (
        baseline_audit
        .non_watershed
        .validate_source_checksum(
            baseline_audit.SOURCE_PATH,
            baseline_audit.REGISTRY_PATH,
        )
    )

    if not checksum.startswith(
        "sha256:"
    ):
        raise FundingPriorityError(
            "PRB source checksum verification failed."
        )

    reader = PdfReader(
        baseline_audit.SOURCE_PATH
    )

    records = (
        baseline_audit.audit_non_watershed(
            reader
        )
        + baseline_audit.audit_watershed(
            reader
        )
    )

    if len(records) != EXPECTED_PROJECT_COUNT:
        raise FundingPriorityError(
            "Baseline prerequisite audit did not return 106 projects."
        )

    failures = [
        record
        for record in records
        if not record[
            "baseline_satisfied"
        ]
    ]

    if failures:
        failed_ids = [
            str(
                record[
                    "decision_unit_id"
                ]
            )
            for record in failures
        ]

        raise FundingPriorityError(
            "One or more analytical projects "
            "fail the PRB baseline prerequisite: "
            f"{failed_ids}"
        )


def load_eligible_records(
    eligibility_path: Path,
) -> tuple[
    dict[str, object],
    ...,
]:
    artifact = load_eligibility(
        eligibility_path
    )

    records = artifact.get(
        "records"
    )

    if not isinstance(
        records,
        list,
    ):
        raise FundingPriorityError(
            "M3.7E-B eligibility artifact has no record list."
        )

    if len(records) != EXPECTED_PROJECT_COUNT:
        raise FundingPriorityError(
            f"Expected {EXPECTED_PROJECT_COUNT} "
            "M3.7E-B records; "
            f"found {len(records)}."
        )

    project_ids: list[str] = []
    category_counts = Counter()

    for record in records:
        if (
            record.get(
                "model_scope"
            )
            != MODEL_SCOPE
        ):
            raise FundingPriorityError(
                "Eligibility record has unexpected model scope."
            )

        if (
            record.get(
                "evidence_feasibility_status"
            )
            != "FEASIBLE"
        ):
            raise FundingPriorityError(
                "M3.7F cannot rank an evidence-infeasible project."
            )

        if (
            record.get(
                "model_eligible"
            )
            is not True
        ):
            raise FundingPriorityError(
                "M3.7F cannot rank a model-ineligible project."
            )

        if (
            record.get(
                "blocking_reason_codes"
            )
            != []
        ):
            raise FundingPriorityError(
                "Eligible ranking cohort must have "
                "no blocking reason codes."
            )

        decision_unit_id = record.get(
            "decision_unit_id"
        )

        if (
            not isinstance(
                decision_unit_id,
                str,
            )
            or not decision_unit_id
        ):
            raise FundingPriorityError(
                "Eligible project is missing decision_unit_id."
            )

        category = record.get(
            "presentation_category"
        )

        if (
            not isinstance(
                category,
                str,
            )
            or category
            not in EXPECTED_CATEGORY_COUNTS
        ):
            raise FundingPriorityError(
                "Eligible project has unexpected presentation category."
            )

        decimal_score(
            record.get(
                "prb_grand_total"
            )
        )

        project_ids.append(
            decision_unit_id
        )

        category_counts[
            category
        ] += 1

    if (
        len(project_ids)
        != len(
            set(project_ids)
        )
    ):
        raise FundingPriorityError(
            "decision_unit_id values must be unique."
        )

    if dict(
        category_counts
    ) != EXPECTED_CATEGORY_COUNTS:
        raise FundingPriorityError(
            "Cross-category eligibility counts changed unexpectedly: "
            f"{dict(category_counts)}"
        )

    return tuple(records)


def build_ranking_records(
    eligible_records: tuple[
        dict[str, object],
        ...,
    ],
) -> tuple[
    dict[str, object],
    ...,
]:
    ordered = sorted(
        eligible_records,
        key=lambda record: (
            -decimal_score(
                record[
                    "prb_grand_total"
                ]
            ),
            str(
                record[
                    "decision_unit_id"
                ]
            ),
        ),
    )

    score_counts = Counter(
        decimal_score(
            record[
                "prb_grand_total"
            ]
        )
        for record in ordered
    )

    display_positions: dict[
        Decimal,
        int,
    ] = {}

    output: list[
        dict[str, object]
    ] = []

    previous_score: (
        Decimal
        | None
    ) = None

    current_rank: (
        int
        | None
    ) = None

    for position, record in enumerate(
        ordered,
        start=1,
    ):
        score = decimal_score(
            record[
                "prb_grand_total"
            ]
        )

        if score != previous_score:
            current_rank = position
            previous_score = score

        if current_rank is None:
            raise FundingPriorityError(
                "Competition rank failed to initialize."
            )

        display_positions[
            score
        ] = (
            display_positions.get(
                score,
                0,
            )
            + 1
        )

        output.append(
            {
                "decision_unit_id": str(
                    record[
                        "decision_unit_id"
                    ]
                ),
                "canonical_project_id": (
                    record.get(
                        "canonical_project_id"
                    )
                ),
                "presentation_category": str(
                    record[
                        "presentation_category"
                    ]
                ),
                "model_scope": MODEL_SCOPE,
                "funding_priority_score": (
                    json_score(score)
                ),
                "funding_priority_rank": (
                    current_rank
                ),
                "is_tied": (
                    score_counts[
                        score
                    ]
                    > 1
                ),
                "tie_group_size": (
                    score_counts[
                        score
                    ]
                ),
                "display_order_within_tie": (
                    display_positions[
                        score
                    ]
                ),
                "display_tiebreak_has_analytical_meaning": (
                    False
                ),
            }
        )

    return tuple(output)


def validate_ranking_records(
    records: tuple[
        dict[str, object],
        ...,
    ],
) -> dict[str, object]:
    if len(records) != EXPECTED_PROJECT_COUNT:
        raise FundingPriorityError(
            f"Expected {EXPECTED_PROJECT_COUNT} "
            "ranking records; "
            f"found {len(records)}."
        )

    project_ids = [
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
    ]

    if (
        len(project_ids)
        != len(
            set(project_ids)
        )
    ):
        raise FundingPriorityError(
            "Ranking decision_unit_ids must be unique."
        )

    scores = [
        decimal_score(
            record[
                "funding_priority_score"
            ]
        )
        for record in records
    ]

    score_counts = Counter(
        scores
    )

    unique_score_count = len(
        score_counts
    )

    tied_score_group_count = sum(
        1
        for count
        in score_counts.values()
        if count > 1
    )

    tied_project_count = sum(
        count
        for count
        in score_counts.values()
        if count > 1
    )

    maximum_score = max(
        scores
    )

    minimum_score = min(
        scores
    )

    half_point_scores = {
        score
        for score in score_counts
        if score
        != score.to_integral_value()
    }

    if (
        unique_score_count
        != EXPECTED_UNIQUE_SCORE_COUNT
    ):
        raise FundingPriorityError(
            "Unique Funding Priority score count changed unexpectedly."
        )

    if (
        tied_score_group_count
        != EXPECTED_TIE_GROUP_COUNT
    ):
        raise FundingPriorityError(
            "Tied score-group count changed unexpectedly."
        )

    if (
        tied_project_count
        != EXPECTED_TIED_PROJECT_COUNT
    ):
        raise FundingPriorityError(
            "Tied project count changed unexpectedly."
        )

    if (
        maximum_score
        != EXPECTED_MAX_SCORE
        or minimum_score
        != EXPECTED_MIN_SCORE
    ):
        raise FundingPriorityError(
            "Funding Priority score range changed unexpectedly."
        )

    if (
        half_point_scores
        != EXPECTED_HALF_POINT_SCORES
    ):
        raise FundingPriorityError(
            "Half-point Funding Priority scores changed unexpectedly: "
            f"{sorted(half_point_scores)}"
        )

    previous_score: (
        Decimal
        | None
    ) = None

    expected_rank: (
        int
        | None
    ) = None

    for position, record in enumerate(
        records,
        start=1,
    ):
        score = decimal_score(
            record[
                "funding_priority_score"
            ]
        )

        if score != previous_score:
            expected_rank = position
            previous_score = score

        if (
            record[
                "funding_priority_rank"
            ]
            != expected_rank
        ):
            raise FundingPriorityError(
                "Funding Priority rank is not "
                "deterministic competition ranking."
            )

    for score in score_counts:
        group = [
            record
            for record in records
            if decimal_score(
                record[
                    "funding_priority_score"
                ]
            )
            == score
        ]

        ids = [
            str(
                record[
                    "decision_unit_id"
                ]
            )
            for record in group
        ]

        if ids != sorted(ids):
            raise FundingPriorityError(
                "Tie display order is not "
                "decision_unit_id ascending."
            )

        expected_positions = list(
            range(
                1,
                len(group) + 1,
            )
        )

        actual_positions = [
            int(
                record[
                    "display_order_within_tie"
                ]
            )
            for record in group
        ]

        if (
            actual_positions
            != expected_positions
        ):
            raise FundingPriorityError(
                "Tie display positions are not deterministic."
            )

        if any(
            record[
                "display_tiebreak_has_analytical_meaning"
            ]
            is not False
            for record in group
        ):
            raise FundingPriorityError(
                "Display tiebreak must have no analytical meaning."
            )

    category_counts = Counter(
        str(
            record[
                "presentation_category"
            ]
        )
        for record in records
    )

    if dict(
        category_counts
    ) != EXPECTED_CATEGORY_COUNTS:
        raise FundingPriorityError(
            "Ranking category counts changed unexpectedly."
        )

    return {
        "analytical_project_count": (
            len(records)
        ),
        "category_counts": (
            EXPECTED_CATEGORY_COUNTS
        ),
        "unique_funding_priority_score_count": (
            unique_score_count
        ),
        "tied_score_group_count": (
            tied_score_group_count
        ),
        "projects_in_tied_score_groups": (
            tied_project_count
        ),
        "maximum_funding_priority_score": (
            json_score(
                maximum_score
            )
        ),
        "minimum_funding_priority_score": (
            json_score(
                minimum_score
            )
        ),
        "half_point_score_count": (
            len(
                half_point_scores
            )
        ),
    }


def render_artifact(
    records: tuple[
        dict[str, object],
        ...,
    ],
    summary: dict[
        str,
        object,
    ],
) -> bytes:
    artifact = {
        "artifact_version": (
            ARTIFACT_VERSION
        ),
        "governance_checkpoint": (
            "M3.7F"
        ),
        "historical_decision_snapshot_date": (
            "2026-01-21"
        ),
        "model_scope": (
            MODEL_SCOPE
        ),
        "cross_category_ranking_authorized": (
            True
        ),
        "portfolio_selection_authorized": (
            False
        ),
        "runtime_integration_authorized": (
            False
        ),
        "source_artifacts": {
            "model_eligibility": (
                "data/governed/cross_category/"
                "model_eligibility/"
                "cross-category-prb-model-eligibility.json"
            ),
            "prb_reconciliation": (
                "data/governed/cross_category/"
                "reconciliation/"
                "cross-category-prb-reconciliation.json"
            ),
            "baseline_criteria_audit": (
                "scripts/data/"
                "audit_cross_category_prb_baseline_criteria.py"
            ),
        },
        "comparability_policy": {
            "decision": (
                "AUTHORIZED_FOR_COMMON_ORDINAL_PRIORITY"
            ),
            "basis": [
                (
                    "COMMON_OFFICIAL_PRB_RUBRIC"
                ),
                (
                    "COMMON_SIX_COMPONENT_WEIGHTED_STRUCTURE"
                ),
                (
                    "COMMON_ZERO_TO_100_GRAND_TOTAL_SCALE"
                ),
                (
                    "ALL_106_SATISFY_PRB_BASELINE_PREREQUISITE"
                ),
                (
                    "ALL_106_HAVE_COMPLETE_VALID_PRB_SCORE_VECTORS"
                ),
            ],
            "interpretation": (
                "ORDINAL_PRB_BASED_PROJECT_PRIORITY"
            ),
            "not_authorized_interpretations": [
                "CARDINAL_PUBLIC_BENEFIT",
                "COST_EFFECTIVENESS",
                "BENEFIT_COST_RATIO",
                "HISTORICAL_RECOMMENDATION_PROBABILITY",
                "ADDITIVE_PORTFOLIO_UTILITY",
            ],
            "reviewer_calibration_limitation": (
                "COMMON_RUBRIC_DOES_NOT_PROVE_PERFECT "
                "CROSS_DEPARTMENT_REVIEWER_CALIBRATION"
            ),
            "normalization_authorized": (
                False
            ),
        },
        "ranking_policy": {
            "funding_priority_score_authority": (
                "OFFICIAL_PRB_GRAND_TOTAL"
            ),
            "direction": (
                "HIGHER_IS_HIGHER_PRIORITY"
            ),
            "rank_method": (
                "COMPETITION_RANK_DESCENDING"
            ),
            "tie_policy": (
                "SHARED_SUBSTANTIVE_RANK"
            ),
            "display_tiebreak": (
                "DECISION_UNIT_ID_ASCENDING"
            ),
            "display_tiebreak_has_analytical_meaning": (
                False
            ),
            "forbidden_score_transformations": [
                "CATEGORY_NORMALIZATION",
                "Z_SCORE_NORMALIZATION",
                "PERCENTILE_NORMALIZATION",
                "SCORE_PER_DOLLAR",
                "INVENTED_CLIMATE_CAPITAL_WEIGHTS",
            ],
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
        "records": list(
            records
        ),
    }

    return (
        json.dumps(
            artifact,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    ).encode(
        "utf-8"
    )


def write_artifact(
    output_path: Path,
    content: bytes,
) -> str:
    if output_path.exists():
        existing = (
            output_path.read_bytes()
        )

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite differing "
            "governed Funding Priority artifact: "
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
        "--eligibility-path",
        type=Path,
        default=(
            DEFAULT_ELIGIBILITY_PATH
        ),
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

    validate_baseline_prerequisite()

    eligible_records = (
        load_eligible_records(
            args.eligibility_path
        )
    )

    ranking_records = (
        build_ranking_records(
            eligible_records
        )
    )

    summary = (
        validate_ranking_records(
            ranking_records
        )
    )

    print(
        "M3.7F Cross-Category PRB Funding Priority"
    )

    print(
        "Analytical projects:",
        summary[
            "analytical_project_count"
        ],
    )

    print(
        "Unique PRB Grand Totals:",
        summary[
            "unique_funding_priority_score_count"
        ],
    )

    print(
        "Tied score groups:",
        summary[
            "tied_score_group_count"
        ],
    )

    print(
        "Projects in tied score groups:",
        summary[
            "projects_in_tied_score_groups"
        ],
    )

    print(
        "Score range:",
        f"{summary['minimum_funding_priority_score']}-"
        f"{summary['maximum_funding_priority_score']}",
    )

    print(
        "Rank method: "
        "COMPETITION_RANK_DESCENDING"
    )

    print(
        "Tie policy: "
        "SHARED_SUBSTANTIVE_RANK"
    )

    print(
        "Display tiebreak: "
        "DECISION_UNIT_ID_ASCENDING "
        "(non-analytical)"
    )

    print(
        "Cross-category ranking authorized: true"
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
        "Governed Funding Priority artifact:",
        f"{result}:",
        args.output_path,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )