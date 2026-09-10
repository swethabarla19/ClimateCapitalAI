import { useEffect, useMemo, useRef, useState } from 'react'
import type {
  BoundaryResolutionInput,
  FundingPlanResult,
  RuntimeCatalog,
  SelectedProjectResult,
  SelectionSource,
} from '../api/contracts'
import { BoundaryResolution } from '../components/BoundaryResolution'
import {
  formatDollars,
  formatFundingPriority,
} from '../lib/format'
import {
  cloneFundingPlanInput,
  type BrowserSessionState,
  type SessionRequestError,
} from '../session/contracts'
import {
  PlanRequestCoordinator,
  type FundingPlanEvaluator,
} from '../session/planRequests'
import {
  applyPlanFailure,
  applyPlanSuccess,
  beginPlanRequest,
  cancelPlanRequest,
  clearExpectedPlanFingerprint,
  setBoundaryResolutions,
  setWorkingBudget,
} from '../session/planState'

interface FundingPlanProps {
  catalog: RuntimeCatalog
  session: BrowserSessionState
  onSessionChange: (session: BrowserSessionState) => void
  evaluator?: FundingPlanEvaluator
  onReloadRuntime?: () => void
}

interface BudgetPreset {
  dollars: number
  amountLabel: string
  label: string
  description: string
}

const budgetPresets: BudgetPreset[] = [
  {
    dollars: 332_000_000,
    amountLabel: '$332M',
    label: 'Historical matched-cohort reference',
    description:
      '$332M is the historical recommendation amount associated with projects represented in ClimateCapital\'s governed 106-project analytical universe.',
  },
]

interface ParsedBudget {
  dollars: number | null
  error: string | null
}

function parseBudgetInput(value: string, maximum: number): ParsedBudget {
  const normalized = value.replace(/[$,\s]/g, '')

  if (normalized.length === 0) {
    return { dollars: null, error: 'Enter an Available Project Budget.' }
  }

  if (!/^\d+$/.test(normalized)) {
    return { dollars: null, error: 'Use whole dollars without cents.' }
  }

  const dollars = Number(normalized)

  if (!Number.isSafeInteger(dollars)) {
    return { dollars: null, error: 'Enter a valid whole-dollar amount.' }
  }

  if (dollars > maximum) {
    return {
      dollars: null,
      error: `Available Project Budget cannot exceed ${formatDollars(maximum)}, the governed request total.`,
    }
  }

  return { dollars, error: null }
}

function selectionSourceLabel(source: SelectionSource): string {
  if (source === 'AUTO_COMPLETE_TIER') {
    return 'Complete higher-priority tier'
  }
  if (source === 'AUTO_UNIQUE_BUDGET_FEASIBLE') {
    return 'Unique budget-feasible project in tier'
  }
  return 'Analyst resolution'
}

function errorPresentation(error: SessionRequestError): {
  heading: string
  explanation: string
  recovery: 'RETRY' | 'CLEAR_FINGERPRINT' | 'RELOAD_RUNTIME'
} {
  if (
    error.error_code === 'DATA_VERSION_CONFLICT' ||
    error.error_code === 'CONTRACT_VERSION_CONFLICT' ||
    error.error_code === 'STALE_RUNTIME_RESPONSE'
  ) {
    return {
      heading: 'Runtime data changed',
      explanation:
        'This plan input no longer matches the active governed runtime. Reload runtime data before evaluating again.',
      recovery: 'RELOAD_RUNTIME',
    }
  }

  if (error.error_code === 'PLAN_FINGERPRINT_CONFLICT') {
    return {
      heading: 'Plan state changed',
      explanation:
        'The prior evaluation fingerprint is no longer current. Re-evaluate the same analyst inputs without relying on the stale fingerprint.',
      recovery: 'CLEAR_FINGERPRINT',
    }
  }

  if (error.kind === 'NETWORK_ERROR') {
    return {
      heading: 'Funding Plan service unavailable',
      explanation:
        'The governed evaluator could not be reached. Your analyst inputs remain available for retry.',
      recovery: 'RETRY',
    }
  }

  if (error.kind === 'UNEXPECTED_PAYLOAD') {
    return {
      heading: 'Plan response could not be verified',
      explanation:
        'No unverified analytical result is being shown. Retry the evaluation or reload the governed runtime if the issue continues.',
      recovery: 'RETRY',
    }
  }

  if (error.status === 422) {
    return {
      heading: 'Plan input needs attention',
      explanation:
        'The governed evaluator rejected part of the submitted input. Review the budget and active boundary resolution before retrying.',
      recovery: 'RETRY',
    }
  }

  return {
    heading: 'Funding Plan could not be evaluated',
    explanation:
      'The governed evaluator did not return a usable plan. Your analyst inputs remain available for retry.',
    recovery: 'RETRY',
  }
}

function selectedProjectOrder(
  left: SelectedProjectResult,
  right: SelectedProjectResult,
): number {
  return (
    right.funding_priority_score - left.funding_priority_score ||
    left.funding_priority_rank - right.funding_priority_rank ||
    left.decision_unit_id.localeCompare(right.decision_unit_id)
  )
}

interface PlanResultProps {
  catalog: RuntimeCatalog
  result: FundingPlanResult
  loading: boolean
  boundaryResolutions: BoundaryResolutionInput[]
  onBoundarySubmit: (resolution: BoundaryResolutionInput) => void
}

function PlanResult({
  catalog,
  result,
  loading,
  boundaryResolutions,
  onBoundarySubmit,
}: PlanResultProps) {
  const catalogById = useMemo(
    () =>
      new Map(
        catalog.projects.map((project) => [project.decision_unit_id, project]),
      ),
    [catalog.projects],
  )
  const selectedProjects = useMemo(
    () => [...result.selected_projects].sort(selectedProjectOrder),
    [result.selected_projects],
  )
  const boundary = result.unresolved_boundary
  const budgetUtilization =
    result.available_budget_dollars === 0
      ? '0%'
      : result.included_total_dollars === result.available_budget_dollars
        ? '100%'
        : `${(
            (result.included_total_dollars / result.available_budget_dollars) *
            100
          ).toFixed(1)}%`
  const initialResolution =
    boundary === null
      ? null
      : boundaryResolutions.find(
          (resolution) =>
            resolution.funding_priority_rank === boundary.funding_priority_rank &&
            resolution.funding_priority_score === boundary.funding_priority_score,
        ) ?? null

  return (
    <div className="plan-result">
      <section className="plan-summary-panel" aria-label="Plan summary">
        <div className="plan-result-heading">
          <div>
            <p className="eyebrow">Funding Plan result</p>
            <h2>
              {result.status === 'COMPLETE'
                ? 'Plan evaluation complete'
                : 'Analyst resolution required'}
            </h2>
          </div>
          <span
            className={
              result.status === 'COMPLETE'
                ? 'status-badge status-complete'
                : 'status-badge status-boundary'
            }
          >
            {result.status === 'COMPLETE' ? 'Complete' : 'Needs analyst input'}
          </span>
        </div>

        <dl className="plan-summary-grid">
          <div>
            <dt>Available Project Budget</dt>
            <dd>{formatDollars(result.available_budget_dollars)}</dd>
          </div>
          <div>
            <dt>Selected total</dt>
            <dd>{formatDollars(result.included_total_dollars)}</dd>
          </div>
          <div>
            <dt>Remaining budget</dt>
            <dd>{formatDollars(result.remainder_dollars)}</dd>
          </div>
          <div>
            <dt>Selected projects</dt>
            <dd>{result.selected_projects.length}</dd>
          </div>
        </dl>

        <div className="plan-budget-utilization">
          <div>
            <span>Budget utilization</span>
            <strong>{budgetUtilization}</strong>
          </div>
          <progress
            aria-label="Budget utilization"
            max={result.available_budget_dollars || 1}
            value={result.included_total_dollars}
          />
        </div>

        <p className="plan-method-note">
          Remaining budget is a normal result of indivisible full-request projects.
          A complete plan does not need to spend every available dollar.
        </p>
        <details className="evaluation-identity">
          <summary>Evaluation identity</summary>
          <dl>
            <div>
              <dt>Data version</dt>
              <dd>{result.data_version}</dd>
            </div>
            <div>
              <dt>Plan fingerprint</dt>
              <dd className="project-id">{result.plan_fingerprint}</dd>
            </div>
          </dl>
        </details>
      </section>

      {result.warnings.length > 0 && (
        <section className="plan-warning-panel" aria-labelledby="warnings-heading">
          <h2 id="warnings-heading">Plan warnings</h2>
          <ul>
            {result.warnings.map((warning) => (
              <li key={`${warning.warning_code}:${warning.decision_unit_ids.join(':')}`}>
                <strong>Same-tier feasible project remains</strong>
                <span>{warning.message}</span>
              </li>
            ))}
          </ul>
        </section>
      )}

      {result.applied_analyst_overrides.length > 0 && (
        <section
          className="plan-override-panel"
          aria-labelledby="overrides-heading"
        >
          <h2 id="overrides-heading">Analyst acknowledgement applied</h2>
          <ul>
            {result.applied_analyst_overrides.map((override) => (
              <li
                key={`${override.funding_priority_score}:${override.funding_priority_rank}`}
              >
                Funding Priority{' '}
                {formatFundingPriority(override.funding_priority_score)}, Rank{' '}
                {override.funding_priority_rank}: acknowledged advancing while{' '}
                {override.decision_unit_ids_left_feasible.length} same-tier project
                {override.decision_unit_ids_left_feasible.length === 1 ? '' : 's'}{' '}
                remained feasible.
              </li>
            ))}
          </ul>
        </section>
      )}

      {boundary !== null && (
        <BoundaryResolution
          key={`${result.plan_fingerprint}:${boundary.funding_priority_score}:${boundary.funding_priority_rank}`}
          boundary={boundary}
          catalog={catalog}
          initialResolution={initialResolution}
          loading={loading}
          onSubmit={onBoundarySubmit}
        />
      )}

      <section className="selected-projects-panel" aria-labelledby="selected-heading">
        <div className="selected-projects-heading">
          <div>
            <p className="eyebrow">Projects in this Funding Plan</p>
            <h2 id="selected-heading">Selected projects</h2>
          </div>
          <strong>{selectedProjects.length}</strong>
        </div>

        {selectedProjects.length === 0 ? (
          <p>No projects are selected at this budget.</p>
        ) : (
          <ul className="selected-project-list">
            {selectedProjects.map((selected) => {
              const project = catalogById.get(selected.decision_unit_id)
              return (
                <li key={selected.decision_unit_id}>
                  <div className="selected-project-heading">
                    <div>
                      <strong>
                        {project?.governed_name ?? selected.decision_unit_id}
                      </strong>
                      <span>
                        {project?.presentation_category ??
                          'Catalog record unavailable'}
                      </span>
                    </div>
                    <span className="selection-source-badge">
                      {selectionSourceLabel(selected.selection_source)}
                    </span>
                  </div>
                  <dl>
                    <div>
                      <dt>Governed request</dt>
                      <dd>{formatDollars(selected.model_request_dollars)}</dd>
                    </div>
                    <div>
                      <dt>Funding Priority</dt>
                      <dd>
                        {formatFundingPriority(selected.funding_priority_score)} ·
                        Rank {selected.funding_priority_rank}
                      </dd>
                    </div>
                  </dl>
                </li>
              )
            })}
          </ul>
        )}
        <p className="selected-order-note">
          Projects are displayed by Funding Priority. Decision unit ID provides
          deterministic display order inside shared ranks only and has no analytical
          meaning.
        </p>
      </section>
    </div>
  )
}

export function FundingPlan({
  catalog,
  session,
  onSessionChange,
  evaluator,
  onReloadRuntime = () => undefined,
}: FundingPlanProps) {
  const [customBudget, setCustomBudget] = useState(
    session.working_plan.available_budget_dollars === 0
      ? ''
      : String(session.working_plan.available_budget_dollars),
  )
  const [customBudgetTouched, setCustomBudgetTouched] = useState(false)
  const sessionRef = useRef(session)
  const coordinator = useMemo(
    () => new PlanRequestCoordinator(evaluator),
    [evaluator],
  )

  useEffect(() => {
    sessionRef.current = session
  }, [session])

  useEffect(() => () => coordinator.cancel(), [coordinator])

  const commitSession = (next: BrowserSessionState) => {
    sessionRef.current = next
    onSessionChange(next)
  }

  const evaluateSession = (base: BrowserSessionState) => {
    const started = beginPlanRequest(base)
    commitSession(started.session)

    coordinator.evaluate(
      cloneFundingPlanInput(started.session.working_plan),
      started.generation,
      {
        onSuccess: (response, generation) => {
          commitSession(
            applyPlanSuccess(sessionRef.current, response, generation),
          )
        },
        onFailure: (error, generation) => {
          commitSession(
            applyPlanFailure(sessionRef.current, error, generation),
          )
        },
        onCancelled: (generation) => {
          const next = cancelPlanRequest(sessionRef.current, generation)
          if (next !== sessionRef.current) commitSession(next)
        },
      },
    )
  }

  const chooseBudget = (dollars: number) => {
    coordinator.cancel()
    setCustomBudget(String(dollars))
    setCustomBudgetTouched(false)
    evaluateSession(setWorkingBudget(sessionRef.current, dollars))
  }

  const parsedBudget = parseBudgetInput(
    customBudget,
    catalog.governed_request_total_dollars,
  )
  const request = session.plan_request
  const result = session.latest_plan_result
  const error = request.error
  const loading = request.status === 'LOADING'

  const submitCustomBudget = () => {
    setCustomBudgetTouched(true)
    if (parsedBudget.dollars === null) return
    coordinator.cancel()
    evaluateSession(
      setWorkingBudget(sessionRef.current, parsedBudget.dollars),
    )
  }

  const submitBoundaryResolution = (
    resolution: BoundaryResolutionInput,
  ) => {
    const current = sessionRef.current
    const accumulated = current.working_plan.boundary_resolutions.filter(
      (existing) =>
        !(
          existing.funding_priority_score === resolution.funding_priority_score &&
          existing.funding_priority_rank === resolution.funding_priority_rank
        ),
    )
    const next = setBoundaryResolutions(current, [
      ...accumulated,
      resolution,
    ])
    evaluateSession(next)
  }

  const retryEvaluation = (clearFingerprint: boolean) => {
    const current = sessionRef.current
    evaluateSession(
      clearFingerprint ? clearExpectedPlanFingerprint(current) : current,
    )
  }

  return (
    <main id="funding-plan" className="main-content funding-plan-workspace">
      <section className="funding-plan-intro" aria-labelledby="funding-plan-heading">
        <div>
          <p className="eyebrow">Build a funding scenario</p>
          <h1 id="funding-plan-heading">Funding Plan</h1>
          <p>
            Set an Available Project Budget. ClimateCapital automatically evaluates
            indivisible full-request projects from higher to lower official Funding
            Priority. Analyst input is required only when a tied boundary leaves
            multiple valid choices.
          </p>
        </div>
        <div className="method-badge">
          <span>Method</span>
          <strong>Transparent rules + analyst judgment</strong>
        </div>
      </section>

      <section className="budget-panel" aria-labelledby="budget-heading">
        <div className="budget-heading">
          <div>
            <p className="eyebrow">Analyst input</p>
            <h2 id="budget-heading">Available Project Budget</h2>
          </div>
          <strong className="active-budget">
            {formatDollars(session.working_plan.available_budget_dollars)}
          </strong>
        </div>
        <p>
          The historical preset populates the budget only. It does not preload
          project membership, category allocations, or historical decisions. Enter
          any other whole-dollar scenario below.
        </p>

        <div className="budget-presets">
          {budgetPresets.map((preset) => (
            <button
              type="button"
              key={preset.dollars}
              className={
                session.working_plan.available_budget_dollars === preset.dollars
                  ? 'budget-preset budget-preset-active'
                  : 'budget-preset'
              }
              aria-pressed={
                session.working_plan.available_budget_dollars === preset.dollars
              }
              aria-label={`${preset.amountLabel} ${preset.label}`}
              onClick={() => chooseBudget(preset.dollars)}
            >
              <strong>{preset.amountLabel}</strong>
              <span>{preset.label}</span>
              <small>{preset.description}</small>
            </button>
          ))}
        </div>

        <form
          className="custom-budget-form"
          aria-busy={loading}
          onSubmit={(event) => {
            event.preventDefault()
            submitCustomBudget()
          }}
        >
          <label>
            <span>Custom Available Project Budget</span>
            <input
              id="custom-available-project-budget"
              name="available-project-budget"
              type="text"
              inputMode="numeric"
              value={customBudget}
              aria-describedby="custom-budget-guidance"
              aria-invalid={customBudgetTouched && parsedBudget.error !== null}
              placeholder="Enter whole dollars"
              onChange={(event) => {
                setCustomBudget(event.target.value)
                setCustomBudgetTouched(true)
              }}
            />
          </label>
          <button type="submit" disabled={parsedBudget.dollars === null}>
            Evaluate custom budget
          </button>
          <p
            id="custom-budget-guidance"
            className={
              customBudgetTouched && parsedBudget.error !== null
                ? 'validation-message'
                : 'input-guidance'
            }
          >
            {customBudgetTouched && parsedBudget.error !== null
              ? parsedBudget.error
              : `Whole dollars from $0 through ${formatDollars(catalog.governed_request_total_dollars)}.`}
          </p>
        </form>
      </section>

      {loading && (
        <div className="plan-loading" role="status" aria-live="polite">
          <strong>Evaluating Funding Plan…</strong>
          <span>ClimateCapital is applying the Funding Priority rules to this budget.</span>
        </div>
      )}

      {error !== null && (() => {
        const presentation = errorPresentation(error)
        return (
          <section className="plan-error-panel" role="alert">
            <p className="eyebrow">Evaluation not updated</p>
            <h2>{presentation.heading}</h2>
            <p>{presentation.explanation}</p>
            {error.field_path.length > 0 && (
              <p>
                Input field: <code>{error.field_path.join('.')}</code>
              </p>
            )}
            {presentation.recovery === 'RELOAD_RUNTIME' ? (
              <button
                type="button"
                onClick={() => {
                  coordinator.cancel()
                  onReloadRuntime()
                }}
              >
                Reload governed runtime
              </button>
            ) : (
              <button
                type="button"
                onClick={() =>
                  retryEvaluation(
                    presentation.recovery === 'CLEAR_FINGERPRINT',
                  )
                }
              >
                Retry evaluation
              </button>
            )}
          </section>
        )
      })()}

      {result === null && request.status === 'IDLE' && (
        <section className="plan-empty-state">
          <h2>Choose an Available Project Budget</h2>
          <p>
            Choose the historical matched-cohort reference or enter a custom
            whole-dollar amount to evaluate a Funding Plan. Project selections come
            from ClimateCapital&apos;s Funding Priority rules and any required Analyst
            Resolution.
          </p>
        </section>
      )}

      {result !== null && (
        <PlanResult
          catalog={catalog}
          result={result}
          loading={loading}
          boundaryResolutions={session.working_plan.boundary_resolutions}
          onBoundarySubmit={submitBoundaryResolution}
        />
      )}

      <section className="decision-support-note" aria-label="Funding Plan method note">
        <strong>Transparent analyst decision support.</strong>
        <span>
          Funding Priority is ordinal. Project costs, category, project name,
          historical outcomes, and PRB components do not break equal-score ties.
        </span>
      </section>
    </main>
  )
}
