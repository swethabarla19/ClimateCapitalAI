import { useEffect, useState } from 'react'
import {
  ApiClientError,
  fetchHistoricalBenchmark,
} from '../api/client'
import type {
  FundingPlanResult,
  HistoricalBenchmark as HistoricalBenchmarkData,
  HistoricalBenchmarkSuccessEnvelope,
  PresentationCategory,
  RuntimeCatalog,
} from '../api/contracts'
import {
  formatCompactDollars,
  formatDollars,
  formatFundingPriority,
} from '../lib/format'
import type { RuntimeIdentity } from '../session/contracts'

export type HistoricalBenchmarkLoader = (
  signal?: AbortSignal,
) => Promise<HistoricalBenchmarkSuccessEnvelope>

interface HistoricalBenchmarkProps {
  catalog: RuntimeCatalog
  runtimeIdentity: RuntimeIdentity
  currentPlan: FundingPlanResult | null
  loader?: HistoricalBenchmarkLoader
}

type BenchmarkState =
  | { status: 'LOADING' }
  | { status: 'ERROR'; failure: BenchmarkFailure }
  | {
      status: 'READY'
      benchmark: HistoricalBenchmarkData
      responseIdentity: HistoricalBenchmarkSuccessEnvelope['identity']
    }

type BenchmarkFailureCode =
  | 'UNAVAILABLE'
  | 'RUNTIME_MISMATCH'
  | 'UNVERIFIED_RESPONSE'

interface BenchmarkFailure {
  code: BenchmarkFailureCode
  heading: string
  explanation: string
}

const categoryOrder: PresentationCategory[] = [
  'Transportation',
  'Parks & Open Space',
  'Watershed',
  'Community Facilities',
]

function benchmarkFailure(error: unknown): BenchmarkFailure {
  if (error instanceof BenchmarkRuntimeError) {
    return {
      code: 'RUNTIME_MISMATCH',
      heading: 'Historical benchmark does not match this runtime',
      explanation:
        'The returned historical snapshot could not be reconciled to the active governed project catalog. No benchmark outcome is being shown.',
    }
  }

  if (
    error instanceof ApiClientError &&
    (error.kind === 'NETWORK_ERROR' || error.status === 503)
  ) {
    return {
      code: 'UNAVAILABLE',
      heading: 'Historical benchmark unavailable',
      explanation:
        'The historical snapshot could not be loaded. Explore and Funding Plan remain available and are not affected.',
    }
  }

  if (
    error instanceof ApiClientError &&
    (error.status === 409 ||
      error.errorCode === 'DATA_VERSION_CONFLICT' ||
      error.errorCode === 'CONTRACT_VERSION_CONFLICT')
  ) {
    return {
      code: 'RUNTIME_MISMATCH',
      heading: 'Historical benchmark does not match this runtime',
      explanation:
        'The benchmark identity differs from the active governed runtime. Retry after the runtime and benchmark are aligned.',
    }
  }

  return {
    code: 'UNVERIFIED_RESPONSE',
    heading: 'Historical benchmark could not be verified',
    explanation:
      'The response did not satisfy the governed benchmark contract. No unverified historical outcome is being shown.',
  }
}

class BenchmarkRuntimeError extends Error {}

function verifyAgainstRuntime(
  response: HistoricalBenchmarkSuccessEnvelope,
  catalog: RuntimeCatalog,
  runtimeIdentity: RuntimeIdentity,
): HistoricalBenchmarkData {
  const benchmark = response.data.benchmark

  if (
    response.identity.data_version !== runtimeIdentity.data_version ||
    response.identity.release_id !== runtimeIdentity.release_id ||
    benchmark.data_version !== catalog.data_version
  ) {
    throw new BenchmarkRuntimeError('Benchmark runtime identity mismatch.')
  }

  const catalogById = new Map(
    catalog.projects.map((project) => [project.decision_unit_id, project]),
  )
  const outcomeIds = new Set(
    benchmark.project_outcomes.map((outcome) => outcome.decision_unit_id),
  )

  if (
    outcomeIds.size !== catalogById.size ||
    [...outcomeIds].some((decisionUnitId) => !catalogById.has(decisionUnitId)) ||
    benchmark.project_outcomes.some(
      (outcome) =>
        catalogById.get(outcome.decision_unit_id)?.presentation_category !==
        outcome.presentation_category,
    )
  ) {
    throw new BenchmarkRuntimeError('Benchmark project universe mismatch.')
  }

  return benchmark
}

function historicalDateLabel(date: '2026-01-21'): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(`${date}T00:00:00Z`))
}

export function HistoricalBenchmark({
  catalog,
  runtimeIdentity,
  currentPlan,
  loader = fetchHistoricalBenchmark,
}: HistoricalBenchmarkProps) {
  const [attempt, setAttempt] = useState(0)
  const [state, setState] = useState<BenchmarkState>({ status: 'LOADING' })

  useEffect(() => {
    const controller = new AbortController()
    let active = true

    void loader(controller.signal)
      .then((response) => {
        if (!active) return
        const benchmark = verifyAgainstRuntime(
          response,
          catalog,
          runtimeIdentity,
        )
        setState({
          status: 'READY',
          benchmark,
          responseIdentity: response.identity,
        })
      })
      .catch((error: unknown) => {
        if (
          !active ||
          controller.signal.aborted ||
          (error instanceof ApiClientError && error.kind === 'REQUEST_ABORTED')
        ) {
          return
        }
        setState({ status: 'ERROR', failure: benchmarkFailure(error) })
      })

    return () => {
      active = false
      controller.abort()
    }
  }, [attempt, catalog, loader, runtimeIdentity])

  if (state.status === 'LOADING') {
    return (
      <main className="main-content benchmark-workspace">
        <div className="benchmark-loading" role="status" aria-live="polite">
          <strong>Loading historical benchmark…</strong>
          <span>Retrieving the isolated January decision snapshot.</span>
        </div>
      </main>
    )
  }

  if (state.status === 'ERROR') {
    return (
      <main className="main-content benchmark-workspace">
        <section className="benchmark-error" role="alert">
          <p className="eyebrow">Benchmark not loaded</p>
          <h1>{state.failure.heading}</h1>
          <p>{state.failure.explanation}</p>
          <button
            type="button"
            onClick={() => {
              setState({ status: 'LOADING' })
              setAttempt((value) => value + 1)
            }}
          >
            Retry benchmark
          </button>
        </section>
      </main>
    )
  }

  const { benchmark, responseIdentity } = state
  const catalogById = new Map(
    catalog.projects.map((project) => [project.decision_unit_id, project]),
  )
  const recommendedOutcomes = benchmark.project_outcomes
    .filter((outcome) => outcome.historically_recommended)
    .sort((left, right) => {
      const categoryDifference =
        categoryOrder.indexOf(left.presentation_category) -
        categoryOrder.indexOf(right.presentation_category)
      const leftName = catalogById.get(left.decision_unit_id)?.governed_name ?? left.governed_name
      const rightName = catalogById.get(right.decision_unit_id)?.governed_name ?? right.governed_name

      return (
        categoryDifference ||
        leftName.localeCompare(rightName, 'en-US') ||
        left.decision_unit_id.localeCompare(right.decision_unit_id)
      )
    })
  const categorySummaries = [...benchmark.category_summaries].sort(
    (left, right) =>
      categoryOrder.indexOf(left.presentation_category) -
      categoryOrder.indexOf(right.presentation_category),
  )
  const categoryRequestTotals = new Map(
    categoryOrder.map((category) => [
      category,
      catalog.projects
        .filter((project) => project.presentation_category === category)
        .reduce((sum, project) => sum + project.model_request_dollars, 0),
    ]),
  )
  const currentPlanForRuntime =
    currentPlan?.data_version === runtimeIdentity.data_version
      ? currentPlan
      : null
  const historicalRecommendedIds = new Set(
    recommendedOutcomes.map((outcome) => outcome.decision_unit_id),
  )
  const overlapCount =
    currentPlanForRuntime?.selected_projects.filter((project) =>
      historicalRecommendedIds.has(project.decision_unit_id),
    ).length ?? 0
  const dateLabel = historicalDateLabel(
    benchmark.historical_decision_snapshot_date,
  )

  return (
    <main id="historical-benchmark" className="main-content benchmark-workspace">
      <section className="benchmark-intro" aria-labelledby="benchmark-heading">
        <div>
          <p className="eyebrow">Historical reference · {dateLabel}</p>
          <h1 id="benchmark-heading">{dateLabel} Historical Benchmark</h1>
          <p>
            This page shows the City of Austin&apos;s {dateLabel} Initial Draft
            Recommendation as a historical reference. It can be compared with a
            ClimateCapital Funding Plan, but it never changes project scores, ranks,
            or selections.
          </p>
        </div>
        <div className="benchmark-role-badge">
          <span>Evidence role</span>
          <strong>Retrospective only</strong>
        </div>
      </section>

      <section className="benchmark-governance" aria-labelledby="benchmark-role-heading">
        <div>
          <p className="eyebrow">How this benchmark is used</p>
          <h2 id="benchmark-role-heading">
            Historical outcome, not a Funding Plan input
          </h2>
          <p>
            Historical recommendation information is used only for comparison.
            It does not change Funding Priority, project rank, Funding Plan
            selection, or Analyst Resolution.
          </p>
        </div>
        <dl>
          <div>
            <dt>Changes Funding Priority?</dt>
            <dd>{benchmark.ranking_input ? 'Yes' : 'No'}</dd>
          </div>
          <div>
            <dt>Changes Funding Plan selection?</dt>
            <dd>
              {benchmark.portfolio_selection_input ? 'Yes' : 'No'}
            </dd>
          </div>
        </dl>
      </section>

      <section className="benchmark-summary" aria-labelledby="snapshot-summary-heading">
        <div className="benchmark-section-heading">
          <div>
            <p className="eyebrow">Historical snapshot summary</p>
            <h2 id="snapshot-summary-heading">January package reconciliation</h2>
          </div>
          <span className="benchmark-equation">
            {formatCompactDollars(benchmark.matched_analytical_cohort_dollars)} +{' '}
            {formatCompactDollars(benchmark.outside_analytical_cohort_dollars)} ={' '}
            {formatCompactDollars(benchmark.full_initial_recommendation_dollars)}
          </span>
        </div>

        <div className="benchmark-stat-grid">
          <article>
            <strong className="benchmark-stat-value">
              {formatCompactDollars(benchmark.full_initial_recommendation_dollars)}
            </strong>
            <span>Full January Initial Draft Recommendation</span>
          </article>
          <article>
            <strong className="benchmark-stat-value">
              {formatCompactDollars(benchmark.matched_analytical_cohort_dollars)}
            </strong>
            <span>
              Recommendation associated with projects in ClimateCapital&apos;s
              106-project universe
            </span>
          </article>
          <article>
            <strong className="benchmark-stat-value">
              {formatCompactDollars(benchmark.outside_analytical_cohort_dollars)}
            </strong>
            <span>Recommendation outside that project-level universe</span>
          </article>
          <article>
            <strong className="benchmark-stat-value">
              {benchmark.historically_recommended_project_count}
            </strong>
            <span>Historically recommended analytical projects</span>
          </article>
        </div>

        <div className="benchmark-composition" aria-label="Historical package composition">
          <div aria-hidden="true">
            <span
              className="composition-matched"
              style={{ flexGrow: benchmark.matched_analytical_cohort_dollars }}
            />
            <span
              className="composition-outside"
              style={{ flexGrow: benchmark.outside_analytical_cohort_dollars }}
            />
          </div>
          <p>
            The full {formatCompactDollars(benchmark.full_initial_recommendation_dollars)}{' '}
            citywide package included{' '}
            {formatCompactDollars(benchmark.matched_analytical_cohort_dollars)} attached
            to projects in ClimateCapital&apos;s 106-project universe and{' '}
            {formatCompactDollars(benchmark.outside_analytical_cohort_dollars)} outside
            this project-level cohort. This does not establish a model budget.
          </p>
        </div>
      </section>

      <section
        className="benchmark-categories"
        aria-labelledby="category-context-heading"
        aria-label="Historical category context"
      >
        <div className="benchmark-section-heading">
          <div>
            <p className="eyebrow">Analytical-cohort reconciliation</p>
            <h2 id="category-context-heading">Historical category context</h2>
          </div>
        </div>
        <p className="benchmark-section-copy">
          These are observed matched-cohort outcomes, not category targets or quotas.
          The API provides the outside-cohort amount citywide rather than allocating
          it across categories.
        </p>
        <div className="benchmark-category-grid">
          {categorySummaries.map((summary) => (
            <article
              key={summary.presentation_category}
              aria-label={`${summary.presentation_category} historical context`}
            >
              <h3>{summary.presentation_category}</h3>
              <dl>
                <div>
                  <dt>Governed project requests</dt>
                  <dd>
                    {formatCompactDollars(
                      categoryRequestTotals.get(summary.presentation_category) ?? 0,
                    )}
                  </dd>
                </div>
                <div>
                  <dt>Matched historical recommendation</dt>
                  <dd>{formatCompactDollars(summary.recommendation_total_dollars)}</dd>
                </div>
                <div>
                  <dt>Historically recommended projects</dt>
                  <dd>
                    {summary.historically_recommended_project_count} of{' '}
                    {summary.analytical_project_count}
                  </dd>
                </div>
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section
        className="benchmark-plan-comparison"
        aria-label="Current Funding Plan comparison"
      >
        <div className="benchmark-section-heading">
          <div>
            <p className="eyebrow">Descriptive comparison</p>
            <h2 id="current-plan-comparison-heading">Current Funding Plan</h2>
          </div>
        </div>
        {currentPlanForRuntime === null ? (
          <p>
            Evaluate a Funding Plan to see a presentation-only project-set overlap
            with this historical snapshot.
          </p>
        ) : (
          <div className="benchmark-overlap">
            <div>
              <strong>{overlapCount}</strong>
              <span>Projects present in both sets</span>
            </div>
            <p>
              The current priority-constrained Funding Plan contains{' '}
              {currentPlanForRuntime.selected_projects.length} selected projects;
              the historical benchmark contains{' '}
              {benchmark.historically_recommended_project_count}. This project-set
              overlap is presentation only. It is not a score, target, or input to
              the current plan.
            </p>
          </div>
        )}
      </section>

      <section className="benchmark-projects" aria-labelledby="historical-projects-heading">
        <div className="benchmark-section-heading">
          <div>
            <p className="eyebrow">Observed project outcomes</p>
            <h2 id="historical-projects-heading">
              Historically recommended analytical projects
            </h2>
          </div>
          <strong>{recommendedOutcomes.length}</strong>
        </div>
        <p className="benchmark-section-copy">
          Displayed by category and project name only. This order is not a historical
          recommendation ranking, and historical status does not imply higher modeled
          priority.
        </p>
        <ul
          className="historical-project-list"
          aria-label="Historically recommended analytical projects"
        >
          {recommendedOutcomes.map((outcome) => {
            const project = catalogById.get(outcome.decision_unit_id)

            return (
              <li key={outcome.decision_unit_id}>
                <details>
                  <summary>
                    <span>
                      <strong>{project?.governed_name ?? outcome.governed_name}</strong>
                      <small>{outcome.presentation_category}</small>
                    </span>
                    <span className="historical-amount">
                      {formatCompactDollars(outcome.january_recommendation_dollars ?? 0)}
                    </span>
                  </summary>
                  <div className="historical-project-evidence">
                    <div>
                      <span>Historical recommendation</span>
                      <strong>
                        {formatDollars(outcome.january_recommendation_dollars ?? 0)}
                      </strong>
                      <small>Observed historical outcome</small>
                    </div>
                    <div>
                      <span>Governed project request</span>
                      <strong>{formatDollars(project?.model_request_dollars ?? 0)}</strong>
                    </div>
                    <div>
                      <span>Governed Funding Priority</span>
                      <strong>
                        {project === undefined
                          ? 'Unavailable'
                          : `${formatFundingPriority(project.funding_priority_score)} · Rank ${project.funding_priority_rank}`}
                      </strong>
                    </div>
                  </div>
                  {(outcome.source_conflict_flag || outcome.request_version_conflict) && (
                    <p className="benchmark-conflict-note">
                      The governed record retains source or request-version conflict
                      context. Historical status does not resolve that provenance.
                    </p>
                  )}
                </details>
              </li>
            )
          })}
        </ul>
      </section>

      <section className="benchmark-method-note" aria-labelledby="benchmark-method-heading">
        <div>
          <h2 id="benchmark-method-heading">Benchmark provenance</h2>
          <p>{benchmark.limitations.join(' ')}</p>
        </div>
        <details>
          <summary>Runtime and source identity</summary>
          <dl>
            <div>
              <dt>Data version</dt>
              <dd>{responseIdentity.data_version}</dd>
            </div>
            <div>
              <dt>Release ID</dt>
              <dd className="project-id">{responseIdentity.release_id}</dd>
            </div>
            <div>
              <dt>Historical source</dt>
              <dd>{benchmark.source_id}</dd>
            </div>
            <div>
              <dt>Source snapshot SHA-256</dt>
              <dd className="project-id">{benchmark.source_snapshot_sha256}</dd>
            </div>
          </dl>
        </details>
      </section>
    </main>
  )
}
