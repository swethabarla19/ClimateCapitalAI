"""Deterministic M3.7D cross-category Funding Plan state machine.

This evaluator implements Priority-Constrained Analyst-Governed Portfolio
Construction against the validated 106-project runtime-v2 catalog.

It exists in parallel with the legacy Watershed evaluator until the
cross-category runtime integration gate is passed.
"""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict

from climatecapital.contracts.cross_category_runtime import (
    AppliedAnalystOverride,
    BoundaryCandidateResult,
    BoundaryResolutionInput,
    BoundaryTierResult,
    CrossCategoryPlanInput,
    CrossCategoryPlanResult,
    CrossCategoryRuntimeCatalog,
    CrossCategoryRuntimeProject,
    PortfolioWarning,
    SelectedProjectResult,
)


class CrossCategoryPortfolioEvaluationError(
    RuntimeError
):
    """Semantic error in an otherwise schema-valid portfolio request."""

    def __init__(
        self,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            message
        )

        self.code = code
        self.message = message


def _tier_key(
    project: CrossCategoryRuntimeProject,
) -> tuple[float, int]:
    return (
        float(
            project.funding_priority_score
        ),
        project.funding_priority_rank,
    )


def _resolution_key(
    resolution: BoundaryResolutionInput,
) -> tuple[float, int]:
    return (
        float(
            resolution.funding_priority_score
        ),
        resolution.funding_priority_rank,
    )


def _ordered_tiers(
    catalog: CrossCategoryRuntimeCatalog,
) -> list[
    tuple[
        tuple[float, int],
        list[CrossCategoryRuntimeProject],
    ]
]:
    groups: dict[
        tuple[float, int],
        list[CrossCategoryRuntimeProject],
    ] = defaultdict(
        list
    )

    for project in catalog.projects:
        groups[
            _tier_key(
                project
            )
        ].append(
            project
        )

    result = []

    for key in sorted(
        groups,
        key=lambda item: (
            -item[0],
            item[1],
        ),
    ):
        projects = sorted(
            groups[
                key
            ],
            key=lambda project: (
                project.decision_unit_id
            ),
        )

        result.append(
            (
                key,
                projects,
            )
        )

    return result


def _resolution_map(
    plan: CrossCategoryPlanInput,
) -> dict[
    tuple[float, int],
    BoundaryResolutionInput,
]:
    return {
        _resolution_key(
            resolution
        ):
            resolution
        for resolution
        in plan.boundary_resolutions
    }


def _selected_project(
    project: CrossCategoryRuntimeProject,
    *,
    source: str,
) -> SelectedProjectResult:
    return SelectedProjectResult(
        decision_unit_id=(
            project.decision_unit_id
        ),
        model_request_dollars=(
            project.model_request_dollars
        ),
        funding_priority_score=(
            project.funding_priority_score
        ),
        funding_priority_rank=(
            project.funding_priority_rank
        ),
        selection_source=source,
    )


def _boundary_result(
    projects: list[
        CrossCategoryRuntimeProject
    ],
    *,
    remaining_budget: int,
) -> BoundaryTierResult:
    if not projects:
        raise ValueError(
            "Boundary tier cannot be empty."
        )

    first = projects[0]

    return BoundaryTierResult(
        funding_priority_score=(
            first.funding_priority_score
        ),
        funding_priority_rank=(
            first.funding_priority_rank
        ),
        remaining_budget_before_tier_dollars=(
            remaining_budget
        ),
        full_tier_request_dollars=sum(
            project.model_request_dollars
            for project in projects
        ),
        candidates=[
            BoundaryCandidateResult(
                decision_unit_id=(
                    project.decision_unit_id
                ),
                model_request_dollars=(
                    project.model_request_dollars
                ),
                funding_priority_score=(
                    project.funding_priority_score
                ),
                funding_priority_rank=(
                    project.funding_priority_rank
                ),
                individually_budget_feasible=(
                    project.model_request_dollars
                    <= remaining_budget
                ),
            )
            for project
            in projects
        ],
    )


def _normalized_resolution_payload(
    plan: CrossCategoryPlanInput,
) -> list[dict[str, object]]:
    return [
        {
            "funding_priority_score":
                float(
                    resolution
                    .funding_priority_score
                ),
            "funding_priority_rank":
                resolution
                .funding_priority_rank,
            "selected_decision_unit_ids":
                sorted(
                    resolution
                    .selected_decision_unit_ids
                ),
            (
                "advance_with_feasible_"
                "same_tier_project_acknowledged"
            ):
                resolution
                .advance_with_feasible_same_tier_project_acknowledged,
        }
        for resolution
        in sorted(
            plan.boundary_resolutions,
            key=lambda item: (
                -float(
                    item
                    .funding_priority_score
                ),
                item
                .funding_priority_rank,
            ),
        )
    ]


def canonical_cross_category_plan_fingerprint(
    *,
    plan: CrossCategoryPlanInput,
    selected_projects: list[
        SelectedProjectResult
    ],
    status: str,
    unresolved_boundary: (
        BoundaryTierResult | None
    ),
    applied_overrides: list[
        AppliedAnalystOverride
    ],
) -> str:
    """Return deterministic SHA-256 for one evaluated portfolio state."""

    payload = {
        "contract_version":
            plan.contract_version,
        "data_version":
            plan.data_version,
        "available_budget_dollars":
            plan.available_budget_dollars,
        "boundary_resolutions":
            _normalized_resolution_payload(
                plan
            ),
        "selected_decision_unit_ids":
            sorted(
                project.decision_unit_id
                for project
                in selected_projects
            ),
        "status":
            status,
        "unresolved_boundary":
            (
                None
                if unresolved_boundary
                is None
                else {
                    "funding_priority_score":
                        float(
                            unresolved_boundary
                            .funding_priority_score
                        ),
                    "funding_priority_rank":
                        unresolved_boundary
                        .funding_priority_rank,
                }
            ),
        "applied_overrides": [
            {
                "funding_priority_score":
                    float(
                        override
                        .funding_priority_score
                    ),
                "funding_priority_rank":
                    override
                    .funding_priority_rank,
                "decision_unit_ids_left_feasible":
                    sorted(
                        override
                        .decision_unit_ids_left_feasible
                    ),
            }
            for override
            in applied_overrides
        ],
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        canonical
    ).hexdigest()


def _reject_unused_resolutions(
    *,
    resolution_map: dict[
        tuple[float, int],
        BoundaryResolutionInput,
    ],
    consumed_keys: set[
        tuple[float, int]
    ],
) -> None:
    unused = (
        set(
            resolution_map
        )
        - consumed_keys
    )

    if not unused:
        return

    ordered = sorted(
        unused,
        key=lambda item: (
            -item[0],
            item[1],
        ),
    )

    raise CrossCategoryPortfolioEvaluationError(
        "STALE_BOUNDARY_RESOLUTION",
        (
            "Boundary resolution does not "
            "correspond to an active ambiguous "
            "boundary tier under the current "
            f"scenario: {ordered}"
        ),
    )


def _build_result(
    *,
    plan: CrossCategoryPlanInput,
    selected_projects: list[
        SelectedProjectResult
    ],
    status: str,
    unresolved_boundary: (
        BoundaryTierResult | None
    ),
    warnings: list[
        PortfolioWarning
    ],
    applied_overrides: list[
        AppliedAnalystOverride
    ],
) -> CrossCategoryPlanResult:
    included_total = sum(
        project.model_request_dollars
        for project in selected_projects
    )

    remainder = (
        plan.available_budget_dollars
        - included_total
    )

    fingerprint = (
        canonical_cross_category_plan_fingerprint(
            plan=plan,
            selected_projects=(
                selected_projects
            ),
            status=status,
            unresolved_boundary=(
                unresolved_boundary
            ),
            applied_overrides=(
                applied_overrides
            ),
        )
    )

    if (
        plan.expected_fingerprint
        is not None
        and plan.expected_fingerprint
        != fingerprint
    ):
        raise CrossCategoryPortfolioEvaluationError(
            "PLAN_FINGERPRINT_CONFLICT",
            (
                "Expected plan fingerprint "
                "does not match deterministic "
                "evaluation."
            ),
        )

    return CrossCategoryPlanResult(
        contract_version=(
            plan.contract_version
        ),
        data_version=(
            plan.data_version
        ),
        status=status,
        available_budget_dollars=(
            plan.available_budget_dollars
        ),
        selected_projects=(
            selected_projects
        ),
        included_total_dollars=(
            included_total
        ),
        remainder_dollars=(
            remainder
        ),
        unresolved_boundary=(
            unresolved_boundary
        ),
        warnings=warnings,
        applied_analyst_overrides=(
            applied_overrides
        ),
        plan_fingerprint=(
            fingerprint
        ),
    )


def evaluate_cross_category_plan(
    catalog: CrossCategoryRuntimeCatalog,
    plan: CrossCategoryPlanInput,
) -> CrossCategoryPlanResult:
    """Evaluate one analyst-controlled cross-category Funding Plan.

    Rules:
    - projects are indivisible full-request units;
    - process official PRB tiers from highest to lowest;
    - include a complete tier when it fits;
    - if a tier does not fit, inspect only budget feasibility;
    - zero feasible projects -> skip the tier and continue;
    - one feasible project -> include it automatically;
    - multiple feasible tied projects -> analyst resolution required;
    - after analyst resolution, advancing while a same-tier project still
      fits requires explicit acknowledgement;
    - no cost, category, ID, name, GIS, O&M, district, recommendation, or
      PRB-component preference is used as an analytical tiebreaker.
    """

    if (
        plan.data_version
        != catalog.data_version
    ):
        raise CrossCategoryPortfolioEvaluationError(
            "DATA_VERSION_CONFLICT",
            (
                "Plan data version does not "
                "match active runtime catalog."
            ),
        )

    resolution_map = (
        _resolution_map(
            plan
        )
    )

    consumed_resolution_keys: set[
        tuple[float, int]
    ] = set()

    selected_projects: list[
        SelectedProjectResult
    ] = []

    warnings: list[
        PortfolioWarning
    ] = []

    applied_overrides: list[
        AppliedAnalystOverride
    ] = []

    for (
        tier_key,
        tier_projects,
    ) in _ordered_tiers(
        catalog
    ):
        included_total = sum(
            project.model_request_dollars
            for project in selected_projects
        )

        remaining_budget = (
            plan.available_budget_dollars
            - included_total
        )

        tier_total = sum(
            project.model_request_dollars
            for project in tier_projects
        )

        resolution = (
            resolution_map.get(
                tier_key
            )
        )

        # ---------------------------------------------------------------
        # Complete substantive priority tier fits.
        # ---------------------------------------------------------------

        if (
            tier_total
            <= remaining_budget
        ):
            if resolution is not None:
                raise CrossCategoryPortfolioEvaluationError(
                    "RESOLUTION_NOT_REQUIRED",
                    (
                        "Analyst boundary resolution "
                        "was supplied for a priority "
                        "tier that fits completely."
                    ),
                )

            selected_projects.extend(
                _selected_project(
                    project,
                    source=(
                        "AUTO_COMPLETE_TIER"
                    ),
                )
                for project
                in tier_projects
            )

            continue

        # ---------------------------------------------------------------
        # Boundary tier: complete tier does not fit.
        # ---------------------------------------------------------------

        feasible_projects = [
            project
            for project
            in tier_projects
            if (
                project.model_request_dollars
                <= remaining_budget
            )
        ]

        # ---------------------------------------------------------------
        # No project in this priority tier can fit.
        # Skip it and continue to lower priorities.
        # ---------------------------------------------------------------

        if not feasible_projects:
            if resolution is not None:
                raise CrossCategoryPortfolioEvaluationError(
                    "RESOLUTION_NOT_REQUIRED",
                    (
                        "Analyst boundary resolution "
                        "was supplied for a tier with "
                        "no budget-feasible project."
                    ),
                )

            continue

        # ---------------------------------------------------------------
        # Budget feasibility uniquely resolves the tier.
        # This is not a cheapest-first preference.
        # ---------------------------------------------------------------

        if (
            len(
                feasible_projects
            )
            == 1
        ):
            if resolution is not None:
                raise CrossCategoryPortfolioEvaluationError(
                    "RESOLUTION_NOT_REQUIRED",
                    (
                        "Analyst boundary resolution "
                        "was supplied where budget "
                        "feasibility uniquely resolves "
                        "the tier."
                    ),
                )

            selected_projects.append(
                _selected_project(
                    feasible_projects[
                        0
                    ],
                    source=(
                        "AUTO_UNIQUE_"
                        "BUDGET_FEASIBLE"
                    ),
                )
            )

            continue

        # ---------------------------------------------------------------
        # Multiple substantively tied projects remain feasible.
        # Analyst resolution is required.
        # ---------------------------------------------------------------

        if resolution is None:
            _reject_unused_resolutions(
                resolution_map=(
                    resolution_map
                ),
                consumed_keys=(
                    consumed_resolution_keys
                ),
            )

            boundary = (
                _boundary_result(
                    tier_projects,
                    remaining_budget=(
                        remaining_budget
                    ),
                )
            )

            return _build_result(
                plan=plan,
                selected_projects=(
                    selected_projects
                ),
                status=(
                    "ANALYST_RESOLUTION_REQUIRED"
                ),
                unresolved_boundary=(
                    boundary
                ),
                warnings=warnings,
                applied_overrides=(
                    applied_overrides
                ),
            )

        consumed_resolution_keys.add(
            tier_key
        )

        tier_ids = {
            project.decision_unit_id
            for project
            in tier_projects
        }

        requested_ids = set(
            resolution
            .selected_decision_unit_ids
        )

        if not requested_ids.issubset(
            tier_ids
        ):
            unknown = sorted(
                requested_ids
                - tier_ids
            )

            raise CrossCategoryPortfolioEvaluationError(
                "RESOLUTION_PROJECT_NOT_IN_TIER",
                (
                    "Boundary resolution contains "
                    "project IDs outside the active "
                    f"priority tier: {unknown}"
                ),
            )

        selected_from_tier = [
            project
            for project
            in tier_projects
            if (
                project.decision_unit_id
                in requested_ids
            )
        ]

        resolution_total = sum(
            project.model_request_dollars
            for project
            in selected_from_tier
        )

        if (
            resolution_total
            > remaining_budget
        ):
            raise CrossCategoryPortfolioEvaluationError(
                "RESOLUTION_OVER_BUDGET",
                (
                    "Analyst-selected tied projects "
                    "exceed the remaining Available "
                    "Project Budget."
                ),
            )

        selected_projects.extend(
            _selected_project(
                project,
                source=(
                    "ANALYST_BOUNDARY_RESOLUTION"
                ),
            )
            for project
            in selected_from_tier
        )

        post_resolution_remaining = (
            remaining_budget
            - resolution_total
        )

        unselected_same_tier = [
            project
            for project
            in tier_projects
            if (
                project.decision_unit_id
                not in requested_ids
            )
        ]

        still_feasible = [
            project
            for project
            in unselected_same_tier
            if (
                project.model_request_dollars
                <= post_resolution_remaining
            )
        ]

        acknowledgement = (
            resolution
            .advance_with_feasible_same_tier_project_acknowledged
        )

        if still_feasible:
            warning = PortfolioWarning(
                warning_code=(
                    "HIGHER_PRIORITY_"
                    "FEASIBLE_PROJECT_REMAINS"
                ),
                message=(
                    "One or more unselected "
                    "same-priority projects remain "
                    "budget-feasible. Explicit "
                    "analyst acknowledgement is "
                    "required before advancing to "
                    "a lower-priority tier."
                ),
                decision_unit_ids=[
                    project.decision_unit_id
                    for project
                    in still_feasible
                ],
            )

            warnings.append(
                warning
            )

            if not acknowledgement:
                _reject_unused_resolutions(
                    resolution_map=(
                        resolution_map
                    ),
                    consumed_keys=(
                        consumed_resolution_keys
                    ),
                )

                boundary = (
                    _boundary_result(
                        tier_projects,
                        remaining_budget=(
                            remaining_budget
                        ),
                    )
                )

                return _build_result(
                    plan=plan,
                    selected_projects=(
                        selected_projects
                    ),
                    status=(
                        "ANALYST_RESOLUTION_REQUIRED"
                    ),
                    unresolved_boundary=(
                        boundary
                    ),
                    warnings=warnings,
                    applied_overrides=(
                        applied_overrides
                    ),
                )

            applied_overrides.append(
                AppliedAnalystOverride(
                    funding_priority_score=(
                        tier_projects[
                            0
                        ]
                        .funding_priority_score
                    ),
                    funding_priority_rank=(
                        tier_projects[
                            0
                        ]
                        .funding_priority_rank
                    ),
                    acknowledged=True,
                    decision_unit_ids_left_feasible=[
                        project.decision_unit_id
                        for project
                        in still_feasible
                    ],
                )
            )

        elif acknowledgement:
            raise CrossCategoryPortfolioEvaluationError(
                "UNNECESSARY_PRIORITY_OVERRIDE",
                (
                    "Priority-override "
                    "acknowledgement was supplied "
                    "even though no unselected "
                    "same-tier project remains "
                    "budget-feasible."
                ),
            )

    _reject_unused_resolutions(
        resolution_map=(
            resolution_map
        ),
        consumed_keys=(
            consumed_resolution_keys
        ),
    )

    return _build_result(
        plan=plan,
        selected_projects=(
            selected_projects
        ),
        status="COMPLETE",
        unresolved_boundary=None,
        warnings=warnings,
        applied_overrides=(
            applied_overrides
        ),
    )