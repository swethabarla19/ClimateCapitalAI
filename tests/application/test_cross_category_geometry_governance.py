"""Governance and runtime-v3 validation for project map evidence."""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
from collections import Counter
from pathlib import Path

import pytest
from pydantic import ValidationError

from climatecapital.api.cross_category_runtime import (
    CrossCategoryRuntimeLoadError,
    load_cross_category_runtime_state,
)
from climatecapital.contracts.cross_category_geometry import (
    CrossCategoryGeometryGovernanceArtifact,
)
from climatecapital.contracts.cross_category_release import (
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifact,
    CrossCategoryMapContextArtifactV3,
    CrossCategoryReleaseManifestV3,
)
from climatecapital.contracts.cross_category_runtime import (
    CrossCategoryRuntimeCatalog,
)
from scripts.data import build_cross_category_geometry_governance as governance_builder
from scripts.data import (
    build_cross_category_geometry_runtime_bundle as runtime_builder,
)


ROOT = Path(__file__).resolve().parents[2]
RESEARCH_DIR = ROOT / "data/reconnaissance/external_gis/2026-09-08"
GOVERNANCE_PATH = (
    ROOT
    / "data/governed/cross_category/reconciliation/project-geometry-governance.json"
)
RUNTIME_V2_DIR = ROOT / "data/governed/cross_category/runtime_v2"
RUNTIME_V3_DIR = ROOT / "data/governed/cross_category/runtime_v3"
CATALOG_PATH = RUNTIME_V3_DIR / "catalog.json"
MAP_PATH = RUNTIME_V3_DIR / "map-context.geojson"
BENCHMARK_PATH = RUNTIME_V3_DIR / "benchmark.json"
MANIFEST_PATH = RUNTIME_V3_DIR / "manifest.json"
CANDIDATE_GEOMETRY_PATH = (
    RESEARCH_DIR / "CANDIDATE_NOT_GOVERNED_source_geometries.geojson"
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_governance_artifact_validates_and_covers_all_106_projects():
    governance = CrossCategoryGeometryGovernanceArtifact.model_validate_json(
        GOVERNANCE_PATH.read_bytes(), strict=True
    )
    assert governance.promoted_project_count == 74
    assert governance.unmapped_project_count == 32
    assert len(governance.decisions) == 106
    assert governance.fabricated_geometry is False
    assert governance.geocoded_geometry is False
    assert governance.inferred_or_centroid_geometry is False


def test_governance_builder_regenerates_exact_artifact_and_is_idempotent():
    assert load_json(GOVERNANCE_PATH) == governance_builder.build_payload()
    assert governance_builder.write_artifact() == "unchanged"


def test_promotions_are_exactly_the_individually_reviewed_allowlist():
    governance = load_json(GOVERNANCE_PATH)
    promoted = {
        decision["decision_unit_id"]
        for decision in governance["decisions"]
        if decision["governance_status"] == "PROMOTED"
    }
    assert promoted == governance_builder.PROMOTED_IDS
    assert len(promoted) == 74

    for decision in governance["decisions"]:
        assert decision["reviewed_individually"] is True
        if decision["decision_unit_id"] in promoted:
            assert decision["candidate_confidence"] == "HIGH"
            assert decision["candidate_geometry_origin"] == "source-native"
            assert decision["candidate_ambiguity"] is False
            assert decision["source_feature_id"]
            assert decision["display_role"]
            assert decision["unmapped_reason_code"] is None
        else:
            assert decision["display_role"] is None
            assert decision["unmapped_reason_code"]


def test_special_ambiguities_remain_explicitly_unmapped():
    decisions = {
        decision["decision_unit_id"]: decision
        for decision in load_json(GOVERNANCE_PATH)["decisions"]
    }
    expected = {
        "watershed/5789.127": "IDENTITY_SCOPE_CONFLICT",
        "watershed/5789.150": "CITYWIDE_SINGLE_POINT_MISLEADING",
        "community-facilities/ems/demand-station-1": (
            "CONFLICTING_OFFICIAL_LOCATIONS"
        ),
        "community-facilities/ems/demand-station-2": (
            "CONFLICTING_OFFICIAL_LOCATIONS"
        ),
        "parks/bolm-maintenance-center": "OVERBROAD_CONTEXT_GEOMETRY",
        "community-facilities/acme/elizabet-ney-museum": (
            "MULTIPLE_POSSIBLE_PROJECT_FEATURES"
        ),
        "community-facilities/acme/zilker-hillside-theatre": (
            "ADDRESS_ONLY_NO_SOURCE_GEOMETRY"
        ),
    }
    for decision_unit_id, reason in expected.items():
        assert decisions[decision_unit_id]["governance_status"] != "PROMOTED"
        assert decisions[decision_unit_id]["unmapped_reason_code"] == reason


def test_governance_research_hashes_are_pinned():
    governance = load_json(GOVERNANCE_PATH)
    for field in (
        "candidate_reconciliation",
        "candidate_geometry_snapshot",
        "candidate_investigation_report",
    ):
        reference = governance[field]
        assert sha256(ROOT / reference["path"]) == reference["sha256"]


def test_candidate_geometry_snapshot_remains_clearly_research_only():
    candidate = load_json(CANDIDATE_GEOMETRY_PATH)
    assert candidate["research_status"] == "CANDIDATE / RESEARCH / NOT YET GOVERNED"
    assert candidate["feature_count"] == 80
    assert len(candidate["features"]) == 80
    assert all(
        feature["properties"]["geometry_origin"] == "source-native"
        for feature in candidate["features"]
    )


def test_runtime_v3_artifacts_validate():
    CrossCategoryRuntimeCatalog.model_validate_json(CATALOG_PATH.read_bytes(), strict=True)
    CrossCategoryMapContextArtifactV3.model_validate_json(MAP_PATH.read_bytes(), strict=True)
    CrossCategoryBenchmarkArtifact.model_validate_json(
        BENCHMARK_PATH.read_bytes(), strict=True
    )
    CrossCategoryReleaseManifestV3.model_validate_json(
        MANIFEST_PATH.read_bytes(), strict=True
    )


def test_runtime_v3_preserves_catalog_and_benchmark_byte_for_byte():
    assert CATALOG_PATH.read_bytes() == (RUNTIME_V2_DIR / "catalog.json").read_bytes()
    assert BENCHMARK_PATH.read_bytes() == (
        RUNTIME_V2_DIR / "benchmark.json"
    ).read_bytes()


def test_runtime_v2_zero_geometry_release_remains_frozen():
    legacy = CrossCategoryMapContextArtifact.model_validate_json(
        (RUNTIME_V2_DIR / "map-context.geojson").read_bytes(), strict=True
    )
    assert legacy.mapped_project_count == 0
    assert legacy.unmapped_project_count == 106
    assert legacy.features == []


def test_runtime_v3_map_counts_categories_geometry_and_roles():
    map_context = load_json(MAP_PATH)
    assert map_context["mapped_project_count"] == 74
    assert map_context["unmapped_project_count"] == 32
    assert len(map_context["features"]) == 74
    assert map_context["fabricated_geometry"] is False
    assert map_context["derived_geocoded_geometry"] is False
    assert map_context["inferred_or_centroid_geometry"] is False

    assert Counter(
        feature["properties"]["presentation_category"]
        for feature in map_context["features"]
    ) == {
        "Transportation": 1,
        "Parks & Open Space": 21,
        "Watershed": 35,
        "Community Facilities": 17,
    }
    assert Counter(
        feature["properties"]["geometry_type"]
        for feature in map_context["features"]
    ) == {"point": 64, "polygon": 10}
    assert Counter(
        feature["properties"]["display_role"]
        for feature in map_context["features"]
    ) == {
        "PROJECT_DISPLAY_POINT": 42,
        "FACILITY_SITE_CONTEXT": 22,
        "PARK_SITE_CONTEXT": 8,
        "PROJECT_SITE": 1,
        "PROJECT_PARCEL": 1,
    }


def test_runtime_v3_coordinates_are_wgs84_and_within_austin_region():
    positions = []

    def collect(value):
        if (
            isinstance(value, list)
            and len(value) == 2
            and all(isinstance(item, (int, float)) for item in value)
        ):
            positions.append(value)
            return
        if isinstance(value, list):
            for item in value:
                collect(item)

    for feature in load_json(MAP_PATH)["features"]:
        collect(feature["geometry"]["coordinates"])

    assert positions
    assert all(-98.2 <= longitude <= -97.4 for longitude, _ in positions)
    assert all(29.8 <= latitude <= 30.7 for _, latitude in positions)


def test_runtime_map_features_match_catalog_and_governance():
    catalog = {
        project["decision_unit_id"]: project
        for project in load_json(CATALOG_PATH)["projects"]
    }
    governance = {
        decision["decision_unit_id"]: decision
        for decision in load_json(GOVERNANCE_PATH)["decisions"]
    }
    features = load_json(MAP_PATH)["features"]
    for feature in features:
        properties = feature["properties"]
        decision_unit_id = properties["decision_unit_id"]
        assert feature["id"] == decision_unit_id
        assert catalog[decision_unit_id]["governed_name"] == properties["governed_name"]
        assert governance[decision_unit_id]["governance_status"] == "PROMOTED"
        assert governance[decision_unit_id]["source_feature_id"] == properties[
            "source_feature_id"
        ]
        assert governance[decision_unit_id]["caveats"] == properties["caveats"]
    assert "watershed/5789.150" not in {feature["id"] for feature in features}


def test_runtime_v3_manifest_hashes_and_governance_identity_reconcile():
    manifest = load_json(MANIFEST_PATH)
    map_context = load_json(MAP_PATH)
    governance_hash = sha256(GOVERNANCE_PATH)
    candidate_hash = sha256(CANDIDATE_GEOMETRY_PATH)
    assert manifest["artifacts"]["catalog_json"]["sha256"] == sha256(CATALOG_PATH)
    assert manifest["artifacts"]["map_context_geojson"]["sha256"] == sha256(MAP_PATH)
    assert manifest["artifacts"]["benchmark_json"]["sha256"] == sha256(
        BENCHMARK_PATH
    )
    assert manifest["reconciliations"]["geometry_governance_sha256"] == governance_hash
    assert map_context["governance_reconciliation_sha256"] == governance_hash
    assert (
        manifest["reconciliations"]["candidate_geometry_snapshot_sha256"]
        == candidate_hash
        == map_context["candidate_geometry_snapshot_sha256"]
    )


def test_runtime_v3_builder_regenerates_exact_payloads_and_is_idempotent():
    assert load_json(MAP_PATH) == runtime_builder.build_map_payload()
    assert load_json(MANIFEST_PATH) == runtime_builder.build_manifest_payload()
    assert runtime_builder.write_bundle() == {
        "catalog.json": "unchanged",
        "benchmark.json": "unchanged",
        "map-context.geojson": "unchanged",
        "manifest.json": "unchanged",
    }


def test_runtime_loader_activates_governed_geometry_release():
    state = load_cross_category_runtime_state()
    assert state.bundle_directory == RUNTIME_V3_DIR
    assert state.map_context.mapped_project_count == 74
    assert state.map_context.unmapped_project_count == 32
    assert len(state.map_context.features) == 74
    assert state.release_id == load_json(MANIFEST_PATH)["release_id"]


def test_runtime_loader_rejects_map_metadata_drift_even_with_updated_file_hash(
    tmp_path: Path,
):
    bundle = tmp_path / "runtime-v3"
    shutil.copytree(RUNTIME_V3_DIR, bundle)
    map_path = bundle / "map-context.geojson"
    manifest_path = bundle / "manifest.json"

    map_context = load_json(map_path)
    map_context["features"][0]["properties"]["governed_name"] = "Wrong name"
    map_path.write_text(
        json.dumps(map_context, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    manifest = load_json(manifest_path)
    manifest["artifacts"]["map_context_geojson"] = {
        "sha256": sha256(map_path),
        "byte_size": map_path.stat().st_size,
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    with pytest.raises(CrossCategoryRuntimeLoadError, match="map metadata"):
        load_cross_category_runtime_state(bundle)


def test_v3_map_contract_rejects_citywide_geometry():
    payload = copy.deepcopy(load_json(MAP_PATH))
    payload["features"][0]["id"] = "watershed/5789.150"
    payload["features"][0]["properties"]["decision_unit_id"] = "watershed/5789.150"
    with pytest.raises(ValidationError):
        CrossCategoryMapContextArtifactV3.model_validate(payload, strict=True)


def test_v3_map_contract_rejects_geometry_role_mismatch():
    payload = copy.deepcopy(load_json(MAP_PATH))
    point = next(
        feature
        for feature in payload["features"]
        if feature["geometry"]["type"] == "Point"
    )
    point["properties"]["display_role"] = "PROJECT_PARCEL"
    with pytest.raises(ValidationError):
        CrossCategoryMapContextArtifactV3.model_validate(payload, strict=True)
