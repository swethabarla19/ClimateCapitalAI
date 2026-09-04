"""Strict contract for the M3.5 governed cross-category PRB universe."""

from __future__ import annotations

from collections import Counter
from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator, model_validator

from .common import (
    DataVersion,
    IsoDate,
    ProjectId,
    ShortText,
    StableIdentifier,
    StrictModel,
    WholeDollars,
)
from .versions import (
    CROSS_CATEGORY_ANALYTICAL_PROJECT_COUNT,
    CROSS_CATEGORY_NOT_SCORED_COUNT,
    CROSS_CATEGORY_PROGRAM_ALLOCATION_COUNT,
    CROSS_CATEGORY_PROGRAM_BUCKET_COUNT,
    CROSS_CATEGORY_SOURCE_ROW_COUNT,
    CROSS_CATEGORY_UNIVERSE_CONTRACT_VERSION,
)


SourceId = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$"),
]

PrbScore = Annotated[int | float, Field(ge=0, le=100)]


class AnalyticalUnitType(StrEnum):
    ANALYTICAL_PROJECT = "ANALYTICAL_PROJECT"
    PROGRAM_BUCKET = "PROGRAM_BUCKET"
    PROGRAM_ALLOCATION = "PROGRAM_ALLOCATION"
    NOT_SCORED = "NOT_SCORED"


class PresentationCategory(StrEnum):
    TRANSPORTATION = "Transportation"
    PARKS_OPEN_SPACE = "Parks & Open Space"
    WATERSHED = "Watershed"
    COMMUNITY_FACILITIES = "Community Facilities"
    AFFORDABLE_HOUSING = "Affordable Housing"


class EvidenceFeasibilityStatus(StrEnum):
    NOT_EVALUATED = "NOT_EVALUATED"
    PARTIAL = "PARTIAL"
    FEASIBLE = "FEASIBLE"
    INFEASIBLE = "INFEASIBLE"


class ExclusionReason(StrEnum):
    PROGRAM_BUCKET = "PROGRAM_BUCKET"
    PROGRAM_ALLOCATION = "PROGRAM_ALLOCATION"
    PRB_NOT_SCORED = "PRB_NOT_SCORED"


class SourceVersionValue(StrictModel):
    """A source-specific value preserved without overwriting another vintage."""

    source_id: SourceId
    source_date: IsoDate
    source_name: ShortText | None = None
    department_request_dollars: WholeDollars | None = None
    historical_recommendation_amount_dollars: WholeDollars | None = None
    prb_score: PrbScore | None = None
    notes: ShortText | None = None

    @field_validator("prb_score")
    @classmethod
    def score_uses_half_points(cls, value: int | float | None) -> int | float | None:
        if value is not None and float(value) * 2 % 1 != 0:
            raise ValueError("prb_score must use whole- or half-point increments")
        return value

    @model_validator(mode="after")
    def contains_versioned_value(self) -> SourceVersionValue:
        values = (
            self.source_name,
            self.department_request_dollars,
            self.historical_recommendation_amount_dollars,
            self.prb_score,
            self.notes,
        )
        if all(value is None for value in values):
            raise ValueError("source version must preserve at least one value")
        return self


class CrossCategoryDecisionUnit(StrictModel):
    """One governed PRB source row from the January 21 historical universe."""

    decision_unit_id: StableIdentifier
    canonical_project_id: ProjectId | None = None

    source_name: ShortText
    source_department: ShortText
    source_domain: ShortText
    presentation_category: PresentationCategory

    analytical_unit_type: AnalyticalUnitType
    analytical_unit: bool

    prb_scored: bool
    prb_score: PrbScore | None

    department_request_dollars: WholeDollars | None
    historical_recommendation_amount_dollars: WholeDollars | None

    evidence_feasibility_status: EvidenceFeasibilityStatus
    model_eligible: bool
    exclusion_reason: ExclusionReason | None

    source_ids: list[SourceId] = Field(min_length=1)
    source_versions: list[SourceVersionValue] = Field(min_length=1)
    source_conflict_flag: bool

    @field_validator("presentation_category", mode="before")
    @classmethod
    def parse_presentation_category(cls, value):
        if isinstance(value, str):
            return PresentationCategory(value)
        return value

    @field_validator("analytical_unit_type", mode="before")
    @classmethod
    def parse_analytical_unit_type(cls, value):
        if isinstance(value, str):
            return AnalyticalUnitType(value)
        return value

    @field_validator("evidence_feasibility_status", mode="before")
    @classmethod
    def parse_evidence_feasibility_status(cls, value):
        if isinstance(value, str):
            return EvidenceFeasibilityStatus(value)
        return value

    @field_validator("exclusion_reason", mode="before")
    @classmethod
    def parse_exclusion_reason(cls, value):
        if isinstance(value, str):
            return ExclusionReason(value)
        return value

    @field_validator("prb_score")
    @classmethod
    def score_uses_half_points(cls, value: int | float | None) -> int | float | None:
        if value is not None and float(value) * 2 % 1 != 0:
            raise ValueError("prb_score must use whole- or half-point increments")
        return value

    @field_validator("source_ids")
    @classmethod
    def source_ids_are_unique(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("source_ids must be unique")
        return value

    @model_validator(mode="after")
    def classification_semantics(self) -> CrossCategoryDecisionUnit:
        is_project = self.analytical_unit_type == AnalyticalUnitType.ANALYTICAL_PROJECT

        if self.analytical_unit != is_project:
            raise ValueError(
                "analytical_unit must be true only for ANALYTICAL_PROJECT"
            )

        scored_types = {
            AnalyticalUnitType.ANALYTICAL_PROJECT,
            AnalyticalUnitType.PROGRAM_BUCKET,
        }
        should_be_scored = self.analytical_unit_type in scored_types

        if self.prb_scored != should_be_scored:
            raise ValueError(
                "prb_scored must match the governed analytical-unit classification"
            )

        if should_be_scored and self.prb_score is None:
            raise ValueError("scored decision units require prb_score")

        if not should_be_scored and self.prb_score is not None:
            raise ValueError("unscored decision units require null prb_score")

        expected_exclusion = {
            AnalyticalUnitType.ANALYTICAL_PROJECT: None,
            AnalyticalUnitType.PROGRAM_BUCKET: ExclusionReason.PROGRAM_BUCKET,
            AnalyticalUnitType.PROGRAM_ALLOCATION: ExclusionReason.PROGRAM_ALLOCATION,
            AnalyticalUnitType.NOT_SCORED: ExclusionReason.PRB_NOT_SCORED,
        }[self.analytical_unit_type]

        if self.exclusion_reason != expected_exclusion:
            raise ValueError(
                "exclusion_reason must match the governed analytical-unit type"
            )

        if not is_project and self.model_eligible:
            raise ValueError("non-project decision units cannot be model eligible")

        if (
            self.presentation_category == PresentationCategory.WATERSHED
            and is_project
            and self.canonical_project_id is None
        ):
            raise ValueError(
                "Watershed analytical projects require the canonical subproject ID"
            )

        if self.source_conflict_flag and len(self.source_versions) < 2:
            raise ValueError(
                "source_conflict_flag requires at least two preserved source versions"
            )

        version_source_ids = {version.source_id for version in self.source_versions}
        if not version_source_ids.issubset(set(self.source_ids)):
            raise ValueError(
                "every source_version source_id must also appear in source_ids"
            )

        return self


class SourceRowCounts(StrictModel):
    transportation: Literal[18]
    parks_open_space: Literal[34]
    watershed: Literal[42]
    community_facilities: Literal[41]
    affordable_housing: Literal[1]


class AnalyticalProjectCounts(StrictModel):
    transportation: Literal[9]
    parks_open_space: Literal[22]
    watershed: Literal[37]
    community_facilities: Literal[38]


class CrossCategoryUniverseSummary(StrictModel):
    source_row_count: Literal[CROSS_CATEGORY_SOURCE_ROW_COUNT]
    analytical_project_count: Literal[CROSS_CATEGORY_ANALYTICAL_PROJECT_COUNT]
    program_bucket_count: Literal[CROSS_CATEGORY_PROGRAM_BUCKET_COUNT]
    program_allocation_count: Literal[CROSS_CATEGORY_PROGRAM_ALLOCATION_COUNT]
    not_scored_count: Literal[CROSS_CATEGORY_NOT_SCORED_COUNT]

    source_rows_by_presentation_category: SourceRowCounts
    analytical_projects_by_presentation_category: AnalyticalProjectCounts


class CrossCategoryUniverseArtifact(StrictModel):
    """Governed 136-row PRB source universe frozen to January 21, 2026."""

    contract_version: Literal[CROSS_CATEGORY_UNIVERSE_CONTRACT_VERSION]
    data_version: DataVersion

    governance_checkpoint: Literal["M3.5"]
    governance_status: Literal["APPROVED"]
    historical_decision_snapshot_date: Literal["2026-01-21"]

    summary: CrossCategoryUniverseSummary

    decision_units: list[CrossCategoryDecisionUnit] = Field(
        min_length=CROSS_CATEGORY_SOURCE_ROW_COUNT,
        max_length=CROSS_CATEGORY_SOURCE_ROW_COUNT,
    )

    @model_validator(mode="after")
    def exact_governed_universe(self) -> CrossCategoryUniverseArtifact:
        ids = [unit.decision_unit_id for unit in self.decision_units]
        if len(ids) != len(set(ids)):
            raise ValueError("decision_unit_id values must be unique")

        classification_counts = Counter(
            unit.analytical_unit_type for unit in self.decision_units
        )
        expected_classification_counts = {
            AnalyticalUnitType.ANALYTICAL_PROJECT:
                CROSS_CATEGORY_ANALYTICAL_PROJECT_COUNT,
            AnalyticalUnitType.PROGRAM_BUCKET:
                CROSS_CATEGORY_PROGRAM_BUCKET_COUNT,
            AnalyticalUnitType.PROGRAM_ALLOCATION:
                CROSS_CATEGORY_PROGRAM_ALLOCATION_COUNT,
            AnalyticalUnitType.NOT_SCORED:
                CROSS_CATEGORY_NOT_SCORED_COUNT,
        }
        if classification_counts != expected_classification_counts:
            raise ValueError(
                "decision-unit classification counts must match the M3.5 lock"
            )

        source_row_counts = Counter(
            unit.presentation_category for unit in self.decision_units
        )
        expected_source_row_counts = {
            PresentationCategory.TRANSPORTATION: 18,
            PresentationCategory.PARKS_OPEN_SPACE: 34,
            PresentationCategory.WATERSHED: 42,
            PresentationCategory.COMMUNITY_FACILITIES: 41,
            PresentationCategory.AFFORDABLE_HOUSING: 1,
        }
        if source_row_counts != expected_source_row_counts:
            raise ValueError(
                "presentation-category source-row counts must match the M3.5 lock"
            )

        analytical_counts = Counter(
            unit.presentation_category
            for unit in self.decision_units
            if unit.analytical_unit_type == AnalyticalUnitType.ANALYTICAL_PROJECT
        )
        expected_analytical_counts = {
            PresentationCategory.TRANSPORTATION: 9,
            PresentationCategory.PARKS_OPEN_SPACE: 22,
            PresentationCategory.WATERSHED: 37,
            PresentationCategory.COMMUNITY_FACILITIES: 38,
        }
        if analytical_counts != expected_analytical_counts:
            raise ValueError(
                "analytical-project presentation counts must match the M3.5 lock"
            )

        not_scored_names = {
            unit.source_name
            for unit in self.decision_units
            if unit.analytical_unit_type == AnalyticalUnitType.NOT_SCORED
        }
        expected_not_scored_names = {
            "Neighborhood Partnering Program",
            "Open Space Acquisition",
            "Affordable Housing",
        }
        if not_scored_names != expected_not_scored_names:
            raise ValueError(
                "NOT_SCORED quarantine must contain the exact M3.5 records"
            )

        return self
