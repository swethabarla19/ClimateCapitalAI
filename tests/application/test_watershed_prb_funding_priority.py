"""Governance tests for M3.7C Watershed PRB Funding Priority."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from climatecapital.contracts.versions import GOVERNED_PROJECT_IDS
from scripts.data import build_watershed_prb_funding_priority as priority


ROOT = Path(__file__).resolve().parents[2]

ELIGIBILITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "watershed-prb-model-eligibility.json"
)

PRIORITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "watershed-prb-funding-priority.json"
)


EXPECTED_RANKING = (
    ("5282.134", 74, 1),
    ("5282.043", 73, 2),
    ("5282.133", 73, 2),
    ("5789.126", 73, 2),
    ("5754.089", 71, 5),
    ("5282.150", 69, 6),
    ("5282.162", 68, 7),
    ("5789.145", 68, 7),
    ("5789.075", 67, 9),
    ("5848.092", 67, 9),
    ("8598.014", 67, 9),
    ("4015.001", 66, 12),
    ("5754.145", 66, 12),
    ("5789.146", 66, 12),
    ("10878.010", 65, 15),
    ("5754.139", 65, 15),
    ("5789.136", 65, 15),
    ("5789.107", 64, 18),
    ("5848.091", 64, 18),
    ("11889.004", 63, 20),
    ("5754.149", 63, 20),
    ("5754.147", 62, 22),
    ("5848.053", 62, 22),
    ("5848.071", 62, 22),
    ("9999.236", 62, 22),
    ("5789.141", 61, 26),
    ("6039.109", 61, 26),
    ("5789.127", 60, 28),
    ("5789.150", 60, 28),
    ("7492.011", 59, 30),
    ("7492.032", 59, 30),
    ("9999.235", 59, 30),
    ("5789.121", 58, 33),
    ("5789.139", 56, 34),
    ("5848.087", 56, 34),
    ("7492.045", 56, 34),
    ("5848.070", 52, 37),
)


def load_artifact() -> dict:
    return json.loads(
        PRIORITY_PATH.read_text(encoding="utf-8")
    )


def load_records() -> list[dict]:
    return load_artifact()["records"]


def test_m3_7c_artifact_identity_and_scope_are_locked():
    artifact = load_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7c-watershed-prb-funding-priority/1.0.0"
    )
    assert artifact["governance_checkpoint"] == "M3.7C"
    assert (
        artifact["historical_decision_snapshot_date"]
        == "2026-01-21"
    )
    assert (
        artifact["model_scope"]
        == "WATERSHED_PRB_PROJECT_MODEL"
    )

    assert artifact["portfolio_selection_authorized"] is False
    assert artifact["runtime_integration_authorized"] is False


def test_exact_37_project_ranking_cohort():
    rows = load_records()

    assert len(rows) == 37

    ids = [
        row["canonical_project_id"]
        for row in rows
    ]

    assert len(set(ids)) == 37
    assert set(ids) == set(GOVERNED_PROJECT_IDS)


def test_exact_governed_funding_priority_ranking():
    actual = tuple(
        (
            row["canonical_project_id"],
            row["funding_priority_score"],
            row["funding_priority_rank"],
        )
        for row in load_records()
    )

    assert actual == EXPECTED_RANKING


def test_funding_priority_score_is_official_prb_grand_total():
    eligibility = json.loads(
        ELIGIBILITY_PATH.read_text(encoding="utf-8")
    )

    eligible_scores = {
        row["canonical_project_id"]: row["prb_grand_total"]
        for row in eligibility["records"]
    }

    for row in load_records():
        assert (
            row["funding_priority_score"]
            == eligible_scores[row["canonical_project_id"]]
        )


def test_rank_is_descending_competition_rank():
    rows = load_records()

    previous_score = None
    expected_rank = None

    for position, row in enumerate(rows, start=1):
        score = row["funding_priority_score"]

        if score != previous_score:
            expected_rank = position
            previous_score = score

        assert row["funding_priority_rank"] == expected_rank


def test_score_73_projects_share_substantive_rank_two():
    rows = [
        row
        for row in load_records()
        if row["funding_priority_score"] == 73
    ]

    assert [
        row["canonical_project_id"]
        for row in rows
    ] == [
        "5282.043",
        "5282.133",
        "5789.126",
    ]

    assert all(
        row["funding_priority_rank"] == 2
        for row in rows
    )

    assert all(
        row["is_tied"] is True
        for row in rows
    )

    assert all(
        row["tie_group_size"] == 3
        for row in rows
    )

    assert [
        row["display_order_within_tie"]
        for row in rows
    ] == [1, 2, 3]


def test_tie_display_order_never_changes_substantive_rank():
    rows = load_records()

    tied_scores = {
        row["funding_priority_score"]
        for row in rows
        if row["is_tied"]
    }

    for score in tied_scores:
        group = [
            row
            for row in rows
            if row["funding_priority_score"] == score
        ]

        assert len(
            {
                row["funding_priority_rank"]
                for row in group
            }
        ) == 1

        assert [
            row["canonical_project_id"]
            for row in group
        ] == sorted(
            row["canonical_project_id"]
            for row in group
        )

        assert all(
            row["display_tiebreak_has_analytical_meaning"]
            is False
            for row in group
        )


def test_tie_distribution_is_locked():
    summary = load_artifact()["summary"]

    assert summary == {
        "analytical_project_count": 37,
        "unique_funding_priority_score_count": 17,
        "tied_score_group_count": 12,
        "projects_in_tied_score_groups": 32,
        "maximum_funding_priority_score": 74,
        "minimum_funding_priority_score": 52,
    }


def test_top_and_bottom_projects_are_locked():
    rows = load_records()

    assert rows[0]["canonical_project_id"] == "5282.134"
    assert rows[0]["funding_priority_score"] == 74
    assert rows[0]["funding_priority_rank"] == 1
    assert rows[0]["is_tied"] is False

    assert rows[-1]["canonical_project_id"] == "5848.070"
    assert rows[-1]["funding_priority_score"] == 52
    assert rows[-1]["funding_priority_rank"] == 37
    assert rows[-1]["is_tied"] is False


def test_5754_149_request_conflict_has_no_ranking_special_case():
    row = next(
        row
        for row in load_records()
        if row["canonical_project_id"] == "5754.149"
    )

    assert row["funding_priority_score"] == 63
    assert row["funding_priority_rank"] == 20
    assert row["is_tied"] is True
    assert row["tie_group_size"] == 2

    # Ranking artifact intentionally contains no request-conflict
    # override or historical recommendation input.
    assert "request_version_conflict" not in row
    assert "january_recommendation_present" not in row


def test_ranking_policy_is_explicit_and_non_optimizing():
    policy = load_artifact()["ranking_policy"]

    assert (
        policy["funding_priority_score_authority"]
        == "OFFICIAL_PRB_GRAND_TOTAL"
    )
    assert policy["direction"] == "HIGHER_IS_HIGHER_PRIORITY"
    assert (
        policy["rank_method"]
        == "COMPETITION_RANK_DESCENDING"
    )
    assert policy["tie_policy"] == "SHARED_SUBSTANTIVE_RANK"
    assert (
        policy["display_tiebreak"]
        == "CANONICAL_PROJECT_ID_ASCENDING"
    )
    assert (
        policy[
            "display_tiebreak_has_analytical_meaning"
        ]
        is False
    )


def test_forbidden_analytical_tiebreakers_are_locked():
    policy = load_artifact()["ranking_policy"]

    assert set(
        policy["forbidden_analytical_tiebreakers"]
    ) == {
        "PROJECT_COST",
        "JANUARY_INITIAL_RECOMMENDATION",
        "INDIVIDUAL_PRB_COMPONENT",
        "RNA_GEOMETRY",
        "FEMA_FLOODPLAIN_CONTEXT",
        "EAZ_2021_CONTEXT",
        "WATERSHED_PROBLEM_SCORE_CONTEXT",
        "SOURCE_TABLE_ROW_ORDER",
        "PROJECT_NAME",
    }


def test_ranking_records_have_no_portfolio_selection_fields():
    allowed_keys = {
        "canonical_project_id",
        "model_scope",
        "funding_priority_score",
        "funding_priority_rank",
        "is_tied",
        "tie_group_size",
        "display_order_within_tie",
        "display_tiebreak_has_analytical_meaning",
    }

    for row in load_records():
        assert set(row) == allowed_keys


def test_committed_artifact_is_deterministic_builder_output():
    eligible = priority.load_eligible_records(
        ELIGIBILITY_PATH
    )

    records = priority.build_ranking_records(
        eligible
    )

    summary = priority.validate_ranking_records(
        records
    )

    expected = priority.render_artifact(
        records,
        summary,
    )

    assert PRIORITY_PATH.read_bytes() == expected


def test_model_ineligible_project_fails_closed():
    artifact = priority.load_eligibility(
        ELIGIBILITY_PATH
    )

    records = [
        dict(record)
        for record in artifact["records"]
    ]

    records[0]["model_eligible"] = False

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "eligibility.json"
        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError,
            match="model-ineligible",
        ):
            priority.load_eligible_records(path)


def test_evidence_infeasible_project_fails_closed():
    artifact = priority.load_eligibility(
        ELIGIBILITY_PATH
    )

    records = [
        dict(record)
        for record in artifact["records"]
    ]

    records[0]["evidence_feasibility_status"] = "INFEASIBLE"

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "eligibility.json"
        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError,
            match="evidence-infeasible",
        ):
            priority.load_eligible_records(path)


def test_invalid_prb_score_fails_closed():
    artifact = priority.load_eligibility(
        ELIGIBILITY_PATH
    )

    records = [
        dict(record)
        for record in artifact["records"]
    ]

    records[0]["prb_grand_total"] = 101

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "eligibility.json"
        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError,
            match="between 0 and 100",
        ):
            priority.load_eligible_records(path)


def test_builder_refuses_differing_existing_governed_artifact():
    eligible = priority.load_eligible_records(
        ELIGIBILITY_PATH
    )

    records = priority.build_ranking_records(
        eligible
    )

    summary = priority.validate_ranking_records(
        records
    )

    content = priority.render_artifact(
        records,
        summary,
    )

    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "priority.json"

        path.write_text(
            '{"different": true}\n',
            encoding="utf-8",
        )

        with pytest.raises(
            priority.DerivedArtifactConflictError,
            match="Refusing to overwrite differing",
        ):
            priority.write_artifact(
                path,
                content,
            )