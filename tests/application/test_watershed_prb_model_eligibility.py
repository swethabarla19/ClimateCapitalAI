"""Governance tests for M3.7B Watershed PRB-model eligibility."""

from __future__ import annotations

import json
import tempfile
from collections import Counter
from pathlib import Path

import pytest

from climatecapital.contracts.versions import (
    ACTIVE_FAMILY_PROJECT_IDS,
    GOVERNED_PROJECT_IDS,
)
from scripts.data import build_watershed_prb_model_eligibility as eligibility


ROOT = Path(__file__).resolve().parents[2]

WATERSHED_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "source_rows"
    / "watershed.json"
)

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "watershed-prb-reconciliation.json"
)

ELIGIBILITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "watershed-prb-model-eligibility.json"
)


def load_artifact() -> dict:
    return json.loads(
        ELIGIBILITY_PATH.read_text(encoding="utf-8")
    )


def load_records() -> list[dict]:
    return load_artifact()["records"]


def test_m3_7b_artifact_identity_and_scope_are_locked():
    artifact = load_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7b-watershed-prb-model-eligibility/1.0.0"
    )
    assert artifact["governance_checkpoint"] == "M3.7B"
    assert (
        artifact["historical_decision_snapshot_date"]
        == "2026-01-21"
    )
    assert (
        artifact["model_scope"]
        == "WATERSHED_PRB_PROJECT_MODEL"
    )

    # Eligibility approval is not runtime activation.
    assert artifact["runtime_integration_authorized"] is False


def test_exact_37_project_model_eligible_cohort():
    rows = load_records()

    assert len(rows) == 37

    ids = tuple(
        row["canonical_project_id"]
        for row in rows
    )

    assert ids == GOVERNED_PROJECT_IDS
    assert len(set(ids)) == 37

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
        "RECONCILED_CANONICAL_IDENTITY",
        "COMPLETE_PRB_COMPONENT_VECTOR",
        "VALID_PRB_GRAND_TOTAL",
    }

    for row in load_records():
        assert set(row["evidence_reason_codes"]) == expected


def test_every_project_has_exact_required_model_reason_codes():
    expected = {
        "ANALYTICAL_PROJECT",
        "EVIDENCE_FEASIBLE",
        "USABLE_CANONICAL_REQUEST",
    }

    for row in load_records():
        assert (
            set(row["model_eligibility_reason_codes"])
            == expected
        )


def test_5754_149_request_conflict_does_not_block_eligibility():
    row = next(
        row
        for row in load_records()
        if row["canonical_project_id"] == "5754.149"
    )

    assert row["evidence_feasibility_status"] == "FEASIBLE"
    assert row["model_eligible"] is True

    assert row["request_version_conflict"] is True

    # Canonical November request remains the modeling cost authority.
    assert row["canonical_request_dollars"] == 2_500_000

    assert row["blocking_reason_codes"] == []


def test_january_recommendation_is_not_an_eligibility_requirement():
    rows = load_records()

    without_recommendation = [
        row
        for row in rows
        if row["january_recommendation_present"] is False
    ]

    assert len(without_recommendation) == 25

    assert all(
        row["model_eligible"] is True
        for row in without_recommendation
    )


def test_contextual_evidence_is_explicitly_not_required():
    policy = load_artifact()["eligibility_policy"]

    assert set(
        policy["contextual_evidence_not_required"]
    ) == {
        "RNA_GEOMETRY",
        "FEMA_FLOODPLAIN_CONTEXT",
        "EAZ_2021_CONTEXT",
        "WATERSHED_PROBLEM_SCORE_CONTEXT",
    }


def test_historical_recommendation_is_explicitly_excluded():
    policy = load_artifact()["eligibility_policy"]

    assert policy["benchmark_outcome_not_used"] == [
        "JANUARY_INITIAL_RECOMMENDATION"
    ]


def test_summary_matches_record_level_results():
    artifact = load_artifact()
    summary = artifact["summary"]
    rows = artifact["records"]

    assert summary == {
        "analytical_project_count": 37,
        "evidence_feasible_count": 37,
        "model_eligible_count": 37,
        "model_ineligible_count": 0,
        "eligible_with_request_version_conflict_count": 1,
        "eligible_without_january_recommendation_count": 25,
    }

    assert (
        sum(
            row["evidence_feasibility_status"] == "FEASIBLE"
            for row in rows
        )
        == 37
    )

    assert (
        sum(
            row["model_eligible"] is True
            for row in rows
        )
        == 37
    )


def test_existing_12_project_runtime_family_is_not_redefined():
    artifact = load_artifact()

    assert artifact["runtime_integration_authorized"] is False

    # M3.7B proves PRB-model eligibility for all 37 but does not
    # mutate the existing runtime-family contract.
    assert len(GOVERNED_PROJECT_IDS) == 37
    assert len(ACTIVE_FAMILY_PROJECT_IDS) == 12

    assert set(ACTIVE_FAMILY_PROJECT_IDS).issubset(
        set(GOVERNED_PROJECT_IDS)
    )


def test_committed_artifact_is_deterministic_builder_output():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    reconciliation = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    records = eligibility.build_records(
        projects,
        reconciliation,
    )

    summary = eligibility.validate_records(
        records
    )

    expected = eligibility.render_artifact(
        records,
        summary,
    )

    assert ELIGIBILITY_PATH.read_bytes() == expected


def test_missing_canonical_request_fails_model_eligibility():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    reconciliation = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = "5282.134"

    changed = {
        project_id: dict(record)
        for project_id, record in reconciliation.items()
    }

    changed[target_id] = dict(changed[target_id])
    changed[target_id]["november_request_dollars"] = None

    record = eligibility.evaluate_project(
        projects[target_id],
        changed[target_id],
    )

    assert record["evidence_feasibility_status"] == "FEASIBLE"
    assert record["model_eligible"] is False

    assert (
        "MISSING_USABLE_CANONICAL_REQUEST"
        in record["blocking_reason_codes"]
    )


def test_incomplete_prb_vector_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    reconciliation = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = "5282.134"
    changed = dict(reconciliation[target_id])
    changed["climate_resilience"] = None

    record = eligibility.evaluate_project(
        projects[target_id],
        changed,
    )

    assert (
        record["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert record["model_eligible"] is False

    assert (
        "INCOMPLETE_PRB_COMPONENT_VECTOR"
        in record["blocking_reason_codes"]
    )

    assert (
        "INVALID_PRB_GRAND_TOTAL"
        in record["blocking_reason_codes"]
    )


def test_invalid_grand_total_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    reconciliation = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    target_id = "5282.134"
    changed = dict(reconciliation[target_id])
    changed["prb_grand_total"] = 73

    record = eligibility.evaluate_project(
        projects[target_id],
        changed,
    )

    assert (
        record["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert record["model_eligible"] is False

    assert (
        "INVALID_PRB_GRAND_TOTAL"
        in record["blocking_reason_codes"]
    )


def test_unreconciled_identity_fails_evidence_and_model_eligibility():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    target_id = "5282.134"

    record = eligibility.evaluate_project(
        projects[target_id],
        None,
    )

    assert (
        record["evidence_feasibility_status"]
        == "INFEASIBLE"
    )
    assert record["model_eligible"] is False

    assert (
        "UNRECONCILED_CANONICAL_IDENTITY"
        in record["blocking_reason_codes"]
    )


def test_builder_refuses_differing_existing_governed_artifact():
    projects = eligibility.load_analytical_projects(
        WATERSHED_PATH
    )

    reconciliation = eligibility.load_reconciliation(
        RECONCILIATION_PATH
    )

    records = eligibility.build_records(
        projects,
        reconciliation,
    )

    summary = eligibility.validate_records(
        records
    )

    content = eligibility.render_artifact(
        records,
        summary,
    )

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "eligibility.json"
        path.write_text(
            '{"different": true}\n',
            encoding="utf-8",
        )

        with pytest.raises(
            eligibility.DerivedArtifactConflictError,
            match="Refusing to overwrite differing governed eligibility artifact",
        ):
            eligibility.write_artifact(
                path,
                content,
            )


def test_reason_code_counts_are_complete_and_nonduplicated():
    rows = load_records()

    evidence_counts = Counter(
        reason
        for row in rows
        for reason in row["evidence_reason_codes"]
    )

    model_counts = Counter(
        reason
        for row in rows
        for reason in row["model_eligibility_reason_codes"]
    )

    assert evidence_counts == {
        "RECONCILED_CANONICAL_IDENTITY": 37,
        "COMPLETE_PRB_COMPONENT_VECTOR": 37,
        "VALID_PRB_GRAND_TOTAL": 37,
    }

    assert model_counts == {
        "ANALYTICAL_PROJECT": 37,
        "EVIDENCE_FEASIBLE": 37,
        "USABLE_CANONICAL_REQUEST": 37,
    }
