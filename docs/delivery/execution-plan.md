# ClimateCapital AI Execution Plan

> **Status:** Approved initial delivery baseline, reconciled through Methodology
> and Architecture Locks; expected to be refined by the next delivery-planning task
> **Authority:** This is the current high-level delivery sequencing, deadline, and
> release-gate plan. It is not an implementation plan, test plan, or architectural
> design.

## Delivery Objective

Deliver a deployed, tested, finalist-worthy required-P0 Austin Watershed historical
simulation before the September 7, 2026 submission deadline while protecting
analytical credibility, testing time, and a low Google Cloud cost profile.

## Fixed Constraints

- **Official deadline:** September 7, 2026 at 10:00 a.m. CDT.
- **Internal submission window:** September 6, 2026 from 9:30–11:30 a.m. CDT.
- **Capacity basis:** Approximately 65–70 hours across six flexible workdays per
  week. Stretching beyond that is contingency, not the base plan.
- **Required release boundary:** The 11 required core P0 stories in
  [user-stories.md](../product/user-stories.md); P0-9 proposal is post-core stretch.
- **First scope cut:** Conditional SP0-1 exactly-two-project Compare.
- **Second scope cut:** P0-9 natural-language Funding Plan proposal.
- **P1 rule:** Begin no P1 work unless required P0 is complete at least 24 hours
  early and at least 10 contingency hours remain.
- **Buffer rule:** A missed gate freezes or cuts scope; it does not consume the
  testing and submission-recovery buffer.
- **Cost rule:** Follow the scale-to-zero, bounded Gemini/image/logging, billing-
  control, and post-demo procedures in the Architecture Lock.

## Stage and Dependency Order

| Order | Stage | Required outcome | Status |
| ---: | --- | --- | --- |
| 1 | Deadline and success definition | Deadline, capacity, audience assumption, demo length, and success bar | Complete and locked |
| 2 | Product definition | User, problem, value, scope, historical context, terminology, goals, and non-goals | Complete and locked |
| 3 | Backlog definition | Required P0, conditional SP0-1, P1/Later, and acceptance intent | Complete and locked |
| 4 | Product and Design Lock | Screens, navigation, behavior, states, recovery, wireframes, and demo sequence | Complete and locked |
| 5 | Documentation normalization | Purpose-specific durable memory and fresh-task handoff | Complete |
| 6 | Evidence feasibility and Methodology Lock | Reviewed sources, purpose family, evidence roles, missingness, supported arithmetic, and unsupported metrics | Complete; locked 2026-09-01 |
| 7 | Architecture planning and lock | Investigated and explicitly approved architecture, data design, cloud cost plan, and lineage | Complete; locked 2026-09-01 |
| 8 | Implementation and test planning | Milestones, implementation plan, test plan, and architecture-informed execution refinement | Next; not started |
| 9 | Required-P0 implementation | Integrated deterministic and UI/Gemini functionality inside the locked boundary | Not started |
| 10 | Release, QA, demo, and submission | Deployed release candidate, validation, rehearsal, freeze, and verified submission | Not started |

The approved architecture is authoritative in
[p0-architecture.md](../architecture/p0-architecture.md) and
[data-contracts.md](../architecture/data-contracts.md). A fresh delivery-planning
task should now produce or refine:

- implementation-plan.md
- test-plan.md
- execution-plan.md
- milestones.md

PROJECT_PROGRESS.md remains the sole actual progress tracker; no delivery progress
file is permitted.

## What Must Happen Before Implementation

1. Review the Methodology and Architecture Locks and their Product/Design
   reconciliation.
2. Create architecture-informed implementation milestones and a test plan tied to
   required-P0 acceptance criteria and release gates.
3. Lock the initial artifact, API, session, plan, benchmark, and Gemini schema
   versions identified by the architecture.
4. Confirm the first implementation milestone and the authoritative files it must
   read.
5. Verify official submission requirements and ensure required artifacts fit the
   delivery schedule.

Application implementation is not authorized by completion of this document.

## Initial Deadline Plan

| Date | Planned hours | Milestone or focus |
| --- | ---: | --- |
| Aug 25 | 3 | Deadline-plan reset and scope rules |
| Aug 26 | 8 | Lock Stage 3 backlog; check submission requirements by noon |
| Aug 27 | 8 | Complete Product and Design Lock and documentation normalization |
| Aug 28 | 6 | Architecture/technical execution-readiness in a fresh planning task |
| Aug 29 | 7 | Evidence readiness: sources, cohort, scoring, confidence, and vintages |
| Aug 30 | — | Recovery day; use only if an earlier gate slips |
| Aug 31 | 7 | Analytics core, only after required locks and plans |
| Sep 1–2 | 14 | Integrate required P0 and freeze features by Sep 2 evening |
| Sep 3 | 5 | Produce deployed release candidate |
| Sep 4 | 4 | QA and demo gate |
| Sep 5 | 3 | Final freeze and submission package |
| Sep 6 | 2 | Submit during the internal window and verify final links |

The original approved plan placed technical execution-readiness on August 28.
Following the documentation-architecture correction, that work begins as a fresh
Architecture planning task. This clarifies the handoff without pre-approving a
technical solution.

## Release and Demo Gates

- **September 2 — Feature freeze:** Every required P0 story is integrated.
  Conditional SP0-1 remains optional, and no new behavior begins after this gate.
- **September 3 — Release candidate:** A public deployment completes the required
  P0 journey end to end.
- **September 4 — Quality gate:** Zero known critical defects; accessibility and
  resilience checks pass; every displayed or Gemini-cited number agrees with the
  deterministic outputs.
- **September 4 — Demo gate:** Map → Projects → Funding Plan → governed change →
  explanation fits three minutes and expands coherently to five.
- **September 5 — Final freeze:** Submission content and artifacts are complete;
  only submission-blocking fixes remain permissible.
- **September 6 — Submission gate:** Submit between 9:30 and 11:30 a.m. CDT and
  verify every final link, retaining at least 22.5 hours for recovery.

These are release-level gates, intentionally separate from story-level acceptance
criteria.

## Sequencing Rules

- Lock shared schemas first. Then allow data curation and application development
  to proceed in parallel without presenting fixture state as analytical evidence.
- Do not let implementation choices reopen locked product or UX decisions silently.
- Do not implement Funding Priority, ranking, Importance weights, or optimization.
  Keep analyst membership inputs separate from deterministic validation/arithmetic.
- Build required deterministic/manual paths before required grounded Gemini
  explanation; implement natural-language proposal only post-core.
- Never fetch live source services during a release/deployment build. Final
  integration and release require the reviewed, pinned release-data bundle;
  fixture evidence cannot ship.
- Keep Historical City Recommendation data structurally isolated from project
  evidence, analytical-family definition, analyst membership, validation, and
  scenario arithmetic; expose it only through the descriptive benchmark path.
- Preserve the last successful deterministic result during failed, invalid, or
  over-budget scenario attempts.
- Do not begin P1 or Later functionality while required P0 or contingency is at
  risk.
- Use the recovery day only for a slipped prerequisite gate, not elective scope.
- Update PROJECT_PROGRESS.md after every meaningful milestone and update an
  authoritative specification only when an approved change legitimately affects
  it.

## Architecture-Locked Implementation Dependency Order

1. Create and approve `implementation-plan.md`, `test-plan.md`, and
   `milestones.md`.
2. Lock versioned release-artifact, API, browser-session, Funding Plan, benchmark,
   and Gemini contracts.
3. After schema lock, run two coordinated tracks:

   - **Data track:** focused license/reuse confirmation; controlled pinned
     acquisition; benchmark extraction; Problem Score/FEMA/EAZ evidence and RNA
     display artifacts; final provenance, reconciliation, and reviewed release
     bundle.
   - **Application track:** exact-schema fixture bundle with no invented analytical
     claims; deterministic Funding Plan engine; API contracts; frontend shell and
     session reducer; core manual Funding Plan behavior.

4. Replace fixtures with the reviewed pinned release-data bundle, prove the build
   requires no live source, and block fixture state from the release candidate.
5. Complete the manual core, evidence/provenance, map defaults/non-map paths,
   accessibility, recovery, benchmark isolation, and end-to-end tests.
6. Implement required `POST /api/v1/gemini/explain` with grounding, post-validation,
   kill switch, one-process rate/concurrency controls, and content-free token logs.
7. Build, deploy a no-traffic Cloud Run revision, reconcile code/data/manifest/image
   identity, smoke test, canary one explanation, and promote with rollback.
8. Only if the core release candidate and contingency remain intact, implement
   post-core `POST /api/v1/gemini/propose`.

The detailed authoritative order and release gates are in
[p0-architecture.md](../architecture/p0-architecture.md).

## P0 Delivery Boundary

Required P0 includes the complete governed Map → Projects → Funding Plan journey,
the all-37 purpose audit, transparent evidence roles and missingness, the
provisional derived 12-record P0 analytical family, analyst-controlled full-request
membership only within that active family, deterministic budget
validation/arithmetic, Historical Benchmark, one Session Reference Plan, one active
What-If, manual and bounded Gemini interaction paths, grounded explanations,
current-session Reviewed Draft, provenance, accessibility, and recovery behavior.
The required AI path is grounded explanation after explicit analyst action.

It excludes saved scenarios, accounts, collaboration, export, formal approvals,
partial funding, numeric priority/risk/equity/benefit scores, weights, ranking,
optimization, AI-originated recommendations, full mobile support, broader Gemini
analysis, advanced GIS, P1/Later categories, and natural-language Funding Plan
proposal unless post-core P0-9 is completed without threatening the core candidate.

## Major Execution Risks and Responses

| Risk | Delivery response |
| --- | --- |
| Required P0 exceeds remaining capacity | Cut SP0-1 first and P0-9 proposal second; freeze new scope; protect QA and submission buffers. |
| Evidence or family is weaker than expected | Preserve the derived 12-record family, all-37 audit, and explicit limitations; never add scores or curate for demo appeal. |
| Methodology is implemented incorrectly | Treat `docs/methodology/p0-evidence-methodology.md` as authoritative; verify that no score, weight, rank, optimizer, imputation, or hidden district/geometry substitute appears. |
| Implementation departs from Architecture Lock | Treat `docs/architecture/` as authoritative; reject runtime GIS/BigQuery, fixture release, persistent session, or expanded infrastructure. |
| Gemini work threatens core completion | Complete deterministic/manual paths and required explanation; cut proposal. Gemini failure must degrade locally. |
| Map geometry is incomplete | Preserve synchronized non-map paths and label unavailable geometry. |
| Scenario errors overwrite valid results | Keep attempted inputs unapplied and preserve the last successful confirmed result. |
| Official submission details remain unknown | Verify organizer artifacts and judge/demo expectations before final package planning. |
| Cloud cost or public abuse is uncertain | Enforce scale-to-zero, model limits/kill switch, one worker/max instance, bounded logs/images, existing-control inspection, and post-demo disablement from the Architecture Lock. |

## Post-Architecture Delivery-Planning Handoff

A fresh delivery-planning task should begin by reading:

1. [Repository instructions](../../AGENTS.md)
2. [Current project status](../../PROJECT_PROGRESS.md)
3. [Product plan](../product/product-plan.md)
4. [User stories](../product/user-stories.md)
5. [Screen specification](../product/screen-spec.md)
6. [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
7. This execution plan
8. [Decision history](../decisions.md)
9. [P0 Architecture Lock](../architecture/p0-architecture.md)
10. [P0 data and runtime contracts](../architecture/data-contracts.md)

The task should create the architecture-informed implementation, test, and
milestone plans without reopening the locked methodology, product, architecture,
or source reconnaissance.

## Planned Later Delivery Documents

The following are now the next required planning artifacts and remain intentionally
absent until a separately authorized delivery-planning task:

- implementation-plan.md
- test-plan.md
- milestones.md

The approved architecture documents now exist under `docs/architecture/`. No
`docs/delivery/progress.md` will be created.
