import { useEffect, useState } from 'react'
import './App.css'
import { fetchBootstrap } from './api/client'
import type { BootstrapSuccessEnvelope } from './api/contracts'
import { Explore } from './features/Explore'
import { FundingPlan } from './features/FundingPlan'
import {
  HistoricalBenchmark,
  type HistoricalBenchmarkLoader,
} from './features/HistoricalBenchmark'
import { formatDollars } from './lib/format'
import type {
  BrowserSessionState,
  PresentationState,
} from './session/contracts'
import {
  initializeSessionFromBootstrap,
  type SessionInitializationStatus,
} from './session/initialize'
import type { FundingPlanEvaluator } from './session/planRequests'
import { setPresentationRoute } from './session/presentation'

const navigation: Array<{
  label: string
  href: string
  route: PresentationState['route']
}> = [
  { label: 'Explore', href: '#explore', route: 'EXPLORE' },
  {
    label: 'Funding Plan',
    href: '#funding-plan',
    route: 'FUNDING_PLAN',
  },
  {
    label: 'Historical Benchmark',
    href: '#historical-benchmark',
    route: 'HISTORICAL_BENCHMARK',
  },
  {
    label: 'Data & Methodology',
    href: '#data-methodology',
    route: 'DATA_METHODOLOGY',
  },
  {
    label: 'Help & Resources',
    href: '#help-resources',
    route: 'HELP_RESOURCES',
  },
]

type BootstrapLoader = (
  signal?: AbortSignal,
) => Promise<BootstrapSuccessEnvelope>

interface AppProps {
  bootstrapLoader?: BootstrapLoader
  fundingPlanEvaluator?: FundingPlanEvaluator
  historicalBenchmarkLoader?: HistoricalBenchmarkLoader
}

type AppState =
  | { status: 'LOADING' }
  | { status: 'ERROR'; message: string }
  | {
      status: 'READY'
      bootstrap: BootstrapSuccessEnvelope
      session: BrowserSessionState
      sessionInitialization: SessionInitializationStatus
    }

function sessionNotice(status: SessionInitializationStatus): string | null {
  if (status === 'RESET_STALE') {
    return (
      'Saved plan inputs belonged to another runtime release and were reset. ' +
      'Harmless view preferences were preserved.'
    )
  }

  if (status === 'RESET_INVALID') {
    return 'An unreadable saved browser session was discarded and reset.'
  }

  if (status === 'RESTORED_INPUTS') {
    return (
      'Saved analyst inputs were restored for this runtime. ' +
      'Any prior evaluation result must be requested again.'
    )
  }

  return null
}

function App({
  bootstrapLoader = fetchBootstrap,
  fundingPlanEvaluator,
  historicalBenchmarkLoader,
}: AppProps) {
  const [state, setState] = useState<AppState>({ status: 'LOADING' })
  const [bootstrapAttempt, setBootstrapAttempt] = useState(0)

  useEffect(() => {
    const controller = new AbortController()

    void bootstrapLoader(controller.signal)
      .then((bootstrap) => {
        const initialization = initializeSessionFromBootstrap(bootstrap)

        setState({
          status: 'READY',
          bootstrap,
          session: initialization.session,
          sessionInitialization: initialization.status,
        })
      })
      .catch((error: unknown) => {
        if (
          controller.signal.aborted ||
          (error instanceof Error && error.name === 'AbortError')
        ) {
          return
        }

        setState({
          status: 'ERROR',
          message:
            error instanceof Error
              ? error.message
              : 'Bootstrap failed unexpectedly.',
        })
      })

    return () => controller.abort()
  }, [bootstrapAttempt, bootstrapLoader])

  if (state.status === 'LOADING') {
    return (
      <main className="app-state" aria-busy="true">
        <h1>ClimateCapital AI</h1>
        <p>Loading governed release data…</p>
      </main>
    )
  }

  if (state.status === 'ERROR') {
    return (
      <main className="app-state error-panel">
        <h1>ClimateCapital AI could not start</h1>
        <p>
          Governed release data could not be loaded. No analytical results are
          being shown.
        </p>
        <p>{state.message}</p>
        <button
          type="button"
          onClick={() => {
            setState({ status: 'LOADING' })
            setBootstrapAttempt((attempt) => attempt + 1)
          }}
        >
          Retry loading data
        </button>
      </main>
    )
  }

  const { bootstrap, session } = state
  const { catalog, map_context: mapContext } = bootstrap.data
  const notice = sessionNotice(state.sessionInitialization)

  const updateSession = (nextSession: BrowserSessionState) => {
    setState((current) =>
      current.status === 'READY'
        ? { ...current, session: nextSession }
        : current,
    )
  }

  const navigate = (route: PresentationState['route']) => {
    updateSession(setPresentationRoute(session, route))
  }

  const reloadRuntime = () => {
    setState({ status: 'LOADING' })
    setBootstrapAttempt((attempt) => attempt + 1)
  }

  return (
    <div className="app-shell">
      {bootstrap.data.public_configuration.fixture_mode && (
        <div className="fixture-banner" role="status">
          DEVELOPMENT FIXTURE · Not reviewed release data
        </div>
      )}

      <aside className="sidebar">
        <div className="brand">
          <strong>ClimateCapital</strong>
          <span>AI</span>
        </div>

        <nav aria-label="Primary navigation">
          <ul className="nav-list">
            {navigation.map((item) => {
              const current = session.presentation.route === item.route

              return (
                <li key={item.label}>
                  <a
                    href={item.href}
                    aria-current={current ? 'page' : undefined}
                    className={
                      current ? 'nav-link nav-link-active' : 'nav-link'
                    }
                    onClick={(event) => {
                      event.preventDefault()
                      navigate(item.route)
                    }}
                  >
                    {item.label}
                  </a>
                </li>
              )
            })}
          </ul>
        </nav>
      </aside>

      <div className="workspace">
        <header className="decision-header">
          <div>
            <span className="context-label">Decision</span>
            <strong>Austin Cross-Category · January 21, 2026</strong>
          </div>
          <div>
            <span className="context-label">Plan</span>
            <strong>Working Plan</strong>
          </div>
          <div>
            <span className="context-label">Available Project Budget</span>
            <strong>
              {formatDollars(session.working_plan.available_budget_dollars)}
            </strong>
          </div>
        </header>

        {notice && (
          <div className="global-session-notice" role="status" aria-live="polite">
            {notice}
          </div>
        )}

        {session.presentation.route === 'FUNDING_PLAN' ? (
          <FundingPlan
            catalog={catalog}
            session={session}
            onSessionChange={updateSession}
            evaluator={fundingPlanEvaluator}
            onReloadRuntime={reloadRuntime}
          />
        ) : session.presentation.route === 'HISTORICAL_BENCHMARK' ? (
          <HistoricalBenchmark
            catalog={catalog}
            runtimeIdentity={session.runtime_identity}
            currentPlan={session.latest_plan_result}
            loader={historicalBenchmarkLoader}
          />
        ) : session.presentation.route === 'DATA_METHODOLOGY' ? (
          <main id="data-methodology" className="main-content app-state">
            <h1>Data &amp; Methodology</h1>
            <p>
              The activated runtime uses official PRB Funding Priority and the
              governed priority-constrained analyst workflow.
            </p>
          </main>
        ) : session.presentation.route === 'HELP_RESOURCES' ? (
          <main id="help-resources" className="main-content app-state">
            <h1>Help &amp; Resources</h1>
            <p>Manual guidance remains available without Gemini.</p>
          </main>
        ) : (
          <Explore
            catalog={catalog}
            mapContext={mapContext}
            session={session}
            onSessionChange={updateSession}
          />
        )}
      </div>
    </div>
  )
}

export default App
