# ClimateCapital AI Product Plan

> **Status:** Approved Product and Design Lock through Stage 4
> **Locked:** 2026-08-26
> **Authority:** This document is the authoritative product-level definition of
> what ClimateCapital AI is, who it serves, why it exists, and the boundaries of
> the Austin MVP. Detailed backlog acceptance criteria are in
> [user-stories.md](user-stories.md), and the authoritative interface
> specification is in [screen-spec.md](screen-spec.md).

## Product Vision

ClimateCapital AI is a reusable public-sector decision-support product that turns
fragmented project, climate, equity, cost, and geographic evidence into transparent
draft capital-portfolio recommendations. The Austin Watershed historical simulation
is its first pilot, not the permanent product boundary.

The product should help planners compare and prioritize climate-relevant capital
projects by combining capital-project data, place-based climate risk, social
vulnerability, transparent deterministic analysis, constrained funding scenarios,
and grounded Gemini explanations.

## Primary User and Problem

### Primary user

The sole P0 persona is a representative City of Austin capital planning analyst, or
an equivalent cross-department planning analyst, who evaluates project requests and
prepares recommendations but does not authorize funding. The analyst understands
budgets, tables, filters, and maps but need not be a GIS, data-engineering, or AI
specialist.

### Problem

The analyst must reconcile fragmented project requests, place-based risk, equity
need, cost, readiness, data quality, and uncertainty. Individual rankings do not
answer which combination of projects fits a constrained funding envelope, and the
resulting tradeoffs are difficult to explain and defend.

### Value proposition

ClimateCapital AI helps the analyst create a defensible draft portfolio within a
documented funding envelope. Place-based evidence and deterministic analysis
establish the result; governed scenario controls and a bounded Gemini copilot help
the analyst inspect, challenge, revise, and explain it without surrendering human
decision authority.

## Goals and Success Definition

- Submit a compelling Patchamomma MVP by September 7, 2026 at 10:00 a.m. CDT.
- Demonstrate credible analytics and data-engineering skill through transparent,
  reproducible evidence, scoring, ranking, constraints, and portfolio outcomes.
- Keep Google Cloud spending very low.
- Finish a deployed and tested required-P0 product before the deadline.
- Make the planner problem and value legible quickly to program and technical
  reviewers.
- Complete the core product story in three minutes and expand it coherently to
  five minutes if needed.
- Keep every displayed or Gemini-cited number consistent with authoritative
  deterministic results.

The initial audience is assumed to be Google Cloud program and technical reviewers,
followed by an industry-facing finale if selected. The official judging rubric,
submission artifacts, finale date, and live-demo format remain unconfirmed.

## Austin Pilot and Historical Context

The P0 pilot is a historical simulation of individually named Austin Watershed
project requests.

- **January 21, 2026 Historical Decision Snapshot:** The dated context of the City
  of Austin 2026 Bond Initial Draft Project Recommendation. It is context, not an
  arbitrary product date or an analytical result.
- **Historical City Recommendation:** The published January 2026 City Initial
  Recommendation. It is a descriptive benchmark only and never influences
  ClimateCapital eligibility, evidence, scoring, ranking, weights, or portfolio
  selection.
- **ClimateCapital Historical Baseline Scenario:** ClimateCapital's deterministic
  result under the documented January 2026 context, the $125 million Projects
  sub-envelope, and the later-approved methodology.
- **Analyst-created What-If Scenario:** A confirmed deterministic run in which the
  analyst changed only Available Budget or approved weights.

The historical Watershed allocation is $160 million, of which $125 million is the
Projects allocation. P0 uses that $125 million sub-envelope as the ClimateCapital
Historical Baseline constraint for the rule-derived cohort of eligible,
individually named project requests. The remaining Watershed allocations are
outside the P0 portfolio and are not unallocated project funds.

The January 21 date establishes the historical bond decision context. External
evidence may use other defensible vintages; every source and vintage must be
documented explicitly.

## Product Principles

1. **Deterministic analysis is authoritative.** Eligibility, evidence
   transformations, scoring, ranking, constraints, and portfolio outcomes come
   from documented analytical logic, not Gemini.
2. **The analyst retains control.** Gemini can explain governed results or propose
   permitted scenario inputs, but the analyst must review and confirm before the
   deterministic system recalculates.
3. **Historical outcomes do not leak into analysis.** The Historical City
   Recommendation is a descriptive comparison, never training data, ground truth,
   an objective, or an input.
4. **Eligibility is reproducible.** Candidate projects are derived from documented
   rules. The expected range of 15–30 is not a target, and projects may not be
   manually selected to improve the demo.
5. **Ranking and constrained selection are different decisions.** A project's
   individual Funding Priority does not determine its Funding Plan membership.
6. **P0 uses full-project selection.** A ClimateCapital scenario includes or
   excludes an entire project. Partial funding is intentionally out of scope;
   published City treatment remains represented as published.
7. **Evidence limitations are visible.** Unsupported metrics are omitted, approved
   but missing project values are explicit, missing is never treated as zero, and
   confidence means evidence quality/completeness rather than decision correctness.
8. **The product works without Gemini.** Deterministic evidence, manual scenario
   controls, and Funding Plan results remain available when Gemini is unavailable.
9. **Progressive disclosure protects clarity.** Explore stays map-focused; full
   portfolio, scenario, benchmark, and review workflows live in Funding Plan.
10. **Accessibility and non-map access are required.** Every project and required
    action has a keyboard-usable, labeled, non-map path.

## Approved P0 Product Scope

- A rule-derived cohort of eligible, individually named Watershed project requests.
- A Map → Projects → Portfolio journey.
- Flood exposure and expected flood-reduction benefit as primary recommendation
  signals, subject to the evidence-stage methodology.
- Social vulnerability as a cross-cutting equity lens.
- Transparent eligibility, evidence, ranking, constrained portfolio selection,
  uncertainty, and source/vintage disclosure.
- One immutable ClimateCapital Historical Baseline and at most one active,
  confirmed What-If Scenario.
- Scenario controls limited to Available Budget and approved weights.
- Full-project inclusion/exclusion and optimizer-controlled membership without
  manual project overrides.
- Historical City Recommendation comparison as a descriptive benchmark.
- Grounded Gemini explanations and structured scenario proposals within approved
  inputs.
- Current-session Reviewed Draft designation without persistence or approval
  semantics.
- Desktop-first, tablet-usable, accessible and resilient interaction.

Exactly-two-project Compare is conditional SP0-1, not release-blocking, and the
first scope cut. See [user-stories.md](user-stories.md) for all required P0,
conditional SP0-1, P1, and Later acceptance intent.

## P1 and Deferred Direction

P1, in priority order:

1. Parks and Urban Heat as a separate, dated, constrained scenario.
2. Saved and multiple What-If scenarios.
3. Leadership-oriented export.
4. Full scenario comparison.
5. Broader grounded copilot intents.
6. Field-level audit depth and a full eligibility workspace.
7. Advanced spatial selection and custom-area analysis.

Later direction includes transportation as a separately constrained category,
multi-category caps and transfer rules, a clearly hypothetical flexible citywide
scenario, verified partial-funding models, richer optimization objectives,
comparison of three or more projects, accounts and collaboration, full mobile
support, and validated outcome tracking or prediction.

No P1 work begins before submission unless every required P0 story is complete at
least 24 hours early and at least 10 contingency hours remain.

## Explicit Non-Goals

- An official funding decision, prediction, current ballot package, or statement of
  City policy.
- Manually curated candidates or an unrestricted cross-department funding pool.
- Partial project funding in ClimateCapital scenarios.
- Editing source data, project costs, eligibility, analytical constraints, or
  Funding Plan membership.
- Saved/multiple P0 scenarios, permanent accounts, collaboration, formal approval,
  sharing, or report export.
- Separate stakeholder workflows in P0.
- Gemini-authored scores, ranks, constraints, evidence, or portfolio selections.
- Urban heat as a P0 score input. Heat may appear only as defensible context or a
  clearly labeled, project-specific co-benefit when the evidence gate supports it.

## Primary Product Workflow

1. **Orient in Explore:** See the historical decision context, current confirmed
   scenario, Available Budget, eligible cohort context, map, Recommended Projects,
   and a grounded spatial insight.
2. **Inspect a project:** Open the shared Project Detail through a list row or map
   marker path and examine governed evidence, Funding Priority, confidence,
   provenance, missingness, and Funding Plan status.
3. **Review the Funding Plan:** Inspect the deterministic full-project
   recommendation, active budget and constraints, Recommended and Not Included
   candidates, and the separation between individual rank and constrained
   membership.
4. **Run one governed What-If:** Change only budget or approved weights, validate
   and confirm the change, and review supported differences from the immutable
   Historical Baseline.
5. **Request a grounded explanation:** Use Gemini to explain governed evidence,
   rank, membership, constraints, or scenario changes without changing analytical
   authority.
6. **Mark the result as Reviewed Draft:** Designate the exact confirmed result for
   the current session with a draft/non-official disclaimer.

The full interface contract and recovery behavior are in
[screen-spec.md](screen-spec.md).

## Demo/Product Narrative

The three-minute core demo follows the workflow above:

- Establish the January 2026 historical context and current confirmed scenario.
- Reveal one defensible spatial flood/equity pattern in Explore.
- Inspect one project's evidence and portfolio status.
- Show the constrained Funding Plan and why rank can differ from membership.
- Confirm one permitted What-If change and show supported deltas.
- Ask for one grounded explanation and mark the reviewed result as the
  current-session draft.

A five-minute version may add Historical Benchmark, deeper methodology and
provenance, recovery behavior, or exactly-two-project Compare if SP0-1 survives.

## Assumptions and Dependencies

- The final cohort, source vintages, defensible geometry, scoring dimensions,
  transformations, default/editable weights, confidence methodology and warning
  threshold, optimization objective, missing-evidence treatment, and supported
  portfolio metrics remain evidence-stage decisions.
- People Potentially Benefiting and Implementation Readiness are not guaranteed
  fields. Each appears only if the underlying metric is approved.
- Community Vulnerability and Community Equity remain distinct wherever they
  represent different approved measures.
- The evidence stage determines the defensible default analytical map
  visualization and any project-specific heat co-benefit treatment.
- Architecture, data design, cloud cost design, data lineage, implementation plans,
  and test plans are not yet approved.

## Product Risks

- Required P0 breadth is ambitious for the September 2 feature freeze.
- The rule-derived cohort or geometry coverage may be less demo-friendly than
  expected and must not be manually improved.
- Unresolved scoring and confidence choices may undermine trust if rushed.
- The Historical Decision Snapshot, Historical City Recommendation, current
  confirmed scenario, and immutable Historical Baseline can be confused if locked
  terminology is not applied consistently.
- Unsupported metrics, UI-invented confidence warnings, or missing-as-zero
  treatment would mislead users.
- Gemini scope could consume disproportionate time; deterministic and manual paths
  remain the release priority.

## Related Sources of Truth

- [User stories and acceptance intent](user-stories.md)
- [Screen and interaction specification](screen-spec.md)
- [Delivery execution plan](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
