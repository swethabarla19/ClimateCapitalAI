"""Cross-category v2 map, benchmark, and release-manifest contracts.

These contracts complete the deterministic 106-project runtime bundle without
fabricating geometry and without allowing historical recommendation outcomes to
enter ranking or portfolio construction.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, model_validator

from .common import (
    DataVersion,
    PositiveWholeDollars,
    ProjectId,
    Sha256,
    ShortText,
    StableIdentifier,
    StrictModel,
    WholeDollars,
)
from .cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
)


CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION = (
    "p0-cross-category-map-context/2.0.0"
)

CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION = (
    "p0-cross-category-benchmark/2.0.0"
)

CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION = (
    "p0-cross-category-release-manifest/2.0.0"
)

CROSS_CATEGORY_HISTORICAL_FULL_PACKAGE_DOLLARS = (
    700_000_000
)

CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS = (
    332_000_000
)

CROSS_CATEGORY_HISTORICAL_OUTSIDE_COHORT_DOLLARS = (
    368_000_000
)

CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT = (
    20
)

CROSS_CATEGORY_RUNTIME_MAPPED_PROJECT_COUNT = 0

CROSS_CATEGORY_RUNTIME_UNMAPPED_PROJECT_COUNT = (
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
)


ByteSize = Annotated[
    int,
    Field(
        strict=True,
        gt=0,
    ),
]


# ---------------------------------------------------------------------------
# Map context
# ---------------------------------------------------------------------------


class CrossCategoryMapContextArtifact(StrictModel):
    type: Literal["FeatureCollection"]

    contract_version: Literal[
        CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION
    ]

    data_version: DataVersion

    historical_decision_snapshot_date: Literal[
        "2026-01-21"
    ]

    project_identity_key: Literal[
        "decision_unit_id"
    ]

    geometry_authority: Literal[
        "GOVERNED_RUNTIME_GEOMETRY_ONLY"
    ]

    mapping_status: Literal[
        "NO_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE"
    ]

    analytical_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ]

    mapped_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_MAPPED_PROJECT_COUNT
    ]

    unmapped_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_UNMAPPED_PROJECT_COUNT
    ]

    geometry_required_for_model_eligibility: Literal[
        False
    ]

    geometry_required_for_portfolio_selection: Literal[
        False
    ]

    fabricated_geometry: Literal[
        False
    ]

    crs_contract: Literal[
        "RFC_7946_EPSG_4326_IF_GEOMETRY_PRESENT"
    ]

    limitations: list[
        ShortText
    ] = Field(
        min_length=1,
    )

    features: list[
        dict[str, object]
    ] = Field(
        max_length=0,
    )

    @model_validator(mode="after")
    def map_reconciles(
        self,
    ) -> CrossCategoryMapContextArtifact:
        if (
            self.mapped_project_count
            + self.unmapped_project_count
            != self.analytical_project_count
        ):
            raise ValueError(
                "mapped and unmapped project counts "
                "must reconcile to the analytical cohort"
            )

        if self.features:
            raise ValueError(
                "M3.8D2 cannot contain map features "
                "without governed runtime geometry"
            )

        return self


# ---------------------------------------------------------------------------
# Historical benchmark
# ---------------------------------------------------------------------------


PresentationCategory = Literal[
    "Transportation",
    "Parks & Open Space",
    "Watershed",
    "Community Facilities",
]


class CrossCategoryBenchmarkProjectOutcome(
    StrictModel
):
    decision_unit_id: StableIdentifier

    canonical_project_id: (
        ProjectId | None
    ) = None

    governed_name: ShortText

    presentation_category: PresentationCategory

    historically_recommended: bool = Field(
        strict=True
    )

    january_recommendation_dollars: (
        PositiveWholeDollars | None
    ) = None

    source_conflict_flag: bool = Field(
        strict=True
    )

    request_version_conflict: bool = Field(
        strict=True
    )

    outcome_role: Literal[
        "BENCHMARK_OUTCOME_ONLY"
    ]

    @model_validator(mode="after")
    def recommendation_semantics(
        self,
    ) -> CrossCategoryBenchmarkProjectOutcome:
        has_amount = (
            self.january_recommendation_dollars
            is not None
        )

        if (
            self.historically_recommended
            is not has_amount
        ):
            raise ValueError(
                "historically_recommended must "
                "agree with recommendation availability"
            )

        return self


class CrossCategoryBenchmarkCategorySummary(
    StrictModel
):
    presentation_category: PresentationCategory

    analytical_project_count: Annotated[
        int,
        Field(
            strict=True,
            gt=0,
        ),
    ]

    historically_recommended_project_count: Annotated[
        int,
        Field(
            strict=True,
            ge=0,
        ),
    ]

    recommendation_total_dollars: WholeDollars


class CrossCategoryBenchmarkArtifact(
    StrictModel
):
    contract_version: Literal[
        CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION
    ]

    data_version: DataVersion

    historical_decision_snapshot_date: Literal[
        "2026-01-21"
    ]

    source_id: StableIdentifier
    source_snapshot_sha256: Sha256

    outcome_role: Literal[
        "BENCHMARK_OUTCOME_ONLY"
    ]

    analytical_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ]

    full_initial_recommendation_dollars: Literal[
        CROSS_CATEGORY_HISTORICAL_FULL_PACKAGE_DOLLARS
    ]

    matched_analytical_cohort_dollars: Literal[
        CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS
    ]

    outside_analytical_cohort_dollars: Literal[
        CROSS_CATEGORY_HISTORICAL_OUTSIDE_COHORT_DOLLARS
    ]

    historically_recommended_project_count: Literal[
        CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT
    ]

    ranking_input: Literal[False]
    portfolio_selection_input: Literal[False]

    category_summaries: list[
        CrossCategoryBenchmarkCategorySummary
    ] = Field(
        min_length=4,
        max_length=4,
    )

    project_outcomes: list[
        CrossCategoryBenchmarkProjectOutcome
    ] = Field(
        min_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    limitations: list[
        ShortText
    ] = Field(
        min_length=1,
    )

    @model_validator(mode="after")
    def benchmark_reconciles(
        self,
    ) -> CrossCategoryBenchmarkArtifact:
        if (
            self.full_initial_recommendation_dollars
            != (
                self.matched_analytical_cohort_dollars
                + self.outside_analytical_cohort_dollars
            )
        ):
            raise ValueError(
                "full package must reconcile to "
                "matched plus outside-cohort dollars"
            )

        ids = [
            outcome.decision_unit_id
            for outcome in self.project_outcomes
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "benchmark decision_unit_id "
                "values must be unique"
            )

        recommended = [
            outcome
            for outcome in self.project_outcomes
            if outcome.historically_recommended
        ]

        if (
            len(recommended)
            != CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT
        ):
            raise ValueError(
                "benchmark must preserve "
                "20 historically recommended projects"
            )

        recommendation_total = sum(
            outcome.january_recommendation_dollars
            or 0
            for outcome in recommended
        )

        if (
            recommendation_total
            != CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS
        ):
            raise ValueError(
                "benchmark project outcomes must "
                "sum to $332,000,000"
            )

        expected_category_counts = {
            "Transportation": 9,
            "Parks & Open Space": 22,
            "Watershed": 37,
            "Community Facilities": 38,
        }

        expected_recommended_counts = {
            "Transportation": 2,
            "Parks & Open Space": 1,
            "Watershed": 12,
            "Community Facilities": 5,
        }

        expected_category_dollars = {
            "Transportation": 28_000_000,
            "Parks & Open Space": 55_000_000,
            "Watershed": 125_000_000,
            "Community Facilities": 124_000_000,
        }

        summaries = {
            summary.presentation_category:
                summary
            for summary in self.category_summaries
        }

        if (
            set(summaries)
            != set(expected_category_counts)
        ):
            raise ValueError(
                "benchmark must contain exactly "
                "four category summaries"
            )

        for (
            category,
            expected_count,
        ) in expected_category_counts.items():
            summary = summaries[
                category
            ]

            if (
                summary.analytical_project_count
                != expected_count
            ):
                raise ValueError(
                    f"{category} analytical count changed"
                )

            if (
                summary
                .historically_recommended_project_count
                != expected_recommended_counts[
                    category
                ]
            ):
                raise ValueError(
                    f"{category} historical recommendation "
                    "count changed"
                )

            if (
                summary.recommendation_total_dollars
                != expected_category_dollars[
                    category
                ]
            ):
                raise ValueError(
                    f"{category} historical recommendation "
                    "total changed"
                )

        return self


# ---------------------------------------------------------------------------
# Release manifest
# ---------------------------------------------------------------------------


class CrossCategoryArtifactIdentity(
    StrictModel
):
    sha256: Sha256
    byte_size: ByteSize


class CrossCategoryReleaseArtifactIdentities(
    StrictModel
):
    catalog_json: CrossCategoryArtifactIdentity
    map_context_geojson: CrossCategoryArtifactIdentity
    benchmark_json: CrossCategoryArtifactIdentity


class CrossCategoryReleaseContractVersions(
    StrictModel
):
    catalog: Literal[
        CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
    ]

    map_context: Literal[
        CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION
    ]

    benchmark: Literal[
        CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION
    ]

    funding_plan: Literal[
        CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    ]

    manifest: Literal[
        CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION
    ]


class CrossCategoryReleaseReconciliations(
    StrictModel
):
    analytical_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ]

    governed_request_total_dollars: Literal[
        CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
    ]

    mapped_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_MAPPED_PROJECT_COUNT
    ]

    unmapped_project_count: Literal[
        CROSS_CATEGORY_RUNTIME_UNMAPPED_PROJECT_COUNT
    ]

    fabricated_geometry: Literal[
        False
    ]

    benchmark_matched_cohort_dollars: Literal[
        CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS
    ]

    benchmark_project_count: Literal[
        CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT
    ]

    benchmark_isolated_from_catalog: Literal[
        True
    ]

    benchmark_isolated_from_portfolio_selection: Literal[
        True
    ]


class CrossCategoryReleaseManifest(
    StrictModel
):
    contract_version: Literal[
        CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION
    ]

    data_version: DataVersion

    historical_decision_snapshot_date: Literal[
        "2026-01-21"
    ]

    release_bundle_scope: Literal[
        "CROSS_CATEGORY_106_PROJECT_RUNTIME_V2"
    ]

    release_id: Sha256

    source_id: StableIdentifier
    source_snapshot_sha256: Sha256

    contract_versions: (
        CrossCategoryReleaseContractVersions
    )

    artifacts: (
        CrossCategoryReleaseArtifactIdentities
    )

    reconciliations: (
        CrossCategoryReleaseReconciliations
    )

    runtime_integration_authorized: bool = Field(
        strict=True
    )