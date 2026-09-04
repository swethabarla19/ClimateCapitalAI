"""Governance test for the M3.5 Affordable Housing quarantine."""

import json
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
)


PATH = Path(
    "data/governed/cross_category/source_rows/affordable_housing.json"
)


def test_affordable_housing_is_exact_not_scored_quarantine():
    rows = json.loads(PATH.read_text())

    assert len(rows) == 1

    unit = CrossCategoryDecisionUnit.model_validate(rows[0])

    assert unit.source_name == "Affordable Housing"
    assert unit.analytical_unit_type == AnalyticalUnitType.NOT_SCORED
    assert unit.analytical_unit is False
    assert unit.prb_scored is False
    assert unit.prb_score is None
    assert unit.department_request_dollars == 350_000_000
    assert unit.historical_recommendation_amount_dollars == 0
    assert unit.model_eligible is False
    assert unit.exclusion_reason == "PRB_NOT_SCORED"