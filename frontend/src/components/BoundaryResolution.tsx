import { useMemo, useState } from 'react'
import type {
  BoundaryResolutionInput,
  BoundaryTierResult,
  RuntimeCatalog,
} from '../api/contracts'
import {
  formatDollars,
  formatFundingPriority,
} from '../lib/format'

interface BoundaryResolutionProps {
  boundary: BoundaryTierResult
  catalog: RuntimeCatalog
  initialResolution: BoundaryResolutionInput | null
  loading: boolean
  onSubmit: (resolution: BoundaryResolutionInput) => void
}

export function BoundaryResolution({
  boundary,
  catalog,
  initialResolution,
  loading,
  onSubmit,
}: BoundaryResolutionProps) {
  const [selectedIds, setSelectedIds] = useState<Set<string>>(
    () => new Set(initialResolution?.selected_decision_unit_ids ?? []),
  )
  const [acknowledged, setAcknowledged] = useState(
    initialResolution
      ?.advance_with_feasible_same_tier_project_acknowledged ?? false,
  )

  const catalogById = useMemo(
    () =>
      new Map(
        catalog.projects.map((project) => [project.decision_unit_id, project]),
      ),
    [catalog.projects],
  )
  const selectedAmount = boundary.candidates.reduce(
    (total, candidate) =>
      total +
      (selectedIds.has(candidate.decision_unit_id)
        ? candidate.model_request_dollars
        : 0),
    0,
  )
  const remainingAfterSelection =
    boundary.remaining_budget_before_tier_dollars - selectedAmount
  const selectionOverBudget = remainingAfterSelection < 0
  const feasibleProjectsLeft = boundary.candidates.filter(
    (candidate) =>
      !selectedIds.has(candidate.decision_unit_id) &&
      candidate.model_request_dollars <= remainingAfterSelection,
  )
  const acknowledgementRequired = feasibleProjectsLeft.length > 0
  const feasibleCount = boundary.candidates.filter(
    (candidate) => candidate.individually_budget_feasible,
  ).length
  const canSubmit =
    !loading &&
    !selectionOverBudget &&
    (!acknowledgementRequired || acknowledged)

  const toggleCandidate = (decisionUnitId: string) => {
    setSelectedIds((current) => {
      const next = new Set(current)
      if (next.has(decisionUnitId)) next.delete(decisionUnitId)
      else next.add(decisionUnitId)
      return next
    })
  }

  return (
    <section
      className="boundary-panel"
      aria-labelledby="boundary-priority-tier-heading"
    >
      <div className="boundary-heading">
        <div>
          <p className="eyebrow">Analyst resolution</p>
          <h2 id="boundary-priority-tier-heading">Boundary priority tier</h2>
        </div>
        <span className="status-badge status-boundary">
          Resolution required
        </span>
      </div>

      <p className="boundary-explanation">
        The remaining budget cannot fund this complete Funding Priority tier.
        These projects have equal official priority, so the system does not invent
        a tiebreaker. Choose among the feasible same-priority projects.
      </p>

      <dl className="boundary-summary">
        <div>
          <dt>Funding Priority</dt>
          <dd>{formatFundingPriority(boundary.funding_priority_score)}</dd>
        </div>
        <div>
          <dt>Competition rank</dt>
          <dd>Rank {boundary.funding_priority_rank}</dd>
        </div>
        <div>
          <dt>Remaining before tier</dt>
          <dd>{formatDollars(boundary.remaining_budget_before_tier_dollars)}</dd>
        </div>
        <div>
          <dt>Complete tier request</dt>
          <dd>{formatDollars(boundary.full_tier_request_dollars)}</dd>
        </div>
      </dl>

      <div className="boundary-list-heading">
        <h3>Projects in this tier</h3>
        <span>
          {feasibleCount} individually feasible · {boundary.candidates.length}{' '}
          total
        </span>
      </div>
      <p className="boundary-order-note">
        Candidate order is deterministic for display only. No analytical
        preference is assigned within this shared rank.
      </p>

      <ul className="boundary-candidates">
        {boundary.candidates.map((candidate) => {
          const project = catalogById.get(candidate.decision_unit_id)
          const selected = selectedIds.has(candidate.decision_unit_id)

          return (
            <li key={candidate.decision_unit_id}>
              <label
                className={
                  candidate.individually_budget_feasible
                    ? 'boundary-candidate'
                    : 'boundary-candidate boundary-candidate-infeasible'
                }
              >
                <input
                  type="checkbox"
                  checked={selected}
                  disabled={!candidate.individually_budget_feasible || loading}
                  aria-label={`Select ${project?.governed_name ?? candidate.decision_unit_id}, ${formatDollars(candidate.model_request_dollars)}, for analyst resolution`}
                  onChange={() => toggleCandidate(candidate.decision_unit_id)}
                />
                <span className="boundary-candidate-content">
                  <strong>
                    {project?.governed_name ?? candidate.decision_unit_id}
                  </strong>
                  <span>
                    {project?.presentation_category ?? 'Catalog record unavailable'}
                    {' · '}
                    {formatDollars(candidate.model_request_dollars)}
                  </span>
                  <span className="candidate-feasibility">
                    {candidate.individually_budget_feasible
                      ? 'Individually budget-feasible'
                      : 'Does not fit individually within the boundary budget'}
                  </span>
                </span>
              </label>
            </li>
          )
        })}
      </ul>

      <div className="boundary-choice-summary" aria-live="polite">
        <span>
          Analyst-selected in this tier
          <strong>{formatDollars(selectedAmount)}</strong>
        </span>
        <span>
          Remaining after this choice
          <strong>
            {formatDollars(Math.max(remainingAfterSelection, 0))}
          </strong>
        </span>
      </div>

      {selectionOverBudget && (
        <p className="validation-message" role="alert">
          This choice exceeds the boundary budget by{' '}
          {formatDollars(Math.abs(remainingAfterSelection))}. Remove one or more
          projects before submitting.
        </p>
      )}

      {acknowledgementRequired && !selectionOverBudget && (
        <label className="acknowledgement-control">
          <input
            type="checkbox"
            checked={acknowledged}
            disabled={loading}
            onChange={(event) => setAcknowledged(event.target.checked)}
          />
          <span>
            I acknowledge that I am leaving at least one budget-feasible project
            in this same Funding Priority tier unfunded before moving to a
            lower-priority tier.
          </span>
        </label>
      )}

      <div className="boundary-actions">
        <button
          type="button"
          disabled={!canSubmit}
          onClick={() =>
            onSubmit({
              funding_priority_score: boundary.funding_priority_score,
              funding_priority_rank: boundary.funding_priority_rank,
              selected_decision_unit_ids: [...selectedIds].sort(),
              advance_with_feasible_same_tier_project_acknowledged:
                acknowledgementRequired ? acknowledged : false,
            })
          }
        >
          {loading ? 'Submitting resolution…' : 'Submit analyst resolution'}
        </button>
        {acknowledgementRequired && !acknowledged && !selectionOverBudget && (
          <span>Explicit acknowledgement is required for this choice.</span>
        )}
      </div>
    </section>
  )
}
