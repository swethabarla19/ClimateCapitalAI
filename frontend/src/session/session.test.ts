import { beforeEach, describe, expect, it } from 'vitest'
import { ApiClientError } from '../api/client'
import { FUNDING_PLAN_CONTRACT_VERSION } from '../api/contracts'
import {
  TEST_RELEASE_ID,
  bootstrapFixture,
  planResultFixture,
} from '../test/bootstrapFixture'
import {
  DEFAULT_AVAILABLE_PROJECT_BUDGET_DOLLARS,
  createInitialSession,
  runtimeIdentityFromBootstrap,
} from './contracts'
import { initializeSessionFromBootstrap } from './initialize'
import {
  applyPlanFailure,
  applyPlanSuccess,
  beginPlanRequest,
  setBoundaryResolutions,
  setWorkingBudget,
} from './planState'
import { setPresentationRoute } from './presentation'
import {
  SESSION_STORAGE_KEY,
  loadStoredSessionCandidate,
  saveSession,
} from './storage'

beforeEach(() => {
  window.sessionStorage.clear()
  window.localStorage.clear()
})

describe('cross-category browser session', () => {
  it('starts with analyst input state rather than a fixed historical envelope', () => {
    const session = createInitialSession(bootstrapFixture())

    expect(session.runtime_identity.release_id).toBe(TEST_RELEASE_ID)
    expect(session.working_plan).toEqual({
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: session.runtime_identity.data_version,
      available_budget_dollars: DEFAULT_AVAILABLE_PROJECT_BUDGET_DOLLARS,
      boundary_resolutions: [],
      expected_fingerprint: null,
    })
    expect(session.latest_plan_result).toBeNull()
    expect(session.plan_fingerprint).toBeNull()
  })

  it('persists the v2 session only in sessionStorage', () => {
    const session = createInitialSession(bootstrapFixture())

    saveSession(session)

    expect(window.sessionStorage.getItem(SESSION_STORAGE_KEY)).not.toBeNull()
    expect(window.localStorage.getItem(SESSION_STORAGE_KEY)).toBeNull()
  })

  it('persists safe analyst inputs without treating an evaluation as durable', () => {
    let session = createInitialSession(bootstrapFixture())
    session = setWorkingBudget(session, 332_000_000)
    const started = beginPlanRequest(session)
    session = applyPlanSuccess(
      started.session,
      planResultFixture(),
      started.generation,
    )

    saveSession(session)

    const stored = JSON.parse(
      window.sessionStorage.getItem(SESSION_STORAGE_KEY) ?? '{}',
    )
    expect(stored.working_plan.available_budget_dollars).toBe(332_000_000)
    expect(stored.working_plan.expected_fingerprint).toBeNull()
    expect(stored.latest_plan_result).toBeNull()
    expect(stored.plan_fingerprint).toBeNull()
    expect(stored.plan_request.status).toBe('IDLE')
  })

  it('restores safe inputs for the same release but discards evaluated state', () => {
    let session = createInitialSession(bootstrapFixture())
    session = setWorkingBudget(session, 700_000_000)
    session = setBoundaryResolutions(session, [
      {
        funding_priority_score: 67,
        funding_priority_rank: 28,
        selected_decision_unit_ids: [
          'community-facilities/fixture/project-1',
        ],
        advance_with_feasible_same_tier_project_acknowledged: false,
      },
    ])
    const started = beginPlanRequest(session)
    session = applyPlanSuccess(
      started.session,
      planResultFixture(700_000_000),
      started.generation,
    )
    saveSession(session)

    const restored = initializeSessionFromBootstrap(bootstrapFixture())

    expect(restored.status).toBe('RESTORED_INPUTS')
    expect(restored.session.working_plan.available_budget_dollars).toBe(
      700_000_000,
    )
    expect(restored.session.working_plan.boundary_resolutions).toHaveLength(1)
    expect(restored.session.working_plan.expected_fingerprint).toBeNull()
    expect(restored.session.latest_plan_result).toBeNull()
    expect(restored.session.plan_fingerprint).toBeNull()
    expect(restored.session.plan_request.status).toBe('IDLE')
  })

  it('resets plan state across a release change while preserving view preferences', () => {
    const oldBootstrap = bootstrapFixture()
    let session = createInitialSession(oldBootstrap)
    session = setWorkingBudget(session, 750_000_000)
    session.presentation.search_text = 'library'
    session.presentation.filter_ids = ['old-project-filter']
    session.presentation.selected_decision_unit_id =
      'watershed/fixture/project-1'
    saveSession(session)

    const currentBootstrap = bootstrapFixture()
    currentBootstrap.identity.release_id = 'replacement-release'

    const result = initializeSessionFromBootstrap(currentBootstrap)

    expect(result.status).toBe('RESET_STALE')
    expect(result.session.runtime_identity.release_id).toBe('replacement-release')
    expect(result.session.working_plan.available_budget_dollars).toBe(0)
    expect(result.session.working_plan.boundary_resolutions).toEqual([])
    expect(result.session.presentation.search_text).toBe('library')
    expect(result.session.presentation.filter_ids).toEqual([])
    expect(result.session.presentation.selected_decision_unit_id).toBeNull()
  })

  it('fails closed on malformed stored JSON and ignores the retired v1 key', () => {
    window.sessionStorage.setItem(SESSION_STORAGE_KEY, '{not json')
    window.sessionStorage.setItem(
      'climatecapital:p0-browser-session/1.0.0',
      '{"legacy":true}',
    )

    const result = initializeSessionFromBootstrap(bootstrapFixture())

    expect(result.status).toBe('RESET_INVALID')
    expect(result.session.working_plan.available_budget_dollars).toBe(0)
  })

  it('compares persisted identity by data version, release, and catalog contract', () => {
    const bootstrap = bootstrapFixture()
    const session = createInitialSession(bootstrap)
    saveSession(session)

    expect(
      loadStoredSessionCandidate(runtimeIdentityFromBootstrap(bootstrap)).status,
    ).toBe('CANDIDATE')
  })

  it('persists presentation navigation without changing plan input', () => {
    const session = createInitialSession(bootstrapFixture())
    const next = setPresentationRoute(session, 'HISTORICAL_BENCHMARK')

    expect(next.presentation.route).toBe('HISTORICAL_BENCHMARK')
    expect(next.working_plan).toEqual(session.working_plan)
  })

  it('clears prior boundary decisions when the analyst changes the budget', () => {
    let session = createInitialSession(bootstrapFixture())
    session = setBoundaryResolutions(session, [
      {
        funding_priority_score: 67,
        funding_priority_rank: 28,
        selected_decision_unit_ids: ['parks/fixture/project-1'],
        advance_with_feasible_same_tier_project_acknowledged: true,
      },
    ])

    const next = setWorkingBudget(session, 750_000_000)

    expect(next.working_plan.boundary_resolutions).toEqual([])
    expect(next.working_plan.expected_fingerprint).toBeNull()
  })

  it('ignores a stale evaluation response after a newer request starts', () => {
    const initial = createInitialSession(bootstrapFixture())
    const first = beginPlanRequest(initial)
    const second = beginPlanRequest(first.session)

    const unchanged = applyPlanSuccess(
      second.session,
      planResultFixture(),
      first.generation,
    )

    expect(unchanged).toBe(second.session)
    expect(unchanged.latest_plan_result).toBeNull()
    expect(unchanged.plan_request.status).toBe('LOADING')
  })

  it('preserves structured API failure details in plan request state', () => {
    const started = beginPlanRequest(createInitialSession(bootstrapFixture()))
    const failed = applyPlanFailure(
      started.session,
      new ApiClientError('Version conflict.', {
        kind: 'API_ERROR',
        status: 409,
        errorCode: 'DATA_VERSION_CONFLICT',
        fieldPath: ['data_version'],
        retryable: false,
      }),
      started.generation,
    )

    expect(failed.plan_request.error).toEqual({
      kind: 'API_ERROR',
      status: 409,
      error_code: 'DATA_VERSION_CONFLICT',
      message: 'Version conflict.',
      field_path: ['data_version'],
      retryable: false,
      response_identity: null,
    })
  })

  it('keeps the last successful result visible when a retry fails', () => {
    const first = beginPlanRequest(createInitialSession(bootstrapFixture()))
    const succeeded = applyPlanSuccess(
      first.session,
      planResultFixture(),
      first.generation,
    )
    const retry = beginPlanRequest(succeeded)
    const failed = applyPlanFailure(
      retry.session,
      new Error('Temporary failure.'),
      retry.generation,
    )

    expect(failed.latest_plan_result).toEqual(succeeded.latest_plan_result)
    expect(failed.plan_fingerprint).toBe(succeeded.plan_fingerprint)
    expect(failed.plan_request.status).toBe('ERROR')
  })
})
