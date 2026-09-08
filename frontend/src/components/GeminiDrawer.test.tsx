import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import { ApiClientError } from '../api/client'
import {
  GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION,
  type GeminiExplanationRequest,
  type GeminiExplanationStatus,
  type GeminiExplanationSuccessEnvelope,
  type GeminiSurface,
} from '../api/contracts'
import { GeminiDrawer, type GeminiContext } from './GeminiDrawer'

const requestId = '123e4567-e89b-42d3-a456-426614174000'
const releaseId = 'a'.repeat(64)
const dataVersion = 'climatecapital-austin-2026-01-21-cross-category-v2'

function context(surface: GeminiSurface = 'PROJECT'): GeminiContext {
  return {
    key: `${releaseId}:${surface}:project-1`,
    label:
      surface === 'PROJECT'
        ? 'Project · Example project · Project location'
        : surface === 'BOUNDARY'
          ? 'Funding Plan · $700M · Analyst Resolution Required'
          : surface === 'FUNDING_PLAN'
            ? 'Funding Plan · $332M'
            : surface === 'BENCHMARK'
              ? 'Historical Benchmark · January 21, 2026'
              : 'Methodology · Funding Priority',
    surface,
    projectIds: surface === 'PROJECT' ? ['community-facilities/example'] : [],
    fundingPlanInput:
      surface === 'FUNDING_PLAN' || surface === 'BOUNDARY'
        ? {
            contract_version: 'p0-cross-category-funding-plan/2.0.0',
            data_version: dataVersion,
            available_budget_dollars:
              surface === 'BOUNDARY' ? 700_000_000 : 332_000_000,
            boundary_resolutions: [],
            expected_fingerprint: null,
          }
        : null,
    dataVersion,
    releaseId,
  }
}

function success(
  surface: GeminiSurface = 'PROJECT',
  status: GeminiExplanationStatus = 'COMPLETE',
): GeminiExplanationSuccessEnvelope {
  return {
    endpoint: '/api/v1/gemini/explain',
    status: 'SUCCESS',
    identity: {
      request_id: requestId,
      api_namespace: '/api/v1',
      contract_version: GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION,
      data_version: dataVersion,
      release_id: releaseId,
    },
    data: {
      contract_version: GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION,
      data_version: dataVersion,
      release_id: releaseId,
      request_id: requestId,
      status,
      answer:
        status === 'SAFETY_BLOCKED'
          ? 'Gemini could not answer because the response was safety blocked.'
          : 'Funding Priority is the governed ordinal PRB Grand Total.',
      provider: 'vertex_ai',
      model: 'gemini-3.5-flash',
      grounding: {
        snapshot_date: '2026-01-21',
        surface,
        decision_unit_ids: surface === 'PROJECT' ? ['community-facilities/example'] : [],
        plan_fingerprint:
          surface === 'FUNDING_PLAN' || surface === 'BOUNDARY'
            ? 'b'.repeat(64)
            : null,
        benchmark_effective_date: surface === 'BENCHMARK' ? '2026-01-21' : null,
        evidence_sources:
          surface === 'BENCHMARK'
            ? ['HISTORICAL_BENCHMARK']
            : ['GOVERNED_METHODOLOGY'],
      },
      warnings: [],
    },
  }
}

describe('Gemini drawer', () => {
  it('shows title, provider, decision boundary, disclaimer, and visible context', () => {
    render(<GeminiDrawer context={context()} onClose={() => undefined} />)
    expect(screen.getByRole('heading', { name: 'ClimateCapital Gemini' })).toBeInTheDocument()
    expect(screen.getByText('Powered by Gemini on Vertex AI')).toBeInTheDocument()
    expect(screen.getByText('Explains governed evidence. Does not make funding decisions.')).toBeInTheDocument()
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent('Project · Example project · Project location')
    expect(screen.getByText(/Gemini can make mistakes/)).toBeInTheDocument()
  })

  it.each([
    ['PROJECT', "Explain this project's Funding Priority."],
    ['FUNDING_PLAN', 'What does Remaining Budget mean?'],
    ['BOUNDARY', 'Why is Analyst Resolution required?'],
    ['BENCHMARK', 'Explain the $700M, $332M, and $368M relationship.'],
    ['METHODOLOGY', 'Is ClimateCapital an optimization model?'],
  ] as const)('shows %s starter questions without submitting', (surface, starter) => {
    const explainer = vi.fn()
    render(<GeminiDrawer context={context(surface)} onClose={() => undefined} explainer={explainer} />)
    expect(screen.getByRole('button', { name: starter })).toBeInTheDocument()
    expect(explainer).not.toHaveBeenCalled()
  })

  it('submits only explicit questions with handles and renders grounding', async () => {
    const user = userEvent.setup()
    const explainer = vi.fn(
      async (request: GeminiExplanationRequest) => {
        void request
        return success()
      },
    )
    render(<GeminiDrawer context={context()} onClose={() => undefined} explainer={explainer} />)
    await user.type(screen.getByLabelText('Ask about this governed context'), 'Explain it.')
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(explainer).toHaveBeenCalledTimes(1)
    expect(explainer.mock.calls[0]?.[0]).toMatchObject({
      surface: 'PROJECT',
      project_ids: ['community-facilities/example'],
      funding_plan_input: null,
      question: 'Explain it.',
    })
    expect(await screen.findByText(/governed ordinal PRB Grand Total/)).toBeInTheDocument()
    expect(screen.getByText(/Grounded in governed methodology/)).toBeInTheDocument()
  })

  it('announces loading and preserves application-local interaction', async () => {
    const user = userEvent.setup()
    let resolve: ((value: GeminiExplanationSuccessEnvelope) => void) | undefined
    const explainer = vi.fn(() => new Promise<GeminiExplanationSuccessEnvelope>((done) => { resolve = done }))
    render(<GeminiDrawer context={context()} onClose={() => undefined} explainer={explainer} />)
    await user.type(screen.getByLabelText('Ask about this governed context'), 'Explain it.')
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(screen.getByText(/preparing a grounded explanation/)).toBeInTheDocument()
    expect(screen.getByLabelText('Ask about this governed context')).toBeDisabled()
    resolve?.(success())
    expect(await screen.findByText(/governed ordinal PRB Grand Total/)).toBeInTheDocument()
  })

  it.each([
    ['INSUFFICIENT_CONTEXT', 'Insufficient governed context'],
    ['SAFETY_BLOCKED', 'Response safety blocked'],
  ] as const)('renders %s meaning beyond color', async (status, label) => {
    const user = userEvent.setup()
    render(<GeminiDrawer context={context()} onClose={() => undefined} explainer={async () => success('PROJECT', status)} />)
    await user.type(screen.getByLabelText('Ask about this governed context'), 'Question')
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(await screen.findByText(label)).toBeInTheDocument()
  })

  it.each([
    ['GEMINI_DISABLED', /disabled in this environment/i, false],
    ['GEMINI_CONTEXT_MISMATCH', /governed runtime changed/i, false],
    ['GEMINI_CONTEXT_INVALID', /context cannot support/i, false],
    ['GEMINI_RATE_LIMITED', /request limit/i, true],
    ['GEMINI_TIMEOUT', /too long/i, true],
    ['GEMINI_INVALID_RESPONSE', /invalid response/i, false],
    ['GEMINI_UNAVAILABLE', /temporarily unavailable/i, true],
  ] as const)('renders %s and exposes retry only when authorized', async (code, message, canRetry) => {
    const user = userEvent.setup()
    const explainer = vi.fn(async () => {
      throw new ApiClientError('provider error', {
        kind: 'API_ERROR',
        errorCode: code,
        retryable: canRetry,
      })
    })
    render(<GeminiDrawer context={context()} onClose={() => undefined} explainer={explainer} />)
    await user.type(screen.getByLabelText('Ask about this governed context'), 'Question')
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    expect(await screen.findByText(message)).toBeInTheDocument()
    expect(screen.queryByRole('button', { name: 'Retry' }) !== null).toBe(canRetry)
  })

  it('resets conversation when context changes and on New question', async () => {
    const user = userEvent.setup()
    const { rerender } = render(
      <GeminiDrawer context={context()} onClose={() => undefined} explainer={async () => success()} />,
    )
    await user.type(screen.getByLabelText('Ask about this governed context'), 'Question')
    await user.click(screen.getByRole('button', { name: 'Ask Gemini' }))
    await screen.findByText(/governed ordinal PRB Grand Total/)
    await user.click(screen.getByRole('button', { name: 'New question' }))
    expect(screen.queryByText(/governed ordinal PRB Grand Total/)).not.toBeInTheDocument()

    rerender(<GeminiDrawer context={context('BENCHMARK')} onClose={() => undefined} explainer={async () => success('BENCHMARK')} />)
    expect(screen.getByLabelText('Current Gemini context')).toHaveTextContent('Historical Benchmark')
    expect(screen.queryByText(/governed ordinal PRB Grand Total/)).not.toBeInTheDocument()
  })

  it('supports Escape close', async () => {
    const user = userEvent.setup()
    const onClose = vi.fn()
    render(<GeminiDrawer context={context()} onClose={onClose} />)
    await user.keyboard('{Escape}')
    expect(onClose).toHaveBeenCalledTimes(1)
  })
})
