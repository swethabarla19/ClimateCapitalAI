# ClimateCapitalAI Project Progress

> This is the canonical handoff document for work across sessions. Read it before
> starting project work, keep the current-state sections accurate while working,
> and update the session log before ending a session.

## How to Maintain This File

At the start of every session:

1. Read this file completely.
2. Check the repository state and confirm that this snapshot is still accurate.
3. Begin with the first unblocked item in **Next Actions**, unless the user changes
   the priority.

At the end of every session:

1. Rewrite **Current Snapshot** so it describes the project now, not how it began.
2. Move finished work into **Completed Milestones**.
3. Update **Next Actions**, **Blockers**, **Risks**, and **Open Questions**.
4. Record durable choices in **Decision Log**.
5. Add a short, newest-first entry to **Session Log**, including files changed and
   verification performed.

Keep entries factual and concise. Do not mark work complete without evidence. Do
not remove historical decisions or session entries; mark superseded decisions as
superseded and link them to the replacement decision.

## Current Snapshot

- **Last updated:** 2026-08-26
- **Project stage:** Stage 4 Product and Design Lock approved and complete. Stages
  1–3 remain locked and authoritative.
- **Current focus:** Preserve the approved planning baseline through Stage 4, then
  begin technical execution-readiness planning as a separate, explicitly started
  work item without silently reopening product or UX scope.
- **Working state:** Documentation-only Git repository on `main`, connected to the
  public GitHub repository `swethabarla19/ClimateCapitalAI`; no application code or
  tooling exists yet. Approved planning is documented through the final Stage 4
  Product and Design Lock.
- **Most recent outcome:** Approved and locked the minimum screen inventory,
  navigation, screen-level requirements, contextual surfaces, important UI and
  recovery states, low-fidelity wireframes, and three-minute demo sequence.

## Project Definition

- **Vision:** ClimateCapital AI is a reusable public-sector decision-support product
  that turns fragmented project, climate, equity, cost, and geographic evidence
  into transparent draft capital-portfolio recommendations. The Austin Watershed
  historical simulation is its first pilot, not the permanent product boundary.
- **Primary user:** A representative City of Austin capital planning analyst, or
  equivalent cross-department planning analyst, who evaluates project requests and
  prepares recommendations but does not authorize funding. The user understands
  budgets, tables, filters, and maps but need not be a GIS, data-engineering, or AI
  specialist.
- **Problem being solved:** The analyst needs to reconcile fragmented project
  requests, place-based risk, equity need, cost, readiness, data quality, and
  uncertainty. Individual rankings do not answer which combination fits a
  constrained funding envelope, and the resulting tradeoffs are difficult to
  explain and defend.
- **Value proposition:** ClimateCapital AI helps the analyst create a defensible
  draft portfolio within a documented funding envelope. Place-based evidence and
  deterministic analysis establish the result; governed scenario controls and a
  bounded Gemini copilot help the analyst inspect, challenge, revise, and explain
  it without surrendering human decision authority.
- **Success measures:** Submit a deployed, tested, finalist-worthy P0 by the
  internal September 6 submission window; make the problem and planner value clear
  quickly; complete the core story in three minutes and expand it to five; visibly
  demonstrate credible analytics, transparent scoring and constraints, grounded
  Gemini value, uncertainty, and low-cost product discipline.
- **Audience assumption:** The initial submission is aimed at Google Cloud program
  and technical reviewers, followed by an industry-facing finale if selected. The
  official judge mix and rubric remain unconfirmed.
- **Demo target:** A three-minute core journey expandable to five minutes. A live
  demo is conditional on selection, and its date and format are not yet known.
- **Goals:** Submit a compelling Patchamomma MVP; demonstrate real analytics and
  data-engineering skill; keep Google Cloud spending very low; and finish a
  deployed, tested product before the deadline.
- **Historical decision context:** **January 21, 2026 Historical Decision
  Snapshot** is the dated context of the City of Austin 2026 Bond Initial Draft
  Project Recommendation, not an arbitrary product date or an analytical result.
  The historical Watershed allocation is $160 million, including a $125 million
  **Projects** allocation. P0 uses that $125 million Projects sub-envelope as the
  **ClimateCapital Historical Baseline Scenario** constraint for the rule-derived
  cohort of eligible, individually named Watershed project requests; the remaining
  Watershed allocations are outside the P0 portfolio and are not unallocated
  project funds.
- **Scenario terminology:** **Historical City Recommendation** means the published
  January 2026 City Initial Recommendation and is a descriptive benchmark only.
  **ClimateCapital Historical Baseline Scenario** means ClimateCapital's
  deterministic result under the documented January 2026 historical context, $125
  million constraint, and later-approved methodology. **Analyst-created What-If
  Scenario** means a confirmed run with a changed budget or approved weights.
- **In scope:** A rule-derived Watershed candidate cohort; Map → Projects →
  Portfolio; flood exposure and expected flood-reduction benefit as the primary
  recommendation signals; social vulnerability as a cross-cutting equity lens;
  transparent eligibility, evidence, ranking, constrained portfolio selection,
  uncertainty, source/vintage disclosure, scenario comparison, governed budget
  and weight changes, grounded explanations, and current-session draft acceptance.
- **Non-goals/out of scope:** Official funding decisions or predictions; the current ballot
  package; manually curated demo candidates; cross-department competition for an
  unrestricted pool; partial project funding; editing source data, project costs,
  eligibility, or constraints; permanent accounts or saved scenarios; formal
  approvals or report export; separate stakeholder workflows; authoritative AI
  scoring or portfolio selection; and urban heat as a P0 score input. Heat may
  appear only as defensible context or a clearly labeled project-specific
  co-benefit.
- **Analytical authority:** Documented deterministic analysis is authoritative for
  eligibility, evidence transformations, scoring, ranking, constraints, and
  portfolio outcomes. Gemini is a bounded interpretation and explanation layer and
  cannot calculate or change analytical facts or select the portfolio.
- **Core demo journey:** Map → Projects → Portfolio → governed scenario change →
  grounded explanation → current-session draft acceptance. Individual ranking and
  constrained portfolio selection remain visibly separate.

## Approved Deadline Plan

- **Official deadline:** September 7, 2026 at 10:00 a.m. CDT.
- **Internal submission window:** September 6, 2026 from 9:30–11:30 a.m. CDT.
- **Planning capacity:** Approximately 65–70 hours across six flexible workdays per
  week; stretching beyond that is contingency, not the base plan.
- **Scope rule:** Protect testing and submission contingency. A missed gate freezes
  or cuts scope; it does not consume the testing buffer.
- **P1 rule:** No P1 work before submission unless every required P0 story is
  complete at least 24 hours early and at least 10 hours of contingency remain.

| Date | Planned hours | Milestone or focus |
| --- | ---: | --- |
| Aug 25 | 3 | Deadline-plan reset and scope rules |
| Aug 26 | 8 | Lock Stage 3 backlog; check submission requirements by noon |
| Aug 27 | 8 | Complete Product and Design Lock |
| Aug 28 | 6 | Technical execution-readiness in a separate implementation-planning chat |
| Aug 29 | 7 | Evidence readiness: sources, cohort, scoring, confidence, and vintages |
| Aug 30 | — | Recovery day; use only if an earlier gate slips |
| Aug 31 | 7 | Analytics core |
| Sep 1–2 | 14 | Integrate required P0 and freeze features by Sep 2 evening |
| Sep 3 | 5 | Produce deployed release candidate |
| Sep 4 | 4 | QA and demo gate |
| Sep 5 | 3 | Final freeze and submission package |
| Sep 6 | 2 | Submit during the internal window and verify final links |

### Release and Demo Gates

These gates are release-level criteria and are intentionally separate from the
user-story acceptance criteria below.

- **September 2 — Feature freeze:** Every required P0 story is integrated. Stretch
  P0 remains optional, and no new behavior begins after this gate.
- **September 3 — Release candidate:** A public deployment completes the required
  P0 journey end to end.
- **September 4 — Quality gate:** There are zero known critical defects;
  accessibility and resilience checks pass; and every displayed or Gemini-cited
  number agrees with the deterministic outputs.
- **September 4 — Demo gate:** The Map → Projects → Portfolio → governed change →
  explanation journey fits a three-minute core demo and expands coherently to five
  minutes.
- **September 5 — Final freeze:** Submission content and artifacts are complete;
  only submission-blocking fixes remain permissible.
- **September 6 — Submission gate:** Submit between 9:30 and 11:30 a.m. CDT and
  verify every final link, leaving at least 22.5 hours for recovery.

## Locked Stage 3 Backlog

Stage 3 was approved and locked on 2026-08-26. Required P0 stories are
release-blocking. The single stretch P0 story is conditional and the first scope
cut. P1 and Later items cannot displace required P0 work.

### Required P0

#### P0-1 — Establish the historical context and scenario terminology

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

#### P0-2 — Derive and disclose the eligible candidate cohort

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

#### P0-3 — Explore candidates and defensible evidence on a map

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

#### P0-4 — Inspect transparent project priorities

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

#### P0-5 — Review the ClimateCapital Historical Baseline Scenario portfolio

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

#### P0-6 — Compare with the Historical City Recommendation

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

#### P0-7 — Run one governed What-If Scenario

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

#### P0-8 — Receive grounded explanations

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

#### P0-9 — Propose a scenario change through the Gemini copilot

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

#### P0-10 — Accept a reviewed portfolio as the current-session draft

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

#### P0-11 — Inspect methodology and provenance

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

#### P0-12 — Provide an accessible and resilient analyst interface

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

### Conditional Stretch P0

#### SP0-1 — Compare exactly two projects

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

### P1, in priority order

1. Parks and Urban Heat as a separate, dated, constrained scenario.
2. Saved and multiple What-If scenarios.
3. Leadership-oriented export.
4. Full scenario comparison.
5. Broader grounded copilot intents.
6. Field-level audit depth and a full eligibility workspace.
7. Advanced spatial selection and custom-area analysis.

### Later

- Transportation as a separately constrained category.
- Multi-category caps and transfer rules.
- An explicitly hypothetical flexible citywide scenario.
- Partial funding only after project increments and benefits are verified.
- Dependencies, geographic coverage, and richer optimization objectives.
- Comparison of three or more projects and custom comparison metrics.
- Accounts, collaboration, formal approvals, sharing, and roles.
- Full mobile support.
- Outcome tracking or prediction only after suitable validation.

## Locked Stage 4 Product and Design Lock

Stage 4 was approved and locked on 2026-08-26. This is the final Product and
Design Lock for P0. It defines the minimum coherent analyst experience without
changing the locked Stage 1–3 product, backlog, analytical, evidence, or release
decisions. Evidence-dependent content remains unresolved until the evidence stage.

Every project name, count, dollar amount, date, rank, benchmark value, and outcome
inside the low-fidelity wireframes below is an illustrative placeholder. These
examples are not source evidence, implementation constants, or later analytical
decisions.

### Experience and Information Architecture

- Use a desktop-first, tablet-usable application shell with a narrow primary
  sidebar: **Explore**, **Funding Plan**, **Data & Methodology**, and **Help &
  Resources**.
- Keep **Compare** conditional SP0-1. It is reached from existing project list or
  detail paths only if the stretch story survives the release gates; it is not a
  required primary destination.
- Use the global context header to show **Decision: [current decision context]**,
  **Scenario: [current confirmed scenario]**, and **Available Budget: [amount]**.
  The current confirmed scenario may be the supported baseline/default result or
  the active confirmed What-If. Do not label the Historical Benchmark as a
  scenario or confuse either with the immutable Historical Baseline reference.
- Preserve Explore state—map extent, active presentation filters, visible layers,
  selected project, and scroll position—when opening and closing Project Detail or
  navigating to a linked methodology section.
- Search, sorting, and filters on Explore affect only visible map/list results.
  They never change eligibility, scores, ranks, scenario inputs, optimization, or
  Funding Plan membership.
- Use progressive disclosure. The Layers popover is closed by default, Project
  Detail stays hidden until inspection, and Scenario Settings stays hidden until
  **Adjust Scenario** is invoked. Closing the Layers control does not imply that
  all analytical layers are off; the approved default visualization may remain
  active, and its final evidence-backed layer configuration is not a Stage 4
  decision.
- Keep full Funding Plan, scenario editing, Historical Benchmark, Reviewed Draft,
  and permanently open Project Detail content out of Explore.

**Primary navigation flow:** Begin in Explore; inspect a Recommended Projects row
directly in the shared Project Detail panel or use marker preview → Project Detail;
close detail without losing Explore state; use **View Funding Plan** to enter the
dedicated Funding Plan workspace; invoke Scenario Settings, Historical Benchmark,
Reviewed Draft confirmation, or compact Gemini from that workspace; and use
anchored links to Data & Methodology or the primary sidebar without changing the
confirmed scenario. Help & Resources remains independently available from the
sidebar. The three-minute demo follows this flow but does not remove direct access
to any primary destination.

### Required Screens

| Screen | Required P0 content and behavior |
| --- | --- |
| **Explore** | A large immersive map synchronized with a compact **Recommended Projects** list; the current decision/scenario context and Available Budget; compact approved summary metrics; search and presentation-only filters; a click/tap Layers control and legend; distinct matching and eligible-total counts; a slim current Funding Plan status with **View Funding Plan**; and a small proactive, grounded Gemini insight about the current extent, active filters/layers, and visible projects. |
| **Funding Plan** | The full deterministic recommendation in grouped **Recommended** and **Not Included** sections; budget used, Available Budget, remainder, project counts, active constraints, and the later-approved objective; baseline-supported deltas for a confirmed What-If; **Adjust Scenario**; a secondary Historical Benchmark entry; compact on-demand Gemini explanation; and **Mark as Reviewed Draft** with current-session status. Individual Funding Priority remains separate from plan membership. |
| **Data & Methodology** | One anchored, scannable page covering decision context and terminology; eligibility rules, eligible-candidate and excluded-source-record counts, excluded records and reasons; evidence sources and vintages; source versus derived fields; the later-approved transformations, scoring, ranking, confidence, and optimization method; the full-project assumption; missing-data treatment; limitations; and the strict separation of the Historical City Recommendation from ClimateCapital analysis. |
| **Help & Resources** | A compact quick guide to the four decision contexts/results, how to use Explore and Funding Plan, what Gemini can and cannot do, how to interpret confidence and missingness once approved, accessibility/help guidance, and the historical-simulation/non-official disclaimer. Link to Data & Methodology for detailed provenance. |
| **Compare — conditional SP0-1** | If retained, compare exactly two projects using existing governed fields, evidence, confidence, status, provenance, and bounded explanation. Do not introduce new calculations, custom metrics, saved comparisons, or comparison of three or more projects. |

### Required Contextual Surfaces

- **Layers popover:** Opens on click/tap, not hover. It lists only supported layers,
  mirrors the current map visualization state, provides a legend or legend access,
  and closes without resetting selections. Stage 4 does not decide which
  evidence-backed layers are active by default.
- **Map-marker preview:** A lightweight preview appears only after a map marker is
  selected. It shows the project name, Department Request, supported concise
  status/evidence, and **View Project Details**. It does not duplicate the full
  detail panel.
- **Project Detail:** A shared panel used by all project-inspection paths. A
  Recommended Projects row opens it directly; a map marker reaches it through the
  preview. It shows source versus derived values, Department Request, Funding
  Priority/rank, Funding Plan status, and supported Importance, Climate Risk,
  Community Vulnerability, and Community Equity measures; it also shows
  methodology-driven confidence, sources/vintages, limitations, missingness, and
  bounded Gemini actions. Both entry paths preserve Explore state. Any of these
  measures appears only when its underlying metric is approved.
- **Explore Gemini insight:** Compact and proactively visible because spatial
  interpretation is central to Explore. It is grounded only in current map extent,
  active filters/layers, and visible governed project results. Expansion stays in
  the same contextual region and never hides deterministic map/list content.
- **Scenario Settings:** A Funding Plan drawer opened by **Adjust Scenario**. It
  edits only Available Budget and later-approved weights, shows current versus
  proposed values and validation, and requires explicit recalculation/confirmation
  before replacing the active What-If. Unapplied edits never change the visible
  current result.
- **Gemini scenario proposal:** P0-9 remains approved. One atomic, structured
  proposal may change only budget and approved weights; it shows before/after
  values and confirm/cancel actions. Confirmation routes through the same
  validation and deterministic recalculation as manual controls. Gemini does not
  edit Scenario Settings or analytical outcomes directly.
- **Historical Benchmark:** A secondary Funding Plan view of the published January
  2026 Historical City Recommendation. It uses City-specific inclusion terms,
  preserves published amounts/treatment, shows supported overlap and divergence,
  and never serves as a scenario input, target, score, or ground truth.
- **Reviewed Draft confirmation:** An in-place confirmation dialog identifies the
  current confirmed scenario, budget, weights, and supported outcomes; explains
  that the designation is current-session, draft, and non-official; and offers
  cancel/confirm. It does not create a saved scenario, approval, export, or
  persistence workflow.
- **Funding Plan Gemini:** Compact by default and expanded only on analyst request.
  It can explain governed project, ranking, membership, constraint, and scenario
  results but cannot block or replace deterministic results.

### Important UI State and Recovery Model

Use explicit state categories and local recovery. Never collapse the following
conditions into a generic “no results” message.

| Context | Required states and recovery behavior |
| --- | --- |
| **Explore counts and filters** | Always distinguish the rule-derived eligible cohort from the presentation-filter match count. With active filters, use wording such as **[matching count] matching · [eligible total] eligible total**. No filter matches keeps the eligible-total count, map/list frame, and active filters visible and offers **Clear filters**; it does not imply an empty eligible cohort. |
| **No eligible projects** | State that documented eligibility produced no eligible candidates, suppress ranking and Funding Plan claims, and link to the eligibility audit in Data & Methodology. Do not present this as a filter result or system failure. |
| **Missing project geometry** | Keep an otherwise eligible project in the list, ranking, Project Detail, and Funding Plan; label **Map location unavailable** and provide the non-map inspection path. Never invent a marker or exclude the project solely for display geometry. |
| **Approved-field missingness** | If an approved metric is unavailable for one project, show explicit project-level missingness and the methodology-defined effect. Never display or interpret missing as zero, and Gemini must respect the same limitation. If a metric itself lacks evidence approval, omit it rather than showing a missing placeholder. |
| **Eligible but not in plan** | Show **Eligible · Not Included in Funding Plan** separately from rank and explain only the supported deterministic constraint/selection reason. Do not imply ineligibility, low importance, or a City decision. |
| **Valid zero-project plan** | If the deterministic method validly selects no projects under confirmed inputs, show a successful zero-project Funding Plan with the applicable constraint explanation. Distinguish this valid outcome from infeasibility and system failure. |
| **No feasible optimized Funding Plan** | Show a dedicated analytical-infeasibility state with the relevant validated constraint explanation and a path back to Scenario Settings. Preserve the last successful deterministic Funding Plan and label the attempted inputs as not applied. If no prior result exists, show the dedicated unavailable plan state without fabricating membership. |
| **Genuine system error** | Name the affected surface, preserve unaffected deterministic content, provide retry guidance, and avoid implying an analytical result. A map/list error, detail error, benchmark error, or methodology-section error is contained locally where possible. |
| **Project Detail** | Support closed, loading, loaded, approved-field-missing, geometry-missing, locally unavailable, and retry states. Closing or retrying never resets Explore state. A row opens the panel directly; only a marker uses the preview first. |
| **Funding Plan** | Support initial loading, successful baseline/default result, successful confirmed What-If, valid zero-project result, analytical infeasibility, locally unavailable/system error, and current-session Reviewed Draft indicators. Recommended and Not Included remain separately grouped in successful states. |
| **Scenario Settings** | Support pristine, dirty/unapplied, invalid, ready to recalculate, recalculating, replacement confirmation, success, infeasible, and system-failure states. Dirty values do not change header context or the visible Funding Plan. On failure or infeasibility, retain attempted values for correction but label them not applied; preserve the previous confirmed scenario and last successful result. |
| **Historical Benchmark** | Support closed, loading, available, partially supported/missing published fields, unavailable, and retry states. Missing benchmark data never changes ClimateCapital outputs, and City reasoning is never inferred. |
| **Reviewed Draft** | Support not reviewed, confirmation open, marked for the current session, and cleared states. The designation binds to the exact confirmed result. Unapplied edits do not clear it; confirmation of a replacement What-If warns and clears an accepted What-If designation, after which the new result requires separate review. A failed recalculation leaves the existing designation intact because the confirmed result did not change. |
| **Gemini explanation** | Support compact/idle, expanded, loading, grounded answer, bounded refusal, unavailable, and retry states. Failure or refusal never hides project evidence, methodology, or Funding Plan results. No required action depends on Gemini. |
| **Gemini proposal** | Support proposal-ready, validation error, confirmation pending, cancelled, recalculating through the deterministic path, applied, infeasible, and failed. Nothing changes before confirmation; failed or infeasible proposals remain unapplied and preserve the last successful result. |
| **Data & Methodology** | Support the complete page, anchored deep-link focus, locally loading section, approved-field/source missingness, locally unavailable section, and retry states. A failed linked section does not remove the rest of the methodology or reset the originating screen. |
| **Help & Resources** | Provide readable content without Gemini. If a deep link is unavailable, keep the guide usable and offer a retry or route to the Data & Methodology landing page. |

Low-confidence warnings appear only when the later-locked confidence methodology
and threshold require them. Stage 4 introduces no UI-specific confidence judgment.

### Low-Fidelity Wireframes

The wireframes establish hierarchy and behavior, not visual styling or data
values.

#### Explore

```text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ ClimateCapital│ Decision: [decision context]                                 │
│              │ Scenario: [current confirmed scenario]                        │
│ Explore      │ Available Budget: [amount]                                    │
│ Funding Plan ├───────────────────────────────────────────────────────────────┤
│ Data & Method│ [approved summary] [approved summary] [plan status]            │
│ Help         │ [Search] [Presentation filters] [Layers]                       │
│              ├───────────────────────────────┬───────────────────────────────┤
│              │                               │ Recommended Projects          │
│              │        IMMERSIVE MAP          │ [count] matching · [count]    │
│              │        + legend               │ eligible total                │
│              │                               │ [project row]                 │
│              │                               │ [project row]                 │
│              ├───────────────────────────────┴───────────────────────────────┤
│              │ Funding Plan: [count] recommended · [budget use] [View Plan]  │
│              │ Gemini insight: [grounded observation] [Expand]               │
└──────────────┴───────────────────────────────────────────────────────────────┘
```

#### Layers popover

```text
[Layers ▾]
┌──────────────────────────────┐
│ Map layers                   │
│ [current supported layer]    │
│ [current supported layer]    │
│ [Legend / layer explanation] │
└──────────────────────────────┘
```

The control is closed by default. Checked/active states mirror the separately
approved default map visualization; Stage 4 does not force all overlays off.

#### Map-marker preview and Project Detail

```text
Marker click → ┌──────────────────────────┐
               │ [Project name]           │
               │ Request: [amount]        │
               │ [supported brief status] │
               │ [View Project Details]   │
               └──────────────────────────┘

Row click ───────────────────────────────┐
Marker preview → View Project Details ───┤
                                        ▼
                         ┌─────────────────────────────────┐
                         │ Project Detail              [×] │
                         │ [source and derived values]     │
                         │ Funding Priority: [rank/score]  │
                         │ Funding Plan: [status]          │
                         │ [supported evidence/confidence] │
                         │ [missingness and limitations]   │
                         │ [sources and vintages]          │
                         │ [bounded Gemini action]         │
                         └─────────────────────────────────┘
```

#### Explore Gemini insight

```text
Compact:  ┌───────────────────────────────────────────────┐
          │ What stands out here: [grounded insight]       │
          │ [Expand]                                       │
          └───────────────────────────────────────────────┘

Expanded: ┌───────────────────────────────────────────────┐
          │ Based on [extent / filters / layers / projects]│
          │ [grounded explanation + limitations]           │
          │ [Collapse]                                     │
          └───────────────────────────────────────────────┘
```

#### Funding Plan and Scenario Settings

```text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Navigation   │ Funding Plan · [current confirmed scenario]                  │
│              │ [budget used] [Available Budget] [remainder] [project count] │
│              │ [Adjust Scenario] [Historical Benchmark] [Mark Reviewed Draft]│
│              ├──────────────────────────────┬────────────────────────────────┤
│              │ Recommended                 │ Not Included                   │
│              │ [project / request / rank]  │ [project / request / rank]     │
│              │ [project / request / rank]  │ [supported reason/status]      │
│              ├──────────────────────────────┴────────────────────────────────┤
│              │ [constraints/objective] [baseline-supported deltas]          │
│              │ Gemini explanation [Ask / Expand]                            │
└──────────────┴───────────────────────────────────────────────────────────────┘

Adjust Scenario → ┌─────────────────────────────────────────┐
                  │ Scenario Settings                   [×] │
                  │ Available Budget [current → proposed]   │
                  │ Approved weights [current → proposed]   │
                  │ [validation / unapplied status]         │
                  │ [Cancel] [Recalculate and Confirm]      │
                  └─────────────────────────────────────────┘
```

#### Reviewed Draft confirmation

```text
┌─────────────────────────────────────────────────────┐
│ Mark this result as the Reviewed Draft?             │
│ Scenario: [current confirmed scenario]              │
│ Budget / weights / outcomes: [governed summary]     │
│ Current-session only · Draft · Not an official plan │
│                              [Cancel] [Mark Draft]   │
└─────────────────────────────────────────────────────┘
```

#### Historical Benchmark

```text
┌───────────────────────────────────────────────────────────────┐
│ Historical City Recommendation · [published benchmark date]   │
│ Descriptive benchmark only · Not a ClimateCapital scenario    │
│ [City allocation] [City-included count] [supported overlap]    │
│ City-included            │ Not City-included                   │
│ [published treatment]    │ [published treatment]               │
│ [supported divergence; no inferred City reasoning]             │
└───────────────────────────────────────────────────────────────┘
```

#### Data & Methodology

```text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Page anchors │ Data & Methodology                                            │
│ Context      │ [decision/scenario/benchmark terminology]                     │
│ Eligibility  │ [rules] [eligible count] [excluded-record count + reasons]    │
│ Evidence     │ [sources/vintages] [source vs derived] [missingness]           │
│ Scoring      │ [approved transformations/weights/ranking/confidence]          │
│ Portfolio    │ [constraint/objective/full-project assumption]                │
│ Limitations  │ [limits and City benchmark isolation]                         │
└──────────────┴───────────────────────────────────────────────────────────────┘
```

#### Help & Resources

```text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Navigation   │ Help & Resources                                              │
│              │ [Decision-context and scenario quick guide]                   │
│              │ [How to Explore] [How to review a Funding Plan]               │
│              │ [What Gemini can/cannot do] [Confidence/missingness guide]     │
│              │ [Accessibility/help] [Historical simulation disclaimer]       │
│              │ [Open Data & Methodology]                                     │
└──────────────┴───────────────────────────────────────────────────────────────┘
```

#### Compare — conditional SP0-1

```text
┌───────────────────────────────────────────────────────────────┐
│ Compare exactly two projects                                  │
│ [Project A]                       │ [Project B]                │
│ [existing governed fields]        │ [existing governed fields]│
│ [evidence/confidence/missingness]  │ [evidence/confidence]     │
│ [bounded supported explanation]                                │
└───────────────────────────────────────────────────────────────┘
```

### Locked Demo Sequence

The core demo must fit three minutes and follow the approved journey:

1. **Orient:** Establish the January 2026 historical decision context, current
   confirmed scenario, Available Budget, and historical-simulation disclaimer.
2. **Explore:** Use the map and synchronized Recommended Projects list to reveal a
   defensible flood/equity pattern and the proactive grounded spatial insight.
3. **Inspect:** Open one Project Detail from a row or marker path and show source
   evidence, Funding Priority, confidence/missingness, and Funding Plan status.
4. **Review the Funding Plan:** Move to the dedicated workspace and show the
   deterministic full-project recommendation, budget constraint, and why ranking
   differs from constrained membership.
5. **Run one governed What-If:** Adjust only budget or approved weights, confirm
   deterministic recalculation, and show supported deltas from the immutable
   Historical Baseline.
6. **Explain and finish:** Invoke a grounded Gemini explanation, then mark the
   reviewed result as the current-session Reviewed Draft with the non-official
   disclaimer.

A five-minute expansion may add the Historical Benchmark, deeper methodology and
provenance, a second project, failure recovery, or Compare only if conditional
SP0-1 survives. The Historical Benchmark is not required to interrupt the
three-minute core sequence.

### Stage 4 Assumptions, Dependencies, and Risks

**Assumptions:**

- P0 serves one capital planning analyst persona in a desktop-first experience.
- One immutable Historical Baseline and at most one confirmed active What-If are
  sufficient; the Reviewed Draft designation lasts only for the current session.
- Deterministic evidence and results remain usable without Gemini.
- Full-project inclusion/exclusion and presentation-only Explore controls remain
  P0 constraints.

**Dependencies and unresolved evidence decisions:**

- The evidence stage must approve scoring dimensions, transformations, default and
  editable weights, confidence methodology and warning threshold, optimization
  objective, missing-evidence treatment, source vintages, final cohort, defensible
  geometry, and supported portfolio metrics.
- **People Potentially Benefiting** and **Implementation Readiness** appear only if
  evidence decisions approve the underlying measures. If unsupported, omit them;
  if approved but missing for one project, show explicit missingness.
- Community Vulnerability and Community Equity remain distinct wherever they
  represent different approved underlying measures.
- The evidence stage, not Stage 4, determines the approved default analytical map
  visualization/layers and any project-specific heat co-benefit treatment.
- Official judging criteria, submission artifacts, and conditional demo details
  still require verification.

**Product and deadline risks:**

- The required P0 is broad for the release window; conditional Compare remains the
  first cut and no P1 work may displace required P0.
- Dense evidence, scenario, and state information could overwhelm the three-minute
  story; the locked hierarchy and progressive disclosure must be preserved.
- Conflating the current confirmed scenario, immutable Historical Baseline, or
  Historical Benchmark would undermine analytical trust.
- Unsupported metrics, UI-invented confidence warnings, or missing-as-zero
  treatment would create misleading results.
- Failed recalculation or Gemini behavior could appear to overwrite authoritative
  results unless the last-successful-result and unapplied-input rules are enforced.
- Missing geometry may weaken the map demonstration, so synchronized non-map paths
  and visible limitations are release-critical.

## Current Workstream

- **Goal:** Carry the approved Product and Design Lock into a separate technical
  execution-readiness stage while protecting the September 7 MVP scope and gates.
- **Status:** Stages 1–4 are approved and locked. The Product and Design Lock is
  complete, and no application implementation, architecture, data, analytics,
  Gemini, cloud, dependency, or later-stage work has started.
- **Owner:** User and Codex.
- **Relevant files:** `PROJECT_PROGRESS.md`, `AGENTS.md`, `README.md`
- **Acceptance criteria:** The next separately approved plan must treat all Stage
  1–4 locks, unresolved evidence gates, and release constraints as authoritative
  and must not silently expand the required P0.

## Next Actions

1. Begin technical execution-readiness planning as a separate, explicitly
   authorized work item; do not implement application functionality merely because
   the Product and Design Lock is complete.
2. Verify organizer submission artifacts, judging criteria, and conditional live-
   demo details.
3. Resolve evidence-readiness decisions by August 29: governed scoring dimensions,
   default weights, confidence methodology, rule-derived cohort, source vintages,
   supported portfolio metrics, and the heat co-benefit evidence threshold.
4. Reconcile the technical plan and evidence decisions with the September 2
   feature-freeze gate before beginning integrated feature work.
5. Update this tracker and create an approved Git checkpoint after each newly
   locked planning stage.

## Completed Milestones

- **2026-08-26 — Stage 4 Product and Design Lock approved and complete:** Locked
  the minimum screen inventory, information architecture, contextual surfaces,
  screen requirements, important state/recovery model, low-fidelity wireframes,
  demo sequence, and UX assumptions, dependencies, and risks. Compare remains
  conditional SP0-1, and evidence-dependent content remains unresolved.
- **2026-08-26 — Stage 3 backlog approved and locked:** Prioritized 12 required P0
  stories, one conditional stretch P0 story, P1, and Later work; defined testable
  acceptance criteria, scenario-state rules, terminology, scope boundaries, and
  release gates.
- **2026-08-25 — Deadline plan approved:** Allocated approximately 67 hours through
  the September 6 internal submission window, set an August 27 Product and Design
  Lock, placed analytics risk before integration, set a September 2 feature freeze,
  and protected testing and contingency from scope expansion.
- **2026-08-25 — Documentation checkpoint published to GitHub:** Connected the
  public `swethabarla19/ClimateCapitalAI` repository, preserved its initial README,
  and published the Stage 1 and locked Stage 2 history on `main`.
- **2026-08-25 — Stage 1 and Stage 2 Git checkpoint created:** Captured the
  repository guidance and canonical product handoff in the initial local commit
  before beginning Stage 3.
- **2026-08-25 — Stage 2 product definition locked:** Defined the primary user,
  problem, value proposition, January 2026 Historical Baseline decision context,
  scenario terminology, goals, non-goals, assumptions, and core Map → Projects →
  Portfolio journey. These decisions constrain later planning unless material
  source evidence contradicts them.
- **2026-08-24 — Stage 1 deadline and success baseline approved:** Set the official
  September 7 deadline, September 6 internal submission window, 40-hour weekly
  planning capacity, judge-facing audience assumption, three-minute core demo, and
  finalist-worthy deployed P0 success bar.
- **2026-08-24 — Cross-session continuity initialized:** Added a canonical project
  progress document and repository instructions for maintaining it.

## Blockers

- No blocker remains in Stage 4 product or UX definition.
- Evidence-stage decisions block implementation of analytical claims, governed
  metrics, weights, confidence warnings, and default evidence visualizations.
- Official judging criteria, submission artifact requirements, and conditional
  live-demo details remain unconfirmed and block final submission-package planning,
  but not technical execution-readiness planning.

## Risks and Watch Items

- The 12-story required P0 scope is ambitious for the September 2 feature freeze;
  the conditional two-project comparison must be cut first and no P1 work may
  displace required P0.
- The final rule-derived candidate count and evidence coverage may differ from the
  expected 15–30 range; the demo must not drive cohort selection.
- Scoring criteria, default weights, and confidence treatment remain intentionally
  unresolved and could become a trust risk if rushed or presented as arbitrary.
- The Historical Decision Snapshot, Historical City Recommendation, current
  confirmed scenario, and immutable Historical Baseline reference may be confused
  unless the locked names, status, dates, header, and change provenance are applied
  consistently.
- A map-first journey could resemble a generic dashboard unless it reaches the
  constrained portfolio decision quickly.
- Dense screen content could overwhelm the three-minute demo unless progressive
  disclosure and the dedicated Funding Plan workspace are preserved.
- Natural-language propose → review → confirm interactions add meaningful P0 scope
  and must not obscure which inputs changed or who authorized the rerun.
- Eligible candidates without defensible display geometry will weaken the map-first
  presentation; the non-map journey and visible limitation labels are required.
- Gemini proposal and explanation flows could consume disproportionate effort;
  deterministic results and manual scenario controls must remain complete and
  usable if Gemini is unavailable.
- Missing source or methodology support may restrict portfolio comparison metrics;
  P0 must not invent benefits, impacts, or optimization claims for demo appeal.
- Recalculation failures could mislead analysts unless unapplied inputs remain
  visibly separate and the last successful deterministic result is preserved.
- Generic empty/error handling could conflate zero filter matches, no eligible
  cohort, valid zero-project results, analytical infeasibility, and system errors.
- Heat context or co-benefit claims could overstate the evidence unless the team
  defines a clear inclusion threshold and labels them separately from core scores.
- Historical source context and external evidence vintages could be conflated if
  January 21 is incorrectly applied as a blanket dataset-date requirement.
- The `codex-process-jobs` Stop hook currently exits with code 127 because `node`
  is unavailable. This did not affect the documentation checkpoint, but process-job
  completion checks remain unreliable until the runtime or hook configuration is
  fixed.

## Open Questions

- There are no unresolved Stage 4 screen, navigation, state, wireframe, or demo-
  sequence decisions.
- Which governed scoring dimensions, transformations, approved score breakdown,
  optimization objective, and default weights should P0 use?
- How should missing analytical evidence, uncertainty, and confidence affect
  eligibility, scoring, ranking, and presentation?
- What is the final eligible project count after documented rules are applied?
- Which evidence vintages and defensible project geographies are available for the
  rule-derived cohort?
- Which portfolio comparison measures beyond cost, count, overlap, and membership
  changes are supported by the approved methodology and evidence?
- What evidence is sufficient to label a watershed project with an urban-heat
  co-benefit?
- Are People Potentially Benefiting and Implementation Readiness supported well
  enough to approve as product metrics, and how should project-level missingness be
  represented if they are approved?
- Which supported analytical layers, if any, should be visible in the default
  Explore map state?
- What are the official submission artifacts, judging criteria, finale date, and
  live-demo format?

## Technical Map

### Architecture

Not established.

### Repository Structure

- `AGENTS.md` — persistent instructions for agents working in this repository.
- `PROJECT_PROGRESS.md` — canonical current state and cross-session handoff.
- `README.md` — concise repository landing page that points to the canonical
  planning and handoff document.
- Local Git branch: `main`.
- GitHub remote: `origin` → `https://github.com/swethabarla19/ClimateCapitalAI.git`
  (public).

### Environments and External Services

- Public GitHub repository: `https://github.com/swethabarla19/ClimateCapitalAI`.
- Local environment issue: `node` is unavailable, so the `codex-process-jobs`
  Stop hook cannot execute its JavaScript helper.

### Common Commands

- `git status --short --branch` — verify working-tree and upstream status.
- `git log --oneline --decorate --max-count=8` — inspect recent checkpoints.
- `git push origin main` — publish an approved local checkpoint.
- Add setup, development, test, lint, build, migration, and deploy commands when
  application tooling is introduced and verified.

## Decision Log

| ID | Date | Decision | Reason | Status |
| --- | --- | --- | --- | --- |
| D-001 | 2026-08-24 | Use `PROJECT_PROGRESS.md` as the canonical cross-session handoff. | A single maintained source of truth reduces context loss between sessions. | Active |
| D-002 | 2026-08-24 | Keep a current-state summary plus an append-only session history. | Future sessions need both a fast restart point and traceability. | Active |
| D-003 | 2026-08-24 | Use Map → projects → portfolio as the primary P0 journey. | The product should begin interactively, collect user inputs, and then recommend a portfolio from eligible projects. | Active |
| D-004 | 2026-08-24 | Limit P0 to watershed projects; treat parks as a candidate P1 project type. | This keeps the first release focused while leaving room for category expansion. | Active |
| D-005 | 2026-08-24 | Lead P0 with flood evidence and social vulnerability; show urban heat only as context or a labeled co-benefit where defensible. | This keeps the watershed pilot coherent and evidence-based while preserving a credible multi-hazard expansion story. | Active |
| D-006 | 2026-08-25 | Treat September 7, 2026 at 10:00 a.m. CDT as the official submission deadline and September 6, 9:30–11:30 a.m. CDT as the internal submit window. | The earlier internal window provides 22.5 hours for submission recovery. | Active |
| D-007 | 2026-08-25 | Plan against 40 hours per week and a finalist-worthy, deployed, tested P0 with a three-minute core demo expandable to five. | Scope must prioritize completion and clarity over feature count. | Active |
| D-008 | 2026-08-25 | Define the primary user as a representative capital planning analyst who recommends but does not authorize funding. | This persona credibly needs maps, comparison, constrained portfolios, transparent evidence, and plain-language explanations. | Active |
| D-009 | 2026-08-25 | Use January 21, 2026 as the historical decision snapshot because it corresponds to Austin's 2026 Bond Initial Draft Project Recommendation. | The date establishes the decision context and is not an arbitrary product date. | Active |
| D-010 | 2026-08-25 | Use the $125 million Projects sub-envelope within the historical $160 million Watershed allocation as the P0 ClimateCapital Historical Baseline Scenario constraint. | The P0 cohort contains individually named project requests; other Watershed allocations are outside this portfolio rather than unallocated funds. | Active |
| D-011 | 2026-08-25 | Distinguish Historical City Recommendation, ClimateCapital Historical Baseline Scenario, and analyst-created What-If Scenarios everywhere in the product. | Clear names, status, and provenance prevent historical outcomes from being mistaken for ClimateCapital recommendations or user-created runs. | Active |
| D-012 | 2026-08-25 | Isolate the Historical City Recommendation as a descriptive benchmark that never influences ClimateCapital eligibility, evidence, scoring, ranking, weights, or portfolio selection. | This prevents outcome leakage and preserves analytical integrity. | Active |
| D-013 | 2026-08-25 | Apply documented eligibility rules to derive the candidate cohort; retain 15–30 only as an expected range. | Candidate selection must be reproducible and must not be tuned for an attractive demo. | Active |
| D-014 | 2026-08-25 | Use full-project inclusion or exclusion in P0 and disclose that partial funding is intentionally out of scope. | A clear binary assumption keeps the historical portfolio decision understandable without implying operational indivisibility. | Active |
| D-015 | 2026-08-25 | Keep individual project ranking separate from constrained portfolio optimization. | A high-ranking project can be excluded when another combination better satisfies the active envelope and objective. | Active |
| D-016 | 2026-08-25 | Treat January 21 as the bond decision context, not a universal date requirement for external evidence; show each source and vintage explicitly. | Defensible evidence may require datasets from different relevant publication periods. | Active |
| D-017 | 2026-08-25 | Limit scenario changes to budget and approved weights; Gemini may propose changes, but the analyst must review and confirm before deterministic recalculation. | This preserves human control and keeps scoring, ranking, constraints, and portfolio outcomes authoritative and reproducible. | Active |
| D-018 | 2026-08-25 | Defer scoring criteria, default weights, confidence methodology, and the final eligible cohort count beyond Stage 2. | These choices require later evidence and requirements work and must not be implied by the Stage 2 lock. | Active |
| D-019 | 2026-08-25 | Lock Stage 2 decisions as constraints for subsequent planning unless material source evidence contradicts them. | Later stages should refine the product without silently reopening approved product context. | Active |
| D-020 | 2026-08-25 | Create a local documentation checkpoint after Stage 1 and locked Stage 2, before beginning Stage 3. | The approved product context needs a recoverable baseline before backlog planning continues. | Active |
| D-021 | 2026-08-25 | Publish the documentation checkpoint to the public `swethabarla19/ClimateCapitalAI` GitHub repository on `main`. | The remote checkpoint provides durable off-device recovery and a visible project history before Stage 3. | Active |
| D-022 | 2026-08-25 | Pull the deadline plan ahead of UX definition and plan approximately 65–70 hours across six flexible workdays per week. | Early milestone constraints make the remaining product scope and tradeoffs concrete. | Active |
| D-023 | 2026-08-25 | Complete the Product and Design Lock by August 27 evening. | UX ambiguity must be removed before implementation-readiness and evidence work. | Active |
| D-024 | 2026-08-25 | Resolve analytics and evidence risk before integrated feature work. | Eligibility, scoring, confidence, and source support determine whether the product can make defensible claims. | Active |
| D-025 | 2026-08-25 | Freeze required P0 features by September 2 evening. | A fixed scope protects deployment, QA, demo rehearsal, and submission contingency. | Active |
| D-026 | 2026-08-25 | Respond to a missed gate by freezing or cutting scope, not by reducing the testing buffer. | A smaller verified product is more credible than a larger untested submission. | Active |
| D-027 | 2026-08-25 | Start no P1 work unless required P0 is complete at least 24 hours early and at least 10 contingency hours remain. | This prevents optional breadth from jeopardizing the submission. | Active |
| D-028 | 2026-08-26 | Treat exactly-two-project comparison as conditional stretch P0 and the first scope cut. | It can improve analyst understanding but is not necessary to prove the core portfolio journey. | Active |
| D-029 | 2026-08-26 | Use distinct labels for the Historical Decision Snapshot, Historical City Recommendation, ClimateCapital Historical Baseline Scenario, and analyst-created What-If Scenario. | The snapshot is context, the City result is a benchmark, and the two ClimateCapital scenarios are analytical results with different input provenance. | Active |
| D-030 | 2026-08-26 | Apply binary full-project inclusion/exclusion only to ClimateCapital P0 scenarios and preserve published City treatment and amounts separately. | ClimateCapital's simplifying assumption must not rewrite or mischaracterize the historical record. | Active |
| D-031 | 2026-08-26 | Allow either a reviewed ClimateCapital Historical Baseline Scenario portfolio or a confirmed active What-If portfolio to be designated as the current-session draft. | The analyst needs to carry forward the reviewed choice without implying persistence or official approval. | Active |
| D-032 | 2026-08-26 | Permit one atomic Gemini proposal to coordinate multiple approved-weight changes when needed for a valid configuration. | Weight constraints may require coupled changes, while atomic review preserves analyst control. | Active |
| D-033 | 2026-08-26 | Do not make missing display geometry alone an eligibility failure. | Analytical eligibility and map display capability are different concerns; inventing geometry is unacceptable. | Active |
| D-034 | 2026-08-26 | Expose excluded source records and reasons without assuming every excluded record is an individual project. | The eligibility audit must accurately represent heterogeneous source material. | Active |
| D-035 | 2026-08-26 | Defer the exact score-breakdown and normalization structure to the evidence and methodology gate. | Stage 3 can require transparency without pre-judging unsupported analytical design. | Active |
| D-036 | 2026-08-26 | Use the capital planning analyst as the sole P0 product persona. | One coherent decision workflow is achievable before the deadline; stakeholder-specific workflows remain out of scope. | Active |
| D-037 | 2026-08-26 | Keep calendar, demo-duration, deployment, and zero-critical-defect gates separate from story-level acceptance criteria. | Release readiness and user behavior are different test layers and should remain traceable. | Active |
| D-038 | 2026-08-26 | Maintain one immutable ClimateCapital Historical Baseline Scenario and at most one active What-If Scenario in P0. | This supports meaningful exploration without introducing saved-scenario management. | Active |
| D-039 | 2026-08-26 | Preserve the bounded map, provenance, City benchmark, copilot, Parks P1, and accessibility commitments in the prioritized backlog. | These commitments distinguish the product while respecting the approved pilot boundaries. | Active |
| D-040 | 2026-08-26 | Require structured manual budget and approved-weight controls and route them through the same validation and deterministic engine as Gemini proposals. | The core scenario workflow cannot depend on AI availability or create divergent analytical paths. | Active |
| D-041 | 2026-08-26 | Treat draft acceptance as a current-session designation, not a persisted copy; replacing an accepted What-If clears the designation after warning. | This provides a clear end state without adding accounts, storage, versioning, or false workflow semantics. | Active |
| D-042 | 2026-08-26 | Define Historical City Recommendation as the published January 2026 City Initial Recommendation and use City-specific inclusion terminology. | This preserves historical meaning and prevents City treatment from being confused with ClimateCapital selection. | Active |
| D-043 | 2026-08-26 | Lock the Stage 3 backlog and acceptance criteria as constraints for Stage 4 and later planning unless material source evidence contradicts them. | Subsequent stages should define the experience and implementation without silently expanding or reopening approved scope. | Active |
| D-044 | 2026-08-26 | Use Explore and Funding Plan as required primary decision destinations; keep Compare conditional SP0-1. | The smallest coherent P0 needs spatial inspection and a dedicated portfolio workspace, while comparison remains the first deadline cut. | Active |
| D-045 | 2026-08-26 | Keep Explore map-dominant with a synchronized compact Recommended Projects list and presentation-only search, sorting, and filters. | The map should lead the spatial story without allowing display controls to change analytical results. | Active |
| D-046 | 2026-08-26 | Use one shared Project Detail component with distinct map-marker and Recommended Projects row entry paths. | Marker clicks need a lightweight preview, while row clicks can open detail directly; both paths must preserve Explore state and converge on the same evidence. | Active |
| D-047 | 2026-08-26 | Use context-dependent Gemini prominence and shared contextual regions. | Proactive spatial interpretation adds value on Explore, while Funding Plan and project contexts need bounded, optional explanations without permanent chat. | Active |
| D-048 | 2026-08-26 | Evidence-gate optional metrics and drive low-confidence warnings only from the approved methodology and threshold. | The UI must not invent metrics, confidence judgments, or missing-as-zero interpretations. | Active |
| D-049 | 2026-08-26 | Preserve optimizer-controlled Funding Plan membership with no manual project override. | P0 scenarios change only budget and approved weights, preserving deterministic portfolio authority. | Active |
| D-050 | 2026-08-26 | Use one dedicated Funding Plan workspace with a progressive-disclosure Scenario Settings drawer and supported deltas from the immutable Historical Baseline. | The portfolio, governed scenario editing, and comparison need enough space while Explore remains focused. | Active |
| D-051 | 2026-08-26 | Keep Historical Benchmark as a secondary Funding Plan view. | The published City recommendation is useful descriptive context but is not the current scenario, a target, or an analytical input. | Active |
| D-052 | 2026-08-26 | Use in-place Reviewed Draft confirmation and bind review state to the exact current-session deterministic result. | This creates a clear demo end state without persistence, approval workflow, or false official status. | Active |
| D-053 | 2026-08-26 | Use a narrow primary sidebar plus a header showing decision context, current confirmed scenario, and Available Budget. | Persistent context prevents the analyst from confusing the current result with historical references while preserving workspace width. | Active |
| D-054 | 2026-08-26 | Place the eligibility audit and analytical chain on one anchored Data & Methodology page. | A single traceable source supports provenance without expanding P0 into a separate audit workspace. | Active |
| D-055 | 2026-08-26 | Group Funding Plan candidates into Recommended and Not Included sections. | The analyst must see both portfolio membership outcomes while keeping individual Funding Priority separate. | Active |
| D-056 | 2026-08-26 | Keep Help & Resources as a compact quick guide linked to detailed methodology. | Required orientation and limitations need a discoverable home without duplicating the full evidence documentation. | Active |
| D-057 | 2026-08-26 | Use explicit, non-generic UI state categories and contain recoverable failures to the affected surface. | Zero matches, no eligible cohort, missingness, infeasibility, and system errors have different meanings and recovery paths. | Active |
| D-058 | 2026-08-26 | Preserve the last successful deterministic Funding Plan across later failed or infeasible recalculation attempts. | Unapplied scenario changes must never overwrite or masquerade as the current confirmed result. | Active |
| D-059 | 2026-08-26 | Distinguish the presentation-filter match count from the rule-derived eligible-cohort count everywhere. | Filtering changes visibility only and must not appear to change analytical eligibility. | Active |
| D-060 | 2026-08-26 | Treat every value and name shown in Stage 4 low-fidelity wireframes as an illustrative placeholder. | UX examples must not preempt evidence decisions or become implementation constants. | Active |
| D-061 | 2026-08-26 | Reaffirm structured Gemini-generated scenario proposals as an already-approved P0 capability. | P0-9, D-032, and D-040 already authorize bounded proposals for budget and approved weights with analyst confirmation and deterministic execution. | Active |
| D-062 | 2026-08-26 | Keep the Layers control and popover closed by default without deciding default analytical-layer visibility in Stage 4. | Progressive disclosure governs the controls, while the evidence stage must determine the defensible default visualization. | Active |
| D-063 | 2026-08-26 | Label the header with the current confirmed scenario while keeping the immutable Historical Baseline and Historical Benchmark conceptually separate. | The analyst must distinguish the active result, the baseline reference for supported deltas, and the descriptive City comparison. | Active |

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-08-26 | Stage 4 Product and Design Lock closeout | Reviewed the complete documentation diff; ran `git diff --check`; confirmed the changed-file boundary, Stage 4 section coverage, 20 continuous decisions from D-044 through D-063, current-state terminology, and balanced Markdown code fences | Passed; only `PROJECT_PROGRESS.md` and `README.md` changed, Stage 1–3 remain unchanged in meaning, and no application or technical implementation was introduced |
| 2026-08-26 | Stage 3 documentation checkpoint | Read all repository guidance and canonical documentation; ran `git diff --check`; counted 12 P0 stories, one stretch P0 story, and 13 acceptance-criteria blocks; checked decision-log continuity, stale terminology, branch, status, and remotes | Passed; only `PROJECT_PROGRESS.md` and `README.md` are modified, Stage 4 remains unstarted, and no commit or push was made |
| 2026-08-25 | Local/remote tracker reconciliation | Compared local `main` and GitHub commit history, remote URL, branch tracking, working-tree state, milestones, blockers, risks, decisions, technical map, and next actions | Passed; remote head matched local head before this tracker update |
| 2026-08-25 | GitHub checkpoint publication | Verified repository ownership and public visibility, inspected and preserved the remote README commit, merged histories, and pushed `main` | Passed; local `main` tracks `origin/main` |
| 2026-08-25 | Git and Stop-hook checkpoint | Verified repository root, `main` branch, author configuration, status, remotes, hook registration, and executable availability | Local Git ready; GitHub remote absent; process-jobs Stop hook lacks `node` |
| 2026-08-25 | Stage 2 product definition | Checked the locked context against all 12 requested clarifications and confirmed that deferred scoring and cohort choices remain open | Passed |
| 2026-08-24 | P0 hazard and equity framing | Reconciled the selected option with the current watershed scope and Map → projects → portfolio journey | Passed |
| 2026-08-24 | Progress system | Manual review of required handoff sections and repository instructions | Passed |

## Session Log

Add new entries immediately below this guidance so the newest session is first.

### 2026-08-26 — Lock Stage 4 Product and Design documentation

- **Objective:** Persist the approved final Product and Design Lock using the
  repository's existing documentation structure without beginning application or
  technical implementation.
- **Completed:** Marked Stage 4 complete; recorded the required screens, navigation
  and contextual surfaces, screen requirements, important state/recovery model,
  low-fidelity wireframes, demo sequence, assumptions, dependencies, risks, and
  evidence deferrals; kept Compare conditional SP0-1; and added D-044 through
  D-063 while preserving the Stage 1–3 locks.
- **Files changed:** `PROJECT_PROGRESS.md`, `README.md`. No files were created, and
  no application, architecture, data, analytics, Gemini, cloud, or dependency work
  was performed.
- **Verification:** Reviewed the complete documentation diff; `git diff --check`
  passed; confirmed only the two intended documentation files changed, all 20 new
  decisions appear once and in sequence, required Stage 4 content is present,
  current-state language is updated, and Markdown code fences are balanced.
- **Handoff:** The next planned work item is a separately authorized technical
  execution-readiness plan, followed by evidence-stage decisions. Neither has
  begun.

### 2026-08-26 — Prepare the locked Stage 3 documentation checkpoint

- **Objective:** Persist all approved planning through Stage 3 in the existing
  canonical repository structure without beginning Stage 4 or application work.
- **Completed:** Reconciled `AGENTS.md`, `PROJECT_PROGRESS.md`, and `README.md`;
  recorded the locked P0/P1/Later backlog and acceptance criteria, deadline and
  release gates, terminology, scope and scenario rules, deferred decisions, risks,
  milestones, decision log, and Stage 4 handoff; expanded the README only as a
  concise pointer to the canonical tracker.
- **Files changed:** `PROJECT_PROGRESS.md`, `README.md`. No files were created.
- **Verification:** `git diff --check` passed; confirmed 12 required P0 stories,
  one conditional stretch P0 story, 13 acceptance-criteria blocks, continuous
  decisions through D-043, no targeted stale-current-state phrases, branch `main`,
  upstream tracking, and the configured `origin` remote.
- **Handoff:** Await user review. Do not commit, push, or begin Stage 4 until the
  user explicitly approves the checkpoint.

### 2026-08-25 — Reconcile the local and remote progress tracker

- **Objective:** Ensure the canonical tracker reflects all approved product work,
  the local checkpoint, GitHub publication, current operational issue, and the next
  planning stage.
- **Completed:** Confirmed Stage 1 and Stage 2 milestones and constraints; verified
  the public repository and commit history; updated the current snapshot,
  workstream, risks, technical map, verified Git commands, and next-action handoff.
- **Files changed:** `PROJECT_PROGRESS.md`.
- **Verification:** Compared the local `main` history and clean upstream state with
  GitHub's reported commits and reviewed every required tracker section for current
  accuracy.
- **Handoff:** Start Stage 3 by defining and prioritizing P0, P1, and Later user
  stories with testable acceptance criteria; preserve the locked Stage 2
  constraints.

### 2026-08-25 — Publish the Stage 1 and Stage 2 checkpoint to GitHub

- **Objective:** Connect the authorized public GitHub repository and publish all
  completed documentation before Stage 3.
- **Completed:** Verified `swethabarla19/ClimateCapitalAI` ownership and public
  visibility; added it as `origin`; inspected and preserved its one-line README
  commit; merged the histories; and pushed the Stage 1 and locked Stage 2
  checkpoint to `main`.
- **Files changed:** `README.md` added from the remote history;
  `PROJECT_PROGRESS.md` updated with the current repository state.
- **Verification:** Confirmed GitHub admin and push permissions, fetched and
  inspected `origin/main`, completed a non-destructive merge, pushed successfully,
  and configured local `main` to track `origin/main`.
- **Handoff:** Begin Stage 3 with the locked Stage 2 constraints and checkpointed
  documentation.

### 2026-08-25 — Diagnose Stop hook and create documentation checkpoint

- **Objective:** Verify Git/GitHub state, diagnose the exit-127 Stop hook, and
  checkpoint the approved Stage 1 and Stage 2 documentation before Stage 3.
- **Completed:** Identified the `codex-process-jobs` Stop hook's unavailable `node`
  runtime; verified the local repository, `main` branch, author configuration, and
  absent remote; captured `AGENTS.md` and `PROJECT_PROGRESS.md` in the initial local
  checkpoint.
- **Files changed:** `PROJECT_PROGRESS.md`; `AGENTS.md` and `PROJECT_PROGRESS.md`
  added to local version control.
- **Verification:** Reproduced exit 127 for unavailable `node`; inspected hook
  registration and command; checked Git root, branch, status, author, history,
  remotes, and GitHub CLI availability.
- **Handoff:** Obtain an existing GitHub repository URL or explicit authorization
  to create one before adding `origin` or pushing; then begin Stage 3.

### 2026-08-25 — Lock Stage 2 product definition

- **Objective:** Incorporate the historical decision context and analytical
  boundaries, then lock Stage 2 before backlog prioritization.
- **Completed:** Defined the January 2026 Historical Baseline, $125 million Projects
  constraint, scenario terminology, rule-derived cohort, binary funding assumption,
  ranking-versus-portfolio distinction, source-vintage policy, City benchmark
  isolation, Gemini boundary, editable inputs, and deferred later-stage decisions.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Reconciled the canonical snapshot, next actions, open questions,
  risks, decisions, and handoff against the 12 approved clarifications.
- **Handoff:** Begin Stage 3 by prioritizing P0, P1, and Later user stories with
  acceptance criteria; do not silently reopen the locked Stage 2 constraints.

### 2026-08-24 — Choose the P0 hazard and equity framing

- **Objective:** Decide whether the watershed pilot should prove multi-hazard
  breadth or a coherent first decision domain.
- **Completed:** Selected flood plus equity as the P0 core; kept urban heat as
  optional context or a clearly labeled, evidence-backed co-benefit.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Checked the choice against the existing watershed scope and
  Map → projects → portfolio decision.
- **Handoff:** Define the flood and vulnerability inputs and the evidence threshold
  for displaying a heat co-benefit.

### 2026-08-24 — Select the P0 product journey

- **Objective:** Clarify the primary product journey and how it can expand beyond
  watershed projects.
- **Completed:** Selected Map → projects → portfolio; established that users
  enter inputs before receiving a recommendation; scoped P0 to watershed projects
  and parks as a candidate P1 type.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Reconciled the decisions with the repository; no application
  implementation exists yet.
- **Handoff:** Define the P0 map inputs, watershed-project data model, and portfolio
  recommendation rules before choosing the implementation architecture.

### 2026-08-24 — Initialize cross-session project tracking

- **Objective:** Create durable project context that can bridge multiple sessions.
- **Completed:** Created the canonical progress file and agent maintenance rules.
- **Files changed:** `PROJECT_PROGRESS.md`, `AGENTS.md`
- **Verification:** Reviewed the documents for startup guidance, current status,
  actions, decisions, blockers, risks, technical context, and session history.
- **Handoff:** Start with **Project Definition**, then revise **Current Snapshot** and
  **Next Actions** to reflect the agreed direction.
