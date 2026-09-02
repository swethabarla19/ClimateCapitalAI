# ClimateCapital AI P0 Implementation Plan

> **Status:** Approved by explicit user authorization on 2026-09-02; M0 and M1
> complete and explicitly approved
> **Authority:** Delivery sequencing and milestone scope only. The
> Product, Methodology, Evidence, and Architecture Locks remain controlling.

## Objective

Deliver the locked P0 Austin Watershed historical decision-support experience in
small, dependency-ordered milestones without changing analytical meaning or
shipping fixture evidence. The implementation must preserve the manual
Explore → Project Detail → Funding Plan journey, exact server-authoritative plan
evaluation, the isolated Historical City Recommendation, current-session browser
state, explicit evidence/missingness, and bounded grounded Gemini explanation.

This plan instantiates the implementation order in
[p0-architecture.md](../architecture/p0-architecture.md). It does not approve a
score, rank, Importance weight, optimizer, new evidence source, topology change,
or cloud resource.

## Controlling Authorities

Implementation follows the repository's existing domain authority and explicit
supersession model:

- [Repository instructions](../../AGENTS.md) govern repository work and handoff.
- [Current project state](../../PROJECT_PROGRESS.md) records the canonical current
  stage, blockers, risks, and next actions.
- The [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
  governs analytical semantics.
- Evidence/source governance in the Methodology Lock, source registry, and governed
  evidence assets controls admissible evidence and evidence states.
- The [approved product plan](../product/product-plan.md),
  [user stories](../product/user-stories.md), and
  [screen specification](../product/screen-spec.md) govern active product behavior.
- The [P0 Architecture Lock](../architecture/p0-architecture.md) and
  [data and runtime contracts](../architecture/data-contracts.md) govern technical
  and system boundaries.
- [Decision history](../decisions.md) records durable decisions and explicit
  supersessions. Later active decisions such as D-076 and D-077 supersede the
  earlier analytical mechanics identified in their status text.
- This plan, [test-plan.md](test-plan.md), and [milestones.md](milestones.md) govern
  implementation sequence only and remain subordinate to those domain authorities.

This is not a new blanket precedence ranking. Explicit supersession is honored. If
authorities genuinely conflict without an explicit resolution, implementation
stops at that detail rather than inventing a precedence rule or resolving it in
code or delivery planning.

## Locked Invariants

- Retain all 37 governed records and `$327,970,000` in governed requests.
- Retain the exact derived 12-record P0 analytical family and `$143,005,000`.
- Keep project IDs as strings and all money as whole-dollar integers.
- Keep analyst-controlled full-request membership inside the active family.
- Deterministic code validates and calculates; it never selects, ranks, scores, or
  optimizes membership.
- Missing, unsupported, not applicable, fixture-only, and numeric zero remain
  different states. Missing geometry never removes a record.
- Treat current RNA geometry as research-only and historical fit as uncertain.
- Give `5789.150` no marker, centroid, footprint, or project-level contextual
  association.
- Keep the Historical City Recommendation outside the core catalog and plan
  engine, with a one-way dependency from a freshly evaluated plan to comparison.
- Keep browser workflow state in `sessionStorage`; create no application database,
  durable session, account, approval, or sharing workflow.
- Keep Gemini explicit-action, grounded, bounded, and non-authoritative. Manual
  deterministic behavior remains complete when Gemini is disabled or unavailable.
- Release builds consume only a reviewed pinned four-file bundle and make no live
  source-service request. Fixture tier can never become a release candidate.
- Use one same-origin React/TypeScript/Vite and FastAPI/Uvicorn container, one
  worker, and the locked scale-to-zero Cloud Run boundary.

## Repository Implementation Layout

The following is the minimal target layout. A milestone creates only the paths it
owns; empty directories and speculative modules are not added.

~~~text
backend/
  climatecapital/
    api/                 # FastAPI routes, request identity, typed errors
    benchmark/           # isolated artifact repository and comparator
    contracts/           # contract constants and Pydantic request/artifact models
    gemini/              # required explanation mediation, added after manual core
    plans/               # deterministic evaluator and current/reference comparison
    release/             # bundle loader, semantic validation, runtime identity
    main.py              # one application entry point and compiled-SPA serving
frontend/
  src/
    api/                 # same-origin typed client
    components/          # shared Project Detail and contextual surfaces
    features/            # Explore, Funding Plan, benchmark, methodology/help
    session/             # reducer, storage adapter, restoration revalidation
    styles/              # accessible shared styling
  public/                # robots and local neutral map fallback assets
contracts/
  schemas/               # versioned JSON/GeoJSON request and artifact schemas
release-data/
  fixture/               # visibly marked schema-valid development bundle only
scripts/
  release/               # deterministic bundle and release-identity validators
tests/
  application/           # backend contract/engine/integration tests
  release/               # schema, bundle, isolation, and forbidden-field tests
  e2e/                   # required browser journeys and accessibility checks
~~~

Existing `scripts/data/`, `tests/test_*`, governed `data/` artifacts, and SQL
quality checks remain intact. Dependency manifests, container files, and build
configuration are introduced only in the milestone that uses them and are pinned
then; no dependency is added during this planning unit.

## Work Breakdown

### M1 — Contract and release-validator foundation

This is the first application implementation milestone after this plan is
approved.

Create the version constants and machine-enforced artifact, plan, session,
benchmark, API-envelope, and Gemini contracts already specified in
`data-contracts.md`. Implement deterministic release-bundle validation before
building business behavior.

Required outcome:

- Exact initial contract identifiers are represented once and imported by
  consumers.
- Schemas reject unknown fields, floats for money, numeric project IDs, invalid
  availability/role combinations, forbidden analytical fields, benchmark leakage,
  invalid map layers/defaults, fixture state in reviewed releases, checksum or
  cross-file identity mismatch, and governed reconciliation failures.
- The exact family reconciliation is independent of geometry: missing-geometry
  family records remain valid and auditable, while geometry cannot promote an
  out-of-family governed record into Funding Plan membership.
- `manifest_sha256` remains external; the manifest cannot contain its own checksum,
  containing Git SHA, image digest, or runtime state.
- The validator distinguishes `FIXTURE` from `REVIEWED_RELEASE` and fails closed.
- No release bundle or fixture is produced in M1, and no runtime API, UI, Gemini,
  or cloud resource is created.

Expected initial write surface:

- application Python dependency/configuration manifest;
- `backend/climatecapital/contracts/`;
- `backend/climatecapital/release/`;
- `contracts/schemas/`;
- `scripts/release/validate_bundle.py`;
- focused tests under `tests/release/` and `tests/application/`;
- only necessary package markers/configuration; and
- `PROJECT_PROGRESS.md`.

### M2A — Controlled data-track prerequisites

After M1 schemas are green, perform only the focused City-derived layer
reuse/license metadata confirmation, then controlled pinned acquisition for the
already approved benchmark, Problem Score, FEMA, and EAZ inputs. Preserve exact
bytes, source identity, checksums/generations, historical fit, and evidence roles.
Do not broaden source reconnaissance or infer unavailable claims.

### M2B — Fixture and deterministic plan engine

After M1 schemas are green, build one visibly marked `FIXTURE` bundle using
governed facts and `NOT_EVALUATED_FIXTURE` where curation is incomplete. It must
contain no invented location, association, score, beneficiary, benchmark
treatment, or analytical claim.

Implement the server-side plan evaluator:

- independently evaluate current and optional reference inputs;
- resolve request dollars from the catalog only;
- enumerate and test every one of the 4,096 active-family subsets;
- return exact totals, remainder/overage, count, canonical membership, warnings,
  and fingerprint;
- reject duplicates, unknown IDs, out-of-family IDs, edited requests, invalid
  versions, and invalid primitives; and
- compute only the supported current/reference deltas.

### M3 — Core same-origin APIs

Implement startup bundle loading, `/healthz`, bootstrap, plan evaluation, and the
isolated benchmark repository/API/comparator. Keep typed errors and request
identity stable. Benchmark failures remain local; the plan engine cannot import
benchmark data. Gemini endpoints are not part of M3.

### M4 — Application-track frontend and required surfaces

Create the React/TypeScript/Vite/Leaflet shell and accessible navigation. Implement
the exact browser-session state model, restoration revalidation, stale-identity
handling, working-plan versus confirmed-plan separation, one immutable Session
Reference Plan, at most one What-If, exact Reviewed Draft binding, and manual
full-request Funding Plan behavior. Use fixture-mode chrome while fixture data is
active.

Then, still within the Architecture-defined application track and before reviewed-
data integration, implement shared Project Detail, Data & Methodology, Help &
Resources, the map shell/default/fallback and non-map behavior, and the isolated
Historical Benchmark against the locked contracts and conspicuous fixture tier.
Map visibility, context, search, filtering, sorting, and layer state remain
presentation-only and cannot alter analytical-family or Funding Plan membership.

### M5 — Reviewed data bundle

Complete isolated benchmark extraction, contextual evidence materialization,
current RNA display geometry transformation/validation, explicit coverage and
missingness, source provenance, and all governed reconciliations. Produce the
immutable reviewed four-file bundle. Review exact bytes and the external manifest
checksum before promotion. This milestone owns evidence artifacts, not application
semantics.

### M6 — Reviewed-data integration and fixture removal

Replace fixture bytes, remove fixture mode from the release candidate, and prove
the build has no source-service dependency. Bind the already implemented Explore,
shared Project Detail, Data & Methodology, Help & Resources, locked map/non-map
behavior, and isolated Historical Benchmark to the reviewed bundle without adding
new application semantics.

### M7 — Manual-core release gate

Complete scenario recovery, last-successful-result preservation, accessibility,
OSM protections, Reviewed Draft, end-to-end manual workflow, and three-minute demo
verification with `GEMINI_ENABLED=false`. A manual-core failure blocks Gemini
implementation and deployment progression.

### M8 — Required grounded Gemini explanation

Implement only `POST /api/v1/gemini/explain` for core P0: ADC publisher access,
allowlisted grounding, independent plan evaluation, structured response,
numeric/citation guards, content-safe rendering, token/rate/concurrency/retry
bounds, redacted structured logs, and a kill switch. Provider failure remains
local. Proposal remains absent or disabled.

### M9 — Container, no-traffic deployment, and promotion

Add the multi-stage non-root image and Cloud Build/deployment configuration. Before
any cloud mutation, inspect current pricing, quotas, budgets, alerts, and Spend Cap
availability without duplicating controls. Build from the reviewed bundle, push by
immutable digest, deploy no traffic, reconcile code/data/manifest/image identity,
run smoke and one explicitly authorized Gemini canary, then promote with rollback.

### M10 — Post-core stretch only

Only after the core release candidate and contingency remain intact may the team
consider P0-9 Gemini proposal and then conditional SP0-1 Compare. Compare remains
the first scope cut; proposal remains the second. Neither may change core
contracts or block release.

## Dependency and Integration Rules

- M0 planning approval precedes M1.
- M1 precedes both M2A and M2B; those tracks may then proceed independently.
- M2B, M3, and M4 implement the Architecture application-track steps in order.
- M4 application-track completion and M5 reviewed-data approval both precede M6
  release integration.
- M6 and M7 precede M8; M8 precedes M9 promotion.
- Shared schema, lockfile, manifest, generated artifact, and release-identity
  changes are serialized under one owner.
- Every milestone ends with a clean reviewable diff, focused and broad checks,
  `git diff --check`, and a current `PROJECT_PROGRESS.md` handoff.
- A failed prerequisite blocks the dependent milestone; it does not authorize a
  substitute source, inferred metric, extra service, or weaker validator.

## Cost and Cloud Boundary

M0 through M8 are local by default. M2A may read approved source services and
preserve exact artifacts only when separately authorized. M9 is the first
infrastructure/deployment milestone. No milestone provisions Cloud SQL,
Firestore, Redis, a runtime warehouse, a separate frontend, a load balancer, CDN,
VPC connector, user identity, or another rejected service.

## Approval Gate

Explicit approval of this plan on 2026-09-02 authorizes M1 only. The approval
record does not begin M1 and does not authorize M2A acquisition, cloud mutation,
M9 deployment, commit, or push. Each completed milestone must be reviewed before
the next begins unless the user separately authorizes a broader sequence
consistent with the locked dependency order.

M1 received independent closure-audit approval on 2026-09-02. That approval
satisfies the M1 review gate; no M2 or later work began in the approval session.
