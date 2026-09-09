"""Focused F7A.1 coverage for the production deployment boundary."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from starlette.routing import Mount

from climatecapital.api.cross_category_runtime import (
    CrossCategoryRuntimeLoadError,
    load_cross_category_runtime_state,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.main import create_app


ROOT = Path(__file__).resolve().parents[2]
RUNTIME_DIRECTORY = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v3"
)
MANIFEST_BYTES = (RUNTIME_DIRECTORY / "manifest.json").read_bytes()
MANIFEST = json.loads(MANIFEST_BYTES)
DATA_VERSION = MANIFEST["data_version"]
RELEASE_ID = MANIFEST["release_id"]
MANIFEST_SHA256 = hashlib.sha256(MANIFEST_BYTES).hexdigest()
CODE_GIT_SHA = "a" * 40
CONTAINER_IMAGE_DIGEST = "sha256:" + ("b" * 64)


def _set_production_identity(monkeypatch) -> None:
    values = {
        "ENVIRONMENT_LABEL": "production",
        "CODE_GIT_SHA": CODE_GIT_SHA,
        "DATA_VERSION": DATA_VERSION,
        "MANIFEST_SHA256": MANIFEST_SHA256,
        "CONTAINER_IMAGE_DIGEST": CONTAINER_IMAGE_DIGEST,
        "RELEASE_ID": RELEASE_ID,
        "GEMINI_ENABLED": "false",
    }
    for name, value in values.items():
        monkeypatch.setenv(name, value)


def _static_bundle(tmp_path: Path) -> Path:
    directory = tmp_path / "dist"
    assets = directory / "assets"
    assets.mkdir(parents=True)
    (directory / "index.html").write_text(
        "<!doctype html><html><head>"
        '<meta name="robots" content="noindex,nofollow,noarchive">'
        "</head><body>F7A1-SPA"
        '<script type="module" src="/assets/app.js"></script>'
        "</body></html>",
        encoding="utf-8",
    )
    (assets / "app.js").write_text("window.f7a1 = true;", encoding="utf-8")
    (directory / "favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
        encoding="utf-8",
    )
    (directory / "icons.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg"></svg>',
        encoding="utf-8",
    )
    (directory / "robots.txt").write_text(
        "User-agent: *\nDisallow: /\n",
        encoding="utf-8",
    )
    return directory


def test_production_serves_spa_assets_and_keeps_api_routes_owned(
    monkeypatch,
    tmp_path,
):
    _set_production_identity(monkeypatch)
    application = create_app(static_directory=_static_bundle(tmp_path))

    with TestClient(application) as client:
        root = client.get("/")
        asset = client.get("/assets/app.js")
        favicon = client.get("/favicon.svg")
        robots = client.get("/robots.txt")
        health = client.get("/healthz")
        bootstrap = client.get("/api/v1/bootstrap")
        unknown_api = client.get("/api/v1/not-a-route")

    assert root.status_code == 200
    assert "F7A1-SPA" in root.text
    assert asset.status_code == 200
    assert "window.f7a1" in asset.text
    assert favicon.status_code == 200
    assert robots.status_code == 200
    assert robots.text == "User-agent: *\nDisallow: /\n"
    assert health.status_code == 200
    assert bootstrap.status_code == 200
    assert unknown_api.status_code == 404
    assert unknown_api.headers["content-type"].startswith("application/json")
    assert unknown_api.json() == {"detail": "Not Found"}
    assert "F7A1-SPA" not in unknown_api.text
    static_mounts = [
        route.path
        for route in application.routes
        if isinstance(route, Mount)
    ]
    assert static_mounts == ["/assets"]


def test_production_health_uses_validated_runtime_v3_identity(monkeypatch, tmp_path):
    _set_production_identity(monkeypatch)
    monkeypatch.setenv(
        "CLIMATECAPITAL_BUNDLE_DIR",
        str(ROOT / "release-data" / "fixture"),
    )
    application = create_app(static_directory=_static_bundle(tmp_path))

    with TestClient(application) as client:
        health = client.get("/healthz").json()
        bootstrap = client.get("/api/v1/bootstrap").json()
        runtime = application.state.cross_category_runtime

    assert not hasattr(application.state, "runtime")
    assert runtime.bundle_directory == RUNTIME_DIRECTORY
    assert runtime.public_configuration.fixture_mode is False
    assert health["identity"]["data_version"] == DATA_VERSION
    assert health["identity"]["release_id"] == RELEASE_ID
    assert health["data"]["deployment_identity"] == {
        "code_git_sha": CODE_GIT_SHA,
        "manifest_sha256": MANIFEST_SHA256,
        "container_image_digest": CONTAINER_IMAGE_DIGEST,
        "release_tier": "REVIEWED_RELEASE",
    }
    assert health["identity"]["data_version"] == bootstrap["identity"]["data_version"]
    assert health["identity"]["release_id"] == bootstrap["identity"]["release_id"]
    assert bootstrap["data"]["catalog"]["project_count"] == 106
    assert bootstrap["data"]["map_context"]["mapped_project_count"] == 74
    assert bootstrap["data"]["public_configuration"]["fixture_mode"] is False
    assert health["data"]["contract_versions"] == MANIFEST["contract_versions"]


@pytest.mark.parametrize(
    ("name", "bad_value", "message"),
    [
        ("DATA_VERSION", "wrong-data", "DATA_VERSION"),
        ("MANIFEST_SHA256", "c" * 64, "MANIFEST_SHA256"),
        ("RELEASE_ID", "d" * 64, "RELEASE_ID"),
    ],
)
def test_production_rejects_runtime_identity_mismatch(
    monkeypatch,
    name,
    bad_value,
    message,
):
    _set_production_identity(monkeypatch)
    monkeypatch.setenv(name, bad_value)

    with pytest.raises(CrossCategoryRuntimeLoadError, match=message):
        load_cross_category_runtime_state()


@pytest.mark.parametrize(
    ("name", "bad_value"),
    [
        ("CODE_GIT_SHA", "ABC123"),
        ("CODE_GIT_SHA", "A" * 40),
        ("CONTAINER_IMAGE_DIGEST", "b" * 64),
        ("CONTAINER_IMAGE_DIGEST", "sha256:" + ("B" * 64)),
    ],
)
def test_production_rejects_malformed_git_sha_or_image_digest(
    monkeypatch,
    name,
    bad_value,
):
    _set_production_identity(monkeypatch)
    monkeypatch.setenv(name, bad_value)

    with pytest.raises(
        CrossCategoryRuntimeLoadError,
        match="invalid shape",
    ):
        load_cross_category_runtime_state()


def test_production_requires_every_external_identity_value(monkeypatch):
    _set_production_identity(monkeypatch)
    monkeypatch.delenv("CONTAINER_IMAGE_DIGEST")

    with pytest.raises(
        CrossCategoryRuntimeLoadError,
        match="CONTAINER_IMAGE_DIGEST",
    ):
        load_cross_category_runtime_state()


def test_production_security_crawler_and_docs_boundary(monkeypatch, tmp_path):
    _set_production_identity(monkeypatch)
    application = create_app(static_directory=_static_bundle(tmp_path))

    with TestClient(application) as client:
        root = client.get("/")
        health = client.get("/healthz")
        docs = client.get("/docs")
        redoc = client.get("/redoc")
        openapi = client.get("/openapi.json")

    for response in (root, health, docs, redoc, openapi):
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["x-frame-options"] == "DENY"
        assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
        assert response.headers["strict-transport-security"] == "max-age=31536000"
        assert response.headers["x-robots-tag"] == "noindex, nofollow, noarchive"
        csp = response.headers["content-security-policy"]
        assert "default-src 'self'" in csp
        assert "script-src 'self'" in csp
        assert "connect-src 'self'" in csp
        assert "https://tile.openstreetmap.org" in csp
        assert "frame-ancestors 'none'" in csp
        assert "*" not in csp

    assert docs.status_code == redoc.status_code == openapi.status_code == 404
    assert "F7A1-SPA" not in docs.text
    assert "Traceback" not in docs.text


def test_development_without_dist_keeps_api_and_docs_available(monkeypatch, tmp_path):
    monkeypatch.setenv("ENVIRONMENT_LABEL", "development")
    for name in (
        "CODE_GIT_SHA",
        "DATA_VERSION",
        "MANIFEST_SHA256",
        "CONTAINER_IMAGE_DIGEST",
        "RELEASE_ID",
    ):
        monkeypatch.delenv(name, raising=False)
    application = create_app(static_directory=tmp_path / "not-built")

    with TestClient(application) as client:
        root = client.get("/")
        health = client.get("/healthz")
        docs = client.get("/docs")

    assert root.status_code == 503
    assert "Vite development server" in root.text
    assert health.status_code == 200
    assert docs.status_code == 200
    assert "strict-transport-security" not in health.headers


def test_production_startup_fails_if_compiled_frontend_is_absent(
    monkeypatch,
    tmp_path,
):
    _set_production_identity(monkeypatch)
    application = create_app(static_directory=tmp_path / "not-built")

    with pytest.raises(RuntimeError, match="compiled frontend/dist"):
        with TestClient(application):
            pass


def test_frontend_sources_contain_crawler_protections():
    index = (ROOT / "frontend" / "index.html").read_text(encoding="utf-8")
    robots = (ROOT / "frontend" / "public" / "robots.txt").read_text(
        encoding="utf-8"
    )

    assert '<meta name="robots" content="noindex,nofollow,noarchive"' in index
    assert robots == "User-agent: *\nDisallow: /\n"


def test_container_boundary_is_pinned_non_root_and_runtime_v3_only():
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")

    assert "FROM node:22.23.2-bookworm-slim" in dockerfile
    assert "npm@11.19.1" in dockerfile
    assert "RUN npm ci" in dockerfile
    assert "RUN npm run build" in dockerfile
    assert "FROM python:3.14.7-slim-bookworm" in dockerfile
    assert "requirements-application.txt" in dockerfile
    assert "data/governed/cross_category/runtime_v3" in dockerfile
    assert "release-data/fixture" not in dockerfile
    assert "data/staging" not in dockerfile
    assert "data/reconnaissance" not in dockerfile
    assert "USER 10001:10001" in dockerfile
    assert "--host 0.0.0.0" in dockerfile
    assert '--port \\"${PORT:-8080}\\" --workers 1' in dockerfile
    assert dockerignore.startswith("**\n")
    assert "!data/governed/cross_category/runtime_v3/**" in dockerignore
    assert "**/__pycache__/" in dockerignore
    assert "**/*.py[cod]" in dockerignore
    for forbidden in (
        ".node-version",
        ".git",
        ".venv",
        "node_modules",
        "release-data",
        "data/staging",
        "data/reconnaissance",
    ):
        assert f"!{forbidden}" not in dockerignore


def test_representative_funding_plan_remains_available_in_production(
    monkeypatch,
    tmp_path,
):
    _set_production_identity(monkeypatch)
    application = create_app(static_directory=_static_bundle(tmp_path))
    payload = {
        "contract_version": CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "available_budget_dollars": 332_000_000,
        "boundary_resolutions": [],
        "expected_fingerprint": None,
    }

    with TestClient(application) as client:
        response = client.post("/api/v1/plans/evaluate", json=payload)

    assert response.status_code == 200
    result = response.json()["data"]
    assert result["status"] == "COMPLETE"
    assert len(result["selected_projects"]) == 18
    assert result["included_total_dollars"] == 331_825_000
    assert result["remainder_dollars"] == 175_000
