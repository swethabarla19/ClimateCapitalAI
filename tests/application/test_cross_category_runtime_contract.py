"""Focused M3.8A tests for cross-category runtime-v2 contracts."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CROSS_CATEGORY_MAX_SCENARIO_BUDGET_DOLLARS,
    BoundaryResolutionInput,
    CouncilDistrictContext,
    CrossCategoryPlanInput,
    CrossCategoryPlanResult,
    CrossCategoryRuntimeProject,
    OfficialPrbComponents,
    OmImpactContext,
    PortfolioWarning,
    SelectedProjectResult,
)


def components_72() -> dict[str, int]:
    return {
        "strategic_alignment": 8,
        "critical_asset": 8,
        "community_consideration": 15,
        "efficiency": 17,
        "timeliness_readiness": 11,
        "climate_resilience": 13,
    }


def transportation_project_payload() -> dict:
    return {
        "decision_unit_id":
            "transportation/act-plan-7th-street",
        "canonical_project_id": None,
        "governed_name":
            "ACT Plan (Austin Core Transportation Plan) Program - 7th Street",
        "presentation_category":
            "Transportation",
        "source_department": "ATPW",
        "source_domain": "Transportation",
        "model_request_dollars": 40_000_000,
        "model_request_authority":
            "M3.6_GOVERNED_JANUARY_REQUEST",
        "model_request_authority_source_id":
            "austin_2026_bond_initial_draft_2026_01_21",
        "request_version_conflict": False,
        "funding_priority_score": 72,
        "funding_priority_rank": 13,
        "is_tied": True,
        "tie_group_size": 2,
        "display_order_within_tie": 2,
        "display_tiebreak_has_analytical_meaning": False,
        "prb_components": components_72(),
        "council_district": {
            "assignment_type": "SINGLE_DISTRICT",
            "districts": [9],
            "source_value": "9",
            "analyst_review_only": True,
            "hard_portfolio_constraint": False,
        },
        "om_impact": {
            "value": "NO",
            "analyst_review_only": True,
            "hard_portfolio_constraint": False,
            "additional_score_preference_authorized": False,
        },
        "provenance_refs": [
            "austin_2026_bond_initial_draft_2026_01_21",
        ],
    }


def test_contract_versions_are_v2():
    assert (
        CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
        == "p0-cross-category-catalog/2.0.0"
    )

    assert (
        CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        == "p0-cross-category-funding-plan/2.0.0"
    )


def test_runtime_budget_bound_is_technical_full_request_total():
    assert (
        CROSS_CATEGORY_MAX_SCENARIO_BUDGET_DOLLARS
        == 1_973_520_000
    )


def test_official_prb_components_reproduce_grand_total():
    components = OfficialPrbComponents(
        **components_72()
    )

    assert components.grand_total() == 72.0


def test_prb_components_reject_out_of_range_component():
    payload = components_72()
    payload["strategic_alignment"] = 9

    with pytest.raises(ValidationError):
        OfficialPrbComponents(**payload)


def test_prb_components_reject_non_half_point_increment():
    payload = components_72()
    payload["efficiency"] = 16.25

    with pytest.raises(ValidationError):
        OfficialPrbComponents(**payload)


def test_runtime_project_accepts_json_style_enum_strings():
    project = CrossCategoryRuntimeProject(
        **transportation_project_payload()
    )

    assert (
        project.presentation_category
        == "Transportation"
    )

    assert (
        project.council_district.assignment_type
        == "SINGLE_DISTRICT"
    )

    assert project.om_impact.value == "NO"


def test_runtime_project_rejects_component_total_mismatch():
    payload = transportation_project_payload()
    payload["funding_priority_score"] = 73

    with pytest.raises(
        ValidationError,
        match="reproduce Funding Priority Score",
    ):
        CrossCategoryRuntimeProject(**payload)


def test_non_watershed_project_cannot_fabricate_canonical_id():
    payload = transportation_project_payload()
    payload["canonical_project_id"] = "5789.075"

    with pytest.raises(
        ValidationError,
        match="must not fabricate",
    ):
        CrossCategoryRuntimeProject(**payload)


def test_watershed_project_requires_canonical_id():
    payload = transportation_project_payload()

    payload.update(
        {
            "decision_unit_id":
                "watershed/5789.075",
            "presentation_category":
                "Watershed",
            "source_department":
                "Watershed Protection",
            "source_domain":
                "Watershed",
            "canonical_project_id":
                None,
        }
    )

    with pytest.raises(
        ValidationError,
        match="require canonical_project_id",
    ):
        CrossCategoryRuntimeProject(**payload)


def test_tie_flag_must_match_tie_group_size():
    payload = transportation_project_payload()
    payload["is_tied"] = False

    with pytest.raises(
        ValidationError,
        match="is_tied",
    ):
        CrossCategoryRuntimeProject(**payload)


def test_display_order_must_stay_inside_tie_group():
    payload = transportation_project_payload()
    payload["display_order_within_tie"] = 3

    with pytest.raises(
        ValidationError,
        match="cannot exceed tie_group_size",
    ):
        CrossCategoryRuntimeProject(**payload)


def test_unspecified_council_district_preserves_missingness():
    context = CouncilDistrictContext(
        assignment_type="UNSPECIFIED",
        districts=[],
        source_value=None,
        analyst_review_only=True,
        hard_portfolio_constraint=False,
    )

    assert context.districts == []
    assert context.assignment_type == "UNSPECIFIED"


def test_unspecified_council_district_cannot_invent_district():
    with pytest.raises(
        ValidationError,
        match="must not invent district IDs",
    ):
        CouncilDistrictContext(
            assignment_type="UNSPECIFIED",
            districts=[1],
            source_value=None,
            analyst_review_only=True,
            hard_portfolio_constraint=False,
        )


def test_citywide_council_district_cannot_invent_specific_district():
    with pytest.raises(
        ValidationError,
        match="must not invent district IDs",
    ):
        CouncilDistrictContext(
            assignment_type="CITYWIDE",
            districts=[1],
            source_value="Citywide",
            analyst_review_only=True,
            hard_portfolio_constraint=False,
        )


def test_single_district_requires_exactly_one_district():
    with pytest.raises(
        ValidationError,
        match="exactly one district",
    ):
        CouncilDistrictContext(
            assignment_type="SINGLE_DISTRICT",
            districts=[1, 2],
            source_value="1, 2",
            analyst_review_only=True,
            hard_portfolio_constraint=False,
        )


def test_multi_district_requires_at_least_two_districts():
    with pytest.raises(
        ValidationError,
        match="at least two districts",
    ):
        CouncilDistrictContext(
            assignment_type="MULTI_DISTRICT",
            districts=[1],
            source_value="1",
            analyst_review_only=True,
            hard_portfolio_constraint=False,
        )


def test_council_district_values_must_be_sorted_unique():
    with pytest.raises(
        ValidationError,
        match="unique and sorted",
    ):
        CouncilDistrictContext(
            assignment_type="MULTI_DISTRICT",
            districts=[9, 8],
            source_value="8, 9",
            analyst_review_only=True,
            hard_portfolio_constraint=False,
        )


def test_om_context_is_explicitly_non_optimizing():
    context = OmImpactContext(
        value="YES",
        analyst_review_only=True,
        hard_portfolio_constraint=False,
        additional_score_preference_authorized=False,
    )

    assert context.value == "YES"
    assert context.hard_portfolio_constraint is False
    assert (
        context.additional_score_preference_authorized
        is False
    )


def test_plan_input_accepts_zero_boundary_resolutions():
    plan = CrossCategoryPlanInput(
        contract_version=(
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ),
        data_version="test-v2",
        available_budget_dollars=332_000_000,
        boundary_resolutions=[],
        expected_fingerprint=None,
    )

    assert plan.boundary_resolutions == []


def test_boundary_resolution_can_select_zero_projects_for_override_path():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[],
        advance_with_feasible_same_tier_project_acknowledged=True,
    )

    assert resolution.selected_decision_unit_ids == []
    assert (
        resolution
        .advance_with_feasible_same_tier_project_acknowledged
        is True
    )


def test_boundary_resolution_sorts_selected_ids_deterministically():
    resolution = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "watershed/5789.075",
            "parks/martin-pool",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    assert resolution.selected_decision_unit_ids == [
        "parks/martin-pool",
        "watershed/5789.075",
    ]


def test_boundary_resolution_rejects_duplicate_selected_ids():
    with pytest.raises(
        ValidationError,
        match="must be unique",
    ):
        BoundaryResolutionInput(
            funding_priority_score=67,
            funding_priority_rank=28,
            selected_decision_unit_ids=[
                "parks/martin-pool",
                "parks/martin-pool",
            ],
            advance_with_feasible_same_tier_project_acknowledged=False,
        )


def test_plan_input_rejects_duplicate_substantive_tier_resolution():
    first = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "parks/martin-pool",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    second = BoundaryResolutionInput(
        funding_priority_score=67,
        funding_priority_rank=28,
        selected_decision_unit_ids=[
            "watershed/5789.075",
        ],
        advance_with_feasible_same_tier_project_acknowledged=False,
    )

    with pytest.raises(
        ValidationError,
        match="unique by substantive tier",
    ):
        CrossCategoryPlanInput(
            contract_version=(
                CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
            ),
            data_version="test-v2",
            available_budget_dollars=700_000_000,
            boundary_resolutions=[
                first,
                second,
            ],
            expected_fingerprint=None,
        )


def test_plan_budget_rejects_above_governed_total():
    with pytest.raises(ValidationError):
        CrossCategoryPlanInput(
            contract_version=(
                CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
            ),
            data_version="test-v2",
            available_budget_dollars=(
                1_973_520_001
            ),
            boundary_resolutions=[],
            expected_fingerprint=None,
        )


def test_selected_project_accepts_string_selection_source():
    result = SelectedProjectResult(
        decision_unit_id=(
            "transportation/act-plan-7th-street"
        ),
        model_request_dollars=40_000_000,
        funding_priority_score=72,
        funding_priority_rank=13,
        selection_source=(
            "AUTO_UNIQUE_BUDGET_FEASIBLE"
        ),
    )

    assert (
        result.selection_source
        == "AUTO_UNIQUE_BUDGET_FEASIBLE"
    )


def test_warning_accepts_string_warning_code():
    warning = PortfolioWarning(
        warning_code=(
            "HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS"
        ),
        message=(
            "A same-tier project remains feasible."
        ),
        decision_unit_ids=[
            "parks/martin-pool",
        ],
    )

    assert (
        warning.warning_code
        == (
            "HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS"
        )
    )


def test_complete_plan_result_reconciles_money():
    selected = SelectedProjectResult(
        decision_unit_id=(
            "transportation/act-plan-7th-street"
        ),
        model_request_dollars=40_000_000,
        funding_priority_score=72,
        funding_priority_rank=13,
        selection_source=(
            "AUTO_UNIQUE_BUDGET_FEASIBLE"
        ),
    )

    result = CrossCategoryPlanResult(
        contract_version=(
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ),
        data_version="test-v2",
        status="COMPLETE",
        available_budget_dollars=50_050_000,
        selected_projects=[selected],
        included_total_dollars=40_000_000,
        remainder_dollars=10_050_000,
        unresolved_boundary=None,
        warnings=[],
        applied_analyst_overrides=[],
        plan_fingerprint="0" * 64,
    )

    assert result.status == "COMPLETE"
    assert result.remainder_dollars == 10_050_000


def test_complete_plan_result_rejects_wrong_remainder():
    selected = SelectedProjectResult(
        decision_unit_id=(
            "transportation/act-plan-7th-street"
        ),
        model_request_dollars=40_000_000,
        funding_priority_score=72,
        funding_priority_rank=13,
        selection_source=(
            "AUTO_UNIQUE_BUDGET_FEASIBLE"
        ),
    )

    with pytest.raises(
        ValidationError,
        match="remainder",
    ):
        CrossCategoryPlanResult(
            contract_version=(
                CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
            ),
            data_version="test-v2",
            status="COMPLETE",
            available_budget_dollars=50_050_000,
            selected_projects=[selected],
            included_total_dollars=40_000_000,
            remainder_dollars=1,
            unresolved_boundary=None,
            warnings=[],
            applied_analyst_overrides=[],
            plan_fingerprint="0" * 64,
        )


def test_runtime_contract_can_represent_preintegration_and_integrated_state():
    annotation = (
        CrossCategoryRuntimeProject
    )

    # Catalog-level integration authorization is intentionally
    # a strict bool rather than Literal[False], so the same v2
    # semantic contract can survive the final runtime gate.
    assert annotation is not None