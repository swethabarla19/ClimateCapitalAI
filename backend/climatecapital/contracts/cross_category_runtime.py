"""Cross-category v2 runtime contracts for the governed 106-project model.

These contracts are introduced in parallel with the existing Watershed-oriented
v1 runtime. They do not activate runtime integration by themselves.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator, model_validator

from .common import (
    DataVersion,
    NonEmptyString,
    PositiveWholeDollars,
    ProjectId,
    Sha256,
    ShortText,
    StableIdentifier,
    StrictModel,
    WholeDollars,
)


# ---------------------------------------------------------------------------
# Contract identity
# ---------------------------------------------------------------------------

CROSS_CATEGORY_CATALOG_CONTRACT_VERSION = (
    "p0-cross-category-catalog/2.0.0"
)

CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION = (
    "p0-cross-category-funding-plan/2.0.0"
)

CROSS_CATEGORY_RUNTIME_MODEL_SCOPE = (
    "CROSS_CATEGORY_PRB_PROJECT_MODEL"
)

CROSS_CATEGORY_PORTFOLIO_METHODOLOGY = (
    "PRIORITY_CONSTRAINED_"
    "ANALYST_GOVERNED_"
    "PORTFOLIO_CONSTRUCTION"
)


# ---------------------------------------------------------------------------
# Exact governed cross-category reconciliation values
# ---------------------------------------------------------------------------

CROSS_CATEGORY_RUNTIME_PROJECT_COUNT = 106

CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS = (
    1_973_520_000
)

CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT = 35
CROSS_CATEGORY_TIED_SCORE_GROUP_COUNT = 24
CROSS_CATEGORY_PROJECTS_IN_TIES = 95

HISTORICAL_MATCHED_COHORT_BUDGET_DOLLARS = (
    332_000_000
)

# Technical scenario bound only.
# This is not City policy. A budget above all governed project requests
# cannot change the selected full-request project universe.
CROSS_CATEGORY_MAX_SCENARIO_BUDGET_DOLLARS = (
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
)


# ---------------------------------------------------------------------------
# Shared primitives
# ---------------------------------------------------------------------------

DecisionUnitId = StableIdentifier

CrossCategoryScenarioBudgetDollars = Annotated[
    int,
    Field(
        strict=True,
        ge=0,
        le=CROSS_CATEGORY_MAX_SCENARIO_BUDGET_DOLLARS,
    ),
]

FundingPriorityRank = Annotated[
    int,
    Field(
        strict=True,
        ge=1,
        le=CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    ),
]

TieGroupSize = Annotated[
    int,
    Field(
        strict=True,
        ge=1,
        le=CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    ),
]

DisplayOrderWithinTie = Annotated[
    int,
    Field(
        strict=True,
        ge=1,
        le=CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    ),
]


def _validate_half_point_score(
    value: int | float,
    *,
    minimum: float,
    maximum: float,
    label: str,
) -> int | float:
    numeric = float(value)

    if not minimum <= numeric <= maximum:
        raise ValueError(
            f"{label} must be between "
            f"{minimum:g} and {maximum:g}"
        )

    if numeric * 2 % 1 != 0:
        raise ValueError(
            f"{label} must use whole- "
            "or half-point increments"
        )

    return value


FundingPriorityScore = Annotated[
    int | float,
    Field(
        ge=0,
        le=100,
    ),
]


# ---------------------------------------------------------------------------
# Presentation and source-context enums
# ---------------------------------------------------------------------------


class RuntimePresentationCategory(StrEnum):
    TRANSPORTATION = "Transportation"
    PARKS_OPEN_SPACE = "Parks & Open Space"
    WATERSHED = "Watershed"
    COMMUNITY_FACILITIES = "Community Facilities"


class CouncilDistrictAssignmentType(StrEnum):
    SINGLE_DISTRICT = "SINGLE_DISTRICT"
    MULTI_DISTRICT = "MULTI_DISTRICT"
    CITYWIDE = "CITYWIDE"
    UNSPECIFIED = "UNSPECIFIED"


class OmImpact(StrEnum):
    YES = "YES"
    NO = "NO"


class PortfolioEvaluationStatus(StrEnum):
    COMPLETE = "COMPLETE"
    ANALYST_RESOLUTION_REQUIRED = (
        "ANALYST_RESOLUTION_REQUIRED"
    )


class SelectionSource(StrEnum):
    AUTO_COMPLETE_TIER = "AUTO_COMPLETE_TIER"
    AUTO_UNIQUE_BUDGET_FEASIBLE = (
        "AUTO_UNIQUE_BUDGET_FEASIBLE"
    )
    ANALYST_BOUNDARY_RESOLUTION = (
        "ANALYST_BOUNDARY_RESOLUTION"
    )


class PortfolioWarningCode(StrEnum):
    HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS = (
        "HIGHER_PRIORITY_FEASIBLE_PROJECT_REMAINS"
    )


# ---------------------------------------------------------------------------
# PRB scoring
# ---------------------------------------------------------------------------


class OfficialPrbComponents(StrictModel):
    strategic_alignment: int | float
    critical_asset: int | float
    community_consideration: int | float
    efficiency: int | float
    timeliness_readiness: int | float
    climate_resilience: int | float

    @field_validator("strategic_alignment")
    @classmethod
    def strategic_alignment_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=8,
            label="strategic_alignment",
        )

    @field_validator("critical_asset")
    @classmethod
    def critical_asset_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=8,
            label="critical_asset",
        )

    @field_validator("community_consideration")
    @classmethod
    def community_consideration_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=20,
            label="community_consideration",
        )

    @field_validator("efficiency")
    @classmethod
    def efficiency_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=20,
            label="efficiency",
        )

    @field_validator("timeliness_readiness")
    @classmethod
    def timeliness_readiness_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=24,
            label="timeliness_readiness",
        )

    @field_validator("climate_resilience")
    @classmethod
    def climate_resilience_valid(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=20,
            label="climate_resilience",
        )

    def grand_total(self) -> float:
        return sum(
            float(value)
            for value in (
                self.strategic_alignment,
                self.critical_asset,
                self.community_consideration,
                self.efficiency,
                self.timeliness_readiness,
                self.climate_resilience,
            )
        )


# ---------------------------------------------------------------------------
# Council District / O&M analyst-review context
# ---------------------------------------------------------------------------


class CouncilDistrictContext(StrictModel):
    assignment_type: CouncilDistrictAssignmentType

    @field_validator("assignment_type", mode="before")
    @classmethod
    def parse_assignment_type(
        cls,
        value,
    ):
        if isinstance(value, str):
            return CouncilDistrictAssignmentType(value)
        return value

    districts: list[
        Annotated[
            int,
            Field(
                strict=True,
                ge=1,
                le=10,
            ),
        ]
    ] = Field(
        max_length=10,
    )

    source_value: ShortText | None = None

    analyst_review_only: Literal[True]
    hard_portfolio_constraint: Literal[False]

    @model_validator(mode="after")
    def assignment_matches_districts(
        self,
    ) -> CouncilDistrictContext:
        if self.districts != sorted(
            set(self.districts)
        ):
            raise ValueError(
                "Council District values must "
                "be unique and sorted"
            )

        if (
            self.assignment_type
            == CouncilDistrictAssignmentType.SINGLE_DISTRICT
        ):
            if len(self.districts) != 1:
                raise ValueError(
                    "SINGLE_DISTRICT requires "
                    "exactly one district"
                )

        elif (
            self.assignment_type
            == CouncilDistrictAssignmentType.MULTI_DISTRICT
        ):
            if len(self.districts) < 2:
                raise ValueError(
                    "MULTI_DISTRICT requires "
                    "at least two districts"
                )

        else:
            if self.districts:
                raise ValueError(
                    "CITYWIDE and UNSPECIFIED "
                    "must not invent district IDs"
                )

        return self


class OmImpactContext(StrictModel):
    value: OmImpact

    @field_validator("value", mode="before")
    @classmethod
    def parse_om_impact(
        cls,
        value,
    ):
        if isinstance(value, str):
            return OmImpact(value)
        return value

    analyst_review_only: Literal[True]
    hard_portfolio_constraint: Literal[False]
    additional_score_preference_authorized: Literal[False]


# ---------------------------------------------------------------------------
# Catalog v2
# ---------------------------------------------------------------------------


class CrossCategoryRuntimeProject(StrictModel):
    decision_unit_id: DecisionUnitId
    canonical_project_id: ProjectId | None = None

    governed_name: ShortText

    presentation_category: RuntimePresentationCategory

    @field_validator("presentation_category", mode="before")
    @classmethod
    def parse_presentation_category(
        cls,
        value,
    ):
        if isinstance(value, str):
            return RuntimePresentationCategory(value)
        return value

    source_department: ShortText
    source_domain: ShortText

    model_request_dollars: PositiveWholeDollars
    model_request_authority: StableIdentifier
    model_request_authority_source_id: StableIdentifier
    request_version_conflict: bool = Field(
        strict=True
    )

    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    is_tied: bool = Field(
        strict=True
    )

    tie_group_size: TieGroupSize

    display_order_within_tie: DisplayOrderWithinTie

    display_tiebreak_has_analytical_meaning: Literal[
        False
    ]

    prb_components: OfficialPrbComponents

    council_district: CouncilDistrictContext
    om_impact: OmImpactContext

    provenance_refs: list[
        StableIdentifier
    ] = Field(
        min_length=1,
    )

    @field_validator("funding_priority_score")
    @classmethod
    def funding_priority_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )

    @field_validator("provenance_refs")
    @classmethod
    def provenance_is_unique(
        cls,
        value: list[str],
    ) -> list[str]:
        if value != sorted(
            set(value)
        ):
            raise ValueError(
                "provenance_refs must be "
                "unique and sorted"
            )

        return value

    @model_validator(mode="after")
    def project_semantics(
        self,
    ) -> CrossCategoryRuntimeProject:
        if (
            self.presentation_category
            == RuntimePresentationCategory.WATERSHED
            and self.canonical_project_id is None
        ):
            raise ValueError(
                "Watershed runtime projects "
                "require canonical_project_id"
            )

        if (
            self.presentation_category
            != RuntimePresentationCategory.WATERSHED
            and self.canonical_project_id is not None
        ):
            raise ValueError(
                "Non-Watershed runtime projects "
                "must not fabricate "
                "canonical_project_id"
            )

        expected_tied = (
            self.tie_group_size > 1
        )

        if self.is_tied is not expected_tied:
            raise ValueError(
                "is_tied must agree with "
                "tie_group_size"
            )

        if (
            self.display_order_within_tie
            > self.tie_group_size
        ):
            raise ValueError(
                "display_order_within_tie "
                "cannot exceed tie_group_size"
            )

        component_total = (
            self.prb_components.grand_total()
        )

        if (
            component_total
            != float(
                self.funding_priority_score
            )
        ):
            raise ValueError(
                "official PRB components must "
                "reproduce Funding Priority Score"
            )

        return self


class RuntimeCategoryCounts(StrictModel):
    transportation: Literal[9]
    parks_open_space: Literal[22]
    watershed: Literal[37]
    community_facilities: Literal[38]


class CrossCategoryRuntimeCatalog(StrictModel):
    contract_version: Literal[
        CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
    ]

    data_version: DataVersion

    historical_decision_snapshot_date: Literal[
        "2026-01-21"
    ]

    model_scope: Literal[
        CROSS_CATEGORY_RUNTIME_MODEL_SCOPE
    ]

    methodology_name: Literal[
        CROSS_CATEGORY_PORTFOLIO_METHODOLOGY
    ]

    cross_category_ranking_authorized: Literal[
        True
    ]

    portfolio_selection_authorized: Literal[
        True
    ]

    runtime_integration_authorized: bool = Field(
        strict=True
    )

    project_count: Literal[
        CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ]

    governed_request_total_dollars: Literal[
        CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
    ]

    category_counts: RuntimeCategoryCounts

    unique_funding_priority_score_count: Literal[
        CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT
    ]

    tied_score_group_count: Literal[
        CROSS_CATEGORY_TIED_SCORE_GROUP_COUNT
    ]

    projects_in_tied_score_groups: Literal[
        CROSS_CATEGORY_PROJECTS_IN_TIES
    ]

    projects: list[
        CrossCategoryRuntimeProject
    ] = Field(
        min_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    @model_validator(mode="after")
    def catalog_reconciles(
        self,
    ) -> CrossCategoryRuntimeCatalog:
        ids = [
            project.decision_unit_id
            for project in self.projects
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "decision_unit_id values "
                "must be unique"
            )

        if (
            sum(
                project.model_request_dollars
                for project in self.projects
            )
            != CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
        ):
            raise ValueError(
                "catalog requests must reconcile "
                "to $1,973,520,000"
            )

        category_counts = {
            RuntimePresentationCategory.TRANSPORTATION:
                0,
            RuntimePresentationCategory.PARKS_OPEN_SPACE:
                0,
            RuntimePresentationCategory.WATERSHED:
                0,
            RuntimePresentationCategory.COMMUNITY_FACILITIES:
                0,
        }

        for project in self.projects:
            category_counts[
                project.presentation_category
            ] += 1

        if category_counts != {
            RuntimePresentationCategory.TRANSPORTATION:
                9,
            RuntimePresentationCategory.PARKS_OPEN_SPACE:
                22,
            RuntimePresentationCategory.WATERSHED:
                37,
            RuntimePresentationCategory.COMMUNITY_FACILITIES:
                38,
        }:
            raise ValueError(
                "runtime project category "
                "counts must equal 9/22/37/38"
            )

        unique_scores = {
            float(
                project.funding_priority_score
            )
            for project in self.projects
        }

        if (
            len(unique_scores)
            != CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT
        ):
            raise ValueError(
                "catalog must preserve "
                "35 unique Funding Priority scores"
            )

        tied_projects = [
            project
            for project in self.projects
            if project.is_tied
        ]

        if (
            len(tied_projects)
            != CROSS_CATEGORY_PROJECTS_IN_TIES
        ):
            raise ValueError(
                "catalog must preserve "
                "95 projects participating in ties"
            )

        tied_scores = {
            float(
                project.funding_priority_score
            )
            for project in tied_projects
        }

        if (
            len(tied_scores)
            != CROSS_CATEGORY_TIED_SCORE_GROUP_COUNT
        ):
            raise ValueError(
                "catalog must preserve "
                "24 tied score groups"
            )

        return self


# ---------------------------------------------------------------------------
# Funding Plan v2 request contracts
# ---------------------------------------------------------------------------


class BoundaryResolutionInput(StrictModel):
    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    selected_decision_unit_ids: list[
        DecisionUnitId
    ] = Field(
        default_factory=list,
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    advance_with_feasible_same_tier_project_acknowledged: bool = (
        Field(
            strict=True
        )
    )

    @field_validator("funding_priority_score")
    @classmethod
    def boundary_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )

    @field_validator("selected_decision_unit_ids")
    @classmethod
    def selected_ids_are_unique(
        cls,
        value: list[str],
    ) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError(
                "boundary selected IDs "
                "must be unique"
            )

        return sorted(value)


class CrossCategoryPlanInput(StrictModel):
    contract_version: Literal[
        CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    ]

    data_version: DataVersion

    available_budget_dollars: (
        CrossCategoryScenarioBudgetDollars
    )

    boundary_resolutions: list[
        BoundaryResolutionInput
    ] = Field(
        default_factory=list,
        max_length=(
            CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT
        ),
    )

    expected_fingerprint: Sha256 | None = None

    @model_validator(mode="after")
    def boundary_resolutions_are_unique(
        self,
    ) -> CrossCategoryPlanInput:
        keys = [
            (
                float(
                    resolution.funding_priority_score
                ),
                resolution.funding_priority_rank,
            )
            for resolution
            in self.boundary_resolutions
        ]

        if len(keys) != len(set(keys)):
            raise ValueError(
                "boundary resolutions must "
                "be unique by substantive tier"
            )

        return self


# ---------------------------------------------------------------------------
# Funding Plan v2 result contracts
# ---------------------------------------------------------------------------


class SelectedProjectResult(StrictModel):
    decision_unit_id: DecisionUnitId

    model_request_dollars: PositiveWholeDollars

    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    selection_source: SelectionSource

    @field_validator("selection_source", mode="before")
    @classmethod
    def parse_selection_source(
        cls,
        value,
    ):
        if isinstance(value, str):
            return SelectionSource(value)
        return value

    @field_validator("funding_priority_score")
    @classmethod
    def selected_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )


class BoundaryCandidateResult(StrictModel):
    decision_unit_id: DecisionUnitId

    model_request_dollars: PositiveWholeDollars

    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    individually_budget_feasible: bool = Field(
        strict=True
    )

    @field_validator("funding_priority_score")
    @classmethod
    def candidate_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )


class BoundaryTierResult(StrictModel):
    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    remaining_budget_before_tier_dollars: WholeDollars

    full_tier_request_dollars: PositiveWholeDollars

    candidates: list[
        BoundaryCandidateResult
    ] = Field(
        min_length=1,
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    @field_validator("funding_priority_score")
    @classmethod
    def tier_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )

    @model_validator(mode="after")
    def candidates_match_tier(
        self,
    ) -> BoundaryTierResult:
        ids = [
            candidate.decision_unit_id
            for candidate in self.candidates
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "boundary candidate IDs "
                "must be unique"
            )

        for candidate in self.candidates:
            if (
                float(
                    candidate.funding_priority_score
                )
                != float(
                    self.funding_priority_score
                )
                or candidate.funding_priority_rank
                != self.funding_priority_rank
            ):
                raise ValueError(
                    "boundary candidates must "
                    "belong to the same "
                    "substantive priority tier"
                )

        if (
            sum(
                candidate.model_request_dollars
                for candidate in self.candidates
            )
            != self.full_tier_request_dollars
        ):
            raise ValueError(
                "boundary candidate requests "
                "must reproduce tier request total"
            )

        return self


class PortfolioWarning(StrictModel):
    warning_code: PortfolioWarningCode

    @field_validator("warning_code", mode="before")
    @classmethod
    def parse_warning_code(
        cls,
        value,
    ):
        if isinstance(value, str):
            return PortfolioWarningCode(value)
        return value

    message: NonEmptyString

    decision_unit_ids: list[
        DecisionUnitId
    ] = Field(
        min_length=1,
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    @field_validator("decision_unit_ids")
    @classmethod
    def warning_ids_are_unique(
        cls,
        value: list[str],
    ) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError(
                "warning decision-unit IDs "
                "must be unique"
            )

        return sorted(value)


class AppliedAnalystOverride(StrictModel):
    funding_priority_score: FundingPriorityScore
    funding_priority_rank: FundingPriorityRank

    acknowledged: Literal[True]

    decision_unit_ids_left_feasible: list[
        DecisionUnitId
    ] = Field(
        min_length=1,
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    @field_validator("funding_priority_score")
    @classmethod
    def override_score_is_half_point(
        cls,
        value: int | float,
    ) -> int | float:
        return _validate_half_point_score(
            value,
            minimum=0,
            maximum=100,
            label="funding_priority_score",
        )

    @field_validator("decision_unit_ids_left_feasible")
    @classmethod
    def override_ids_are_unique(
        cls,
        value: list[str],
    ) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError(
                "override project IDs "
                "must be unique"
            )

        return sorted(value)


class CrossCategoryPlanResult(StrictModel):
    contract_version: Literal[
        CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
    ]

    data_version: DataVersion

    status: PortfolioEvaluationStatus

    @field_validator("status", mode="before")
    @classmethod
    def parse_evaluation_status(
        cls,
        value,
    ):
        if isinstance(value, str):
            return PortfolioEvaluationStatus(value)
        return value

    available_budget_dollars: (
        CrossCategoryScenarioBudgetDollars
    )

    selected_projects: list[
        SelectedProjectResult
    ] = Field(
        max_length=(
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
        ),
    )

    included_total_dollars: WholeDollars
    remainder_dollars: WholeDollars

    unresolved_boundary: (
        BoundaryTierResult | None
    ) = None

    warnings: list[
        PortfolioWarning
    ] = Field(
        max_length=(
            CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT
        ),
    )

    applied_analyst_overrides: list[
        AppliedAnalystOverride
    ] = Field(
        max_length=(
            CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT
        ),
    )

    plan_fingerprint: Sha256

    @model_validator(mode="after")
    def result_reconciles(
        self,
    ) -> CrossCategoryPlanResult:
        ids = [
            project.decision_unit_id
            for project in self.selected_projects
        ]

        if len(ids) != len(set(ids)):
            raise ValueError(
                "selected project IDs "
                "must be unique"
            )

        selected_total = sum(
            project.model_request_dollars
            for project in self.selected_projects
        )

        if (
            selected_total
            != self.included_total_dollars
        ):
            raise ValueError(
                "selected project requests "
                "must reproduce included total"
            )

        if (
            self.included_total_dollars
            > self.available_budget_dollars
        ):
            raise ValueError(
                "portfolio result cannot "
                "exceed Available Project Budget"
            )

        expected_remainder = (
            self.available_budget_dollars
            - self.included_total_dollars
        )

        if (
            self.remainder_dollars
            != expected_remainder
        ):
            raise ValueError(
                "remainder must equal budget "
                "minus included total"
            )

        if (
            self.status
            == PortfolioEvaluationStatus.ANALYST_RESOLUTION_REQUIRED
        ):
            if self.unresolved_boundary is None:
                raise ValueError(
                    "ANALYST_RESOLUTION_REQUIRED "
                    "requires unresolved_boundary"
                )

        elif self.unresolved_boundary is not None:
            raise ValueError(
                "COMPLETE results cannot retain "
                "an unresolved boundary"
            )

        return self