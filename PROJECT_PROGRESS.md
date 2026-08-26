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
- **Project stage:** Stage 3 backlog approved and locked; Stage 4 screen and UX
  definition has not started.
- **Current focus:** Review and checkpoint the approved planning work through Stage
  3, then define the minimum screen inventory, navigation, requirements, states,
  and low-fidelity wireframes in Stage 4.
- **Working state:** Documentation-only Git repository on `main`, connected to the
  public GitHub repository `swethabarla19/ClimateCapitalAI`; no application code or
  tooling exists yet. The Stage 1 and locked Stage 2 checkpoint is published, and
  the Stage 3 documentation checkpoint is awaiting review before commit.
- **Most recent outcome:** Approved and locked the required P0, conditional stretch
  P0, P1, and Later backlog; story-level acceptance criteria; terminology and scope
  boundaries; scenario-state rules; and deadline release gates.

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

## Current Workstream

- **Goal:** Complete an approved Product and Design Lock for the September 7 MVP
  submission.
- **Status:** Stage 1 and Stage 2 are approved and published; the deadline plan and
  Stage 3 backlog are approved and locked. Stage 4 has not started. The current
  documentation-only checkpoint is awaiting review before commit or push.
- **Owner:** User and Codex.
- **Relevant files:** `PROJECT_PROGRESS.md`, `AGENTS.md`, `README.md`
- **Acceptance criteria:** Product vision, primary user and problem, goals and
  non-goals, prioritized backlog and acceptance criteria, primary journey,
  approved screens and wireframes, demo sequence, timeline, assumptions, risks,
  and open questions are documented and explicitly approved.

## Next Actions

1. Review this Stage 3 documentation checkpoint and, only after explicit approval,
   commit and push it.
2. Begin Stage 4 by defining the minimum screen inventory, navigation flow, screen
   requirements, states, and low-fidelity wireframes; obtain explicit Stage 4
   approval before continuing.
3. Finalize the primary demo sequence and complete the Product and Design Lock by
   the August 27 gate.
4. Verify organizer submission artifacts, judging criteria, and conditional live-
   demo details.
5. Resolve evidence-readiness decisions by August 29: governed scoring dimensions,
   default weights, confidence methodology, rule-derived cohort, source vintages,
   supported portfolio metrics, and the heat co-benefit evidence threshold.
6. Update this tracker and create an approved Git checkpoint after each newly
   locked planning stage.

## Completed Milestones

- **2026-08-26 — Stage 3 backlog approved and locked:** Prioritized 12 required P0
  stories, one conditional stretch P0 story, P1, and Later work; defined testable
  acceptance criteria, scenario-state rules, terminology, scope boundaries, and
  release gates. Stage 4 remains unstarted.
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

- No blocker prevents continued product and UX planning.
- Official judging criteria, submission artifact requirements, and conditional
  live-demo details remain unconfirmed and block final submission-package planning,
  but not Stage 4 UX definition.

## Risks and Watch Items

- The 12-story required P0 scope is ambitious for the September 2 feature freeze;
  the conditional two-project comparison must be cut first and no P1 work may
  displace required P0.
- The final rule-derived candidate count and evidence coverage may differ from the
  expected 15–30 range; the demo must not drive cohort selection.
- Scoring criteria, default weights, and confidence treatment remain intentionally
  unresolved and could become a trust risk if rushed or presented as arbitrary.
- The three scenario types may be confused unless names, dates, status, and change
  provenance are consistently visible.
- A map-first journey could resemble a generic dashboard unless it reaches the
  constrained portfolio decision quickly.
- Natural-language propose → review → confirm interactions add meaningful P0 scope
  and must not obscure which inputs changed or who authorized the rerun.
- Eligible candidates without defensible display geometry will weaken the map-first
  presentation; the non-map journey and visible limitation labels are required.
- Gemini proposal and explanation flows could consume disproportionate effort;
  deterministic results and manual scenario controls must remain complete and
  usable if Gemini is unavailable.
- Missing source or methodology support may restrict portfolio comparison metrics;
  P0 must not invent benefits, impacts, or optimization claims for demo appeal.
- Heat context or co-benefit claims could overstate the evidence unless the team
  defines a clear inclusion threshold and labels them separately from core scores.
- Historical source context and external evidence vintages could be conflated if
  January 21 is incorrectly applied as a blanket dataset-date requirement.
- The `codex-process-jobs` Stop hook currently exits with code 127 because `node`
  is unavailable. This did not affect the documentation checkpoint, but process-job
  completion checks remain unreliable until the runtime or hook configuration is
  fixed.

## Open Questions

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

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-08-26 | Stage 3 documentation checkpoint | Read all repository guidance and canonical documentation; ran `git diff --check`; counted 12 P0 stories, one stretch P0 story, and 13 acceptance-criteria blocks; checked decision-log continuity, stale terminology, branch, status, and remotes | Passed; only `PROJECT_PROGRESS.md` and `README.md` are modified, Stage 4 remains unstarted, and no commit or push was made |
| 2026-08-25 | Local/remote tracker reconciliation | Compared local `main` and GitHub commit history, remote URL, branch tracking, working-tree state, milestones, blockers, risks, decisions, technical map, and next actions | Passed; remote head matched local head before this tracker update |
| 2026-08-25 | GitHub checkpoint publication | Verified repository ownership and public visibility, inspected and preserved the remote README commit, merged histories, and pushed `main` | Passed; local `main` tracks `origin/main` |
| 2026-08-25 | Git and Stop-hook checkpoint | Verified repository root, `main` branch, author configuration, status, remotes, hook registration, and executable availability | Local Git ready; GitHub remote absent; process-jobs Stop hook lacks `node` |
| 2026-08-25 | Stage 2 product definition | Checked the locked context against all 12 requested clarifications and confirmed that deferred scoring and cohort choices remain open | Passed |
| 2026-08-24 | P0 hazard and equity framing | Reconciled the selected option with the current watershed scope and Map → projects → portfolio journey | Passed |
| 2026-08-24 | Progress system | Manual review of required handoff sections and repository instructions | Passed |

## Session Log

Add new entries immediately below this guidance so the newest session is first.

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
