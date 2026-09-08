import { useState } from 'react'
import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ApiClientError } from '../api/client'
import type { FundingPlanSuccessEnvelope } from '../api/contracts'
import { createInitialSession } from '../session/contracts'
import type { FundingPlanEvaluator } from '../session/planRequests'
import {
  bootstrapFixture,
  boundary700PlanFixture,
  boundary750PlanFixture,
  complete332PlanFixture,
  planResultFixture,
  resolved700PlanFixture,
  runtimeProjectsFixture,
} from '../test/bootstrapFixture'
import { FundingPlan } from './FundingPlan'

interface HarnessProps {
  evaluator: FundingPlanEvaluator
  onReloadRuntime?: () => void
}

function Harness({ evaluator, onReloadRuntime = vi.fn() }: HarnessProps) {
  const bootstrap = bootstrapFixture()
  const [session, setSession] = useState(() => createInitialSession(bootstrap))

  return (
    <FundingPlan
      catalog={bootstrap.data.catalog}
      session={session}
      onSessionChange={setSession}
      evaluator={evaluator}
      onReloadRuntime={onReloadRuntime}
    />
  )
}

function deferred<T>() {
  let resolve!: (value: T) => void
  const promise = new Promise<T>((resolvePromise) => {
    resolve = resolvePromise
  })
  return { promise, resolve }
}

beforeEach(() => window.sessionStorage.clear())

describe('Funding Plan', () => {
  it('evaluates the $332M matched-cohort preset and presents remaining budget neutrally', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async () =>
      complete332PlanFixture(),
    )
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$332m historical matched-cohort reference/i,
      }),
    )

    expect(
      await screen.findByRole('heading', { name: /plan evaluation complete/i }),
    ).toBeInTheDocument()

    expect(evaluator).toHaveBeenCalledWith(
      expect.objectContaining({
        available_budget_dollars: 332_000_000,
        boundary_resolutions: [],
        expected_fingerprint: null,
      }),
      expect.any(AbortSignal),
    )

    const summary = screen.getByRole('region', { name: /plan summary/i })
    expect(summary).toHaveTextContent('$331,825,000')
    expect(summary).toHaveTextContent('$175,000')
    expect(summary).toHaveTextContent('18')
    expect(summary).toHaveTextContent('99.9%')
    expect(screen.getByRole('progressbar', { name: /budget utilization/i })).toHaveAttribute(
      'value',
      '331825000',
    )
    expect(document.body).not.toHaveTextContent(/optimization failure|wasted budget/i)
    expect(screen.queryByRole('button', { name: /add .* to plan/i })).toBeNull()

    const sentInput = evaluator.mock.calls[0][0]
    expect(JSON.stringify(sentInput)).not.toMatch(/benchmark|project_ids/)
  })

  it('shows the $700M score-67 rank-28 boundary with all feasible tied candidates unselected', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async () =>
      boundary700PlanFixture(),
    )
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )

    const boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    expect(boundary).toHaveTextContent('67')
    expect(boundary).toHaveTextContent('Rank 28')
    expect(boundary).toHaveTextContent('$108,275,000')
    expect(boundary).toHaveTextContent('5 individually feasible')

    const checkboxes = within(boundary).getAllByRole('checkbox', {
      name: /select .* for analyst resolution/i,
    })
    expect(checkboxes).toHaveLength(5)
    expect(checkboxes.every((checkbox) => !checkbox.hasAttribute('checked'))).toBe(
      true,
    )
    expect(boundary).toHaveTextContent(/no analytical preference is assigned/i)
  })

  it('shows the $750M score-65 rank-37 boundary', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async () =>
      boundary750PlanFixture(),
    )
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$750m pre-snapshot citywide financial-capacity reference/i,
      }),
    )

    const boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    expect(boundary).toHaveTextContent('65')
    expect(boundary).toHaveTextContent('Rank 37')
    expect(boundary).toHaveTextContent('$33,280,000')
    expect(
      within(boundary).getAllByRole('checkbox', {
        name: /select .* for analyst resolution/i,
      }),
    ).toHaveLength(8)
  })

  it('submits an analyst-entered custom whole-dollar budget', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async (input) =>
      planResultFixture(input.available_budget_dollars),
    )
    render(<Harness evaluator={evaluator} />)

    const input = screen.getByLabelText('Custom Available Project Budget')
    await user.clear(input)
    await user.type(input, '$123,456,789')
    await user.click(
      screen.getByRole('button', { name: /evaluate custom budget/i }),
    )

    expect(evaluator).toHaveBeenCalledWith(
      expect.objectContaining({ available_budget_dollars: 123_456_789 }),
      expect.any(AbortSignal),
    )
  })

  it('joins selected and boundary records to catalog names by decision_unit_id', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async () =>
      boundary700PlanFixture(),
    )
    const projects = runtimeProjectsFixture()
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )

    expect(
      await screen.findByText(projects[0].governed_name),
    ).toBeInTheDocument()
    expect(screen.getByText(projects[30].governed_name)).toBeInTheDocument()
    expect(screen.getAllByText(/Rank 2/).length).toBeGreaterThan(1)
  })

  it('submits the exact boundary resolution and requires explicit same-tier acknowledgement', async () => {
    const user = userEvent.setup()
    const boundaryResponse = boundary700PlanFixture()
    const candidate = boundaryResponse.data.unresolved_boundary?.candidates[1]
    if (candidate === undefined) throw new Error('Missing boundary candidate fixture.')

    const evaluator = vi
      .fn<FundingPlanEvaluator>()
      .mockResolvedValueOnce(boundaryResponse)
      .mockResolvedValueOnce(
        resolved700PlanFixture([candidate.decision_unit_id], true),
      )
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )

    const boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    await user.click(
      within(boundary).getByRole('checkbox', {
        name: new RegExp(`select .*${candidate.model_request_dollars / 1_000_000}.*analyst resolution`, 'i'),
      }),
    )

    const submit = within(boundary).getByRole('button', {
      name: /submit analyst resolution/i,
    })
    expect(submit).toBeDisabled()

    await user.click(
      within(boundary).getByRole('checkbox', {
        name: /leaving at least one budget-feasible project/i,
      }),
    )
    await user.click(submit)

    expect(evaluator.mock.calls[1][0]).toEqual(
      expect.objectContaining({
        available_budget_dollars: 700_000_000,
        expected_fingerprint: null,
        boundary_resolutions: [
          {
            funding_priority_score: 67,
            funding_priority_rank: 28,
            selected_decision_unit_ids: [candidate.decision_unit_id],
            advance_with_feasible_same_tier_project_acknowledged: true,
          },
        ],
      }),
    )

    expect(
      await screen.findByRole('heading', { name: /plan evaluation complete/i }),
    ).toBeInTheDocument()
    expect(screen.getByText(/analyst acknowledgement applied/i)).toBeInTheDocument()
  })

  it('blocks an obviously over-budget boundary choice locally', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn<FundingPlanEvaluator>(async () =>
      boundary700PlanFixture(),
    )
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )
    const boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })

    for (const checkbox of within(boundary).getAllByRole('checkbox', {
      name: /select .* for analyst resolution/i,
    })) {
      await user.click(checkbox)
    }

    expect(boundary).toHaveTextContent(/exceeds the boundary budget by \$4,725,000/i)
    expect(
      within(boundary).getByRole('button', {
        name: /submit analyst resolution/i,
      }),
    ).toBeDisabled()
    expect(evaluator).toHaveBeenCalledTimes(1)
  })

  it('does not require an override acknowledgement when no same-tier project remains feasible', async () => {
    const user = userEvent.setup()
    const boundaryResponse = boundary700PlanFixture()
    const candidates = boundaryResponse.data.unresolved_boundary?.candidates
    if (candidates === undefined) throw new Error('Missing boundary fixture.')
    const selectedIds = candidates.slice(0, 3).map(
      (candidate) => candidate.decision_unit_id,
    )
    const evaluator = vi
      .fn<FundingPlanEvaluator>()
      .mockResolvedValueOnce(boundaryResponse)
      .mockResolvedValueOnce(resolved700PlanFixture(selectedIds, false))
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )
    const boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    const checkboxes = within(boundary).getAllByRole('checkbox', {
      name: /select .* for analyst resolution/i,
    })
    await user.click(checkboxes[0])
    await user.click(checkboxes[1])
    await user.click(checkboxes[2])

    expect(
      within(boundary).queryByRole('checkbox', {
        name: /leaving at least one budget-feasible project/i,
      }),
    ).toBeNull()
    await user.click(
      within(boundary).getByRole('button', {
        name: /submit analyst resolution/i,
      }),
    )

    expect(evaluator.mock.calls[1][0].boundary_resolutions[0]).toEqual({
      funding_priority_score: 67,
      funding_priority_rank: 28,
      selected_decision_unit_ids: [...selectedIds].sort(),
      advance_with_feasible_same_tier_project_acknowledged: false,
    })
  })

  it('retains accumulated resolutions when the backend returns a later boundary tier', async () => {
    const user = userEvent.setup()
    const firstBoundary = boundary700PlanFixture()
    const firstCandidates = firstBoundary.data.unresolved_boundary?.candidates
    if (firstCandidates === undefined) throw new Error('Missing first boundary.')
    const firstSelectedIds = firstCandidates.slice(0, 3).map(
      (candidate) => candidate.decision_unit_id,
    )
    const secondBoundary = resolved700PlanFixture(firstSelectedIds, false)
    const laterProjects = runtimeProjectsFixture().slice(50, 52)
    secondBoundary.data.status = 'ANALYST_RESOLUTION_REQUIRED'
    secondBoundary.data.unresolved_boundary = {
      funding_priority_score: 65,
      funding_priority_rank: 37,
      remaining_budget_before_tier_dollars: 775_000,
      full_tier_request_dollars: 800_000,
      candidates: laterProjects.map((project) => ({
        decision_unit_id: project.decision_unit_id,
        model_request_dollars: 400_000,
        funding_priority_score: 65,
        funding_priority_rank: 37,
        individually_budget_feasible: true,
      })),
    }
    secondBoundary.data.plan_fingerprint = 'e'.repeat(64)

    const evaluator = vi
      .fn<FundingPlanEvaluator>()
      .mockResolvedValueOnce(firstBoundary)
      .mockResolvedValueOnce(secondBoundary)
      .mockResolvedValueOnce(resolved700PlanFixture(firstSelectedIds, false))
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )
    let boundary = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    const firstCheckboxes = within(boundary).getAllByRole('checkbox', {
      name: /select .* for analyst resolution/i,
    })
    await user.click(firstCheckboxes[0])
    await user.click(firstCheckboxes[1])
    await user.click(firstCheckboxes[2])
    await user.click(
      within(boundary).getByRole('button', {
        name: /submit analyst resolution/i,
      }),
    )

    await waitFor(() => {
      expect(
        screen.getByRole('region', { name: /boundary priority tier/i }),
      ).toHaveTextContent('Rank 37')
    })
    boundary = screen.getByRole('region', { name: /boundary priority tier/i })
    await user.click(
      within(boundary).getAllByRole('checkbox', {
        name: /select .* for analyst resolution/i,
      })[0],
    )
    await user.click(
      within(boundary).getByRole('button', {
        name: /submit analyst resolution/i,
      }),
    )

    expect(evaluator.mock.calls[2][0].boundary_resolutions).toHaveLength(2)
    expect(
      evaluator.mock.calls[2][0].boundary_resolutions.map(
        (resolution) => resolution.funding_priority_rank,
      ),
    ).toEqual([28, 37])
  })

  it('shows every boundary candidate and distinguishes backend-marked infeasibility', async () => {
    const user = userEvent.setup()
    const response = boundary700PlanFixture()
    const boundary = response.data.unresolved_boundary
    if (boundary === null) throw new Error('Missing boundary fixture.')
    boundary.candidates[0].model_request_dollars = 120_000_000
    boundary.candidates[0].individually_budget_feasible = false
    boundary.full_tier_request_dollars = 172_500_000
    const evaluator = vi.fn<FundingPlanEvaluator>().mockResolvedValue(response)
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )

    const panel = await screen.findByRole('region', {
      name: /boundary priority tier/i,
    })
    expect(
      within(panel).getAllByRole('checkbox', {
        name: /select .* for analyst resolution/i,
      }),
    ).toHaveLength(5)
    expect(
      within(panel).getByRole('checkbox', { name: /\$120,000,000/i }),
    ).toBeDisabled()
    expect(panel).toHaveTextContent(/does not fit individually/i)
    expect(panel).toHaveTextContent('4 individually feasible')
  })

  it('lets a newer budget evaluation replace an older in-flight response', async () => {
    const user = userEvent.setup()
    const first = deferred<FundingPlanSuccessEnvelope>()
    const second = deferred<FundingPlanSuccessEnvelope>()
    const evaluator = vi
      .fn<FundingPlanEvaluator>()
      .mockReturnValueOnce(first.promise)
      .mockReturnValueOnce(second.promise)
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$332m historical matched-cohort reference/i,
      }),
    )
    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )

    second.resolve(boundary700PlanFixture())
    expect(
      await screen.findByRole('region', { name: /boundary priority tier/i }),
    ).toBeInTheDocument()

    first.resolve(complete332PlanFixture())
    await Promise.resolve()
    expect(
      screen.getByRole('region', { name: /boundary priority tier/i }),
    ).toHaveTextContent('Rank 28')
    expect(screen.queryByText('$175,000')).toBeNull()
  })

  it('shows backend-unavailable recovery and retries the same analyst input', async () => {
    const user = userEvent.setup()
    const evaluator = vi
      .fn<FundingPlanEvaluator>()
      .mockRejectedValueOnce(
        new ApiClientError('The ClimateCapital API is unavailable.', {
          kind: 'NETWORK_ERROR',
          errorCode: 'BACKEND_UNAVAILABLE',
          retryable: true,
        }),
      )
      .mockResolvedValueOnce(complete332PlanFixture())
    render(<Harness evaluator={evaluator} />)

    await user.click(
      screen.getByRole('button', {
        name: /\$332m historical matched-cohort reference/i,
      }),
    )

    expect(
      await screen.findByRole('heading', {
        name: /funding plan service unavailable/i,
      }),
    ).toBeInTheDocument()
    await user.click(screen.getByRole('button', { name: /retry evaluation/i }))

    expect(
      await screen.findByRole('heading', { name: /plan evaluation complete/i }),
    ).toBeInTheDocument()
    expect(evaluator).toHaveBeenCalledTimes(2)
  })

  it('uses governed conflict recovery and rejects unsupported custom amounts', async () => {
    const user = userEvent.setup()
    const onReloadRuntime = vi.fn()
    const evaluator = vi.fn<FundingPlanEvaluator>().mockRejectedValue(
      new ApiClientError('Data version conflict.', {
        kind: 'API_ERROR',
        status: 409,
        errorCode: 'DATA_VERSION_CONFLICT',
      }),
    )
    render(
      <Harness evaluator={evaluator} onReloadRuntime={onReloadRuntime} />,
    )

    const custom = screen.getByLabelText('Custom Available Project Budget')
    await user.clear(custom)
    await user.type(custom, '1973520001')
    expect(screen.getByText(/cannot exceed \$1,973,520,000/i)).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: /evaluate custom budget/i }),
    ).toBeDisabled()

    await user.click(
      screen.getByRole('button', {
        name: /\$700m full january initial draft recommendation reference/i,
      }),
    )
    expect(
      await screen.findByRole('heading', { name: /runtime data changed/i }),
    ).toBeInTheDocument()
    await user.click(
      screen.getByRole('button', { name: /reload governed runtime/i }),
    )
    expect(onReloadRuntime).toHaveBeenCalledOnce()
  })
})
