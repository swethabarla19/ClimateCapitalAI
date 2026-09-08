import type { RuntimeProject } from '../api/contracts'
import {
  formatDollars,
  formatFundingPriority,
} from '../lib/format'

interface ProjectDetailProps {
  project: RuntimeProject
  onClose: () => void
}

const components: Array<{
  key: keyof RuntimeProject['prb_components']
  label: string
  maximum: number
}> = [
  { key: 'strategic_alignment', label: 'Strategic Alignment', maximum: 8 },
  { key: 'critical_asset', label: 'Critical Asset', maximum: 8 },
  {
    key: 'community_consideration',
    label: 'Community Consideration',
    maximum: 20,
  },
  { key: 'efficiency', label: 'Efficiency', maximum: 20 },
  {
    key: 'timeliness_readiness',
    label: 'Timeliness & Readiness',
    maximum: 24,
  },
  {
    key: 'climate_resilience',
    label: 'Climate Resilience',
    maximum: 20,
  },
]

function councilDistrictLabel(project: RuntimeProject): string {
  const { assignment_type: assignment, districts } = project.council_district

  if (assignment === 'CITYWIDE') return 'Citywide'
  if (assignment === 'UNSPECIFIED') return 'Not specified'

  return districts.length === 1
    ? `District ${districts[0]}`
    : `Districts ${districts.join(', ')}`
}

export function ProjectDetail({ project, onClose }: ProjectDetailProps) {
  const headingId = `project-detail-${project.decision_unit_id.replace(
    /[^A-Za-z0-9_-]/g,
    '-',
  )}`

  return (
    <aside className="project-detail" aria-labelledby={headingId}>
      <header className="project-detail-heading">
        <div>
          <p className="eyebrow">Project detail</p>
          <h2 id={headingId}>{project.governed_name}</h2>
          <span className="category-badge">{project.presentation_category}</span>
        </div>
        <button type="button" className="text-button" onClick={onClose}>
          Close detail
        </button>
      </header>

      <section aria-labelledby={`${headingId}-identity`}>
        <h3 id={`${headingId}-identity`}>Identity and source</h3>
        <dl className="detail-list">
          <div>
            <dt>Decision unit ID</dt>
            <dd className="project-id">{project.decision_unit_id}</dd>
          </div>
          {project.canonical_project_id !== null && (
            <div>
              <dt>Canonical project ID</dt>
              <dd>{project.canonical_project_id}</dd>
            </div>
          )}
          <div>
            <dt>Source department</dt>
            <dd>{project.source_department}</dd>
          </div>
          <div>
            <dt>Source domain</dt>
            <dd>{project.source_domain}</dd>
          </div>
        </dl>
      </section>

      <section aria-labelledby={`${headingId}-funding`}>
        <h3 id={`${headingId}-funding`}>Funding</h3>
        <p className="detail-emphasis">
          <span>Governed model request</span>
          <strong>{formatDollars(project.model_request_dollars)}</strong>
        </p>
        {project.request_version_conflict && (
          <p className="evidence-notice" role="note">
            A governed request-version conflict is preserved for this project.
            The displayed model request follows the runtime’s governed authority.
          </p>
        )}
      </section>

      <section aria-labelledby={`${headingId}-priority`}>
        <h3 id={`${headingId}-priority`}>Funding Priority</h3>
        <div className="priority-summary">
          <div>
            <span>Official PRB Grand Total</span>
            <strong>{formatFundingPriority(project.funding_priority_score)}</strong>
          </div>
          <div>
            <span>Competition rank</span>
            <strong>Rank {project.funding_priority_rank}</strong>
          </div>
        </div>
        {project.is_tied ? (
          <p className="tie-explanation">
            Shared rank with {project.tie_group_size} projects at the same official
            score. Display order within this tie has no analytical meaning.
          </p>
        ) : (
          <p className="tie-explanation">This project does not share its rank.</p>
        )}
        <p className="method-note">
          Funding Priority is the official January 21, 2026 PRB Grand Total and is
          used as an ordinal project-priority measure. Higher scores indicate higher
          priority; the score is not a benefit/cost or predicted recommendation.
        </p>
      </section>

      <section aria-labelledby={`${headingId}-components`}>
        <h3 id={`${headingId}-components`}>Official PRB components</h3>
        <p className="section-intro">
          Each component is shown against its own official rubric maximum.
        </p>
        <ul className="component-list">
          {components.map(({ key, label, maximum }) => {
            const value = project.prb_components[key]
            return (
              <li key={key}>
                <div>
                  <span>{label}</span>
                  <strong>
                    {formatFundingPriority(value)} / {maximum}
                  </strong>
                </div>
                <progress
                  value={value}
                  max={maximum}
                  aria-label={`${label}: ${formatFundingPriority(value)} of ${maximum}`}
                />
              </li>
            )
          })}
        </ul>
      </section>

      <section aria-labelledby={`${headingId}-context`}>
        <h3 id={`${headingId}-context`}>Context and provenance</h3>
        <dl className="detail-list">
          <div>
            <dt>Council District context</dt>
            <dd>{councilDistrictLabel(project)} · analyst review only</dd>
          </div>
          <div>
            <dt>Operations &amp; maintenance impact</dt>
            <dd>
              {project.om_impact.value === 'YES' ? 'Yes' : 'No'} · context only,
              not a portfolio constraint or score preference
            </dd>
          </div>
          <div>
            <dt>Model-request authority</dt>
            <dd>{project.model_request_authority}</dd>
          </div>
          <div>
            <dt>Authority source</dt>
            <dd className="project-id">
              {project.model_request_authority_source_id}
            </dd>
          </div>
          <div>
            <dt>Provenance references</dt>
            <dd>{project.provenance_refs.join(', ')}</dd>
          </div>
          <div>
            <dt>Project map location</dt>
            <dd>Unavailable in the governed January 21, 2026 snapshot</dd>
          </div>
        </dl>
      </section>
    </aside>
  )
}
