import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { ApiClientError } from '../api/client'
import type {
  FundingPlanResult,
  HistoricalBenchmarkSuccessEnvelope,
} from '../api/contracts'
import {
  benchmarkFixture,
  bootstrapFixture,
  complete332PlanFixture,
} from '../test/bootstrapFixture'
import { HistoricalBenchmark } from './HistoricalBenchmark'

function renderBenchmark(options?: {
  loader?: () => Promise<HistoricalBenchmarkSuccessEnvelope>
  currentPlan?: FundingPlanResult | null
}) {
  const bootstrap = bootstrapFixture()
  const loader = options?.loader ?? (async () => benchmarkFixture())

  render(
    <HistoricalBenchmark
      catalog={bootstrap.data.catalog}
      runtimeIdentity={{
        data_version: bootstrap.identity.data_version,
        release_id: bootstrap.identity.release_id,
        catalog_contract_version: bootstrap.data.catalog.contract_version,
      }}
      currentPlan={options?.currentPlan ?? null}
      loader={loader}
    />,
  )
}

describe('January 21 Historical Benchmark', () => {
  it('loads independently and presents the governed historical reconciliation', async () => {
    const loader = vi.fn(async () => benchmarkFixture())
    renderBenchmark({ loader })

    expect(screen.getByRole('status')).toHaveTextContent(
      /loading historical benchmark/i,
    )
    expect(
      await screen.findByRole('heading', {
        name: 'January 21, 2026 Historical Benchmark',
      }),
    ).toBeInTheDocument()
    expect(loader).toHaveBeenCalledTimes(1)
    expect(screen.getByText('$700M')).toBeInTheDocument()
    expect(screen.getByText('$332M')).toBeInTheDocument()
    expect(screen.getByText('$368M')).toBeInTheDocument()
    expect(screen.getByText('20', { selector: '.benchmark-stat-value' })).toBeInTheDocument()
    expect(screen.getByText('$332M + $368M = $700M')).toBeInTheDocument()
  })

  it('renders category summaries from benchmark data as historical context', async () => {
    renderBenchmark()

    const categories = await screen.findByRole('region', {
      name: 'Historical category context',
    })
    const transportation = within(categories).getByRole('article', {
      name: 'Transportation historical context',
    })

    expect(within(transportation).getByText('$28M')).toBeInTheDocument()
    expect(within(transportation).getByText('2 of 9')).toBeInTheDocument()
    expect(within(categories).getByText('$55M')).toBeInTheDocument()
    expect(within(categories).getByText('$125M')).toBeInTheDocument()
    expect(within(categories).getByText('$124M')).toBeInTheDocument()
    expect(categories).toHaveTextContent(/not category targets or quotas/i)
  })

  it('joins recommended outcomes to catalog evidence by decision_unit_id', async () => {
    const payload = benchmarkFixture()
    const firstRecommended = payload.data.benchmark.project_outcomes.find(
      (outcome) => outcome.historically_recommended,
    )
    if (firstRecommended === undefined) throw new Error('Missing fixture outcome.')
    firstRecommended.governed_name = 'Do not use this benchmark-side name'

    renderBenchmark({ loader: async () => payload })

    const list = await screen.findByRole('list', {
      name: 'Historically recommended analytical projects',
    })
    const catalogName = bootstrapFixture().data.catalog.projects.find(
      (project) => project.decision_unit_id === firstRecommended.decision_unit_id,
    )?.governed_name

    expect(catalogName).toBeDefined()
    expect(within(list).getByText(String(catalogName))).toBeInTheDocument()
    expect(within(list).queryByText(firstRecommended.governed_name)).toBeNull()
    expect(within(list).getAllByRole('listitem')).toHaveLength(20)
  })

  it('keeps historical status distinct from governed Funding Priority', async () => {
    renderBenchmark()

    const list = await screen.findByRole('list', {
      name: 'Historically recommended analytical projects',
    })
    const first = within(list).getAllByRole('listitem')[0]

    expect(within(first).getByText('Historical recommendation')).toBeInTheDocument()
    expect(within(first).getByText('Governed Funding Priority')).toBeInTheDocument()
    expect(first).toHaveTextContent(/rank/i)
    expect(first).toHaveTextContent(/observed historical outcome/i)
  })

  it('makes benchmark isolation and the false governance flags visible', async () => {
    renderBenchmark()

    await screen.findByRole('heading', {
      name: 'January 21, 2026 Historical Benchmark',
    })
    expect(screen.getByText('Changes Funding Priority?')).toBeInTheDocument()
    expect(screen.getByText('Changes Funding Plan selection?')).toBeInTheDocument()
    expect(screen.getAllByText('No')).toHaveLength(2)
    expect(document.body).toHaveTextContent(
      /historical recommendation information is used only for comparison/i,
    )
    expect(document.body).toHaveTextContent(
      /does not change Funding Priority.*Funding Plan selection.*Analyst Resolution/i,
    )
  })

  it('shows presentation-only project overlap with an authoritative current plan', async () => {
    renderBenchmark({ currentPlan: complete332PlanFixture().data })

    const comparison = await screen.findByRole('region', {
      name: 'Current Funding Plan comparison',
    })
    expect(within(comparison).getByText('3')).toBeInTheDocument()
    expect(comparison).toHaveTextContent(/project-set overlap/i)
    expect(comparison).toHaveTextContent(/presentation only/i)
    expect(comparison).not.toHaveTextContent(/accuracy|similarity score|quality/i)
  })

  it('does not infer a comparison when no current plan has been evaluated', async () => {
    renderBenchmark()

    const comparison = await screen.findByRole('region', {
      name: 'Current Funding Plan comparison',
    })
    expect(comparison).toHaveTextContent(/evaluate a Funding Plan/i)
    expect(comparison).not.toHaveTextContent(/predicted recommendation/i)
  })

  it('contains benchmark failures locally and retries through the same loader', async () => {
    const user = userEvent.setup()
    const loader = vi
      .fn()
      .mockRejectedValueOnce(
        new ApiClientError('Unavailable.', {
          kind: 'NETWORK_ERROR',
          errorCode: 'BACKEND_UNAVAILABLE',
          retryable: true,
        }),
      )
      .mockResolvedValueOnce(benchmarkFixture())

    renderBenchmark({ loader })

    expect(
      await screen.findByRole('heading', {
        name: 'Historical benchmark unavailable',
      }),
    ).toBeInTheDocument()
    expect(document.body).toHaveTextContent(
      /Explore and Funding Plan remain available/i,
    )

    await user.click(screen.getByRole('button', { name: 'Retry benchmark' }))

    expect(
      await screen.findByRole('heading', {
        name: 'January 21, 2026 Historical Benchmark',
      }),
    ).toBeInTheDocument()
    expect(loader).toHaveBeenCalledTimes(2)
  })

  it('rejects a benchmark response from another runtime identity', async () => {
    const payload = benchmarkFixture()
    payload.identity.release_id = 'another-release'

    renderBenchmark({ loader: async () => payload })

    expect(
      await screen.findByRole('heading', {
        name: 'Historical benchmark does not match this runtime',
      }),
    ).toBeInTheDocument()
    expect(screen.queryByText('$700M')).toBeNull()
  })

  it('shows only the governed January 21, 2026 snapshot', async () => {
    renderBenchmark()

    expect(
      await screen.findByRole('heading', {
      name: 'January 21, 2026 Historical Benchmark',
      }),
    ).toBeInTheDocument()
    expect(document.body).not.toHaveTextContent(/February 2026|March 2026/)
  })
})
