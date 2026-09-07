"""Focused M3.8D2 tests for the governed cross-category runtime-v2 bundle."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

import pytest

from climatecapital.contracts.cross_category_release import (
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifact,
    CrossCategoryReleaseManifest,
)
from climatecapital.contracts.cross_category_runtime import (
    CrossCategoryRuntimeCatalog,
)
from scripts.data import (
    build_cross_category_runtime_bundle as bundle_builder,
)


ROOT = Path(__file__).resolve().parents[2]

RUNTIME_DIR = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v2"
)

CATALOG_PATH = RUNTIME_DIR / "catalog.json"
MAP_PATH = RUNTIME_DIR / "map-context.geojson"
BENCHMARK_PATH = RUNTIME_DIR / "benchmark.json"
MANIFEST_PATH = RUNTIME_DIR / "manifest.json"


def load_json(path: Path) -> dict:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def test_all_four_runtime_bundle_files_exist():
    assert CATALOG_PATH.is_file()
    assert MAP_PATH.is_file()
    assert BENCHMARK_PATH.is_file()
    assert MANIFEST_PATH.is_file()


def test_catalog_validates():
    CrossCategoryRuntimeCatalog.model_validate(
        load_json(CATALOG_PATH)
    )


def test_map_validates():
    CrossCategoryMapContextArtifact.model_validate(
        load_json(MAP_PATH)
    )


def test_benchmark_validates():
    CrossCategoryBenchmarkArtifact.model_validate(
        load_json(BENCHMARK_PATH)
    )


def test_manifest_validates():
    CrossCategoryReleaseManifest.model_validate(
        load_json(MANIFEST_PATH)
    )


def test_all_runtime_artifacts_share_one_data_version():
    versions = {
        load_json(CATALOG_PATH)["data_version"],
        load_json(MAP_PATH)["data_version"],
        load_json(BENCHMARK_PATH)["data_version"],
        load_json(MANIFEST_PATH)["data_version"],
    }

    assert versions == {
        (
            "climatecapital-austin-"
            "2026-01-21-cross-category-v2"
        )
    }


def test_map_truthfully_reports_zero_governed_geometry():
    data = load_json(MAP_PATH)

    assert data["type"] == "FeatureCollection"
    assert data["analytical_project_count"] == 106
    assert data["mapped_project_count"] == 0
    assert data["unmapped_project_count"] == 106

    assert data["features"] == []

    assert (
        data["fabricated_geometry"]
        is False
    )

    assert (
        data[
            "geometry_required_for_model_eligibility"
        ]
        is False
    )

    assert (
        data[
            "geometry_required_for_portfolio_selection"
        ]
        is False
    )


def test_benchmark_preserves_historical_scope():
    data = load_json(BENCHMARK_PATH)

    assert (
        data[
            "full_initial_recommendation_dollars"
        ]
        == 700_000_000
    )

    assert (
        data[
            "matched_analytical_cohort_dollars"
        ]
        == 332_000_000
    )

    assert (
        data[
            "outside_analytical_cohort_dollars"
        ]
        == 368_000_000
    )

    assert (
        data[
            "historically_recommended_project_count"
        ]
        == 20
    )

    assert (
        data["ranking_input"]
        is False
    )

    assert (
        data[
            "portfolio_selection_input"
        ]
        is False
    )


def test_benchmark_contains_exactly_106_project_outcomes():
    outcomes = load_json(
        BENCHMARK_PATH
    )[
        "project_outcomes"
    ]

    assert len(outcomes) == 106

    ids = [
        outcome["decision_unit_id"]
        for outcome in outcomes
    ]

    assert len(set(ids)) == 106
    assert ids == sorted(ids)


def test_benchmark_20_recommended_projects_sum_to_332m():
    outcomes = load_json(
        BENCHMARK_PATH
    )[
        "project_outcomes"
    ]

    recommended = [
        outcome
        for outcome in outcomes
        if outcome[
            "historically_recommended"
        ]
    ]

    assert len(recommended) == 20

    assert (
        sum(
            outcome[
                "january_recommendation_dollars"
            ]
            for outcome in recommended
        )
        == 332_000_000
    )


def test_not_recommended_is_null_not_zero():
    outcomes = load_json(
        BENCHMARK_PATH
    )[
        "project_outcomes"
    ]

    not_recommended = [
        outcome
        for outcome in outcomes
        if not outcome[
            "historically_recommended"
        ]
    ]

    assert len(not_recommended) == 86

    assert all(
        outcome[
            "january_recommendation_dollars"
        ]
        is None
        for outcome
        in not_recommended
    )


def test_benchmark_category_counts_and_dollars_reconcile():
    summaries = {
        summary[
            "presentation_category"
        ]:
            summary
        for summary
        in load_json(
            BENCHMARK_PATH
        )[
            "category_summaries"
        ]
    }

    assert summaries[
        "Transportation"
    ] == {
        "presentation_category":
            "Transportation",
        "analytical_project_count":
            9,
        "historically_recommended_project_count":
            2,
        "recommendation_total_dollars":
            28_000_000,
    }

    assert summaries[
        "Parks & Open Space"
    ][
        "recommendation_total_dollars"
    ] == 55_000_000

    assert summaries[
        "Watershed"
    ][
        "recommendation_total_dollars"
    ] == 125_000_000

    assert summaries[
        "Community Facilities"
    ][
        "recommendation_total_dollars"
    ] == 124_000_000


def test_benchmark_project_ids_match_catalog_exactly():
    catalog_ids = {
        project[
            "decision_unit_id"
        ]
        for project in load_json(
            CATALOG_PATH
        )[
            "projects"
        ]
    }

    benchmark_ids = {
        outcome[
            "decision_unit_id"
        ]
        for outcome in load_json(
            BENCHMARK_PATH
        )[
            "project_outcomes"
        ]
    }

    assert benchmark_ids == catalog_ids


def test_catalog_still_contains_no_historical_outcome_fields():
    forbidden = {
        "historically_recommended",
        "january_recommendation_dollars",
        "historical_category_allocation",
    }

    for project in load_json(
        CATALOG_PATH
    )[
        "projects"
    ]:
        assert (
            forbidden
            & set(project)
        ) == set()


def test_manifest_hashes_match_current_artifacts():
    manifest = load_json(
        MANIFEST_PATH
    )

    assert (
        manifest[
            "artifacts"
        ][
            "catalog_json"
        ][
            "sha256"
        ]
        == sha256(CATALOG_PATH)
    )

    assert (
        manifest[
            "artifacts"
        ][
            "map_context_geojson"
        ][
            "sha256"
        ]
        == sha256(MAP_PATH)
    )

    assert (
        manifest[
            "artifacts"
        ][
            "benchmark_json"
        ][
            "sha256"
        ]
        == sha256(BENCHMARK_PATH)
    )


def test_manifest_reconciliations_are_locked():
    recon = load_json(
        MANIFEST_PATH
    )[
        "reconciliations"
    ]

    assert (
        recon[
            "analytical_project_count"
        ]
        == 106
    )

    assert (
        recon[
            "governed_request_total_dollars"
        ]
        == 1_973_520_000
    )

    assert (
        recon[
            "mapped_project_count"
        ]
        == 0
    )

    assert (
        recon[
            "unmapped_project_count"
        ]
        == 106
    )

    assert (
        recon[
            "fabricated_geometry"
        ]
        is False
    )

    assert (
        recon[
            "benchmark_matched_cohort_dollars"
        ]
        == 332_000_000
    )

    assert (
        recon[
            "benchmark_project_count"
        ]
        == 20
    )

    assert (
        recon[
            "benchmark_isolated_from_catalog"
        ]
        is True
    )

    assert (
        recon[
            "benchmark_isolated_from_portfolio_selection"
        ]
        is True
    )


def test_manifest_records_runtime_integration_authority():
    manifest = load_json(
        MANIFEST_PATH
    )

    assert (
        manifest[
            "runtime_integration_authorized"
        ]
        is True
    )


def test_source_checksum_is_pinned():
    benchmark = load_json(
        BENCHMARK_PATH
    )

    manifest = load_json(
        MANIFEST_PATH
    )

    expected = (
        "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359"
    )

    assert (
        benchmark[
            "source_snapshot_sha256"
        ]
        == expected
    )

    assert (
        manifest[
            "source_snapshot_sha256"
        ]
        == expected
    )


def test_bundle_builder_regenerates_exact_payloads():
    assert (
        load_json(MAP_PATH)
        == bundle_builder.build_map_payload()
    )

    assert (
        load_json(BENCHMARK_PATH)
        == bundle_builder.build_benchmark_payload()
    )

    assert (
        load_json(MANIFEST_PATH)
        == bundle_builder.build_manifest_payload()
    )


def test_bundle_builder_is_idempotent():
    results = (
        bundle_builder.write_bundle()
    )

    assert results == {
        "map-context.geojson":
            "unchanged",
        "benchmark.json":
            "unchanged",
        "manifest.json":
            "unchanged",
    }


def test_recommended_counts_by_category_match_governed_benchmark():
    outcomes = load_json(
        BENCHMARK_PATH
    )[
        "project_outcomes"
    ]

    counts = Counter(
        outcome[
            "presentation_category"
        ]
        for outcome in outcomes
        if outcome[
            "historically_recommended"
        ]
    )

    assert counts == {
        "Transportation": 2,
        "Parks & Open Space": 1,
        "Watershed": 12,
        "Community Facilities": 5,
    }