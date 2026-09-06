"""Governance tests for M3.7D cross-category portfolio methodology."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

import pytest
from pypdf import PdfReader

from scripts.data import (
    audit_cross_category_official_portfolio_constraints as constraints,
)
from scripts.data import (
    build_cross_category_portfolio_methodology as portfolio,
)


ROOT = Path(__file__).resolve().parents[2]

METHODOLOGY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "portfolio_methodology"
    / "cross-category-portfolio-methodology.json"
)

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


def load_methodology() -> dict:
    return json.loads(
        METHODOLOGY_PATH.read_text(
            encoding="utf-8"
        )
    )


def load_priority() -> dict:
    return json.loads(
        PRIORITY_PATH.read_text(
            encoding="utf-8"
        )
    )


def load_reconciliation() -> dict:
    return json.loads(
        RECONCILIATION_PATH.read_text(
            encoding="utf-8"
        )
    )


def boundary_for_budget(
    budget: int,
) -> dict[str, object]:
    priority = load_priority()
    reconciliation = load_reconciliation()

    requests = {
        row["decision_unit_id"]:
        int(row["model_request_dollars"])
        for row in reconciliation["records"]
    }

    groups = defaultdict(list)

    for row in priority["records"]:
        score = Decimal(
            str(
                row["funding_priority_score"]
            )
        )

        groups[score].append(
            {
                "decision_unit_id":
                    row["decision_unit_id"],
                "rank":
                    row["funding_priority_rank"],
                "cost":
                    requests[
                        row["decision_unit_id"]
                    ],
            }
        )

    cumulative = 0

    for score in sorted(
        groups,
        reverse=True,
    ):
        projects = groups[score]

        tier_cost = sum(
            project["cost"]
            for project in projects
        )

        if cumulative + tier_cost <= budget:
            cumulative += tier_cost
            continue

        remaining = (
            budget - cumulative
        )

        individually_fitting = [
            project
            for project in projects
            if project["cost"] <= remaining
        ]

        return {
            "score": score,
            "rank": projects[0]["rank"],
            "projects": projects,
            "tier_cost": tier_cost,
            "cumulative_before": cumulative,
            "remaining": remaining,
            "individually_fitting":
                individually_fitting,
        }

    raise AssertionError(
        "Expected budget boundary tier."
    )


def test_m3_7d_artifact_identity_and_authority_are_locked():
    artifact = load_methodology()

    assert (
        artifact["artifact_version"]
        == (
            "m3.7d-cross-category-"
            "portfolio-methodology/1.0.0"
        )
    )

    assert (
        artifact["governance_checkpoint"]
        == "M3.7D"
    )

    assert (
        artifact[
            "historical_decision_snapshot_date"
        ]
        == "2026-01-21"
    )

    assert (
        artifact["model_scope"]
        == "CROSS_CATEGORY_PRB_PROJECT_MODEL"
    )

    assert (
        artifact[
            "cross_category_ranking_authorized"
        ]
        is True
    )

    assert (
        artifact[
            "portfolio_selection_authorized"
        ]
        is True
    )

    assert (
        artifact[
            "runtime_integration_authorized"
        ]
        is False
    )


def test_methodology_name_and_interpretation_are_locked():
    artifact = load_methodology()

    assert (
        artifact["methodology_name"]
        == (
            "PRIORITY_CONSTRAINED_"
            "ANALYST_GOVERNED_"
            "PORTFOLIO_CONSTRUCTION"
        )
    )

    assert (
        artifact[
            "methodology_interpretation"
        ]
        == (
            "DECISION_SUPPORT_NOT_"
            "CARDINAL_UTILITY_OPTIMIZATION"
        )
    )


def test_machine_operational_inputs_are_exact():
    artifact = load_methodology()

    assert (
        artifact[
            "machine_operational_inputs"
        ]
        == [
            "MODEL_ELIGIBILITY",
            (
                "OFFICIAL_PRB_ORDINAL_"
                "FUNDING_PRIORITY"
            ),
            (
                "GOVERNED_MODEL_REQUEST_"
                "DOLLARS"
            ),
            (
                "ANALYST_SUPPLIED_"
                "AVAILABLE_PROJECT_BUDGET"
            ),
        ]
    )


def test_project_funding_is_full_request_and_indivisible():
    policy = load_methodology()[
        "project_funding_semantics"
    ]

    assert (
        policy["funding_unit"]
        == "FULL_PROJECT_REQUEST"
    )

    assert (
        policy["project_indivisible"]
        is True
    )

    assert (
        policy[
            "partial_funding_authorized"
        ]
        is False
    )

    assert (
        policy["cost_authority"]
        == (
            "GOVERNED_MODEL_REQUEST_"
            "DOLLARS"
        )
    )


def test_available_budget_is_analyst_scenario_input():
    policy = load_methodology()[
        "budget_policy"
    ]

    assert (
        policy[
            "available_project_budget"
        ]
        == (
            "ANALYST_SUPPLIED_SCENARIO_INPUT"
        )
    )

    assert (
        policy["hard_budget_rule"]
        == (
            "SUM_SELECTED_MODEL_REQUEST_"
            "DOLLARS_LE_AVAILABLE_"
            "PROJECT_BUDGET"
        )
    )


def test_historical_budget_roles_are_separate():
    policy = load_methodology()[
        "budget_policy"
    ]

    assert (
        policy[
            "historical_matched_cohort_budget_dollars"
        ]
        == 332_000_000
    )

    assert (
        policy[
            "historical_matched_cohort_role"
        ]
        == "BENCHMARK_COMPARISON_SCENARIO"
    )

    assert (
        policy[
            "historical_full_package_dollars"
        ]
        == 700_000_000
    )

    assert (
        policy[
            "historical_full_package_role"
        ]
        == "BENCHMARK_OUTCOME_REFERENCE"
    )

    assert (
        policy[
            "historical_citywide_capacity_reference_dollars"
        ]
        == 750_000_000
    )

    assert (
        policy[
            "historical_citywide_capacity_role"
        ]
        == (
            "CITYWIDE_REFERENCE_NOT_"
            "106_PROJECT_BUDGET"
        )
    )

    assert (
        policy[
            "historical_category_allocations_as_constraints"
        ]
        is False
    )


def test_priority_policy_preserves_ordinal_ties():
    policy = load_methodology()[
        "priority_policy"
    ]

    assert (
        policy["authority"]
        == "OFFICIAL_PRB_GRAND_TOTAL"
    )

    assert (
        policy["interpretation"]
        == "ORDINAL"
    )

    assert (
        policy["processing_order"]
        == "DESCENDING_PRIORITY_TIERS"
    )

    assert (
        policy["equal_score_policy"]
        == "SHARED_SUBSTANTIVE_PRIORITY"
    )

    assert (
        policy[
            "display_order_has_analytical_meaning"
        ]
        is False
    )


def test_selection_state_machine_is_locked():
    state = load_methodology()[
        "selection_state_machine"
    ]

    assert state == {
        "complete_tier_fits":
            "AUTO_INCLUDE_COMPLETE_TIER",
        "complete_tier_does_not_fit":
            "BOUNDARY_PRIORITY_TIER",
        "boundary_no_project_fits":
            (
                "NO_SELECTION_FROM_TIER_"
                "BUDGET_INFEASIBLE"
            ),
        "boundary_exactly_one_project_fits":
            (
                "AUTO_INCLUDE_UNIQUE_"
                "BUDGET_FEASIBLE_PROJECT"
            ),
        "boundary_multiple_projects_fit":
            "ANALYST_RESOLUTION_REQUIRED",
        (
            "same_tier_project_still_fits_"
            "after_analyst_choice"
        ):
            (
                "WARN_HIGHER_PRIORITY_"
                "FEASIBLE_PROJECT_REMAINS"
            ),
        (
            "lower_tier_advancement_with_"
            "feasible_higher_priority_project"
        ):
            (
                "EXPLICIT_ANALYST_OVERRIDE_"
                "REQUIRED"
            ),
    }


def test_cardinal_and_cost_efficiency_objectives_are_forbidden():
    forbidden = set(
        load_methodology()[
            "forbidden_machine_objectives"
        ]
    )

    assert forbidden == {
        "MAXIMIZE_SUM_PRB_GRAND_TOTAL",
        "MAXIMIZE_SCORE_PER_DOLLAR",
        "MINIMIZE_PROJECT_COST",
        "MAXIMIZE_PROJECT_COUNT",
        "MAXIMIZE_BUDGET_UTILIZATION",
        (
            "MAXIMIZE_INDIVIDUAL_"
            "PRB_COMPONENT"
        ),
        "CATEGORY_NORMALIZATION",
        (
            "HISTORICAL_RECOMMENDATION_"
            "MATCHING"
        ),
    }


def test_automatic_tiebreakers_are_forbidden():
    forbidden = set(
        load_methodology()[
            "forbidden_automatic_tiebreakers"
        ]
    )

    assert forbidden == {
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
        (
            "WATERSHED_PROBLEM_"
            "SCORE_CONTEXT"
        ),
    }


def test_council_district_is_review_not_hard_constraint():
    policy = load_methodology()[
        "analyst_review_context"
    ][
        "council_district"
    ]

    assert (
        policy["role"]
        == "REPORTING_AND_ANALYST_REVIEW"
    )

    assert (
        policy["hard_constraint"]
        is False
    )


def test_om_is_context_not_portfolio_cap():
    policy = load_methodology()[
        "analyst_review_context"
    ][
        "om_impact"
    ]

    assert (
        policy["role"]
        == "CONTEXT_AND_WARNING"
    )

    assert (
        policy["hard_constraint"]
        is False
    )


def test_deliverability_and_preventative_maintenance_are_review_only():
    context = load_methodology()[
        "analyst_review_context"
    ]

    assert (
        context[
            "six_year_deliverability"
        ][
            "role"
        ]
        == "ANALYST_REVIEW_ONLY"
    )

    assert (
        context[
            "six_year_deliverability"
        ][
            "hard_constraint"
        ]
        is False
    )

    assert (
        context[
            "preventative_maintenance"
        ][
            "role"
        ]
        == "ANALYST_REVIEW_ONLY"
    )

    assert (
        context[
            "preventative_maintenance"
        ][
            "hard_constraint"
        ]
        is False
    )


def test_double_counting_is_explicitly_prohibited():
    policy = load_methodology()[
        "double_counting_policy"
    ]

    assert (
        policy[
            "matching_funds_additional_rule"
        ]
        is False
    )

    assert (
        policy[
            "strategic_alignment_additional_rule"
        ]
        is False
    )

    assert (
        policy[
            "om_additional_score_preference"
        ]
        is False
    )


def test_historical_outcomes_are_isolated():
    policy = load_methodology()[
        "historical_outcome_isolation"
    ]

    assert (
        policy[
            "historical_category_allocations_used_for_selection"
        ]
        is False
    )

    assert (
        policy[
            "historical_project_membership_used_for_selection"
        ]
        is False
    )

    assert (
        policy[
            "historical_recommendation_role"
        ]
        == "BENCHMARK_OUTCOME_ONLY"
    )


def test_summary_preserves_106_project_universe():
    summary = load_methodology()[
        "summary"
    ]

    assert (
        summary[
            "analytical_project_count"
        ]
        == 106
    )

    assert (
        summary[
            "governed_request_total_dollars"
        ]
        == 1_973_520_000
    )

    assert (
        summary[
            "funding_priority_unique_score_count"
        ]
        == 35
    )

    assert (
        summary[
            "tied_score_group_count"
        ]
        == 24
    )

    assert (
        summary[
            "projects_in_tied_score_groups"
        ]
        == 95
    )


def test_m3_7f_predecessor_remains_non_portfolio_artifact():
    predecessor = load_priority()

    assert (
        predecessor[
            "cross_category_ranking_authorized"
        ]
        is True
    )

    assert (
        predecessor[
            "portfolio_selection_authorized"
        ]
        is False
    )

    assert (
        predecessor[
            "runtime_integration_authorized"
        ]
        is False
    )


def test_reconciliation_and_priority_identity_sets_match():
    priority_ids = {
        row["decision_unit_id"]
        for row in load_priority()[
            "records"
        ]
    }

    reconciliation_ids = {
        row["decision_unit_id"]
        for row in load_reconciliation()[
            "records"
        ]
    }

    assert len(priority_ids) == 106
    assert len(reconciliation_ids) == 106
    assert (
        priority_ids
        == reconciliation_ids
    )


def test_governed_request_total_is_exact():
    total = sum(
        int(
            row["model_request_dollars"]
        )
        for row in load_reconciliation()[
            "records"
        ]
    )

    assert total == 1_973_520_000


def test_332m_boundary_is_uniquely_resolved_by_budget_feasibility():
    boundary = boundary_for_budget(
        332_000_000
    )

    assert (
        boundary["score"]
        == Decimal("72")
    )

    assert (
        boundary["rank"]
        == 13
    )

    assert (
        boundary[
            "cumulative_before"
        ]
        == 281_950_000
    )

    assert (
        boundary["remaining"]
        == 50_050_000
    )

    assert (
        boundary["tier_cost"]
        == 91_000_000
    )

    fitting = boundary[
        "individually_fitting"
    ]

    assert len(fitting) == 1

    assert (
        fitting[0][
            "decision_unit_id"
        ]
        == (
            "transportation/"
            "act-plan-7th-street"
        )
    )

    assert (
        fitting[0]["cost"]
        == 40_000_000
    )


def test_700m_boundary_requires_analyst_resolution():
    boundary = boundary_for_budget(
        700_000_000
    )

    assert (
        boundary["score"]
        == Decimal("67")
    )

    assert (
        boundary["rank"]
        == 28
    )

    assert (
        boundary[
            "cumulative_before"
        ]
        == 591_725_000
    )

    assert (
        boundary["remaining"]
        == 108_275_000
    )

    assert (
        boundary["tier_cost"]
        == 113_000_000
    )

    assert (
        len(
            boundary[
                "individually_fitting"
            ]
        )
        == 5
    )


def test_750m_boundary_requires_analyst_resolution():
    boundary = boundary_for_budget(
        750_000_000
    )

    assert (
        boundary["score"]
        == Decimal("65")
    )

    assert (
        boundary["rank"]
        == 37
    )

    assert (
        boundary[
            "cumulative_before"
        ]
        == 716_720_000
    )

    assert (
        boundary["remaining"]
        == 33_280_000
    )

    assert (
        boundary["tier_cost"]
        == 93_850_000
    )

    assert (
        len(
            boundary[
                "individually_fitting"
            ]
        )
        == 8
    )


def test_b0_structured_source_coverage_is_locked():
    checksum = (
        constraints
        .non_watershed
        .validate_source_checksum(
            constraints.SOURCE_PATH,
            constraints.REGISTRY_PATH,
        )
    )

    assert checksum == (
        "sha256:"
        "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359"
    )

    reconciliation = (
        load_reconciliation()
    )

    january_requests = {}

    for record in reconciliation[
        "records"
    ]:
        decision_unit_id = str(
            record["decision_unit_id"]
        )

        request = record.get(
            "january_request_dollars"
        )

        if request is None:
            request = record[
                "model_request_dollars"
            ]

        january_requests[
            decision_unit_id
        ] = int(request)

    reader = PdfReader(
        constraints.SOURCE_PATH
    )

    records = [
        *constraints.extract_non_watershed(
            reader,
            january_requests,
        ),
        *constraints.extract_watershed(
            reader,
            january_requests,
        ),
    ]

    assert len(records) == 106

    om_counts = Counter(
        record["om_impact"]
        for record in records
    )

    assert om_counts == {
        "no": 74,
        "yes": 32,
    }

    district_counts = Counter(
        constraints.district_type(
            str(
                record[
                    "council_district"
                ]
            )
        )
        for record in records
    )

    assert district_counts == {
        "SINGLE_DISTRICT": 85,
        "MULTI_DISTRICT": 12,
        "CITYWIDE": 1,
        "UNSPECIFIED": 8,
    }


def test_unspecified_district_is_preserved_not_invented():
    reconciliation = (
        load_reconciliation()
    )

    january_requests = {}

    for record in reconciliation[
        "records"
    ]:
        request = record.get(
            "january_request_dollars"
        )

        if request is None:
            request = record[
                "model_request_dollars"
            ]

        january_requests[
            str(
                record[
                    "decision_unit_id"
                ]
            )
        ] = int(request)

    reader = PdfReader(
        constraints.SOURCE_PATH
    )

    records = (
        constraints
        .extract_non_watershed(
            reader,
            january_requests,
        )
    )

    fire_b = next(
        record
        for record in records
        if (
            record[
                "decision_unit_id"
            ]
            == (
                "community-facilities/"
                "fire/education-building-b"
            )
        )
    )

    assert (
        fire_b["council_district"]
        == "UNSPECIFIED"
    )


def test_committed_artifact_equals_deterministic_builder_output():
    expected = (
        portfolio.serialized_artifact()
    )

    actual = (
        METHODOLOGY_PATH.read_text(
            encoding="utf-8"
        )
    )

    assert actual == expected


def test_builder_refuses_differing_existing_artifact(
    monkeypatch,
    tmp_path,
):
    output = (
        tmp_path
        / "portfolio-methodology.json"
    )

    monkeypatch.setattr(
        portfolio,
        "OUTPUT_PATH",
        output,
    )

    assert (
        portfolio.write_artifact()
        == "created"
    )

    assert (
        portfolio.write_artifact()
        == "unchanged"
    )

    output.write_text(
        '{"different": true}\n',
        encoding="utf-8",
    )

    with pytest.raises(
        portfolio.DerivedArtifactConflictError
    ):
        portfolio.write_artifact()


def test_builder_fails_closed_if_predecessor_portfolio_is_already_authorized(
    monkeypatch,
    tmp_path,
):
    priority = load_priority()

    priority[
        "portfolio_selection_authorized"
    ] = True

    path = (
        tmp_path
        / "priority.json"
    )

    path.write_text(
        json.dumps(priority),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        portfolio,
        "PRIORITY_PATH",
        path,
    )

    with pytest.raises(
        portfolio.MethodologyError,
        match="predecessor",
    ):
        portfolio.validate_prerequisites()


def test_builder_fails_closed_if_cross_category_ranking_is_not_authorized(
    monkeypatch,
    tmp_path,
):
    priority = load_priority()

    priority[
        "cross_category_ranking_authorized"
    ] = False

    path = (
        tmp_path
        / "priority.json"
    )

    path.write_text(
        json.dumps(priority),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        portfolio,
        "PRIORITY_PATH",
        path,
    )

    with pytest.raises(
        portfolio.MethodologyError,
        match="ranking",
    ):
        portfolio.validate_prerequisites()


def test_builder_fails_closed_if_request_total_changes(
    monkeypatch,
    tmp_path,
):
    reconciliation = (
        load_reconciliation()
    )

    reconciliation[
        "records"
    ][0][
        "model_request_dollars"
    ] += 1

    path = (
        tmp_path
        / "reconciliation.json"
    )

    path.write_text(
        json.dumps(
            reconciliation
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        portfolio,
        "RECONCILIATION_PATH",
        path,
    )

    with pytest.raises(
        portfolio.MethodologyError,
        match="request total",
    ):
        portfolio.validate_prerequisites()
