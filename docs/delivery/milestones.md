# ClimateCapital AI P0 Delivery Milestones

> **Status:** Delivery baseline approved 2026-09-02; M0 and M1 explicitly approved
> 2026-09-02; M2A, M2B, and M3 explicitly approved 2026-09-03
> **Rule:** Milestones are dependency-ordered. Approval of one milestone does not
> silently authorize cloud mutation, deployment, commit, push, P1, or Later work.

## Milestone Summary

| ID | Milestone | Status | Cloud cost impact |
| --- | --- | --- | --- |
| M0 | Architecture-informed implementation/test/milestone plans | Complete; explicitly approved 2026-09-02 | None |
| M1 | Versioned contracts and fail-closed release validators | Complete; explicitly approved 2026-09-02 | None; local only |
| M2A | Controlled data prerequisites and pinned approved inputs  | Complete; explicitly approved 2026-09-03 | Bounded existing GCS/query use only if separately authorized |
| M2B | Exact-schema fixture and deterministic plan engine | Complete; explicitly approved 2026-09-03 | None; local only |
| M3  | Health/bootstrap/plan/benchmark APIs | Complete; explicitly approved 2026-09-03 | None; local only |
| M4 | Application-track frontend and required product surfaces | Next; M3 prerequisite satisfied | None; local only |
| M5 | Reviewed pinned release-data bundle | Blocked by M2A | Bounded existing GCS/BigQuery release-gate use |
| M6 | Reviewed-data integration and fixture removal | Blocked by M4 and M5 | None; local build only |
| M7 | Manual-core, recovery, accessibility, and E2E gate | Blocked by M6 | None; local only |
| M8 | Required grounded Gemini explanation | Blocked by M7 | Mocked locally; one later authorized canary |
| M9 | Container, no-traffic deployment, verification, promotion | Blocked by M8 and explicit cloud authorization | Bounded locked GCP services |
| M10 | P0-9 / SP0-1 stretch evaluation | Blocked by core candidate and contingency | No new infrastructure |

## M0 — Delivery Plan Gate

**Outcome:** `implementation-plan.md`, `test-plan.md`, and `milestones.md` are
reviewed together and explicitly approved.

**Acceptance:**

- The three documents preserve all locks and D-080–D-096 dependency order.
- The first implementation milestone, write surface, tests, and stop point are
  unambiguous.
- Fixture/reviewed-data, benchmark, deterministic authority, missingness, Gemini,
  identity, cost, and cloud-authorization boundaries are explicit.
- `execution-plan.md` and `PROJECT_PROGRESS.md` record M0 approval as the satisfied
  repository authorization gate before M1. Unresolved official submission
  requirements remain urgent but do not block independent M1 contract/validator
  work.
- Current repository tests and documentation integrity checks pass.

**Stop point:** M0 was explicitly approved on 2026-09-02. Stop after recording the
gate; do not begin M1 in the approval-recording task.

## M1 — Contract and Validator Foundation

**Outcome:** Machine-enforced initial schemas and a fail-closed bundle validator
implement the already locked contract versions without an application UI, runtime
API, fixture bundle, or cloud work.

**Acceptance:**

- Contract identifiers and strict artifact/request/state models exist.
- Cross-file checksums, identity, governed totals/family, evidence-state rules,
  map defaults, citywide/no-feature, fixture/reviewed tier, benchmark isolation,
  and forbidden fields are enforced.
- Contract tests prove that active-family membership remains valid without geometry,
  geometry cannot promote an out-of-family project, geometry fields have no
  membership authority, and valid bundles require no fabricated/null features.
- Positive technical contract objects and material negative paths are tested.
- Existing 46 tests plus M1 focused tests, compilation/type/static checks,
  dependency integrity, and `git diff --check` pass.
- `PROJECT_PROGRESS.md` records files, tests, deviations, risks, and M2A/M2B
  recommendation.

**Stop point:** M1 received independent closure-audit approval on 2026-09-02. No
post-schema work began during the approval and publication session.

## M2A — Controlled Data Prerequisites

**Status:** Complete; explicitly approved by the user on 2026-09-03.

**Outcome:** Only approved inputs required for the reviewed bundle are pinned with
focused reuse/license metadata and exact provenance.

**Acceptance:** Source identity, checksum/generation, retrieval, historical fit,
role, license/reuse state, and limitations are explicit; acquisition is create-only
where preserved; no broad source hunt or new methodology is introduced.

**Stop point:** M2A received explicit user approval on 2026-09-03. M5 remains the owner of reviewed release-data construction.

## M2B — Fixture and Deterministic Engine

**Status:** Complete; explicitly approved by the user on 2026-09-03.

**Outcome:** A conspicuous schema-valid fixture unblocks application work and the
server deterministically evaluates current/reference plan inputs.

**Acceptance:** The fixture contains no invented analytical claims; all 4,096
subsets and input boundaries pass; client analytical fields have no authority;
fingerprints and only supported deltas are stable; invalid attempts cannot imply a
confirmed result.

**Stop point:** M2B received explicit user approval on 2026-09-03. M3 is now the next dependency-ordered milestone.

## M3 — Core APIs

**Status:** Complete; explicitly approved by the user on 2026-09-03.

**Outcome:** Local FastAPI exposes only health, bootstrap, plan evaluation, and
isolated benchmark core contracts required at this stage.

**Acceptance:** Startup validates the core bundle fail-closed; typed errors/status
behavior is stable; both plan sides are independently evaluated through the M2B
engine; benchmark dependency remains one-way; benchmark comparison fresh-evaluates
the analyst plan; optional benchmark failure is contained; oversized bodies are
bounded; no Gemini, frontend, source-service, database, or cloud dependency is
required.

**Verification checkpoint:** 17 focused M3 tests, 71 application tests plus 23
subtests, 41 release tests plus 20 subtests, 159 full-repository tests, 22 schema
checks, `pip check`, and `git diff --check` pass. One dependency-level Starlette /
AnyIO deprecation warning is non-failing.

**Stop point:** M3 received explicit user approval on 2026-09-03. Approval
does not itself authorize commit/push. M4 begins only after the approved M3
checkpoint is published.

## M4 — Application-Track Frontend and Required Surfaces

**Outcome:** Against the conspicuous fixture tier, the local SPA completes the
Architecture application track in order: accessible shell/navigation, exact
session lifecycle and manual Funding Plan, then Project Detail, Data & Methodology,
Help & Resources, map/default/fallback and non-map behavior, and the isolated
Historical Benchmark.

**Acceptance:** Session/reference/What-If/dirty/reviewed/presentation states remain
separate; restoration revalidates; stale identity is visible; last confirmed plan
survives invalid/over-budget/failure attempts; `5789.150` has a non-map path; all
required behavior works with Gemini disabled; fixture mode is unmistakable; map
visibility/context/search/filter/sort/layer state cannot alter analytical-family or
Funding Plan membership; benchmark dependency remains one-way and fails locally.

## M5 — Reviewed Release-Data Bundle

**Outcome:** Reviewed `catalog.json`, `map-context.geojson`, isolated
`benchmark.json`, and `manifest.json` are promoted under one immutable data
version with an external manifest checksum.

**Acceptance:** Exact sources, transformations, evidence coverage/missingness,
37/12 reconciliations, map semantics, benchmark identity, artifact checksums, and
release tier pass independent review; no fixture state or unsupported field
remains.

## M6 — Reviewed-Data Integration

**Outcome:** The already implemented application surfaces are bound to reviewed
data only, with fixture mode removed and no new application semantics introduced.

**Acceptance:** A source-disconnected build passes; fixture mode is absent from the
candidate; all records remain auditable/non-map accessible; map defaults and
evidence labels match the locks; benchmark failure is local; the M4 behavior passes
unchanged against the reviewed bundle.

## M7 — Manual-Core Release Candidate

**Outcome:** Manual Session Reference Plan, one What-If, comparison, Reviewed
Draft, recovery, accessibility, and three-minute journey pass with Gemini off.

**Acceptance:** Story-level traceability for all required non-Gemini behavior is
fresh; state/recovery matrix and end-to-end checks pass; no critical defect is
known; deterministic API/UI values match exactly.

## M8 — Required Gemini Explanation

**Outcome:** Explicit-action grounded explanation works within locked authority,
token, rate, logging, and failure boundaries.

**Acceptance:** Grounding, fresh plan evaluation, benchmark scoping,
post-validation, refusal, kill switch, rate/concurrency/retry, redaction, and local
failure tests pass with mocked provider calls. No proposal endpoint is required.

## M9 — Verified Deployment

**Outcome:** One non-root multi-stage image is deployed by immutable digest to one
scale-to-zero Cloud Run service and promoted only after no-traffic verification.

**Acceptance:** Existing billing controls are inspected before changes; the image
and logs remain bounded; `/healthz` and revision identity reconcile code, data,
manifest, image, and release; manual core passes with Gemini off; one authorized
canary and token-log inspection pass; rollback remains available.

## M10 — Stretch Decision

**Outcome:** Either preserve the verified core unchanged or separately authorize a
bounded stretch.

**Rules:** Compare is cut first and Gemini proposal second under pressure, matching
the locked order. Neither is necessary for M9. No P1 or Later work begins unless
the approved time/contingency rule is satisfied.

## Closeout Record Required for Every Milestone

Update `PROJECT_PROGRESS.md` with:

- work completed and exact files/components changed;
- tests/checks and exact results;
- deviations, unresolved issues, and new risks;
- decision IDs, if an approved durable decision was necessary;
- cloud or dependency impact;
- current Git state; and
- the recommended next milestone.

Do not commit or push unless the user explicitly authorizes it after reviewing the
milestone checkpoint.
