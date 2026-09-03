"""Persistent M3 integration coverage over the approved fixture bundle."""

from __future__ import annotations

import shutil

import pytest
from pathlib import Path

from fastapi.testclient import TestClient

from climatecapital.contracts.api import (
    BenchmarkComparisonSuccessEnvelope,
    BenchmarkSuccessEnvelope,
    BootstrapSuccessEnvelope,
    HealthSuccessEnvelope,
    PlanEvaluationSuccessEnvelope,
)
from climatecapital.contracts.versions import (
    BENCHMARK_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.api.runtime import RuntimeLoadError
from climatecapital.main import app

ROOT = Path(__file__).resolve().parents[2]


def _client(monkeypatch) -> TestClient:
    monkeypatch.setenv(
        "CLIMATECAPITAL_BUNDLE_DIR",
        str(ROOT / "release-data" / "fixture"),
    )
    monkeypatch.delenv("MANIFEST_SHA256", raising=False)
    return TestClient(app)


def test_health_ready_and_schema(monkeypatch):
    with _client(monkeypatch) as client:
        response = client.get("/healthz")
    assert response.status_code == 200
    parsed = HealthSuccessEnvelope.model_validate_json(response.content, strict=True)
    assert parsed.data.status == "READY"
    assert parsed.data.gemini_enabled is False
    assert parsed.data.deployment_identity.release_tier == "FIXTURE"


def test_bootstrap_exact_fixture_contract_and_all_37(monkeypatch):
    with _client(monkeypatch) as client:
        response = client.get("/api/v1/bootstrap")
    assert response.status_code == 200
    parsed = BootstrapSuccessEnvelope.model_validate_json(
        response.content, strict=True
    )
    assert len(parsed.data.catalog.projects) == 37
    assert parsed.data.catalog.governed_universe_summary.project_count == 37
    assert parsed.data.catalog.active_family_summary.project_count == 12
    assert parsed.data.public_configuration.fixture_mode is True


def test_bootstrap_retains_missing_geometry_and_citywide(monkeypatch):
    with _client(monkeypatch) as client:
        payload = client.get("/api/v1/bootstrap").content
    parsed = BootstrapSuccessEnvelope.model_validate_json(payload, strict=True)
    projects = {p.project_id: p for p in parsed.data.catalog.projects}
    assert any(
        p.geography_status == "DISPLAY_GEOMETRY_MISSING"
        for p in projects.values()
    )
    citywide = projects["5789.150"]
    assert citywide.program_scope == "CITYWIDE_PROGRAM"
    assert citywide.geography_status == "NON_PROJECT_GEOGRAPHY"
    map_ids = {
        feature.properties.project_id
        for feature in parsed.data.map_context.features
        if feature.properties.project_id is not None
    }
    assert "5789.150" not in map_ids


def test_plan_endpoint_is_deterministic(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = BootstrapSuccessEnvelope.model_validate_json(
            client.get("/api/v1/bootstrap").content, strict=True
        )
        data_version = bootstrap.data.catalog.data_version
        ids = bootstrap.data.catalog.active_family_summary.project_ids[:2]
        body = {
            "current": {
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": data_version,
                "available_budget_dollars": 125_000_000,
                "project_ids": ids,
                "expected_fingerprint": None,
            },
            "reference": None,
        }
        first = client.post("/api/v1/plans/evaluate", json=body)
        second = client.post("/api/v1/plans/evaluate", json=body)
    assert first.status_code == second.status_code == 200
    p1 = PlanEvaluationSuccessEnvelope.model_validate_json(
        first.content, strict=True
    )
    p2 = PlanEvaluationSuccessEnvelope.model_validate_json(
        second.content, strict=True
    )
    assert p1.data == p2.data


def test_plan_membership_partitions_active_family_and_totals_reconcile(
    monkeypatch,
):
    with _client(monkeypatch) as client:
        bootstrap = BootstrapSuccessEnvelope.model_validate_json(
            client.get("/api/v1/bootstrap").content, strict=True
        )
        family = bootstrap.data.catalog.active_family_summary.project_ids
        body = {
            "current": {
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": bootstrap.data.catalog.data_version,
                "available_budget_dollars": 125_000_000,
                "project_ids": family[:3],
                "expected_fingerprint": None,
            },
            "reference": None,
        }
        response = client.post("/api/v1/plans/evaluate", json=body)
    parsed = PlanEvaluationSuccessEnvelope.model_validate_json(
        response.content, strict=True
    )
    evaluated = parsed.data.current.evaluated_plan
    assert evaluated is not None
    assert (
        set(evaluated.included_project_ids)
        | set(evaluated.not_included_active_family_project_ids)
    ) == set(family)
    assert evaluated.included_total_dollars == sum(
        row.governed_request_dollars
        for row in evaluated.included_governed_requests
    )


def test_plan_data_version_conflict_is_409(monkeypatch):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            json={
                "current": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": "wrong-version",
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": None,
                },
                "reference": None,
            },
        )
    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "DATA_VERSION_CONFLICT"


def test_unknown_request_field_is_422(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = client.get("/api/v1/bootstrap").json()
        data_version = bootstrap["data"]["catalog"]["data_version"]
        response = client.post(
            "/api/v1/plans/evaluate",
            json={
                "current": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": None,
                    "invented_score": 99,
                },
                "reference": None,
            },
        )
    assert response.status_code == 422
    assert response.json()["error"]["error_code"] == "UNKNOWN_FIELD"


def test_benchmark_endpoint_is_separate_and_schema_valid(monkeypatch):
    with _client(monkeypatch) as client:
        response = client.get("/api/v1/benchmark")
    assert response.status_code == 200
    parsed = BenchmarkSuccessEnvelope.model_validate_json(
        response.content, strict=True
    )
    assert parsed.data.benchmark.benchmark_identity.source_id



def test_benchmark_failure_is_local(monkeypatch, tmp_path):
    bundle = tmp_path / "fixture"
    shutil.copytree(ROOT / "release-data" / "fixture", bundle)
    (bundle / "benchmark.json").write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv("CLIMATECAPITAL_BUNDLE_DIR", str(bundle))
    monkeypatch.delenv("MANIFEST_SHA256", raising=False)
    with TestClient(app) as client:
        assert client.get("/healthz").status_code == 200
        assert client.get("/api/v1/bootstrap").status_code == 200
        assert client.get("/api/v1/benchmark").status_code == 503

def test_benchmark_cannot_change_plan_result(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = BootstrapSuccessEnvelope.model_validate_json(
            client.get("/api/v1/bootstrap").content, strict=True
        )
        family = bootstrap.data.catalog.active_family_summary.project_ids[:2]
        body = {
            "current": {
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": bootstrap.data.catalog.data_version,
                "available_budget_dollars": 125_000_000,
                "project_ids": family,
                "expected_fingerprint": None,
            },
            "reference": None,
        }
        before = client.post("/api/v1/plans/evaluate", json=body).json()
        _ = client.get("/api/v1/benchmark")
        after = client.post("/api/v1/plans/evaluate", json=body).json()
    assert before["data"] == after["data"]


def test_oversized_declared_body_is_413(monkeypatch):
    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            content=b"{}",
            headers={"content-length": str(65 * 1024)},
        )
    assert response.status_code == 413
    assert response.json()["error"]["error_code"] == "BODY_TOO_LARGE"


def test_core_bundle_corruption_fails_startup(monkeypatch, tmp_path):
    bundle = tmp_path / "fixture"
    shutil.copytree(ROOT / "release-data" / "fixture", bundle)

    catalog_path = bundle / "catalog.json"
    catalog_path.write_bytes(catalog_path.read_bytes() + b"\n")

    monkeypatch.setenv("CLIMATECAPITAL_BUNDLE_DIR", str(bundle))
    monkeypatch.delenv("MANIFEST_SHA256", raising=False)

    with pytest.raises(RuntimeLoadError):
        with TestClient(app):
            pass


def test_invalid_reference_preserves_valid_current(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = BootstrapSuccessEnvelope.model_validate_json(
            client.get("/api/v1/bootstrap").content,
            strict=True,
        )
        data_version = bootstrap.data.catalog.data_version

        response = client.post(
            "/api/v1/plans/evaluate",
            json={
                "current": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": None,
                },
                "reference": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": ["99999.999"],
                    "expected_fingerprint": None,
                },
            },
        )

    assert response.status_code == 200
    parsed = PlanEvaluationSuccessEnvelope.model_validate_json(
        response.content,
        strict=True,
    )
    assert parsed.data.current.status == "VALID"
    assert parsed.data.reference is not None
    assert parsed.data.reference.status == "INVALID"
    assert parsed.data.comparison is None


def test_benchmark_compare_freshly_evaluates_plan(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = BootstrapSuccessEnvelope.model_validate_json(
            client.get("/api/v1/bootstrap").content,
            strict=True,
        )
        data_version = bootstrap.data.catalog.data_version
        chosen_ids = bootstrap.data.catalog.active_family_summary.project_ids[:2]

        expected_total = sum(
            project.governed_request_dollars
            for project in bootstrap.data.catalog.projects
            if project.project_id in chosen_ids
        )

        response = client.post(
            "/api/v1/benchmark/compare",
            json={
                "plan": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": chosen_ids,
                    "expected_fingerprint": None,
                },
                "expected_benchmark_contract_version": BENCHMARK_CONTRACT_VERSION,
                "expected_benchmark_data_version": data_version,
            },
        )

    assert response.status_code == 200
    parsed = BenchmarkComparisonSuccessEnvelope.model_validate_json(
        response.content,
        strict=True,
    )
    assert parsed.data.evaluated_plan.included_project_ids == sorted(chosen_ids)
    assert parsed.data.evaluated_plan.included_total_dollars == expected_total
    assert parsed.data.benchmark_data_version == data_version


def test_benchmark_contract_version_conflict_is_409(monkeypatch):
    with _client(monkeypatch) as client:
        bootstrap = client.get("/api/v1/bootstrap").json()
        data_version = bootstrap["data"]["catalog"]["data_version"]

        response = client.post(
            "/api/v1/benchmark/compare",
            json={
                "plan": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": None,
                },
                "expected_benchmark_contract_version": "p0-benchmark/999.0.0",
                "expected_benchmark_data_version": data_version,
            },
        )

    assert response.status_code == 409
    assert response.json()["error"]["error_code"] == "CONTRACT_VERSION_CONFLICT"


def test_chunked_oversized_body_is_413(monkeypatch):
    def chunks():
        yield b"x" * (65 * 1024)

    with _client(monkeypatch) as client:
        response = client.post(
            "/api/v1/plans/evaluate",
            content=chunks(),
            headers={
                "transfer-encoding": "chunked",
                "content-type": "application/json",
            },
        )

    assert response.status_code == 413
    assert response.json()["error"]["error_code"] == "BODY_TOO_LARGE"


def test_benchmark_failure_does_not_disable_plan_api(monkeypatch, tmp_path):
    bundle = tmp_path / "fixture"
    shutil.copytree(ROOT / "release-data" / "fixture", bundle)
    (bundle / "benchmark.json").write_text("{}\n", encoding="utf-8")

    monkeypatch.setenv("CLIMATECAPITAL_BUNDLE_DIR", str(bundle))
    monkeypatch.delenv("MANIFEST_SHA256", raising=False)

    with TestClient(app) as client:
        bootstrap = client.get("/api/v1/bootstrap")
        assert bootstrap.status_code == 200
        data_version = bootstrap.json()["data"]["catalog"]["data_version"]

        plan = client.post(
            "/api/v1/plans/evaluate",
            json={
                "current": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": None,
                },
                "reference": None,
            },
        )

        assert plan.status_code == 200
        assert client.get("/api/v1/benchmark").status_code == 503
