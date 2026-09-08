import { afterEach, describe, expect, it, vi } from 'vitest'
import {
  ApiClientError,
  evaluateFundingPlan,
  fetchBootstrap,
  fetchHistoricalBenchmark,
} from './client'
import { FUNDING_PLAN_CONTRACT_VERSION } from './contracts'
import {
  TEST_DATA_VERSION,
  TEST_RELEASE_ID,
  benchmarkFixture,
  bootstrapFixture,
  planResultFixture,
  complete332PlanFixture,
} from '../test/bootstrapFixture'

function response(payload: unknown, status = 200): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    json: async () => payload,
  } as Response
}

function governedError(status: number, errorCode: string) {
  return response(
    {
      status: 'ERROR',
      identity: {
        request_id: '123e4567-e89b-12d3-a456-426614174099',
        api_namespace: '/api/v1',
        contract_version: FUNDING_PLAN_CONTRACT_VERSION,
        data_version: TEST_DATA_VERSION,
        release_id: TEST_RELEASE_ID,
      },
      error: {
        error_code: errorCode,
        message: 'Governed safe message.',
        field_path: ['available_budget_dollars'],
        retryable: status >= 500,
      },
    },
    status,
  )
}

afterEach(() => vi.unstubAllGlobals())

describe('cross-category API client', () => {
  it('loads and validates all 106 bootstrap projects from the standard endpoint', async () => {
    const fetchMock = vi.fn(async () => response(bootstrapFixture()))
    vi.stubGlobal('fetch', fetchMock)

    const result = await fetchBootstrap()

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/bootstrap',
      expect.objectContaining({ method: 'GET' }),
    )
    expect(result.data.catalog.projects).toHaveLength(106)
    expect(result.data.catalog.category_counts).toEqual({
      transportation: 9,
      parks_open_space: 22,
      watershed: 37,
      community_facilities: 38,
    })
    expect(result.data.catalog.governed_request_total_dollars).toBe(
      1_973_520_000,
    )
    expect(result.data.map_context).toMatchObject({
      mapped_project_count: 0,
      unmapped_project_count: 106,
      fabricated_geometry: false,
      project_identity_key: 'decision_unit_id',
    })
  })

  it('preserves half-point Funding Priority scores and decision-unit identity', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => response(bootstrapFixture())))

    const result = await fetchBootstrap()
    const project = result.data.catalog.projects.find(
      (entry) => entry.funding_priority_score === 54.5,
    )

    expect(project?.decision_unit_id).toBe(
      'parks-open-space/fixture/project-17',
    )
    expect(project?.canonical_project_id).toBeNull()
    expect(project?.funding_priority_score).toBe(54.5)
  })

  it('posts only the governed v2 Funding Plan input to the standard endpoint', async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        void input
        void init
        return response(planResultFixture())
      },
    )
    vi.stubGlobal('fetch', fetchMock)
    const input = {
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      available_budget_dollars: 332_000_000,
      boundary_resolutions: [],
      expected_fingerprint: null,
    }

    const result = await evaluateFundingPlan(input)
    const init = fetchMock.mock.calls[0]?.[1]

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/plans/evaluate',
      expect.objectContaining({ method: 'POST' }),
    )
    expect(JSON.parse(String(init?.body))).toEqual(input)
    expect(String(init?.body)).not.toMatch(/benchmark|project_ids|reference/)
    expect(result.data.selected_projects[0].funding_priority_score).toBe(54.5)
  })

  it('loads the isolated historical benchmark from the standard endpoint', async () => {
    const fetchMock = vi.fn(
      async (input: RequestInfo | URL, init?: RequestInit) => {
        void input
        void init
        return response(benchmarkFixture())
      },
    )
    vi.stubGlobal('fetch', fetchMock)

    const result = await fetchHistoricalBenchmark()

    expect(fetchMock).toHaveBeenCalledWith(
      '/api/v1/benchmark',
      expect.objectContaining({ method: 'GET' }),
    )
    expect(fetchMock.mock.calls[0]?.[0]).not.toBe('/api/v1/benchmark/compare')
    expect(result.data.benchmark).toMatchObject({
      full_initial_recommendation_dollars: 700_000_000,
      matched_analytical_cohort_dollars: 332_000_000,
      outside_analytical_cohort_dollars: 368_000_000,
      historically_recommended_project_count: 20,
      ranking_input: false,
      portfolio_selection_input: false,
    })
  })

  it('rejects benchmark outcome membership that does not reconcile to its dollars', async () => {
    const payload = benchmarkFixture()
    const recommended = payload.data.benchmark.project_outcomes.find(
      (outcome) => outcome.historically_recommended,
    )
    if (recommended === undefined) throw new Error('Missing fixture outcome.')
    recommended.historically_recommended = false

    vi.stubGlobal('fetch', vi.fn(async () => response(payload)))

    const error = await fetchHistoricalBenchmark().catch(
      (caught: unknown) => caught,
    )

    expect(error).toMatchObject({
      kind: 'UNEXPECTED_PAYLOAD',
      status: 200,
      errorCode: 'UNEXPECTED_PAYLOAD',
    })
  })

  it.each([
    [409, 'DATA_VERSION_CONFLICT'],
    [409, 'CONTRACT_VERSION_CONFLICT'],
    [422, 'UNKNOWN_FIELD'],
    [413, 'BODY_TOO_LARGE'],
    [503, 'OPTIONAL_DEPENDENCY_UNAVAILABLE'],
  ])('preserves structured HTTP %i errors', async (status, errorCode) => {
    vi.stubGlobal('fetch', vi.fn(async () => governedError(status, errorCode)))

    const error = await fetchBootstrap().catch((caught: unknown) => caught)

    expect(error).toBeInstanceOf(ApiClientError)
    expect(error).toMatchObject({
      kind: 'API_ERROR',
      status,
      errorCode,
      fieldPath: ['available_budget_dollars'],
      retryable: status >= 500,
      identity: expect.objectContaining({ release_id: TEST_RELEASE_ID }),
    })
  })

  it('distinguishes backend-unavailable failures from governed API errors', async () => {
    vi.stubGlobal('fetch', vi.fn(async () => Promise.reject(new TypeError('offline'))))

    const error = await fetchBootstrap().catch((caught: unknown) => caught)

    expect(error).toMatchObject({
      kind: 'NETWORK_ERROR',
      status: null,
      errorCode: 'BACKEND_UNAVAILABLE',
      retryable: true,
    })
  })

  it('rejects malformed success payloads without treating them as governed errors', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => response({ status: 'SUCCESS', data: {} })),
    )

    const error = await fetchBootstrap().catch((caught: unknown) => caught)

    expect(error).toMatchObject({
      kind: 'UNEXPECTED_PAYLOAD',
      status: 200,
      errorCode: 'UNEXPECTED_PAYLOAD',
    })
  })

  it('rejects a Funding Plan success whose selected projects do not reconcile', async () => {
    const payload = complete332PlanFixture()
    payload.data.selected_projects[0].model_request_dollars += 1
    vi.stubGlobal('fetch', vi.fn(async () => response(payload)))

    const error = await evaluateFundingPlan({
      contract_version: FUNDING_PLAN_CONTRACT_VERSION,
      data_version: TEST_DATA_VERSION,
      available_budget_dollars: 332_000_000,
      boundary_resolutions: [],
      expected_fingerprint: null,
    }).catch((caught: unknown) => caught)

    expect(error).toMatchObject({
      kind: 'UNEXPECTED_PAYLOAD',
      status: 200,
      errorCode: 'UNEXPECTED_PAYLOAD',
    })
  })
})
