"""Build the immutable runtime-v3 bundle with governed project map evidence."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.cross_category_geometry import (
    CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION,
    CrossCategoryGeometryGovernanceArtifact,
)
from climatecapital.contracts.cross_category_release import (
    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
    CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS,
    CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT,
    CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION_V3,
    CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION_V3,
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifactV3,
    CrossCategoryReleaseManifest,
    CrossCategoryReleaseManifestV3,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
    CrossCategoryRuntimeCatalog,
)


DATA_VERSION = "climatecapital-austin-2026-01-21-cross-category-v2"
SOURCE_RUNTIME_DIR = ROOT / "data/governed/cross_category/runtime_v2"
RUNTIME_DIR = ROOT / "data/governed/cross_category/runtime_v3"
SOURCE_CATALOG_PATH = SOURCE_RUNTIME_DIR / "catalog.json"
SOURCE_BENCHMARK_PATH = SOURCE_RUNTIME_DIR / "benchmark.json"
SOURCE_MANIFEST_PATH = SOURCE_RUNTIME_DIR / "manifest.json"
CATALOG_PATH = RUNTIME_DIR / "catalog.json"
MAP_PATH = RUNTIME_DIR / "map-context.geojson"
BENCHMARK_PATH = RUNTIME_DIR / "benchmark.json"
MANIFEST_PATH = RUNTIME_DIR / "manifest.json"
GOVERNANCE_PATH = (
    ROOT
    / "data/governed/cross_category/reconciliation/project-geometry-governance.json"
)
CANDIDATE_GEOMETRY_PATH = (
    ROOT
    / "data/reconnaissance/external_gis/2026-09-08/"
    / "CANDIDATE_NOT_GOVERNED_source_geometries.geojson"
)


class RuntimeBundleBuildError(RuntimeError):
    """Raised when governed geometry inputs fail reconciliation."""


class DerivedArtifactConflictError(RuntimeBundleBuildError):
    """Raised when an immutable target artifact already differs."""


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def artifact_identity(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {"sha256": sha256_bytes(payload), "byte_size": len(payload)}


def load_source_artifacts() -> tuple[
    CrossCategoryRuntimeCatalog,
    CrossCategoryBenchmarkArtifact,
    CrossCategoryReleaseManifest,
]:
    catalog = CrossCategoryRuntimeCatalog.model_validate_json(
        SOURCE_CATALOG_PATH.read_bytes(), strict=True
    )
    benchmark = CrossCategoryBenchmarkArtifact.model_validate_json(
        SOURCE_BENCHMARK_PATH.read_bytes(), strict=True
    )
    manifest = CrossCategoryReleaseManifest.model_validate_json(
        SOURCE_MANIFEST_PATH.read_bytes(), strict=True
    )
    if {catalog.data_version, benchmark.data_version, manifest.data_version} != {
        DATA_VERSION
    }:
        raise RuntimeBundleBuildError("runtime-v2 source data identity changed")
    return catalog, benchmark, manifest


def load_governance() -> CrossCategoryGeometryGovernanceArtifact:
    governance = CrossCategoryGeometryGovernanceArtifact.model_validate_json(
        GOVERNANCE_PATH.read_bytes(), strict=True
    )
    if governance.data_version != DATA_VERSION:
        raise RuntimeBundleBuildError("geometry governance data identity changed")
    return governance


def load_candidate_geometry() -> dict[str, dict[str, object]]:
    payload = load_json(CANDIDATE_GEOMETRY_PATH)
    if payload.get("research_status") != "CANDIDATE / RESEARCH / NOT YET GOVERNED":
        raise RuntimeBundleBuildError("candidate geometry status changed")
    if payload.get("feature_count") != 80:
        raise RuntimeBundleBuildError("expected 80 captured candidate geometries")
    features = payload.get("features")
    if not isinstance(features, list):
        raise RuntimeBundleBuildError("candidate geometry features are missing")
    result = {}
    for feature in features:
        if not isinstance(feature, dict):
            raise RuntimeBundleBuildError("candidate geometry feature is invalid")
        decision_unit_id = feature.get("id")
        if not isinstance(decision_unit_id, str) or decision_unit_id in result:
            raise RuntimeBundleBuildError("candidate geometry IDs must be unique")
        result[decision_unit_id] = feature
    return result


def build_map_payload() -> dict[str, object]:
    catalog, _, _ = load_source_artifacts()
    governance = load_governance()
    candidate_geometry = load_candidate_geometry()
    catalog_by_id = {
        project.decision_unit_id: project
        for project in catalog.projects
    }
    decisions = {
        decision.decision_unit_id: decision
        for decision in governance.decisions
    }
    if set(decisions) != set(catalog_by_id):
        raise RuntimeBundleBuildError("geometry decisions must equal catalog identities")

    features = []
    for decision_unit_id in sorted(decisions):
        decision = decisions[decision_unit_id]
        if decision.governance_status != "PROMOTED":
            continue
        project = catalog_by_id[decision_unit_id]
        candidate = candidate_geometry.get(decision_unit_id)
        if candidate is None:
            raise RuntimeBundleBuildError(
                f"{decision_unit_id}: promoted candidate geometry is missing"
            )
        candidate_properties = candidate.get("properties", {})
        if candidate_properties.get("feature_object_id") != decision.source_feature_id:
            raise RuntimeBundleBuildError(
                f"{decision_unit_id}: source feature identity changed"
            )
        if candidate_properties.get("source_url") != decision.source_url:
            raise RuntimeBundleBuildError(f"{decision_unit_id}: source URL changed")
        if project.governed_name != decision.governed_name:
            raise RuntimeBundleBuildError(f"{decision_unit_id}: governed name changed")
        if str(project.presentation_category) != decision.presentation_category:
            raise RuntimeBundleBuildError(f"{decision_unit_id}: category changed")

        features.append(
            {
                "type": "Feature",
                "id": decision_unit_id,
                "properties": {
                    "decision_unit_id": decision_unit_id,
                    "governed_name": decision.governed_name,
                    "presentation_category": decision.presentation_category,
                    "display_role": decision.display_role,
                    "confidence": "HIGH",
                    "geometry_type": decision.candidate_geometry_type,
                    "geometry_origin": "SOURCE_NATIVE_FEATURE",
                    "source_title": decision.candidate_source_title,
                    "source_url": decision.source_url,
                    "source_agency": decision.source_agency,
                    "source_feature_id": decision.source_feature_id,
                    "arcgis_item_id": decision.arcgis_item_id,
                    "arcgis_service_id": decision.arcgis_service_id,
                    "source_layer_id": decision.source_layer_id,
                    "source_date": decision.source_date,
                    "source_last_updated_date": decision.source_last_updated_date,
                    "historical_fit_class": decision.historical_fit_class,
                    "historical_fit_judgment": decision.historical_fit_judgment,
                    "match_identifiers": decision.match_identifiers,
                    "match_method": decision.match_method,
                    "governance_decision_id": governance.governance_decision_id,
                    "caveats": decision.caveats,
                },
                "geometry": candidate["geometry"],
            }
        )

    payload = {
        "type": "FeatureCollection",
        "contract_version": CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION_V3,
        "data_version": DATA_VERSION,
        "historical_decision_snapshot_date": "2026-01-21",
        "project_identity_key": "decision_unit_id",
        "geometry_authority": "GOVERNED_RUNTIME_GEOMETRY_ONLY",
        "mapping_status": "PARTIAL_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE",
        "analytical_project_count": CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
        "mapped_project_count": governance.promoted_project_count,
        "unmapped_project_count": governance.unmapped_project_count,
        "governance_decision_id": governance.governance_decision_id,
        "governance_reconciliation_sha256": sha256(GOVERNANCE_PATH),
        "candidate_geometry_snapshot_sha256": sha256(CANDIDATE_GEOMETRY_PATH),
        "geometry_required_for_model_eligibility": False,
        "geometry_required_for_portfolio_selection": False,
        "fabricated_geometry": False,
        "derived_geocoded_geometry": False,
        "inferred_or_centroid_geometry": False,
        "crs_contract": "RFC_7946_EPSG_4326",
        "limitations": [
            "Only 74 individually approved source-native geometries are governed for display; 32 projects remain explicitly unmapped.",
            "Park, facility, and parcel context must not be described as a capital-project construction footprint.",
            "Post-snapshot source refreshes are used only where the stable location remains historically compatible; later project facts are excluded.",
            "Missing geometry does not remove a project from Explore or Funding Plan and does not affect Funding Priority.",
            "Council District, ZIP, neighborhood, address geocodes, and inferred centroids are not substituted for missing project geometry.",
        ],
        "features": features,
    }
    validated = CrossCategoryMapContextArtifactV3.model_validate(payload)
    return validated.model_dump(mode="json")


def release_id(
    *, catalog_sha256: str, map_sha256: str, benchmark_sha256: str
) -> str:
    semantic = (
        f"{DATA_VERSION}\n"
        f"{CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION_V3}\n"
        f"{catalog_sha256}\n{map_sha256}\n{benchmark_sha256}\n"
    ).encode("utf-8")
    return sha256_bytes(semantic)


def build_manifest_payload() -> dict[str, object]:
    catalog, benchmark, source_manifest = load_source_artifacts()
    governance = load_governance()
    if not all(path.is_file() for path in (CATALOG_PATH, MAP_PATH, BENCHMARK_PATH)):
        raise RuntimeBundleBuildError("runtime-v3 artifacts must exist before manifest")

    catalog_identity = artifact_identity(CATALOG_PATH)
    map_identity = artifact_identity(MAP_PATH)
    benchmark_identity = artifact_identity(BENCHMARK_PATH)
    payload = {
        "contract_version": CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION_V3,
        "data_version": DATA_VERSION,
        "historical_decision_snapshot_date": "2026-01-21",
        "release_bundle_scope": "CROSS_CATEGORY_106_PROJECT_RUNTIME_V3",
        "release_id": release_id(
            catalog_sha256=catalog_identity["sha256"],
            map_sha256=map_identity["sha256"],
            benchmark_sha256=benchmark_identity["sha256"],
        ),
        "source_id": source_manifest.source_id,
        "source_snapshot_sha256": source_manifest.source_snapshot_sha256,
        "contract_versions": {
            "catalog": CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
            "map_context": CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION_V3,
            "benchmark": CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
            "funding_plan": CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
            "manifest": CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION_V3,
            "geometry_governance": CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION,
        },
        "artifacts": {
            "catalog_json": catalog_identity,
            "map_context_geojson": map_identity,
            "benchmark_json": benchmark_identity,
        },
        "reconciliations": {
            "analytical_project_count": len(catalog.projects),
            "governed_request_total_dollars": sum(
                project.model_request_dollars for project in catalog.projects
            ),
            "mapped_project_count": governance.promoted_project_count,
            "unmapped_project_count": governance.unmapped_project_count,
            "fabricated_geometry": False,
            "derived_geocoded_geometry": False,
            "inferred_or_centroid_geometry": False,
            "geometry_governance_decision_id": governance.governance_decision_id,
            "geometry_governance_sha256": sha256(GOVERNANCE_PATH),
            "candidate_geometry_snapshot_sha256": sha256(CANDIDATE_GEOMETRY_PATH),
            "benchmark_matched_cohort_dollars": (
                benchmark.matched_analytical_cohort_dollars
            ),
            "benchmark_project_count": benchmark.historically_recommended_project_count,
            "benchmark_isolated_from_catalog": True,
            "benchmark_isolated_from_portfolio_selection": True,
        },
        "runtime_integration_authorized": True,
    }
    if (
        payload["reconciliations"]["governed_request_total_dollars"]
        != CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
        or benchmark.matched_analytical_cohort_dollars
        != CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS
        or benchmark.historically_recommended_project_count
        != CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT
    ):
        raise RuntimeBundleBuildError("protected analytical or benchmark values changed")
    validated = CrossCategoryReleaseManifestV3.model_validate(payload)
    return validated.model_dump(mode="json")


def serialized_json(payload: dict[str, object]) -> bytes:
    return (
        json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def write_create_only(path: Path, payload: bytes) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() == payload:
            return "unchanged"
        raise DerivedArtifactConflictError(
            f"{path} already exists with different deterministic content"
        )
    path.write_bytes(payload)
    return "created"


def write_bundle() -> dict[str, str]:
    load_source_artifacts()
    results = {
        "catalog.json": write_create_only(CATALOG_PATH, SOURCE_CATALOG_PATH.read_bytes()),
        "benchmark.json": write_create_only(
            BENCHMARK_PATH, SOURCE_BENCHMARK_PATH.read_bytes()
        ),
    }
    results["map-context.geojson"] = write_create_only(
        MAP_PATH, serialized_json(build_map_payload())
    )
    results["manifest.json"] = write_create_only(
        MANIFEST_PATH, serialized_json(build_manifest_payload())
    )
    return results


def main() -> int:
    results = write_bundle()
    manifest = load_json(MANIFEST_PATH)
    map_context = load_json(MAP_PATH)
    print("Cross-category governed-geometry runtime-v3 bundle")
    for artifact, result in results.items():
        print(f"{artifact}: {result}")
    print(f"Mapped projects: {map_context['mapped_project_count']}")
    print(f"Unmapped projects: {map_context['unmapped_project_count']}")
    print(f"Release ID: {manifest['release_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
