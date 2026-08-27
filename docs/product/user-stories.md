# ClimateCapital AI User Stories

> **Status:** Approved and locked through Stage 3; constrained by the Stage 4
> Product and Design Lock
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
  Recommendation, ClimateCapital Historical Baseline Scenario, and analyst-created
  What-If Scenario by name and status.
- State that the historical Watershed allocation was $160 million and that the
  ClimateCapital baseline constrains eligible, individually named projects to the
  $125 million Projects sub-envelope.
- Label the experience as a historical simulation, not an official funding
  decision, prediction, or current ballot package.

### P0-2 — Derive and disclose the eligible candidate cohort

The analyst can understand which source records became ClimateCapital candidates
and why other records did not.

**Acceptance criteria:**

- Show eligible-candidate and excluded-source-record counts and an inspectable list
  of excluded records with documented reasons; do not imply every excluded record
  is a project.
- Apply documented eligibility rules reproducibly; do not force the cohort into
  the expected 15–30 range or manually select candidates for the demo.
- Score and optimize only eligible candidates, and never use the Historical City
  Recommendation as an eligibility or analytical input.
- Do not exclude an otherwise eligible candidate solely because display geometry
  is unavailable. Label it and keep it available through non-map paths.
- Defer the treatment of missing analytical evidence to the approved methodology.

### P0-3 — Explore candidates and defensible evidence on a map

The analyst can use geography to enter the decision journey without losing access
to candidates that cannot be mapped.

**Acceptance criteria:**

- Display defensible candidate geography plus supported flood and equity layers,
  with a legend and pan, zoom, and layer controls.
- Selecting mapped geography opens concise project and evidence detail.
- Never invent geometry. Keep candidates without display geometry available in
  Projects and Portfolio and label the limitation visibly.
- Provide a non-map path to every candidate and exclude drawing tools, custom GIS
  analysis, and unrelated map layers from P0.

### P0-4 — Inspect transparent project priorities

The analyst can examine the individual ranking and its evidence independently from
portfolio membership.

**Acceptance criteria:**

- Show Department Request, governed score and rank, portfolio status, evidence
  confidence, and supported flood and equity signals for each eligible candidate.
- Project detail distinguishes source fields from derived values; shows sources,
  vintages, limitations, relevant evidence inputs, and the approved score breakdown
  or contributions once the methodology is defined.
- Make missing information explicit. Sorting and filtering change presentation
  only, never scores, ranks, eligibility, or portfolio outcomes.
- Keep the Historical City Recommendation separate from the ClimateCapital ranking
  and do not pre-lock component scores or normalization in this story.

### P0-5 — Review the ClimateCapital Historical Baseline Scenario portfolio

The analyst can see the reproducible full-project portfolio produced under the
historical $125 million constraint.

**Acceptance criteria:**

- Show selected and unselected eligible candidates, Department Request amounts,
  total allocation, remaining envelope, and applied constraints.
- Identify the approved optimization objective or selection criterion once it has
  been defined; never exceed the active envelope.
- Explain why individual rank and constrained portfolio membership can differ and
  ensure the same inputs reproduce the same result.
- Use full-project inclusion/exclusion only for ClimateCapital scenarios. Preserve
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
- Explain ClimateCapital's analytical reasons only; do not speculate about City
  reasoning or characterize either result as right or wrong.
- Use City-specific terms such as “historically recommended,” “not historically
  recommended,” “City-included,” and “not City-included,” rather than borrowing
  ClimateCapital's selected/unselected labels.

### P0-7 — Run one governed What-If Scenario

The analyst can change permitted inputs and compare one active scenario with the
immutable baseline.

**Acceptance criteria:**

- Retain one immutable ClimateCapital Historical Baseline Scenario and at most one
  active What-If Scenario; do not provide saved or multiple What-If scenarios.
- Provide directly editable structured controls for budget and approved weights.
  These are the only P0 scenario inputs.
- Route manual and Gemini-originated changes through identical validation,
  deterministic recalculation, and rerun behavior.
- Require a clear confirmation before replacing an active What-If Scenario.
- Show before/after inputs and methodology-supported changes, including candidates
  entering, leaving, or remaining in the portfolio; do not invent unsupported
  comparison metrics.

### P0-8 — Receive grounded explanations

The analyst can ask bounded questions about governed results without Gemini
becoming an analytical authority.

**Acceptance criteria:**

- Support explanations of project evidence and score, rank differences,
  selection/exclusion, ranking versus constrained selection, and approved scenario
  changes.
- Ground every answer in governed structured results and provenance, keep cited
  numbers consistent with deterministic output, and communicate uncertainty and
  limitations.
- Decline or bound unsupported requests, undocumented City reasoning, and broad
  analytical requests outside the governed product surface.

### P0-9 — Propose a scenario change through the Gemini copilot

The analyst can express a permitted change in natural language while retaining
explicit control over execution.

**Acceptance criteria:**

- Interpret requests only for budget and approved weights and present one atomic
  proposal at a time. A proposal may coordinate multiple approved-weight changes
  when required to produce a valid weight configuration.
- Show before/after values with confirm and cancel actions; change no state before
  confirmation.
- Gemini only interprets intent and structures the proposal. Confirmed changes use
  the same validation and deterministic scenario engine as manual controls.
- Gemini never calculates or changes facts, scores, ranks, constraints, or
  portfolio membership. It may explain the governed result after recalculation.

### P0-10 — Accept a reviewed portfolio as the current-session draft

The analyst can designate the reviewed result they intend to carry forward without
creating a false persistence or approval workflow.

**Acceptance criteria:**

- Allow acceptance of either the reviewed ClimateCapital Historical Baseline
  Scenario portfolio or a confirmed active What-If portfolio.
- Treat acceptance as a current-session designation, not a new persisted scenario,
  snapshot, official recommendation, or approval.
- Preserve and identify the chosen scenario, budget, weights, outcomes, and
  explanation and show a draft/non-official disclaimer.
- If an accepted What-If is replaced, warn that its draft designation will be
  cleared; require the replacement to be reviewed and accepted separately.
- Exclude accounts, persistence, multiple snapshots, workflow, sharing, and export
  from P0.

### P0-11 — Inspect methodology and provenance

The analyst can trace how the product moves from source records to portfolio
results and understand the limits of those results.

**Acceptance criteria:**

- Document the complete chain: eligibility → evidence → transformations → scoring
  → ranking → constrained optimization.
- Disclose sources and vintages, confidence meaning, limitations, and
  ClimateCapital's full-project inclusion/exclusion assumption.
- Define confidence as evidence quality/completeness, not decision correctness.
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
- Reuse existing Department Request, methodology-defined score and rank, evidence,
  confidence, portfolio status, provenance, and grounded explanations.
- Explain supported ranking or portfolio-status differences and expose missing
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
  inputs, optimization, or Funding Plan membership.
- The eligible-cohort count and presentation-filter match count are always
  separate.
- Missing geometry is not, by itself, an eligibility failure.
- Unsupported metrics are omitted. If an approved metric is missing for one
  project, the missingness is explicit and never interpreted as zero.
- Low-confidence warnings come only from the later-approved confidence methodology
  and threshold.
- An eligible project may be Not Included in the Funding Plan; this status is
  distinct from ineligibility and from individual rank.
- A valid zero-project result, an infeasible optimization, and a genuine system
  error are different outcomes.
- Failed or infeasible What-If attempts leave the prior confirmed scenario and last
  successful deterministic Funding Plan intact.
- Gemini failure never blocks deterministic evidence or results.
- Every project has a non-map path, and every required P0 flow has a non-Gemini
  path.

## Related Sources of Truth

- [Product plan](product-plan.md)
- [Screen and interaction specification](screen-spec.md)
- [Delivery and release gates](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
