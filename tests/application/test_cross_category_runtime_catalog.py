"""Focused M3.8B tests for the deterministic 106-project runtime-v2 catalog."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
    CrossCategoryRuntimeCatalog,
)
from scripts.data import (
    build_cross_category_runtime_catalog as catalog_builder,
)


ROOT = Path(__file__).resolve().parents[2]

CATALOG_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v2"
    / "catalog.json"
)


def load_catalog() -> dict:
    return json.loads(
        CATALOG_PATH.read_text(
            encoding="utf-8"
        )
    )


def project_index() -> dict[str, dict]:
    return {
        project["decision_unit_id"]:
            project
        for project in load_catalog()[
            "projects"
        ]
    }


def test_runtime_catalog_exists():
    assert CATALOG_PATH.is_file()


def test_runtime_catalog_validates_against_v2_contract():
    payload = load_catalog()

    validated = (
        CrossCategoryRuntimeCatalog
        .model_validate(
            payload
        )
    )

    assert (
        validated.contract_version
        == CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
    )


def test_runtime_catalog_identity_and_authority_are_locked():
    catalog = load_catalog()

    assert (
        catalog["contract_version"]
        == "p0-cross-category-catalog/2.0.0"
    )

    assert (
        catalog["data_version"]
        == (
            "climatecapital-austin-"
            "2026-01-21-cross-category-v2"
        )
    )

    assert (
        catalog[
            "historical_decision_snapshot_date"
        ]
        == "2026-01-21"
    )

    assert (
        catalog["model_scope"]
        == "CROSS_CATEGORY_PRB_PROJECT_MODEL"
    )

    assert (
        catalog["methodology_name"]
        == (
            "PRIORITY_CONSTRAINED_"
            "ANALYST_GOVERNED_"
            "PORTFOLIO_CONSTRUCTION"
        )
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


def test_runtime_catalog_contains_exactly_106_projects():
    catalog = load_catalog()

    projects = catalog[
        "projects"
    ]

    assert (
        catalog["project_count"]
        == CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        == 106
    )

    assert len(projects) == 106


def test_runtime_decision_unit_ids_are_unique_and_deterministically_sorted():
    ids = [
        project[
            "decision_unit_id"
        ]
        for project in load_catalog()[
            "projects"
        ]
    ]

    assert len(ids) == 106
    assert len(set(ids)) == 106

    assert ids == sorted(ids)


def test_runtime_category_counts_are_exact():
    catalog = load_catalog()

    projects = catalog[
        "projects"
    ]

    counts = Counter(
        project[
            "presentation_category"
        ]
        for project in projects
    )

    assert counts == {
        "Transportation": 9,
        "Parks & Open Space": 22,
        "Watershed": 37,
        "Community Facilities": 38,
    }

    assert (
        catalog[
            "category_counts"
        ]
        == {
            "transportation": 9,
            "parks_open_space": 22,
            "watershed": 37,
            "community_facilities": 38,
        }
    )


def test_runtime_request_total_is_exact():
    catalog = load_catalog()

    total = sum(
        project[
            "model_request_dollars"
        ]
        for project in catalog[
            "projects"
        ]
    )

    assert (
        total
        == CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
        == 1_973_520_000
    )

    assert (
        catalog[
            "governed_request_total_dollars"
        ]
        == 1_973_520_000
    )


def test_all_runtime_project_requests_are_positive():
    for project in load_catalog()[
        "projects"
    ]:
        assert (
            project[
                "model_request_dollars"
            ]
            > 0
        )


def test_funding_priority_structure_is_preserved():
    catalog = load_catalog()

    projects = catalog[
        "projects"
    ]

    score_counts = Counter(
        float(
            project[
                "funding_priority_score"
            ]
        )
        for project in projects
    )

    unique_score_count = len(
        score_counts
    )

    tied_score_groups = {
        score: count
        for score, count
        in score_counts.items()
        if count > 1
    }

    tied_project_count = sum(
        tied_score_groups.values()
    )

    assert unique_score_count == 35
    assert len(tied_score_groups) == 24
    assert tied_project_count == 95

    assert (
        catalog[
            "unique_funding_priority_score_count"
        ]
        == 35
    )

    assert (
        catalog[
            "tied_score_group_count"
        ]
        == 24
    )

    assert (
        catalog[
            "projects_in_tied_score_groups"
        ]
        == 95
    )


def test_half_point_priority_scores_are_preserved_exactly():
    half_points = {
        float(
            project[
                "funding_priority_score"
            ]
        )
        for project in load_catalog()[
            "projects"
        ]
        if (
            float(
                project[
                    "funding_priority_score"
                ]
            )
            % 1
            != 0
        )
    }

    assert half_points == {
        54.5,
        53.5,
        50.5,
    }


def test_watershed_and_non_watershed_canonical_identity_semantics():
    projects = load_catalog()[
        "projects"
    ]

    watershed = [
        project
        for project in projects
        if (
            project[
                "presentation_category"
            ]
            == "Watershed"
        )
    ]

    non_watershed = [
        project
        for project in projects
        if (
            project[
                "presentation_category"
            ]
            != "Watershed"
        )
    ]

    assert len(watershed) == 37
    assert len(non_watershed) == 69

    assert all(
        project[
            "canonical_project_id"
        ]
        is not None
        for project in watershed
    )

    assert all(
        project[
            "canonical_project_id"
        ]
        is None
        for project in non_watershed
    )


def test_prb_component_vectors_reproduce_priority_scores():
    component_names = (
        "strategic_alignment",
        "critical_asset",
        "community_consideration",
        "efficiency",
        "timeliness_readiness",
        "climate_resilience",
    )

    for project in load_catalog()[
        "projects"
    ]:
        components = project[
            "prb_components"
        ]

        total = sum(
            float(
                components[
                    name
                ]
            )
            for name
            in component_names
        )

        assert total == float(
            project[
                "funding_priority_score"
            ]
        )


def test_tie_metadata_is_internally_consistent():
    projects = load_catalog()[
        "projects"
    ]

    groups: dict[
        float,
        list[dict],
    ] = {}

    for project in projects:
        score = float(
            project[
                "funding_priority_score"
            ]
        )

        groups.setdefault(
            score,
            [],
        ).append(
            project
        )

    for members in groups.values():
        expected_size = len(
            members
        )

        for project in members:
            assert (
                project[
                    "tie_group_size"
                ]
                == expected_size
            )

            assert (
                project[
                    "is_tied"
                ]
                is (
                    expected_size > 1
                )
            )

            assert (
                project[
                    "display_tiebreak_has_analytical_meaning"
                ]
                is False
            )

        display_orders = sorted(
            project[
                "display_order_within_tie"
            ]
            for project
            in members
        )

        assert display_orders == list(
            range(
                1,
                expected_size + 1,
            )
        )


def test_council_district_assignment_coverage_matches_b0():
    counts = Counter(
        project[
            "council_district"
        ][
            "assignment_type"
        ]
        for project in load_catalog()[
            "projects"
        ]
    )

    assert counts == {
        "SINGLE_DISTRICT": 85,
        "MULTI_DISTRICT": 12,
        "CITYWIDE": 1,
        "UNSPECIFIED": 8,
    }


def test_om_coverage_matches_b0():
    counts = Counter(
        project[
            "om_impact"
        ][
            "value"
        ]
        for project in load_catalog()[
            "projects"
        ]
    )

    assert counts == {
        "NO": 74,
        "YES": 32,
    }


def test_council_district_and_om_remain_non_optimizing_context():
    for project in load_catalog()[
        "projects"
    ]:
        district = project[
            "council_district"
        ]

        om = project[
            "om_impact"
        ]

        assert (
            district[
                "analyst_review_only"
            ]
            is True
        )

        assert (
            district[
                "hard_portfolio_constraint"
            ]
            is False
        )

        assert (
            om[
                "analyst_review_only"
            ]
            is True
        )

        assert (
            om[
                "hard_portfolio_constraint"
            ]
            is False
        )

        assert (
            om[
                "additional_score_preference_authorized"
            ]
            is False
        )


def test_fire_education_building_b_preserves_unspecified_district():
    project = project_index()[
        (
            "community-facilities/"
            "fire/education-building-b"
        )
    ]

    district = project[
        "council_district"
    ]

    assert (
        district[
            "assignment_type"
        ]
        == "UNSPECIFIED"
    )

    assert (
        district[
            "districts"
        ]
        == []
    )

    assert (
        district[
            "source_value"
        ]
        is None
    )


def test_source_request_conflicts_are_preserved_not_excluded():
    projects = load_catalog()[
        "projects"
    ]

    conflicts = {
        project[
            "decision_unit_id"
        ]
        for project in projects
        if (
            project[
                "request_version_conflict"
            ]
            is True
        )
    }

    assert conflicts == {
        (
            "community-facilities/acme/"
            "george-washington-carver-museum"
        ),
        (
            "community-facilities/library/"
            "colony-park-branch-library"
        ),
        "watershed/5754.149",
    }


def test_top_and_bottom_priority_projects_are_preserved():
    projects = load_catalog()[
        "projects"
    ]

    top = min(
        projects,
        key=lambda project: (
            project[
                "funding_priority_rank"
            ],
            project[
                "decision_unit_id"
            ],
        ),
    )

    bottom = max(
        projects,
        key=lambda project: (
            project[
                "funding_priority_rank"
            ],
            project[
                "decision_unit_id"
            ],
        ),
    )

    assert (
        top[
            "decision_unit_id"
        ]
        == "parks/bolm-maintenance-center"
    )

    assert (
        top[
            "funding_priority_score"
        ]
        == 83
    )

    assert (
        top[
            "funding_priority_rank"
        ]
        == 1
    )

    assert (
        bottom[
            "decision_unit_id"
        ]
        == (
            "community-facilities/"
            "fire/education-building-b"
        )
    )

    assert (
        bottom[
            "funding_priority_score"
        ]
        == 40
    )

    assert (
        bottom[
            "funding_priority_rank"
        ]
        == 106
    )


def test_benchmark_outcome_fields_do_not_leak_into_runtime_catalog():
    forbidden = {
        "january_recommendation_dollars",
        "january_recommendation_present",
        "historical_recommendation_amount_dollars",
        "historical_category_allocation",
    }

    for project in load_catalog()[
        "projects"
    ]:
        assert (
            forbidden
            & set(project)
        ) == set()


def test_provenance_refs_are_sorted_and_unique():
    for project in load_catalog()[
        "projects"
    ]:
        refs = project[
            "provenance_refs"
        ]

        assert refs
        assert refs == sorted(
            set(refs)
        )


def test_committed_runtime_catalog_equals_deterministic_builder_output():
    actual = (
        CATALOG_PATH.read_text(
            encoding="utf-8"
        )
    )

    expected = (
        catalog_builder
        .serialized_catalog()
    )

    assert actual == expected


def test_runtime_catalog_builder_is_idempotent_with_temp_output(
    monkeypatch,
    tmp_path,
):
    output = (
        tmp_path
        / "catalog.json"
    )

    monkeypatch.setattr(
        catalog_builder,
        "OUTPUT_PATH",
        output,
    )

    assert (
        catalog_builder.write_catalog()
        == "created"
    )

    assert (
        catalog_builder.write_catalog()
        == "unchanged"
    )


def test_runtime_catalog_builder_refuses_differing_existing_output(
    monkeypatch,
    tmp_path,
):
    output = (
        tmp_path
        / "catalog.json"
    )

    monkeypatch.setattr(
        catalog_builder,
        "OUTPUT_PATH",
        output,
    )

    assert (
        catalog_builder.write_catalog()
        == "created"
    )

    output.write_text(
        '{"different": true}\n',
        encoding="utf-8",
    )

    with pytest.raises(
        catalog_builder.DerivedArtifactConflictError
    ):
        catalog_builder.write_catalog()


def test_runtime_catalog_builder_fails_if_runtime_integration_was_prematurely_authorized(
    monkeypatch,
    tmp_path,
):
    methodology = (
        catalog_builder.load_json(
            catalog_builder.METHODOLOGY_PATH
        )
    )

    methodology[
        "runtime_integration_authorized"
    ] = True

    path = (
        tmp_path
        / "methodology.json"
    )

    path.write_text(
        json.dumps(
            methodology
        ),
        encoding="utf-8",
    )

    monkeypatch.setattr(
        catalog_builder,
        "METHODOLOGY_PATH",
        path,
    )

    with pytest.raises(
        catalog_builder.RuntimeCatalogBuildError,
        match=(
            "M3.7D predecessor methodology "
            "must retain"
        ),
    ):
        catalog_builder.build_catalog_payload()