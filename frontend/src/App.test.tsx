import { render, screen, within } from '@testing-library/react'
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

beforeEach(() => {
  window.sessionStorage.clear()
  window.history.replaceState(null, '', '/')
})

describe('ClimateCapital application shell', () => {
  it('groups workspace and reference navigation while keeping the profile last', async () => {
    render(<App bootstrapLoader={async () => bootstrapFixture()} />)
    await screen.findByRole('heading', { name: 'Explore projects' })

    const primary = screen.getByRole('navigation', {
      name: 'Primary workspace navigation',
    })
    const reference = screen.getByRole('navigation', {
      name: 'Reference navigation',
    })
    expect(within(primary).getAllByRole('link').map((link) => link.textContent)).toEqual([
      'Explore',
      'Funding Plan',
    ])
    expect(
      within(reference).getAllByRole('link').map((link) => link.textContent),
    ).toEqual([
      'Historical Benchmark',
      'Data & Methodology',
      'Help & Resources',
    ])
    const profile = screen.getByLabelText('Current workspace role')
    expect(
      reference.compareDocumentPosition(profile) & Node.DOCUMENT_POSITION_FOLLOWING,
    ).toBeTruthy()
  })

  it('activates Ask Gemini without making a request when the drawer opens', async () => {
    const user = userEvent.setup()
    const geminiExplainer = vi.fn()
    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        geminiExplainer={geminiExplainer}
      />,
    )

    const button = await screen.findByRole('button', { name: 'Ask Gemini' })
    expect(button).toBeVisible()
    await user.click(button)
    expect(
      screen.getByRole('heading', { name: 'ClimateCapital Gemini' }),
    ).toBeInTheDocument()
    expect(geminiExplainer).not.toHaveBeenCalled()
  })

  it('uses the same governed project handle for list selection and shows mapped evidence', async () => {
    const user = userEvent.setup()
    const geminiExplainer = vi.fn()
    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        geminiExplainer={geminiExplainer}
      />,
    )
    await user.click(
      await screen.findByRole('button', {
        name: 'View details for Transportation fixture project 1',
      }),
    )
    expect(geminiExplainer).not.toHaveBeenCalled()
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Project · Transportation fixture project 1 · Project location',
    )
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Funding Priority 83 · Rank 1',
    )
    expect(
      screen.getByRole('heading', { name: 'Transportation fixture project 1' }),
    ).toBeInTheDocument()
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    expect(document.querySelector('.app-shell-gemini-open')).not.toBeNull()

    await user.click(screen.getByRole('button', { name: 'Close Gemini' }))
    expect(
      screen.getByRole('heading', { name: 'Transportation fixture project 1' }),
    ).toBeInTheDocument()
    expect(document.querySelector('.app-shell-gemini-open')).toBeNull()
  })

  it('keeps unmapped project context explicitly location unavailable', async () => {
    const user = userEvent.setup()
    render(<App bootstrapLoader={async () => bootstrapFixture()} />)
    await user.click(
      await screen.findByRole('button', {
        name: 'View details for Community Facilities fixture project 7',
      }),
    )
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Location unavailable',
    )
  })

  it('shows Funding Plan and authoritative boundary contexts without automatic Gemini calls', async () => {
    const user = userEvent.setup()
    const geminiExplainer = vi.fn()
    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        fundingPlanEvaluator={async () => boundary700PlanFixture()}
        geminiExplainer={geminiExplainer}
      />,
    )
    await user.click(await screen.findByRole('link', { name: 'Funding Plan' }))
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Funding Plan · $0M',
    )
    await user.click(screen.getByRole('button', { name: 'Close Gemini' }))
    const customBudget = screen.getByLabelText('Custom Available Project Budget')
    await user.type(customBudget, '700000000')
    await user.click(
      screen.getByRole('button', { name: /evaluate custom budget/i }),
    )
    await screen.findByRole('heading', { name: 'Boundary priority tier' })
    expect(geminiExplainer).not.toHaveBeenCalled()
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Funding Plan · $700M · Analyst Resolution Required',
    )
  })

  it('shows benchmark and methodology contexts without automatic navigation calls', async () => {
    const user = userEvent.setup()
    const geminiExplainer = vi.fn()
    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        historicalBenchmarkLoader={async () => benchmarkFixture()}
        geminiExplainer={geminiExplainer}
      />,
    )
    await user.click(await screen.findByRole('link', { name: 'Historical Benchmark' }))
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Historical Benchmark · January 21, 2026',
    )
    await user.click(screen.getByRole('button', { name: 'Close Gemini' }))
    await user.click(screen.getByRole('link', { name: 'Data & Methodology' }))
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent(
      'Methodology · Funding Priority',
    )
    expect(geminiExplainer).not.toHaveBeenCalled()
  })

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

  expect(document.body).toHaveTextContent(
    /\$332M historical matched-cohort reference preset/i,
  )
  expect(document.body).toHaveTextContent(
    /74 of the 106 projects.*remaining 32 projects/i,
  )
  expect(document.body).not.toHaveTextContent(/reference budgets/i)
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

    expect(document.body).toHaveTextContent(
      /\$332M historical matched-cohort reference preset/i,
    )
    expect(document.body).toHaveTextContent(
      /74 governed mapped project contexts.*remaining 32 projects/i,
    )
    expect(document.body).not.toHaveTextContent(/reference budgets/i)
    expect(document.body).not.toHaveTextContent(
      /project locations displayed on a map/i,
    )
  })

  it.each([
    ['#explore', 'Explore projects'],
    ['#funding-plan', 'Funding Plan'],
    ['#historical-benchmark', 'January 21, 2026 Historical Benchmark'],
    ['#data-methodology', 'Data & Methodology'],
    ['#help-resources', 'Help & Resources'],
  ])('opens the supported direct route %s', async (hash, heading) => {
    window.history.replaceState(null, '', hash)

    render(
      <App
        bootstrapLoader={async () => bootstrapFixture()}
        historicalBenchmarkLoader={async () => benchmarkFixture()}
      />,
    )

    expect(
      await screen.findByRole('heading', { name: heading }),
    ).toBeInTheDocument()
  })

  it('writes the selected route hash and restores it on refresh', async () => {
    const user = userEvent.setup()
    const app = (
      <App bootstrapLoader={async () => bootstrapFixture()} />
    )
    const { unmount } = render(app)

    await user.click(await screen.findByRole('link', { name: 'Funding Plan' }))
    expect(window.location.hash).toBe('#funding-plan')
    expect(
      screen.getByRole('heading', { name: 'Funding Plan' }),
    ).toBeInTheDocument()

    unmount()
    window.sessionStorage.clear()
    render(app)

    expect(
      await screen.findByRole('heading', { name: 'Funding Plan' }),
    ).toBeInTheDocument()
  })

  it('initializes from the activated cross-category bootstrap shape', async () => {
    render(<App bootstrapLoader={async () => bootstrapFixture()} />)

    expect(
      await screen.findByRole('heading', { name: 'Explore projects' }),
    ).toBeInTheDocument()
    expect(screen.getByLabelText('106 of 106 projects')).toBeInTheDocument()
    expect(screen.getByText('$1,973,520,000')).toBeInTheDocument()
    expect(screen.getByLabelText('Project portfolio summary')).toHaveTextContent(
      '74 mapped · 32 location unavailable',
    )
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
    const customBudget = screen.getByLabelText('Custom Available Project Budget')
    await user.type(customBudget, '700000000')
    await user.click(
      screen.getByRole('button', { name: /evaluate custom budget/i }),
    )
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
