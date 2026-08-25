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

- **Last updated:** 2026-08-25
- **Project stage:** Stage 2 product definition locked; Stage 3 backlog definition
  is next.
- **Current focus:** Convert the locked product context and Map → Projects →
  Portfolio journey into prioritized P0, P1, and Later user stories with acceptance
  criteria.
- **Working state:** Documentation-only Git repository on `main`; no application
  code or tooling exists yet. The Stage 1 and locked Stage 2 documentation is
  captured in the initial local checkpoint.
- **Most recent outcome:** Locked the January 2026 Historical Baseline as a
  historical Austin Watershed decision-support simulation using the $125 million
  Projects sub-envelope, with strict separation between City history,
  ClimateCapital analysis, and analyst-created what-if scenarios.

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
- **Historical decision context:** January 21, 2026 is the City of Austin 2026 Bond
  Initial Draft Project Recommendation snapshot, not an arbitrary product date.
  The historical Watershed allocation is $160 million, including a $125 million
  **Projects** allocation. P0 uses that $125 million Projects sub-envelope as the
  Historical Baseline constraint for eligible individually named Watershed project
  requests; the remaining Watershed allocations are outside the P0 portfolio and
  are not unallocated project funds.
- **Scenario terminology:** **Historical City Recommendation** means the published
  City outcome and is a descriptive benchmark only. **ClimateCapital Historical
  Baseline** means ClimateCapital's result under the documented January 2026
  historical context and $125 million constraint. **Analyst-created What-If
  Scenario** means a confirmed run with an altered budget or approved weights.
- **In scope:** A rule-derived Watershed candidate cohort; Map → Projects →
  Portfolio; flood exposure and expected flood-reduction benefit as the primary
  recommendation signals; social vulnerability as a cross-cutting equity lens;
  transparent eligibility, evidence, ranking, constrained portfolio selection,
  uncertainty, source/vintage disclosure, scenario comparison, governed budget
  and weight changes, grounded explanations, and current-session draft acceptance.
- **Out of scope:** Official funding decisions or predictions; the current ballot
  package; manually curated demo candidates; cross-department competition for an
  unrestricted pool; partial project funding; editing source data, project costs,
  eligibility, or constraints; permanent accounts or saved scenarios; formal
  approvals or report export; separate stakeholder workflows; authoritative AI
  scoring or portfolio selection; and urban heat as a P0 score input. Heat may
  appear only as defensible context or a clearly labeled project-specific
  co-benefit.

## Current Workstream

- **Goal:** Complete an approved Product and Design Lock for the September 7 MVP
  submission.
- **Status:** Stage 1 and Stage 2 approved; Stage 3 not started.
- **Owner:** User and Codex.
- **Relevant files:** `PROJECT_PROGRESS.md`, `AGENTS.md`
- **Acceptance criteria:** Product vision, primary user and problem, goals and
  non-goals, prioritized backlog and acceptance criteria, primary journey,
  approved screens and wireframes, demo sequence, timeline, assumptions, risks,
  and open questions are documented and explicitly approved.

## Next Actions

1. Define and prioritize P0, P1, and Later user stories with acceptance criteria.
2. Decide the governed P0 scoring criteria, default weights, and confidence
   treatment during the appropriate later requirements stage; do not treat them as
   Stage 2 decisions.
3. Define the minimum screen inventory, navigation, requirements, states, and
   low-fidelity wireframes.
4. Create a deadline plan with scope checkpoints and contingency time leading to
   the September 6 internal submission window.
5. Verify organizer submission requirements and finalize the Product and Design
   Lock.

## Completed Milestones

- **2026-08-25 — Stage 1 and Stage 2 Git checkpoint created:** Captured the
  repository guidance and canonical product handoff in the initial local commit
  before beginning Stage 3.
- **2026-08-25 — Stage 2 product definition locked:** Defined the primary user,
  problem, value proposition, Historical Baseline decision context, scenario
  terminology, goals, non-goals, assumptions, and core Map → Projects → Portfolio
  journey. These decisions constrain later planning unless material source evidence
  contradicts them.
- **2026-08-24 — Stage 1 deadline and success baseline approved:** Set the official
  September 7 deadline, September 6 internal submission window, 40-hour weekly
  planning capacity, judge-facing audience assumption, three-minute core demo, and
  finalist-worthy deployed P0 success bar.
- **2026-08-24 — Cross-session continuity initialized:** Added a canonical project
  progress document and repository instructions for maintaining it.

## Blockers

- No blocker prevents continued product and UX planning.
- No GitHub remote is configured; the local checkpoint cannot be pushed until an
  existing repository URL is provided or creation of a new repository is explicitly
  authorized.
- Official judging criteria, submission artifact requirements, and conditional
  live-demo details remain unconfirmed.

## Risks and Watch Items

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
- Heat context or co-benefit claims could overstate the evidence unless the team
  defines a clear inclusion threshold and labels them separately from core scores.
- Historical source context and external evidence vintages could be conflated if
  January 21 is incorrectly applied as a blanket dataset-date requirement.

## Open Questions

- Which governed scoring criteria and default weights should P0 use?
- How should missingness, uncertainty, and confidence affect eligibility, scoring,
  and presentation?
- What is the final eligible project count after documented rules are applied?
- Which copilot questions and budget/weight proposal phrasings must P0 support?
- How much Historical City Recommendation comparison belongs in the three-minute
  path?
- Can every eligible candidate be represented with defensible point, area, or
  service-geography evidence?
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
- Local Git branch: `main`.
- GitHub remote: Not configured.

### Environments and External Services

None established.

### Common Commands

None established. Add setup, development, test, lint, build, migration, and deploy
commands here as they are introduced and verified.

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
| D-010 | 2026-08-25 | Use the $125 million Projects sub-envelope within the historical $160 million Watershed allocation as the P0 Historical Baseline constraint. | The P0 cohort contains individually named project requests; other Watershed allocations are outside this portfolio rather than unallocated funds. | Active |
| D-011 | 2026-08-25 | Distinguish Historical City Recommendation, ClimateCapital Historical Baseline, and analyst-created What-If Scenarios everywhere in the product. | Clear names, status, and provenance prevent historical outcomes from being mistaken for ClimateCapital recommendations or user-created runs. | Active |
| D-012 | 2026-08-25 | Isolate the Historical City Recommendation as a descriptive benchmark that never influences ClimateCapital eligibility, evidence, scoring, ranking, weights, or portfolio selection. | This prevents outcome leakage and preserves analytical integrity. | Active |
| D-013 | 2026-08-25 | Apply documented eligibility rules to derive the candidate cohort; retain 15–30 only as an expected range. | Candidate selection must be reproducible and must not be tuned for an attractive demo. | Active |
| D-014 | 2026-08-25 | Use full-project inclusion or exclusion in P0 and disclose that partial funding is intentionally out of scope. | A clear binary assumption keeps the historical portfolio decision understandable without implying operational indivisibility. | Active |
| D-015 | 2026-08-25 | Keep individual project ranking separate from constrained portfolio optimization. | A high-ranking project can be excluded when another combination better satisfies the active envelope and objective. | Active |
| D-016 | 2026-08-25 | Treat January 21 as the bond decision context, not a universal date requirement for external evidence; show each source and vintage explicitly. | Defensible evidence may require datasets from different relevant publication periods. | Active |
| D-017 | 2026-08-25 | Limit scenario changes to budget and approved weights; Gemini may propose changes, but the analyst must review and confirm before deterministic recalculation. | This preserves human control and keeps scoring, ranking, constraints, and portfolio outcomes authoritative and reproducible. | Active |
| D-018 | 2026-08-25 | Defer scoring criteria, default weights, confidence methodology, and the final eligible cohort count beyond Stage 2. | These choices require later evidence and requirements work and must not be implied by the Stage 2 lock. | Active |
| D-019 | 2026-08-25 | Lock Stage 2 decisions as constraints for subsequent planning unless material source evidence contradicts them. | Later stages should refine the product without silently reopening approved product context. | Active |
| D-020 | 2026-08-25 | Create a local documentation checkpoint after Stage 1 and locked Stage 2, before beginning Stage 3. | The approved product context needs a recoverable baseline before backlog planning continues. | Active |

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-08-25 | Git and Stop-hook checkpoint | Verified repository root, `main` branch, author configuration, status, remotes, hook registration, and executable availability | Local Git ready; GitHub remote absent; process-jobs Stop hook lacks `node` |
| 2026-08-25 | Stage 2 product definition | Checked the locked context against all 12 requested clarifications and confirmed that deferred scoring and cohort choices remain open | Passed |
| 2026-08-24 | P0 hazard and equity framing | Reconciled the selected option with the current watershed scope and Map → projects → portfolio journey | Passed |
| 2026-08-24 | Progress system | Manual review of required handoff sections and repository instructions | Passed |

## Session Log

Add new entries immediately below this guidance so the newest session is first.

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
