"""Deterministic server-authoritative Funding Plan evaluation."""

from __future__ import annotations

import hashlib
import json

from climatecapital.contracts.artifacts import CatalogArtifact
from climatecapital.contracts.plans import (
    EvaluatedPlan,
    FingerprintVerification,
    IncludedGovernedRequest,
    MembershipDollarDelta,
    PlanComparison,
    PlanEvaluationRequest,
    PlanEvaluationResponseData,
    PlanInput,
    PlanMembershipContractError,
    PlanSemanticError,
    PlanSideResult,
    validate_plan_membership_contract,
)


def canonical_plan_fingerprint(
    plan: PlanInput,
    canonical_project_ids: tuple[str, ...],
) -> str:
    """Return the deterministic SHA-256 fingerprint for one plan input.

    Only the locked fingerprint inputs participate:
    - Funding Plan contract version
    - data version
    - whole-dollar Available Budget
    - unique included project IDs in canonical lexical order
    """

    payload = {
        "contract_version": plan.contract_version,
        "data_version": plan.data_version,
        "available_budget_dollars": plan.available_budget_dollars,
        "project_ids": list(canonical_project_ids),
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

    return hashlib.sha256(canonical).hexdigest()


def _invalid_side(
    *,
    error_code: str,
    field_path: list[str | int],
    message: str,
    project_id: str | None = None,
) -> PlanSideResult:
    return PlanSideResult(
        status="INVALID",
        evaluated_plan=None,
        semantic_errors=[
            PlanSemanticError(
                error_code=error_code,
                field_path=field_path,
                message=message,
                project_id=project_id,
            )
        ],
    )


def evaluate_plan(
    catalog: CatalogArtifact,
    plan: PlanInput,
) -> PlanSideResult:
    """Evaluate exactly one untrusted plan against one validated catalog."""

    if plan.data_version != catalog.data_version:
        return _invalid_side(
            error_code="DATA_VERSION_CONFLICT",
            field_path=["data_version"],
            message="Plan data version does not match the active catalog.",
        )

    try:
        canonical_ids = validate_plan_membership_contract(
            catalog,
            list(plan.project_ids),
        )
    except PlanMembershipContractError as error:
        try:
            index = plan.project_ids.index(error.project_id)
        except ValueError:
            index = 0

        return _invalid_side(
            error_code=error.code,
            field_path=["project_ids", index],
            message=str(error),
            project_id=error.project_id,
        )

    projects_by_id = {
        project.project_id: project
        for project in catalog.projects
    }

    included_requests = [
        IncludedGovernedRequest(
            project_id=project_id,
            governed_request_dollars=projects_by_id[
                project_id
            ].governed_request_dollars,
        )
        for project_id in canonical_ids
    ]

    included_total = sum(
        entry.governed_request_dollars
        for entry in included_requests
    )

    if included_total <= plan.available_budget_dollars:
        status = "VALID"
        remainder = plan.available_budget_dollars - included_total
        overage = None
    else:
        status = "OVER_BUDGET"
        remainder = None
        overage = included_total - plan.available_budget_dollars

    active_family_ids = set(catalog.active_family_summary.project_ids)
    included_id_set = set(canonical_ids)

    not_included_ids = sorted(
        active_family_ids - included_id_set
    )

    fingerprint = canonical_plan_fingerprint(
        plan,
        canonical_ids,
    )

    verification = FingerprintVerification(
        expected_fingerprint=plan.expected_fingerprint,
        matches=(
            None
            if plan.expected_fingerprint is None
            else plan.expected_fingerprint == fingerprint
        ),
    )

    evaluated = EvaluatedPlan(
        contract_version=plan.contract_version,
        data_version=plan.data_version,
        included_project_ids=list(canonical_ids),
        not_included_active_family_project_ids=not_included_ids,
        included_count=len(canonical_ids),
        included_governed_requests=included_requests,
        included_total_dollars=included_total,
        available_budget_dollars=plan.available_budget_dollars,
        remainder_dollars=remainder,
        overage_dollars=overage,
        confirmation_status=status,
        warnings=[],
        plan_fingerprint=fingerprint,
        fingerprint_verification=verification,
    )

    return PlanSideResult(
        status=status,
        evaluated_plan=evaluated,
        semantic_errors=[],
    )


def _membership_delta(
    catalog: CatalogArtifact,
    project_ids: set[str],
) -> MembershipDollarDelta:
    projects_by_id = {
        project.project_id: project
        for project in catalog.projects
    }

    ordered_ids = sorted(project_ids)

    return MembershipDollarDelta(
        project_ids=ordered_ids,
        governed_request_total_dollars=sum(
            projects_by_id[project_id].governed_request_dollars
            for project_id in ordered_ids
        ),
    )


def _compare_valid_plans(
    catalog: CatalogArtifact,
    current: EvaluatedPlan,
    reference: EvaluatedPlan,
) -> PlanComparison:
    if current.remainder_dollars is None:
        raise ValueError("current plan must be VALID for comparison")
    if reference.remainder_dollars is None:
        raise ValueError("reference plan must be VALID for comparison")

    current_ids = set(current.included_project_ids)
    reference_ids = set(reference.included_project_ids)

    return PlanComparison(
        budget_difference_dollars=(
            current.available_budget_dollars
            - reference.available_budget_dollars
        ),
        included_total_difference_dollars=(
            current.included_total_dollars
            - reference.included_total_dollars
        ),
        remainder_difference_dollars=(
            current.remainder_dollars
            - reference.remainder_dollars
        ),
        included_count_difference=(
            current.included_count
            - reference.included_count
        ),
        entering=_membership_delta(
            catalog,
            current_ids - reference_ids,
        ),
        leaving=_membership_delta(
            catalog,
            reference_ids - current_ids,
        ),
        unchanged_project_ids=sorted(
            current_ids & reference_ids
        ),
    )


def evaluate_plan_request(
    catalog: CatalogArtifact,
    request: PlanEvaluationRequest,
) -> PlanEvaluationResponseData:
    """Independently evaluate current and optional reference plan inputs."""

    current = evaluate_plan(catalog, request.current)

    reference = (
        evaluate_plan(catalog, request.reference)
        if request.reference is not None
        else None
    )

    comparison = None

    if (
        current.status == "VALID"
        and reference is not None
        and reference.status == "VALID"
    ):
        assert current.evaluated_plan is not None
        assert reference.evaluated_plan is not None

        comparison = _compare_valid_plans(
            catalog,
            current.evaluated_plan,
            reference.evaluated_plan,
        )

    return PlanEvaluationResponseData(
        current=current,
        reference=reference,
        comparison=comparison,
    )
