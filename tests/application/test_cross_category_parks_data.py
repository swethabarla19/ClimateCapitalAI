"""Governance tests for the M3.5 Parks source-row slice."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
)


PATH = Path("data/governed/cross_category/source_rows/parks.json")


def load_units():
    rows = json.loads(PATH.read_text())
    return [CrossCategoryDecisionUnit.model_validate(row) for row in rows]


def test_parks_slice_has_exact_locked_counts():
    units = load_units()

    assert len(units) == 34

    assert Counter(unit.analytical_unit_type for unit in units) == {
        AnalyticalUnitType.ANALYTICAL_PROJECT: 22,
        AnalyticalUnitType.PROGRAM_BUCKET: 8,
        AnalyticalUnitType.PROGRAM_ALLOCATION: 4,
    }


def test_parks_analytical_project_request_total():
    units = load_units()

    total = sum(
        unit.department_request_dollars or 0
        for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.ANALYTICAL_PROJECT
    )

    assert total == 253_450_000


def test_parks_program_allocations_are_unscored():
    units = load_units()

    allocations = [
        unit for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.PROGRAM_ALLOCATION
    ]

    assert len(allocations) == 4
    assert all(unit.prb_scored is False for unit in allocations)
    assert all(unit.prb_score is None for unit in allocations)
    assert all(unit.model_eligible is False for unit in allocations)


def test_parks_scored_program_buckets_remain_non_project_units():
    units = load_units()

    buckets = [
        unit for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.PROGRAM_BUCKET
    ]

    assert len(buckets) == 8
    assert all(unit.prb_scored is True for unit in buckets)
    assert all(unit.prb_score is not None for unit in buckets)
    assert all(unit.analytical_unit is False for unit in buckets)


def test_parent_allocations_are_not_added_to_project_total():
    units = load_units()

    project_total = sum(
        unit.department_request_dollars or 0
        for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.ANALYTICAL_PROJECT
    )

    allocation_total = sum(
        unit.department_request_dollars or 0
        for unit in units
        if unit.analytical_unit_type == AnalyticalUnitType.PROGRAM_ALLOCATION
    )

    assert project_total == 253_450_000
    assert allocation_total == 225_000_000
    assert project_total != project_total + allocation_total
