"""Grounded Gemini explain request and structured response contracts."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints, model_validator

from .common import (
    Count,
    DataVersion,
    NonEmptyString,
    ProjectId,
    StableIdentifier,
    StrictModel,
)
from .plans import PlanInput
from .versions import GEMINI_EXPLAIN_CONTRACT_VERSION


class GeminiExpectedFingerprints(StrictModel):
    current: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")
    reference: str | None = Field(default=None, pattern=r"^[0-9a-f]{64}$")


class GeminiExplainRequest(StrictModel):
    contract_version: Literal[GEMINI_EXPLAIN_CONTRACT_VERSION]
    data_version: DataVersion
    context_type: Literal[
        "PROJECT",
        "PLAN",
        "SCENARIO_COMPARISON",
        "BENCHMARK",
        "METHODOLOGY",
        "PROVENANCE",
    ]
    project_ids: list[ProjectId] = Field(default_factory=list, max_length=12)
    current_plan: PlanInput | None = None
    reference_plan: PlanInput | None = None
    expected_fingerprints: GeminiExpectedFingerprints | None = None
    user_question: Annotated[str, StringConstraints(min_length=1, max_length=1_000)]

    @model_validator(mode="after")
    def context_requires_minimum_references(self) -> GeminiExplainRequest:
        if len(self.project_ids) != len(set(self.project_ids)):
            raise ValueError("project IDs must be unique")
        if self.context_type == "PROJECT" and len(self.project_ids) != 1:
            raise ValueError("PROJECT context requires exactly one project ID")
        if self.context_type == "PLAN" and self.current_plan is None:
            raise ValueError("PLAN context requires a current plan input")
        if self.context_type == "SCENARIO_COMPARISON" and (
            self.current_plan is None or self.reference_plan is None
        ):
            raise ValueError("SCENARIO_COMPARISON requires current and reference plan inputs")
        if self.reference_plan is not None and self.current_plan is None:
            raise ValueError("a reference plan cannot be supplied without a current plan")
        for label, plan in (
            ("current", self.current_plan),
            ("reference", self.reference_plan),
        ):
            if plan is not None and plan.data_version != self.data_version:
                raise ValueError(f"{label} plan data version must match Gemini request")
        if self.expected_fingerprints is not None:
            for label, plan in (
                ("current", self.current_plan),
                ("reference", self.reference_plan),
            ):
                expected = getattr(self.expected_fingerprints, label)
                if expected is not None and plan is None:
                    raise ValueError(f"{label} fingerprint requires a {label} plan")
                if (
                    expected is not None
                    and plan is not None
                    and plan.expected_fingerprint is not None
                    and expected != plan.expected_fingerprint
                ):
                    raise ValueError(
                        f"{label} expected fingerprints disagree across request fields"
                    )
        return self


class GeminiCitation(StrictModel):
    citation_id: StableIdentifier
    source_id: StableIdentifier
    evidence_id: StableIdentifier | None = None


class GeminiModelIdentity(StrictModel):
    model: Literal["gemini-3.6-flash"]
    location: Literal["global"]
    access_tier: Literal["STANDARD_ON_DEMAND"]
    thinking_level: Literal["MINIMAL"]


class GeminiUsage(StrictModel):
    input_tokens: Count
    visible_output_tokens: Count = Field(le=400)
    reasoning_tokens: Count | None = None
    total_tokens: Count

    @model_validator(mode="after")
    def token_total_reconciles(self) -> GeminiUsage:
        expected = self.input_tokens + self.visible_output_tokens + (self.reasoning_tokens or 0)
        if self.total_tokens != expected:
            raise ValueError("provider token counts must reconcile")
        return self


class GeminiExplainResponse(StrictModel):
    contract_version: Literal[GEMINI_EXPLAIN_CONTRACT_VERSION]
    data_version: DataVersion
    status: Literal["ANSWER", "REFUSAL"]
    sanitized_visible_text: Annotated[str, StringConstraints(min_length=1, max_length=8_000)]
    citations: list[GeminiCitation] = Field(max_length=30)
    limitations: list[NonEmptyString] = Field(min_length=1, max_length=20)
    model_identity: GeminiModelIdentity
    usage: GeminiUsage | None = None
    mutates_state: Literal[False]

    @model_validator(mode="after")
    def refusal_has_no_citations(self) -> GeminiExplainResponse:
        if self.status == "REFUSAL" and self.citations:
            raise ValueError("bounded refusals cannot assert evidence citations")
        return self


class GeminiGroundingReference(StrictModel):
    reference_id: StableIdentifier
    source_ids: list[StableIdentifier]
    exact_numeric_strings: list[str]
    public_text: NonEmptyString


class GeminiGroundingPackage(StrictModel):
    contract_version: Literal[GEMINI_EXPLAIN_CONTRACT_VERSION]
    data_version: DataVersion
    context_type: Literal[
        "PROJECT",
        "PLAN",
        "SCENARIO_COMPARISON",
        "BENCHMARK",
        "METHODOLOGY",
        "PROVENANCE",
    ]
    methodology_constraints: list[NonEmptyString] = Field(min_length=1)
    references: list[GeminiGroundingReference] = Field(min_length=1)
    bounded_user_question: Annotated[str, StringConstraints(min_length=1, max_length=1_000)]
    constructed_input_token_limit: Literal[2_000]
    benchmark_data_included: bool = Field(strict=True)

    @model_validator(mode="after")
    def benchmark_data_is_context_scoped(self) -> GeminiGroundingPackage:
        if self.benchmark_data_included != (self.context_type == "BENCHMARK"):
            raise ValueError("benchmark grounding is permitted only for BENCHMARK context")
        return self
