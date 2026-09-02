"""Funding Plan request, result, and comparison contracts (no plan engine)."""

from __future__ import annotations

from typing import Literal

from pydantic import Field, model_validator

from .artifacts import CatalogArtifact, PublishedCountValue, PublishedMoneyValue
from .common import (
    Count,
    DataVersion,
    NonEmptyString,
    PositiveWholeDollars,
    ProjectId,
    ScenarioBudgetDollars,
    Sha256,
    StableIdentifier,
    StrictModel,
    WholeDollars,
)
from .versions import (
    ACTIVE_FAMILY_PROJECT_ID_SET,
    ACTIVE_FAMILY_REQUEST_DOLLARS,
    BENCHMARK_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    HISTORICAL_BENCHMARK_SOURCE_ID,
)

class PlanMembershipContractError(ValueError):
    """Typed M1 membership-contract rejection; no arithmetic is performed."""

    def __init__(self, code: str, project_id: str):
        self.code = code
        self.project_id = project_id
        super().__init__(f"{code}: {project_id}")


def validate_plan_membership_contract(
    catalog: CatalogArtifact, project_ids: list[str]
) -> tuple[str, ...]:
    """Validate ID membership from catalog family facts, never geometry."""

    if len(project_ids) != len(set(project_ids)):
        duplicate = next(project_id for project_id in project_ids if project_ids.count(project_id) > 1)
        raise PlanMembershipContractError("DUPLICATE_PROJECT_ID", duplicate)
    projects = {project.project_id: project for project in catalog.projects}
    for project_id in project_ids:
        project = projects.get(project_id)
        if project is None:
            raise PlanMembershipContractError("UNKNOWN_PROJECT_ID", project_id)
        if not project.p0_family.member:
            raise PlanMembershipContractError("OUT_OF_FAMILY_PROJECT_ID", project_id)
    return tuple(sorted(project_ids))


class PlanInput(StrictModel):
    contract_version: Literal[FUNDING_PLAN_CONTRACT_VERSION]
    data_version: DataVersion
    available_budget_dollars: ScenarioBudgetDollars
    project_ids: list[ProjectId] = Field(max_length=12)
    expected_fingerprint: Sha256 | None = None

    @model_validator(mode="after")
    def reject_duplicate_ids(self) -> PlanInput:
        if len(self.project_ids) != len(set(self.project_ids)):
            raise ValueError("duplicate project IDs are forbidden")
        return self


class PlanEvaluationRequest(StrictModel):
    current: PlanInput
    reference: PlanInput | None = None

    @model_validator(mode="after")
    def plan_data_versions_agree(self) -> PlanEvaluationRequest:
        if self.reference is not None and self.reference.data_version != self.current.data_version:
            raise ValueError("current and reference plan data versions must agree")
        return self


class IncludedGovernedRequest(StrictModel):
    project_id: ProjectId
    governed_request_dollars: PositiveWholeDollars


class PlanWarning(StrictModel):
    warning_code: StableIdentifier
    project_id: ProjectId | None
    message: NonEmptyString
    evidence_context_only: Literal[True]


class FingerprintVerification(StrictModel):
    expected_fingerprint: Sha256 | None = None
    matches: bool | None = Field(default=None, strict=True)

    @model_validator(mode="after")
    def fingerprint_match_requires_expectation(self) -> FingerprintVerification:
        if self.expected_fingerprint is None and self.matches is not None:
            raise ValueError("matches must be null when no fingerprint was expected")
        if self.expected_fingerprint is not None and self.matches is None:
            raise ValueError("matches is required when a fingerprint was expected")
        return self


class EvaluatedPlan(StrictModel):
    contract_version: Literal[FUNDING_PLAN_CONTRACT_VERSION]
    data_version: DataVersion
    included_project_ids: list[ProjectId] = Field(max_length=12)
    not_included_active_family_project_ids: list[ProjectId] = Field(max_length=12)
    included_count: Count
    included_governed_requests: list[IncludedGovernedRequest] = Field(max_length=12)
    included_total_dollars: WholeDollars
    available_budget_dollars: ScenarioBudgetDollars
    remainder_dollars: WholeDollars | None
    overage_dollars: WholeDollars | None
    confirmation_status: Literal["VALID", "OVER_BUDGET"]
    warnings: list[PlanWarning]
    plan_fingerprint: Sha256
    fingerprint_verification: FingerprintVerification

    @model_validator(mode="after")
    def result_is_internally_consistent(self) -> EvaluatedPlan:
        if self.included_project_ids != sorted(self.included_project_ids):
            raise ValueError("included project IDs must use canonical lexical order")
        if self.not_included_active_family_project_ids != sorted(
            self.not_included_active_family_project_ids
        ):
            raise ValueError("not-included project IDs must use canonical lexical order")
        if len(self.included_project_ids) != len(set(self.included_project_ids)):
            raise ValueError("included project IDs must be unique")
        if len(self.not_included_active_family_project_ids) != len(
            set(self.not_included_active_family_project_ids)
        ):
            raise ValueError("not-included project IDs must be unique")
        if set(self.included_project_ids) & set(self.not_included_active_family_project_ids):
            raise ValueError("included and not-included IDs must be disjoint")
        if (
            set(self.included_project_ids)
            | set(self.not_included_active_family_project_ids)
        ) != ACTIVE_FAMILY_PROJECT_ID_SET:
            raise ValueError("evaluated membership must partition the exact active family")
        request_ids = [entry.project_id for entry in self.included_governed_requests]
        if len(request_ids) != len(set(request_ids)):
            raise ValueError("governed request entries must be unique")
        if request_ids != self.included_project_ids:
            raise ValueError("governed request entries must match canonical included IDs")
        for entry in self.included_governed_requests:
            if ACTIVE_FAMILY_REQUEST_DOLLARS.get(entry.project_id) != entry.governed_request_dollars:
                raise ValueError(
                    "governed request entries must use exact locked full-request dollars"
                )
        if self.included_count != len(self.included_project_ids):
            raise ValueError("included_count must match included_project_ids")
        if sum(entry.governed_request_dollars for entry in self.included_governed_requests) != self.included_total_dollars:
            raise ValueError("included request entries must sum to included_total_dollars")
        verification = self.fingerprint_verification
        if verification.expected_fingerprint is not None and verification.matches is not (
            verification.expected_fingerprint == self.plan_fingerprint
        ):
            raise ValueError(
                "fingerprint matches must equal expected_fingerprint == plan_fingerprint"
            )
        if self.confirmation_status == "VALID":
            if self.included_total_dollars > self.available_budget_dollars:
                raise ValueError("VALID plans cannot exceed Available Budget")
            expected_remainder = self.available_budget_dollars - self.included_total_dollars
            if self.remainder_dollars != expected_remainder or self.overage_dollars is not None:
                raise ValueError("VALID plan remainder/overage fields are inconsistent")
        else:
            if self.included_total_dollars <= self.available_budget_dollars:
                raise ValueError("OVER_BUDGET plans must exceed Available Budget")
            expected_overage = self.included_total_dollars - self.available_budget_dollars
            if self.overage_dollars != expected_overage or self.remainder_dollars is not None:
                raise ValueError("OVER_BUDGET plan remainder/overage fields are inconsistent")
        return self


class PlanSemanticError(StrictModel):
    error_code: Literal[
        "UNKNOWN_PROJECT_ID",
        "OUT_OF_FAMILY_PROJECT_ID",
        "DUPLICATE_PROJECT_ID",
        "CONTRACT_VERSION_CONFLICT",
        "DATA_VERSION_CONFLICT",
    ]
    field_path: list[str | int]
    message: NonEmptyString
    project_id: ProjectId | None = None


class PlanSideResult(StrictModel):
    status: Literal["VALID", "OVER_BUDGET", "INVALID"]
    evaluated_plan: EvaluatedPlan | None
    semantic_errors: list[PlanSemanticError]

    @model_validator(mode="after")
    def status_controls_payload(self) -> PlanSideResult:
        if self.status == "INVALID":
            if self.evaluated_plan is not None or not self.semantic_errors:
                raise ValueError("INVALID sides require errors and no evaluated plan")
        else:
            if self.evaluated_plan is None or self.semantic_errors:
                raise ValueError("evaluated sides require a plan and no semantic errors")
            if self.evaluated_plan.confirmation_status != self.status:
                raise ValueError("side status and evaluated plan status disagree")
        return self


class MembershipDollarDelta(StrictModel):
    project_ids: list[ProjectId]
    governed_request_total_dollars: WholeDollars

    @model_validator(mode="after")
    def exact_governed_membership_dollars(self) -> MembershipDollarDelta:
        if self.project_ids != sorted(set(self.project_ids)):
            raise ValueError("membership-delta IDs must be unique and canonical")
        if not set(self.project_ids) <= ACTIVE_FAMILY_PROJECT_ID_SET:
            raise ValueError("membership-delta IDs must belong to the active family")
        expected = sum(ACTIVE_FAMILY_REQUEST_DOLLARS[item] for item in self.project_ids)
        if self.governed_request_total_dollars != expected:
            raise ValueError("membership-delta dollars must use exact governed requests")
        return self


class PlanComparison(StrictModel):
    budget_difference_dollars: int = Field(strict=True)
    included_total_difference_dollars: int = Field(strict=True)
    remainder_difference_dollars: int = Field(strict=True)
    included_count_difference: int = Field(strict=True)
    entering: MembershipDollarDelta
    leaving: MembershipDollarDelta
    unchanged_project_ids: list[ProjectId]


class PlanEvaluationResponseData(StrictModel):
    current: PlanSideResult
    reference: PlanSideResult | None = None
    comparison: PlanComparison | None = None

    @model_validator(mode="after")
    def comparison_requires_two_valid_sides(self) -> PlanEvaluationResponseData:
        both_valid = (
            self.current.status == "VALID"
            and self.reference is not None
            and self.reference.status == "VALID"
        )
        if (self.comparison is not None) != both_valid:
            raise ValueError("comparison is present only when both plan sides are VALID")
        if both_valid:
            assert self.reference is not None
            assert self.current.evaluated_plan is not None
            assert self.reference.evaluated_plan is not None
            assert self.comparison is not None
            current = self.current.evaluated_plan
            reference = self.reference.evaluated_plan
            comparison = self.comparison
            current_ids = set(current.included_project_ids)
            reference_ids = set(reference.included_project_ids)
            expected = {
                "budget_difference_dollars": (
                    current.available_budget_dollars
                    - reference.available_budget_dollars
                ),
                "included_total_difference_dollars": (
                    current.included_total_dollars
                    - reference.included_total_dollars
                ),
                "remainder_difference_dollars": (
                    current.remainder_dollars - reference.remainder_dollars
                ),
                "included_count_difference": (
                    current.included_count - reference.included_count
                ),
            }
            for field, value in expected.items():
                if getattr(comparison, field) != value:
                    raise ValueError(f"comparison {field} is not derived from both plans")
            if comparison.entering.project_ids != sorted(current_ids - reference_ids):
                raise ValueError("comparison entering IDs are not derived from both plans")
            if comparison.leaving.project_ids != sorted(reference_ids - current_ids):
                raise ValueError("comparison leaving IDs are not derived from both plans")
            if comparison.unchanged_project_ids != sorted(current_ids & reference_ids):
                raise ValueError("comparison unchanged IDs are not derived from both plans")
        return self


class BenchmarkComparisonRequest(StrictModel):
    plan: PlanInput
    expected_benchmark_contract_version: Literal[BENCHMARK_CONTRACT_VERSION]
    expected_benchmark_data_version: DataVersion

    @model_validator(mode="after")
    def benchmark_and_plan_data_versions_agree(self) -> BenchmarkComparisonRequest:
        if self.expected_benchmark_data_version != self.plan.data_version:
            raise ValueError("benchmark and plan data versions must agree")
        return self


class BenchmarkOverlap(StrictModel):
    project_ids: list[ProjectId] = Field(max_length=12)
    project_count: Count
    published_amount: PublishedMoneyValue

    @model_validator(mode="after")
    def overlap_ids_are_canonical(self) -> BenchmarkOverlap:
        if self.project_ids != sorted(set(self.project_ids)):
            raise ValueError("benchmark overlap IDs must be unique and canonical")
        if self.project_count != len(self.project_ids):
            raise ValueError("benchmark overlap count must match its IDs")
        return self


class BenchmarkComparisonResponseData(StrictModel):
    benchmark_contract_version: Literal[BENCHMARK_CONTRACT_VERSION]
    benchmark_data_version: DataVersion
    benchmark_source_id: Literal[HISTORICAL_BENCHMARK_SOURCE_ID]
    evaluated_plan: EvaluatedPlan
    published_allocation: PublishedMoneyValue
    city_included_count: PublishedCountValue
    overlap: BenchmarkOverlap | None = None
    documented_divergences: list[NonEmptyString]

    @model_validator(mode="after")
    def comparison_uses_fresh_valid_plan(self) -> BenchmarkComparisonResponseData:
        if self.evaluated_plan.confirmation_status != "VALID":
            raise ValueError("benchmark comparison requires a freshly valid plan")
        if self.evaluated_plan.data_version != self.benchmark_data_version:
            raise ValueError("benchmark response and evaluated plan data versions must agree")
        if self.overlap is not None and not set(self.overlap.project_ids) <= set(
            self.evaluated_plan.included_project_ids
        ):
            raise ValueError("benchmark overlap must be contained in the evaluated plan")
        return self
