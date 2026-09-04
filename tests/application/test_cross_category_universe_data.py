"""Whole-universe validation for the governed M3.5 cross-category artifact."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryUniverseArtifact,
)


PATH = Path(
    "data/governed/cross_category/cross-category-universe.json"
)


def load_artifact():
    return CrossCategoryUniverseArtifact.model_validate(
        json.loads(PATH.read_text())
    )


def test_cross_category_universe_validates_as_governed_artifact():
    artifact = load_artifact()

    assert len(artifact.decision_units) == 136

    assert Counter(
        unit.analytical_unit_type
        for unit in artifact.decision_units
    ) == {
        AnalyticalUnitType.ANALYTICAL_PROJECT: 106,
        AnalyticalUnitType.PROGRAM_BUCKET: 23,
        AnalyticalUnitType.PROGRAM_ALLOCATION: 4,
        AnalyticalUnitType.NOT_SCORED: 3,
    }


def test_analytical_projects_reconcile_by_presentation_group():
    artifact = load_artifact()

    counts = Counter(
        unit.presentation_category
        for unit in artifact.decision_units
        if unit.analytical_unit_type
        == AnalyticalUnitType.ANALYTICAL_PROJECT
    )

    assert counts == {
        "Transportation": 9,
        "Parks & Open Space": 22,
        "Watershed": 37,
        "Community Facilities": 38,
    }


def test_not_scored_quarantine_is_exact():
    artifact = load_artifact()

    quarantined = {
        unit.source_name
        for unit in artifact.decision_units
        if unit.analytical_unit_type
        == AnalyticalUnitType.NOT_SCORED
    }

    assert quarantined == {
        "Neighborhood Partnering Program",
        "Open Space Acquisition",
        "Affordable Housing",
    }


def test_no_nonproject_unit_is_model_eligible():
    artifact = load_artifact()

    nonprojects = [
        unit
        for unit in artifact.decision_units
        if unit.analytical_unit_type
        != AnalyticalUnitType.ANALYTICAL_PROJECT
    ]

    assert nonprojects
    assert all(unit.model_eligible is False for unit in nonprojects)


def test_m35_does_not_auto_promote_analytical_projects_to_model_eligible():
    artifact = load_artifact()

    projects = [
        unit
        for unit in artifact.decision_units
        if unit.analytical_unit_type
        == AnalyticalUnitType.ANALYTICAL_PROJECT
    ]

    assert len(projects) == 106
    assert all(unit.model_eligible is False for unit in projects)
    assert all(
        unit.evidence_feasibility_status == "NOT_EVALUATED"
        for unit in projects
    )


def test_decision_unit_ids_are_unique():
    artifact = load_artifact()

    ids = [
        unit.decision_unit_id
        for unit in artifact.decision_units
    ]

    assert len(ids) == 136
    assert len(set(ids)) == 136