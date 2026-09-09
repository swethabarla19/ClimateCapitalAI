"""Persistent API integration coverage for the activated cross-category runtime."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from climatecapital.api.runtime import RuntimeLoadError, load_runtime_state
from climatecapital.contracts.api import (
    HealthSuccessEnvelope,
)
from climatecapital.contracts.cross_category_api import (
    CrossCategoryBenchmarkSuccessEnvelope,
    CrossCategoryPlanSuccessEnvelope,
    CrossCategoryRuntimeBootstrapEnvelope,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.main import app


ROOT = Path(__file__).resolve().parents[2]

DATA_VERSION = (
    "climatecapital-austin-"
    "2026-01-21-cross-category-v2"
)

RELEASE_ID = (
    "3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1"
)


def _client(
    monkeypatch,
) -> TestClient:
    """Keep the legacy fixture available while the standard API serves governed data."""

    monkeypatch.setenv(
        "CLIMATECAPITAL_BUNDLE_DIR",
        str(
            ROOT
            / "release-data"
            / "fixture"
        ),
    )

    monkeypatch.delenv(
        "MANIFEST_SHA256",
        raising=False,
    )

    return TestClient(app)


def _plan_payload(
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


def test_health_ready_and_schema(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.get(
            "/health"
        )

    assert response.status_code == 200
    assert response.json()["endpoint"] == "/health"

    parsed = (
        HealthSuccessEnvelope
        .model_validate_json(
            response.content,
            strict=True,
        )
    )

    assert (
        parsed.data.status
        == "READY"
    )

    assert (
        parsed.data.gemini_enabled
        is False
    )


def test_standard_bootstrap_serves_106_project_contract(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    assert response.status_code == 200

    parsed = (
        CrossCategoryRuntimeBootstrapEnvelope
        .model_validate_json(
            response.content,
            strict=True,
        )
    )

    assert (
        parsed.endpoint
        == "/api/v1/bootstrap"
    )

    assert (
        parsed.identity.data_version
        == DATA_VERSION
    )

    assert (
        parsed.identity.release_id
        == RELEASE_ID
    )

    assert (
        parsed.data.catalog.project_count
        == 106
    )

    assert (
        len(
            parsed.data.catalog.projects
        )
        == 106
    )

    assert (
        parsed.data.catalog
        .governed_request_total_dollars
        == 1_973_520_000
    )

    assert (
        parsed.data.public_configuration
        .fixture_mode
        is False
    )


def test_bootstrap_preserves_partial_geometry_without_fabrication(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.get(
            "/api/v1/bootstrap"
        )

    parsed = (
        CrossCategoryRuntimeBootstrapEnvelope
        .model_validate_json(
            response.content,
            strict=True,
        )
    )

    map_context = (
        parsed.data.map_context
    )

    assert (
        map_context
        .analytical_project_count
        == 106
    )

    assert (
        map_context.mapped_project_count
        == 74
    )

    assert (
        map_context
        .unmapped_project_count
        == 32
    )

    assert (
        len(map_context.features)
        == 74
    )

    assert (
        map_context.fabricated_geometry
        is False
    )


def test_plan_endpoint_is_deterministic(
    monkeypatch,
):
    body = _plan_payload(
        700_000_000
    )

    with _client(monkeypatch) as client:
        first = client.post(
            "/api/v1/plans/evaluate",
            json=body,
        )

        second = client.post(
            "/api/v1/plans/evaluate",
            json=body,
        )

    assert (
        first.status_code
        == second.status_code
        == 200
    )

    first_parsed = (
        CrossCategoryPlanSuccessEnvelope
        .model_validate_json(
            first.content,
            strict=True,
        )
    )

    second_parsed = (
        CrossCategoryPlanSuccessEnvelope
        .model_validate_json(
            second.content,
            strict=True,
        )
    )

    assert (
        first_parsed.data
        == second_parsed.data
    )

    assert (
        first_parsed.data.status
        == "ANALYST_RESOLUTION_REQUIRED"
    )

    assert (
        first_parsed.data
        .unresolved_boundary
        is not None
    )

    assert (
        first_parsed.data
        .unresolved_boundary
        .funding_priority_score
        == 67
    )


def test_332m_plan_preserves_unique_budget_feasibility_rule(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=_plan_payload(
                332_000_000
            ),
        )

    assert response.status_code == 200

    parsed = (
        CrossCategoryPlanSuccessEnvelope
        .model_validate_json(
            response.content,
            strict=True,
        )
    )

    selected = {
        project.decision_unit_id:
            project
        for project
        in parsed.data.selected_projects
    }

    project = selected[
        "transportation/"
        "act-plan-7th-street"
    ]

    assert (
        project.selection_source
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


def test_plan_data_version_conflict_is_409(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=_plan_payload(
                700_000_000,
                data_version=(
                    "wrong-version"
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
        body["identity"]["data_version"]
        == DATA_VERSION
    )

    assert (
        body["identity"]["release_id"]
        == RELEASE_ID
    )


def test_unknown_request_field_is_422(
    monkeypatch,
):
    body = _plan_payload(
        700_000_000
    )

    body[
        "invented_score"
    ] = 99

    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json=body,
        )

    assert response.status_code == 422

    assert (
        response.json()[
            "error"
        ][
            "error_code"
        ]
        == "UNKNOWN_FIELD"
    )


def test_benchmark_endpoint_is_separate_and_v2_schema_valid(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.get(
            "/api/v1/benchmark"
        )

    assert response.status_code == 200

    parsed = (
        CrossCategoryBenchmarkSuccessEnvelope
        .model_validate_json(
            response.content,
            strict=True,
        )
    )

    benchmark = (
        parsed.data.benchmark
    )

    assert (
        benchmark
        .historically_recommended_project_count
        == 20
    )

    assert (
        benchmark
        .matched_analytical_cohort_dollars
        == 332_000_000
    )

    assert (
        benchmark.ranking_input
        is False
    )

    assert (
        benchmark.portfolio_selection_input
        is False
    )


def test_benchmark_cannot_change_plan_result(
    monkeypatch,
):
    body = _plan_payload(
        700_000_000
    )

    with _client(monkeypatch) as client:
        before = client.post(
            "/api/v1/plans/evaluate",
            json=body,
        ).json()

        benchmark = client.get(
            "/api/v1/benchmark"
        )

        after = client.post(
            "/api/v1/plans/evaluate",
            json=body,
        ).json()

    assert (
        benchmark.status_code
        == 200
    )

    assert (
        before["data"]
        == after["data"]
    )


def test_benchmark_compare_is_explicitly_unavailable(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/benchmark/compare",
            json={},
        )

    assert response.status_code == 503

    assert (
        response.json()[
            "error"
        ][
            "error_code"
        ]
        == (
            "OPTIONAL_DEPENDENCY_UNAVAILABLE"
        )
    )


def test_oversized_declared_body_is_413(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            content=b"{}",
            headers={
                "content-length":
                    str(
                        65 * 1024
                    )
            },
        )

    assert response.status_code == 413

    assert (
        response.json()[
            "error"
        ][
            "error_code"
        ]
        == "BODY_TOO_LARGE"
    )


def test_chunked_oversized_body_is_413(
    monkeypatch,
):
    def chunks():
        yield (
            b"x"
            * (
                65 * 1024
            )
        )

    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            content=chunks(),
            headers={
                "transfer-encoding":
                    "chunked",
                "content-type":
                    "application/json",
            },
        )

    assert response.status_code == 413

    assert (
        response.json()[
            "error"
        ][
            "error_code"
        ]
        == "BODY_TOO_LARGE"
    )


def test_legacy_core_bundle_corruption_still_fails_legacy_loader(
    monkeypatch,
    tmp_path,
):
    """Historical fixture validation remains fail closed outside app startup."""

    bundle = (
        tmp_path
        / "fixture"
    )

    shutil.copytree(
        ROOT
        / "release-data"
        / "fixture",
        bundle,
    )

    catalog_path = (
        bundle
        / "catalog.json"
    )

    catalog_path.write_bytes(
        catalog_path.read_bytes()
        + b"\n"
    )

    monkeypatch.setenv(
        "CLIMATECAPITAL_BUNDLE_DIR",
        str(bundle),
    )

    monkeypatch.delenv(
        "MANIFEST_SHA256",
        raising=False,
    )

    with pytest.raises(
        RuntimeLoadError
    ):
        load_runtime_state()
