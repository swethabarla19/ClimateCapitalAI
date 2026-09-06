"""Focused M3.8C tests for the executable cross-category portfolio state machine."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    BoundaryResolutionInput,
    CrossCategoryPlanInput,
    CrossCategoryRuntimeCatalog,
)
from climatecapital.plans.cross_category_evaluator import (
    CrossCategoryPortfolioEvaluationError,
    evaluate_cross_category_plan,
)


ROOT = Path(__file__).resolve().parents[2]

CATALOG_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v2"
    / "catalog.json"
)


def load_catalog() -> CrossCategoryRuntimeCatalog:
    payload = json.loads(
        CATALOG_PATH.read_text(
            encoding="utf-8"
        )
    )

    return (
        CrossCategoryRuntimeCatalog
        .model_validate(
            payload
        )
    )


def plan(
    budget: int,
    *,
    resolutions: list[
        BoundaryResolutionInput
    ] | None = None,
    expected_fingerprint: str | None = None,
) -> CrossCategoryPlanInput:
    catalog = load_catalog()

    return CrossCategoryPlanInput(
        contract_version=(
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ),
        data_version=(
            catalog.data_version
        ),
        available_budget_dollars=budget,
        boundary_resolutions=(
            resolutions or []
        ),
        expected_fingerprint=(
            expected_fingerprint
        ),
    )


def test_zero_budget_completes_with_no_projects():
    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(0),
    )

    assert result.status == "COMPLETE"
    assert result.selected_projects == []
    assert result.included_total_dollars == 0
    assert result.remainder_dollars == 0


def test_full_request_total_selects_all_106_projects():
    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            1_973_520_000
        ),
    )

    assert result.status == "COMPLETE"

    assert (
        len(
            result.selected_projects
        )
        == 106
    )

    assert (
        result.included_total_dollars
        == 1_973_520_000
    )

    assert (
        result.remainder_dollars
        == 0
    )

    assert all(
        project.selection_source
        == "AUTO_COMPLETE_TIER"
        for project
        in result.selected_projects
    )


def test_700m_stops_at_ambiguous_score_67_boundary():
    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            700_000_000
        ),
    )

    assert (
        result.status
        == "ANALYST_RESOLUTION_REQUIRED"
    )

    assert (
        result.unresolved_boundary
        is not None
    )

    assert (
        result.unresolved_boundary
        .funding_priority_score
        == 67
    )

    assert (
        result.unresolved_boundary
        .funding_priority_rank
        == 28
    )

    assert (
        result.unresolved_boundary
        .remaining_budget_before_tier_dollars
        == 108_275_000
    )

    assert (
        result.unresolved_boundary
        .full_tier_request_dollars
        == 113_000_000
    )

    feasible = [
        candidate
        for candidate
        in result
        .unresolved_boundary
        .candidates
        if (
            candidate
            .individually_budget_feasible
        )
    ]

    assert len(feasible) == 5


def test_750m_stops_at_ambiguous_score_65_boundary():
    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            750_000_000
        ),
    )

    assert (
        result.status
        == "ANALYST_RESOLUTION_REQUIRED"
    )

    assert (
        result.unresolved_boundary
        is not None
    )

    assert (
        result.unresolved_boundary
        .funding_priority_score
        == 65
    )

    assert (
        result.unresolved_boundary
        .funding_priority_rank
        == 37
    )

    assert (
        result.unresolved_boundary
        .remaining_budget_before_tier_dollars
        == 33_280_000
    )

    feasible = [
        candidate
        for candidate
        in result
        .unresolved_boundary
        .candidates
        if (
            candidate
            .individually_budget_feasible
        )
    ]

    assert len(feasible) == 8


def test_332m_uniquely_includes_7th_street_at_score_72():
    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            332_000_000
        ),
    )

    selected = {
        project.decision_unit_id:
            project
        for project
        in result.selected_projects
    }

    project = selected[
        "transportation/act-plan-7th-street"
    ]

    assert (
        project.selection_source
        == (
            "AUTO_UNIQUE_"
            "BUDGET_FEASIBLE"
        )
    )

    assert (
        project.model_request_dollars
        == 40_000_000
    )

    assert (
        "community-facilities/"
        "public-health/northeast"
        not in selected
    )


def test_plan_never_exceeds_available_budget():
    catalog = load_catalog()

    for budget in (
        0,
        100_000_000,
        332_000_000,
        700_000_000,
        750_000_000,
        1_973_520_000,
    ):
        result = (
            evaluate_cross_category_plan(
                catalog,
                plan(
                    budget
                ),
            )
        )

        assert (
            result.included_total_dollars
            <= budget
        )

        assert (
            result.remainder_dollars
            == (
                budget
                - result
                .included_total_dollars
            )
        )


def test_wrong_data_version_fails_closed():
    catalog = load_catalog()

    request = CrossCategoryPlanInput(
        contract_version=(
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ),
        data_version="wrong-data-version",
        available_budget_dollars=700_000_000,
        boundary_resolutions=[],
        expected_fingerprint=None,
    )

    with pytest.raises(
        CrossCategoryPortfolioEvaluationError,
        match="data version",
    ) as error:
        evaluate_cross_category_plan(
            catalog,
            request,
        )

    assert (
        error.value.code
        == "DATA_VERSION_CONFLICT"
    )


def test_resolution_project_must_belong_to_active_boundary():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "transportation/barton-springs-bridge",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    with pytest.raises(
        CrossCategoryPortfolioEvaluationError,
    ) as error:
        evaluate_cross_category_plan(
            load_catalog(),
            plan(
                700_000_000,
                resolutions=[
                    resolution
                ],
            ),
        )

    assert (
        error.value.code
        == "RESOLUTION_PROJECT_NOT_IN_TIER"
    )


def test_resolution_cannot_exceed_remaining_budget():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            (
                "community-facilities/"
                "police/canyon-creek-northwest"
            ),
            "parks/martin-pool",
            "watershed/5789.075",
            "watershed/5848.092",
            "watershed/8598.014",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    with pytest.raises(
        CrossCategoryPortfolioEvaluationError,
    ) as error:
        evaluate_cross_category_plan(
            load_catalog(),
            plan(
                700_000_000,
                resolutions=[
                    resolution
                ],
            ),
        )

    assert (
        error.value.code
        == "RESOLUTION_OVER_BUDGET"
    )


def test_partial_700m_boundary_choice_requires_ack_when_same_tier_still_fits():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "parks/martin-pool",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            700_000_000,
            resolutions=[
                resolution
            ],
        ),
    )

    assert (
        result.status
        == "ANALYST_RESOLUTION_REQUIRED"
    )

    assert any(
        warning.warning_code
        == (
            "HIGHER_PRIORITY_"
            "FEASIBLE_PROJECT_REMAINS"
        )
        for warning
        in result.warnings
    )

    selected = {
        project.decision_unit_id:
            project
        for project
        in result.selected_projects
    }

    assert (
        selected[
            "parks/martin-pool"
        ].selection_source
        == (
            "ANALYST_BOUNDARY_RESOLUTION"
        )
    )


def test_acknowledged_700m_override_is_recorded():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "parks/martin-pool",
        ],
        advance_with_feasible_same_tier_project_acknowledged=True,
    )

    result = evaluate_cross_category_plan(
        load_catalog(),
        plan(
            700_000_000,
            resolutions=[
                resolution
            ],
        ),
    )

    assert (
        result.applied_analyst_overrides
    )

    override = (
        result
        .applied_analyst_overrides[
            0
        ]
    )

    assert (
        override.funding_priority_score
        == 67
    )

    assert (
        override.funding_priority_rank
        == 28
    )

    assert (
        override.acknowledged
        is True
    )


def test_fingerprint_is_deterministic():
    catalog = load_catalog()

    first = evaluate_cross_category_plan(
        catalog,
        plan(
            750_000_000
        ),
    )

    second = evaluate_cross_category_plan(
        catalog,
        plan(
            750_000_000
        ),
    )

    assert (
        first.plan_fingerprint
        == second.plan_fingerprint
    )

    assert (
        len(
            first.plan_fingerprint
        )
        == 64
    )


def test_matching_expected_fingerprint_is_accepted():
    catalog = load_catalog()

    first = evaluate_cross_category_plan(
        catalog,
        plan(
            750_000_000
        ),
    )

    second = evaluate_cross_category_plan(
        catalog,
        plan(
            750_000_000,
            expected_fingerprint=(
                first.plan_fingerprint
            ),
        ),
    )

    assert (
        second.plan_fingerprint
        == first.plan_fingerprint
    )


def test_wrong_expected_fingerprint_fails_closed():
    with pytest.raises(
        CrossCategoryPortfolioEvaluationError,
    ) as error:
        evaluate_cross_category_plan(
            load_catalog(),
            plan(
                750_000_000,
                expected_fingerprint=(
                    "0" * 64
                ),
            ),
        )

    assert (
        error.value.code
        == "PLAN_FINGERPRINT_CONFLICT"
    )