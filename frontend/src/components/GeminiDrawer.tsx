import { useEffect, useId, useRef, useState, type FormEvent } from 'react'
import {
  GEMINI_EXPLANATION_REQUEST_CONTRACT_VERSION,
  type FundingPlanInput,
  type GeminiExplanationRequest,
  type GeminiExplanationSuccessEnvelope,
  type GeminiHistoryMessage,
  type GeminiSurface,
} from '../api/contracts'
import { ApiClientError, explainWithGemini } from '../api/client'
import { AppIcon } from './AppIcon'

export type GeminiExplainer = (
  request: GeminiExplanationRequest,
  signal?: AbortSignal,
) => Promise<GeminiExplanationSuccessEnvelope>

export interface GeminiContext {
  key: string
  label: string
  surface: GeminiSurface
  projectIds: string[]
  fundingPlanInput: FundingPlanInput | null
  dataVersion: string
  releaseId: string
  visibleFacts?: string[]
}

interface ConversationMessage {
  role: 'USER' | 'ASSISTANT'
  content: string
  grounding?: string
  status?: 'COMPLETE' | 'INSUFFICIENT_CONTEXT' | 'SAFETY_BLOCKED'
}

interface GeminiDrawerProps {
  context: GeminiContext
  onClose: () => void
  explainer?: GeminiExplainer
}

const starters: Record<GeminiSurface, string[]> = {
  PROJECT: [
    "Explain this project's Funding Priority.",
    "What drives this project's score?",
    "Summarize this project's governed evidence.",
    'Explain the six PRB components.',
  ],
  FUNDING_PLAN: [
    'Why did this Funding Plan stop here?',
    'Explain this boundary priority tier.',
    'Why is Analyst Resolution required?',
    'What does Remaining Budget mean?',
  ],
  BOUNDARY: [
    'Why did this Funding Plan stop here?',
    'Explain this boundary priority tier.',
    'Why is Analyst Resolution required?',
    'What does Remaining Budget mean?',
  ],
  BENCHMARK: [
    'Explain the $700M, $332M, and $368M relationship.',
    "Why doesn't a $700M Funding Plan reproduce the historical recommendation?",
    'How is the Historical Benchmark used?',
  ],
  METHODOLOGY: [
    'How does Funding Priority work?',
    "Why doesn't ClimateCapital automatically break ties?",
    'Is ClimateCapital an optimization model?',
  ],
}

function historyForRequest(messages: ConversationMessage[]): GeminiHistoryMessage[] {
  return messages.slice(-6).map(({ role, content }) => ({ role, content }))
}

function groundingLabel(envelope: GeminiExplanationSuccessEnvelope): string {
  return envelope.data.grounding.evidence_sources
    .map((source) => source.replaceAll('_', ' ').toLocaleLowerCase())
    .join(' · ')
}

function friendlyFailure(error: unknown): string {
  if (!(error instanceof ApiClientError)) {
    return 'Gemini is temporarily unavailable. Project evidence and Funding Plan calculations remain available.'
  }

  if (error.errorCode === 'GEMINI_DISABLED') {
    return 'Gemini is disabled in this environment. Project evidence and Funding Plan calculations remain available.'
  }
  if (error.errorCode === 'GEMINI_CONTEXT_MISMATCH') {
    return 'The governed runtime changed. Close this panel and retry with the current application context.'
  }
  if (error.errorCode === 'GEMINI_CONTEXT_INVALID') {
    return 'This context cannot support that Gemini request. Review the current project or Funding Plan state.'
  }
  if (error.errorCode === 'GEMINI_RATE_LIMITED') {
    return 'Gemini has reached its request limit. Wait briefly, then retry.'
  }
  if (error.errorCode === 'GEMINI_TIMEOUT') {
    return 'Gemini took too long to respond. Project evidence and Funding Plan calculations remain available.'
  }
  if (error.errorCode === 'GEMINI_INVALID_RESPONSE') {
    return 'Gemini returned an invalid response, so ClimateCapital did not display it.'
  }
  return 'Gemini is temporarily unavailable. Project evidence and Funding Plan calculations remain available.'
}

function GeminiDrawerContent({
  context,
  onClose,
  explainer = explainWithGemini,
}: GeminiDrawerProps) {
  const titleId = useId()
  const inputRef = useRef<HTMLTextAreaElement>(null)
  const requestRef = useRef<AbortController | null>(null)
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState<ConversationMessage[]>([])
  const [state, setState] = useState<'IDLE' | 'LOADING' | 'ERROR'>('IDLE')
  const [failure, setFailure] = useState<string | null>(null)
  const [retryable, setRetryable] = useState(false)
  const [lastQuestion, setLastQuestion] = useState<string | null>(null)

  useEffect(() => {
    inputRef.current?.focus()
    return () => requestRef.current?.abort()
  }, [])

  useEffect(() => {
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') onClose()
    }
    document.addEventListener('keydown', closeOnEscape)
    return () => document.removeEventListener('keydown', closeOnEscape)
  }, [onClose])

  const ask = async (rawQuestion: string) => {
    const submittedQuestion = rawQuestion.trim()
    if (submittedQuestion.length === 0 || state === 'LOADING') return

    const history = historyForRequest(messages)
    const controller = new AbortController()
    requestRef.current?.abort()
    requestRef.current = controller
    setMessages((current) => [
      ...current,
      { role: 'USER', content: submittedQuestion },
    ])
    setQuestion('')
    setLastQuestion(submittedQuestion)
    setFailure(null)
    setRetryable(false)
    setState('LOADING')

    try {
      const response = await explainer(
        {
          contract_version: GEMINI_EXPLANATION_REQUEST_CONTRACT_VERSION,
          data_version: context.dataVersion,
          release_id: context.releaseId,
          surface: context.surface,
          question: submittedQuestion,
          project_ids: [...context.projectIds],
          funding_plan_input: context.fundingPlanInput,
          history,
        },
        controller.signal,
      )
      if (controller.signal.aborted) return
      setMessages((current) => [
        ...current,
        {
          role: 'ASSISTANT',
          content: response.data.answer,
          status: response.data.status,
          grounding: groundingLabel(response),
        },
      ])
      setState('IDLE')
    } catch (error: unknown) {
      if (controller.signal.aborted) return
      setMessages((current) =>
        current.at(-1)?.role === 'USER' &&
        current.at(-1)?.content === submittedQuestion
          ? current.slice(0, -1)
          : current,
      )
      setFailure(friendlyFailure(error))
      setRetryable(error instanceof ApiClientError && error.retryable)
      setState('ERROR')
    }
  }

  const reset = () => {
    requestRef.current?.abort()
    setQuestion('')
    setMessages([])
    setState('IDLE')
    setFailure(null)
    setRetryable(false)
    setLastQuestion(null)
    inputRef.current?.focus()
  }

  return (
    <aside
      className="gemini-drawer"
      role="dialog"
      aria-labelledby={titleId}
      onClick={(event) => event.stopPropagation()}
    >
      <header className="gemini-drawer-header">
        <div>
          <p className="eyebrow">Powered by Gemini on Vertex AI</p>
          <h2 id={titleId}>ClimateCapital Gemini</h2>
          <p>Explains governed evidence. Does not make funding decisions.</p>
        </div>
        <button
          className="icon-button"
          type="button"
          aria-label="Close Gemini"
          onClick={onClose}
        >
          ×
        </button>
      </header>

      <div className="gemini-context-pill" aria-label="Current Gemini context">
        <AppIcon name="sparkle" size={16} />
        <div>
          <span>{context.label}</span>
          {context.visibleFacts && context.visibleFacts.length > 0 && (
            <small>{context.visibleFacts.join(' · ')}</small>
          )}
        </div>
      </div>

      <div className="gemini-conversation" aria-live="polite" aria-busy={state === 'LOADING'}>
        {messages.length === 0 && (
          <div className="gemini-starters">
            <strong>Try a governed question</strong>
            {starters[context.surface].map((starter) => (
              <button key={starter} type="button" onClick={() => setQuestion(starter)}>
                {starter}
              </button>
            ))}
          </div>
        )}
        {messages.map((message, index) => (
          <article
            className={`gemini-message gemini-message-${message.role.toLocaleLowerCase()}`}
            key={`${message.role}-${index}`}
          >
            <strong>{message.role === 'USER' ? 'You' : 'Gemini'}</strong>
            <p>{message.content}</p>
            {message.status === 'INSUFFICIENT_CONTEXT' && (
              <span className="gemini-answer-status">Insufficient governed context</span>
            )}
            {message.status === 'SAFETY_BLOCKED' && (
              <span className="gemini-answer-status">Response safety blocked</span>
            )}
            {message.grounding && (
              <small className="gemini-grounding">Grounded in {message.grounding}</small>
            )}
          </article>
        ))}
        {state === 'LOADING' && <p className="gemini-loading">Gemini is preparing a grounded explanation…</p>}
        {state === 'ERROR' && failure && (
          <div className="gemini-error" role="alert">
            <p>{failure}</p>
            {retryable && lastQuestion && (
              <button type="button" onClick={() => void ask(lastQuestion)}>Retry</button>
            )}
          </div>
        )}
      </div>

      <form
        className="gemini-composer"
        onSubmit={(event: FormEvent) => {
          event.preventDefault()
          void ask(question)
        }}
      >
        <label htmlFor="gemini-question">Ask about this governed context</label>
        <textarea
          id="gemini-question"
          ref={inputRef}
          value={question}
          maxLength={2_000}
          rows={3}
          disabled={state === 'LOADING'}
          onChange={(event) => setQuestion(event.target.value)}
        />
        <div className="gemini-composer-actions">
          <button type="button" className="text-button" onClick={reset}>New question</button>
          <button type="submit" disabled={question.trim().length === 0 || state === 'LOADING'}>
            Ask Gemini
          </button>
        </div>
      </form>

      <p className="gemini-disclaimer">
        Gemini can make mistakes. Governed ClimateCapital values and deterministic
        Funding Plan results remain authoritative.
      </p>
    </aside>
  )
}

export function GeminiDrawer(props: GeminiDrawerProps) {
  return <GeminiDrawerContent key={props.context.key} {...props} />
}
