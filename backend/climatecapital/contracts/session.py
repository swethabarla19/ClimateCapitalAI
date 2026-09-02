"""Browser session state contract; persistence remains sessionStorage-only."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import Field, StringConstraints, model_validator

from .common import (
    DataVersion,
    NonEmptyString,
    ProjectId,
    ScenarioBudgetDollars,
    Sha256,
    StrictModel,
)
from .plans import EvaluatedPlan, PlanInput
from .versions import (
    BROWSER_SESSION_CONTRACT_VERSION,
    HISTORICAL_ENVELOPE_DOLLARS,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)


class SessionDeploymentIdentity(StrictModel):
    data_version: DataVersion
    manifest_sha256: Sha256
    release_id: Annotated[str, StringConstraints(min_length=1, max_length=200)]
    release_manifest_contract_version: Literal[RELEASE_MANIFEST_CONTRACT_VERSION]


class MapExtent(StrictModel):
    west: float = Field(ge=-180, le=180, allow_inf_nan=False)
    south: float = Field(ge=-90, le=90, allow_inf_nan=False)
    east: float = Field(ge=-180, le=180, allow_inf_nan=False)
    north: float = Field(ge=-90, le=90, allow_inf_nan=False)
    zoom: float = Field(ge=0, le=24, allow_inf_nan=False)

    @model_validator(mode="after")
    def ordered_bounds(self) -> MapExtent:
        if self.west > self.east or self.south > self.north:
            raise ValueError("map extent bounds must be ordered")
        return self


class PresentationState(StrictModel):
    route: Literal["EXPLORE", "FUNDING_PLAN", "DATA_METHODOLOGY", "HELP_RESOURCES"]
    search_text: Annotated[str, StringConstraints(max_length=200)]
    filter_ids: list[str] = Field(max_length=50)
    sort: Literal["SOURCE_ORDER", "NAME", "REQUEST_ASC", "REQUEST_DESC"]
    map_extent: MapExtent | None = None
    visible_layers: list[
        Literal[
            "rna_current_project_display",
            "fema_current_hazard_context",
            "eaz_2021_context",
        ]
    ] = Field(max_length=3)
    selected_project_id: ProjectId | None = None
    list_position: int = Field(strict=True, ge=0)

    @model_validator(mode="after")
    def layer_ids_are_unique(self) -> PresentationState:
        if len(self.visible_layers) != len(set(self.visible_layers)):
            raise ValueError("visible layer IDs must be unique")
        return self


class ConfirmedPlanState(StrictModel):
    validated_identity: SessionDeploymentIdentity
    input: PlanInput
    last_server_result: EvaluatedPlan
    fingerprint: Sha256

    @model_validator(mode="after")
    def input_result_identity_agrees(self) -> ConfirmedPlanState:
        if self.last_server_result.confirmation_status != "VALID":
            raise ValueError("confirmed plans require a VALID server result")
        if self.input.data_version != self.last_server_result.data_version:
            raise ValueError("confirmed plan input and result data versions disagree")
        if self.input.data_version != self.validated_identity.data_version:
            raise ValueError("confirmed plan is stale under its validated deployment identity")
        if self.input.available_budget_dollars != self.last_server_result.available_budget_dollars:
            raise ValueError("confirmed plan input and result budgets disagree")
        if sorted(self.input.project_ids) != self.last_server_result.included_project_ids:
            raise ValueError("confirmed plan input and result memberships disagree")
        if self.fingerprint != self.last_server_result.plan_fingerprint:
            raise ValueError("confirmed fingerprint must equal the server result")
        verification = self.last_server_result.fingerprint_verification
        if self.input.expected_fingerprint != verification.expected_fingerprint:
            raise ValueError("input and result expected fingerprints disagree")
        if self.input.expected_fingerprint is not None and verification.matches is not True:
            raise ValueError("confirmed plans require a matching expected fingerprint")
        return self


class WhatIfState(ConfirmedPlanState):
    confirmation_state: Literal["CONFIRMED"]


class DirtyAttempt(StrictModel):
    input: PlanInput
    validation_state: Literal[
        "DIRTY_UNAPPLIED",
        "INVALID",
        "OVER_BUDGET",
        "VALIDATING",
        "FAILED",
    ]
    message: NonEmptyString | None = None


class PendingGeminiProposal(StrictModel):
    action: Literal["SET_BUDGET", "ADD_PROJECT", "REMOVE_PROJECT"]
    available_budget_dollars: ScenarioBudgetDollars | None = None
    project_id: ProjectId | None = None
    applied: Literal[False]

    @model_validator(mode="after")
    def action_shape(self) -> PendingGeminiProposal:
        if self.action == "SET_BUDGET":
            if self.available_budget_dollars is None or self.project_id is not None:
                raise ValueError("SET_BUDGET requires only available_budget_dollars")
        elif self.project_id is None or self.available_budget_dollars is not None:
            raise ValueError("project actions require only project_id")
        return self


class ReviewedDraftBinding(StrictModel):
    plan: Literal["REFERENCE", "WHAT_IF"]
    fingerprint: Sha256
    validated_identity: SessionDeploymentIdentity
    current_session_only: Literal[True]
    non_official: Literal[True]


class LocalRequestState(StrictModel):
    surface: Literal[
        "BOOTSTRAP",
        "PLAN",
        "BENCHMARK",
        "GEMINI",
        "PROJECT_DETAIL",
        "MAP_TILES",
    ]
    status: Literal["IDLE", "LOADING", "SUCCESS", "ERROR"]
    error_code: str | None = None


class VisibleExplanation(StrictModel):
    context_type: Literal[
        "PROJECT",
        "PLAN",
        "SCENARIO_COMPARISON",
        "BENCHMARK",
        "METHODOLOGY",
        "PROVENANCE",
    ]
    sanitized_text: Annotated[str, StringConstraints(max_length=8_000)]


class BrowserSessionState(StrictModel):
    contract_version: Literal[BROWSER_SESSION_CONTRACT_VERSION]
    validated_identity: SessionDeploymentIdentity
    presentation: PresentationState
    working_plan: PlanInput
    session_reference_plan: ConfirmedPlanState | None = None
    what_if: WhatIfState | None = None
    current_confirmed_plan: Literal["REFERENCE", "WHAT_IF"] | None = None
    dirty_attempt: DirtyAttempt | None = None
    pending_gemini_proposal: PendingGeminiProposal | None = None
    reviewed_draft: ReviewedDraftBinding | None = None
    local_request_states: list[LocalRequestState]
    visible_explanation: VisibleExplanation | None = None

    @model_validator(mode="after")
    def state_references_existing_confirmed_results(self) -> BrowserSessionState:
        if self.current_confirmed_plan == "REFERENCE" and self.session_reference_plan is None:
            raise ValueError("REFERENCE pointer requires a Session Reference Plan")
        if self.current_confirmed_plan == "WHAT_IF" and self.what_if is None:
            raise ValueError("WHAT_IF pointer requires a confirmed What-If")
        if self.current_confirmed_plan is None and (
            self.session_reference_plan is not None or self.what_if is not None
        ):
            raise ValueError("confirmed plan state requires a Current Confirmed Plan pointer")
        if self.what_if is not None and self.session_reference_plan is None:
            raise ValueError("a What-If requires an immutable Session Reference Plan")
        if (
            self.session_reference_plan is not None
            and self.session_reference_plan.input.available_budget_dollars
            != HISTORICAL_ENVELOPE_DOLLARS
        ):
            raise ValueError(
                "Session Reference Plan must use the $125,000,000 Historical Envelope"
            )
        if self.reviewed_draft is not None:
            selected = (
                self.session_reference_plan
                if self.reviewed_draft.plan == "REFERENCE"
                else self.what_if
            )
            if selected is None or selected.fingerprint != self.reviewed_draft.fingerprint:
                raise ValueError("Reviewed Draft must bind to an exact confirmed fingerprint")
            if self.reviewed_draft.validated_identity != self.validated_identity:
                raise ValueError(
                    "Reviewed Draft is stale under the currently validated deployment identity"
                )
        if self.working_plan.data_version != self.validated_identity.data_version:
            raise ValueError("working plan data identity must match the validated identity")
        confirmed = (
            ("session_reference_plan", self.session_reference_plan),
            ("what_if", self.what_if),
        )
        for label, state in confirmed:
            if state is not None and state.validated_identity != self.validated_identity:
                raise ValueError(
                    f"{label} is stale under the currently validated deployment/data identity"
                )
        if (
            self.dirty_attempt is not None
            and self.dirty_attempt.input.data_version
            != self.validated_identity.data_version
        ):
            raise ValueError("dirty attempt data identity must match validated identity")
        return self
