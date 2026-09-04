"""Governance tests for the M3.5 Watershed source-row slice."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
)
from climatecapital.contracts.versions import GOVERNED_PROJECT_IDS


PATH = Path(
    "data/governed/cross_category/source_rows/watershed.json"
)

NOV_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"


def load_units():
    rows = json.loads(PATH.read_text())
    return [CrossCategoryDecisionUnit.model_validate(row) for row in rows]


def analytical_projects():
    return [
        unit
        for unit in load_units()
        if unit.analytical_unit_type
        == AnalyticalUnitType.ANALYTICAL_PROJECT
    ]


def test_watershed_slice_has_exact_locked_counts():
    units = load_units()

    assert len(units) == 42

    assert Counter(unit.analytical_unit_type for unit in units) == {
        AnalyticalUnitType.ANALYTICAL_PROJECT: 37,
        AnalyticalUnitType.PROGRAM_BUCKET: 4,
        AnalyticalUnitType.NOT_SCORED: 1,
    }


def test_watershed_canonical_ids_match_existing_governed_universe():
    ids = [
        unit.canonical_project_id
        for unit in analytical_projects()
    ]

    assert tuple(ids) == GOVERNED_PROJECT_IDS


def test_watershed_canonical_request_total_remains_locked():
    total = sum(
        unit.department_request_dollars or 0
        for unit in analytical_projects()
    )

    assert total == 327_970_000


def test_watershed_january_prb_request_total_is_preserved_separately():
    total = 0

    for unit in analytical_projects():
        january = next(
            version
            for version in unit.source_versions
            if version.source_id == JAN_SOURCE_ID
        )
        total += january.department_request_dollars or 0

    assert total == 328_095_000


def test_watershed_historical_project_subenvelope_is_125m():
    total = sum(
        unit.historical_recommendation_amount_dollars or 0
        for unit in analytical_projects()
    )

    assert total == 125_000_000


def test_5754_149_preserves_exact_request_conflict():
    unit = next(
        unit
        for unit in analytical_projects()
        if unit.canonical_project_id == "5754.149"
    )

    versions = {
        version.source_id: version
        for version in unit.source_versions
    }

    assert unit.source_conflict_flag is True
    assert unit.department_request_dollars == 2_500_000
    assert (
        versions[NOV_SOURCE_ID].department_request_dollars
        == 2_500_000
    )
    assert (
        versions[JAN_SOURCE_ID].department_request_dollars
        == 2_625_000
    )


def test_5754_149_is_only_request_conflict():
    conflicts = [
        unit.canonical_project_id
        for unit in analytical_projects()
        if unit.source_conflict_flag
    ]

    assert conflicts == ["5754.149"]


def test_open_space_is_exact_not_scored_quarantine():
    open_space = next(
        unit
        for unit in load_units()
        if unit.source_name == "Open Space Acquisition"
    )

    assert (
        open_space.analytical_unit_type
        == AnalyticalUnitType.NOT_SCORED
    )
    assert open_space.prb_scored is False
    assert open_space.prb_score is None
    assert open_space.department_request_dollars == 300_000_000
    assert (
        open_space.historical_recommendation_amount_dollars
        == 10_000_000
    )
    assert open_space.model_eligible is False


def test_watershed_programs_remain_non_project_units():
    programs = [
        unit
        for unit in load_units()
        if unit.analytical_unit_type
        == AnalyticalUnitType.PROGRAM_BUCKET
    ]

    assert len(programs) == 4
    assert all(unit.analytical_unit is False for unit in programs)
    assert all(unit.model_eligible is False for unit in programs)
    assert all(unit.prb_scored is True for unit in programs)