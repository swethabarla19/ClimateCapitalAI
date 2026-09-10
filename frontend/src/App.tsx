import { useEffect, useRef, useState } from 'react'
import './App.css'
import { fetchBootstrap } from './api/client'
import type { BootstrapSuccessEnvelope } from './api/contracts'
import { Explore } from './features/Explore'
import { FundingPlan } from './features/FundingPlan'
import { DataMethodology } from './features/DataMethodology'
import { HelpResources } from './features/HelpResources'
import {
  HistoricalBenchmark,
  type HistoricalBenchmarkLoader,
} from './features/HistoricalBenchmark'
import { formatDollars } from './lib/format'
import { AppIcon } from './components/AppIcon'
import {
  GeminiDrawer,
  type GeminiContext,
  type GeminiExplainer,
} from './components/GeminiDrawer'
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
  icon: 'explore' | 'plan' | 'benchmark' | 'methodology' | 'help'
}> = [
  { label: 'Explore', href: '#explore', route: 'EXPLORE', icon: 'explore' },
  {
    label: 'Funding Plan',
    href: '#funding-plan',
    route: 'FUNDING_PLAN',
    icon: 'plan',
  },
  {
    label: 'Historical Benchmark',
    href: '#historical-benchmark',
    route: 'HISTORICAL_BENCHMARK',
    icon: 'benchmark',
  },
  {
    label: 'Data & Methodology',
    href: '#data-methodology',
    route: 'DATA_METHODOLOGY',
    icon: 'methodology',
  },
  {
    label: 'Help & Resources',
    href: '#help-resources',
    route: 'HELP_RESOURCES',
    icon: 'help',
  },
]

function routeFromHash(
  hash: string,
): PresentationState['route'] | null {
  return navigation.find((item) => item.href === hash)?.route ?? null
}

function hashForRoute(route: PresentationState['route']): string {
  return (
    navigation.find((item) => item.route === route)?.href ?? '#explore'
  )
}

type BootstrapLoader = (
  signal?: AbortSignal,
) => Promise<BootstrapSuccessEnvelope>

interface AppProps {
  bootstrapLoader?: BootstrapLoader
  fundingPlanEvaluator?: FundingPlanEvaluator
  historicalBenchmarkLoader?: HistoricalBenchmarkLoader
  geminiExplainer?: GeminiExplainer
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
  geminiExplainer,
}: AppProps) {
  const [state, setState] = useState<AppState>({ status: 'LOADING' })
  const [bootstrapAttempt, setBootstrapAttempt] = useState(0)
  const [geminiOpen, setGeminiOpen] = useState(false)
  const geminiButtonRef = useRef<HTMLButtonElement>(null)

  useEffect(() => {
    const controller = new AbortController()

    void bootstrapLoader(controller.signal)
      .then((bootstrap) => {
        const initialization = initializeSessionFromBootstrap(bootstrap)
        const requestedRoute = routeFromHash(window.location.hash)
        const session =
          requestedRoute !== null &&
          requestedRoute !== initialization.session.presentation.route
            ? setPresentationRoute(initialization.session, requestedRoute)
            : initialization.session

        setState({
          status: 'READY',
          bootstrap,
          session,
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

  useEffect(() => {
    const applyHashRoute = () => {
      const requestedRoute = routeFromHash(window.location.hash)

      if (requestedRoute === null) {
        return
      }

      setState((current) => {
        if (
          current.status !== 'READY' ||
          current.session.presentation.route === requestedRoute
        ) {
          return current
        }

        return {
          ...current,
          session: setPresentationRoute(current.session, requestedRoute),
        }
      })
    }

    window.addEventListener('hashchange', applyHashRoute)
    window.addEventListener('popstate', applyHashRoute)

    return () => {
      window.removeEventListener('hashchange', applyHashRoute)
      window.removeEventListener('popstate', applyHashRoute)
    }
  }, [])

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
  const currentRouteLabel =
    navigation.find((item) => item.route === session.presentation.route)?.label ??
    'Explore'

  const updateSession = (nextSession: BrowserSessionState) => {
    setState((current) =>
      current.status === 'READY'
        ? { ...current, session: nextSession }
        : current,
    )
  }

  const navigate = (route: PresentationState['route']) => {
    const href = hashForRoute(route)

    if (window.location.hash !== href) {
      window.history.pushState(null, '', href)
    }

    setState((current) =>
      current.status === 'READY'
        ? {
            ...current,
            session: setPresentationRoute(current.session, route),
          }
        : current,
    )
  }

  const reloadRuntime = () => {
    setState({ status: 'LOADING' })
    setBootstrapAttempt((attempt) => attempt + 1)
  }

  const selectedProject =
    session.presentation.selected_decision_unit_id === null
      ? null
      : catalog.projects.find(
          (project) =>
            project.decision_unit_id ===
            session.presentation.selected_decision_unit_id,
        ) ?? null
  const selectedFeature =
    selectedProject === null
      ? null
      : mapContext.features.find(
          (feature) => feature.id === selectedProject.decision_unit_id,
        ) ?? null

  let geminiContext: GeminiContext
  if (session.presentation.route === 'EXPLORE' && selectedProject !== null) {
    const locationLabel =
      selectedFeature === null
        ? 'Location unavailable'
        : selectedFeature.properties.display_role === 'FACILITY_SITE_CONTEXT'
          ? 'Facility/site context'
          : selectedFeature.properties.display_role === 'PARK_SITE_CONTEXT'
            ? 'Park/site context'
            : 'Project location'
    geminiContext = {
      key: [
        session.runtime_identity.release_id,
        'PROJECT',
        selectedProject.decision_unit_id,
      ].join(':'),
      label: `Project · ${selectedProject.governed_name} · ${locationLabel}`,
      surface: 'PROJECT',
      projectIds: [selectedProject.decision_unit_id],
      fundingPlanInput: null,
      dataVersion: session.runtime_identity.data_version,
      releaseId: session.runtime_identity.release_id,
      visibleFacts: [
        selectedProject.presentation_category,
        `${formatDollars(selectedProject.model_request_dollars)} request`,
        `Funding Priority ${selectedProject.funding_priority_score} · Rank ${selectedProject.funding_priority_rank}`,
      ],
    }
  } else if (session.presentation.route === 'FUNDING_PLAN') {
    const result = session.latest_plan_result
    const isBoundary = result?.status === 'ANALYST_RESOLUTION_REQUIRED'
    const budgetMillions = session.working_plan.available_budget_dollars / 1_000_000
    const budgetLabel = `$${Number.isInteger(budgetMillions) ? budgetMillions : budgetMillions.toFixed(1)}M`
    geminiContext = {
      key: [
        session.runtime_identity.release_id,
        isBoundary ? 'BOUNDARY' : 'FUNDING_PLAN',
        JSON.stringify(session.working_plan),
      ].join(':'),
      label: isBoundary
        ? `Funding Plan · ${budgetLabel} · Analyst Resolution Required`
        : `Funding Plan · ${budgetLabel}`,
      surface: isBoundary ? 'BOUNDARY' : 'FUNDING_PLAN',
      projectIds: [],
      fundingPlanInput: session.working_plan,
      dataVersion: session.runtime_identity.data_version,
      releaseId: session.runtime_identity.release_id,
    }
  } else if (session.presentation.route === 'HISTORICAL_BENCHMARK') {
    geminiContext = {
      key: `${session.runtime_identity.release_id}:BENCHMARK`,
      label: 'Historical Benchmark · January 21, 2026',
      surface: 'BENCHMARK',
      projectIds: [],
      fundingPlanInput: null,
      dataVersion: session.runtime_identity.data_version,
      releaseId: session.runtime_identity.release_id,
    }
  } else {
    const topic =
      session.presentation.route === 'HELP_RESOURCES'
        ? 'Help & Resources'
        : 'Funding Priority'
    geminiContext = {
      key: `${session.runtime_identity.release_id}:METHODOLOGY:${topic}`,
      label: `Methodology · ${topic}`,
      surface: 'METHODOLOGY',
      projectIds: [],
      fundingPlanInput: null,
      dataVersion: session.runtime_identity.data_version,
      releaseId: session.runtime_identity.release_id,
    }
  }

  const closeGemini = () => {
    setGeminiOpen(false)
    window.setTimeout(() => geminiButtonRef.current?.focus(), 0)
  }

  return (
    <div className={geminiOpen ? 'app-shell app-shell-gemini-open' : 'app-shell'}>
      {bootstrap.data.public_configuration.fixture_mode && (
        <div className="fixture-banner" role="status">
          DEVELOPMENT FIXTURE · Not reviewed release data
        </div>
      )}

      <aside className="sidebar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 40 40" fill="none">
              <circle cx="20" cy="20" r="17" />
              <path d="M9 23c5-9 10 1 16-7 2-3 4-3 6-2" />
              <path d="M13 28c5-2 9-6 13-12" />
            </svg>
          </span>
          <span className="brand-name"><strong>ClimateCapital</strong><span>AI</span></span>
        </div>

        <div className="sidebar-navigation">
          <nav aria-label="Primary workspace navigation">
            <ul className="nav-list nav-list-primary">
              {navigation.slice(0, 2).map((item) => {
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
                      <AppIcon name={item.icon} />
                      {item.label}
                    </a>
                  </li>
                )
              })}
            </ul>
          </nav>

          <nav className="reference-navigation" aria-label="Reference navigation">
            <span className="navigation-group-label">Reference</span>
            <ul className="nav-list nav-list-reference">
              {navigation.slice(2).map((item) => {
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
                      <AppIcon name={item.icon} />
                      {item.label}
                    </a>
                  </li>
                )
              })}
            </ul>
          </nav>
        </div>

        <div className="analyst-profile" aria-label="Current workspace role">
          <span className="analyst-avatar" aria-hidden="true">SA</span>
          <span><strong>S. Analyst</strong><small>Capital Planning</small></span>
        </div>
      </aside>

      <div className="workspace">
        <header className="decision-header">
          <div className="header-title">
            <span className="context-label">Historical decision workspace</span>
            <strong>Austin Climate Investment Plan</strong>
            <span className="header-date">January 21, 2026 snapshot</span>
          </div>
          <div className="header-context-pill">
            <span className="context-label">Workspace</span>
            <strong>{currentRouteLabel}</strong>
          </div>
          <div className="header-budget">
            <span className="context-label">Available Project Budget</span>
            <strong>
              {formatDollars(session.working_plan.available_budget_dollars)}
            </strong>
          </div>
          <button
            ref={geminiButtonRef}
            className="gemini-preview-button"
            type="button"
            aria-expanded={geminiOpen}
            aria-controls="gemini-assistant-panel"
            onClick={() => setGeminiOpen(true)}
          >
            <AppIcon name="sparkle" size={18} />
            Ask Gemini
          </button>
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
          <DataMethodology />
        ) : session.presentation.route === 'HELP_RESOURCES' ? (
          <HelpResources />
        ) : (
          <Explore
            catalog={catalog}
            mapContext={mapContext}
            publicConfiguration={bootstrap.data.public_configuration}
            session={session}
            onSessionChange={updateSession}
            onOpenFundingPlan={() => navigate('FUNDING_PLAN')}
          />
        )}
      </div>
      {geminiOpen && (
        <div className="gemini-overlay" onClick={closeGemini}>
          <div id="gemini-assistant-panel">
            <GeminiDrawer
              context={geminiContext}
              onClose={closeGemini}
              explainer={geminiExplainer}
            />
          </div>
        </div>
      )}
    </div>
  )
}

export default App
