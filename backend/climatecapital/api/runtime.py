"""Immutable local/runtime loading for the M3 API surface."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from climatecapital.contracts.api import (
    BootstrapMapDefaults,
    DeploymentIdentityData,
    PublicConfiguration,
)
from climatecapital.contracts.artifacts import (
    BenchmarkArtifact,
    CatalogArtifact,
    MapContextArtifact,
    ReleaseManifest,
)
from climatecapital.contracts.common import ReleaseTier

MAX_ARTIFACT_BYTES = 50 * 1024 * 1024


class RuntimeLoadError(RuntimeError):
    """Safe startup rejection with no source bytes or secret material."""


class BenchmarkUnavailableError(RuntimeError):
    """Local benchmark failure; core runtime remains usable."""


@dataclass(frozen=True, slots=True)
class RuntimeState:
    manifest: ReleaseManifest
    catalog: CatalogArtifact
    map_context: MapContextArtifact
    benchmark: BenchmarkArtifact | None
    benchmark_error: str | None
    manifest_sha256: str
    deployment_identity: DeploymentIdentityData
    map_defaults: BootstrapMapDefaults
    public_configuration: PublicConfiguration
    gemini_enabled: bool
    release_id: str


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _read_json(path: Path, model_type: type[Any]) -> tuple[bytes, Any]:
    if path.is_symlink() or not path.is_file():
        raise RuntimeLoadError(f"{path.name} must be a regular file")
    size = path.stat().st_size
    if size <= 0 or size > MAX_ARTIFACT_BYTES:
        raise RuntimeLoadError(f"{path.name} has an invalid byte size")
    payload = path.read_bytes()
    if payload.startswith(b"\xef\xbb\xbf"):
        raise RuntimeLoadError(f"{path.name} must not contain a UTF-8 BOM")
    try:
        model = model_type.model_validate_json(payload, strict=True)
    except (ValidationError, ValueError) as error:
        raise RuntimeLoadError(f"{path.name} failed schema validation") from error
    return payload, model


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _artifact_identity_matches(
    payload: bytes,
    *,
    expected_sha256: str,
    expected_size: int,
) -> bool:
    return len(payload) == expected_size and _sha256(payload) == expected_sha256


def _load_core(bundle_dir: Path) -> tuple[
    ReleaseManifest,
    CatalogArtifact,
    MapContextArtifact,
    str,
]:
    manifest_bytes, manifest = _read_json(
        bundle_dir / "manifest.json", ReleaseManifest
    )
    catalog_bytes, catalog = _read_json(
        bundle_dir / "catalog.json", CatalogArtifact
    )
    map_bytes, map_context = _read_json(
        bundle_dir / "map-context.geojson", MapContextArtifact
    )

    manifest_sha = _sha256(manifest_bytes)
    expected_external = os.getenv("MANIFEST_SHA256")
    if expected_external and expected_external != manifest_sha:
        raise RuntimeLoadError("manifest checksum does not match runtime identity")

    if not _artifact_identity_matches(
        catalog_bytes,
        expected_sha256=manifest.artifacts.catalog_json.sha256,
        expected_size=manifest.artifacts.catalog_json.byte_size,
    ):
        raise RuntimeLoadError("catalog identity does not match manifest")
    if not _artifact_identity_matches(
        map_bytes,
        expected_sha256=manifest.artifacts.map_context_geojson.sha256,
        expected_size=manifest.artifacts.map_context_geojson.byte_size,
    ):
        raise RuntimeLoadError("map identity does not match manifest")

    if (
        catalog.data_version != manifest.data_version
        or map_context.data_version != manifest.data_version
        or catalog.release_tier != manifest.release_tier
        or map_context.release_tier != manifest.release_tier
    ):
        raise RuntimeLoadError("core artifact identity is inconsistent")

    available_geometry = {
        project.project_id
        for project in catalog.projects
        if project.geography_status == "DISPLAY_GEOMETRY_AVAILABLE"
    }
    map_projects = {
        feature.properties.project_id
        for feature in map_context.features
        if feature.properties.layer_id == "rna_current_project_display"
    }
    if map_projects != available_geometry:
        raise RuntimeLoadError("catalog/map RNA geometry coverage is inconsistent")

    return manifest, catalog, map_context, manifest_sha


def _load_benchmark(
    bundle_dir: Path,
    manifest: ReleaseManifest,
) -> tuple[BenchmarkArtifact | None, str | None]:
    try:
        benchmark_bytes, benchmark = _read_json(
            bundle_dir / "benchmark.json", BenchmarkArtifact
        )
        expected = manifest.artifacts.benchmark_json
        if not _artifact_identity_matches(
            benchmark_bytes,
            expected_sha256=expected.sha256,
            expected_size=expected.byte_size,
        ):
            raise BenchmarkUnavailableError(
                "benchmark identity does not match manifest"
            )
        if (
            benchmark.data_version != manifest.data_version
            or benchmark.release_tier != manifest.release_tier
            or (
                benchmark.benchmark_identity.source_id
                != manifest.benchmark_identity.source_id
            )
        ):
            raise BenchmarkUnavailableError(
                "benchmark runtime identity is inconsistent"
            )
        return benchmark, None
    except (RuntimeLoadError, BenchmarkUnavailableError) as error:
        return None, str(error)


def _identity_value(name: str, fixture_default: str) -> str:
    value = os.getenv(name)
    if value:
        return value
    return fixture_default


def load_runtime_state(
    bundle_directory: Path | None = None,
) -> RuntimeState:
    """Load the immutable bundle once without contacting any external service."""

    bundle_dir = bundle_directory or Path(
        os.getenv(
            "CLIMATECAPITAL_BUNDLE_DIR",
            str(_repo_root() / "release-data" / "fixture"),
        )
    )

    manifest, catalog, map_context, manifest_sha = _load_core(bundle_dir)

    if (
        manifest.release_tier == ReleaseTier.REVIEWED_RELEASE
        and not os.getenv("MANIFEST_SHA256")
    ):
        raise RuntimeLoadError(
            "reviewed runtime requires external MANIFEST_SHA256"
        )

    benchmark, benchmark_error = _load_benchmark(bundle_dir, manifest)
    fixture = manifest.release_tier == ReleaseTier.FIXTURE

    deployment = DeploymentIdentityData(
        code_git_sha=_identity_value("CODE_GIT_SHA", "0" * 40),
        manifest_sha256=manifest_sha,
        container_image_digest=_identity_value(
            "CONTAINER_IMAGE_DIGEST", "sha256:" + ("0" * 64)
        ),
        release_tier=ReleaseTier(manifest.release_tier),
    )

    configuration = PublicConfiguration(
        environment_label=os.getenv(
            "ENVIRONMENT_LABEL",
            "local-fixture" if fixture else "release",
        ),
        osm_tile_url=os.getenv(
            "OSM_TILE_URL",
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        ),
        osm_attribution=os.getenv(
            "OSM_ATTRIBUTION",
            "© OpenStreetMap contributors",
        ),
        fixture_mode=fixture,
    )

    return RuntimeState(
        manifest=manifest,
        catalog=catalog,
        map_context=map_context,
        benchmark=benchmark,
        benchmark_error=benchmark_error,
        manifest_sha256=manifest_sha,
        deployment_identity=deployment,
        map_defaults=BootstrapMapDefaults(
            rna_current_project_display=True,
            fema_current_hazard_context=False,
            eaz_2021_context=False,
        ),
        public_configuration=configuration,
        gemini_enabled=False,
        release_id=os.getenv(
            "RELEASE_ID",
            f"{manifest.data_version}-fixture"
            if fixture
            else manifest.data_version,
        ),
    )
