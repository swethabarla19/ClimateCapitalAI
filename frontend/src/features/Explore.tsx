import { useEffect, useMemo, useRef } from 'react'
import type {
  RuntimeCatalog,
  RuntimeMapContext,
  RuntimeProject,
  PublicConfiguration,
} from '../api/contracts'
import { AustinContextMap } from '../components/AustinContextMap'
import { ProjectDetail } from '../components/ProjectDetail'
import {
  formatDollars,
  formatFundingPriority,
} from '../lib/format'
import type {
  BrowserSessionState,
  PresentationState,
} from '../session/contracts'
import {
  readExploreFilters,
  resetExploreFilters,
  selectExploreProject,
  setExploreCategoryFilter,
  setExplorePriorityFilter,
  setExploreRequestAmountFilter,
  setExploreSearch,
  setExploreSort,
  type CategoryFilter,
  type PriorityFilter,
  type RequestAmountFilter,
} from '../session/exploreState'

interface ExploreProps {
  catalog: RuntimeCatalog
  mapContext: RuntimeMapContext
  publicConfiguration: PublicConfiguration
  session: BrowserSessionState
  onSessionChange: (session: BrowserSessionState) => void
  onOpenFundingPlan?: () => void
}

function matchesRequestAmount(
  project: RuntimeProject,
  filter: RequestAmountFilter,
): boolean {
  const request = project.model_request_dollars

  if (filter === 'UNDER_5M') return request < 5_000_000
  if (filter === '5M_TO_20M') return request >= 5_000_000 && request < 20_000_000
  if (filter === '20M_TO_50M') return request >= 20_000_000 && request < 50_000_000
  if (filter === '50M_PLUS') return request >= 50_000_000
  return true
}

function priorityRankLimit(filter: PriorityFilter): number | null {
  if (filter === 'TOP_10') return 10
  if (filter === 'TOP_25') return 25
  if (filter === 'TOP_50') return 50
  return null
}

function compareDecisionUnitId(
  left: RuntimeProject,
  right: RuntimeProject,
): number {
  return left.decision_unit_id.localeCompare(right.decision_unit_id)
}

function sortProjects(
  projects: RuntimeProject[],
  sort: PresentationState['sort'],
): RuntimeProject[] {
  return [...projects].sort((left, right) => {
    if (sort === 'REQUEST_DESC') {
      return (
        right.model_request_dollars - left.model_request_dollars ||
        compareDecisionUnitId(left, right)
      )
    }

    if (sort === 'REQUEST_ASC') {
      return (
        left.model_request_dollars - right.model_request_dollars ||
        compareDecisionUnitId(left, right)
      )
    }

    if (sort === 'NAME') {
      return (
        left.governed_name.localeCompare(right.governed_name, 'en-US') ||
        compareDecisionUnitId(left, right)
      )
    }

    return (
      right.funding_priority_score - left.funding_priority_score ||
      left.funding_priority_rank - right.funding_priority_rank ||
      compareDecisionUnitId(left, right)
    )
  })
}

function mapEvidenceLabel(
  feature: RuntimeMapContext['features'][number] | undefined,
): string {
  if (feature === undefined) return 'Location unavailable'
  if (feature.properties.display_role === 'PARK_SITE_CONTEXT') {
    return 'Park/site context'
  }
  if (feature.properties.display_role === 'FACILITY_SITE_CONTEXT') {
    return 'Facility/site context'
  }
  return 'Project location'
}

export function Explore({
  catalog,
  mapContext,
  publicConfiguration,
  session,
  onSessionChange,
  onOpenFundingPlan = () => undefined,
}: ExploreProps) {
  const projectButtonRefs = useRef(new Map<string, HTMLButtonElement>())
  const pendingMapSelection = useRef<string | null>(null)
  const filters = readExploreFilters(session.presentation)
  const normalizedSearch = session.presentation.search_text.trim().toLocaleLowerCase()

  const visibleProjects = useMemo(() => {
    const rankLimit = priorityRankLimit(filters.priority)
    const matching = catalog.projects.filter((project) => {
      const nameMatches =
        normalizedSearch.length === 0 ||
        project.governed_name.toLocaleLowerCase().includes(normalizedSearch)
      const categoryMatches =
        filters.category === 'ALL' ||
        project.presentation_category === filters.category
      const priorityMatches =
        rankLimit === null || project.funding_priority_rank <= rankLimit

      return (
        nameMatches &&
        categoryMatches &&
        priorityMatches &&
        matchesRequestAmount(project, filters.requestAmount)
      )
    })

    return sortProjects(matching, session.presentation.sort)
  }, [catalog.projects, filters, normalizedSearch, session.presentation.sort])

  const selectedProject =
    session.presentation.selected_decision_unit_id === null
      ? null
      : catalog.projects.find(
          (project) =>
            project.decision_unit_id ===
            session.presentation.selected_decision_unit_id,
        ) ?? null

  const selectedMapFeature =
    selectedProject === null
      ? null
      : mapContext.features.find(
          (feature) =>
            feature.properties.decision_unit_id ===
            selectedProject.decision_unit_id,
        ) ?? null

  const mapFeatureByDecisionUnitId = useMemo(
    () =>
      new Map(
        mapContext.features.map((feature) => [
          feature.properties.decision_unit_id,
          feature,
        ]),
      ),
    [mapContext.features],
  )

  const visibleDecisionUnitIds = useMemo(
    () => new Set(visibleProjects.map((project) => project.decision_unit_id)),
    [visibleProjects],
  )

  useEffect(() => {
    const selectedDecisionUnitId =
      session.presentation.selected_decision_unit_id

    if (
      selectedDecisionUnitId === null ||
      pendingMapSelection.current !== selectedDecisionUnitId
    ) {
      return
    }

    projectButtonRefs.current
      .get(selectedDecisionUnitId)
      ?.scrollIntoView?.({ block: 'nearest' })
    pendingMapSelection.current = null
  }, [session.presentation.selected_decision_unit_id])

  const hasActiveFilters =
    session.presentation.search_text.length > 0 ||
    filters.category !== 'ALL' ||
    filters.priority !== 'ALL' ||
    filters.requestAmount !== 'ALL'

  const visibleRequestTotal = visibleProjects.reduce(
    (total, project) => total + project.model_request_dollars,
    0,
  )

  return (
    <main id="explore" className="main-content explore-page">
      <section className="explore-intro" aria-labelledby="explore-heading">
        <div>
          <p className="eyebrow">
            January 21, 2026 project snapshot
          </p>
          <h1 id="explore-heading">Explore projects</h1>
          <p>
            Search, filter, and inspect governed projects across the map and list.
            Display controls do not change analytical results.
          </p>
        </div>
        <aside className="explore-snapshot-summary" aria-label="Project portfolio summary">
          <div className="snapshot-metrics">
            <span><strong>{catalog.project_count}</strong> governed projects</span>
            <span>
              <strong>{formatDollars(catalog.governed_request_total_dollars)}</strong>{' '}
              requests
            </span>
            <span>
              <strong>{mapContext.mapped_project_count} mapped</strong> ·{' '}
              {mapContext.unmapped_project_count} location unavailable
            </span>
          </div>
          <div
            className="snapshot-categories"
            role="region"
            aria-label="Project category counts"
          >
            <span>Transportation <strong>{catalog.category_counts.transportation}</strong></span>
            <span>Parks &amp; Open Space <strong>{catalog.category_counts.parks_open_space}</strong></span>
            <span>Watershed <strong>{catalog.category_counts.watershed}</strong></span>
            <span>Community Facilities <strong>{catalog.category_counts.community_facilities}</strong></span>
          </div>
        </aside>
      </section>

      <section className="explore-controls" aria-labelledby="discovery-heading">
        <div className="controls-heading">
          <div>
            <p className="eyebrow">Project discovery</p>
            <h2 id="discovery-heading">Find projects</h2>
          </div>
          <button
            type="button"
            className="text-button"
            disabled={!hasActiveFilters}
            onClick={() => onSessionChange(resetExploreFilters(session))}
          >
            Clear filters
          </button>
        </div>

        <div className="filter-grid">
          <label className="search-field">
            <span>Search project name</span>
            <input
              id="explore-project-search"
              name="project-search"
              type="search"
              value={session.presentation.search_text}
              placeholder="Search projects"
              onChange={(event) =>
                onSessionChange(setExploreSearch(session, event.target.value))
              }
            />
          </label>

          <label>
            <span>Category</span>
            <select
              id="explore-category-filter"
              name="category-filter"
              value={filters.category}
              onChange={(event) =>
                onSessionChange(
                  setExploreCategoryFilter(
                    session,
                    event.target.value as CategoryFilter,
                  ),
                )
              }
            >
              <option value="ALL">All categories</option>
              <option value="Transportation">Transportation</option>
              <option value="Parks & Open Space">Parks &amp; Open Space</option>
              <option value="Watershed">Watershed</option>
              <option value="Community Facilities">Community Facilities</option>
            </select>
          </label>

          <label>
            <span>Funding Priority</span>
            <select
              id="explore-priority-filter"
              name="priority-filter"
              value={filters.priority}
              onChange={(event) =>
                onSessionChange(
                  setExplorePriorityFilter(
                    session,
                    event.target.value as PriorityFilter,
                  ),
                )
              }
            >
              <option value="ALL">All ranks</option>
              <option value="TOP_10">Top priority ranks 1–10</option>
              <option value="TOP_25">Top priority ranks 1–25</option>
              <option value="TOP_50">Top priority ranks 1–50</option>
            </select>
          </label>

          <label>
            <span>Governed request</span>
            <select
              id="explore-request-filter"
              name="request-filter"
              value={filters.requestAmount}
              onChange={(event) =>
                onSessionChange(
                  setExploreRequestAmountFilter(
                    session,
                    event.target.value as RequestAmountFilter,
                  ),
                )
              }
            >
              <option value="ALL">All request amounts</option>
              <option value="UNDER_5M">Under $5M</option>
              <option value="5M_TO_20M">$5M to under $20M</option>
              <option value="20M_TO_50M">$20M to under $50M</option>
              <option value="50M_PLUS">$50M and above</option>
            </select>
          </label>

          <label>
            <span>Sort projects</span>
            <select
              id="explore-sort"
              name="project-sort"
              value={session.presentation.sort}
              onChange={(event) =>
                onSessionChange(
                  setExploreSort(
                    session,
                    event.target.value as PresentationState['sort'],
                  ),
                )
              }
            >
              <option value="FUNDING_PRIORITY">Funding Priority — highest first</option>
              <option value="REQUEST_DESC">Governed request — highest first</option>
              <option value="REQUEST_ASC">Governed request — lowest first</option>
              <option value="NAME">Project name — alphabetical</option>
            </select>
          </label>

          <button
            type="button"
            className="filter-reset-button"
            disabled={!hasActiveFilters}
            onClick={() => onSessionChange(resetExploreFilters(session))}
          >
            Clear filters
          </button>
        </div>
      </section>

      <div className="explore-workspace">
        <AustinContextMap
          mapContext={mapContext}
          publicConfiguration={publicConfiguration}
          visibleDecisionUnitIds={visibleDecisionUnitIds}
          selectedDecisionUnitId={
            session.presentation.selected_decision_unit_id
          }
          onSelectProject={(decisionUnitId) => {
            pendingMapSelection.current = decisionUnitId
            onSessionChange(
              selectExploreProject(session, decisionUnitId),
            )
          }}
        />
        <section className="projects-panel" aria-labelledby="projects-heading">
          <div className="projects-heading">
            <div>
              <h2 id="projects-heading">Projects</h2>
              <p
                aria-label={`${visibleProjects.length} of ${catalog.project_count} projects`}
                aria-live="polite"
                aria-atomic="true"
              >
                <strong>{visibleProjects.length}</strong> of {catalog.project_count}{' '}
                projects · {formatDollars(visibleRequestTotal)} in governed requests
              </p>
            </div>
          </div>

          {visibleProjects.length === 0 ? (
            <div className="empty-results" role="status">
              <h3>No projects match these filters</h3>
              <p>Adjust the discovery controls or clear them to see all projects.</p>
              <button
                type="button"
                onClick={() => onSessionChange(resetExploreFilters(session))}
              >
                Clear filters
              </button>
            </div>
          ) : (
            <ul className="explore-project-list">
              {visibleProjects.map((project) => {
                const selected =
                  project.decision_unit_id ===
                  session.presentation.selected_decision_unit_id
                const mapFeature = mapFeatureByDecisionUnitId.get(
                  project.decision_unit_id,
                )
                const evidenceLabel = mapEvidenceLabel(mapFeature)

                return (
                  <li key={project.decision_unit_id}>
                    <button
                      type="button"
                      className={
                        selected
                          ? 'explore-project-card explore-project-card-selected'
                          : 'explore-project-card'
                      }
                      aria-pressed={selected}
                      aria-label={`View details for ${project.governed_name}`}
                      ref={(element) => {
                        if (element === null) {
                          projectButtonRefs.current.delete(
                            project.decision_unit_id,
                          )
                        } else {
                          projectButtonRefs.current.set(
                            project.decision_unit_id,
                            element,
                          )
                        }
                      }}
                      onClick={() =>
                        onSessionChange(
                          selectExploreProject(session, project.decision_unit_id),
                        )
                      }
                    >
                      <span className="project-card-heading">
                        <span className="project-name">{project.governed_name}</span>
                        <span className="category-badge">
                          {project.presentation_category}
                        </span>
                      </span>
                      <span className="project-source">{project.source_department}</span>
                      <span
                        className={
                          mapFeature === undefined
                            ? 'project-map-status project-map-status-unavailable'
                            : `project-map-status ${
                                mapFeature.properties.display_role ===
                                'PARK_SITE_CONTEXT'
                                  ? 'project-map-status-park'
                                  : mapFeature.properties.display_role ===
                                      'FACILITY_SITE_CONTEXT'
                                    ? 'project-map-status-facility'
                                    : 'project-map-status-project'
                              }`
                        }
                      >
                        <span aria-hidden="true">●</span>
                        {evidenceLabel}
                      </span>
                      <span className="project-card-metrics">
                        <span>
                          <small>Governed request</small>
                          <strong>{formatDollars(project.model_request_dollars)}</strong>
                        </span>
                        <span>
                          <small>Funding Priority</small>
                          <strong>
                            {formatFundingPriority(project.funding_priority_score)} · Rank{' '}
                            {project.funding_priority_rank}
                          </strong>
                        </span>
                      </span>
                      {project.is_tied && (
                        <span className="tie-badge">
                          Shared rank · {project.tie_group_size} projects
                        </span>
                      )}
                    </button>
                  </li>
                )
              })}
            </ul>
          )}
        </section>

        {selectedProject !== null && (
          <div className="detail-panel-region" aria-live="polite">
            <ProjectDetail
              project={selectedProject}
              mapFeature={selectedMapFeature}
              onClose={() =>
                onSessionChange(selectExploreProject(session, null))
              }
            />
          </div>
        )}
      </div>

      <section className="priority-explainer" aria-label="Funding Priority explanation">
        <strong>How Funding Priority works</strong>
        <span>
          It is the official January 21, 2026 PRB Grand Total and is used as an
          ordinal project-priority measure. Equal scores share the same competition
          rank; within-tie display order has no analytical meaning.
        </span>
      </section>

      <section className="explore-plan-strip" aria-label="Current Funding Plan status">
        <div>
          <span className="metric-icon metric-icon-purple" aria-hidden="true">▥</span>
          <span><strong>Current Funding Plan</strong><small>Governed full-request projects</small></span>
        </div>
        {session.latest_plan_result === null ? (
          <strong>No evaluated plan in this session</strong>
        ) : (
          <strong>
            {session.latest_plan_result.selected_projects.length} projects ·{' '}
            {formatDollars(session.latest_plan_result.included_total_dollars)} selected
          </strong>
        )}
        <button type="button" className="primary-outline-button" onClick={onOpenFundingPlan}>
          View Funding Plan <span aria-hidden="true">→</span>
        </button>
      </section>

      <section className="disclaimer" aria-label="Prototype disclaimer">
        <strong>Historical decision-support prototype.</strong>
        <span>
          Funding Priority is ordinal decision support, not public benefit,
          cost-effectiveness, predicted recommendation, or an official funding
          decision.
        </span>
      </section>
    </main>
  )
}
