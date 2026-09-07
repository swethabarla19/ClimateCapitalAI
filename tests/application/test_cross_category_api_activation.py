"""Focused M3.8D1 tests for parallel cross-category FastAPI activation."""

from __future__ import annotations

from fastapi.testclient import TestClient

from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.main import app


DATA_VERSION = (
    "climatecapital-austin-"
    "2026-01-21-cross-category-v2"
)


def plan_payload(
    budget: int,
    *,
    resolutions: list[dict] | None = None,
) -> dict:
    return {
        "contract_version": (
            CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ),
        "data_version": DATA_VERSION,
        "available_budget_dollars": budget,
        "boundary_resolutions": (
            resolutions or []
        ),
        "expected_fingerprint": None,
    }


def test_cross_category_bootstrap_exposes_106_project_catalog():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/cross-category/bootstrap"
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "SUCCESS"

    assert (
        body["endpoint"]
        == "/api/v1/cross-category/bootstrap"
    )

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    catalog = body["data"]["catalog"]

    assert catalog["project_count"] == 106

    assert (
        len(
            catalog["projects"]
        )
        == 106
    )

    assert (
        catalog[
            "governed_request_total_dollars"
        ]
        == 1_973_520_000
    )


def test_cross_category_bootstrap_exposes_runtime_activation_flag():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/cross-category/bootstrap"
        )

    catalog = (
        response.json()[
            "data"
        ][
            "catalog"
        ]
    )

    assert (
        catalog[
            "cross_category_ranking_authorized"
        ]
        is True
    )

    assert (
        catalog[
            "portfolio_selection_authorized"
        ]
        is True
    )

    assert (
        catalog[
            "runtime_integration_authorized"
        ]
        is True
    )


def test_cross_category_bootstrap_contains_no_historical_recommendation_fields():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/cross-category/bootstrap"
        )

    projects = (
        response.json()[
            "data"
        ][
            "catalog"
        ][
            "projects"
        ]
    )

    forbidden = {
        "january_recommendation_dollars",
        "january_recommendation_present",
        "historical_recommendation_amount_dollars",
        "historical_category_allocation",
    }

    for project in projects:
        assert (
            forbidden
            & set(project)
        ) == set()


def test_700m_api_returns_score_67_analyst_boundary():
    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=plan_payload(
                700_000_000
            ),
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "SUCCESS"

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
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

    assert (
        len(
            [
                candidate
                for candidate
                in boundary[
                    "candidates"
                ]
                if candidate[
                    "individually_budget_feasible"
                ]
            ]
        )
        == 5
    )


def test_750m_api_returns_score_65_analyst_boundary():
    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=plan_payload(
                750_000_000
            ),
        )

    assert response.status_code == 200

    result = response.json()[
        "data"
    ]

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

    assert (
        len(
            [
                candidate
                for candidate
                in boundary[
                    "candidates"
                ]
                if candidate[
                    "individually_budget_feasible"
                ]
            ]
        )
        == 8
    )


def test_332m_api_applies_unique_budget_feasible_7th_street_selection():
    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=plan_payload(
                332_000_000
            ),
        )

    assert response.status_code == 200

    result = response.json()[
        "data"
    ]

    selected = {
        project[
            "decision_unit_id"
        ]:
            project
        for project
        in result[
            "selected_projects"
        ]
    }

    assert (
        "transportation/"
        "act-plan-7th-street"
        in selected
    )

    assert (
        selected[
            "transportation/"
            "act-plan-7th-street"
        ][
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


def test_wrong_cross_category_data_version_returns_409_with_v2_identity():
    payload = plan_payload(
        700_000_000
    )

    payload[
        "data_version"
    ] = "wrong-data-version"

    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=payload,
        )

    assert response.status_code == 409

    body = response.json()

    assert body["status"] == "ERROR"

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


def test_wrong_cross_category_contract_version_returns_409_with_v2_identity():
    payload = plan_payload(
        700_000_000
    )

    payload[
        "contract_version"
    ] = "wrong-contract-version"

    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=payload,
        )

    assert response.status_code == 409

    body = response.json()

    assert (
        body["error"]["error_code"]
        == "CONTRACT_VERSION_CONFLICT"
    )

    assert (
        body["identity"]["contract_version"]
        == CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    )

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )


def test_cross_category_unknown_field_fails_closed():
    payload = plan_payload(
        700_000_000
    )

    payload[
        "invented_optimizer_weight"
    ] = 0.75

    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
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


def test_resolution_outside_active_tier_returns_422():
    resolution = {
        "funding_priority_score": 67,
        "funding_priority_rank": 28,
        "selected_decision_unit_ids": [
            (
                "transportation/"
                "barton-springs-bridge"
            )
        ],
        (
            "advance_with_feasible_"
            "same_tier_project_acknowledged"
        ): False,
    }

    with TestClient(app) as client:
        response = client.post(
            (
                "/api/v1/cross-category/"
                "plans/evaluate"
            ),
            json=plan_payload(
                700_000_000,
                resolutions=[
                    resolution
                ],
            ),
        )

    assert response.status_code == 422

    body = response.json()

    assert (
        body["error"]["error_code"]
        == "MALFORMED_REQUEST"
    )

    assert (
        "outside the active priority tier"
        in body["error"]["message"]
    )


def test_standard_bootstrap_is_now_cross_category_v2():
    with TestClient(app) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "SUCCESS"

    catalog = body["data"]["catalog"]

    assert catalog["project_count"] == 106
    assert len(catalog["projects"]) == 106

    assert (
        body["identity"]["data_version"]
        == DATA_VERSION
    )


def test_health_endpoint_remains_available():
    with TestClient(app) as client:
        response = client.get(
            "/healthz"
        )

    assert response.status_code == 200

    assert (
        response.json()[
            "data"
        ][
            "status"
        ]
        == "READY"
    )