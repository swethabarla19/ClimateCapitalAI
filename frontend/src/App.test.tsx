import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { ApiClientError } from './api/client'
import type { FundingPlanInput } from './api/contracts'
import App from './App'
import {
  benchmarkFixture,
  bootstrapFixture,
  boundary700PlanFixture,
  complete332PlanFixture,
} from './test/bootstrapFixture'

beforeEach(() => window.sessionStorage.clear())

describe('ClimateCapital application shell', () => {
  it('shows a bounded loading state before bootstrap completes', () => {
    render(<App bootstrapLoader={() => new Promise(() => undefined)} />)

    expect(
      screen.getByText(/loading governed release data/i),
    ).toBeInTheDocument()
})
  it('presents plain-language Data & Methodology guidance and the Gemini decision boundary', async () => {
  const user = userEvent.setup()

  render(<App bootstrapLoader={async () => bootstrapFixture()} />)

  await user.click(
    await screen.findByRole('link', { name: 'Data & Methodology' }),
  )

  expect(
    screen.getByRole('heading', { name: 'Data & Methodology' }),
  ).toBeInTheDocument()

  expect(
    screen.getByRole('heading', { name: 'What is Funding Priority?' }),
  ).toBeInTheDocument()

  expect(
    screen.getByText(/PRB stands for Project Review Board/i),
  ).toBeInTheDocument()

  expect(document.body).toHaveTextContent(
    /ClimateCapital calculates the Funding Plan; Gemini helps you understand it/i,
  )

  expect(document.body).toHaveTextContent(
    /not an official City of Austin recommendation/i,
  )
})

  it('provides first-time-user Help & Resources guidance without giving Gemini decision authority', async () => {
    const user = userEvent.setup()

    render(<App bootstrapLoader={async () => bootstrapFixture()} />)

    await user.click(
      await screen.findByRole('link', { name: 'Help & Resources' }),
    )

    expect(
      screen.getByRole('heading', { name: 'Help & Resources' }),
    ).toBeInTheDocument()

    expect(
      screen.getByRole('heading', { name: 'Quick Start' }),
    ).toBeInTheDocument()

    expect(document.body).toHaveTextContent(
      /Gemini explains the information; it does not make funding decisions/i,
    )

    expect(document.body).toHaveTextContent(
      /The final choice remains an analyst decision/i,
    )
  })

  it('initializes from the activated cross-category bootstrap shape', async () => {
    render(<App bootstrapLoader={async () => bootstrapFixture()} />)

    expect(
      await screen.findByRole('heading', { name: 'Explore projects' }),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('106 of 106 projects')).toBeInTheDocument()
    expect(screen.getAllByText('$1,973,520,000')).toHaveLength(2)
    expect(
      screen.getByText(/74 mapped · 32 location unavailable/i),
    ).toBeInTheDocument()
    expect(
      screen.getByText('Austin Climate Investment Plan'),
    ).toBeInTheDocument()
    expect(screen.queryByText(/12 projects/i)).not.toBeInTheDocument()
  })

  it('routes to the governed Funding Plan without arbitrary membership controls', async () => {
    const user = userEvent.setup()
    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        fundingPlanEvaluator={async () => complete332PlanFixture()}
      />,
    )

    await user.click(
      await screen.findByRole('link', { name: 'Funding Plan' }),
    )

    expect(
      screen.getByRole('heading', { name: 'Funding Plan' }),
    ).toBeInTheDocument()
    expect(
      screen.getByRole('heading', { name: 'Available Project Budget' }),
    ).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /add .* to plan/i })).toBeNull()
  })

  it('loads the Historical Benchmark only when its dedicated route is entered', async () => {
    const user = userEvent.setup()
    const benchmarkLoader = vi.fn(async () => benchmarkFixture())

    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        historicalBenchmarkLoader={benchmarkLoader}
      />,
    )

    await screen.findByRole('heading', { name: 'Explore projects' })
    expect(benchmarkLoader).not.toHaveBeenCalled()

    await user.click(
      screen.getByRole('link', { name: 'Historical Benchmark' }),
    )

    expect(
      await screen.findByRole('heading', {
        name: 'January 21, 2026 Historical Benchmark',
      }),
    ).toBeInTheDocument()
    expect(benchmarkLoader).toHaveBeenCalledTimes(1)
  })

  it('contains benchmark failure without breaking Explore or Funding Plan', async () => {
    const user = userEvent.setup()

    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        historicalBenchmarkLoader={async () => {
          throw new ApiClientError('Unavailable.', {
            kind: 'NETWORK_ERROR',
            errorCode: 'BACKEND_UNAVAILABLE',
            retryable: true,
          })
        }}
      />,
    )

    await user.click(
      await screen.findByRole('link', { name: 'Historical Benchmark' }),
    )
    expect(
      await screen.findByRole('heading', {
        name: 'Historical benchmark unavailable',
      }),
    ).toBeInTheDocument()

    await user.click(screen.getByRole('link', { name: 'Explore' }))
    expect(
      screen.getByRole('heading', { name: 'Explore projects' }),
    ).toBeInTheDocument()

    await user.click(screen.getByRole('link', { name: 'Funding Plan' }))
    expect(
      screen.getByRole('heading', { name: 'Available Project Budget' }),
    ).toBeInTheDocument()
  })

  it('keeps benchmark membership out of plan input and preserves boundary state', async () => {
    const user = userEvent.setup()
    const evaluator = vi.fn(async (input: FundingPlanInput) => {
      void input
      return boundary700PlanFixture()
    })

    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        fundingPlanEvaluator={evaluator}
        historicalBenchmarkLoader={async () => benchmarkFixture()}
      />,
    )

    await user.click(await screen.findByRole('link', { name: 'Funding Plan' }))
    await user.click(screen.getByRole('button', { name: /\$700M/i }))
    expect(
      await screen.findByRole('heading', { name: 'Boundary priority tier' }),
    ).toBeInTheDocument()

    const planInput = evaluator.mock.calls[0]?.[0]
    expect(Object.keys(planInput ?? {}).sort()).toEqual([
      'available_budget_dollars',
      'boundary_resolutions',
      'contract_version',
      'data_version',
      'expected_fingerprint',
    ])
    expect(JSON.stringify(planInput)).not.toMatch(/benchmark|historically_recommended/)

    await user.click(
      screen.getByRole('link', { name: 'Historical Benchmark' }),
    )
    await screen.findByRole('heading', {
      name: 'January 21, 2026 Historical Benchmark',
    })
    await user.click(screen.getByRole('link', { name: 'Funding Plan' }))

    expect(
      screen.getByRole('heading', { name: 'Boundary priority tier' }),
    ).toBeInTheDocument()
    expect(evaluator).toHaveBeenCalledTimes(1)
  })

  it('fails closed when bootstrap cannot load', async () => {
    render(
      <App
        bootstrapLoader={async () => {
          throw new Error('Core release data is unavailable.')
        }}
      />,
    )

    expect(
      await screen.findByRole('heading', { name: /could not start/i }),
    ).toBeInTheDocument()
    expect(
      screen.getByText(/no analytical results are being shown/i),
    ).toBeInTheDocument()
    expect(
      screen.getByText(/core release data is unavailable/i),
    ).toBeInTheDocument()
  })

  it('retries bootstrap through the same loader after a failure', async () => {
    const user = userEvent.setup()
    const loader = vi
      .fn()
      .mockRejectedValueOnce(new Error('Temporary outage.'))
      .mockResolvedValueOnce(bootstrapFixture())

    render(<App bootstrapLoader={loader} />)

    await user.click(
      await screen.findByRole('button', { name: /retry loading data/i }),
    )

    expect(
      await screen.findByRole('heading', { name: 'Explore projects' }),
    ).toBeInTheDocument()
    expect(loader).toHaveBeenCalledTimes(2)
  })
})
