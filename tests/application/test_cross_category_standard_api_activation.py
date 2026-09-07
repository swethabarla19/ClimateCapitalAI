"""M3.8D3 standard FastAPI activation tests for runtime-v2."""

from __future__ import annotations

from fastapi.testclient import TestClient

from climatecapital.contracts.cross_category_release import (
    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.main import app


DATA_VERSION = (
    "climatecapital-austin-"
    "2026-01-21-cross-category-v2"
)

RELEASE_ID = (
    "efb3783b2f4c7568012fb9ae590ff40dbf5a46d18a3ff1942a22d424a4b52207"
)


def plan_payload(
    budget: int,
    *,
    data_version: str = DATA_VERSION,
) -> dict:
    return {
        "contract_version":
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
        "data_version":
            data_version,
        "available_budget_dollars":
            budget,
        "boundary_resolutions":
            [],
        "expected_fingerprint":
            None,
    }


def test_standard_bootstrap_serves_cross_category_v2():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "SUCCESS"
    assert body["endpoint"] == "/api/v1/bootstrap"

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )

    catalog = body["data"]["catalog"]

    assert catalog["project_count"] == 106

    assert (
        catalog[
            "governed_request_total_dollars"
        ]
        == 1_973_520_000
    )


def test_standard_bootstrap_exposes_truthful_zero_geometry():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    map_context = (
        response.json()[
            "data"
        ][
            "map_context"
        ]
    )

    assert map_context["mapped_project_count"] == 0
    assert map_context["unmapped_project_count"] == 106
    assert map_context["features"] == []

    assert (
        map_context["fabricated_geometry"]
        is False
    )


def test_standard_bootstrap_runtime_configuration_is_not_fixture_mode():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    configuration = (
        response.json()[
            "data"
        ][
            "public_configuration"
        ]
    )

    assert (
        configuration[
            "fixture_mode"
        ]
        is False
    )


def test_standard_700m_plan_stops_at_score_67_boundary():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=plan_payload(
                700_000_000
            ),
        )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )

    result = body["data"]

    assert (
        result["status"]
        == "ANALYST_RESOLUTION_REQUIRED"
    )

    boundary = result[
        "unresolved_boundary"
    ]

    assert (
        boundary[
            "funding_priority_score"
        ]
        == 67
    )

    assert (
        boundary[
            "funding_priority_rank"
        ]
        == 28
    )

    assert (
        boundary[
            "remaining_budget_before_tier_dollars"
        ]
        == 108_275_000
    )


def test_standard_750m_plan_stops_at_score_65_boundary():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=plan_payload(
                750_000_000
            ),
        )

    assert response.status_code == 200

    boundary = (
        response.json()[
            "data"
        ][
            "unresolved_boundary"
        ]
    )

    assert (
        boundary[
            "funding_priority_score"
        ]
        == 65
    )

    assert (
        boundary[
            "funding_priority_rank"
        ]
        == 37
    )

    assert (
        boundary[
            "remaining_budget_before_tier_dollars"
        ]
        == 33_280_000
    )


def test_standard_332m_plan_preserves_unique_budget_feasible_selection():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=plan_payload(
                332_000_000
            ),
        )

    assert response.status_code == 200

    selected = {
        project[
            "decision_unit_id"
        ]:
            project
        for project
        in response.json()[
            "data"
        ][
            "selected_projects"
        ]
    }

    project = selected[
        "transportation/"
        "act-plan-7th-street"
    ]

    assert (
        project[
            "selection_source"
        ]
        == (
            "AUTO_UNIQUE_"
            "BUDGET_FEASIBLE"
        )
    )

    assert (
        "community-facilities/"
        "public-health/northeast"
        not in selected
    )


def test_standard_plan_wrong_data_version_returns_v2_409():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=plan_payload(
                700_000_000,
                data_version=(
                    "wrong-data-version"
                ),
            ),
        )

    assert response.status_code == 409

    body = response.json()

    assert (
        body["error"]["error_code"]
        == "DATA_VERSION_CONFLICT"
    )

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )


def test_standard_plan_unknown_field_fails_closed_with_v2_identity():
    payload = plan_payload(
        700_000_000
    )

    payload[
        "invented_optimizer_weight"
    ] = 0.75

    with TestClient(app) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=payload,
        )

    assert response.status_code == 422

    body = response.json()

    assert (
        body["error"]["error_code"]
        == "UNKNOWN_FIELD"
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )


def test_standard_benchmark_serves_isolated_historical_outcome():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/benchmark"
        )

    assert response.status_code == 200

    body = response.json()

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )

    benchmark = (
        body["data"][
            "benchmark"
        ]
    )

    assert (
        benchmark[
            "full_initial_recommendation_dollars"
        ]
        == 700_000_000
    )

    assert (
        benchmark[
            "matched_analytical_cohort_dollars"
        ]
        == 332_000_000
    )

    assert (
        benchmark[
            "outside_analytical_cohort_dollars"
        ]
        == 368_000_000
    )

    assert (
        benchmark[
            "historically_recommended_project_count"
        ]
        == 20
    )

    assert (
        benchmark[
            "ranking_input"
        ]
        is False
    )

    assert (
        benchmark[
            "portfolio_selection_input"
        ]
        is False
    )


def test_standard_benchmark_compare_is_explicitly_not_activated():
    with TestClient(app) as client:
        response = client.post(
            "/api/v1/benchmark/compare",
            json={},
        )

    assert response.status_code == 503

    body = response.json()

    assert (
        body["error"]["error_code"]
        == "OPTIONAL_DEPENDENCY_UNAVAILABLE"
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )


def test_transition_alias_bootstrap_matches_standard_release():
    with TestClient(app) as client:
        standard = client.get(
            "/api/v1/bootstrap"
        )

        alias = client.get(
            "/api/v1/cross-category/bootstrap"
        )

    assert standard.status_code == 200
    assert alias.status_code == 200

    assert (
        standard.json()[
            "identity"
        ][
            "release_id"
        ]
        == alias.json()[
            "identity"
        ][
            "release_id"
        ]
        == RELEASE_ID
    )

    assert (
        standard.json()[
            "data"
        ][
            "catalog"
        ]
        == alias.json()[
            "data"
        ][
            "catalog"
        ]
    )


def test_transition_alias_plan_matches_standard_plan():
    payload = plan_payload(
        700_000_000
    )

    with TestClient(app) as client:
        standard = client.post(
            "/api/v1/plans/evaluate",
            json=payload,
        )

        alias = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=payload,
        )

    assert standard.status_code == 200
    assert alias.status_code == 200

    assert (
        standard.json()["data"]
        == alias.json()["data"]
    )