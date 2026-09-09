"""Immutable loading for the governed cross-category runtime-v3 bundle."""

from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from climatecapital.contracts.api import (
    DeploymentIdentityData,
    PublicConfiguration,
)
from climatecapital.contracts.common import ReleaseTier

from climatecapital.contracts.cross_category_release import (
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifactV3,
    CrossCategoryReleaseManifestV3,
)
from climatecapital.contracts.cross_category_runtime import (
    CrossCategoryRuntimeCatalog,
)


MAX_RUNTIME_ARTIFACT_BYTES = (
    50 * 1024 * 1024
)


class CrossCategoryRuntimeLoadError(
    RuntimeError
):
    """Reject an invalid cross-category runtime-v3 bundle."""


@dataclass(
    frozen=True,
    slots=True,
)
class CrossCategoryRuntimeState:
    catalog: CrossCategoryRuntimeCatalog
    map_context: CrossCategoryMapContextArtifactV3
    benchmark: CrossCategoryBenchmarkArtifact
    manifest: CrossCategoryReleaseManifestV3

    bundle_directory: Path

    catalog_path: Path
    map_context_path: Path
    benchmark_path: Path
    manifest_path: Path

    manifest_sha256: str
    release_id: str
    deployment_identity: DeploymentIdentityData
    public_configuration: PublicConfiguration


def _repo_root() -> Path:
    return (
        Path(__file__)
        .resolve()
        .parents[3]
    )


def default_bundle_directory() -> Path:
    return (
        _repo_root()
        / "data"
        / "governed"
        / "cross_category"
        / "runtime_v3"
    )


def is_production_environment() -> bool:
    """Use the existing environment label as the production trust boundary."""

    return (
        os.getenv(
            "ENVIRONMENT_LABEL",
            "",
        )
        .strip()
        .lower()
        == "production"
    )


def _sha256(
    payload: bytes,
) -> str:
    return hashlib.sha256(
        payload
    ).hexdigest()


def _read_artifact(
    path: Path,
    model_type: type[Any],
) -> tuple[bytes, Any]:
    if (
        path.is_symlink()
        or not path.is_file()
    ):
        raise CrossCategoryRuntimeLoadError(
            f"{path.name} must be a regular file"
        )

    size = path.stat().st_size

    if (
        size <= 0
        or size
        > MAX_RUNTIME_ARTIFACT_BYTES
    ):
        raise CrossCategoryRuntimeLoadError(
            f"{path.name} has an invalid byte size"
        )

    payload = path.read_bytes()

    if payload.startswith(
        b"\xef\xbb\xbf"
    ):
        raise CrossCategoryRuntimeLoadError(
            f"{path.name} must not contain a UTF-8 BOM"
        )

    try:
        artifact = (
            model_type
            .model_validate_json(
                payload,
                strict=True,
            )
        )

    except (
        ValidationError,
        ValueError,
    ) as error:
        raise (
            CrossCategoryRuntimeLoadError(
                f"{path.name} failed "
                "contract validation"
            )
        ) from error

    return (
        payload,
        artifact,
    )


def _identity_matches(
    payload: bytes,
    *,
    expected_sha256: str,
    expected_size: int,
) -> bool:
    return (
        len(payload)
        == expected_size
        and _sha256(payload)
        == expected_sha256
    )


def load_cross_category_runtime_state(
    bundle_directory: Path | None = None,
) -> CrossCategoryRuntimeState:
    bundle_dir = (
        bundle_directory
        or default_bundle_directory()
    )

    manifest_path = (
        bundle_dir
        / "manifest.json"
    )

    catalog_path = (
        bundle_dir
        / "catalog.json"
    )

    map_context_path = (
        bundle_dir
        / "map-context.geojson"
    )

    benchmark_path = (
        bundle_dir
        / "benchmark.json"
    )

    (
        manifest_bytes,
        manifest,
    ) = _read_artifact(
        manifest_path,
        CrossCategoryReleaseManifestV3,
    )

    (
        catalog_bytes,
        catalog,
    ) = _read_artifact(
        catalog_path,
        CrossCategoryRuntimeCatalog,
    )

    (
        map_bytes,
        map_context,
    ) = _read_artifact(
        map_context_path,
        CrossCategoryMapContextArtifactV3,
    )

    (
        benchmark_bytes,
        benchmark,
    ) = _read_artifact(
        benchmark_path,
        CrossCategoryBenchmarkArtifact,
    )

    # ---------------------------------------------------------------
    # Manifest artifact identity checks
    # ---------------------------------------------------------------

    if not _identity_matches(
        catalog_bytes,
        expected_sha256=(
            manifest
            .artifacts
            .catalog_json
            .sha256
        ),
        expected_size=(
            manifest
            .artifacts
            .catalog_json
            .byte_size
        ),
    ):
        raise CrossCategoryRuntimeLoadError(
            "catalog identity does not match manifest"
        )

    if not _identity_matches(
        map_bytes,
        expected_sha256=(
            manifest
            .artifacts
            .map_context_geojson
            .sha256
        ),
        expected_size=(
            manifest
            .artifacts
            .map_context_geojson
            .byte_size
        ),
    ):
        raise CrossCategoryRuntimeLoadError(
            "map identity does not match manifest"
        )

    if not _identity_matches(
        benchmark_bytes,
        expected_sha256=(
            manifest
            .artifacts
            .benchmark_json
            .sha256
        ),
        expected_size=(
            manifest
            .artifacts
            .benchmark_json
            .byte_size
        ),
    ):
        raise CrossCategoryRuntimeLoadError(
            "benchmark identity does not match manifest"
        )

    # ---------------------------------------------------------------
    # Cross-artifact data identity
    # ---------------------------------------------------------------

    data_versions = {
        manifest.data_version,
        catalog.data_version,
        map_context.data_version,
        benchmark.data_version,
    }

    if len(data_versions) != 1:
        raise CrossCategoryRuntimeLoadError(
            "runtime artifact data versions "
            "are inconsistent"
        )

    if (
        catalog.project_count
        != manifest
        .reconciliations
        .analytical_project_count
    ):
        raise CrossCategoryRuntimeLoadError(
            "catalog project count does not "
            "match manifest reconciliation"
        )

    if (
        catalog
        .governed_request_total_dollars
        != manifest
        .reconciliations
        .governed_request_total_dollars
    ):
        raise CrossCategoryRuntimeLoadError(
            "catalog request total does not "
            "match manifest reconciliation"
        )

    if (
        map_context.mapped_project_count
        != manifest
        .reconciliations
        .mapped_project_count
    ):
        raise CrossCategoryRuntimeLoadError(
            "map coverage does not match manifest"
        )

    if (
        map_context.unmapped_project_count
        != manifest
        .reconciliations
        .unmapped_project_count
    ):
        raise CrossCategoryRuntimeLoadError(
            "map missingness does not match manifest"
        )

    if (
        benchmark
        .matched_analytical_cohort_dollars
        != manifest
        .reconciliations
        .benchmark_matched_cohort_dollars
    ):
        raise CrossCategoryRuntimeLoadError(
            "benchmark dollars do not match manifest"
        )

    if (
        benchmark
        .historically_recommended_project_count
        != manifest
        .reconciliations
        .benchmark_project_count
    ):
        raise CrossCategoryRuntimeLoadError(
            "benchmark project count does not "
            "match manifest"
        )

    # ---------------------------------------------------------------
    # Benchmark identity must equal the analytical cohort.
    # ---------------------------------------------------------------

    catalog_ids = {
        project.decision_unit_id
        for project
        in catalog.projects
    }

    benchmark_ids = {
        outcome.decision_unit_id
        for outcome
        in benchmark.project_outcomes
    }

    if (
        catalog_ids
        != benchmark_ids
    ):
        raise CrossCategoryRuntimeLoadError(
            "benchmark project identities do not "
            "match runtime catalog"
        )

    # ---------------------------------------------------------------
    # Governed map identities and metadata must equal the analytical cohort.
    # ---------------------------------------------------------------

    if len(map_context.features) != map_context.mapped_project_count:
        raise CrossCategoryRuntimeLoadError(
            "map feature count does not match governed coverage"
        )

    map_by_id = {
        feature.properties.decision_unit_id: feature
        for feature in map_context.features
    }
    if not set(map_by_id) <= catalog_ids:
        raise CrossCategoryRuntimeLoadError(
            "map contains identities outside the runtime catalog"
        )

    catalog_by_id = {
        project.decision_unit_id: project
        for project in catalog.projects
    }
    for decision_unit_id, feature in map_by_id.items():
        project = catalog_by_id[decision_unit_id]
        if (
            feature.properties.governed_name != project.governed_name
            or feature.properties.presentation_category
            != str(project.presentation_category)
        ):
            raise CrossCategoryRuntimeLoadError(
                f"map metadata does not match catalog for {decision_unit_id}"
            )

    if (
        map_context.governance_reconciliation_sha256
        != manifest.reconciliations.geometry_governance_sha256
        or map_context.candidate_geometry_snapshot_sha256
        != manifest.reconciliations.candidate_geometry_snapshot_sha256
        or map_context.governance_decision_id
        != manifest.reconciliations.geometry_governance_decision_id
    ):
        raise CrossCategoryRuntimeLoadError(
            "map governance identity does not match manifest"
        )

    manifest_sha256 = (
        _sha256(
            manifest_bytes
        )
    )

    production = is_production_environment()
    identity_names = (
        "CODE_GIT_SHA",
        "DATA_VERSION",
        "MANIFEST_SHA256",
        "CONTAINER_IMAGE_DIGEST",
        "RELEASE_ID",
    )
    if production:
        missing = [
            name
            for name in identity_names
            if not os.getenv(name)
        ]
        if missing:
            raise CrossCategoryRuntimeLoadError(
                "production deployment identity is incomplete: "
                + ", ".join(missing)
            )

    configured_data_version = os.getenv(
        "DATA_VERSION",
        manifest.data_version,
    )
    if configured_data_version != manifest.data_version:
        raise CrossCategoryRuntimeLoadError(
            "DATA_VERSION does not match the governed runtime"
        )

    configured_manifest_sha256 = os.getenv(
        "MANIFEST_SHA256",
        manifest_sha256,
    )
    if configured_manifest_sha256 != manifest_sha256:
        raise CrossCategoryRuntimeLoadError(
            "MANIFEST_SHA256 does not match the governed runtime"
        )

    configured_release_id = os.getenv(
        "RELEASE_ID",
        manifest.release_id,
    )
    if configured_release_id != manifest.release_id:
        raise CrossCategoryRuntimeLoadError(
            "RELEASE_ID does not match the governed runtime"
        )

    try:
        deployment_identity = DeploymentIdentityData(
            code_git_sha=os.getenv(
                "CODE_GIT_SHA",
                "0" * 40,
            ),
            manifest_sha256=configured_manifest_sha256,
            container_image_digest=os.getenv(
                "CONTAINER_IMAGE_DIGEST",
                "sha256:" + ("0" * 64),
            ),
            release_tier=ReleaseTier.REVIEWED_RELEASE,
        )
    except ValidationError as error:
        raise CrossCategoryRuntimeLoadError(
            "deployment identity has an invalid shape"
        ) from error

    public_configuration = PublicConfiguration(
        environment_label=os.getenv(
            "ENVIRONMENT_LABEL",
            "local-cross-category-v3",
        ),
        osm_tile_url=os.getenv(
            "OSM_TILE_URL",
            "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
        ),
        osm_attribution=os.getenv(
            "OSM_ATTRIBUTION",
            "© OpenStreetMap contributors",
        ),
        fixture_mode=False,
    )

    return CrossCategoryRuntimeState(
        catalog=catalog,
        map_context=map_context,
        benchmark=benchmark,
        manifest=manifest,
        bundle_directory=bundle_dir,
        catalog_path=catalog_path,
        map_context_path=map_context_path,
        benchmark_path=benchmark_path,
        manifest_path=manifest_path,
        manifest_sha256=manifest_sha256,
        release_id=manifest.release_id,
        deployment_identity=deployment_identity,
        public_configuration=public_configuration,
    )
