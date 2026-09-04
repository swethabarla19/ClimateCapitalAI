"""Governance tests for the M3.5 Community Facilities source-row slice."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.cross_category import (
    AnalyticalUnitType,
    CrossCategoryDecisionUnit,
)


PATH = Path(
    "data/governed/cross_category/source_rows/"
    "community_facilities.json"
)

JUL_SOURCE_ID = (
    "austin_2026_bond_initial_project_request_list_2025_07_31"
)
JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"


def load_units():
    rows = json.loads(PATH.read_text())
    return [CrossCategoryDecisionUnit.model_validate(row) for row in rows]


def test_community_facilities_slice_has_exact_locked_counts():
    units = load_units()

    assert len(units) == 41

    assert Counter(unit.analytical_unit_type for unit in units) == {
        AnalyticalUnitType.ANALYTICAL_PROJECT: 38,
        AnalyticalUnitType.PROGRAM_BUCKET: 3,
    }


def test_community_facilities_preserves_source_domains():
    units = load_units()

    counts = Counter(unit.source_domain for unit in units)

    assert counts == {
        "Cultural / ACME": 7,
        "Libraries": 5,
        "Public Health": 2,
        "Emergency Medical Services": 7,
        "Fire": 5,
        "Fleet Services": 4,
        "Homeless Strategy": 2,
        "Police": 7,
        "Animal Services": 1,
        "Municipal Court": 1,
    }

    assert all(
        unit.presentation_category == "Community Facilities"
        for unit in units
    )


def test_community_facilities_analytical_request_total():
    total = sum(
        unit.department_request_dollars or 0
        for unit in load_units()
        if unit.analytical_unit_type
        == AnalyticalUnitType.ANALYTICAL_PROJECT
    )

    assert total == 1_248_400_000


def test_community_facilities_recommendations_remain_separate():
    units = load_units()

    analytical_total = sum(
        unit.historical_recommendation_amount_dollars or 0
        for unit in units
        if unit.analytical_unit_type
        == AnalyticalUnitType.ANALYTICAL_PROJECT
    )

    all_total = sum(
        unit.historical_recommendation_amount_dollars or 0
        for unit in units
    )

    assert analytical_total == 124_000_000
    assert all_total == 149_000_000


def test_community_facilities_program_buckets_are_exact():
    programs = {
        unit.source_name
        for unit in load_units()
        if unit.analytical_unit_type
        == AnalyticalUnitType.PROGRAM_BUCKET
    }

    assert programs == {
        "Regional Library Land Acquisition",
        "Safe & Secure Libraries Project",
        "Austin Shelters",
    }


def test_july_to_january_source_version_changes_are_preserved():
    units = {
        unit.decision_unit_id: unit
        for unit in load_units()
    }

    carver = units[
        "community-facilities/acme/george-washington-carver-museum"
    ]
    colony_library = units[
        "community-facilities/library/colony-park-branch-library"
    ]
    safe_libraries = units[
        "community-facilities/library/safe-secure-libraries"
    ]

    assert carver.source_conflict_flag is True
    assert colony_library.source_conflict_flag is True
    assert safe_libraries.source_conflict_flag is True

    carver_versions = {
        version.source_id: version
        for version in carver.source_versions
    }
    assert (
        carver_versions[JUL_SOURCE_ID].department_request_dollars
        == 6_000_000
    )
    assert (
        carver_versions[JAN_SOURCE_ID].department_request_dollars
        == 12_000_000
    )

    colony_versions = {
        version.source_id: version
        for version in colony_library.source_versions
    }
    assert (
        colony_versions[JUL_SOURCE_ID].department_request_dollars
        == 58_800_000
    )
    assert (
        colony_versions[JAN_SOURCE_ID].department_request_dollars
        == 58_000_000
    )

    safe_versions = {
        version.source_id: version
        for version in safe_libraries.source_versions
    }
    assert (
        safe_versions[JUL_SOURCE_ID].source_name
        == "Safe & Ready Libraries Project"
    )
    assert (
        safe_versions[JAN_SOURCE_ID].source_name
        == "Safe & Secure Libraries Project"
    )