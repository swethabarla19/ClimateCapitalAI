"""Governance tests for the M3.5 Transportation source-row slice."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
)


PATH = Path(
    "data/governed/cross_category/source_rows/transportation.json"
)


def load_units():
    rows = json.loads(PATH.read_text())
    return [CrossCategoryDecisionUnit.model_validate(row) for row in rows]


def test_transportation_slice_has_exact_locked_counts():
    units = load_units()

    assert len(units) == 18

    counts = Counter(unit.analytical_unit_type for unit in units)

    assert counts == {
        AnalyticalUnitType.ANALYTICAL_PROJECT: 9,
        AnalyticalUnitType.PROGRAM_BUCKET: 8,
        AnalyticalUnitType.NOT_SCORED: 1,
    }


def test_transportation_not_scored_quarantine_is_exact():
    units = load_units()

    quarantined = [
        unit for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.NOT_SCORED
    ]

    assert len(quarantined) == 1
    assert quarantined[0].source_name == "Neighborhood Partnering Program"
    assert quarantined[0].prb_score is None
    assert quarantined[0].model_eligible is False


def test_transportation_analytical_projects_are_not_auto_model_eligible():
    units = load_units()

    analytical = [
        unit for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.ANALYTICAL_PROJECT
    ]

    assert len(analytical) == 9
    assert all(unit.evidence_feasibility_status == "NOT_EVALUATED" for unit in analytical)
    assert all(unit.model_eligible is False for unit in analytical)


def test_transportation_recommendation_does_not_replace_request():
    units = {unit.decision_unit_id: unit for unit in load_units()}

    west_cannon = units["transportation/west-william-cannon-rehab"]
    assert west_cannon.department_request_dollars == 8_000_000
    assert west_cannon.historical_recommendation_amount_dollars == 8_000_000

    street_rehab = units["transportation/street-rehabilitation-program"]
    assert street_rehab.department_request_dollars == 194_000_000
    assert street_rehab.historical_recommendation_amount_dollars == 96_000_000
