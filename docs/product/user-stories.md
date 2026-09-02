# ClimateCapital AI User Stories

> **Status:** Approved backlog, reconciled with the 2026-09-01 Methodology Lock
> **Authority:** This is the authoritative prioritized backlog and acceptance
> intent. It preserves the 12 required P0 stories, conditional SP0-1, P1 order, and
> Later scope approved on 2026-08-26.

## Priority Model

- **Required P0:** Release-blocking for the Austin MVP.
- **Conditional stretch P0 (SP0-1):** Optional, not release-blocking, and the first
  scope cut if schedule or contingency is threatened.
- **P1:** May begin before submission only if required P0 is complete at least 24
  hours early and at least 10 contingency hours remain.
- **Later:** Explicitly deferred and cannot displace P0.

The sole P0 persona is the capital planning analyst defined in
[product-plan.md](product-plan.md). The authoritative screen behavior and recovery
states are in [screen-spec.md](screen-spec.md).

## Required P0

### P0-1 — Establish the historical context and scenario terminology

The analyst can always tell which historical context, City benchmark, or
ClimateCapital result is being viewed.

**Acceptance criteria:**

- Distinguish the January 21, 2026 Historical Decision Snapshot, Historical City
  Recommendation, Historical Envelope, Session Reference Plan, Current Confirmed
  Plan, and analyst-created What-If Scenario by name and status.
- State that the historical Watershed allocation was $160 million, that the
  $125 million Projects sub-envelope is the default Historical Envelope context,
  and that it neither defines the P0 family nor forces project inclusion.
- Label the experience as a historical simulation, not an official funding
  decision, prediction, or current ballot package.

### P0-2 — Derive and disclose the P0 analytical family

The analyst can understand how the complete governed universe was classified and
why the 12 local flood/local drainage records form the provisional P0 analytical
family.

**Acceptance criteria:**

- Show all 37 governed source records, their derived purpose classification,
  classification confidence, ambiguity, 12-record family membership, and the
  24-record broader flood-family limitation.
- State that the purpose classification and P0 family are ClimateCapital
  derivations, not a City taxonomy or eligibility decision.
- Preserve project `5789.150` as a citywide program inside the 12-record family
  with separate treatment rather than implying one project-level geography.
- Never use the Historical City Recommendation as a family, evidence, or scenario
  input; keep it structurally isolated from project evidence, family definition,
  analyst membership, validation, and scenario arithmetic.
- Do not remove a family record because geometry or contextual evidence is
  missing. Keep every record available through non-map and Funding Plan paths.

### P0-3 — Explore candidates and defensible evidence on a map

The analyst can use geography to enter the decision journey without losing access
to candidates that cannot be mapped.

**Acceptance criteria:**

- Display defensible project geography plus supported flood and equity context,
  with a legend and pan, zoom, and layer controls.
- Selecting mapped geography opens concise project and evidence detail.
- Never invent geometry. Keep family records without display geometry available
  in Projects and Funding Plan and label the limitation visibly.
- Provide a non-map path to every candidate and exclude drawing tools, custom GIS
  analysis, and unrelated map layers from P0.

### P0-4 — Inspect transparent project evidence

The analyst can examine governed facts, evidence roles, coverage, and missingness
independently from scenario membership.

**Acceptance criteria:**

- Show Department Request, derived purpose and confidence, current scenario status,
  and supported problem, geometry, FEMA, and EAZ context with its analytical role.
- Project detail distinguishes source facts, derived facts, contextual evidence,
  research-only evidence, and unavailable/unsupported fields; it shows sources,
  vintages, coverage, and limitations.
- Make missing information explicit. Sorting and filtering change presentation
  only, never family membership, confirmed Funding Plan membership, or arithmetic.
- Show no Funding Priority score, rank, expected flood-reduction benefit, or
  cohort-wide vulnerability score.

### P0-5 — Build and review the Session Reference Plan

The analyst can assemble and confirm a reproducible full-request plan under the
historical $125 million default envelope.

**Acceptance criteria:**

- Show Included in Plan and Available Projects, governed request amounts, included
  total, remaining envelope, and applied full-request/budget constraints.
- Let the analyst add or remove records from the documented 12-record family; do
  not imply that the system recommended, ranked, or optimized the combination.
- Reject unknown IDs and governed IDs outside the active analytical family unless
  a later governed methodology decision changes that family contract.
- Reject confirmation when the included total exceeds Available Budget and ensure
  the same budget/membership inputs reproduce the same arithmetic.
- Use full-request inclusion/exclusion only for ClimateCapital scenarios. Preserve
  published City treatment and amounts separately, even if they were partial or
  otherwise different, and never feed them into ClimateCapital analysis.

### P0-6 — Compare with the Historical City Recommendation

The analyst can use the published City Initial Recommendation as a descriptive
benchmark without treating it as ground truth.

**Acceptance criteria:**

- Preserve the published January 2026 City Initial Recommendation treatment and
  amounts.
- Show City portfolio allocation, number historically recommended or
  City-included, overlap with ClimateCapital, and meaningful divergences supported
  by the available data.
- Explain documented scenario and evidence differences only; do not speculate
  about City reasoning or characterize either result as right or wrong.
- Use City-specific terms such as “historically recommended,” “not historically
  recommended,” “City-included,” and “not City-included,” rather than borrowing
  ClimateCapital's selected/unselected labels.

### P0-7 — Run one governed What-If Scenario

The analyst can change permitted inputs and compare one active scenario with the
immutable Session Reference Plan.

**Acceptance criteria:**

- Retain one immutable Session Reference Plan and at most one active What-If
  Scenario; do not provide saved or multiple What-If scenarios.
- Provide directly editable structured controls for Available Budget and project
  inclusion/removal. These are the only P0 scenario inputs.
- Route manual changes and Gemini-translated explicit analyst commands through
  identical validation, deterministic recalculation, and rerun behavior.
- Require a clear confirmation before replacing an active What-If Scenario.
- Show before/after inputs and methodology-supported changes, including projects
  entering, leaving, or remaining in the plan; do not invent unsupported
  comparison metrics.

### P0-8 — Receive grounded explanations

The analyst can ask bounded questions about governed results without Gemini
becoming an analytical authority.

**Acceptance criteria:**

- Support explanations of project evidence roles, missingness, the analyst's
  confirmed membership, budget arithmetic, and approved scenario changes.
- Ground every answer in governed structured results and provenance, keep cited
  numbers consistent with deterministic output, and communicate uncertainty and
  limitations.
- Decline or bound unsupported requests, undocumented City reasoning, and broad
  analytical requests outside the governed product surface.

### P0-9 — Translate an explicit scenario command through the Gemini copilot

The analyst can express a specific permitted action in natural language while
retaining explicit control over execution.

**Acceptance criteria:**

- Interpret only explicit Available Budget changes or named project
  inclusion/removal commands and present one atomic proposal at a time. Gemini may
  not originate which projects should be funded.
- Show before/after values with confirm and cancel actions; change no state before
  confirmation.
- Gemini only interprets intent and structures the proposal. Confirmed changes use
  the same validation and deterministic scenario engine as manual controls.
- Gemini never authors facts, evidence roles, purpose classifications, request
  amounts, or recommendations. It may structure the analyst's explicit command;
  confirmed membership and arithmetic come from the deterministic scenario path.

### P0-10 — Accept a reviewed portfolio as the current-session draft

The analyst can designate the reviewed result they intend to carry forward without
creating a false persistence or approval workflow.

**Acceptance criteria:**

- Allow acceptance of either the reviewed Session Reference Plan or a confirmed
  active What-If portfolio.
- Treat acceptance as a current-session designation, not a new persisted scenario,
  snapshot, official recommendation, or approval.
- Preserve and identify the chosen scenario, budget, project membership, arithmetic
  outcomes, and explanation and show a draft/non-official disclaimer.
- If an accepted What-If is replaced, warn that its draft designation will be
  cleared; require the replacement to be reviewed and accepted separately.
- Exclude accounts, persistence, multiple snapshots, workflow, sharing, and export
  from P0.

### P0-11 — Inspect methodology and provenance

The analyst can trace how the product moves from source records to portfolio
results and understand the limits of those results.

**Acceptance criteria:**

- Document the complete chain: governed universe → derived purpose classification
  → P0 analytical family → evidence roles/missingness → analyst membership →
  budget validation/arithmetic → supported scenario comparison.
- Disclose sources and vintages, confidence meaning, limitations, and
  ClimateCapital's full-project inclusion/exclusion assumption.
- Define confidence as the strength of a documented classification, association,
  or source linkage, not need, severity, benefit, priority, or decision correctness.
- Use consistent provenance across screens and isolate the Historical City
  Recommendation from ClimateCapital's analytical pipeline.

### P0-12 — Provide an accessible and resilient analyst interface

The capital planning analyst can complete every required journey with clear
recovery when data or Gemini is unavailable.

**Acceptance criteria:**

- Design for the capital planning analyst as the sole P0 product persona, with a
  desktop-first experience that remains usable on a tablet.
- Support keyboard operation, visible focus, programmatic labels, sufficient
  contrast, and non-map equivalents for map interactions.
- Define loading, empty, invalid-input, missing-data, analytical-error, and Gemini-
  unavailable states with recovery guidance.
- Ensure Gemini failure never hides or invalidates deterministic results.
- Keep calendar, demo-duration, and zero-critical-defect criteria in the release
  gates rather than this user story.

## Conditional Stretch P0

### SP0-1 — Compare exactly two projects

The analyst may compare two candidates side by side only if required P0 and the
deadline contingency are intact.

**Acceptance criteria:**

- Select exactly two candidates from existing list or detail paths.
- Reuse existing Department Request, purpose, evidence roles, confidence,
  scenario status, provenance, and grounded explanations.
- Explain supported evidence or scenario-status differences and expose missing
  information.
- Exclude three-or-more comparison, custom metrics, saved sets, exports, and any
  separate analytical logic.

This is the first scope-cut candidate and is not release-blocking.

## P1, in Priority Order

1. Parks and Urban Heat as a separate, dated, constrained scenario.
2. Saved and multiple What-If scenarios.
3. Leadership-oriented export.
4. Full scenario comparison.
5. Broader grounded copilot intents.
6. Field-level audit depth and a full eligibility workspace.
7. Advanced spatial selection and custom-area analysis.

## Later

- Transportation as a separately constrained category.
- Multi-category caps and transfer rules.
- An explicitly hypothetical flexible citywide scenario.
- Partial funding only after project increments and benefits are verified.
- Dependencies, geographic coverage, and richer optimization objectives.
- Comparison of three or more projects and custom comparison metrics.
- Accounts, collaboration, formal approvals, sharing, and roles.
- Full mobile support.
- Outcome tracking or prediction only after suitable validation.

## Workflow Relationships

| Workflow step | Primary stories |
| --- | --- |
| Establish context and candidate set | P0-1, P0-2, P0-11 |
| Explore and inspect projects | P0-3, P0-4, P0-12 |
| Review the constrained portfolio | P0-5, P0-6 |
| Change and compare one scenario | P0-7, P0-9 |
| Explain and accept the reviewed result | P0-8, P0-10 |
| Optional exactly-two-project comparison | SP0-1 |

## Cross-Story Acceptance Boundaries

- Explore search, sort, and filters are presentation-only and never alter scenario
  inputs, confirmed membership, or budget arithmetic.
- The P0 analytical-family count and presentation-filter match count are always
  separate.
- Missing geometry does not remove a record from the P0 family or Funding Plan.
- Unsupported metrics are omitted. If an approved metric is missing for one
  project, the missingness is explicit and never interpreted as zero.
- Confidence labels follow the locked classification/association/source-linkage
  meaning and never become a need, severity, benefit, or priority signal.
- A family record may be Not Included in the Funding Plan; this status reflects
  analyst scenario membership and is not an eligibility, need, or City judgment.
- A valid zero-project plan, an over-budget/invalid attempted plan, and a genuine
  system error are different outcomes.
- Failed, invalid, or over-budget What-If attempts leave the prior confirmed
  scenario and last successful deterministic Funding Plan intact.
- Gemini failure never blocks deterministic evidence or results.
- Every project has a non-map path, and every required P0 flow has a non-Gemini
  path.

## Related Sources of Truth

- [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
- [Product plan](product-plan.md)
- [Screen and interaction specification](screen-spec.md)
- [Delivery and release gates](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
