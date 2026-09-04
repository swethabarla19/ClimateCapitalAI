"""Contract tests for the governed M3.5 cross-category universe."""

import pytest
from pydantic import ValidationError

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
    EvidenceFeasibilityStatus,
    ExclusionReason,
    PresentationCategory,
    SourceVersionValue,
)


SOURCE_ID = "austin-prb-2026-01-21"


def make_unit(**overrides):
    values = {
        "decision_unit_id": "test-project",
        "canonical_project_id": None,
        "source_name": "Test Project",
        "source_department": "Test Department",
        "source_domain": "Test Domain",
        "presentation_category": PresentationCategory.TRANSPORTATION,
        "analytical_unit_type": AnalyticalUnitType.ANALYTICAL_PROJECT,
        "analytical_unit": True,
        "prb_scored": True,
        "prb_score": 70,
        "department_request_dollars": 10_000_000,
        "historical_recommendation_amount_dollars": None,
        "evidence_feasibility_status": EvidenceFeasibilityStatus.NOT_EVALUATED,
        "model_eligible": False,
        "exclusion_reason": None,
        "source_ids": [SOURCE_ID],
        "source_versions": [
            SourceVersionValue(
                source_id=SOURCE_ID,
                source_date="2026-01-21",
                source_name="Test Project",
                department_request_dollars=10_000_000,
                prb_score=70,
            )
        ],
        "source_conflict_flag": False,
    }
    values.update(overrides)
    return CrossCategoryDecisionUnit(**values)


def test_analytical_project_is_structurally_valid():
    unit = make_unit()

    assert unit.analytical_unit is True
    assert unit.prb_scored is True
    assert unit.prb_score == 70
    assert unit.model_eligible is False


def test_not_scored_requires_null_prb_score():
    unit = make_unit(
        analytical_unit_type=AnalyticalUnitType.NOT_SCORED,
        analytical_unit=False,
        prb_scored=False,
        prb_score=None,
        model_eligible=False,
        exclusion_reason=ExclusionReason.PRB_NOT_SCORED,
    )

    assert unit.prb_score is None

    with pytest.raises(ValidationError):
        make_unit(
            analytical_unit_type=AnalyticalUnitType.NOT_SCORED,
            analytical_unit=False,
            prb_scored=False,
            prb_score=0,
            model_eligible=False,
            exclusion_reason=ExclusionReason.PRB_NOT_SCORED,
        )


def test_program_bucket_cannot_be_model_eligible():
    with pytest.raises(ValidationError):
        make_unit(
            analytical_unit_type=AnalyticalUnitType.PROGRAM_BUCKET,
            analytical_unit=False,
            prb_scored=True,
            prb_score=69,
            model_eligible=True,
            exclusion_reason=ExclusionReason.PROGRAM_BUCKET,
        )


def test_program_allocation_is_unscored_but_not_not_scored():
    unit = make_unit(
        analytical_unit_type=AnalyticalUnitType.PROGRAM_ALLOCATION,
        analytical_unit=False,
        prb_scored=False,
        prb_score=None,
        model_eligible=False,
        exclusion_reason=ExclusionReason.PROGRAM_ALLOCATION,
    )

    assert unit.analytical_unit_type == "PROGRAM_ALLOCATION"
    assert unit.exclusion_reason == "PROGRAM_ALLOCATION"


def test_watershed_analytical_project_requires_canonical_subproject_id():
    with pytest.raises(ValidationError):
        make_unit(
            presentation_category=PresentationCategory.WATERSHED,
            canonical_project_id=None,
        )

    unit = make_unit(
        presentation_category=PresentationCategory.WATERSHED,
        canonical_project_id="5754.149",
    )
    assert unit.canonical_project_id == "5754.149"


def test_source_conflict_requires_multiple_versions():
    with pytest.raises(ValidationError):
        make_unit(source_conflict_flag=True)


def test_source_version_must_be_declared_in_source_ids():
    other_version = SourceVersionValue(
        source_id="austin-wpd-2025-11-21",
        source_date="2025-11-21",
        source_name="Earlier Project Name",
    )

    with pytest.raises(ValidationError):
        make_unit(source_versions=[other_version])
