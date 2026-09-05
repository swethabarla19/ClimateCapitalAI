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
| Locked P0 evidence roles, analytical family, missingness, and deterministic Funding Plan method | [docs/methodology/p0-evidence-methodology.md](docs/methodology/p0-evidence-methodology.md) |
| Product vision, scope, principles, workflow, and non-goals | [docs/product/product-plan.md](docs/product/product-plan.md) |
| Prioritized stories and acceptance intent | [docs/product/user-stories.md](docs/product/user-stories.md) |
| Screens, navigation, UI behavior, states, recovery, and wireframes | [docs/product/screen-spec.md](docs/product/screen-spec.md) |
| Initial delivery sequencing, deadline, and release gates | [docs/delivery/execution-plan.md](docs/delivery/execution-plan.md) |
| Durable decision history | [docs/decisions.md](docs/decisions.md) |
| Approved P0 topology, services, deployment, security, observability, cost, and implementation order | [docs/architecture/p0-architecture.md](docs/architecture/p0-architecture.md) |
| Approved release artifacts, runtime APIs, session state, Funding Plan, benchmark, and Gemini contracts | [docs/architecture/data-contracts.md](docs/architecture/data-contracts.md) |
| Superseded pre-lock technical planning reference | [docs/reference/technical-architecture-reference.md](docs/reference/technical-architecture-reference.md) |
| Approved architecture-informed implementation and test plans | [docs/delivery/implementation-plan.md](docs/delivery/implementation-plan.md), [docs/delivery/test-plan.md](docs/delivery/test-plan.md), and [docs/delivery/milestones.md](docs/delivery/milestones.md) — M0 and M1 explicitly approved 2026-09-02; M2A and M2B explicitly approved 2026-09-03; M3 explicitly approved 2026-09-03 |

Git is the version history for all repository memory. Fresh tasks must not depend on
access to prior chat conversations.

## Current Snapshot

- **Last updated:** 2026-09-04
- **Project stage:** M3.5 governed analytical universe, M3.6 structural cross-category dataset, M3.7A Watershed PRB reconciliation, M3.7B Watershed PRB model eligibility, M3.7C Watershed Funding Priority methodology, and M3.7E cross-category PRB evidence/model eligibility have completed implementation and verification. M3.7E checkpoint approval is pending.
- **Current milestone:** M3.7E — cross-category PRB reconciliation and model eligibility for all 106 analytical projects; implementation and verification complete, checkpoint approval pending.
- **Next gate:** Approve, commit, and publish M3.7E, then audit whether official PRB Grand Total is analytically comparable enough across all four presentation categories to authorize one cross-category Funding Priority. Portfolio optimization remains deferred until that comparability gate is resolved.
- **Delivery context:** The completed/deployed application remains the delivery goal. This analytical-methodology reopening does not change Product, Architecture, evidence provenance, or historical-snapshot authority.
- **Working state:** Git repository is on `main`. M3.7C is committed and published to `origin/main` at `fe29765`. M3.7E scripts, governed artifacts, tests, and documentation are local pending approval. Unrelated `.node-version` and `frontend/` work remain outside the M3.7E checkpoint.
- **Data/methodology state:** The governed universe contains 106 analytical projects: Transportation 9, Parks & Open Space 22, Watershed 37, and Community Facilities 38. M3.7E-A reconciles 106/106 to complete official six-component PRB vectors with valid Grand Totals, preserving three source/request-version conflicts and three legitimate half-point projects. M3.7E-B proves 106/106 evidence-feasible and model-eligible for `CROSS_CATEGORY_PRB_PROJECT_MODEL`; 86 eligible projects have no January recommendation. Governed model-request authority totals $1,973,520,000.
- **Runtime boundary:** M3.7E establishes evidence feasibility and scoped model eligibility only. `cross_category_ranking_authorized=false`, `portfolio_selection_authorized=false`, and `runtime_integration_authorized=false`. Cross-category PRB-score comparability must be resolved before ranking or optimization.
- **M3 runtime state:** The approved FastAPI runtime remains unchanged. Existing health/bootstrap/plan/benchmark APIs and the M2B deterministic evaluator retain their approved semantics while M3.7 analytical-methodology work is resolved.
- **Most recent verification:** M3.7E focused tests: 25 passed. Combined M3.7A/B/C/E regression: 69 passed. Full repository: 276 passed plus 137 subtests. `pip check` reports no broken requirements. All three M3.7E generated artifacts regenerate identically as `unchanged`. One known Starlette TestClient/AnyIO deprecation warning remains non-blocking.

## Approved Locks

- **Stage 1 — Deadline and success:** Official deadline September 7, 2026 at
  10:00 a.m. CDT; internal submit window September 6 from 9:30–11:30 a.m. CDT;
  finalist-worthy deployed/tested P0; three-minute core demo expandable to five.
- **Stage 2 — Product definition:** Capital planning analyst persona, Austin
  Watershed historical simulation, January 2026 context, $125 million Projects
  sub-envelope, full-request treatment, and strict City benchmark isolation remain.
  The former rule-derived cohort, score/rank, weight, and optimizer implications
  are superseded by Methodology Lock.
- **Stage 3 — Backlog:** Twelve required P0 stories, conditional SP0-1 Compare as
  the first cut, ordered P1, Later scope, acceptance intent, and release gates.
- **Stage 4 — Product and Design Lock:** Required screens and contextual surfaces,
  navigation, UI states/recovery, low-fidelity wireframes, evidence gates, and
  three-minute demo sequence remain, reconciled to analyst-controlled Funding Plan
  membership and evidence-first terminology.
- **Methodology Lock — Evidence-first P0:** All 37 source records remain governed;
  the all-37 purpose classification and provisional 12-record / $143,005,000
  analytical family
  are explicit ClimateCapital derivations; evidence roles and missingness are
  governed; P0 has no Funding Priority score, rank, Importance weights, quantitative
  risk/equity score, expected flood-reduction benefit, or optimizer.
- **Architecture Lock — Minimal reproducible P0:** Controlled source preparation
  produces a reviewed four-file release-data bundle; one small public Cloud Run
  container serves the SPA/API with one worker, no application database, no
  runtime BigQuery/GCS/GIS access, browser-session-only state, independently
  recomputed plan inputs, isolated benchmark, explicit map defaults, keyless
  bounded Gemini, non-circular deployment identity, scale-to-zero cost controls,
  and a reviewed-data release gate.

Unchanged portions of Stages 1–4 remain authoritative. The empirical evidence gate
materially contradicted and reopened the optimizer-authoritative assumptions; the
historical record and exact replacements are preserved in docs/decisions.md. Full
current detail is in docs/methodology and docs/product.

The evidence-driven reopening does not change ClimateCapital AI, the Austin
Watershed P0 pilot, January 21, 2026 context, Map → Projects → Funding Plan journey,
full-request treatment, benchmark isolation, current-session plan limit,
Reviewed Draft, accessibility, or recovery behavior. It narrows deterministic
authority to facts, evidence states, validation, arithmetic, and supported
comparison; the $125 million figure is historical/default context, not eligibility.

## Current Workstream

- **Goal:** Close M3.7E cross-category evidence feasibility and model eligibility
  without conflating eligibility with cross-category score comparability.
- **Status:** M3.7E-A and M3.7E-B implementation and verification are complete;
  explicit checkpoint approval, commit, and publication remain.
- **Owner:** User and implementation tooling.
- **Analytical boundary:** All 106 analytical projects now have reconciled official
  PRB component evidence and a usable governed request. This authorizes scoped
  model eligibility only.
- **Explicit exclusions:** No cross-category Funding Priority, analytical tie-break,
  portfolio objective, optimizer, runtime activation, or use of January
  recommendation as an analytical input.
- **Parallel repository note:** Existing untracked `.node-version` and `frontend/`
  work belongs to a separate application track and must not enter the M3.7E
  checkpoint.
- **Exit condition:** M3.7E documentation and staged-file audit are clean, the
  checkpoint receives explicit user approval, and only M3.7E files are committed
  and pushed.

## Next Actions

1. Complete the M3.7E governance documentation and staged-file audit.
2. Obtain explicit M3.7E checkpoint approval before commit/push.
3. Commit and publish only the M3.7E files; keep `.node-version` and `frontend/`
   outside the checkpoint.
4. Audit cross-category PRB Grand Total comparability before authorizing a single
   Funding Priority across all 106 projects.
5. Define portfolio optimization methodology only after the comparable ranking
   evidence and governing budget/policy constraints are established.

## Active Implementation Checkpoint

### 2026-09-03 — M3 implementation checkpoint; awaiting explicit re-audit/approval

- **Runtime/API implementation:** Added a local FastAPI application with startup
  runtime loading, `/healthz`, bootstrap, deterministic plan evaluation, isolated
  benchmark retrieval, and benchmark comparison. The plan endpoint delegates to
  the approved M2B evaluator rather than introducing a second analytical engine.
- **Startup boundary:** Core manifest/catalog/map identity, bytes, checksums,
  release-tier/data-version relationships, and map/catalog geometry availability
  agreement are validated before the core API becomes usable. A corrupt core
  artifact fails startup.
- **Benchmark isolation:** Benchmark loading is structurally separate so benchmark
  corruption/unavailability returns a local `503` on benchmark surfaces while
  health/bootstrap/Funding Plan remain usable. Benchmark comparison receives only
  a freshly server-evaluated valid plan; benchmark data never enters the M2 plan
  engine.
- **HTTP contract:** API namespace uses the locked `/api/v1` value. Contract/data
  conflicts, malformed/unknown input, oversized request bodies including
  chunked/no-Content-Length bodies, optional dependency failure, and unexpected
  errors are handled through bounded typed responses. Semantic plan
  `VALID`/`OVER_BUDGET`/`INVALID` results remain normal parsed endpoint responses.
- **Preserved semantics:** No score, rank, optimizer, recommendation, expected
  benefit, beneficiary estimate, geometry-derived membership, or fabricated
  evidence was introduced. Missing geometry does not remove a project, and
  `5789.150` remains citywide and featureless.
- **Files/components:** `requirements-application.txt`;
  `backend/climatecapital/api/`; `backend/climatecapital/benchmark/`;
  `backend/climatecapital/main.py`; and
  `tests/application/test_m3_api.py`.
- **Dependencies:** Added `fastapi==0.128.2` and `uvicorn==0.48.0`. No cloud,
  frontend, Gemini, data-source, database, or infrastructure work occurred.
- **Verification:** 17 focused M3 tests; 71 application tests plus 23 subtests;
  41 release tests plus 20 subtests; 159 full-repository tests; 22 schema checks;
  `pip check`; and `git diff --check` all pass.
- **Known issue/risk:** Starlette TestClient currently emits one AnyIO
  `BlockingPortal` deprecation warning under Python 3.14. It is dependency-level,
  non-failing, and does not alter the M3 runtime contract.
- **Git state:** M3 changes remain local and uncommitted. Nothing has been staged,
  committed, or pushed for M3.
- **Approval state:** M3 received explicit user approval on 2026-09-03.
- **Boundary:** Approval recording does not authorize commit/push or silently begin M4.
  Gemini, reviewed-data integration, container/deployment, and later work remain out of scope.

### 2026-09-03 — M2A/M2B approved closure checkpoint

- **M2A:** Approved controlled prerequisites preserve the governed 37-project /
  $327,970,000 universe, exact source provenance, historical fit, limitations,
  conservative `UNVERIFIED` reuse states, and controlled acquisition boundaries.
  RNA remains 15/37 exact matches overall and 5/12 within the analytical family;
  geometry remains research-only and has no membership authority.
- **M2B fixture:** Approved persistent four-file `FIXTURE` contains exact all-37
  purpose/confidence semantics, uses `NOT_EVALUATED_FIXTURE` for deferred RNA
  curation, preserves `5789.150` as citywide/non-project geography, invents no
  geometry, and attributes Problem Score, FEMA, EAZ, and RNA evidence to their
  correct governed sources.
- **M2B evaluator:** Approved deterministic server-side evaluator resolves governed
  requests only from the validated catalog, enforces the exact 12-project family,
  evaluates all current/reference inputs independently, produces only supported
  arithmetic/fingerprint/delta outputs, and contains no score, rank, optimizer,
  recommendation, or geometry-derived membership authority.
- **Source authority correction:** FEMA and Problem Score composite local snapshots
  use immutable snapshot-manifest identities; EAZ uses the exact governed feature
  payload. Sources with approved GCS pins remain exact-pin enforced; sources
  explicitly governed without a GCS object cannot fabricate one.
- **Final verification:** 54 application tests, 41 release tests, 142 total tests,
  22 schema checks, `pip check`, and `git diff --check` all pass.
- **Approval:** User explicitly approved M2A and M2B on 2026-09-03.
- **Boundary:** Working tree remains uncommitted. No M3 API, frontend, reviewed
  release bundle, Gemini integration, container, or deployment work has begun.

## Completed Milestones

- **2026-09-03 — M3 Core APIs explicitly approved and complete:** Implemented
  local FastAPI startup/runtime loading, `/healthz`, bootstrap, deterministic
  current/reference plan evaluation, isolated benchmark retrieval/comparison,
  typed HTTP errors, and bounded request-body enforcement. The API reuses the
  approved M2B evaluator, keeps benchmark dependency one-way, preserves local
  benchmark failure containment, and introduces no scoring/ranking/optimizer,
  fabricated evidence, frontend, Gemini, database, source-service runtime access,
  cloud mutation, container, or deployment work. Final verification passed 17
  focused M3 tests, 71 application tests plus 23 subtests, 41 release tests plus
  20 subtests, 159 full-repository tests, 22 schema checks, dependency integrity,
  and `git diff --check`. User explicitly approved M3 on 2026-09-03. The approved
  working tree remains uncommitted pending separate commit/push authorization.

- **2026-09-03 — M2A controlled data prerequisites and M2B fixture/deterministic
  engine explicitly approved and complete:** Preserved and reconciled the approved
  benchmark, RNA, FEMA FloodPro layer 8, EAZ 2021, and Problem Score documentary
  inputs with explicit provenance, historical-fit, limitations, and conservative
  reuse status. Built the conspicuous four-file development fixture without
  invented analytical claims or geometry and implemented the deterministic
  server-authoritative Funding Plan evaluator. Closure corrections fixed exact
  purpose/confidence semantics, deferred RNA state, fixture Git visibility,
  contextual evidence provenance, composite-source authority, and persistent
  regression coverage. Final verification passed 54 application tests, 41 release
  tests, 142 full-repository tests, 22 schema checks, dependency integrity, and
  `git diff --check`. No M3, frontend, Gemini, deployment, or reviewed-release
  implementation began before approval.

- **2026-09-02 — M1 contract and validator milestone approved and complete:** Added the
  pinned Python 3.14.7/Pydantic 2.13.5 contract environment, centralized initial
  versions, strict artifact/API/session/plan/benchmark/Gemini Pydantic models, 22
  deterministic JSON Schemas, a schema generator/checker, and the fail-closed
  four-file release validator/CLI. After independent audit, corrected exact all-37
  identity/fact enforcement, evidence-type semantics, authoritative source pins
  and provenance, evaluated-plan uniqueness/exact arithmetic, independently
  available benchmark fields and comparison contracts, closed endpoint response
  payloads and cross-language dictionary schemas, optional/duplicated identity
  semantics, and stale confirmed/reviewed browser state. A second audit then
  corrected schema parity, exact fingerprint truth, derived comparison fields,
  and API release-tier agreement. Added 64 focused tests; 110 total tests pass.
  The independent closure audit returned A — APPROVE M1 with no changes required.
  No release bundle, plan engine, runtime API, frontend, source acquisition,
  cloud, authority, or decision change occurred, and no M2 work began.
- **2026-09-02 — M0 delivery-plan gate explicitly approved:** Approved
  `implementation-plan.md`, `test-plan.md`, `milestones.md`, and the reconciled
  `execution-plan.md` as the delivery baseline subordinate to Product, Methodology,
  Evidence, and Architecture. Recorded approval status only; no contract,
  application, dependency, cloud resource, commit, push, or M1 work changed.
- **2026-09-02 — P0 Architecture Lock persisted after 2026-09-01 approval:** Locked the
  source-to-release flow, four-file reviewed data bundle, non-circular deployment
  identity, single-worker Cloud Run topology, browser session model, exact plan
  trust boundary, benchmark isolation, map/OSM defaults, required Gemini
  explanation and post-core proposal scope, rate/cost/security/observability
  controls, verification gates, parallel implementation tracks, and cut order;
  reconciled the durable handoff without application, cloud, commit, or push work.
- **2026-09-01 — P0 Methodology Lock completed and reviewed:** Closed the final
  evidence-feasibility gate; preserved the 37-project governed universe and derived
  all-37 purpose audit; locked the 12-record local flood/local drainage family;
  classified Problem Score, RNA/FloodPro, expected benefit, and EAZ evidence by
  role and historical fit; removed unsupported scores/weights/ranking/optimization;
  and reconciled Product/Design to analyst-controlled scenarios and deterministic
  budget arithmetic without application, architecture, cloud, or push changes.
- **2026-09-01 — Live RNA layer-8 geometry reconnaissance completed:** Preserved a
  stable 577-feature native ArcGIS JSON snapshot with exact-byte and semantic
  fingerprints, exact numeric-token ID handling, native CRS/geometry audit, and
  create-only generation-verified GCS storage; tested all 37 governed IDs and
  retained 15 single matches, 22 zero matches, and no multiple matches without
  inferring historical validity, eligibility, exposure, or benefit.
- **2026-08-31 — Raw BigQuery ingestion and quality checkpoint completed:**
  Reviewed and hardened the manual loader without replacing its core approach;
  verified the existing `us-central1` table's exact schema and 37 rows; passed 21
  independent SQL checks including $327,970,000, full source sequence, row-level
  spot checks, and an ordered semantic fingerprint; changed no existing cloud
  data, dataset configuration, IAM, architecture, methodology, or benchmark state.
- **2026-08-31 — Official 37-project source universe extracted:** Added a pinned
  data-only PDF parser, checksum-gated fail-closed extractor, deterministic tracked
  CSV, and source-verified tests; reconciled 37 unique records and $327,970,000
  across row amounts, the table total, and memorandum request; preserved source
  order and made no eligibility, GIS, analytical, benchmark, or cloud change.
- **2026-08-31 — Two raw source snapshots preserved in Cloud Storage:** Confirmed
  local and registry checksums, authenticated project/bucket access, absence of both
  destination objects, and create-only upload support; uploaded exactly two PDFs;
  verified sizes, generations, and generation-specific streamed SHA-256 values;
  changed no infrastructure, IAM, bucket settings, credentials, BigQuery, or
  analytical state.
- **2026-08-31 — Minimal source-ingestion foundation implemented:** Added the
  canonical source registry, deterministic immutable local fetcher, Git protections,
  and validation tests; downloaded and independently reconciled both authoritative
  PDFs; performed no extraction, upload, BigQuery work, cloud provisioning,
  architecture, methodology, or application work.
- **2026-08-31 — Architecture Lock paused for evidence reconnaissance:** Preserved
  the approved product/design boundary, identified evidence comparability as an
  Architecture dependency, and established the 37-project authoritative-source
  reconnaissance sequence before Architecture Planning resumes.
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

The approved September 2 feature-freeze gate remains at critical schedule risk.
M1 is approved and complete, and every post-schema data/
application milestone and the reviewed release, manual core, Gemini explanation,
and deployment remain unstarted.

## Blockers

- Official judging criteria, submission artifacts, and conditional live-demo
  details remain unconfirmed. They urgently block submission-dependent work and
  final submission-package planning. They did not block M1 and do not silently
  authorize or redefine either post-schema track.

## Active Risks

- Source-license/reuse terms remain explicitly `UNVERIFIED` for the governed
  sources, including RNA, FEMA layer 8, EAZ 2021, and Problem Score documentary
  context. The focused review and canonical metadata agree; reviewed-release use
  remains blocked until supported confirmation exists, without broad source
  reconnaissance or invented verification.
- RNA Projects layer 8 and the current FloodPro services do not establish their
  January 2026 geometry/data state. RNA geometry is research-only for governed
  analysis; FEMA is current contextual hazard evidence only.
- Twenty-two of the 37 governed projects, including 7/12 local-drainage family
  records, have no exact ID geometry match in the captured live RNA snapshot.
  Missing geometry is not evidence of low need and does not remove a family record.
- Three of the 15 exact-ID GIS matches have non-identical project names. Names were
  retained as evidence but did not affect matching; project identity still needs
  source-specific review wherever later analytical use is contemplated.
- Layer-8 features are source polygons in ESRI:102739/EPSG:2277. The acquisition
  preserves them without transformation, simplification, curve densification, or
  repair, and polygon semantics have not been validated as project footprints or
  benefit areas.
- Fully Developed FloodPro contains relevant invalid source geometries, remains
  research-only, and is not shipped in P0; repaired geometry must not become
  governed source truth.
- Problem Score project/problem association strength is provenance, not severity,
  and no reproducible January 2026 Local Flood numeric score covers the family.
- EAZ 2021 is a 2019-ACS-based Austin Transportation vulnerability snapshot with
  defensible project-level location context for only 5/12 family records. It is not
  current-2026 vulnerability or a project-beneficiary measure.
- Project 5789.150 is a citywide renewal program. Treating it like one discrete
  footprint would create false location, hazard, vulnerability, or beneficiary
  precision.
- BigQuery does not enforce project-ID uniqueness, source sequence, totals, or the
  semantic fingerprint as table constraints. The loader refuses an existing table,
  but any separately authorized mutation by another tool or user requires rerunning
  the durable SQL quality suite before the raw snapshot is trusted.
- The local Python 3.12 installation has no default CA bundle configured; verified
  HTTPS succeeded only when `SSL_CERT_FILE=/etc/ssl/cert.pem` selected the host CA
  bundle. Certificate verification was not disabled.
- Comparable project-level expected flood-reduction evidence is unsupported for
  P0; project/floodplain intersection cannot substitute for benefit evidence.
- Project identifiers, geometry, engineering evidence, hazard evidence, exposure,
  and equity joins may be inconsistent across sources or valid only for different
  historical vintages.
- The source says projects are sorted by project ID, but published row order places
  5789.150 before 5789.145 and 5789.146. Extraction preserves rather than repairs
  this source-level inconsistency.
- The current delivery remains at critical schedule risk: M1 is approved and
  complete, while the reviewed release-data bundle, plan/API/
  frontend behavior, manual core, required Gemini explanation, and deployment do
  not yet exist.
- Required P0 remains ambitious for the September 2 feature freeze; optional scope
  must not erode testing or recovery time.
- Post-schema data/application implementation is now on the critical path and must
  preserve the locked narrow method, M1 contracts, and topology without reopening
  evidence reconnaissance.
- Product language or contracts could silently reintroduce a Funding Priority,
  ranking, Importance weights, optimizer, recommendation, or missing-evidence
  penalty even though no defensible objective supports them.
- Analyst-controlled membership could be misrepresented as a ClimateCapital or
  City recommendation; provenance and confirmation labels must remain explicit.
- The Historical Decision Snapshot, Historical Envelope, Historical City
  Recommendation, Current Confirmed Plan, and Session Reference Plan may be
  confused if the locked terminology is not implemented consistently.
- Gemini or map work could consume disproportionate effort; deterministic/manual
  paths, non-map access, and required grounded explanation remain release
  priorities; proposal is post-core stretch.
- A fixture bundle could be mistaken for reviewed evidence. Release validation
  must reject fixture tier and `NOT_EVALUATED_FIXTURE` states.
- M1 deliberately has no positive reviewed-bundle test because the approved test
  plan reserves that evidence for the reviewed M5 bundle. The validator is proven
  against narrow temporary technical objects and material negative paths; final
  reviewed bytes and source-license completion remain later release gates.
- The M1 machine source-authority map remains the release allowlist for the three
  exactly pinned/GCS-preserved sources. The canonical registry now also carries
  three M2A sources with composite or locally preserved snapshot metadata; their
  presence does not make them release-approved, and bundle-internal source
  registration remains forbidden.
- M2A/M2B producers must consume the exact M1 schemas. A field/meaning/enum change
  requires the locked contract change-control path rather than producer-specific
  relaxation or an unversioned compatibility shortcut.
- A release build could accidentally contact mutable sources. Build verification
  must prove it consumes only pinned reviewed artifacts.
- In-memory Gemini limits reset on process restart and per-client/IP protection is
  best-effort; they reduce public-abuse cost but are not a hard spend guarantee.
- Direct OSM tiles create an external demo dependency and policy obligation;
  attribution, normal Referer/cache behavior, no prefetch/bulk use, configurable
  provider, noindex/robots discouragement, and neutral fallback are mandatory.
- Code/data/manifest/image identity could drift unless `/healthz`, the Cloud Run
  revision, external manifest checksum, and deployed image digest reconcile before
  traffic promotion.
- Failed recalculation must not overwrite the last successful deterministic result.
- The process-job Stop hook still exits with code 127 because node is unavailable;
  process-job completion checks remain unreliable until its runtime/configuration is
  fixed.
- Cloud pricing and service behavior were checked for Architecture Lock but remain
  time-sensitive; quotas, organizer program requirements, existing billing
  controls, Spend Cap availability, and source licensing require focused
  implementation/deployment-time confirmation.

## Open Questions

### Evidence and methodology

- No evidence or methodology decision remains open for P0. Source licensing/reuse
  remains unverified operational metadata, not a reason to broaden reconnaissance.
- Any later metric proposal requires an explicit methodology revision documenting
  source, vintage, historical fit, coverage, comparability, missingness,
  transformation, and effect; it is not part of the current handoff.

### Architecture

- No P0 Architecture decision remains open. The approved topology, data/runtime
  contracts, map defaults, Gemini boundary, cost controls, verification, and
  dependency order are in `docs/architecture/`.
- Delivery planning must instantiate those contracts without introducing a new
  architecture choice. Any material topology/trust/persistence change requires an
  explicit sequential Architecture decision.

### Submission

- What are the official submission artifacts, judging criteria, finale date, and
  live-demo format?

There are no unresolved P0 scoring, weighting, ranking, optimization, or evidence-
imputation decisions. Existing Stage 4 screen/navigation structure remains locked;
its evidence-driven terminology and Funding Plan behavior are reconciled in
docs/product.

## Technical Map

### Architecture

Established and locked:

- one React/TypeScript/Vite SPA plus Leaflet and one FastAPI/Uvicorn application
  worker in one public request-billed Cloud Run service, `us-central1`, minimum 0
  and maximum 1 instances;
- one reviewed four-file release-data bundle packaged in the image; controlled
  acquisition is separate and release builds make no live source requests;
- no runtime BigQuery, Cloud Storage, GIS, application database, or server session
  store; browser `sessionStorage` holds bounded current-session workflow state;
- independently recomputed current/reference Funding Plans with exact integer
  arithmetic, isolated Historical Benchmark, and no client-authoritative results;
- direct configurable OSM with required safeguards; RNA display geometry on where
  available, FEMA/EAZ off by default, no Fully Developed FloodPro, and no fabricated
  `5789.150` geography;
- required bounded Gemini explanation through the global standard on-demand
  publisher endpoint and ADC; proposal is post-core stretch; and
- external manifest checksum plus separate code/data/image release identity,
  bounded observability/images/costs, no-traffic verification, and rollback.

See [p0-architecture.md](docs/architecture/p0-architecture.md) and
[data-contracts.md](docs/architecture/data-contracts.md). The technical reference
is preserved as superseded pre-lock material.

### M1 Contract and Release-Validator Foundation

Implemented, independently audited, and approved on 2026-09-02:

- `.python-version` and `requirements-application.txt` pin Python 3.14.7 and the
  only M1 application dependency, Pydantic 2.13.5;
- `backend/climatecapital/contracts/` centralizes the initial version identifiers
  and strict common, artifact, plan, session, API-envelope, benchmark, and Gemini
  models;
- `contracts/schemas/` contains 22 deterministic generated JSON Schemas whose
  bytes are checked against the Python models;
- `backend/climatecapital/release/validator.py` and
  `scripts/release/validate_bundle.py` validate the exact four-file set,
  deterministic JSON bytes, strict schemas, external manifest checksum, artifact
  sizes/checksums, exact governed source-row semantics, repository-authoritative
  source pins/provenance, governed/family/evidence/map/benchmark reconciliation,
  forbidden fields, and release tier; and
- The original M1 tests continue to use narrow temporary objects. The later M2B
  work adds a conspicuous persistent fixture and direct fixture regressions; no
  reviewed bundle is present in the repository.

### Evidence Repository

The minimal foundation is established:

- data/metadata/source_registry.csv — canonical Git-tracked source metadata for
  the two authoritative PDFs, RNA, FEMA FloodPro layer 8, EAZ 2021, and Problem
  Score documentary context, with explicit roles, historical fit, retrieval,
  checksum/inventory boundaries, and conservative reuse state. Registry presence
  does not by itself confer reviewed-release authority.
- data/metadata/m2a/source_reuse_review.csv — focused six-source reuse review;
  RNA, FEMA, EAZ, and Problem Score are explicitly `UNVERIFIED` because preserved
  metadata does not establish reuse permission for the exact bytes.
- scripts/data/fetch_sources.py — standard-library HTTPS fetcher with deterministic
  paths, PDF-byte validation, exact-byte persistence, and overwrite refusal.
- tests/test_source_ingestion.py — registry, checksum, HTTPS, metadata-update, and
  immutable-snapshot validation.
- requirements-data.txt — pinned local data-tool dependency declaration containing
  only pypdf 6.16.2.
- scripts/data/extract_watershed_projects.py — checksum-gated fail-closed extractor
  for the November named-project table; it records 1-based physical PDF pages,
  preserves published source order and strings, reconciles totals, and refuses
  differing-artifact overwrite.
- data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv —
  Git-tracked nine-column, 37-record official source universe; presence in this
  artifact does not establish analytical eligibility.
- tests/test_watershed_project_extraction.py — source-verified row-association,
  boundary, anomaly, schema, reconciliation, failure-path, and deterministic-output
  validation.
- requirements-cloud.txt — pinned local BigQuery client declaration containing
  only google-cloud-bigquery 3.44.0.
- scripts/data/load_watershed_projects_bigquery.py — exact-artifact and CSV-contract
  preflight plus explicit-schema, `us-central1`, `WRITE_EMPTY` raw loader; it
  refuses an existing target and validates schema/location/count after creation.
- tests/test_watershed_bigquery_loader.py — non-destructive local checks for target,
  schema, encoding, header, artifact checksum, location, overwrite refusal, and
  post-load metadata validation.
- sql/quality/watershed_projects_raw_checks.sql — 21 read-only warehouse checks
  covering schema, identity, completeness, totals, strings, source-specific row
  associations, and the full ordered semantic fingerprint.
- scripts/data/fetch_rna_projects_gis.py — layer-8-only native ArcGIS JSON
  acquisition and create-only GCS preservation CLI with exact numeric-token
  parsing, frozen pre/post OBJECTID checks, schema/CRS/geometry audits, raw and
  semantic fingerprints, and generation-specific cloud-byte verification.
- scripts/data/match_watershed_projects_rna.py — deterministic exact-ID matcher
  covering the complete governed source universe, preserving explicit zero- and
  multi-match states and reconciling governed project counts and request dollars.
- tests/test_rna_projects_gis_reconnaissance.py — focused source-fidelity,
  Decimal-ID, OBJECTID consistency, geometry/CRS, manifest, matching,
  reconciliation, create-only GCS, cloud-byte, and tracked-artifact validation.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/20260901T183323Z/manifest.json —
  Git-tracked acquisition manifest for the immutable native snapshot; the ID is a
  UTC retrieval timestamp, not a source vintage.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/20260901T183323Z/gcs_receipt.json —
  Git-tracked GCS object generations, byte sizes, local checksums, and independently
  streamed generation-specific cloud checksums; the receipt itself is not uploaded.
- data/reconnaissance/city_austin/rna_projects/layer_8/20260901T183323Z/project_id_geometry_matches.csv —
  Git-tracked 37-project exact-ID match artifact with 15 single matches, 22 zero
  matches, and no multiple matches in the captured live snapshot.
- data/staging/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf —
  ignored local raw source-universe snapshot.
- data/staging/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf —
  ignored local benchmark-only snapshot.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf#1788210198102506 — verified cloud source-universe snapshot, 1,151,348 bytes, SHA-256 `d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e`.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf#1788210202820922 — verified cloud benchmark-only snapshot, 412,820 bytes, SHA-256 `da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359`.
- climatecapital-ai.raw.watershed_projects_2025_11_21 — source-faithful BigQuery
  raw table in `us-central1`, with 37 REQUIRED-schema rows and 21 passing SQL
  quality checks.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/ —
  six create-only raw/provenance objects (`service.json`, `layer.json`, pre/post
  OBJECTID responses, `features.arcgis.json`, and `manifest.json`) whose exact
  local bytes were verified against generation-specific cloud streams.

The ordered raw-table schema is `source_id STRING REQUIRED`,
`source_pdf_page INTEGER REQUIRED`, `source_table_row_order INTEGER REQUIRED`,
`map_label STRING REQUIRED`, `subproject_id STRING REQUIRED`,
`project_name STRING REQUIRED`,
`current_funding_request_estimate_source STRING REQUIRED`,
`current_funding_request_estimate_dollars INTEGER REQUIRED`, and
`council_districts_source STRING REQUIRED`.

The 37 official source rows above have been extracted, loaded only to the raw
table, and tested against one immutable live/current GIS snapshot. No GIS match is
an eligibility result, and the snapshot does not establish January 2026 geometry.
The all-37 purpose classification and exact provisional 12-record P0 analytical
family are documented derivations in the Methodology Lock; they are not persisted
analytical tables or a City taxonomy. No flood/exposure/benefit score, optimization result,
staging/curated table, or benchmark table has been created. Benchmark isolation
remains explicit.

### Repository Structure

- AGENTS.md — repository rules and task-start routing.
- PROJECT_PROGRESS.md — sole current state/progress/handoff document.
- README.md — repository landing page and documentation map.
- docs/methodology/p0-evidence-methodology.md — authoritative locked P0 evidence
  roles, family, missingness treatment, and deterministic Funding Plan method.
- docs/product/product-plan.md — approved product-level Product and Design Lock.
- docs/product/user-stories.md — authoritative prioritized backlog and acceptance
  intent.
- docs/product/screen-spec.md — authoritative UI, state, and wireframe specification.
- docs/delivery/execution-plan.md — initial approved delivery sequencing and gates.
- docs/delivery/implementation-plan.md — approved lock-preserving implementation
  sequence and milestone write surfaces.
- docs/delivery/test-plan.md — approved architecture-required verification layers,
  story traceability, and release rules.
- docs/delivery/milestones.md — approved M0–M10 dependency, acceptance, cost, and
  stop gates.
- docs/decisions.md — authoritative durable decision history.
- docs/architecture/p0-architecture.md — authoritative P0 topology, source/release
  flow, services, runtime, deployment, security, observability, cost, verification,
  implementation order, and scope cuts.
- docs/architecture/data-contracts.md — authoritative release artifact, manifest,
  deployment identity, API, browser-session, Funding Plan, benchmark, and Gemini
  contracts.
- docs/reference/technical-architecture-reference.md — superseded pre-lock
  planning reference retained for history.
- .gitignore — raw/staging, PDF, GeoJSON, temporary-response, Python, and common
  credential-file protections.
- requirements-data.txt — pinned dependency for local source extraction only.
- requirements-cloud.txt — pinned BigQuery client dependency for the manual raw
  load/checkpoint workflow only.
- data/metadata/source_registry.csv — canonical source and provenance registry.
- data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv —
  tracked official source-universe extraction.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/ — tracked
  timestamped GIS acquisition manifests and post-upload GCS receipts.
- data/reconnaissance/city_austin/rna_projects/layer_8/ — tracked timestamped
  complete-universe project-ID/geometry match artifacts.
- scripts/data/fetch_sources.py — minimal reproducible source downloader.
- scripts/data/extract_watershed_projects.py — deterministic source-universe
  extractor and reconciliation CLI.
- scripts/data/load_watershed_projects_bigquery.py — guarded raw BigQuery loader.
- scripts/data/fetch_rna_projects_gis.py — immutable layer-8 acquisition and
  create-only verified GCS upload CLI.
- scripts/data/match_watershed_projects_rna.py — complete-universe exact-ID GIS
  matcher and governed funding reconciliation CLI.
- sql/quality/watershed_projects_raw_checks.sql — read-only warehouse data-quality
  suite.
- tests/test_source_ingestion.py — lightweight source-ingestion validation suite.
- tests/test_watershed_project_extraction.py — source extraction and failure-path
  validation suite.
- tests/test_watershed_bigquery_loader.py — non-destructive raw-loader contract and
  safety tests.
- tests/test_rna_projects_gis_reconnaissance.py — native source, provenance,
  matching, reconciliation, and cloud-preservation tests.
- data/metadata/source_snapshots/austin_floodpro_fema_layer_8_live/,
  data/metadata/source_snapshots/austin_equity_analysis_zones_2021/, and
  data/metadata/source_snapshots/austin_wpd_problem_score_documentary_context/ —
  controlled local snapshot manifests with exact response inventories, evidence
  roles, historical-fit limits, and reuse state.
- scripts/data/fetch_fema_floodplain_gis.py,
  scripts/data/fetch_eaz_2021_gis.py, and
  scripts/data/fetch_problem_score_sources.py — controlled acquisition commands
  for the bounded M2A inputs; release/runtime builds do not invoke them.
- docs/delivery/implementation-plan.md, test-plan.md, and milestones.md — approved
  together as the M0 delivery baseline on 2026-09-02.
- .python-version — exact M1 application Python runtime pin.
- requirements-application.txt — exact direct M1 application dependency pin.
- backend/climatecapital/contracts/ — initial strict contract constants/models and
  deterministic schema export.
- backend/climatecapital/release/ — fail-closed four-file bundle validator.
- contracts/schemas/ — 22 generated versioned JSON Schemas.
- scripts/release/generate_schemas.py — generate/check tracked schema bytes.
- scripts/release/validate_bundle.py — reviewed-release-default validator CLI with
  an explicit development-fixture mode.
- release-data/fixture/ — conspicuous four-file M2B development fixture; not a
  reviewed release.
- backend/climatecapital/plans/ — deterministic M2B Funding Plan evaluator.
- tests/application/ and tests/release/ — contract, evaluator, validator, and
  direct persistent-fixture tests.

Local branch: main. Public GitHub remote:
https://github.com/swethabarla19/ClimateCapitalAI.git.

### Environments and External Services

- Verified Google Cloud context: configured project `climatecapital-ai`, active
  gcloud authentication and ADC, and existing raw-data bucket
  `gs://climatecapital-ai-raw-swetha/`. The existing `raw` BigQuery dataset and
  `watershed_projects_2025_11_21` table were inspected in `us-central1`; the table
  has the exact governed schema and 37 rows. Six create-only objects for the
  20260901T183323Z RNA layer-8 snapshot were added under the authorized raw-data
  prefix and independently verified from generation-specific streams. No existing
  cloud object, infrastructure, IAM, dataset/bucket setting, or credential was
  changed; staging, curated, and benchmark datasets/tables were not inspected.
- Current local data runtime verified with Python 3.14.7, pypdf 6.16.2, and
  google-cloud-bigquery 3.44.0 in the ignored `.venv`. BigQuery access used local
  ADC; no credential material is stored in the repository. The earlier Python 3.12
  source-fetch runtime lacked a default CA bundle; `/etc/ssl/cert.pem` was used for
  verified HTTPS without disabling certificate verification.
- The M1 application contract environment is pinned to Python 3.14.7 and Pydantic
  2.13.5 in the ignored `.venv`; dependency integrity passes. No application server
  or frontend environment exists. Frontend package-manager/runtime setup remains
  deferred to M4, the first frontend application work unit.
- No Cloud Run, Artifact Registry, Cloud Build, runtime IAM, Gemini configuration,
  billing-control, or deployment change has been made; the Architecture Lock is
  documentation only.
- The local process-job Stop hook lacks the node runtime it expects.

### Common Commands

- git status --short --branch — verify working tree and upstream.
- git log --oneline --decorate --max-count=8 — inspect checkpoints.
- git diff --check — validate documentation whitespace.
- python3 -m venv .venv — create the ignored local data-tool environment.
- .venv/bin/python -m pip install -r requirements-data.txt — install the pinned
  local data-extraction dependency.
- .venv/bin/python -m pip install -r requirements-cloud.txt — install the pinned
  BigQuery client dependency in the same ignored environment.
- .venv/bin/python -m unittest discover -s tests -v — run ingestion, extraction,
  reconnaissance, M1 contract, and release-validator validation.
- .venv/bin/python -m unittest discover -s tests/application -v — run the focused
  strict application-contract suite.
- .venv/bin/python -m unittest discover -s tests/release -v — run the focused
  release-validator suite.
- .venv/bin/python scripts/release/generate_schemas.py --check — prove the 22
  tracked schemas exactly match the Pydantic contracts.
- .venv/bin/python scripts/release/validate_bundle.py BUNDLE_DIR
  --manifest-sha256 SHA256 — fail-closed reviewed-release validation; the explicit
  `--development-fixture` flag is test/development-only.
- .venv/bin/python scripts/data/extract_watershed_projects.py — verify the source
  checksum, extract/reconcile the 37 rows, and create or confirm the deterministic
  source-universe CSV.
- .venv/bin/python scripts/data/load_watershed_projects_bigquery.py — create the raw
  table only when absent; current reruns refuse the existing historical target.
- SSL_CERT_FILE=/etc/ssl/cert.pem .venv/bin/python
  scripts/data/fetch_rna_projects_gis.py acquire --max-attempts 3 — acquire a new
  UTC-timestamped layer-8 native snapshot after frozen-OBJECTID consistency,
  source-contract, numeric-ID, geometry, and manifest validation.
- .venv/bin/python scripts/data/match_watershed_projects_rna.py --snapshot-id
  20260901T183323Z — create or confirm the deterministic complete-universe exact-ID
  match artifact and funding reconciliation for the preserved snapshot.
- .venv/bin/python scripts/data/fetch_rna_projects_gis.py upload --snapshot-id
  20260901T183323Z --bucket gs://climatecapital-ai-raw-swetha/ — preserve the
  validated raw snapshot create-only and write/confirm the Git-tracked
  generation-specific verification receipt; requires existing authenticated
  gcloud access.
- bq --project_id=climatecapital-ai query --use_legacy_sql=false
  --location=us-central1 < sql/quality/watershed_projects_raw_checks.sql — rerun the
  read-only warehouse quality suite using local authenticated tooling.
- python3 scripts/data/fetch_sources.py — fetch both registered sources when the
  Python environment has a working default CA bundle.
- SSL_CERT_FILE=/etc/ssl/cert.pem python3 scripts/data/fetch_sources.py — verified
  fetch command for the current local Python installation.
- Add verified setup, test, lint, build, migration, and deploy commands only when
  tooling exists.

## Decision Summary

The authoritative history is [docs/decisions.md](docs/decisions.md).

- D-001–D-063 preserve all Stage 1–4 and repository decisions.
- D-064 establishes the purpose-specific repository-memory hierarchy.
- D-065 keeps the technical reference non-authoritative; D-080–D-096 fulfill the
  explicit Architecture Lock requirement.
- D-066 keeps PROJECT_PROGRESS.md as the only progress file and defers
  architecture-informed delivery plans.
- D-067's evidence pause is fulfilled; evidence and Methodology Lock completed
  before Architecture resumed and locked.
- D-068 establishes the 37-project source-universe path and structurally separate
  Historical City Recommendation benchmark path.
- D-069 establishes the canonical registry and immutable raw-fetch/provenance
  contract without selecting a production pipeline or architecture.
- D-070 establishes create-only two-object cloud preservation with independent
  generation-specific SHA-256 verification.
- D-071 establishes checksum-gated, fail-closed, source-faithful extraction of the
  complete 37-record Watershed reconnaissance universe without deciding analytical
  eligibility.
- D-072 establishes the exact-schema, create-only, independently checked BigQuery
  raw warehouse contract without selecting a production pipeline or analytical
  architecture.
- D-073 establishes live RNA layer 8 as the sole canonical GIS source for this
  bounded work unit, with native immutable acquisition, exact numeric-ID matching,
  explicit missingness, and uncertain historical fit.
- D-074 closes evidence feasibility and governs the four evidence roles and final
  P0 treatment of Problem Score, RNA/FloodPro, expected benefit, and EAZ 2021.
- D-075 preserves the all-37 universe, all-37 derived purpose audit, incoherent
  24-record broad flood family, exact provisional 12-record P0 analytical family,
  and separate citywide treatment for 5789.150.
- D-076 removes unsupported scores, ranks, weights, expected benefit, optimization,
  imputation, missingness penalties, and confidence-as-need.
- D-077 reopens Funding Plan membership to analyst control with deterministic
  validation/arithmetic and non-recommendation terminology.
- D-078 separates the $125 million Historical Envelope from the analyst-created
  Session Reference Plan and Current Confirmed Plan, supports analyst-defined
  Available Budget What-If scenarios, and structurally isolates the Historical
  City Recommendation benchmark.
- D-079 limits Gemini to grounded explanation and confirmed translation of explicit
  analyst commands; it cannot originate facts, membership, or recommendations.
- D-080–D-083 lock the single-container Cloud Run topology, source-independent
  release flow, non-circular four-file bundle identity, and minimal GCS/BigQuery
  treatment.
- D-084–D-087 lock map/OSM defaults, browser-session state, the independent
  current/reference plan trust boundary, and benchmark isolation.
- D-088–D-090 lock required Gemini explanation, post-core proposal, Google Cloud
  publisher/ADC model access, one-process rate/cost controls, narrow APIs, public
  access, and least-privilege configuration.
- D-091–D-095 lock bounded observability, deployment identity, image retention,
  testing/release gates, and normal/abuse/billing/shutdown cost controls.
- D-096 locks post-schema parallel data/application tracks, exact-schema fixture
  constraints, reviewed-data final integration, and the Compare/proposal cut order.
- Next available decision ID: **D-107**.

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-09-03 | M2A/M2B closure-audit correction checkpoint | Corrected only findings 1–5; ran the 17-test focused correction set, application and release suites, full repository suite, schema check, dependency check, diff/status review, fixture tracking/validator checks, and later-scope scan | Passed: 17 focused tests, 54 application tests, 39 release tests, and 140 total tests; 22 schemas match; `pip check` passes. The full suite initially caught an attempted edit to the immutable uploaded RNA manifest; that edit was removed and the generation-verified bytes again pass. Final diff/status/scope checks are clean within M2A/M2B. No evaluator, M3/later implementation, cloud, staging, commit, or push change; M2A/M2B remain unapproved pending re-audit |
| 2026-09-02 | Independent M1 closure approval | Independent closure audit reported by the user after the corrected M1 verification | A — APPROVE M1; no changes required; recommendation to approve and commit M1. Approval recording changes status only and introduces no implementation, authority, reviewed-data, M2, or cloud change |
| 2026-09-02 | Second independent M1-audit correction pass | Corrected only published-schema parity, fingerprint truth, current/reference comparison derivation, and API deployment/artifact release-tier agreement; ran the four focused adversarial tests, application and release suites, full repository tests, deterministic schema check, compilation, dependency integrity, `git diff --check`, scope/authority scans, and final Git inspection | Passed: 4/4 focused regressions, 31 application tests, 33 release tests, and 110 total tests; 22 schemas match generated output; compilation and `pip check` pass; M1 remains unapproved pending re-review; no authority, M2, reviewed data, cloud, stage, commit, or push change |
| 2026-09-02 | Independent-audit M1 correction pass | Recovered unchanged Git state and locked authority; mapped and corrected all ten audit findings; ran 27 focused application-contract tests, 33 focused release-validator tests, the complete repository suite, deterministic schema regeneration/check, Python compilation, dependency integrity, explicit adversarial regressions, authority/scope scans, Markdown checks, `git diff --check`, and final Git state inspection | Passed: 27 application tests, 33 release tests, and 106 total tests; 22 generated schemas match exactly; all requested invalid probes fail and permitted optional/partial cases pass; exact governed identities/facts, source authority/provenance, evidence semantics, canonical plan partitions/arithmetic, benchmark isolation, endpoint-typed responses, and deployment/data session identity now fail closed; no new authority/fact, release bundle, later-milestone surface, cloud action, stage, commit, or push; `pip check` passes |
| 2026-09-02 | Initial M1 contract and fail-closed release-validator checkpoint (superseded by correction row above) | Recovered the complete approved repository baseline; ran focused application and release suites, the full repository suite, deterministic schema generation/check, broad Python compilation, dependency integrity, contract/version/family/boundary assertions, credential and later-scope scans, `git diff --check`, and final Git state inspection | Mechanically passed 12 application-contract tests, 23 release-validator tests, and 81 total tests with 14 generated schemas, but a subsequent independent approval audit found blocking semantic enforcement gaps; this checkpoint was not approved and its enforcement claims are superseded by the corrected M1 verification above |
| 2026-09-02 | Explicit M0 delivery-baseline approval record | Updated approval/status metadata in the four delivery-baseline documents, README routing, and canonical progress handoff; ran `.venv/bin/python -m unittest discover -s tests -v`, Python compilation, `pip check`, relative Markdown link/fence validation, intended-file trailing-whitespace scan, approval-boundary review, full-diff inspection, `git diff --check`, and Git state inspection | Passed: 46 tests; Python compilation passed; no broken requirements; 133 relative links resolve and all fences balance; no trailing whitespace or diff-check error; only approval/gate/status/handoff text changed; M0 is approved and complete, M1 is authorized next but not started; no contract, application, dependency, governed data, cloud, decision, commit, or push change; pip emitted only its existing unwritable-cache warning |
| 2026-09-02 | Corrected M0 delivery package and pre-approval re-audit | Reconciled the delivery sequence to Architecture units 3–5; independently parsed the exact Methodology family table and reconciled it to the governed CSV and RNA match artifact; classified repository-wide Importance/weight/score/rank/optimizer terms; ran `.venv/bin/python -m unittest discover -s tests -v`, Python compilation, `pip check`, semantic assertions for all six original audit findings, relative Markdown link/fence validation, intended-file trailing-whitespace scan, full-diff review, `git diff --check`, and Git state inspection | Passed: 46 tests; exact 12 / $143,005,000 reconciles to governed requests; all-37 is 37 / $327,970,000; GIS remains separate at 15/22 all-37 and 5/7 within the family; all original findings resolved; no stale active analytical mechanic or new contradiction found; 133 relative links resolve and all fences balance; pip emitted only its existing unwritable-cache warning; package remains proposed and M1 remains blocked pending explicit approval |
| 2026-09-02 | Initial draft of M0 architecture-informed delivery plans | Recovered the complete repository and locked documents; inspected Git, manifests, code, tests, scripts, configuration, and governed evidence assets; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, `pip check`, `git diff --check`, intended-file trailing-whitespace checks, relative Markdown link/fence validation, stale delivery-handoff searches, lock-boundary term review, and final Git status/stat inspection | Mechanical checks passed: 46 tests, Python compilation, dependency integrity, 133 resolving relative Markdown links, and balanced fences; a later pre-approval semantic audit found work-order, gate, stale-language, M1-tooling, geometry-test, and authority-wording inconsistencies, so this initial draft was not approval-ready; pip emitted only its existing unwritable-cache warning |
| 2026-09-02 | Final P0 scenario-budget bound correction | Replaced the prior representation-limit maximum with the approved `$0`–`$1,000,000,000` application input bound; searched repository documentation for the obsolete bound; ran the full repository test suite, `git diff --check`, and focused Architecture/Methodology budget-contract assertions | Passed: 46 tests; no obsolete safe-integer bound remains; the application-only limit preserves exact whole-dollar arithmetic, City-policy and eligibility separation, the `$125,000,000` Historical Envelope, and ample headroom above the 37-project / `$327,970,000` governed universe; no application, commit, or push change |
| 2026-09-02 | P0 Architecture Lock | Read the complete governing repository state; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, relative Markdown link/fence checks, D-001–D-096 continuity, stable-story/core-scope checks, exact governed/family CSV-methodology reconciliation, required Architecture contract assertions, stale optimizer/ranking/weights/runtime-GIS/runtime-BigQuery searches, changed-file boundary review, and Git status/stat review | Passed: 46 tests; 12 Markdown files have resolving relative links and balanced fences; 96 decisions are continuous and unique; all 12 stable P0 IDs remain, with 11 required core and P0-9 post-core stretch; 37 / $327,970,000 and exact 12 / $143,005,000 reconcile; stale-term hits are explicit exclusions or preserved superseded history; only the ten authorized documentation files changed or were created; no application, data, cloud, commit, or push change |
| 2026-09-01 | Reviewed Methodology Lock commit gate | Confirmed the exact documentation-only working-tree boundary; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, and staged-scope validation | Passed: 46 tests; only the ten intended methodology, Product/Design, delivery, reference, repository-routing, and current-state Markdown files are included; no application, data, cloud, architecture, or push change |
| 2026-09-01 | Final Methodology Lock semantic audit | Audited Historical Envelope versus analyst plan terminology, Historical City Recommendation isolation, provisional analytical-family versus eligibility language, and active-family/full-request/deterministic-membership boundaries; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, exact source/family/broad reconciliation, obsolete-current-term guards, D-001–D-079 continuity/supersession checks, and Markdown link/fence validation | Passed: 46 tests; $125 million is only Historical Envelope context; Session Reference Plan and Current Confirmed Plan are distinct analyst-plan terms; City benchmark is structurally isolated; 12 projects / $143,005,000 remain a provisional analytical family inside the visible 37-project / $327,970,000 universe; membership is active-family-only and full-request; deterministic logic validates but does not select; no commit or push |
| 2026-09-01 | P0 evidence and Methodology Lock | Reviewed the interrupted working-tree diff and all authoritative handoff files; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, exact CSV/methodology reconciliation, all-37 and family name/ID/request checks, broad-family total check, D-001–D-079 continuity, relative Markdown-link and fence validation, stale-current-language guards, and deferred-file boundary checks | Passed: 46 tests; 37 projects / $327,970,000; exact 12 records / $143,005,000; exact broad 24 / $233,380,000; official names and requests reconcile; 79 continuous unique decisions; 13 Markdown files have valid relative links and balanced fences; no stale optimizer/weight/recommendation contract in current handoff; no application, architecture, cloud, commit, or push change |
| 2026-09-01 | RNA layer-8 GIS reconnaissance | Acquired the live service/layer metadata, frozen pre-ID set, exact feature response, and post-ID set; ran the matcher twice for created/identical behavior; uploaded six create-only objects and streamed each generation-specific cloud object for independent SHA-256; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, `pip check`, manifest/match/receipt reconciliation, `git diff --check`, credential scan, and tracked/ignored status review | Passed: 577/577 stable OBJECTIDs and polygon geometries, exact 11-field schema, native 102739/2277 CRS, no transfer-limit flag, no missing/unexpected IDs, 577 safe numeric ID tokens, no true curves, 15 single/22 zero/0 multiple governed matches, $163,975,000 matched plus $163,995,000 unmatched equals 37 projects and $327,970,000; local/cloud bytes and SHA-256 match for all six objects; no benchmark, BigQuery, infrastructure, IAM, architecture, methodology, commit, or push change |
| 2026-08-31 | Raw BigQuery ingestion and warehouse quality | Inspected dataset/table metadata; ran the final `sql/quality/watershed_projects_raw_checks.sql` in `us-central1`; exercised the loader's existing-target refusal; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, `pip check`, `git diff --check`, credential scan, and tracked/ignored status review | Passed: exact nine-column ordered REQUIRED STRING/INT64 schema; 21/21 warehouse checks; 37 rows and unique IDs; $327,970,000; page/source/order/district/spot checks and semantic SHA-256 match; 29 tests; loader refused the existing table before load submission; no cloud data/configuration or credentials changed |
| 2026-08-31 | Official Watershed source-universe extraction | Verified the raw checksum against the registry; inspected rendered source table pages; ran the extractor twice for created/identical behavior; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, an independent standard-library CSV count/sum/spot-check read, and `git diff --check` | Passed: 19 tests; 37 unique source records; row sum, independently parsed table total, and memorandum program request all equal $327,970,000; first/last, page boundary, multi-district, and 5789.150/5789.145/5789.146 order checks passed; ambiguous structure, checksum mismatch, unparseable row, missing total, and differing-output paths fail closed |
| 2026-08-31 | Two-object Cloud Storage raw preservation | Confirmed local existence, byte sizes, independent SHA-256, and registry agreement; verified configured project, active gcloud auth, ADC, bucket access, initial object 404s, and create-only generation support; uploaded with `--if-generation-match=0`; described both objects; streamed each generation-specific object through independent SHA-256; ran `git diff --check`, credential scan, tracked/ignored status review, and repository-file review | Passed: exactly two objects created at the authorized paths; local, registry, expected, and cloud-streamed SHA-256 values and byte sizes match; generations 1788210198102506 and 1788210202820922 verified; raw PDFs remain ignored/untracked; no credentials, infrastructure, IAM, bucket settings, BigQuery, extraction, commit, or push changed |
| 2026-08-31 | Minimal source-ingestion and provenance foundation | Ran `python3 -m unittest discover -s tests -v`, `python3 -m py_compile`, canonical-registry validation, `wc -c`, independent `shasum -a 256`, PDF file-type inspection, `git diff --check`, trailing-whitespace scan, `git check-ignore`, and tracked/ignored status review; fetched both sources over verified HTTPS using the host CA bundle | Passed: 9 tests; 2 valid registry rows; both HTTP 200 downloads reconciled byte-for-byte to registry checksums; raw PDFs and Python cache files are ignored; no cloud upload, BigQuery load, extraction, architecture, methodology, application, commit, or push occurred |
| 2026-08-31 | Architecture pause and evidence-reconnaissance handoff | Reviewed the complete documentation diff; ran `git diff --check`; confirmed 68 continuous decision rows through D-068, next ID D-069, removal of stale “not started”/“ready” status, and preservation of the Product and Design Lock boundary | Passed; only PROJECT_PROGRESS.md, README.md, and docs/decisions.md changed; no architecture, methodology, source data, pipeline, application, cloud, or approved product specification changed |
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

### 2026-09-03 — Correct M2A/M2B closure-audit findings

- **Objective:** Correct only the five independent closure-audit findings for the
  uncommitted M2A/M2B working set and stop for re-audit without beginning M3.
- **Fixture/contract:** Replaced generic/high purpose assumptions with the exact
  all-37 locked audit, regenerated the four-file fixture at data version
  `m2b-development-fixture-1`, used fixture state for incomplete RNA display
  curation, retained the separate 15/37 and 5/12 RNA evidence, kept `5789.150`
  citywide and featureless, and narrowly reconciled the cross-field contract with
  the already-approved fixture rule. The deterministic evaluator did not change.
- **Tracking/tests:** Added only the precise fixture-map `.gitignore` exception and
  six direct persistent-fixture tests covering governed semantics, coverage,
  citywide treatment, Git visibility/usability, validator modes, and evaluator
  loading.
- **M2A governance:** Reconciled historical-fit and conservative `UNVERIFIED`
  reuse metadata across the canonical registry, focused review, acquisition
  output, and new snapshot manifests for RNA, FEMA layer 8, EAZ 2021, and Problem
  Score context. Preserved the previously uploaded RNA manifest bytes after the
  full suite detected that mutating them would break its verified receipt.
- **Verification:** Passed 17 focused tests, 54 application tests, 39 release
  tests, 140 total tests, 22-schema parity, dependency integrity, and final
  diff/status/scope checks. No staging, commit, push, cloud mutation, M3, frontend,
  Gemini, deployment, refactor, or source research occurred.
- **Handoff:** M2A and M2B are corrected but not approved or complete. Re-audit
  this uncommitted checkpoint before any milestone closure or M3 work.

### 2026-09-02 — Approve and publish M1

- **Objective:** Record the independent closure-audit approval, commit and push
  only the approved M1 scope, and stop before M2.
- **Approval:** The independent closure audit returned A — APPROVE M1 with no
  changes required and recommended approval and commit.
- **Documentation:** Updated only M1 approval/current-status metadata and handoff
  text in this tracker and the four approved delivery documents. No implementation
  contract or validator changed during approval recording.
- **Verification basis:** The approved checkpoint retains its passing four focused
  adversarial regressions, 31 application tests, 33 release tests, 110-test full
  suite, 22-schema deterministic check, compilation, dependency, scope, authority,
  credential, whitespace, and Git-integrity results. Publication uses a final
  lightweight diff, staged-scope, and Git-synchronization sanity check.
- **Boundaries:** No Product, Methodology, Evidence/source-governance,
  Architecture, active-family semantics, reviewed data, application UI, M2, or
  cloud work changed. No decision ID was created.
- **Handoff:** M1 is approved and complete. Begin M2A only in a subsequent
  implementation session and preserve the approved M1 contracts and validator.

### 2026-09-02 — Correct four blockers from the second independent M1 audit

- **Objective:** Correct only schema parity, fingerprint truth, plan-comparison
  derivation, and API release-tier agreement; verify M1; and stop for re-review
  without starting M2 or staging, committing, or pushing.
- **Implementation:** Added explicit Draft 2020-12 constraints for representable
  model-validator invariants: unique plan-membership arrays, exact governed and
  active-family identities, exact evidence-type coverage, locked evidence role/
  fact-kind/availability combinations, and governed active-family request values.
  `EvaluatedPlan` now makes `matches` equal the actual expected/server fingerprint
  comparison. `PlanEvaluationResponseData` recomputes scalar and membership deltas
  from its current/reference results. Bootstrap and benchmark response data now
  require deployment and artifact release tiers to agree.
- **Tests and results:** Added four focused public regressions in
  `tests/application/test_m1_second_audit_regressions.py`; all four pass. The 31
  application tests, 33 release tests, and full 110-test repository suite pass; 22
  schemas regenerate/check deterministically.
- **Schema limitation:** Standard JSON Schema cannot calculate SHA-256, arithmetic
  sums/differences, sibling-field equality, or cross-array set derivation. Those
  invariants remain fail-closed in the authoritative Pydantic/release validators;
  no non-standard schema keyword was invented.
- **Boundaries:** No Product, Methodology, Evidence/source-governance,
  Architecture, active-family meaning, scoring/optimization semantics, Gemini
  authority, reviewed data, runtime API, UI, frontend, source acquisition, or
  GCP/cloud resource changed. No decision ID was created.
- **Handoff:** M1 is corrected but not approved. Stop for re-review and begin no M2
  work until M1 is closed.

### 2026-09-02 — Correct M1 after independent approval audit

- **Subsequent audit:** A second independent audit found four remaining contract
  gaps; this entry is superseded for current M1 status by the correction above and
  remains as session history.

- **Objective:** Correct only the ten independently reported M1 contract and
  release-validator findings, rerun every approved M1 verification, and stop for
  re-review without staging, committing, pushing, or starting later work.
- **Implementation:** Bound the catalog to the existing all-37 governed semantic
  fingerprint and exact active-family requests; bound every evidence type to its
  locked role/fact-kind/availability; encoded the three already registered source
  identities and preserved GCS pins for external validation; reconciled evidence/
  map vintage, historical fit, and transformation versions; rejected duplicate or
  non-canonical evaluated-plan partitions; added independently available benchmark
  values and benchmark-comparison request/response contracts; replaced generic API
  success data with closed endpoint-specific payloads; made documented optional
  fields omittable; enforced duplicate identity/fingerprint agreement; and bound
  confirmed/reference/What-If/Reviewed Draft state to the complete current
  deployment/data identity. The generic non-negative whole-dollar primitive is now
  separate from the scenario-only $1 billion input maximum.
- **Tests and results:** Added public regressions for every audit bypass plus
  explicit BOM, CRLF, final-newline, non-finite-number, symlink, source-vintage,
  transformation, positive current-session, closed-schema, and partial-benchmark
  paths. The 27 application-contract tests, 33 release-validator tests, and all 106
  repository tests pass; 22 generated schemas match exactly; compilation and
  dependency integrity pass.
- **Files/components:** Corrected only M1 contract, release-validator, schema, test,
  and temporary-test-factory files plus this canonical progress handoff. No domain
  authority or durable decision was changed, and no decision ID was created.
- **Deviations and risks:** No scope or authority deviation. As approved, no
  positive reviewed bundle exists before M5; source reuse/license status remains
  explicitly unverified and a later controlled-data gate.
- **Boundaries:** No Product, Methodology, Evidence/source-governance,
  Architecture, active family, scoring/optimization semantics, Gemini authority,
  reviewed data, application UI, frontend tooling, or GCP/cloud resource changed.
- **Handoff:** Stop for corrected M1 re-review. Begin neither M2A nor M2B without
  separate authorization.

### 2026-09-02 — Implement M1 contracts and fail-closed release validation

- **Subsequent audit:** This initial checkpoint was not approved. Its 14-schema/
  35-test verification did not cover all locked semantic bypasses and is superseded
  by the M1 correction entry above; it remains here as session history.

- **Objective:** Recover M1 from the approved repository, implement only the
  initial contract/release-validator foundation, run every applicable M1 check,
  and stop without staging, committing, pushing, or starting later work.
- **Implementation:** Pinned Python 3.14.7 and Pydantic 2.13.5; centralized all
  initial contract versions; added strict Pydantic common/artifact/API/session/
  plan/benchmark/Gemini models; generated 14 deterministic JSON Schemas; added
  geometry-independent plan-membership contract validation; and added a canonical-
  JSON, exact-four-file, external-manifest-checksum release validator and CLI that
  defaults to `REVIEWED_RELEASE` and fails closed.
- **Validation behavior:** Enforced strict primitives/unknown-field rejection,
  exact artifact and cross-file identity, approved/pinned source closure, 37 and 12
  count/dollar/family reconciliation, evidence roles and missingness denominators,
  no geometry membership authority, `5789.150` no-feature treatment, locked map
  layers/defaults, benchmark isolation, forbidden analytical/circular fields, and
  fixture/reviewed-tier separation. No fixed 15/22 geometry count was made a schema
  assumption.
- **Tests and results:** Added 12 application-contract and 23 release-validator
  tests. Focused suites and the full 81-test suite pass; deterministic schema check,
  broad compilation, dependency integrity, semantic/boundary scans, credential
  scan, and `git diff --check` pass. Pip reports only the known unwritable-cache
  warning.
- **Files/components:** Added `.python-version`,
  `requirements-application.txt`, `backend/climatecapital/contracts/`,
  `backend/climatecapital/release/`, `contracts/schemas/`,
  `scripts/release/`, `tests/application/`, `tests/release/`, and test package
  markers; updated only this canonical progress handoff among pre-existing files.
- **Deviations and risks:** No scope or authority deviation and no new decision ID.
  Per the approved test plan, M1 adds no positive reviewed bundle; reviewed-byte
  validation remains an M5 gate. M2 producers must use the exact schemas rather
  than relax them.
- **Boundaries:** No Product, Methodology, Evidence/source-governance,
  Architecture, active family, scoring/optimization, Gemini authority, reviewed
  data, UI, frontend tooling, or GCP/cloud resource changed. Temporary technical
  objects exist only during tests; no fixture/reviewed bundle was added.
- **Handoff:** Stop for M1 review. Begin neither M2A nor M2B without separate
  authorization.

### 2026-09-02 — Record explicit M0 delivery-baseline approval

- **Objective:** Record the user's explicit approval of the corrected delivery-plan
  package and stop before M1.
- **Approval:** Marked `docs/delivery/implementation-plan.md`, `test-plan.md`,
  `milestones.md`, and the reconciled `execution-plan.md` as the approved M0
  delivery baseline subordinate to Product, Methodology, Evidence, and
  Architecture. M0 is complete; M1 is authorized next but not started.
- **Files changed:** Updated only approval/status, stage/gate, routing, verification,
  and handoff text in the four delivery documents, README, and PROJECT_PROGRESS.
- **Verification:** The full 46-test suite, Python compilation, dependency check,
  133-link/fence validation, intended-file whitespace scan, approval-boundary
  review, full-diff inspection, and `git diff --check` passed. Pip reported only
  its existing unwritable-cache warning.
- **Boundaries:** No implementation, test, milestone, Product, Methodology,
  Evidence, Architecture, or decision contract changed substantively. The exact
  37/$327,970,000 governed universe, 12/$143,005,000 active family, manual full-
  request membership, deterministic authority, geometry independence, benchmark
  isolation, non-authoritative Problem Score treatment, and bounded Gemini
  authority remain unchanged. No application, dependency, governed data, cloud,
  stage, commit, or push operation occurred.
- **Handoff:** Stop after M0 approval recording. Begin only M1 in a subsequent
  implementation task; do not skip to either post-schema track.

### 2026-09-02 — Correct and re-audit the proposed delivery-plan package

- **Objective:** Resolve only the six pre-approval delivery-plan findings without
  reopening or implementing Product, Methodology, Evidence, or Architecture.
- **Corrections:** Restored the Architecture application track before reviewed-data
  integration; limited M6 to reviewed-byte integration and fixture removal;
  clarified official Patchamomma requirements as urgent submission-dependent work,
  not a blanket M1 gate; replaced the stale scoring-readiness entry; deferred
  frontend tooling to M4; added M1 geometry/membership-authority contract tests;
  and replaced the invented authority ranking with domain authority plus explicit
  supersession and conflict-stop language.
- **Analytical trace:** Re-read the exact 12-row Methodology table and D-075/D-077,
  then independently reconciled its IDs and requests to the governed 37-row CSV.
  The family is exactly 12 / $143,005,000 and is purpose-derived independently of
  geometry. RNA exact-ID geometry is 15 matched / 22 unmatched over all 37 and 5/7
  within the 12-family subset; neither result changes family membership.
- **Semantic sweep:** Classified repository-wide Importance, weight, score, rank,
  and optimizer terms. Current uses are the proper-name Problem Score, explicit
  prohibitions/non-goals, or later-scope possibilities contingent on a future
  methodology revision; older affirmative mechanics occur only in decision/status
  history marked superseded/resolved. The sole stale active delivery entry was
  corrected. No out-of-scope higher-authority rewrite was needed.
- **Verification:** The full 46-test suite, Python compilation, dependency check,
  all-six-finding semantic assertions, exact cohort/source/GIS reconciliation,
  link/fence validation, whitespace check, full-diff review, and `git diff --check`
  passed. Pip reported only its existing unwritable-cache warning.
- **Files changed:** Corrected the proposed implementation, test, and milestone
  plans plus the related execution-plan and canonical progress text. README routing
  remained accurate and required no correction in this pass.
- **Deviations, risks, and decisions:** No deviation from the locked work order, no
  new contradiction, and no new decision ID. Official submission requirements
  remain urgent and unresolved for submission-dependent work. No application,
  dependency, governed data, cloud, stage, commit, or push change occurred.
- **Handoff:** The corrected package passed the pre-approval re-audit and remains
  proposed for explicit user approval. Do not begin M1 automatically.

### 2026-09-02 — Draft the architecture-informed delivery-plan gate

- **Objective:** Recover project state from the repository, identify the first
  outstanding Architecture work unit, and perform only that unit without skipping
  into application implementation.
- **Recovery result:** Confirmed clean `main` at the Architecture Lock checkpoint,
  no application code or application dependency manifest, the existing governed
  data/reconnaissance foundation, and the authoritative Architecture Lock in
  `docs/architecture/p0-architecture.md` and `data-contracts.md`. The lock makes
  delivery-plan creation/approval the first outstanding unit and prohibits
  application code before it.
- **Semantic reconciliation:** Preserved the active evidence-first method. D-076
  and D-077 supersede the earlier weight/optimizer premise: P0 has no Importance
  weights or optimizer, and analyst-controlled full-request membership within the
  exact 12-record family flows through deterministic validation/arithmetic.
- **Initial draft:** Drafted `docs/delivery/implementation-plan.md`,
  `docs/delivery/test-plan.md`, and `docs/delivery/milestones.md`; refined the
  approved execution plan, README map, and canonical current handoff. The draft
  defined M1 contract/validator work as the first application milestone and kept
  reviewed-data, Gemini, identity, cost, and cloud gates explicit.
- **Verification:** The full 46-test repository suite, Python compilation,
  dependency check, diff/whitespace checks, relative-link/fence validation, stale
  handoff searches, and locked-term review passed mechanically. A later semantic
  pre-approval audit found that the draft did not yet preserve the Architecture
  application-track/integration split and contained five additional consistency
  issues; this entry therefore does not record delivery-plan approval readiness.
  Pip reported only its existing unwritable-cache warning; no broken requirement
  existed.
- **Files changed:** Added the three proposed delivery plans; updated
  `docs/delivery/execution-plan.md`, `PROJECT_PROGRESS.md`, and `README.md`.
- **Deviations and issues:** No application code was created because M0 approval is
  a locked prerequisite. The initial draft ambiguously assigned frontend runtime/
  package-manager pinning to M1 and treated official submission requirements
  inconsistently; both were sent to the narrow correction pass. No new durable
  decision was needed.
- **Boundaries:** No Product, Methodology, Evidence, Architecture, scoring,
  optimization, Gemini-authority, governed data, dependency, cloud resource,
  commit, or push change occurred.
- **Handoff:** Superseded by the pre-approval audit and narrow correction pass. Do
  not begin M1 automatically.

### 2026-09-02 — Correct the P0 scenario-budget validation bound

- **Objective:** Apply only the approved final input-bound precision correction
  before the Architecture Lock commit checkpoint.
- **Result:** `docs/architecture/data-contracts.md` now accepts scenario budgets
  from `$0` through `$1,000,000,000` as application validation and input-safety
  bounds. The contract explicitly preserves City-policy and eligibility
  separation, the `$125,000,000` Historical Envelope, ample headroom over the
  `$327,970,000` governed universe, and exact whole-dollar arithmetic.
- **Verification:** The full 46-test repository suite, `git diff --check`, the
  obsolete-bound search, and focused Architecture/Methodology consistency checks
  passed. No other documentation referenced the old maximum.
- **Boundaries:** No other architecture contract, decision, application code,
  cloud state, commit, or push changed.

### 2026-09-02 — Persist the approved P0 Architecture Lock

- **Objective:** Persist the user-approved implementation architecture and final
  precision corrections without reopening methodology, product design, source
  reconnaissance, or application implementation.
- **Architecture result:** Created the authoritative single-container
  React/TypeScript/Vite/Leaflet plus one-worker FastAPI Cloud Run topology; pinned
  source-to-release flow; minimal GCS/BigQuery roles; precomputed GIS; browser-only
  current-session state; exact plan trust boundary; isolated Historical Benchmark;
  direct bounded OSM defaults; keyless required Gemini explanation; post-core
  proposal; bounded security, observability, cost, image, and deployment controls;
  and the post-schema parallel data/application work order.
- **Contract result:** Created normative four-file release-bundle, non-circular
  manifest/deployment identity, evidence/missingness, fixture/review tier, catalog,
  map, benchmark, stateless current/reference plan, API, session reducer, Gemini,
  configuration, and release-gate contracts. A release candidate cannot contain
  fixture evidence or acquire live source data.
- **Product/delivery reconciliation:** Made grounded explanation the only required
  P0 AI capability, moved stable story P0-9 proposal to post-core stretch, replaced
  proactive/page-load Gemini behavior with explicit invocation, locked RNA/FEMA/EAZ
  defaults and FloodPro omission, marked the reference superseded, and made
  delivery planning the next gate.
- **Decision history:** Added D-080–D-096 and updated only statuses/links on earlier
  rows to identify explicit fulfillment, resolution, or narrowing; no historical
  decision text or ID was renumbered or silently rewritten.
- **Files:** Created `docs/architecture/p0-architecture.md` and
  `docs/architecture/data-contracts.md`; updated `PROJECT_PROGRESS.md`, `README.md`,
  `docs/decisions.md`, the three `docs/product/` specifications,
  `docs/delivery/execution-plan.md`, and the superseded
  `docs/reference/technical-architecture-reference.md`.
- **Verification:** The full 46-test repository suite and `git diff --check` passed.
  Independent checks validated all relative Markdown links and fences, continuous
  D-001–D-096, all 12 stable P0 IDs with 11 required core stories and P0-9 stretch,
  exact 37/$327,970,000 and 12/$143,005,000 reconciliations, all approved manifest,
  identity, one-process Gemini, plan, fixture, map, BigQuery/GIS, cost, and two-track
  invariants, and no affirmative stale optimizer/ranking/weights/runtime-data
  contract. Git review found documentation-only changes.
- **Open items:** Focused City-derived layer reuse/license confirmation, organizer
  submission requirements, current quotas and existing billing-control inspection,
  reviewed evidence bundle construction, application implementation, and deployment
  remain future authorized work.
- **Boundaries:** No application code, dependency, source snapshot, analytical
  result, BigQuery/GCS resource, IAM, billing control, Gemini call, deployment,
  commit, or push changed.
- **Handoff:** In a separately authorized task, create and approve the
  architecture-informed implementation, test, and milestone plans before any
  application or data-track implementation.

### 2026-09-01 — Lock the P0 evidence-first methodology

- **Objective:** Persist the closed evidence-feasibility findings, reconcile their
  consequences with the prior Product and Design Lock, and lock the smallest
  defensible P0 method without application or architecture implementation.
- **Methodology result:** Retained all 37 governed projects / $327,970,000 and the
  all-37 derived purpose classification with official name, evidence, confidence,
  and ambiguity. Recorded the 24-project / $233,380,000 broad flood-related family
  as analytically incoherent and locked the exact 12-record local flood/local
  drainage analytical family / $143,005,000, with 5789.150 retained as a citywide
  program requiring separate geography/evidence treatment.
- **Evidence treatment:** Locked FACT, CONTEXTUAL EVIDENCE, RESEARCH-ONLY EVIDENCE,
  and UNAVAILABLE / UNSUPPORTED. Problem Score and FEMA remain contextual; current
  RNA and Fully Developed FloodPro are research-only for governed analytical use;
  EAZ 2021 is contextual for 5/12 and unavailable at project level for 7/12;
  expected flood-reduction benefit and a cohort-wide numeric risk/equity model are
  unsupported.
- **Product reconciliation:** Explicitly removed Funding Priority, rank, Importance
  weights, expected benefit, missingness penalties/imputation, and optimization.
  Reopened Funding Plan inclusion/removal as an analyst-controlled input; limited
  deterministic authority to governed facts/evidence states, validation,
  integer-dollar arithmetic, and supported comparison; limited Gemini to grounded
  explanation and confirmed translation of explicit analyst commands. Retained
  $125 million as Historical Envelope context, not family or eligibility logic.
- **Decision history:** Added D-074–D-079 and marked the original conflicting
  decision text superseded, narrowed, or resolved rather than overwriting it.
- **Final semantic audit:** Reserved Historical Envelope for the $125 million
  historical context; renamed the first analyst-confirmed plan Session Reference
  Plan and the active plan Current Confirmed Plan; made City benchmark isolation,
  active-family-only membership, full-request treatment, and deterministic
  non-selection authority explicit throughout the affected handoff.
- **Files changed:** Added docs/methodology/p0-evidence-methodology.md; updated
  AGENTS.md, PROJECT_PROGRESS.md, README.md, docs/decisions.md,
  docs/product/product-plan.md, docs/product/user-stories.md,
  docs/product/screen-spec.md, docs/delivery/execution-plan.md, and
  docs/reference/technical-architecture-reference.md.
- **Verification:** The full 46-test suite and `git diff --check` passed. Independent
  documentation checks reconciled the exact governed/family/broad counts and
  dollars to the source CSV, matched all 37 names and family requests, confirmed
  continuous D-001–D-079, validated 13 Markdown files' relative links/fences, and
  found no stale current optimizer/weight/recommendation contract. The final
  semantic audit also passed explicit guards for Historical Envelope/session-plan
  separation, City benchmark isolation, provisional-family/non-eligibility
  treatment, and active-family-only full-request membership with deterministic
  validation rather than selection.
- **Boundaries:** No new source reconnaissance, Buildings/SVI ingestion, geometry,
  score, weights, optimization, application code, production pipeline, architecture,
  cloud resource, or push occurred. The reviewed documentation checkpoint was
  authorized for commit.
- **Handoff:** Review is complete. In a separately authorized task, resume
  Architecture Planning against the locked methodology and reconciled
  Product/Design handoff.

### 2026-09-01 — Acquire and match Austin RNA Projects layer 8

- **Objective:** Preserve one reproducible native snapshot of the canonical live
  RNA Projects layer 8, test all governed memo IDs without fuzzy/name matching,
  and quantify current GIS evidence coverage without inferring analytical use.
- **Acquisition:** Captured service/layer metadata, 577 pre-acquisition OBJECTIDs,
  the exact frozen-ID feature response with geometry, and 577 post-acquisition
  OBJECTIDs under snapshot `20260901T183323Z`. Pre/post sets matched, all requested
  features returned exactly once, no unexpected features or transfer-limit flag
  occurred, and the semantic feature fingerprint is
  `sha256:3d81feb35841e816c0ce5bab5e2abbca05b46a903f98c1ea3b16c8cf604b940f`.
- **Source fidelity:** Parsed native JSON numeric tokens without binary-float
  conversion. All 577 `SUB_PROJECT_ID` values mapped exactly to the governed
  three-decimal domain by representational zero-padding only; 548 canonical IDs
  are unique in the full layer and source duplicates remain visible. The exact
  11-field schema and native ESRI:102739/EPSG:2277 polygon CRS passed validation.
- **Geometry:** All 577 features contain native polygon geometry; no true curves
  were observed. No reprojection, simplification, densification, repair,
  precision/offset setting, or quantization was applied.
- **Match result:** The complete-universe artifact retains all 37 official projects
  and derives 15 single matches, 22 zero matches, and no multiple matches by exact
  canonical ID only. Three matching GIS names differ from the memo names, which is
  retained as evidence and does not affect matching. Matched governed requests are
  $163,975,000 and unmatched requests are $163,995,000, reconciling to 37 and
  $327,970,000.
- **Cloud preservation:** Created exactly six objects below
  `gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/`.
  Every generation-specific cloud byte stream matched its local size and exact-byte
  SHA-256. The finalized manifest was uploaded; the non-circular GCS receipt is
  Git-tracked only.
- **Files:** Added the two focused CLIs, one focused test module, the timestamped
  manifest/receipt/match artifacts, and D-073; updated the source registry,
  registry validation, README, and this progress handoff. Raw HTTP/GIS responses
  remain ignored and untracked.
- **Verification:** The full repository suite, Python compilation, dependency
  check, independent manifest/match/receipt reconciliation, diff check, credential
  scan, and Git tracked/ignored review passed. The matcher also confirmed
  identical-output behavior on rerun.
- **Boundaries:** Layer 8 is live/current and remains `historical_fit=uncertain`,
  `analytical_role=research-only`; the snapshot does not establish January 2026
  geometry. A match does not establish eligibility, project footprint semantics,
  hazard, exposure, benefit, or analytical comparability. No additional GIS,
  benchmark, BigQuery, methodology, Architecture, application, commit, or push
  work occurred.
- **Handoff:** Review this bounded GIS checkpoint, then explicitly authorize the
  next analytical-feasibility evidence work unit. Architecture Planning remains
  paused before lock.

### 2026-08-31 — Validate and harden raw BigQuery ingestion

- **Objective:** Complete the raw warehouse checkpoint by reviewing the manual
  loader, validating the existing table without overwriting it, adding durable SQL
  quality checks, and preserving the result without beginning GIS or architecture.
- **Manual implementation review:** Retained the correct project/dataset/table,
  explicit nine-column schema, STRING project IDs and district source text,
  INTEGER page/order/dollar fields, UTF-8/header handling, `us-central1` job
  location, local ADC, and `WRITE_EMPTY` behavior. Hardened only material gaps:
  repository-anchored CSV resolution, exact CSV checksum and contract preflight,
  dataset-location and existing-target checks, explicit load options, post-load
  schema/location/count validation, and human-readable failures.
- **Warehouse result:** Verified the existing
  `climatecapital-ai.raw.watershed_projects_2025_11_21` table and its `raw` dataset
  are in `us-central1`. All nine ordered columns and REQUIRED modes match the
  governed schema; `subproject_id` and source fields are STRING, while page, row
  order, and normalized dollars are INTEGER. The table has 37 rows.
- **Data-quality result:** All 21 final read-only SQL checks passed: 37 unique IDs,
  no duplicates or governed NULLs, one expected source ID, contiguous order 1–37,
  exact A–AK sequence, page 4/5 domain and 19/18 counts, positive/reconciled
  funding values totaling $327,970,000, valid source-form district strings, exact
  first/boundary/multi-district/final rows, preserved 5789.150/5789.145/5789.146
  order, and full ordered semantic SHA-256
  `c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a`.
- **Tests and safety:** The full 29-test suite, `py_compile`, `pip check`, and
  `git diff --check` passed; the credential-pattern scan found no matches. A live
  loader preflight refused the already-existing table before load submission.
  Authentication used local ADC; no credentials or credential paths were added.
- **Files changed:** Retained the manually added requirements-cloud.txt; hardened
  scripts/data/load_watershed_projects_bigquery.py; added
  tests/test_watershed_bigquery_loader.py and
  sql/quality/watershed_projects_raw_checks.sql; updated PROJECT_PROGRESS.md,
  README.md, and docs/decisions.md; recorded D-072.
- **Limitations:** The live schema/data prove the current warehouse copy is
  source-faithful, but the hardened code cannot retroactively prove the exact
  configuration of the already-completed manual load job. BigQuery does not enforce
  the SQL semantic contracts as constraints, so the suite must be rerun after any
  separately authorized mutation. Source reuse terms remain unresolved.
- **Boundaries preserved:** No existing table or other cloud state was recreated,
  overwritten, or changed. No staging/curated/benchmark table, January benchmark
  inspection, GIS work, eligibility, evidence inference, scoring, optimization,
  Product/Design change, Architecture Planning, commit, or push occurred.
- **Handoff:** Await review. The recommended next separately authorized work unit
  is complete 37-ID Austin GIS geometry matching with retained unmatched records
  and explicit match evidence; do not begin it in this task.

### 2026-08-31 — Extract the official Watershed source universe

- **Objective:** Derive and validate only the complete named-project source universe
  from the checksum-governed November 21, 2025 memo without deciding eligibility,
  geometry, project type, flood evidence, methodology, or architecture.
- **Completed:** Pinned pypdf 6.16.2 as a local data-only dependency; added a
  checksum-gated extractor that requires table anchors and columns, parses each row
  without crossing row boundaries, records 1-based physical PDF pages, preserves
  official IDs and published order as strings, retains source currency alongside
  integer dollars, reconciles totals, and refuses differing-artifact overwrite;
  generated the deterministic 37-record CSV; recorded D-071.
- **Data result:** Extracted 19 records from physical PDF page 4 and 18 from page 5.
  All 37 map labels and subproject IDs are unique. The row sum, separately parsed
  table total, and memorandum program request each equal $327,970,000. Presence in
  the artifact does not establish ClimateCapital eligibility.
- **Schema:** `source_id`, `source_pdf_page`, `source_table_row_order`, `map_label`,
  `subproject_id`, `project_name`, `current_funding_request_estimate_source`,
  `current_funding_request_estimate_dollars`, `council_districts_source`.
- **Tests and results:** The focused 10-test extraction suite and full 19-test
  repository suite passed. Source-verified first/last, page-4/page-5 boundary,
  multi-district, and 5789.150/5789.145/5789.146 anomaly checks passed; checksum,
  anchor, column, row, total, and overwrite failure paths passed; `py_compile`, an
  independent CSV count/sum read, and `git diff --check` passed; a repeated CLI run
  reported the artifact as identical.
- **Files changed:** Added requirements-data.txt,
  scripts/data/extract_watershed_projects.py,
  data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv,
  and tests/test_watershed_project_extraction.py; updated
  data/metadata/source_registry.csv, PROJECT_PROGRESS.md, README.md, and
  docs/decisions.md.
- **Issues and risks:** The source claims project-ID sorting but places 5789.150
  before 5789.145 and 5789.146; the artifact preserves that published order. PDF
  line-wrap whitespace was collapsed while punctuation, spelling, and displayed
  currency were retained. Source reuse and redistribution terms remain unresolved.
- **Boundaries preserved:** The January benchmark PDF was not inspected or used.
  No GIS matching, eligibility, project-type classification, flood-benefit
  inference, BigQuery table, scoring, optimization, application, cloud mutation,
  Architecture Planning, commit, or push occurred.
- **Handoff:** Await user review. Do not begin GIS matching or further evidence work
  until separately authorized.

### 2026-08-31 — Preserve the two raw snapshots in existing Cloud Storage

- **Objective:** Upload only the two governed local raw PDFs to their exact paths in
  the existing bucket without changing infrastructure or silently overwriting an
  object, then independently verify cloud bytes against local and registry SHA-256.
- **Completed:** Verified local existence, sizes, expected and registry checksums,
  configured project `climatecapital-ai`, active gcloud authentication, ADC, and
  access to `gs://climatecapital-ai-raw-swetha/`; confirmed both destination objects
  were absent; uploaded each with `--if-generation-match=0`; recorded D-070.
- **Cloud results:** The Watershed source object is generation
  `1788210198102506`, 1,151,348 bytes. The benchmark object is generation
  `1788210202820922`, 412,820 bytes. Both have metageneration 1 and content type
  application/pdf.
- **Integrity verification:** Streamed each generation-specific GCS object through
  an independent SHA-256 calculation. Each cloud byte size and SHA-256 matched the
  corresponding local file, expected digest, and canonical registry checksum.
  GCS CRC32C and MD5 metadata were observed but were not treated as SHA-256.
- **Files changed:** Updated PROJECT_PROGRESS.md and docs/decisions.md for durable
  external-state handoff. No source metadata, raw local file, code, test, product,
  design, architecture, or analytical file changed.
- **Issues and warnings:** Sandboxed gcloud version/help checks could not write SDK
  logs under the local gcloud configuration directory; authenticated commands were
  executed with approved access and succeeded. No cloud conflict or integrity
  warning occurred, and no token or credential content was printed or stored.
- **Boundaries preserved:** No infrastructure, IAM, bucket setting, service account,
  credential file, additional object, BigQuery resource, extraction, project table,
  methodology, Architecture Planning, or push.
- **Handoff:** Await user review. Do not extract the 37 projects or perform further
  cloud work until separately authorized.

### 2026-08-31 — Implement the minimal source-ingestion foundation

- **Objective:** Establish only the reproducible source registry, immutable local
  fetch, provenance metadata, tests, and Git protections required to preserve the
  first two authoritative City documents.
- **Completed:** Added the exact 15-column canonical registry and registered the
  November 21 source-universe memo as analytical and the January 21 recommendation
  as benchmark-only; added a standard-library HTTPS fetcher with deterministic
  paths, exact-byte SHA-256, UTC retrieval metadata, PDF/header checks, and
  differing-snapshot overwrite refusal; downloaded both PDFs; added nine focused
  tests and raw/temporary/credential Git protections; recorded D-069.
- **Tests and results:** `python3 -m unittest discover -s tests -v` passed 9/9;
  `python3 -m py_compile` passed; registry validation found two valid unique rows;
  independent byte counts and `shasum -a 256` values matched the registry; both
  files were recognized as PDF 1.7; `git diff --check` and the trailing-whitespace
  scan passed; `git check-ignore` and status confirmed both raw PDFs are ignored.
- **Files changed:** Added .gitignore, data/metadata/source_registry.csv,
  scripts/data/fetch_sources.py, and tests/test_source_ingestion.py; updated
  PROJECT_PROGRESS.md, README.md, and docs/decisions.md. The two downloaded PDFs
  exist only in ignored data/staging paths.
- **Deviations and issues:** The sandboxed attempt could not resolve the host. The
  unrestricted Python retry then exposed a missing default CA bundle; verified
  HTTPS succeeded with `SSL_CERT_FILE=/etc/ssl/cert.pem`. Certificate verification
  was never disabled. License/reuse terms remain unverified. The exact existing GCS
  bucket name was not supplied, so no upload was attempted.
- **Boundaries preserved:** No PDF extraction, OCR, 37-project derivation,
  eligibility, analytical evidence, scoring, optimization, Gemini, application,
  BigQuery table/load, cloud provisioning, Architecture Lock, commit, or push.
- **Handoff:** Await user review. If Cloud Storage upload is requested, obtain the
  exact existing bucket name first. Otherwise, the recommended next separately
  authorized milestone is source-only derivation of the 37 project records without
  eligibility or analytical inference.

### 2026-08-31 — Pause Architecture Lock for evidence reconnaissance

- **Objective:** Record the controlled Architecture Planning dependency-resolution
  step needed to test the 37 official Watershed projects against authoritative,
  historically valid evidence before architecture or methodology is locked.
- **Completed:** Preserved every approved Product and Design Lock; paused
  Architecture Planning before lock; made the 37-project evidence repository and
  matrix the immediate objective; recorded the source-universe and benchmark-only
  separation; updated blockers, risks, open questions, Next Actions, and the
  Architecture handoff; added D-067 and D-068.
- **Files changed:** PROJECT_PROGRESS.md, README.md, and docs/decisions.md. No
  product specification, architecture file, methodology, source dataset, pipeline,
  application code, dependency, Gemini integration, or cloud resource changed.
- **Verification:** Reviewed the complete diff; `git diff --check` passed; confirmed
  68 continuous decision rows through D-068, next ID D-069, and no stale current
  status claiming Architecture Planning is unstarted or ready to lock.
- **Handoff:** Begin with the November 21, 2025 source memo, preserve all 37 source
  projects, keep the January 21, 2026 City recommendation structurally separate,
  and build the evidence matrix without inventing benefit, geometry, exclusions,
  or methodology. Resume Architecture Planning only after findings are reviewed.

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
- **Completed:** Defined the then-named January 2026 Historical Baseline, $125
  million Projects constraint, scenario terminology, rule-derived cohort, binary funding assumption,
  ranking-versus-portfolio distinction, source-vintage policy, City benchmark
  isolation, Gemini boundary, editable inputs, and deferred later-stage decisions.
  D-078 later superseded the plan terminology with Session Reference Plan.
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

### 2026-09-03 — M3.5 Cross-Category Analytical Feasibility Audit

**Status:** Complete and explicitly approved 2026-09-03.

M3.5 freezes the January 21, 2026 historical analytical universe before
cross-category implementation:

- 136 PRB source rows
- 106 `ANALYTICAL_PROJECT` units
- 23 `PROGRAM_BUCKET` units
- 4 `PROGRAM_ALLOCATION` units
- 3 quarantined `NOT_SCORED` units
- analytical projects by presentation group:
  - Transportation: 9
  - Parks & Open Space: 22
  - Watershed: 37
  - Community Facilities: 38

`ANALYTICAL_PROJECT` establishes a structurally valid project-level decision
unit only; evidence feasibility and model eligibility remain separate.

Community Facilities is a presentation grouping and does not overwrite
`source_department` or `source_domain`.

Authoritative governance:
`docs/delivery/m3-5-analytical-universe.md`

M4 and subsequent cross-category implementation must conform to this locked
universe.

## 2026-09-04 — M3.6 Governed Cross-Category Dataset and Schema

M3.6 implementation is complete.

The approved M3.5 January 21, 2026 historical analytical-universe semantics
are now implemented as a strict governed artifact:

- `data/governed/cross_category/cross-category-universe.json`
- 136 PRB source rows
- 106 `ANALYTICAL_PROJECT`
- 23 `PROGRAM_BUCKET`
- 4 `PROGRAM_ALLOCATION`
- 3 `NOT_SCORED`

Analytical projects reconcile exactly to:

- Transportation: 9
- Parks & Open Space: 22
- Watershed: 37
- Community Facilities: 38

The exact NOT_SCORED quarantine remains:

- Neighborhood Partnering Program
- Open Space Acquisition
- Affordable Housing

The implementation preserves source department/domain separately from
presentation category, preserves department request separately from historical
recommendation amount, retains source-version conflicts rather than
overwriting them, and keeps analytical-unit status, evidence feasibility, and
model eligibility separate.

The existing 37-project Watershed runtime catalog remains unchanged. The
136-row cross-category universe is a separate governed source artifact and
does not automatically expand M2/M3 runtime/model eligibility.

Watershed retains the canonical November 21, 2025 37-project universe and
$327,970,000 request total, with the January PRB overlay preserved separately.
The 5754.149 $2.500M versus $2.625M request conflict remains explicit.

The July 31, 2025 Initial Project Request List is now registered as governed
historical source-version evidence.

Verification completed:

- 38 focused M3.6 tests passed
- 109 application tests plus 23 subtests passed
- 197 full-suite tests plus 58 subtests passed
- 23 schemas generated
- `git diff --check` passed
- no new dependency was introduced solely for external JSON-Schema validation

Detailed checkpoint:

`docs/delivery/m3-6-governed-cross-category-dataset.md`

Next analytical work must derive evidence-feasibility and model-eligibility
from this governed universe rather than treating all 106 structural
analytical projects as automatically model-ready.

## 2026-09-04 — M3.7A Watershed PRB Score Reconciliation

M3.7A implementation and verification are complete; checkpoint approval and
commit remain pending.

The governed November 21, 2025 Watershed universe was reconciled against the
checksum-verified January 21, 2026 PRB scoring source.

Result:

- 37/37 governed Watershed analytical projects reconciled
- 37/37 complete six-component PRB score vectors
- 37/37 valid PRB Grand Totals
- 7 exact November/January source-name matches
- 30 governed source-version name matches
- 0 ambiguous matches
- 0 unmatched projects
- 1 request-version conflict: `5754.149`
- canonical November request total: $327,970,000
- January PRB project request total: $328,095,000
- January named-project recommendation total: $125,000,000

The January PRB extraction is checksum-gated, fail-closed, deterministic, and
idempotent. Every six-component vector sums exactly to its governed Grand
Total.

Canonical November identity remains authoritative. January names, scores,
requests, and recommendation values remain overlays.

The January source authority remains structurally separated: PRB scoring
evidence may be considered for analytical use in M3.7B/C, while Initial
Recommendation remains benchmark/outcome-only and cannot become a model input.

No Funding Priority formula, ranking, tie-breaking rule, optimization
objective, or portfolio optimizer was introduced in M3.7A.

Verification:

- M3.7A focused extraction tests: 10 passed, 79 subtests passed
- combined Watershed regression checkpoint: 38 passed, 84 subtests passed
- full repository: 216 passed, 137 subtests passed
- `python -m pip check`: no broken requirements
- one existing Starlette/AnyIO deprecation warning remains non-failing

Detailed checkpoint:

`docs/delivery/m3-7a-watershed-prb-reconciliation.md`

Next:

M3.7B — determine Watershed evidence feasibility and model eligibility using
the now-proven 37/37 PRB evidence layer before reopening deterministic Funding
Priority or $125M optimization.

## 2026-09-04 — M3.7B Watershed PRB Model Eligibility

M3.7B implementation, verification, approval, commit, and publication are complete. The checkpoint is published to `origin/main` at `ae41444`.

- **Scope:** Evaluated only the 37 governed Watershed `Analytical_Project` records for participation in `WATERSHED_PRB_PROJECT_MODEL`.
- **Eligibility result:** 37/37 are `FEASIBLE` and model-eligible. Every project has reconciled canonical identity, a complete official six-component PRB vector, a valid PRB Grand Total, and a usable canonical November request.
- **Outcome isolation:** 25/37 eligible projects have no January recommendation. The Initial Recommendation remains benchmark/outcome-only and has no eligibility authority.
- **Conflict handling:** `5754.149` remains eligible using its canonical November `$2,500,000` request while the January `$2,625,000` request-version conflict remains explicit provenance.
- **Contextual evidence:** RNA geometry, FEMA floodplain context, EAZ 2021 context, and Watershed Problem Score context remain non-gating for the base PRB model.
- **Artifact:** `data/governed/cross_category/model_eligibility/watershed-prb-model-eligibility.json`.
- **Boundary:** M3.7B is persisted as a separate governed overlay. M3.6 structural artifacts are not rewritten, `runtime_integration_authorized=false`, and the existing 12-project runtime family remains unchanged.
- **Verification:** 17 focused M3.7B tests; 55 combined Watershed tests plus 84 subtests; 233 full-repository tests plus 137 subtests; `pip check`; deterministic artifact regeneration; and `git diff --check` all pass. The known Starlette/AnyIO deprecation warning remains non-blocking.
- **Not decided:** No Funding Priority, ranking, tie-break, portfolio optimization, cross-category eligibility, or 37-project runtime activation is introduced.
- **Next:** M3.7C became the next analytical checkpoint and evaluates deterministic PRB Funding Priority and tie methodology before cross-category eligibility and final portfolio optimization work.

## 2026-09-04 — M3.7C Watershed PRB Funding Priority

M3.7C implementation and verification are complete; checkpoint approval is pending.

- **Scope:** Ranked only the 37 Watershed projects already approved as model-eligible in M3.7B under `WATERSHED_PRB_PROJECT_MODEL`.
- **Score authority:** `Funding Priority Score` is the official PRB Grand Total. Higher Grand Total means higher Funding Priority. No ClimateCapital-created weighting, normalization, cost adjustment, spatial adjustment, missing-evidence penalty, or January-recommendation adjustment is applied.
- **Ranking method:** Funding Priority uses descending competition ranking. Equal PRB Grand Totals retain the same substantive rank, so rank gaps are intentional.
- **Tie evidence:** The cohort has 17 unique scores, 12 tied score groups, and 32 of 37 projects participating in tied groups. Ties are therefore a material methodology rule rather than a presentation edge case.
- **Display ordering:** Canonical project ID ascending is used only to provide deterministic row order inside an equal-score group. `display_tiebreak_has_analytical_meaning=false`.
- **Forbidden analytical tie-breakers:** Project cost, January Initial Recommendation, individual PRB components, RNA geometry, FEMA floodplain context, EAZ 2021 context, Watershed Problem Score context, source table row order, and project name do not break substantive PRB-score ties.
- **Top result:** `5282.134` has Funding Priority Score 74 and rank 1. Projects `5282.043`, `5282.133`, and `5789.126` each have score 73 and shared rank 2.
- **Conflict handling:** `5754.149` has score 63 and shared rank 20. Its request-version conflict has no ranking special case because M3.7C ranks only the already-governed eligible cohort using PRB Grand Total.
- **Artifact:** `data/governed/cross_category/funding_priority/watershed-prb-funding-priority.json`.
- **Boundary:** `portfolio_selection_authorized=false` and `runtime_integration_authorized=false`. M3.7C creates no optimizer, portfolio-selection rule, score-per-dollar metric, or runtime activation.
- **Verification:** 18 focused M3.7C tests; 73 combined Watershed tests plus 84 subtests; 251 full-repository tests plus 137 subtests; `pip check`; deterministic artifact regeneration; and `git diff --check` all pass. The known Starlette/AnyIO deprecation warning remains non-blocking.
- **Not decided:** No portfolio optimization objective, `$125M` selection algorithm, category allocation constraint, cross-category eligibility/ranking comparability, or 37-project runtime activation is introduced.
- **Next:** M3.7E evaluates evidence feasibility and model eligibility across all 106 analytical projects before final portfolio optimization methodology is locked.
