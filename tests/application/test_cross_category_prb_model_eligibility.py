"""Persistent governance tests for M3.7E cross-category PRB evidence and eligibility."""

from __future__ import annotations

import json
import tempfile
from collections import Counter
from pathlib import Path

import pytest

from scripts.data import build_cross_category_prb_model_eligibility as eligibility
from scripts.data import build_cross_category_prb_reconciliation as reconciliation


ROOT = Path(__file__).resolve().parents[2]

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

ELIGIBILITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "cross-category-prb-model-eligibility.json"
)

WATERSHED_RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "watershed-prb-reconciliation.json"
)

NON_WATERSHED_SCORE_PATH = (
    ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "non_watershed_prb_scores.csv"
)

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}

EXPECTED_CONFLICT_IDS = {
    "watershed/5754.149",
    "community-facilities/acme/george-washington-carver-museum",
    "community-facilities/library/colony-park-branch-library",
}

EXPECTED_HALF_POINT_IDS = {
    "community-facilities/ems/station-03",
    "community-facilities/ems/station-14",
    "community-facilities/fleet/consolidated-service-center",
}

COMPONENT_FIELDS = (
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
)


def load_reconciliation_artifact() -> dict:
    return json.loads(
        RECONCILIATION_PATH.read_text(encoding="utf-8")
    )


def load_eligibility_artifact() -> dict:
    return json.loads(
        ELIGIBILITY_PATH.read_text(encoding="utf-8")
    )


def test_m3_7e_a_artifact_identity_and_boundaries_are_locked():
    artifact = load_reconciliation_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7e-a-cross-category-prb-reconciliation/1.0.0"
    )
    assert artifact["governance_checkpoint"] == "M3.7E-A"
    assert (
        artifact["historical_decision_snapshot_date"]
        == "2026-01-21"
    )
    assert (
        artifact["artifact_scope"]
        == "CROSS_CATEGORY_PRB_RECONCILIATION"
    )

    assert artifact["cross_category_ranking_authorized"] is False
    assert artifact["portfolio_selection_authorized"] is False
    assert artifact["runtime_integration_authorized"] is False


def test_m3_7e_a_exact_106_project_reconciliation():
    artifact = load_reconciliation_artifact()
    rows = artifact["records"]

    assert len(rows) == 106

    ids = [
        row["decision_unit_id"]
        for row in rows
    ]

    assert len(ids) == len(set(ids)) == 106

    counts = Counter(
        row["presentation_category"]
        for row in rows
    )

    assert dict(counts) == EXPECTED_CATEGORY_COUNTS


def test_m3_7e_a_all_projects_have_complete_valid_prb_vectors():
    rows = load_reconciliation_artifact()["records"]

    for row in rows:
        assert all(
            row[field] is not None
            for field in COMPONENT_FIELDS
        )

        component_sum = sum(
            row[field]
            for field in COMPONENT_FIELDS
        )

        assert component_sum == row["prb_grand_total"]


def test_m3_7e_a_identity_authority_is_category_specific():
    rows = load_reconciliation_artifact()["records"]

    watershed = [
        row
        for row in rows
        if row["presentation_category"] == "Watershed"
    ]

    non_watershed = [
        row
        for row in rows
        if row["presentation_category"] != "Watershed"
    ]

    assert len(watershed) == 37
    assert len(non_watershed) == 69

    assert all(
        row["canonical_project_id"] is not None
        for row in watershed
    )

    assert all(
        row["identity_authority"]
        == "M3.7A_WATERSHED_CANONICAL_PROJECT_ID"
        for row in watershed
    )

    assert all(
        row["canonical_project_id"] is None
        for row in non_watershed
    )

    assert all(
        row["identity_authority"]
        == "M3.6_GOVERNED_DECISION_UNIT_ID"
        for row in non_watershed
    )


def test_m3_7e_a_request_authority_preserves_watershed_boundary():
    rows = load_reconciliation_artifact()["records"]

    watershed = [
        row
        for row in rows
        if row["presentation_category"] == "Watershed"
    ]

    non_watershed = [
        row
        for row in rows
        if row["presentation_category"] != "Watershed"
    ]

    assert all(
        row["model_request_authority"]
        == "CANONICAL_NOVEMBER_2025_WATERSHED_REQUEST"
        for row in watershed
    )

    assert all(
        row["model_request_authority"]
        == "M3.6_GOVERNED_JANUARY_REQUEST"
        for row in non_watershed
    )

    assert (
        sum(row["model_request_dollars"] for row in rows)
        == 1_973_520_000
    )

    assert (
        sum(row["january_request_dollars"] for row in rows)
        == 1_973_645_000
    )


def test_5754_149_preserves_canonical_watershed_request():
    row = next(
        row
        for row in load_reconciliation_artifact()["records"]
        if row["decision_unit_id"] == "watershed/5754.149"
    )

    assert row["canonical_project_id"] == "5754.149"
    assert row["model_request_dollars"] == 2_500_000
    assert row["january_request_dollars"] == 2_625_000
    assert row["request_version_conflict"] is True


def test_non_watershed_historical_request_conflicts_are_preserved():
    rows = {
        row["decision_unit_id"]: row
        for row in load_reconciliation_artifact()["records"]
    }

    carver = rows[
        "community-facilities/acme/george-washington-carver-museum"
    ]

    colony = rows[
        "community-facilities/library/colony-park-branch-library"
    ]

    assert carver["model_request_dollars"] == 12_000_000
    assert colony["model_request_dollars"] == 58_000_000

    assert carver["source_conflict_flag"] is True
    assert colony["source_conflict_flag"] is True

    assert carver["request_version_conflict"] is True
    assert colony["request_version_conflict"] is True


def test_exact_three_source_version_conflicts_are_preserved():
    rows = load_reconciliation_artifact()["records"]

    source_conflicts = {
        row["decision_unit_id"]
        for row in rows
        if row["source_conflict_flag"]
    }

    request_conflicts = {
        row["decision_unit_id"]
        for row in rows
        if row["request_version_conflict"]
    }

    assert source_conflicts == EXPECTED_CONFLICT_IDS
    assert request_conflicts == EXPECTED_CONFLICT_IDS


def test_half_point_prb_scores_are_preserved_without_rounding():
    rows = load_reconciliation_artifact()["records"]

    half_point_ids = {
        row["decision_unit_id"]
        for row in rows
        if any(
            reconciliation.is_half_point(row[field])
            for field in (
                *COMPONENT_FIELDS,
                "prb_grand_total",
            )
        )
    }

    assert half_point_ids == EXPECTED_HALF_POINT_IDS

    totals = {
        row["decision_unit_id"]: row["prb_grand_total"]
        for row in rows
        if row["decision_unit_id"] in EXPECTED_HALF_POINT_IDS
    }

    assert totals == {
        "community-facilities/ems/station-03": 54.5,
        "community-facilities/ems/station-14": 53.5,
        "community-facilities/fleet/consolidated-service-center": 50.5,
    }


def test_january_recommendation_remains_project_level_benchmark_outcome():
    artifact = load_reconciliation_artifact()
    rows = artifact["records"]

    assert (
        sum(
            row["january_recommendation_dollars"] or 0
            for row in rows
        )
        == 332_000_000
    )

    assert (
        sum(
            row["january_recommendation_dollars"] is not None
            for row in rows
        )
        == 20
    )

    assert (
        artifact["authority_policy"]["january_initial_recommendation"]
        == "BENCHMARK_OUTCOME_ONLY"
    )


def test_m3_7e_a_summary_is_exact():
    summary = load_reconciliation_artifact()["summary"]

    assert summary["analytical_project_count"] == 106
    assert summary["category_counts"] == EXPECTED_CATEGORY_COUNTS
    assert summary["complete_prb_component_vector_count"] == 106
    assert summary["valid_prb_grand_total_count"] == 106
    assert summary["non_watershed_exact_identity_match_count"] == 69
    assert summary["watershed_exact_name_match_count"] == 7
    assert (
        summary["watershed_governed_source_version_match_count"]
        == 30
    )
    assert summary["source_conflict_count"] == 3
    assert summary["request_version_conflict_count"] == 3
    assert summary["half_point_project_count"] == 3
    assert summary["model_request_total_dollars"] == 1_973_520_000
    assert (
        summary["january_request_overlay_total_dollars"]
        == 1_973_645_000
    )
    assert (
        summary["january_project_recommendation_total_dollars"]
        == 332_000_000
    )
    assert summary["january_recommendation_present_count"] == 20


def test_m3_7e_a_committed_artifact_is_deterministic_builder_output():
    projects = reconciliation.load_analytical_projects()

    watershed = reconciliation.load_watershed_reconciliation(
        WATERSHED_RECONCILIATION_PATH
    )

    scores = reconciliation.load_non_watershed_scores(
        NON_WATERSHED_SCORE_PATH
    )

    records = reconciliation.build_records(
        projects,
        watershed,
        scores,
    )

    summary = reconciliation.validate_records(
        records
    )

    expected = reconciliation.render_artifact(
        records,
        summary,
    )

    assert RECONCILIATION_PATH.read_bytes() == expected


def test_m3_7e_b_artifact_identity_and_boundaries_are_locked():
    artifact = load_eligibility_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7e-b-cross-category-prb-model-eligibility/1.0.0"
    )
    assert artifact["governance_checkpoint"] == "M3.7E-B"
    assert (
        artifact["historical_decision_snapshot_date"]
        == "2026-01-21"
    )
    assert (
        artifact["model_scope"]
        == "CROSS_CATEGORY_PRB_PROJECT_MODEL"
    )

    assert artifact["cross_category_ranking_authorized"] is False
    assert artifact["portfolio_selection_authorized"] is False
    assert artifact["runtime_integration_authorized"] is False


def test_exact_106_project_model_eligible_cohort():
    rows = load_eligibility_artifact()["records"]

    assert len(rows) == 106

    assert len(
        {
            row["decision_unit_id"]
            for row in rows
        }
    ) == 106

    assert all(
        row["evidence_feasibility_status"] == "FEASIBLE"
        for row in rows
    )

    assert all(
        row["model_eligible"] is True
        for row in rows
    )

    assert all(
        row["blocking_reason_codes"] == []
        for row in rows
    )


def test_every_project_has_exact_required_evidence_reason_codes():
    expected = {
        "RECONCILED_GOVERNED_IDENTITY",
        "COMPLETE_PRB_COMPONENT_VECTOR",
        "VALID_PRB_GRAND_TOTAL",
    }

    for row in load_eligibility_artifact()["records"]:
        assert set(row["evidence_reason_codes"]) == expected


def test_every_project_has_exact_required_model_reason_codes():
    expected = {
        "ANALYTICAL_PROJECT",
        "EVIDENCE_FEASIBLE",
        "USABLE_GOVERNED_MODEL_REQUEST",
    }

    for row in load_eligibility_artifact()["records"]:
        assert (
            set(row["model_eligibility_reason_codes"])
            == expected
        )


def test_source_version_conflicts_do_not_block_model_eligibility():
    rows = load_eligibility_artifact()["records"]

    conflicts = [
        row
        for row in rows
        if row["source_conflict_flag"]
    ]

    assert len(conflicts) == 3

    assert {
        row["decision_unit_id"]
        for row in conflicts
    } == EXPECTED_CONFLICT_IDS

    assert all(
        row["model_eligible"] is True
        for row in conflicts
    )

    assert all(
        row["blocking_reason_codes"] == []
        for row in conflicts
    )


def test_january_recommendation_is_not_an_eligibility_requirement():
    rows = load_eligibility_artifact()["records"]

    without_recommendation = [
        row
        for row in rows
        if row["january_recommendation_present"] is False
    ]

    assert len(without_recommendation) == 86

    assert all(
        row["model_eligible"] is True
        for row in without_recommendation
    )

    policy = load_eligibility_artifact()["eligibility_policy"]

    assert policy["benchmark_outcome_not_used"] == [
        "JANUARY_INITIAL_RECOMMENDATION"
    ]


def test_m3_7e_b_summary_is_exact():
    summary = load_eligibility_artifact()["summary"]

    assert summary == {
        "analytical_project_count": 106,
        "category_counts": EXPECTED_CATEGORY_COUNTS,
        "evidence_feasible_count": 106,
        "model_eligible_count": 106,
        "model_ineligible_count": 0,
        "eligible_with_source_version_conflict_count": 3,
        "eligible_without_january_recommendation_count": 86,
        "half_point_project_count": 3,
        "model_request_total_dollars": 1_973_520_000,
    }


def test_m3_7e_b_committed_artifact_is_deterministic_builder_output():
    projects = eligibility.load_analytical_projects()

    reconciled = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    records = eligibility.build_records(
        projects,
        reconciled,
    )

    summary = eligibility.validate_records(
        records
    )

    expected = eligibility.render_artifact(
        records,
        summary,
    )

    assert ELIGIBILITY_PATH.read_bytes() == expected


def test_missing_model_request_fails_model_eligibility_only():
    projects = eligibility.load_analytical_projects()

    reconciled = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = "transportation/barton-springs-bridge"

    changed = dict(
        reconciled[target_id]
    )

    changed["model_request_dollars"] = None

    row = eligibility.evaluate_project(
        projects[target_id],
        changed,
    )

    assert (
        row["evidence_feasibility_status"]
        == "FEASIBLE"
    )
    assert row["model_eligible"] is False

    assert (
        "MISSING_USABLE_GOVERNED_MODEL_REQUEST"
        in row["blocking_reason_codes"]
    )


def test_incomplete_component_vector_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects()

    reconciled = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = "parks/bolm-maintenance-center"

    changed = dict(
        reconciled[target_id]
    )

    changed["climate_resilience"] = None

    row = eligibility.evaluate_project(
        projects[target_id],
        changed,
    )

    assert (
        row["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert row["model_eligible"] is False

    assert (
        "INCOMPLETE_PRB_COMPONENT_VECTOR"
        in row["blocking_reason_codes"]
    )


def test_invalid_grand_total_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects()

    reconciled = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = (
        "community-facilities/acme/dougherty-arts-center"
    )

    changed = dict(
        reconciled[target_id]
    )

    changed["prb_grand_total"] = 76

    row = eligibility.evaluate_project(
        projects[target_id],
        changed,
    )

    assert (
        row["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert row["model_eligible"] is False

    assert (
        "INVALID_PRB_GRAND_TOTAL"
        in row["blocking_reason_codes"]
    )


def test_unreconciled_identity_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects()

    target_id = "transportation/barton-springs-bridge"

    row = eligibility.evaluate_project(
        projects[target_id],
        None,
    )

    assert (
        row["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert row["model_eligible"] is False

    assert (
        "UNRECONCILED_GOVERNED_IDENTITY"
        in row["blocking_reason_codes"]
    )


def test_builders_refuse_overwriting_differing_governed_artifacts():
    reconciliation_content = (
        RECONCILIATION_PATH.read_bytes()
    )

    eligibility_content = (
        ELIGIBILITY_PATH.read_bytes()
    )

    with tempfile.TemporaryDirectory() as directory:
        directory_path = Path(directory)

        recon_path = (
            directory_path
            / "reconciliation.json"
        )

        recon_path.write_text(
            '{"different": true}\n',
            encoding="utf-8",
        )

        with pytest.raises(
            reconciliation.DerivedArtifactConflictError
        ):
            reconciliation.write_artifact(
                recon_path,
                reconciliation_content,
            )

        eligibility_path = (
            directory_path
            / "eligibility.json"
        )

        eligibility_path.write_text(
            '{"different": true}\n',
            encoding="utf-8",
        )

        with pytest.raises(
            eligibility.DerivedArtifactConflictError
        ):
            eligibility.write_artifact(
                eligibility_path,
                eligibility_content,
            )