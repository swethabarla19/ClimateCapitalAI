# ClimateCapitalAI Project Progress

> **Canonical role:** Current state, stage, progress, blockers, active risks, open
> questions, milestones, and cross-task handoff. Detailed specifications and
> decision history live in the linked authoritative documents below.

## How to Maintain This File

At the start of every task:

1. Read this file completely.
2. Reconcile it with the repository; repository state wins if they differ.
3. Read the authoritative documents listed for the active task.
4. Begin with the first unblocked item in **Next Actions** unless the user changes
   priority.

At the end of every task:

1. Update the current snapshot, workstream, next actions, milestones, blockers,
   active risks, open questions, verification record, technical map, and session
   log wherever the task changed them.
2. Keep the session log newest-first and preserve historical entries.
3. Record detailed durable decisions in
   [docs/decisions.md](docs/decisions.md) using the next sequential ID.
4. Update a purpose-specific specification only when an approved change
   legitimately affects it; do not duplicate the same detail here.

Never record secrets, credentials, tokens, or sensitive personal data. Do not
create docs/delivery/progress.md; this file is the only progress/status tracker.

## Source-of-Truth Map

| Subject | Authoritative source |
| --- | --- |
| Repository working rules and task startup | [AGENTS.md](AGENTS.md) |
| Current state, progress, blockers, risks, and handoff | This file |
| Product vision, scope, principles, workflow, and non-goals | [docs/product/product-plan.md](docs/product/product-plan.md) |
| Prioritized stories and acceptance intent | [docs/product/user-stories.md](docs/product/user-stories.md) |
| Screens, navigation, UI behavior, states, recovery, and wireframes | [docs/product/screen-spec.md](docs/product/screen-spec.md) |
| Initial delivery sequencing, deadline, and release gates | [docs/delivery/execution-plan.md](docs/delivery/execution-plan.md) |
| Durable decision history | [docs/decisions.md](docs/decisions.md) |
| Architecture-planning reference; not an approved design | [docs/reference/technical-architecture-reference.md](docs/reference/technical-architecture-reference.md) |
| Approved architecture after explicit Architecture Lock | docs/architecture/ — intentionally absent |
| Architecture-informed implementation and test plans | docs/delivery/implementation-plan.md, test-plan.md, and milestones.md — intentionally absent |

Git is the version history for all repository memory. Fresh tasks must not depend on
access to prior chat conversations.

## Current Snapshot

- **Last updated:** 2026-08-27
- **Project stage:** Product and Design planning is complete and locked through
  Stage 4. Documentation normalization is complete; Architecture planning has not
  started.
- **Current milestone:** Hand off the approved Product and Design Lock to a fresh
  Architecture planning task.
- **Next milestone:** Investigate and explicitly approve an Architecture Lock before
  creating/finalizing the approved architecture, data-design, cloud-cost, and
  lineage documents.
- **Working state:** Documentation-only Git repository on main, connected to the
  public swethabarla19/ClimateCapitalAI GitHub repository. No application code,
  datasets, pipelines, dependencies, cloud resources, or architecture
  implementation exist.
- **Most recent outcome:** Extracted the approved Stage 1–4 planning into
  purpose-specific product, design, delivery, decision, and reference documents.
  PROJECT_PROGRESS.md remains the sole current-status tracker.

## Approved Locks

- **Stage 1 — Deadline and success:** Official deadline September 7, 2026 at
  10:00 a.m. CDT; internal submit window September 6 from 9:30–11:30 a.m. CDT;
  finalist-worthy deployed/tested P0; three-minute core demo expandable to five.
- **Stage 2 — Product definition:** Capital planning analyst persona, Austin
  Watershed historical simulation, January 2026 context, $125 million Projects
  sub-envelope, deterministic authority, rule-derived cohort, full-project
  selection, and strict City benchmark isolation.
- **Stage 3 — Backlog:** Twelve required P0 stories, conditional SP0-1 Compare as
  the first cut, ordered P1, Later scope, acceptance intent, and release gates.
- **Stage 4 — Product and Design Lock:** Required screens and contextual surfaces,
  navigation, UI states/recovery, low-fidelity wireframes, evidence gates, and
  three-minute demo sequence.

Stages 1–4 remain authoritative unless new source evidence creates a material
contradiction. Full details are in docs/product and docs/decisions.md.

## Current Workstream

- **Goal:** Begin a fresh, decision-complete Architecture planning task without
  reopening locked product/design scope or mistaking reference material for an
  approved architecture.
- **Status:** Ready for Architecture planning. No Architecture Lock or technical
  implementation has begun.
- **Owner:** User and Codex.
- **Required reading:** AGENTS.md, this file, all files under docs/product,
  docs/delivery/execution-plan.md, docs/decisions.md, and
  docs/reference/technical-architecture-reference.md.
- **Exit condition:** The user explicitly approves an Architecture Lock. Only then
  may the approved architecture files under docs/architecture be
  created/finalized.

## Next Actions

1. Start a fresh Architecture planning task and read the required handoff set above.
2. Reconcile current repository reality with the locked product/design constraints
   and the non-authoritative technical reference.
3. Investigate architecture alternatives, current cloud/service facts, data design,
   security, observability, testing implications, and low-cost deployment.
4. Present a decision-complete Architecture Lock proposal and obtain explicit
   approval before creating/finalizing docs/architecture files.
5. Resolve evidence readiness: sources, rule-derived cohort, vintages, defensible
   geometry, scoring, default/editable weights, confidence methodology,
   optimization objective, missingness, supported metrics, and map defaults.
6. Verify organizer submission artifacts, judging criteria, finale date, and
   conditional live-demo format.
7. After Architecture Lock, start a fresh implementation/testing planning task to
   create/refine implementation-plan.md, test-plan.md, execution-plan.md, and
   milestones.md.
8. Update this tracker and create an approved Git checkpoint after each locked
   stage or meaningful delivery milestone.

## Completed Milestones

- **2026-08-27 — Documentation architecture normalized:** Created authoritative
  product, story, screen, delivery, and decision documents plus a clearly
  non-authoritative technical reference; reduced this tracker to current status and
  pointers; added fresh-task reading rules.
- **2026-08-26 — Stage 4 Product and Design Lock approved:** Locked screen
  inventory, navigation, contextual surfaces, screen requirements, important
  states/recovery, wireframes, demo sequence, assumptions, dependencies, and risks.
- **2026-08-26 — Stage 3 backlog approved:** Locked 12 required P0 stories,
  conditional SP0-1, P1/Later, acceptance intent, terminology, and scope boundaries.
- **2026-08-25 — Deadline plan approved:** Protected an August 27 Product and
  Design Lock, September 2 feature freeze, testing, and submission contingency.
- **2026-08-25 — Stage 1 and Stage 2 checkpoint published:** Connected the public
  GitHub repository and published the approved product-context baseline.
- **2026-08-25 — Stage 2 product definition locked:** Locked the user, problem,
  value, historical context, scope, scenario terminology, and analytical
  boundaries.
- **2026-08-24 — Stage 1 deadline and success baseline approved:** Locked deadline,
  capacity, audience assumption, demo target, and success bar.
- **2026-08-24 — Cross-session continuity initialized:** Added repository guidance
  and a canonical progress tracker.

## Delivery Checkpoints

The detailed plan and sequencing rationale are authoritative in
[docs/delivery/execution-plan.md](docs/delivery/execution-plan.md).

- **Sep 2:** Required-P0 feature freeze.
- **Sep 3:** Public release candidate.
- **Sep 4:** Quality and three-minute demo gates.
- **Sep 5:** Final freeze.
- **Sep 6:** Internal submission and link verification.
- **Sep 7, 10:00 a.m. CDT:** Official deadline.

A missed gate cuts or freezes scope; it does not consume testing/submission
contingency. Conditional SP0-1 Compare is the first cut. P1 cannot begin early
unless required P0 is at least 24 hours ahead and 10 contingency hours remain.

## Blockers

- No blocker prevents Architecture investigation and planning.
- No architecture is approved; this blocks architecture implementation and final
  architecture documents.
- Evidence decisions block implementation of analytical claims, governed metrics,
  weights, confidence warnings, optimization, and default evidence visualizations.
- Official judging criteria, submission artifacts, and conditional live-demo
  details remain unconfirmed and block final submission-package planning.

## Active Risks

- Required P0 remains ambitious for the September 2 feature freeze; optional scope
  must not erode testing or recovery time.
- Architecture and evidence work are now on the critical path and must stay bounded.
- The final rule-derived cohort, evidence coverage, and geometry may be less
  demo-friendly than expected and must not be manually tuned.
- Unresolved scoring, confidence, missingness, and optimization choices may become
  trust risks if rushed or presented as arbitrary.
- The Historical Decision Snapshot, Historical City Recommendation, current
  confirmed scenario, and immutable Historical Baseline may be confused if the
  locked terminology is not implemented consistently.
- Gemini or map work could consume disproportionate effort; deterministic/manual
  paths and non-map access remain release priorities.
- Failed recalculation must not overwrite the last successful deterministic result.
- The process-job Stop hook still exits with code 127 because node is unavailable;
  process-job completion checks remain unreliable until its runtime/configuration is
  fixed.
- Current cloud pricing, quotas, program requirements, and source licensing have not
  been verified.

## Open Questions

### Evidence and methodology

- Which governed scoring dimensions, transformations, score breakdown,
  optimization objective, and default/editable weights should P0 use?
- How should missing evidence, uncertainty, and confidence affect eligibility,
  scoring, ranking, optimization, and presentation?
- What is the final eligible cohort after documented rules are applied?
- Which evidence vintages and defensible project geometries are available?
- Which portfolio comparison measures are supported?
- What evidence is sufficient for a project-specific heat co-benefit?
- Are People Potentially Benefiting and Implementation Readiness supported metrics?
- Which supported analytical layers should be active in the default Explore map?

### Architecture

- What is the smallest low-cost deployable system that satisfies required P0?
- Which work is precomputed versus performed at runtime?
- What governed contract separates deterministic analysis, UI, Historical
  Benchmark, and Gemini?
- Which Google Cloud, Gemini, frontend, map, storage, and deployment options meet
  deadline, cost, security, and reliability constraints?
- What data-versioning, lineage, observability, and teardown approach is required?

### Submission

- What are the official submission artifacts, judging criteria, finale date, and
  live-demo format?

There are no unresolved Stage 4 screen, navigation, state, wireframe, or demo
sequence decisions.

## Technical Map

### Architecture

Not established. The technical reference is exploratory and does not constitute an
Architecture Lock.

### Repository Structure

- AGENTS.md — repository rules and task-start routing.
- PROJECT_PROGRESS.md — sole current state/progress/handoff document.
- README.md — repository landing page and documentation map.
- docs/product/product-plan.md — approved product-level Product and Design Lock.
- docs/product/user-stories.md — authoritative prioritized backlog and acceptance
  intent.
- docs/product/screen-spec.md — authoritative UI, state, and wireframe specification.
- docs/delivery/execution-plan.md — initial approved delivery sequencing and gates.
- docs/decisions.md — authoritative durable decision history.
- docs/reference/technical-architecture-reference.md — exploratory Architecture
  planning reference.
- docs/architecture/ — intentionally absent until explicit Architecture Lock.
- docs/delivery/implementation-plan.md, test-plan.md, and milestones.md —
  intentionally absent until post-Architecture delivery planning.

Local branch: main. Public GitHub remote:
https://github.com/swethabarla19/ClimateCapitalAI.git.

### Environments and External Services

- No application environment or cloud resource is established.
- The local process-job Stop hook lacks the node runtime it expects.

### Common Commands

- git status --short --branch — verify working tree and upstream.
- git log --oneline --decorate --max-count=8 — inspect checkpoints.
- git diff --check — validate documentation whitespace.
- Add verified setup, test, lint, build, migration, and deploy commands only when
  tooling exists.

## Decision Summary

The authoritative history is [docs/decisions.md](docs/decisions.md).

- D-001–D-063 preserve all Stage 1–4 and repository decisions.
- D-064 establishes the purpose-specific repository-memory hierarchy.
- D-065 keeps the technical reference non-authoritative until Architecture Lock.
- D-066 keeps PROJECT_PROGRESS.md as the only progress file and defers
  architecture-informed delivery plans.
- Next available decision ID: **D-067**.

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-08-27 | Documentation architecture normalization | Reviewed all repository documentation and the complete changed-file set; ran git diff --check; validated relative Markdown links, required/forbidden file boundaries, 12 required P0 plus one SP0-1 and 13 acceptance blocks, continuous D-001–D-066, required Stage 4 state coverage, balanced fences, and preservation of historical verification/session content | Passed; detailed planning now has purpose-specific authoritative homes, PROJECT_PROGRESS.md remains the only progress tracker, deferred architecture/delivery files are absent, and no application or architecture implementation changed |
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

### 2026-08-27 — Normalize durable planning documentation

- **Objective:** Move detailed approved planning out of the monolithic progress
  tracker into purpose-specific repository memory that can support a fresh
  Architecture task without chat history.
- **Completed:** Created authoritative product plan, user-story backlog, screen
  specification, initial execution plan, and decision history; created a
  comprehensive but explicitly non-authoritative technical reference; updated
  repository working rules and README navigation; reduced PROJECT_PROGRESS.md to
  current status, milestones, blockers, risks, questions, pointers, verification,
  and session history; recorded D-064–D-066.
- **Files changed:** AGENTS.md, PROJECT_PROGRESS.md, README.md. Created
  docs/product/product-plan.md, docs/product/user-stories.md,
  docs/product/screen-spec.md, docs/delivery/execution-plan.md,
  docs/decisions.md, and
  docs/reference/technical-architecture-reference.md. No application,
  architecture, data, cloud, dependency, or UI implementation changed.
- **Verification:** git diff --check passed; all relative Markdown links resolve;
  required closeout files exist; deferred architecture, implementation, test,
  milestone, and duplicate progress files are absent; story and decision sequences
  are complete; key Stage 4 states remain represented; historical verification and
  session content was preserved.
- **Handoff:** Ready for a fresh Architecture planning task using the required
  reading set in AGENTS.md and Current Workstream. No Architecture Lock or
  implementation has begun.

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
