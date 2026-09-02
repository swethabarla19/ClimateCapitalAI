# ClimateCapital AI P0 Test Plan

> **Status:** Approved by explicit user authorization on 2026-09-02; M0 and M1
> complete and explicitly approved
> **Scope:** Verification required by the locked Methodology, Product,
> Architecture, and data/runtime contracts

## Test Objective

Provide fresh, traceable evidence that ClimateCapital AI preserves governed data,
deterministic authority, explicit missingness, browser-session behavior,
benchmark isolation, bounded Gemini behavior, accessibility, reproducible release
identity, and the locked low-cost deployment boundary.

Passing tests never permit a fixture release, weaken a reconciliation, or replace
review of analytical meaning. Expected values come from locked contracts,
governed source artifacts, or independent calculations—not from copied production
logic.

## Required Check Layers

### 1. Existing source and reconnaissance regression suite

Retain and run the current `unittest` suite for source-registry validation,
immutable acquisition, 37-record extraction, BigQuery loader safety, native RNA
snapshot validation, exact-ID matching, geometry missingness, and cloud-byte
verification. New application work must not weaken or bypass these checks.

### 2. Artifact schema and release validation

Cover all four release-data artifacts and their cross-file contract:

- exact contract/data version and release-tier agreement;
- JSON/GeoJSON shape, strict unknown-field behavior, project-ID strings, exact
  integer money, finite numbers, and deterministic serialization;
- artifact SHA-256 and byte-size verification plus external manifest SHA-256;
- 37 unique projects / `$327,970,000` and exact 12 / `$143,005,000` family
  reconciliation;
- source IDs, exact checksums/generations, transformation versions, coverage, and
  missingness denominators;
- `5789.150` citywide/no-feature invariant;
- current RNA 15/22 snapshot evidence retained as source-specific current state,
  without turning that count into a permanent family/schema assumption;
- an active-family catalog record with `DISPLAY_GEOMETRY_MISSING` remains valid,
  auditable, and usable for analyst-controlled Funding Plan membership without a
  corresponding map feature;
- changing a catalog record between allowed display-geometry availability states
  cannot change its locked `p0_family` value or governed request treatment;
- a geometry-backed governed record outside the exact active family remains outside
  that family and is rejected from Funding Plan membership;
- geometry, map-feature presence, spatial association, and map-layer fields are
  rejected as membership-authority inputs, and the exact family reconciliation is
  validated independently of them;
- permitted map layers and locked default visibility;
- catalog/map coverage agreement without requiring a feature for every governed or
  active-family project, no Fully Developed FloodPro feature, and no fabricated or
  null-geometry placeholder feature;
- benchmark isolation scans; and
- rejection of fixture markers, `NOT_EVALUATED_FIXTURE`, forbidden score/rank/
  weight/optimizer/benefit/imputation fields, circular manifest identity, mutable
  source pointers, and mismatched contract versions in a reviewed release.

Positive release tests use only the reviewed bundle after M5. Before then, valid
development tests use a conspicuous `FIXTURE` tier or narrowly constructed
contract objects; they cannot claim analytical completeness.

The geometry-authority cases above are M1 contract/release-validator tests. They do
not require or authorize frontend, map, API, or session implementation.

### 3. Deterministic plan engine

Enumerate all 4,096 subsets of the exact active family and independently calculate
expected totals from governed request dollars. Cover:

- `$0`, `$125,000,000`, `$1,000,000,000`, exact-total, one-dollar-under, and
  one-dollar-over boundaries;
- a valid empty plan;
- unique canonical ordering and stable fingerprint inputs;
- duplicate, malformed, unknown, and governed-but-out-of-family IDs;
- non-integer, negative, cents, string, boolean, `NaN`/infinity-equivalent, and
  over-maximum budgets at input boundaries;
- edited/partial request and client analytical fields rejected by strict schemas;
- exact `VALID` versus `OVER_BUDGET` output, remainder versus overage, included and
  active-family-not-included IDs, and warnings limited to governed context;
- independently recomputed current and reference inputs;
- comparison only when both sides are valid and only for supported deltas; and
- fingerprint mismatch visible without treating the client fingerprint as
  authentication or cached authority.

### 4. API contract and isolation

Use in-process FastAPI contract tests for HTTP status, stable typed errors,
request/release identity, strict request shapes, and safe error content.

- `/healthz` performs no dependency fan-out and exposes required identity.
- Bootstrap contains catalog/map/configuration but no benchmark treatment.
- Benchmark API failure does not affect bootstrap or plans.
- Plan evaluation preserves the current-side result when an optional reference is
  invalid and omits comparison.
- Benchmark comparison re-evaluates the untrusted plan and cannot feed the plan
  engine.
- Unknown input fields and client totals/evidence/results fail at the correct
  boundary.
- No stack trace, filesystem path, credential, prompt, source bytes, or raw
  provider response appears in errors.

### 5. Frontend reducer and component behavior

Use unit/component tests for the session reducer, storage adapter, accessible UI
components, and locally contained failures:

- one immutable Session Reference Plan and at most one What-If;
- Current Confirmed Plan points only to a freshly evaluated valid result;
- dirty, invalid, over-budget, timed-out, or failed attempts preserve the last
  successful confirmed result and header context;
- restoration calls the server before restoring confirmation/review state;
- stale data/release identity invalidates cached confirmation visibly;
- Reviewed Draft binds to the exact fingerprint and clears only under the locked
  replacement rule;
- at M4, map visibility/context and presentation search/filter/sort/layer state
  never changes analytical-family or Funding Plan membership authority;
- zero filter matches, no-family, valid zero plan, geometry missing, approved-field
  missing, unsupported, invalid attempt, and system failure remain distinct;
- Project Detail paths converge and closing/retrying preserves Explore state;
- `5789.150` remains available through list/detail/plan without a map selection;
- map defaults, neutral tile fallback, attribution, and non-map access persist;
- fixture mode is unmistakable; and
- `GEMINI_ENABLED=false` leaves all required manual behavior usable.

### 6. Gemini mediation

Mock provider calls for normal automated tests; perform only one bounded release
canary when explicitly authorized.

- Context allowlists select the minimum governed grounding.
- Plan grounding always comes from fresh server evaluation.
- Benchmark facts enter only `BENCHMARK` context.
- Constructed input stays near the initial 2,000-token bound; visible output does
  not exceed 400 tokens; `thinking_level=MINIMAL` and the fixed model/location are
  enforced.
- Citations resolve only to supplied evidence/source IDs and numeric claims match
  exact grounding strings.
- Recommendation, rank, score, benefit, beneficiary, missing-as-zero, unknown
  citation, mutation, or invented evidence responses are discarded.
- Disabled, refusal, invalid response, timeout, transient retry exhaustion,
  sustained/burst/concurrency limits, and restart-scoped limiter behavior return
  local typed states without deterministic-state change.
- Logs include allowed request/model/status/latency/retry/token fields and exclude
  prompt, response, grounding, browser state, and raw IP.

### 7. Accessibility and end-to-end workflows

Automate the critical browser path with keyboard-first coverage and supplement it
with manual inspection:

- Explore → non-map or marker Project Detail → Funding Plan → Session Reference
  Plan → one What-If → supported deltas → Reviewed Draft;
- the full manual core with Gemini disabled;
- one grounded explanation after explicit action when enabled;
- every specified loading, missing, invalid, unavailable, retry, and recovery
  state relevant to the released surface;
- visible focus, logical tab order, semantic landmarks/headings, programmatic
  labels, dialog/drawer focus management, contrast, and screen-reader names;
- tablet-width usability and desktop primary layout;
- OSM attribution, no prefetch/bulk behavior, neutral fallback, robots/noindex;
  and
- three-minute core demo rehearsal with deterministic values cross-checked against
  API output.

Conditional SP0-1 and P0-9 receive their own tests only if separately authorized;
their absence cannot fail the core release.

### 8. Build, identity, and deployment

- Build/test succeeds with source-service network access absent.
- Image contains production dependencies, compiled SPA, API, and exactly one
  reviewed bundle; it contains no raw credential, staging source, test fixture, or
  development server.
- Runtime is non-root, same-origin, one worker, and starts only after bundle and
  identity validation.
- CSP and standard security headers allow only locked application needs.
- `/healthz`, manifest bytes, environment/revision configuration, code Git SHA,
  external manifest checksum, image digest, data version, and release ID reconcile.
- No-traffic smoke tests include golden current/reference plan and benchmark
  isolation, then the full manual core with Gemini disabled.
- One authorized Gemini canary is checked against status, latency, and provider
  token logs before traffic promotion.
- Post-promotion smoke and rollback identity checks pass.

## Story Traceability

| Story | Primary evidence |
| --- | --- |
| P0-1 | terminology component tests and end-to-end header/context assertions |
| P0-2 | artifact reconciliations, all-37 audit rendering, `5789.150` treatment |
| P0-3 | map/default/fallback tests and non-map end-to-end path |
| P0-4 | evidence-role/missingness schema and Project Detail component tests |
| P0-5 | exhaustive plan-engine tests and manual Funding Plan end-to-end path |
| P0-6 | benchmark isolation, API comparison, and local-failure tests |
| P0-7 | reducer invariants, independent current/reference evaluation, recovery |
| P0-8 | Gemini grounding/post-validation/failure tests and bounded canary |
| P0-10 | exact-fingerprint Reviewed Draft reducer and end-to-end tests |
| P0-11 | provenance/reconciliation tests and Data & Methodology rendering |
| P0-12 | state matrix, keyboard/accessibility, local-failure, tablet checks |
| P0-9 / SP0-1 | excluded from core gate; tested only if separately implemented |

## Milestone Verification Commands

Commands become authoritative only when their tooling is added. The intended
check surface is:

~~~text
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m py_compile scripts/data/*.py tests/*.py
.venv/bin/python -m pip check
<application-python-environment> -m unittest discover -s tests/application -v
<application-python-environment> -m unittest discover -s tests/release -v
<frontend-package-manager> test
<frontend-package-manager> run typecheck
<frontend-package-manager> run lint
<frontend-package-manager> run format:check
<frontend-package-manager> run build
<frontend-package-manager> run test:e2e
git diff --check
~~~

M1 pins and records only the application Python runtime, dependencies, and
configuration required to implement and verify contracts and release validators.
It does not instantiate a frontend package manager/runtime, frontend package
manifest, UI scaffold, or frontend build/lint/type tooling.

The frontend package manager/runtime and its package resolution/lockfile are pinned
and reviewed at M4, the first frontend application work unit, before the frontend
angle-bracket commands become authoritative. Tooling is added only when its owning
milestone begins.

## Failure Classification and Release Rule

Every failed check is classified as product defect, test defect, environment
problem, flaky result, or unmet external prerequisite. Retrying does not convert a
flaky test into a pass. Fixture evidence, missing reviewed sources, reconciliation
failure, forbidden fields, benchmark leakage, identity mismatch, or a broken
manual core is release-blocking and is never downgraded to a warning.

The release candidate requires fresh evidence from all applicable layers above,
zero known critical defects, and explicit user authorization before deployment or
traffic promotion.
