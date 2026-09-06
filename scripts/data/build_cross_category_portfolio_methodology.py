#!/usr/bin/env python3
"""Build the governed M3.7D cross-category portfolio-selection methodology."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PRIORITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "cross-category-prb-funding-priority.json"
)

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

OUTPUT_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "portfolio_methodology"
    / "cross-category-portfolio-methodology.json"
)

EXPECTED_PROJECT_COUNT = 106
EXPECTED_REQUEST_TOTAL = 1_973_520_000
HISTORICAL_MATCHED_COHORT_BUDGET = 332_000_000
HISTORICAL_FULL_PACKAGE_REFERENCE = 700_000_000
HISTORICAL_CITYWIDE_CAPACITY_REFERENCE = 750_000_000

ARTIFACT_VERSION = (
    "m3.7d-cross-category-portfolio-methodology/1.0.0"
)

MODEL_SCOPE = "CROSS_CATEGORY_PRB_PROJECT_MODEL"


class MethodologyError(RuntimeError):
    """Raised when the M3.7D methodology prerequisites are invalid."""


class DerivedArtifactConflictError(MethodologyError):
    """Raised when a differing governed artifact already exists."""


def load_json(path: Path) -> dict[str, object]:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def validate_prerequisites() -> tuple[
    dict[str, object],
    dict[str, object],
]:
    priority = load_json(
        PRIORITY_PATH
    )

    reconciliation = load_json(
        RECONCILIATION_PATH
    )

    if (
        priority.get(
            "model_scope"
        )
        != MODEL_SCOPE
    ):
        raise MethodologyError(
            "Unexpected M3.7F model scope."
        )

    if (
        priority.get(
            "cross_category_ranking_authorized"
        )
        is not True
    ):
        raise MethodologyError(
            "Cross-category ranking must "
            "already be authorized."
        )

    if (
        priority.get(
            "portfolio_selection_authorized"
        )
        is not False
    ):
        raise MethodologyError(
            "M3.7F predecessor must keep "
            "portfolio selection unauthorized."
        )

    if (
        priority.get(
            "runtime_integration_authorized"
        )
        is not False
    ):
        raise MethodologyError(
            "M3.7F predecessor must keep "
            "runtime integration unauthorized."
        )

    priority_records = priority.get(
        "records"
    )

    reconciliation_records = (
        reconciliation.get(
            "records"
        )
    )

    if not isinstance(
        priority_records,
        list,
    ):
        raise MethodologyError(
            "Priority records must be a list."
        )

    if not isinstance(
        reconciliation_records,
        list,
    ):
        raise MethodologyError(
            "Reconciliation records "
            "must be a list."
        )

    if (
        len(priority_records)
        != EXPECTED_PROJECT_COUNT
    ):
        raise MethodologyError(
            "Expected 106 Funding Priority "
            "records."
        )

    if (
        len(reconciliation_records)
        != EXPECTED_PROJECT_COUNT
    ):
        raise MethodologyError(
            "Expected 106 reconciliation "
            "records."
        )

    priority_ids = {
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in priority_records
    }

    reconciliation_ids = {
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record
        in reconciliation_records
    }

    if (
        priority_ids
        != reconciliation_ids
    ):
        raise MethodologyError(
            "M3.7F priority identities "
            "do not match reconciliation."
        )

    request_total = sum(
        int(
            record[
                "model_request_dollars"
            ]
        )
        for record
        in reconciliation_records
    )

    if (
        request_total
        != EXPECTED_REQUEST_TOTAL
    ):
        raise MethodologyError(
            "Governed request total changed."
        )

    return (
        priority,
        reconciliation,
    )


def build_artifact() -> dict[str, object]:
    (
        priority,
        reconciliation,
    ) = validate_prerequisites()

    priority_records = priority[
        "records"
    ]

    reconciliation_records = (
        reconciliation[
            "records"
        ]
    )

    requests = {
        str(
            record[
                "decision_unit_id"
            ]
        ): int(
            record[
                "model_request_dollars"
            ]
        )
        for record
        in reconciliation_records
    }

    maximum_project_request = max(
        requests.values()
    )

    minimum_project_request = min(
        requests.values()
    )

    return {
        "artifact_version": (
            ARTIFACT_VERSION
        ),
        "governance_checkpoint": (
            "M3.7D"
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
            True
        ),
        "runtime_integration_authorized": (
            False
        ),
        "methodology_name": (
            "PRIORITY_CONSTRAINED_"
            "ANALYST_GOVERNED_"
            "PORTFOLIO_CONSTRUCTION"
        ),
        "methodology_interpretation": (
            "DECISION_SUPPORT_NOT_"
            "CARDINAL_UTILITY_OPTIMIZATION"
        ),
        "source_artifacts": {
            "funding_priority": (
                "data/governed/"
                "cross_category/"
                "funding_priority/"
                "cross-category-prb-"
                "funding-priority.json"
            ),
            "prb_reconciliation": (
                "data/governed/"
                "cross_category/"
                "reconciliation/"
                "cross-category-prb-"
                "reconciliation.json"
            ),
            "budget_scope_audit": (
                "scripts/data/"
                "audit_cross_category_"
                "portfolio_budget_"
                "structure.py"
            ),
            "rank_cost_frontier_audit": (
                "scripts/data/"
                "audit_cross_category_"
                "rank_cost_frontier.py"
            ),
            "official_constraint_audit": (
                "scripts/data/"
                "audit_cross_category_"
                "official_portfolio_"
                "constraints.py"
            ),
        },
        "machine_operational_inputs": [
            "MODEL_ELIGIBILITY",
            "OFFICIAL_PRB_ORDINAL_"
            "FUNDING_PRIORITY",
            "GOVERNED_MODEL_REQUEST_"
            "DOLLARS",
            "ANALYST_SUPPLIED_"
            "AVAILABLE_PROJECT_BUDGET",
        ],
        "project_funding_semantics": {
            "funding_unit": (
                "FULL_PROJECT_REQUEST"
            ),
            "project_indivisible": (
                True
            ),
            "partial_funding_authorized": (
                False
            ),
            "cost_authority": (
                "GOVERNED_MODEL_REQUEST_"
                "DOLLARS"
            ),
        },
        "budget_policy": {
            "available_project_budget": (
                "ANALYST_SUPPLIED_SCENARIO_INPUT"
            ),
            "hard_budget_rule": (
                "SUM_SELECTED_MODEL_REQUEST_"
                "DOLLARS_LE_AVAILABLE_"
                "PROJECT_BUDGET"
            ),
            "historical_matched_cohort_budget_dollars": (
                HISTORICAL_MATCHED_COHORT_BUDGET
            ),
            "historical_matched_cohort_role": (
                "BENCHMARK_COMPARISON_SCENARIO"
            ),
            "historical_full_package_dollars": (
                HISTORICAL_FULL_PACKAGE_REFERENCE
            ),
            "historical_full_package_role": (
                "BENCHMARK_OUTCOME_REFERENCE"
            ),
            "historical_citywide_capacity_reference_dollars": (
                HISTORICAL_CITYWIDE_CAPACITY_REFERENCE
            ),
            "historical_citywide_capacity_role": (
                "CITYWIDE_REFERENCE_NOT_"
                "106_PROJECT_BUDGET"
            ),
            "historical_category_allocations_as_constraints": (
                False
            ),
        },
        "priority_policy": {
            "authority": (
                "OFFICIAL_PRB_GRAND_TOTAL"
            ),
            "interpretation": (
                "ORDINAL"
            ),
            "processing_order": (
                "DESCENDING_PRIORITY_TIERS"
            ),
            "equal_score_policy": (
                "SHARED_SUBSTANTIVE_PRIORITY"
            ),
            "display_order_has_analytical_meaning": (
                False
            ),
        },
        "selection_state_machine": {
            "complete_tier_fits": (
                "AUTO_INCLUDE_COMPLETE_TIER"
            ),
            "complete_tier_does_not_fit": (
                "BOUNDARY_PRIORITY_TIER"
            ),
            "boundary_no_project_fits": (
                "NO_SELECTION_FROM_TIER_"
                "BUDGET_INFEASIBLE"
            ),
            "boundary_exactly_one_project_fits": (
                "AUTO_INCLUDE_UNIQUE_"
                "BUDGET_FEASIBLE_PROJECT"
            ),
            "boundary_multiple_projects_fit": (
                "ANALYST_RESOLUTION_REQUIRED"
            ),
            "same_tier_project_still_fits_after_analyst_choice": (
                "WARN_HIGHER_PRIORITY_"
                "FEASIBLE_PROJECT_REMAINS"
            ),
            "lower_tier_advancement_with_feasible_higher_priority_project": (
                "EXPLICIT_ANALYST_OVERRIDE_REQUIRED"
            ),
        },
        "forbidden_machine_objectives": [
            "MAXIMIZE_SUM_PRB_GRAND_TOTAL",
            "MAXIMIZE_SCORE_PER_DOLLAR",
            "MINIMIZE_PROJECT_COST",
            "MAXIMIZE_PROJECT_COUNT",
            "MAXIMIZE_BUDGET_UTILIZATION",
            "MAXIMIZE_INDIVIDUAL_PRB_COMPONENT",
            "CATEGORY_NORMALIZATION",
            "HISTORICAL_RECOMMENDATION_MATCHING",
        ],
        "forbidden_automatic_tiebreakers": [
            "PROJECT_COST",
            "DECISION_UNIT_ID",
            "PROJECT_NAME",
            "SOURCE_TABLE_ROW_ORDER",
            "JANUARY_INITIAL_RECOMMENDATION",
            "INDIVIDUAL_PRB_COMPONENT",
            "COUNCIL_DISTRICT",
            "OM_IMPACT",
            "RNA_GEOMETRY",
            "FEMA_FLOODPLAIN_CONTEXT",
            "EAZ_2021_CONTEXT",
            "WATERSHED_PROBLEM_SCORE_CONTEXT",
        ],
        "analyst_review_context": {
            "council_district": {
                "role": (
                    "REPORTING_AND_ANALYST_REVIEW"
                ),
                "hard_constraint": (
                    False
                ),
                "reason": (
                    "NO_ADOPTED_REPRODUCIBLE_"
                    "PROJECT_SELECTION_QUOTA"
                ),
            },
            "om_impact": {
                "role": (
                    "CONTEXT_AND_WARNING"
                ),
                "hard_constraint": (
                    False
                ),
                "reason": (
                    "BOOLEAN_FIELD_NOT_"
                    "QUANTIFIED_PORTFOLIO_COST"
                ),
            },
            "six_year_deliverability": {
                "role": (
                    "ANALYST_REVIEW_ONLY"
                ),
                "hard_constraint": (
                    False
                ),
                "reason": (
                    "NO_GOVERNED_PROJECT_LEVEL_"
                    "DELIVERY_CAPACITY_MODEL"
                ),
            },
            "preventative_maintenance": {
                "role": (
                    "ANALYST_REVIEW_ONLY"
                ),
                "hard_constraint": (
                    False
                ),
                "reason": (
                    "NO_COMPLETE_GOVERNED_"
                    "PROJECT_LEVEL_AVOIDED_"
                    "COST_MEASURE"
                ),
            },
        },
        "double_counting_policy": {
            "matching_funds_additional_rule": (
                False
            ),
            "strategic_alignment_additional_rule": (
                False
            ),
            "om_additional_score_preference": (
                False
            ),
        },
        "historical_outcome_isolation": {
            "historical_category_allocations_used_for_selection": (
                False
            ),
            "historical_project_membership_used_for_selection": (
                False
            ),
            "historical_recommendation_role": (
                "BENCHMARK_OUTCOME_ONLY"
            ),
        },
        "summary": {
            "analytical_project_count": (
                EXPECTED_PROJECT_COUNT
            ),
            "governed_request_total_dollars": (
                EXPECTED_REQUEST_TOTAL
            ),
            "maximum_project_request_dollars": (
                maximum_project_request
            ),
            "minimum_project_request_dollars": (
                minimum_project_request
            ),
            "funding_priority_unique_score_count": (
                priority[
                    "summary"
                ][
                    "unique_funding_priority_score_count"
                ]
            ),
            "tied_score_group_count": (
                priority[
                    "summary"
                ][
                    "tied_score_group_count"
                ]
            ),
            "projects_in_tied_score_groups": (
                priority[
                    "summary"
                ][
                    "projects_in_tied_score_groups"
                ]
            ),
        },
    }


def serialized_artifact() -> str:
    return (
        json.dumps(
            build_artifact(),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )


def write_artifact() -> str:
    rendered = serialized_artifact()

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if OUTPUT_PATH.exists():
        existing = OUTPUT_PATH.read_text(
            encoding="utf-8"
        )

        if existing == rendered:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Governed portfolio methodology "
            "artifact already exists with "
            "different content."
        )

    OUTPUT_PATH.write_text(
        rendered,
        encoding="utf-8",
    )

    return "created"


def main() -> int:
    result = write_artifact()

    print(
        "M3.7D portfolio methodology:",
        result,
    )

    artifact = build_artifact()

    print(
        "Portfolio selection authorized:",
        artifact[
            "portfolio_selection_authorized"
        ],
    )

    print(
        "Runtime integration authorized:",
        artifact[
            "runtime_integration_authorized"
        ],
    )

    print(
        "Methodology:",
        artifact[
            "methodology_name"
        ],
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
