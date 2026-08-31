# ClimateCapital AI Decision History

> **Status:** Authoritative durable decision log
> **Last updated:** 2026-08-31
> **Rule:** Existing IDs are immutable and may not be renumbered. New decisions use
> the next sequential ID. A decision remains active unless this file explicitly
> marks it superseded and links the replacement.

## How to Use This Log

PROJECT_PROGRESS.md reports current state and highlights decisions relevant to the
active milestone. This file preserves the detailed historical record.

The original D-001–D-063 records contained date, decision, rationale, and status.
They did not consistently record alternatives or separate consequence fields.
This normalization preserves those records without inventing missing deliberation.
Explicitly recoverable alternatives and consequences are summarized after the
table. Detailed active constraints are also expressed in the authoritative product
and delivery specifications.

## Decisions

| ID | Date / stage | Decision | Rationale | Status |
| --- | --- | --- | --- | --- |
| D-001 | 2026-08-24 / Repository continuity | Use `PROJECT_PROGRESS.md` as the canonical cross-session handoff. | A single maintained source of truth reduces context loss between sessions. | Active; clarified by D-064 |
| D-002 | 2026-08-24 / Repository continuity | Keep a current-state summary plus an append-only session history. | Future sessions need both a fast restart point and traceability. | Active |
| D-003 | 2026-08-24 / Early product definition | Use Map → projects → portfolio as the primary P0 journey. | The product should begin interactively, collect user inputs, and then recommend a portfolio from eligible projects. | Active |
| D-004 | 2026-08-24 / Early product definition | Limit P0 to watershed projects; treat parks as a candidate P1 project type. | This keeps the first release focused while leaving room for category expansion. | Active |
| D-005 | 2026-08-24 / Early product definition | Lead P0 with flood evidence and social vulnerability; show urban heat only as context or a labeled co-benefit where defensible. | This keeps the watershed pilot coherent and evidence-based while preserving a credible multi-hazard expansion story. | Active |
| D-006 | 2026-08-25 / Stage 1 | Treat September 7, 2026 at 10:00 a.m. CDT as the official submission deadline and September 6, 9:30–11:30 a.m. CDT as the internal submit window. | The earlier internal window provides 22.5 hours for submission recovery. | Active |
| D-007 | 2026-08-25 / Stage 1 | Plan against 40 hours per week and a finalist-worthy, deployed, tested P0 with a three-minute core demo expandable to five. | Scope must prioritize completion and clarity over feature count. | Active |
| D-008 | 2026-08-25 / Stage 1 | Define the primary user as a representative capital planning analyst who recommends but does not authorize funding. | This persona credibly needs maps, comparison, constrained portfolios, transparent evidence, and plain-language explanations. | Active |
| D-009 | 2026-08-25 / Stage 2 | Use January 21, 2026 as the historical decision snapshot because it corresponds to Austin's 2026 Bond Initial Draft Project Recommendation. | The date establishes the decision context and is not an arbitrary product date. | Active |
| D-010 | 2026-08-25 / Stage 2 | Use the $125 million Projects sub-envelope within the historical $160 million Watershed allocation as the P0 ClimateCapital Historical Baseline Scenario constraint. | The P0 cohort contains individually named project requests; other Watershed allocations are outside this portfolio rather than unallocated funds. | Active |
| D-011 | 2026-08-25 / Stage 2 | Distinguish Historical City Recommendation, ClimateCapital Historical Baseline Scenario, and analyst-created What-If Scenarios everywhere in the product. | Clear names, status, and provenance prevent historical outcomes from being mistaken for ClimateCapital recommendations or user-created runs. | Active |
| D-012 | 2026-08-25 / Stage 2 | Isolate the Historical City Recommendation as a descriptive benchmark that never influences ClimateCapital eligibility, evidence, scoring, ranking, weights, or portfolio selection. | This prevents outcome leakage and preserves analytical integrity. | Active |
| D-013 | 2026-08-25 / Stage 2 | Apply documented eligibility rules to derive the candidate cohort; retain 15–30 only as an expected range. | Candidate selection must be reproducible and must not be tuned for an attractive demo. | Active |
| D-014 | 2026-08-25 / Stage 2 | Use full-project inclusion or exclusion in P0 and disclose that partial funding is intentionally out of scope. | A clear binary assumption keeps the historical portfolio decision understandable without implying operational indivisibility. | Active |
| D-015 | 2026-08-25 / Stage 2 | Keep individual project ranking separate from constrained portfolio optimization. | A high-ranking project can be excluded when another combination better satisfies the active envelope and objective. | Active |
| D-016 | 2026-08-25 / Stage 2 | Treat January 21 as the bond decision context, not a universal date requirement for external evidence; show each source and vintage explicitly. | Defensible evidence may require datasets from different relevant publication periods. | Active |
| D-017 | 2026-08-25 / Stage 2 | Limit scenario changes to budget and approved weights; Gemini may propose changes, but the analyst must review and confirm before deterministic recalculation. | This preserves human control and keeps scoring, ranking, constraints, and portfolio outcomes authoritative and reproducible. | Active |
| D-018 | 2026-08-25 / Stage 2 | Defer scoring criteria, default weights, confidence methodology, and the final eligible cohort count beyond Stage 2. | These choices require later evidence and requirements work and must not be implied by the Stage 2 lock. | Active |
| D-019 | 2026-08-25 / Stage 2 | Lock Stage 2 decisions as constraints for subsequent planning unless material source evidence contradicts them. | Later stages should refine the product without silently reopening approved product context. | Active |
| D-020 | 2026-08-25 / Git checkpoint | Create a local documentation checkpoint after Stage 1 and locked Stage 2, before beginning Stage 3. | The approved product context needs a recoverable baseline before backlog planning continues. | Active |
| D-021 | 2026-08-25 / Git checkpoint | Publish the documentation checkpoint to the public `swethabarla19/ClimateCapitalAI` GitHub repository on `main`. | The remote checkpoint provides durable off-device recovery and a visible project history before Stage 3. | Active |
| D-022 | 2026-08-25 / Deadline planning | Pull the deadline plan ahead of UX definition and plan approximately 65–70 hours across six flexible workdays per week. | Early milestone constraints make the remaining product scope and tradeoffs concrete. | Active |
| D-023 | 2026-08-25 / Deadline planning | Complete the Product and Design Lock by August 27 evening. | UX ambiguity must be removed before implementation-readiness and evidence work. | Active; achieved |
| D-024 | 2026-08-25 / Deadline planning | Resolve analytics and evidence risk before integrated feature work. | Eligibility, scoring, confidence, and source support determine whether the product can make defensible claims. | Active |
| D-025 | 2026-08-25 / Deadline planning | Freeze required P0 features by September 2 evening. | A fixed scope protects deployment, QA, demo rehearsal, and submission contingency. | Active |
| D-026 | 2026-08-25 / Deadline planning | Respond to a missed gate by freezing or cutting scope, not by reducing the testing buffer. | A smaller verified product is more credible than a larger untested submission. | Active |
| D-027 | 2026-08-25 / Deadline planning | Start no P1 work unless required P0 is complete at least 24 hours early and at least 10 contingency hours remain. | This prevents optional breadth from jeopardizing the submission. | Active |
| D-028 | 2026-08-26 / Stage 3 | Treat exactly-two-project comparison as conditional stretch P0 and the first scope cut. | It can improve analyst understanding but is not necessary to prove the core portfolio journey. | Active |
| D-029 | 2026-08-26 / Stage 3 | Use distinct labels for the Historical Decision Snapshot, Historical City Recommendation, ClimateCapital Historical Baseline Scenario, and analyst-created What-If Scenario. | The snapshot is context, the City result is a benchmark, and the two ClimateCapital scenarios are analytical results with different input provenance. | Active |
| D-030 | 2026-08-26 / Stage 3 | Apply binary full-project inclusion/exclusion only to ClimateCapital P0 scenarios and preserve published City treatment and amounts separately. | ClimateCapital's simplifying assumption must not rewrite or mischaracterize the historical record. | Active |
| D-031 | 2026-08-26 / Stage 3 | Allow either a reviewed ClimateCapital Historical Baseline Scenario portfolio or a confirmed active What-If portfolio to be designated as the current-session draft. | The analyst needs to carry forward the reviewed choice without implying persistence or official approval. | Active |
| D-032 | 2026-08-26 / Stage 3 | Permit one atomic Gemini proposal to coordinate multiple approved-weight changes when needed for a valid configuration. | Weight constraints may require coupled changes, while atomic review preserves analyst control. | Active |
| D-033 | 2026-08-26 / Stage 3 | Do not make missing display geometry alone an eligibility failure. | Analytical eligibility and map display capability are different concerns; inventing geometry is unacceptable. | Active |
| D-034 | 2026-08-26 / Stage 3 | Expose excluded source records and reasons without assuming every excluded record is an individual project. | The eligibility audit must accurately represent heterogeneous source material. | Active |
| D-035 | 2026-08-26 / Stage 3 | Defer the exact score-breakdown and normalization structure to the evidence and methodology gate. | Stage 3 can require transparency without pre-judging unsupported analytical design. | Active |
| D-036 | 2026-08-26 / Stage 3 | Use the capital planning analyst as the sole P0 product persona. | One coherent decision workflow is achievable before the deadline; stakeholder-specific workflows remain out of scope. | Active |
| D-037 | 2026-08-26 / Stage 3 | Keep calendar, demo-duration, deployment, and zero-critical-defect gates separate from story-level acceptance criteria. | Release readiness and user behavior are different test layers and should remain traceable. | Active |
| D-038 | 2026-08-26 / Stage 3 | Maintain one immutable ClimateCapital Historical Baseline Scenario and at most one active What-If Scenario in P0. | This supports meaningful exploration without introducing saved-scenario management. | Active |
| D-039 | 2026-08-26 / Stage 3 | Preserve the bounded map, provenance, City benchmark, copilot, Parks P1, and accessibility commitments in the prioritized backlog. | These commitments distinguish the product while respecting the approved pilot boundaries. | Active |
| D-040 | 2026-08-26 / Stage 3 | Require structured manual budget and approved-weight controls and route them through the same validation and deterministic engine as Gemini proposals. | The core scenario workflow cannot depend on AI availability or create divergent analytical paths. | Active |
| D-041 | 2026-08-26 / Stage 3 | Treat draft acceptance as a current-session designation, not a persisted copy; replacing an accepted What-If clears the designation after warning. | This provides a clear end state without adding accounts, storage, versioning, or false workflow semantics. | Active |
| D-042 | 2026-08-26 / Stage 3 | Define Historical City Recommendation as the published January 2026 City Initial Recommendation and use City-specific inclusion terminology. | This preserves historical meaning and prevents City treatment from being confused with ClimateCapital selection. | Active |
| D-043 | 2026-08-26 / Stage 3 | Lock the Stage 3 backlog and acceptance criteria as constraints for Stage 4 and later planning unless material source evidence contradicts them. | Subsequent stages should define the experience and implementation without silently expanding or reopening approved scope. | Active |
| D-044 | 2026-08-26 / Stage 4 | Use Explore and Funding Plan as required primary decision destinations; keep Compare conditional SP0-1. | The smallest coherent P0 needs spatial inspection and a dedicated portfolio workspace, while comparison remains the first deadline cut. | Active |
| D-045 | 2026-08-26 / Stage 4 | Keep Explore map-dominant with a synchronized compact Recommended Projects list and presentation-only search, sorting, and filters. | The map should lead the spatial story without allowing display controls to change analytical results. | Active |
| D-046 | 2026-08-26 / Stage 4 | Use one shared Project Detail component with distinct map-marker and Recommended Projects row entry paths. | Marker clicks need a lightweight preview, while row clicks can open detail directly; both paths must preserve Explore state and converge on the same evidence. | Active |
| D-047 | 2026-08-26 / Stage 4 | Use context-dependent Gemini prominence and shared contextual regions. | Proactive spatial interpretation adds value on Explore, while Funding Plan and project contexts need bounded, optional explanations without permanent chat. | Active |
| D-048 | 2026-08-26 / Stage 4 | Evidence-gate optional metrics and drive low-confidence warnings only from the approved methodology and threshold. | The UI must not invent metrics, confidence judgments, or missing-as-zero interpretations. | Active |
| D-049 | 2026-08-26 / Stage 4 | Preserve optimizer-controlled Funding Plan membership with no manual project override. | P0 scenarios change only budget and approved weights, preserving deterministic portfolio authority. | Active |
| D-050 | 2026-08-26 / Stage 4 | Use one dedicated Funding Plan workspace with a progressive-disclosure Scenario Settings drawer and supported deltas from the immutable Historical Baseline. | The portfolio, governed scenario editing, and comparison need enough space while Explore remains focused. | Active |
| D-051 | 2026-08-26 / Stage 4 | Keep Historical Benchmark as a secondary Funding Plan view. | The published City recommendation is useful descriptive context but is not the current scenario, a target, or an analytical input. | Active |
| D-052 | 2026-08-26 / Stage 4 | Use in-place Reviewed Draft confirmation and bind review state to the exact current-session deterministic result. | This creates a clear demo end state without persistence, approval workflow, or false official status. | Active |
| D-053 | 2026-08-26 / Stage 4 | Use a narrow primary sidebar plus a header showing decision context, current confirmed scenario, and Available Budget. | Persistent context prevents the analyst from confusing the current result with historical references while preserving workspace width. | Active |
| D-054 | 2026-08-26 / Stage 4 | Place the eligibility audit and analytical chain on one anchored Data & Methodology page. | A single traceable source supports provenance without expanding P0 into a separate audit workspace. | Active |
| D-055 | 2026-08-26 / Stage 4 | Group Funding Plan candidates into Recommended and Not Included sections. | The analyst must see both portfolio membership outcomes while keeping individual Funding Priority separate. | Active |
| D-056 | 2026-08-26 / Stage 4 | Keep Help & Resources as a compact quick guide linked to detailed methodology. | Required orientation and limitations need a discoverable home without duplicating the full evidence documentation. | Active |
| D-057 | 2026-08-26 / Stage 4 | Use explicit, non-generic UI state categories and contain recoverable failures to the affected surface. | Zero matches, no eligible cohort, missingness, infeasibility, and system errors have different meanings and recovery paths. | Active |
| D-058 | 2026-08-26 / Stage 4 | Preserve the last successful deterministic Funding Plan across later failed or infeasible recalculation attempts. | Unapplied scenario changes must never overwrite or masquerade as the current confirmed result. | Active |
| D-059 | 2026-08-26 / Stage 4 | Distinguish the presentation-filter match count from the rule-derived eligible-cohort count everywhere. | Filtering changes visibility only and must not appear to change analytical eligibility. | Active |
| D-060 | 2026-08-26 / Stage 4 | Treat every value and name shown in Stage 4 low-fidelity wireframes as an illustrative placeholder. | UX examples must not preempt evidence decisions or become implementation constants. | Active |
| D-061 | 2026-08-26 / Stage 4 | Reaffirm structured Gemini-generated scenario proposals as an already-approved P0 capability. | P0-9, D-032, and D-040 already authorize bounded proposals for budget and approved weights with analyst confirmation and deterministic execution. | Active |
| D-062 | 2026-08-26 / Stage 4 | Keep the Layers control and popover closed by default without deciding default analytical-layer visibility in Stage 4. | Progressive disclosure governs the controls, while the evidence stage must determine the defensible default visualization. | Active |
| D-063 | 2026-08-26 / Stage 4 | Label the header with the current confirmed scenario while keeping the immutable Historical Baseline and Historical Benchmark conceptually separate. | The analyst must distinguish the active result, the baseline reference for supported deltas, and the descriptive City comparison. | Active |
| D-064 | 2026-08-27 / Documentation closeout | Adopt a purpose-specific repository-memory hierarchy: AGENTS.md for working rules, PROJECT_PROGRESS.md for current status/handoff, docs/product for approved product/design, docs/delivery for delivery plans, docs/reference for non-authoritative reference, and docs/decisions.md for decision history. | Fresh tasks must reconstruct approved context from the repository without relying on chat memory, while detailed specifications should not be duplicated in the progress tracker. | Active |
| D-065 | 2026-08-27 / Documentation closeout | Treat technical-architecture-reference.md as exploratory reference only and create/finalize approved docs/architecture files only after explicit Architecture Lock. | Consolidating technical considerations must not silently approve a system design or preempt Architecture investigation. | Active |
| D-066 | 2026-08-27 / Documentation closeout | Keep PROJECT_PROGRESS.md as the only progress/status file; do not create docs/delivery/progress.md, and create/refine implementation, test, execution, and milestone plans after Architecture Lock. | One progress source avoids drift, while architecture-informed delivery documents provide durable milestone specifications. | Active |
| D-067 | 2026-08-31 / Architecture planning | Pause Architecture Planning before Architecture Lock and perform authoritative-source evidence reconnaissance across the 37 official Austin Watershed projects as a controlled dependency-resolution step, not a new project phase or product reset. | Geometry, hazard, exposure, engineering, expected flood-reduction benefit, equity joins, identifiers, and vintages must be tested against real project-level evidence before the architecture can safely fix processing boundaries and analytical contracts. | Active |
| D-068 | 2026-08-31 / Evidence reconnaissance | Establish the November 21, 2025 Watershed bond-project memo as the source from which to derive and preserve the 37-project reconnaissance universe, while preserving the January 21, 2026 Initial Draft Recommendation through a structurally separate benchmark-only path. | A stable official source universe supports complete project-by-project evidence auditing, while structural benchmark isolation prevents historical recommendation outcomes from leaking into ClimateCapital eligibility or analysis. | Active |
| D-069 | 2026-08-31 / Source-ingestion foundation | Use a Git-tracked canonical source registry for source/vintage/provenance metadata and ignored deterministic local staging paths for immutable raw response bytes; record exact-byte SHA-256 and UTC retrieval time, refuse differing historical-snapshot overwrites, and keep bucket names and credentials outside source metadata and code. | This is the smallest reproducible provenance foundation that preserves authoritative source bytes without committing raw files or prematurely choosing production pipeline, cloud, architecture, or analytical methodology. | Active |

## Explicitly Recoverable Alternatives and Consequences

Most early decisions did not record alternatives separately. The following
alternatives or consequences are recoverable from the approved planning record:

- **D-003–D-005:** The chosen coherent Watershed flood/equity journey displaced a
  broader multi-category or multi-hazard P0. Parks/heat remain P1 or evidence-gated
  context rather than competing core scope.
- **D-010 and D-014:** Using the $125 million Projects sub-envelope with binary
  inclusion avoids treating other Watershed allocations as spare project funds and
  avoids implying a partial-funding model.
- **D-012:** Historical outcome leakage is prohibited; the City benchmark cannot be
  used to tune or validate ClimateCapital analytical results.
- **D-015:** Rank and portfolio membership require separate artifacts,
  explanations, and tests.
- **D-017, D-032, and D-040:** Natural-language convenience was accepted only with
  structured review/confirmation and parity with the manual deterministic path.
- **D-022–D-027:** Deadline protection takes precedence over optional breadth;
  missed gates cut scope rather than testing/recovery time.
- **D-028:** Compare was considered useful but not necessary for the core story and
  is therefore the first cut.
- **D-033:** A non-map path is mandatory because excluding projects for missing
  display geometry was rejected.
- **D-038 and D-041:** Persisted scenario management and workflow semantics were
  rejected for P0 in favor of one active What-If and current-session review state.
- **D-044–D-056:** A dense all-in-one dashboard was rejected in favor of a minimal
  Explore workspace, dedicated Funding Plan, progressive disclosure, and focused
  methodology/help destinations.
- **D-057–D-059:** Generic empty/error handling was rejected because filter
  matches, eligibility, valid zero-project results, infeasibility, and failures
  have different analytical meanings.
- **D-062:** “Controls closed” was chosen over the incorrect inference that all map
  overlays must be off by default; evidence still determines the visualization.
- **D-063:** Ambiguous “Historical context”/scenario labels were rejected in favor
  of explicit decision context, current confirmed scenario, and separate benchmark
  concepts.
- **D-064–D-066:** A monolithic progress file and a second progress tracker were
  rejected in favor of purpose-specific durable documents plus one canonical
  current-status file.
- **D-067–D-069:** Locking architecture or methodology against assumed project
  evidence was rejected. The project will first test all 37 official source
  projects against authoritative evidence while keeping the later City
  recommendation on a separate benchmark-only path; the first source snapshots are
  governed by a minimal registry, checksum, and immutable-fetch contract.

## Source-of-Truth Links

- [Current status and handoff](../PROJECT_PROGRESS.md)
- [Approved product plan](product/product-plan.md)
- [Approved user stories](product/user-stories.md)
- [Approved screen specification](product/screen-spec.md)
- [Delivery execution plan](delivery/execution-plan.md)
- [Non-authoritative technical reference](reference/technical-architecture-reference.md)
