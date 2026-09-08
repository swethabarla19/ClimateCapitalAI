import {
  CATALOG_CONTRACT_VERSION,
  FUNDING_PLAN_CONTRACT_VERSION,
  type BoundaryResolutionInput,
} from '../api/contracts'
import {
  BROWSER_SESSION_CONTRACT_VERSION,
  type BrowserSessionState,
  type RuntimeIdentity,
} from './contracts'

export const SESSION_STORAGE_KEY =
  'climatecapital:p0-browser-session/2.0.0'

export type StoredSessionCandidate =
  | { status: 'MISSING'; session: null }
  | { status: 'INVALID'; session: null }
  | { status: 'STALE'; session: BrowserSessionState }
  | { status: 'CANDIDATE'; session: BrowserSessionState }

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isBoundaryResolution(value: unknown): value is BoundaryResolutionInput {
  return (
    isRecord(value) &&
    typeof value.funding_priority_score === 'number' &&
    Number.isFinite(value.funding_priority_score) &&
    typeof value.funding_priority_rank === 'number' &&
    Number.isInteger(value.funding_priority_rank) &&
    Array.isArray(value.selected_decision_unit_ids) &&
    value.selected_decision_unit_ids.every(
      (id) => typeof id === 'string',
    ) &&
    typeof value.advance_with_feasible_same_tier_project_acknowledged ===
      'boolean'
  )
}

function looksLikeBrowserSession(
  value: unknown,
): value is BrowserSessionState {
  if (
    !isRecord(value) ||
    value.contract_version !== BROWSER_SESSION_CONTRACT_VERSION ||
    !isRecord(value.runtime_identity) ||
    !isRecord(value.presentation) ||
    !isRecord(value.working_plan) ||
    !isRecord(value.plan_request)
  ) {
    return false
  }

  const identity = value.runtime_identity
  const presentation = value.presentation
  const plan = value.working_plan
  const request = value.plan_request

  return (
    typeof identity.data_version === 'string' &&
    typeof identity.release_id === 'string' &&
    identity.catalog_contract_version === CATALOG_CONTRACT_VERSION &&
    [
      'EXPLORE',
      'FUNDING_PLAN',
      'HISTORICAL_BENCHMARK',
      'DATA_METHODOLOGY',
      'HELP_RESOURCES',
    ].includes(
      String(presentation.route),
    ) &&
    typeof presentation.search_text === 'string' &&
    Array.isArray(presentation.filter_ids) &&
    presentation.filter_ids.every((id) => typeof id === 'string') &&
    ['FUNDING_PRIORITY', 'NAME', 'REQUEST_ASC', 'REQUEST_DESC'].includes(
      String(presentation.sort),
    ) &&
    (typeof presentation.selected_decision_unit_id === 'string' ||
      presentation.selected_decision_unit_id === null) &&
    typeof presentation.list_position === 'number' &&
    Number.isInteger(presentation.list_position) &&
    plan.contract_version === FUNDING_PLAN_CONTRACT_VERSION &&
    typeof plan.data_version === 'string' &&
    typeof plan.available_budget_dollars === 'number' &&
    Number.isInteger(plan.available_budget_dollars) &&
    plan.available_budget_dollars >= 0 &&
    Array.isArray(plan.boundary_resolutions) &&
    plan.boundary_resolutions.every(isBoundaryResolution) &&
    (typeof plan.expected_fingerprint === 'string' ||
      plan.expected_fingerprint === null) &&
    ['IDLE', 'LOADING', 'SUCCESS', 'ERROR'].includes(String(request.status)) &&
    typeof request.generation === 'number' &&
    Number.isInteger(request.generation)
  )
}

export function sameRuntimeIdentity(
  left: RuntimeIdentity,
  right: RuntimeIdentity,
): boolean {
  return (
    left.data_version === right.data_version &&
    left.release_id === right.release_id &&
    left.catalog_contract_version === right.catalog_contract_version
  )
}

export function saveSession(session: BrowserSessionState): void {
  const safeStoredSession: BrowserSessionState = {
    ...session,
    working_plan: {
      ...session.working_plan,
      boundary_resolutions: session.working_plan.boundary_resolutions.map(
        (resolution) => ({
          ...resolution,
          selected_decision_unit_ids: [
            ...resolution.selected_decision_unit_ids,
          ],
        }),
      ),
      expected_fingerprint: null,
    },
    latest_plan_result: null,
    plan_fingerprint: null,
    plan_request: {
      status: 'IDLE',
      generation: 0,
      error: null,
    },
  }

  window.sessionStorage.setItem(
    SESSION_STORAGE_KEY,
    JSON.stringify(safeStoredSession),
  )
}

export function clearSession(): void {
  window.sessionStorage.removeItem(SESSION_STORAGE_KEY)
}

export function loadStoredSessionCandidate(
  currentIdentity: RuntimeIdentity,
): StoredSessionCandidate {
  const raw = window.sessionStorage.getItem(SESSION_STORAGE_KEY)

  if (raw === null) return { status: 'MISSING', session: null }

  let parsed: unknown

  try {
    parsed = JSON.parse(raw)
  } catch {
    return { status: 'INVALID', session: null }
  }

  if (!looksLikeBrowserSession(parsed)) {
    return { status: 'INVALID', session: null }
  }

  if (!sameRuntimeIdentity(parsed.runtime_identity, currentIdentity)) {
    return { status: 'STALE', session: parsed }
  }

  return { status: 'CANDIDATE', session: parsed }
}
