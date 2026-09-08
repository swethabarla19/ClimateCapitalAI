"""Strict contracts for bounded Gemini explanation requests and results."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator, model_validator

from .common import DataVersion, NonEmptyString, StableIdentifier, StrictModel
from .cross_category_runtime import CrossCategoryPlanInput


GEMINI_EXPLANATION_REQUEST_CONTRACT_VERSION = (
    "p0-gemini-explanation-request/1.0.0"
)
GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION = (
    "p0-gemini-explanation-result/1.0.0"
)

MAX_GEMINI_QUESTION_CHARACTERS = 2_000
MAX_GEMINI_PROJECT_IDS = 2
MAX_GEMINI_HISTORY_MESSAGES = 6
MAX_GEMINI_HISTORY_MESSAGE_CHARACTERS = 1_000
MAX_GEMINI_HISTORY_CHARACTERS = 6_000

BoundedQuestion = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=MAX_GEMINI_QUESTION_CHARACTERS,
        strip_whitespace=True,
    ),
]

BoundedHistoryContent = Annotated[
    str,
    StringConstraints(
        min_length=1,
        max_length=MAX_GEMINI_HISTORY_MESSAGE_CHARACTERS,
        strip_whitespace=True,
    ),
]


class GeminiSurface(StrEnum):
    PROJECT = "PROJECT"
    FUNDING_PLAN = "FUNDING_PLAN"
    BOUNDARY = "BOUNDARY"
    BENCHMARK = "BENCHMARK"
    METHODOLOGY = "METHODOLOGY"


class GeminiHistoryRole(StrEnum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class GeminiHistoryMessage(StrictModel):
    role: GeminiHistoryRole
    content: BoundedHistoryContent

    @field_validator("role", mode="before")
    @classmethod
    def parse_role(cls, value):
        if isinstance(value, str):
            return GeminiHistoryRole(value)
        return value


class GeminiExplanationRequest(StrictModel):
    contract_version: Literal[
        GEMINI_EXPLANATION_REQUEST_CONTRACT_VERSION
    ]
    data_version: DataVersion
    release_id: Annotated[
        str,
        StringConstraints(min_length=1, max_length=200),
    ]
    surface: GeminiSurface
    question: BoundedQuestion
    project_ids: list[StableIdentifier] = Field(
        default_factory=list,
        max_length=MAX_GEMINI_PROJECT_IDS,
    )
    funding_plan_input: CrossCategoryPlanInput | None = None
    history: list[GeminiHistoryMessage] = Field(
        default_factory=list,
        max_length=MAX_GEMINI_HISTORY_MESSAGES,
    )

    @field_validator("surface", mode="before")
    @classmethod
    def parse_surface(cls, value):
        if isinstance(value, str):
            return GeminiSurface(value)
        return value

    @field_validator("project_ids")
    @classmethod
    def project_ids_are_unique(
        cls,
        value: list[str],
    ) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("project_ids must be unique")
        return value

    @model_validator(mode="after")
    def surface_context_is_bounded(
        self,
    ) -> GeminiExplanationRequest:
        if self.surface == GeminiSurface.PROJECT:
            if not 1 <= len(self.project_ids) <= MAX_GEMINI_PROJECT_IDS:
                raise ValueError("PROJECT requires one or two project_ids")
            if self.funding_plan_input is not None:
                raise ValueError("PROJECT does not accept funding_plan_input")
        elif self.surface in {
            GeminiSurface.FUNDING_PLAN,
            GeminiSurface.BOUNDARY,
        }:
            if self.funding_plan_input is None:
                raise ValueError(
                    f"{self.surface} requires funding_plan_input"
                )
            if self.project_ids:
                raise ValueError(
                    f"{self.surface} does not accept project_ids"
                )
        else:
            if self.project_ids or self.funding_plan_input is not None:
                raise ValueError(
                    f"{self.surface} does not accept project or plan handles"
                )

        if (
            self.funding_plan_input is not None
            and self.funding_plan_input.data_version != self.data_version
        ):
            raise ValueError(
                "funding_plan_input data_version must match request data_version"
            )

        if len(self.history) % 2 != 0:
            raise ValueError("history must contain complete prior exchanges")
        for index, message in enumerate(self.history):
            expected = (
                GeminiHistoryRole.USER
                if index % 2 == 0
                else GeminiHistoryRole.ASSISTANT
            )
            if message.role != expected:
                raise ValueError("history must alternate USER then ASSISTANT")
        if sum(len(message.content) for message in self.history) > (
            MAX_GEMINI_HISTORY_CHARACTERS
        ):
            raise ValueError("history exceeds the total character limit")

        return self


class GeminiExplanationStatus(StrEnum):
    COMPLETE = "COMPLETE"
    INSUFFICIENT_CONTEXT = "INSUFFICIENT_CONTEXT"
    SAFETY_BLOCKED = "SAFETY_BLOCKED"


class GeminiEvidenceSource(StrEnum):
    RUNTIME_CATALOG = "RUNTIME_CATALOG"
    FUNDING_PLAN_EVALUATOR = "FUNDING_PLAN_EVALUATOR"
    HISTORICAL_BENCHMARK = "HISTORICAL_BENCHMARK"
    GOVERNED_METHODOLOGY = "GOVERNED_METHODOLOGY"


class GeminiGroundingMetadata(StrictModel):
    snapshot_date: Literal["2026-01-21"]
    surface: GeminiSurface
    decision_unit_ids: list[StableIdentifier] = Field(max_length=106)
    plan_fingerprint: Annotated[
        str,
        StringConstraints(pattern=r"^[0-9a-f]{64}$"),
    ] | None = None
    benchmark_effective_date: Literal["2026-01-21"] | None = None
    evidence_sources: list[GeminiEvidenceSource] = Field(
        min_length=1,
        max_length=4,
    )

    @model_validator(mode="after")
    def grounding_metadata_is_consistent(
        self,
    ) -> GeminiGroundingMetadata:
        if len(self.decision_unit_ids) != len(set(self.decision_unit_ids)):
            raise ValueError("grounding decision_unit_ids must be unique")
        if len(self.evidence_sources) != len(set(self.evidence_sources)):
            raise ValueError("grounding evidence_sources must be unique")
        if (
            self.benchmark_effective_date is not None
            and self.surface != GeminiSurface.BENCHMARK
        ):
            raise ValueError("benchmark_effective_date is BENCHMARK-only")
        if (
            self.plan_fingerprint is not None
            and self.surface
            not in {GeminiSurface.FUNDING_PLAN, GeminiSurface.BOUNDARY}
        ):
            raise ValueError("plan_fingerprint is plan-surface-only")
        return self


class GeminiExplanationResult(StrictModel):
    contract_version: Literal[
        GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION
    ]
    data_version: DataVersion
    release_id: Annotated[
        str,
        StringConstraints(min_length=1, max_length=200),
    ]
    request_id: Annotated[
        str,
        StringConstraints(
            pattern=(
                r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-"
                r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
            )
        ),
    ]
    status: GeminiExplanationStatus
    answer: NonEmptyString
    provider: Literal["vertex_ai"]
    model: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    grounding: GeminiGroundingMetadata
    warnings: list[NonEmptyString] = Field(default_factory=list, max_length=10)


class GeminiProviderResponse(StrictModel):
    """Private structured generation schema; never returned directly."""

    answer: Annotated[
        str,
        StringConstraints(min_length=1, max_length=4_000, strip_whitespace=True),
    ]
    insufficient_context: bool = Field(strict=True)
