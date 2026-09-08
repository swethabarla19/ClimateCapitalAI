import {
  CATALOG_CONTRACT_VERSION,
  FUNDING_PLAN_CONTRACT_VERSION,
  type BootstrapSuccessEnvelope,
  type BoundaryResolutionInput,
  type FundingPlanInput,
  type FundingPlanResult,
  type ResponseIdentity,
} from '../api/contracts'

export const BROWSER_SESSION_CONTRACT_VERSION =
  'p0-browser-session/2.0.0' as const

export const DEFAULT_AVAILABLE_PROJECT_BUDGET_DOLLARS = 0

export interface RuntimeIdentity {
  data_version: string
  release_id: string
  catalog_contract_version: typeof CATALOG_CONTRACT_VERSION
}

export interface PresentationState {
  route:
    | 'EXPLORE'
    | 'FUNDING_PLAN'
    | 'HISTORICAL_BENCHMARK'
    | 'DATA_METHODOLOGY'
    | 'HELP_RESOURCES'
  search_text: string
  filter_ids: string[]
  sort:
    | 'FUNDING_PRIORITY'
    | 'NAME'
    | 'REQUEST_ASC'
    | 'REQUEST_DESC'
  selected_decision_unit_id: string | null
  list_position: number
}

export type RequestStatus = 'IDLE' | 'LOADING' | 'SUCCESS' | 'ERROR'

export interface SessionRequestError {
  kind: 'API_ERROR' | 'NETWORK_ERROR' | 'UNEXPECTED_PAYLOAD'
  status: number | null
  error_code: string
  message: string
  field_path: Array<string | number>
  retryable: boolean
  response_identity: ResponseIdentity | null
}

export interface PlanRequestState {
  status: RequestStatus
  generation: number
  error: SessionRequestError | null
}

export interface BrowserSessionState {
  contract_version: typeof BROWSER_SESSION_CONTRACT_VERSION
  runtime_identity: RuntimeIdentity
  presentation: PresentationState
  working_plan: FundingPlanInput
  latest_plan_result: FundingPlanResult | null
  plan_fingerprint: string | null
  plan_request: PlanRequestState
}

export function runtimeIdentityFromBootstrap(
  bootstrap: BootstrapSuccessEnvelope,
): RuntimeIdentity {
  return {
    data_version: bootstrap.identity.data_version,
    release_id: bootstrap.identity.release_id,
    catalog_contract_version: CATALOG_CONTRACT_VERSION,
  }
}

export function cloneBoundaryResolutions(
  resolutions: BoundaryResolutionInput[],
): BoundaryResolutionInput[] {
  return resolutions.map((resolution) => ({
    ...resolution,
    selected_decision_unit_ids: [
      ...resolution.selected_decision_unit_ids,
    ],
  }))
}

export function cloneFundingPlanInput(
  input: FundingPlanInput,
): FundingPlanInput {
  return {
    ...input,
    boundary_resolutions: cloneBoundaryResolutions(
      input.boundary_resolutions,
    ),
  }
}

export function createInitialSession(
  bootstrap: BootstrapSuccessEnvelope,
): BrowserSessionState {
  const identity = runtimeIdentityFromBootstrap(bootstrap)

  return {
    contract_version: BROWSER_SESSION_CONTRACT_VERSION,
    runtime_identity: identity,
    presentation: {
      route: 'EXPLORE',
      search_text: '',
      filter_ids: [],
      sort: 'FUNDING_PRIORITY',
      selected_decision_unit_id: null,
      list_position: 0,
    },
    working_plan: {
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: identity.data_version,
      available_budget_dollars:
        DEFAULT_AVAILABLE_PROJECT_BUDGET_DOLLARS,
      boundary_resolutions: [],
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
}
