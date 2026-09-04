"""Persistent governance tests for M3.7A Watershed PRB reconciliation."""

import json
from collections import Counter
from pathlib import Path

from climatecapital.contracts.versions import GOVERNED_PROJECT_IDS


PATH = Path(
    "data/governed/cross_category/reconciliation/"
    "watershed-prb-reconciliation.json"
)


def load_artifact():
    return json.loads(PATH.read_text())


def records():
    return load_artifact()["records"]


def test_m3_7a_artifact_identity_is_locked():
    artifact = load_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7a-watershed-prb-reconciliation/1.0.0"
    )
    assert artifact["governance_checkpoint"] == "M3.7A"
    assert (
        artifact["historical_decision_snapshot_date"]
        == "2026-01-21"
    )
    assert (
        artifact["canonical_identity_source_id"]
        == "austin_wpd_2026_bond_projects_2025_11_21"
    )
    assert (
        artifact["prb_scoring_source_id"]
        == "austin_2026_bond_initial_draft_2026_01_21"
    )


def test_exact_37_project_reconciliation():
    rows = records()

    assert len(rows) == 37

    ids = [row["canonical_project_id"] for row in rows]

    assert len(ids) == len(set(ids))
    assert tuple(ids) == GOVERNED_PROJECT_IDS


def test_every_project_has_complete_prb_component_vector():
    fields = (
        "strategic_alignment",
        "critical_asset",
        "community_consideration",
        "efficiency",
        "timeliness_readiness",
        "climate_resilience",
    )

    for row in records():
        assert all(row[field] is not None for field in fields)

        component_sum = sum(
            row[field]
            for field in fields
        )

        assert component_sum == row["prb_grand_total"]


def test_reconciliation_statuses_are_exactly_governed():
    counts = Counter(
        row["reconciliation_status"]
        for row in records()
    )

    assert counts == {
        "EXACT_NAME_MATCH": 7,
        "GOVERNED_SOURCE_VERSION_MATCH": 30,
    }


def test_name_version_difference_count_is_exact():
    differences = [
        row
        for row in records()
        if row["name_version_difference"]
    ]

    assert len(differences) == 30

    assert all(
        row["reconciliation_status"]
        == "GOVERNED_SOURCE_VERSION_MATCH"
        for row in differences
    )


def test_5754_149_is_only_request_version_conflict():
    conflicts = [
        row
        for row in records()
        if row["request_version_conflict"]
    ]

    assert len(conflicts) == 1

    conflict = conflicts[0]

    assert conflict["canonical_project_id"] == "5754.149"
    assert conflict["november_request_dollars"] == 2_500_000
    assert conflict["january_request_dollars"] == 2_625_000


def test_financial_totals_remain_exact():
    rows = records()

    assert (
        sum(row["november_request_dollars"] for row in rows)
        == 327_970_000
    )

    assert (
        sum(row["january_request_dollars"] for row in rows)
        == 328_095_000
    )

    assert (
        sum(
            row["january_recommendation_dollars"] or 0
            for row in rows
        )
        == 125_000_000
    )


def test_prb_source_provenance_is_present_for_every_project():
    rows = records()

    assert all(
        row["canonical_identity_source_id"]
        == "austin_wpd_2026_bond_projects_2025_11_21"
        for row in rows
    )

    assert all(
        row["prb_scoring_source_id"]
        == "austin_2026_bond_initial_draft_2026_01_21"
        for row in rows
    )

    assert all(
        row["prb_source_pdf_page"] in {8, 9, 10}
        for row in rows
    )

    assert {
        row["prb_source_table_row_order"]
        for row in rows
    } == set(range(1, 38))


def test_summary_matches_record_level_evidence():
    artifact = load_artifact()
    summary = artifact["summary"]
    rows = artifact["records"]

    assert summary["project_count"] == 37
    assert summary["exact_name_match_count"] == 7
    assert (
        summary["governed_source_version_match_count"]
        == 30
    )
    assert summary["name_version_difference_count"] == 30
    assert summary["request_version_conflict_count"] == 1
    assert (
        summary["complete_prb_component_vector_count"]
        == 37
    )
    assert summary["valid_prb_grand_total_count"] == 37

    assert (
        summary["november_request_total_dollars"]
        == sum(
            row["november_request_dollars"]
            for row in rows
        )
    )

    assert (
        summary["january_request_total_dollars"]
        == sum(
            row["january_request_dollars"]
            for row in rows
        )
    )

    assert (
        summary["january_recommendation_total_dollars"]
        == sum(
            row["january_recommendation_dollars"] or 0
            for row in rows
        )
    )
