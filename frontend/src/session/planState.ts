import { ApiClientError } from '../api/client'
import type {
  BoundaryResolutionInput,
  FundingPlanSuccessEnvelope,
} from '../api/contracts'
import {
  cloneBoundaryResolutions,
  cloneFundingPlanInput,
  type BrowserSessionState,
  type SessionRequestError,
} from './contracts'
import { saveSession } from './storage'

function persist(session: BrowserSessionState): BrowserSessionState {
  saveSession(session)
  return session
}

function resetEvaluation(
  session: BrowserSessionState,
): BrowserSessionState {
  return {
    ...session,
    latest_plan_result: null,
    plan_fingerprint: null,
    plan_request: {
      ...session.plan_request,
      status: 'IDLE',
      error: null,
    },
  }
}

export function setWorkingBudget(
  session: BrowserSessionState,
  availableBudgetDollars: number,
): BrowserSessionState {
  return persist({
    ...resetEvaluation(session),
    working_plan: {
      ...cloneFundingPlanInput(session.working_plan),
      available_budget_dollars: availableBudgetDollars,
      boundary_resolutions: [],
      expected_fingerprint: null,
    },
  })
}

export function clearExpectedPlanFingerprint(
  session: BrowserSessionState,
): BrowserSessionState {
  return persist({
    ...session,
    working_plan: {
      ...cloneFundingPlanInput(session.working_plan),
      expected_fingerprint: null,
    },
    plan_request: {
      ...session.plan_request,
      status: 'IDLE',
      error: null,
    },
  })
}

export function setBoundaryResolutions(
  session: BrowserSessionState,
  resolutions: BoundaryResolutionInput[],
): BrowserSessionState {
  return persist({
    ...session,
    working_plan: {
      ...cloneFundingPlanInput(session.working_plan),
      boundary_resolutions: cloneBoundaryResolutions(resolutions),
      expected_fingerprint: null,
    },
    plan_request: {
      ...session.plan_request,
      status: 'IDLE',
      error: null,
    },
  })
}

export interface StartedPlanRequest {
  session: BrowserSessionState
  generation: number
}

export function beginPlanRequest(
  session: BrowserSessionState,
): StartedPlanRequest {
  const generation = session.plan_request.generation + 1
  const next = persist({
    ...session,
    plan_request: {
      status: 'LOADING',
      generation,
      error: null,
    },
  })

  return { session: next, generation }
}

function internalError(
  errorCode: string,
  message: string,
): SessionRequestError {
  return {
    kind: 'UNEXPECTED_PAYLOAD',
    status: null,
    error_code: errorCode,
    message,
    field_path: [],
    retryable: false,
    response_identity: null,
  }
}

export function sessionRequestError(error: unknown): SessionRequestError {
  if (error instanceof ApiClientError) {
    return {
      kind:
        error.kind === 'REQUEST_ABORTED'
          ? 'NETWORK_ERROR'
          : error.kind,
      status: error.status,
      error_code: error.errorCode ?? 'REQUEST_FAILED',
      message: error.message,
      field_path: [...error.fieldPath],
      retryable: error.retryable,
      response_identity: error.identity,
    }
  }

  return {
    kind: 'UNEXPECTED_PAYLOAD',
    status: null,
    error_code: 'UNEXPECTED_FAILURE',
    message:
      error instanceof Error
        ? error.message
        : 'Funding Plan evaluation failed unexpectedly.',
    field_path: [],
    retryable: false,
    response_identity: null,
  }
}

export function applyPlanSuccess(
  session: BrowserSessionState,
  response: FundingPlanSuccessEnvelope,
  generation: number,
): BrowserSessionState {
  if (generation !== session.plan_request.generation) return session

  if (
    response.identity.data_version !== session.runtime_identity.data_version ||
    response.identity.release_id !== session.runtime_identity.release_id
  ) {
    return persist({
      ...session,
      latest_plan_result: null,
      plan_fingerprint: null,
      plan_request: {
        status: 'ERROR',
        generation,
        error: internalError(
          'STALE_RUNTIME_RESPONSE',
          'Funding Plan response belongs to a different runtime release.',
        ),
      },
    })
  }

  return persist({
    ...session,
    working_plan: {
      ...cloneFundingPlanInput(session.working_plan),
      expected_fingerprint: response.data.plan_fingerprint,
    },
    latest_plan_result: {
      ...response.data,
      selected_projects: response.data.selected_projects.map((project) => ({
        ...project,
      })),
      unresolved_boundary:
        response.data.unresolved_boundary === null
          ? null
          : {
              ...response.data.unresolved_boundary,
              candidates: response.data.unresolved_boundary.candidates.map(
                (candidate) => ({ ...candidate }),
              ),
            },
      warnings: response.data.warnings.map((warning) => ({
        ...warning,
        decision_unit_ids: [...warning.decision_unit_ids],
      })),
      applied_analyst_overrides:
        response.data.applied_analyst_overrides.map((override) => ({
          ...override,
          decision_unit_ids_left_feasible: [
            ...override.decision_unit_ids_left_feasible,
          ],
        })),
    },
    plan_fingerprint: response.data.plan_fingerprint,
    plan_request: {
      status: 'SUCCESS',
      generation,
      error: null,
    },
  })
}

export function applyPlanFailure(
  session: BrowserSessionState,
  error: unknown,
  generation: number,
): BrowserSessionState {
  if (generation !== session.plan_request.generation) return session

  return persist({
    ...session,
    plan_request: {
      status: 'ERROR',
      generation,
      error: sessionRequestError(error),
    },
  })
}

export function cancelPlanRequest(
  session: BrowserSessionState,
  generation: number,
): BrowserSessionState {
  if (generation !== session.plan_request.generation) return session

  return persist({
    ...session,
    plan_request: {
      status: 'IDLE',
      generation,
      error: null,
    },
  })
}
