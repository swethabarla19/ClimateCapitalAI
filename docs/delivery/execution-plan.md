# ClimateCapital AI Execution Plan

> **Status:** Approved initial delivery baseline through Product and Design Lock;
> expected to be refined after Architecture Lock
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
- **Required release boundary:** The 12 required P0 stories in
  [user-stories.md](../product/user-stories.md).
- **First scope cut:** Conditional SP0-1 exactly-two-project Compare.
- **P1 rule:** Begin no P1 work unless required P0 is complete at least 24 hours
  early and at least 10 contingency hours remain.
- **Buffer rule:** A missed gate freezes or cuts scope; it does not consume the
  testing and submission-recovery buffer.
- **Cost rule:** Favor a small, bounded MVP and low ongoing Google Cloud spend.
  Cloud choices remain an Architecture-stage decision.

## Stage and Dependency Order

| Order | Stage | Required outcome | Status |
| ---: | --- | --- | --- |
| 1 | Deadline and success definition | Deadline, capacity, audience assumption, demo length, and success bar | Complete and locked |
| 2 | Product definition | User, problem, value, scope, historical context, terminology, goals, and non-goals | Complete and locked |
| 3 | Backlog definition | Required P0, conditional SP0-1, P1/Later, and acceptance intent | Complete and locked |
| 4 | Product and Design Lock | Screens, navigation, behavior, states, recovery, wireframes, and demo sequence | Complete and locked |
| 5 | Documentation normalization | Purpose-specific durable memory and fresh-task handoff | Complete |
| 6 | Architecture planning and lock | Investigated and explicitly approved architecture, data design, cloud cost plan, and lineage | Not started |
| 7 | Evidence readiness | Sources, cohort, vintages, geometry, scoring, confidence, optimization, and supported metrics | Not started |
| 8 | Implementation and test planning | Milestones, implementation plan, test plan, and architecture-informed execution refinement | Not started |
| 9 | Required-P0 implementation | Integrated deterministic and UI/Gemini functionality inside the locked boundary | Not started |
| 10 | Release, QA, demo, and submission | Deployed release candidate, validation, rehearsal, freeze, and verified submission | Not started |

Architecture planning must read the approved product/design specifications and
technical reference, investigate alternatives, and obtain an explicit Architecture
Lock. Only then should the approved architecture files be created/finalized.

After Architecture Lock, a fresh delivery-planning task should produce or refine:

- implementation-plan.md
- test-plan.md
- execution-plan.md
- milestones.md

PROJECT_PROGRESS.md remains the sole actual progress tracker; no delivery progress
file is permitted.

## What Must Happen Before Implementation

1. Approve the Architecture Lock, including system boundaries, data design, cloud
   cost controls, and data lineage.
2. Resolve evidence decisions that affect eligibility, displayed metrics, scoring,
   ranking, confidence, optimization, comparison, and map defaults.
3. Create architecture-informed implementation milestones and a test plan tied to
   required-P0 acceptance criteria and release gates.
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
- **September 4 — Demo gate:** Map → Projects → Portfolio → governed change →
  explanation fits three minutes and expands coherently to five.
- **September 5 — Final freeze:** Submission content and artifacts are complete;
  only submission-blocking fixes remain permissible.
- **September 6 — Submission gate:** Submit between 9:30 and 11:30 a.m. CDT and
  verify every final link, retaining at least 22.5 hours for recovery.

These are release-level gates, intentionally separate from story-level acceptance
criteria.

## Sequencing Rules

- Resolve evidence and analytics risk before presenting analytical claims.
- Do not let implementation choices reopen locked product or UX decisions silently.
- Keep individual ranking and constrained optimization separate in implementation,
  tests, and demo.
- Build required deterministic/manual paths before relying on Gemini.
- Treat Historical City Recommendation comparison as isolated descriptive data.
- Preserve the last successful deterministic result during failed or infeasible
  scenario attempts.
- Do not begin P1 or Later functionality while required P0 or contingency is at
  risk.
- Use the recovery day only for a slipped prerequisite gate, not elective scope.
- Update PROJECT_PROGRESS.md after every meaningful milestone and update an
  authoritative specification only when an approved change legitimately affects
  it.

## P0 Delivery Boundary

Required P0 includes the complete governed Map → Projects → Portfolio journey,
transparent eligibility/evidence/ranking, full-project constrained portfolio,
Historical Benchmark, one active What-If, manual and approved Gemini scenario
proposal paths, grounded explanations, current-session Reviewed Draft, provenance,
accessibility, and recovery behavior.

It excludes saved scenarios, accounts, collaboration, export, formal approvals,
manual plan membership, partial funding, full mobile support, broader Gemini
analysis, advanced GIS, and P1/Later categories.

## Major Execution Risks and Responses

| Risk | Delivery response |
| --- | --- |
| Required P0 exceeds remaining capacity | Cut SP0-1 first; freeze new scope; protect QA and submission buffers. |
| Evidence or cohort is weaker than expected | Preserve rule-derived results and explicit limitations; never curate for demo appeal. |
| Methodology decisions arrive late | Do not hard-code arbitrary criteria; resolve the evidence gate before analytical implementation. |
| Architecture work expands | Prefer the smallest deployable design that satisfies locked P0 and cost constraints; defer optional infrastructure. |
| Gemini work threatens core completion | Complete deterministic and manual paths first; Gemini failure must degrade locally. |
| Map geometry is incomplete | Preserve synchronized non-map paths and label unavailable geometry. |
| Scenario errors overwrite valid results | Keep attempted inputs unapplied and preserve the last successful confirmed result. |
| Official submission details remain unknown | Verify organizer artifacts and judge/demo expectations before final package planning. |
| Cloud cost is uncertain | Require explicit cost assumptions, budgets/alerts or equivalent safeguards, and low-idle-cost evaluation in Architecture planning. |

## Architecture Handoff

A fresh Architecture task should begin by reading:

1. [Repository instructions](../../AGENTS.md)
2. [Current project status](../../PROJECT_PROGRESS.md)
3. [Product plan](../product/product-plan.md)
4. [User stories](../product/user-stories.md)
5. [Screen specification](../product/screen-spec.md)
6. This execution plan
7. [Decision history](../decisions.md)
8. [Technical architecture reference](../reference/technical-architecture-reference.md)

The task should investigate and propose architecture. It must not treat the
technical reference as an approved design or create/finalize approved architecture
files before explicit Architecture Lock.

## Planned Later Delivery Documents

The following are intentionally absent until the Architecture Lock makes them
decision-complete:

- implementation-plan.md
- test-plan.md
- milestones.md

The architecture directory and its approved documents are likewise intentionally
absent until Architecture Lock. No docs/delivery/progress.md will be created.
