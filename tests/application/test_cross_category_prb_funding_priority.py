"""Governance tests for M3.7F cross-category PRB Funding Priority."""

from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pytest

from scripts.data import build_cross_category_prb_funding_priority as priority


ROOT = Path(__file__).resolve().parents[2]

ELIGIBILITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "cross-category-prb-model-eligibility.json"
)

PRIORITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "cross-category-prb-funding-priority.json"
)


EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}


def load_artifact() -> dict:
    return json.loads(
        PRIORITY_PATH.read_text(
            encoding="utf-8"
        )
    )


def load_records() -> list[dict]:
    return load_artifact()["records"]


def test_m3_7f_artifact_identity_and_authority_are_locked():
    artifact = load_artifact()

    assert (
        artifact["artifact_version"]
        == "m3.7f-cross-category-prb-funding-priority/1.0.0"
    )

    assert (
        artifact["governance_checkpoint"]
        == "M3.7F"
    )

    assert (
        artifact[
            "historical_decision_snapshot_date"
        ]
        == "2026-01-21"
    )

    assert (
        artifact["model_scope"]
        == "CROSS_CATEGORY_PRB_PROJECT_MODEL"
    )

    assert (
        artifact[
            "cross_category_ranking_authorized"
        ]
        is True
    )

    assert (
        artifact[
            "portfolio_selection_authorized"
        ]
        is False
    )

    assert (
        artifact[
            "runtime_integration_authorized"
        ]
        is False
    )


def test_exact_106_project_ranking_cohort():
    rows = load_records()

    assert len(rows) == 106

    ids = [
        row["decision_unit_id"]
        for row in rows
    ]

    assert len(set(ids)) == 106


def test_category_counts_are_locked():
    rows = load_records()

    actual = {}

    for row in rows:
        category = row[
            "presentation_category"
        ]

        actual[category] = (
            actual.get(category, 0)
            + 1
        )

    assert actual == EXPECTED_CATEGORY_COUNTS


def test_funding_priority_score_is_exact_official_prb_grand_total():
    eligibility = json.loads(
        ELIGIBILITY_PATH.read_text(
            encoding="utf-8"
        )
    )

    eligible_scores = {
        row["decision_unit_id"]:
        row["prb_grand_total"]
        for row in eligibility["records"]
    }

    for row in load_records():
        assert (
            row["funding_priority_score"]
            == eligible_scores[
                row["decision_unit_id"]
            ]
        )


def test_rank_is_descending_competition_rank():
    rows = load_records()

    previous_score = None
    expected_rank = None

    for position, row in enumerate(
        rows,
        start=1,
    ):
        score = row[
            "funding_priority_score"
        ]

        if score != previous_score:
            expected_rank = position
            previous_score = score

        assert (
            row[
                "funding_priority_rank"
            ]
            == expected_rank
        )


def test_every_tied_score_has_shared_substantive_rank():
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
            if (
                row[
                    "funding_priority_score"
                ]
                == score
            )
        ]

        assert len(group) > 1

        assert len(
            {
                row[
                    "funding_priority_rank"
                ]
                for row in group
            }
        ) == 1

        assert all(
            row[
                "display_tiebreak_has_analytical_meaning"
            ]
            is False
            for row in group
        )


def test_tie_display_order_is_decision_unit_id_only():
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
            if (
                row[
                    "funding_priority_score"
                ]
                == score
            )
        ]

        ids = [
            row["decision_unit_id"]
            for row in group
        ]

        assert ids == sorted(ids)

        assert [
            row[
                "display_order_within_tie"
            ]
            for row in group
        ] == list(
            range(
                1,
                len(group) + 1,
            )
        )


def test_summary_is_locked():
    assert load_artifact()["summary"] == {
        "analytical_project_count": 106,
        "category_counts": {
            "Transportation": 9,
            "Parks & Open Space": 22,
            "Watershed": 37,
            "Community Facilities": 38,
        },
        "unique_funding_priority_score_count": 35,
        "tied_score_group_count": 24,
        "projects_in_tied_score_groups": 95,
        "maximum_funding_priority_score": 83,
        "minimum_funding_priority_score": 40,
        "half_point_score_count": 3,
    }


def test_three_half_point_scores_are_preserved_exactly():
    rows = load_records()

    half_point_rows = {
        row["decision_unit_id"]:
        (
            row[
                "funding_priority_score"
            ],
            row[
                "funding_priority_rank"
            ],
        )
        for row in rows
        if (
            row[
                "funding_priority_score"
            ]
            in {
                54.5,
                53.5,
                50.5,
            }
        )
    }

    assert half_point_rows == {
        (
            "community-facilities/"
            "ems/station-03"
        ): (
            54.5,
            82,
        ),
        (
            "community-facilities/"
            "ems/station-14"
        ): (
            53.5,
            83,
        ),
        (
            "community-facilities/"
            "fleet/"
            "consolidated-service-center"
        ): (
            50.5,
            88,
        ),
    }


def test_top_and_bottom_projects_are_locked():
    rows = load_records()

    top = rows[0]

    assert (
        top["decision_unit_id"]
        == "parks/bolm-maintenance-center"
    )

    assert (
        top["funding_priority_score"]
        == 83
    )

    assert (
        top["funding_priority_rank"]
        == 1
    )

    bottom = rows[-1]

    assert (
        bottom["decision_unit_id"]
        == (
            "community-facilities/"
            "fire/education-building-b"
        )
    )

    assert (
        bottom["funding_priority_score"]
        == 40
    )

    assert (
        bottom["funding_priority_rank"]
        == 106
    )


def test_cross_category_comparability_policy_is_explicit():
    policy = load_artifact()[
        "comparability_policy"
    ]

    assert (
        policy["decision"]
        == (
            "AUTHORIZED_FOR_COMMON_"
            "ORDINAL_PRIORITY"
        )
    )

    assert (
        policy["interpretation"]
        == (
            "ORDINAL_PRB_BASED_"
            "PROJECT_PRIORITY"
        )
    )

    assert (
        policy[
            "normalization_authorized"
        ]
        is False
    )

    assert set(
        policy[
            "not_authorized_interpretations"
        ]
    ) == {
        "CARDINAL_PUBLIC_BENEFIT",
        "COST_EFFECTIVENESS",
        "BENEFIT_COST_RATIO",
        (
            "HISTORICAL_RECOMMENDATION_"
            "PROBABILITY"
        ),
        "ADDITIVE_PORTFOLIO_UTILITY",
    }


def test_comparability_basis_is_locked():
    policy = load_artifact()[
        "comparability_policy"
    ]

    assert set(
        policy["basis"]
    ) == {
        "COMMON_OFFICIAL_PRB_RUBRIC",
        (
            "COMMON_SIX_COMPONENT_"
            "WEIGHTED_STRUCTURE"
        ),
        (
            "COMMON_ZERO_TO_100_"
            "GRAND_TOTAL_SCALE"
        ),
        (
            "ALL_106_SATISFY_PRB_"
            "BASELINE_PREREQUISITE"
        ),
        (
            "ALL_106_HAVE_COMPLETE_"
            "VALID_PRB_SCORE_VECTORS"
        ),
    }


def test_ranking_policy_is_explicit():
    policy = load_artifact()[
        "ranking_policy"
    ]

    assert (
        policy[
            "funding_priority_score_authority"
        ]
        == "OFFICIAL_PRB_GRAND_TOTAL"
    )

    assert (
        policy["direction"]
        == "HIGHER_IS_HIGHER_PRIORITY"
    )

    assert (
        policy["rank_method"]
        == "COMPETITION_RANK_DESCENDING"
    )

    assert (
        policy["tie_policy"]
        == "SHARED_SUBSTANTIVE_RANK"
    )

    assert (
        policy["display_tiebreak"]
        == "DECISION_UNIT_ID_ASCENDING"
    )

    assert (
        policy[
            "display_tiebreak_has_analytical_meaning"
        ]
        is False
    )


def test_forbidden_score_transformations_are_locked():
    policy = load_artifact()[
        "ranking_policy"
    ]

    assert set(
        policy[
            "forbidden_score_transformations"
        ]
    ) == {
        "CATEGORY_NORMALIZATION",
        "Z_SCORE_NORMALIZATION",
        "PERCENTILE_NORMALIZATION",
        "SCORE_PER_DOLLAR",
        "INVENTED_CLIMATE_CAPITAL_WEIGHTS",
    }


def test_forbidden_analytical_tiebreakers_are_locked():
    policy = load_artifact()[
        "ranking_policy"
    ]

    assert set(
        policy[
            "forbidden_analytical_tiebreakers"
        ]
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


def test_ranking_records_have_no_portfolio_membership_field():
    forbidden = {
        "selected",
        "recommended",
        "portfolio_selected",
        "funded",
        "portfolio_status",
    }

    for row in load_records():
        assert (
            forbidden
            .intersection(
                set(row)
            )
            == set()
        )


def test_committed_artifact_is_deterministic_builder_output():
    eligible = (
        priority
        .load_eligible_records(
            ELIGIBILITY_PATH
        )
    )

    records = (
        priority
        .build_ranking_records(
            eligible
        )
    )

    summary = (
        priority
        .validate_ranking_records(
            records
        )
    )

    expected = (
        priority.render_artifact(
            records,
            summary,
        )
    )

    assert (
        PRIORITY_PATH.read_bytes()
        == expected
    )


def test_model_ineligible_project_fails_closed():
    artifact = (
        priority.load_eligibility(
            ELIGIBILITY_PATH
        )
    )

    records = [
        dict(record)
        for record
        in artifact["records"]
    ]

    records[0][
        "model_eligible"
    ] = False

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = (
            Path(directory)
            / "eligibility.json"
        )

        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError,
            match="model-ineligible",
        ):
            priority.load_eligible_records(
                path
            )


def test_evidence_infeasible_project_fails_closed():
    artifact = (
        priority.load_eligibility(
            ELIGIBILITY_PATH
        )
    )

    records = [
        dict(record)
        for record
        in artifact["records"]
    ]

    records[0][
        "evidence_feasibility_status"
    ] = "INFEASIBLE"

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = (
            Path(directory)
            / "eligibility.json"
        )

        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError,
            match="evidence-infeasible",
        ):
            priority.load_eligible_records(
                path
            )


@pytest.mark.parametrize(
    "invalid_score",
    [
        101,
        -1,
        54.25,
        True,
        "54",
    ],
)
def test_invalid_prb_score_fails_closed(
    invalid_score,
):
    artifact = (
        priority.load_eligibility(
            ELIGIBILITY_PATH
        )
    )

    records = [
        dict(record)
        for record
        in artifact["records"]
    ]

    records[0][
        "prb_grand_total"
    ] = invalid_score

    temporary = {
        **artifact,
        "records": records,
    }

    with tempfile.TemporaryDirectory() as directory:
        path = (
            Path(directory)
            / "eligibility.json"
        )

        path.write_text(
            json.dumps(temporary),
            encoding="utf-8",
        )

        with pytest.raises(
            priority.FundingPriorityError
        ):
            priority.load_eligible_records(
                path
            )

def test_all_106_projects_satisfy_prb_baseline_prerequisite():
    priority.validate_baseline_prerequisite()

def test_builder_refuses_differing_existing_governed_artifact():
    eligible = (
        priority
        .load_eligible_records(
            ELIGIBILITY_PATH
        )
    )

    records = (
        priority
        .build_ranking_records(
            eligible
        )
    )

    summary = (
        priority
        .validate_ranking_records(
            records
        )
    )

    content = (
        priority.render_artifact(
            records,
            summary,
        )
    )

    with tempfile.TemporaryDirectory() as directory:
        path = (
            Path(directory)
            / "priority.json"
        )

        path.write_text(
            '{"different": true}\n',
            encoding="utf-8",
        )

        with pytest.raises(
            priority.DerivedArtifactConflictError,
            match=(
                "Refusing to overwrite differing"
            ),
        ):
            priority.write_artifact(
                path,
                content,
            )