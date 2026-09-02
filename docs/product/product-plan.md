# ClimateCapital AI Product Plan

> **Status:** Approved Product and Design Lock, reconciled with Methodology Lock
> **Locked:** 2026-08-26; evidence-driven reconciliation 2026-09-01
> **Authority:** This document is the authoritative product-level definition of
> what ClimateCapital AI is, who it serves, why it exists, and the boundaries of
> the Austin MVP. Detailed backlog acceptance criteria are in
> [user-stories.md](user-stories.md), and the authoritative interface
> specification is in [screen-spec.md](screen-spec.md).

## Product Vision

ClimateCapital AI is a reusable public-sector decision-support product that turns
fragmented project, climate, equity, cost, and geographic evidence into transparent
analyst-reviewed capital-funding scenarios. The Austin Watershed historical
simulation is its first pilot, not the permanent product boundary.

The product helps planners inspect governed project facts, understand the coverage
and limits of place-based evidence, assemble full-request scenarios under an
Available Budget, compare supported scenario changes, and use grounded Gemini
explanations without fabricating a priority model that the evidence cannot support.

## Primary User and Problem

### Primary user

The sole P0 persona is a representative City of Austin capital planning analyst, or
an equivalent cross-department planning analyst, who evaluates project requests and
prepares recommendations but does not authorize funding. The analyst understands
budgets, tables, filters, and maps but need not be a GIS, data-engineering, or AI
specialist.

### Problem

The analyst must reconcile fragmented project requests, purpose, place-based
hazard and vulnerability context, cost, data quality, and uncertainty. The current
evidence does not support a common numeric benefit, risk, or equity measure across
the P0 family, so unsupported rankings would make the resulting tradeoffs harder,
not easier, to defend.

### Value proposition

ClimateCapital AI helps the analyst create and review a transparent draft funding
scenario within a documented envelope. Governed facts, explicit evidence roles,
missingness, full-request controls, and deterministic budget arithmetic establish
the result; a bounded Gemini copilot helps the analyst inspect and explain it
without surrendering human decision authority.

## Goals and Success Definition

- Submit a compelling Patchamomma MVP by September 7, 2026 at 10:00 a.m. CDT.
- Demonstrate credible analytics and data-engineering skill through transparent,
  reproducible evidence governance, purpose classification, missingness, scenario
  validation, budget arithmetic, provenance, and supported comparisons.
- Keep Google Cloud spending very low.
- Finish a deployed and tested required-P0 product before the deadline.
- Make the planner problem and value legible quickly to program and technical
  reviewers.
- Complete the core product story in three minutes and expand it coherently to
  five minutes if needed.
- Keep every displayed or Gemini-cited number and evidence state consistent with
  authoritative deterministic results.

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
  Recommendation. It is a descriptive benchmark only, held structurally apart
  from project evidence, analytical-family definition, analyst membership,
  validation, and scenario arithmetic.
- **Session Reference Plan:** The first analyst-confirmed
  full-request plan created under the documented January 2026 context and the
  $125 million default Projects envelope. It becomes an immutable current-session
  comparison reference; it is not a historical baseline, optimized
  recommendation, Historical City Recommendation, or City plan.
- **Current Confirmed Plan:** The active analyst-confirmed plan, which is either the
  Session Reference Plan or the confirmed What-If Scenario.
- **Analyst-created What-If Scenario:** One confirmed deterministic scenario in
  which the analyst changed Available Budget and/or project membership.

The historical Watershed allocation is $160 million, of which $125 million is the
Projects allocation. P0 uses that $125 million sub-envelope as the default
Historical Envelope context for the derived 12-record local flood/local drainage
analytical family. It does not determine the family, force inclusion, or become an
eligibility threshold. The remaining Watershed allocations are outside the P0
Funding Plan and are not unallocated project funds.

The January 21 date establishes the historical bond decision context. External
evidence may use other defensible vintages; every source and vintage must be
documented explicitly.

## Product Principles

1. **Deterministic governed behavior is authoritative.** Source facts, derived
   purpose classifications, evidence roles, scenario validation, full-request
   membership-state validation, budget arithmetic, and supported comparisons come
   from documented logic and confirmed analyst inputs, not Gemini. Deterministic
   logic does not choose membership.
2. **The analyst retains control.** Gemini can explain governed results or translate
   an explicit analyst command into a pending permitted scenario action, but the
   analyst must review and confirm before the deterministic system recalculates.
3. **Historical outcomes do not leak into analysis.** The Historical City
   Recommendation is a descriptive comparison, never training data, ground truth,
   an objective, or an input.
4. **Family derivation is reproducible and qualified.** The provisional 12-record
   P0 analytical family is derived from all 37 governed records using a documented
   ClimateCapital purpose classification with confidence and ambiguity. It is not
   a City taxonomy or declaration of eligibility.
5. **No unsupported priority model.** P0 has no Funding Priority score, rank,
   Importance weights, expected flood-reduction metric, or optimizer objective.
   Funding Plan membership is an explicit analyst choice constrained by budget.
6. **P0 uses full-request membership.** A ClimateCapital plan includes or excludes
   the complete governed request. Partial funding is intentionally out of scope;
   published City treatment remains represented as published.
7. **Evidence limitations are visible.** Every field is a fact, contextual
   evidence, research-only evidence, or unavailable/unsupported. Missing is never
   treated as zero or a penalty, and confidence describes evidence or
   classification strength rather than need or decision correctness.
8. **The product works without Gemini.** Governed evidence, analyst scenario
   controls, and deterministic Funding Plan arithmetic remain available when
   Gemini is unavailable.
9. **Progressive disclosure protects clarity.** Explore stays map-focused; full
   portfolio, scenario, benchmark, and review workflows live in Funding Plan.
10. **Accessibility and non-map access are required.** Every project and required
    action has a keyboard-usable, labeled, non-map path.

## Approved P0 Product Scope

- The governed all-37 Watershed universe plus a transparent derived 12-record
  local flood/local drainage P0 analytical family.
- A Map → Projects → Funding Plan journey.
- Documented City flood/problem association and current FEMA hazard context where
  available, explicitly as contextual evidence rather than project benefit.
- EAZ 2021 as a dated contextual vulnerability lens where defensible geography
  exists, not a cohort-wide score.
- Transparent purpose-family derivation, evidence roles, missingness, scenario
  membership, budget arithmetic, uncertainty, and source/vintage disclosure.
- One immutable Session Reference Plan and at most one active, confirmed What-If
  Scenario.
- Scenario controls limited to Available Budget and analyst-controlled inclusion
  or removal of complete governed requests within the active 12-record analytical
  family. Projects outside it remain visible in the all-37 governed-universe audit.
- Deterministic validation that confirmed membership fits the active envelope;
  no automatic ranking or optimization.
- Historical City Recommendation comparison as a descriptive benchmark.
- Grounded Gemini explanations and translation of explicit analyst budget or
  named-membership commands into reversible proposals. Gemini does not originate
  which projects should be funded.
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
scenario, verified partial-funding models, evidence-supported scoring or
optimization only after a later methodology revision, comparison of three or more
projects, accounts and collaboration, full mobile support, and validated outcome
tracking or prediction.

No P1 work begins before submission unless every required P0 story is complete at
least 24 hours early and at least 10 contingency hours remain.

## Explicit Non-Goals

- An official funding decision, prediction, current ballot package, or statement of
  City policy.
- A manually curated governed universe or unrestricted cross-department funding
  pool. Analyst membership choices within the active documented 12-record
  analytical family are P0.
- Partial project funding in ClimateCapital scenarios.
- Editing source data, governed request amounts, purpose classifications, evidence
  roles, or budget constraints. Analyst inclusion/removal within the P0 family is
  the intended Funding Plan action.
- Saved/multiple P0 scenarios, permanent accounts, collaboration, formal approval,
  sharing, or report export.
- Separate stakeholder workflows in P0.
- Numeric Funding Priority, Climate Risk, Community Vulnerability, Community
  Equity, expected flood-reduction benefit, Importance weights, project ranking,
  or optimized membership.
- Gemini-authored facts, evidence, purpose classifications, or recommendations.
- Urban heat as a P0 score input. Heat may appear only as defensible context or a
  clearly labeled, project-specific co-benefit when the evidence gate supports it.

## Primary Product Workflow

1. **Orient in Explore:** See the historical decision context, current confirmed
   plan or working-plan state, Available Budget, P0 analytical-family context,
   map, Projects list, and a grounded spatial insight.
2. **Inspect a project:** Open the shared Project Detail through a list row or map
   marker path and examine governed facts, evidence roles, confidence,
   provenance, missingness, and current scenario status.
3. **Build and review the Funding Plan:** Add or remove complete governed requests,
   inspect Included in Plan and Available Projects, and confirm only when exact
   budget arithmetic fits the active envelope.
4. **Run one governed What-If:** Change budget and/or project membership, validate
   and confirm the change, and review supported differences from the immutable
   Session Reference Plan.
5. **Request a grounded explanation:** Use Gemini to explain governed evidence,
   missingness, budget arithmetic, membership chosen by the analyst, or
   scenario changes without changing analytical authority.
6. **Mark the result as Reviewed Draft:** Designate the exact confirmed result for
   the current session with a draft/non-official disclaimer.

The full interface contract and recovery behavior are in
[screen-spec.md](screen-spec.md).

## Demo/Product Narrative

The three-minute core demo follows the workflow above:

- Establish the January 2026 historical context and Current Confirmed Plan.
- Reveal one defensible spatial flood/equity context in Explore with its limits.
- Inspect one project's evidence and missingness.
- Add or remove a project and show deterministic budget arithmetic.
- Confirm one permitted What-If change and show supported membership/dollar deltas.
- Ask for one grounded explanation and mark the reviewed result as the
  current-session draft.

A five-minute version may add Historical Benchmark, deeper methodology and
provenance, recovery behavior, or exactly-two-project Compare if SP0-1 survives.

## Assumptions and Dependencies

- The P0 methodology is authoritative in
  [p0-evidence-methodology.md](../methodology/p0-evidence-methodology.md). It fixes
  the governed universe, derived analytical family, evidence roles, missingness
  treatment, unsupported metrics, analyst-membership controls, and deterministic
  budget behavior.
- People Potentially Benefiting, Structures Benefited, and Implementation Readiness
  are unavailable/unsupported for the locked P0 unless a later explicit methodology
  revision governs the underlying metric.
- EAZ vulnerability context does not become a Watershed-specific equity method,
  beneficiary claim, Community Equity score, or cohort-wide Community
  Vulnerability score.
- Architecture/Product presentation must choose any default map visualization from
  the locked evidence roles without promoting context into a scoring input. Heat is
  omitted from P0 unless a later explicit methodology revision supports it.
- Architecture, data design, cloud cost design, data lineage, implementation plans,
  and test plans are not yet approved.

## Product Risks

- Required P0 breadth is ambitious for the September 2 feature freeze.
- The derived family or geometry coverage may be less demo-friendly than expected
  and must not be manually improved.
- Reintroducing unsupported scores, weights, ranks, optimization, or inferred
  beneficiary claims would contradict the Methodology Lock.
- The Historical Decision Snapshot, Historical Envelope, Historical City
  Recommendation, Current Confirmed Plan, and Session Reference Plan can be
  confused if locked terminology is not applied consistently.
- Unsupported metrics, UI-invented confidence warnings, missing-as-zero treatment,
  or language that implies analyst membership is an optimized recommendation would
  mislead users.
- Gemini scope could consume disproportionate time; deterministic and manual paths
  remain the release priority.

## Related Sources of Truth

- [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
- [User stories and acceptance intent](user-stories.md)
- [Screen and interaction specification](screen-spec.md)
- [Delivery execution plan](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
