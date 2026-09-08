import { describe, expect, it, vi } from 'vitest'
import { FUNDING_PLAN_CONTRACT_VERSION } from '../api/contracts'
import {
  TEST_DATA_VERSION,
  planResultFixture,
} from '../test/bootstrapFixture'
import { PlanRequestCoordinator } from './planRequests'

function deferred<T>() {
  let resolve!: (value: T) => void
  let reject!: (reason?: unknown) => void
  const promise = new Promise<T>((resolvePromise, rejectPromise) => {
    resolve = resolvePromise
    reject = rejectPromise
  })
  return { promise, resolve, reject }
}

const input = {
  contract_version: FUNDING_PLAN_CONTRACT_VERSION,
  data_version: TEST_DATA_VERSION,
  available_budget_dollars: 332_000_000,
  boundary_resolutions: [],
  expected_fingerprint: null,
}

describe('PlanRequestCoordinator', () => {
  it('aborts the prior request and ignores its late response', async () => {
    const first = deferred<ReturnType<typeof planResultFixture>>()
    const second = deferred<ReturnType<typeof planResultFixture>>()
    const evaluator = vi
      .fn()
      .mockReturnValueOnce(first.promise)
      .mockReturnValueOnce(second.promise)
    const coordinator = new PlanRequestCoordinator(evaluator)
    const onSuccess = vi.fn()
    const onFailure = vi.fn()

    coordinator.evaluate(input, 1, { onSuccess, onFailure })
    const firstSignal = evaluator.mock.calls[0][1] as AbortSignal
    coordinator.evaluate(input, 2, { onSuccess, onFailure })

    expect(firstSignal.aborted).toBe(true)

    first.resolve(planResultFixture())
    second.resolve(planResultFixture())
    await Promise.resolve()
    await Promise.resolve()

    expect(onSuccess).toHaveBeenCalledOnce()
    expect(onSuccess).toHaveBeenCalledWith(expect.any(Object), 2)
    expect(onFailure).not.toHaveBeenCalled()
  })

  it('routes only the current request failure to the failure handler', async () => {
    const evaluator = vi.fn(async () => {
      throw new Error('failed')
    })
    const coordinator = new PlanRequestCoordinator(evaluator)
    const onFailure = vi.fn()

    coordinator.evaluate(input, 1, {
      onSuccess: vi.fn(),
      onFailure,
    })
    await Promise.resolve()
    await Promise.resolve()

    expect(onFailure).toHaveBeenCalledWith(expect.any(Error), 1)
  })
})
