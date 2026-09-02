# ClimateCapital AI P0 Architecture Lock

> **Status:** Approved and locked on 2026-09-01
> **Authority:** This document is the authoritative implementation architecture for
> P0. The analytical method remains authoritative in
> [p0-evidence-methodology.md](../methodology/p0-evidence-methodology.md), and the
> normative application and data contracts are in
> [data-contracts.md](data-contracts.md).

## Locked Outcome

P0 uses one small public Cloud Run service containing a React/TypeScript/Vite
single-page application and a Python FastAPI API. The application consumes a
reviewed, versioned release-data bundle packaged into the container. Runtime code
does not query BigQuery, Cloud Storage, ArcGIS, FEMA, EAZ, or another source
service. Deterministic server code independently validates every submitted plan
and performs all authoritative arithmetic. Browser `sessionStorage` holds the
bounded current-session workflow state; there is no application database or
server-side session store.

This is the smallest architecture that supports Explore → Project Detail → manual
Funding Plan → one What-If → evidence/provenance → grounded Gemini explanation
while preserving explicit missing and unsupported states. Natural-language plan
proposal is post-core stretch and cannot block release.

## Component Diagram

~~~text
CONTROLLED SOURCE PREPARATION                         RELEASE / RUNTIME

Official source services and documents
        │  explicit acquisition only
        ▼
Pinned exact source snapshots ───────► Cloud Storage raw preservation
        │                               (existing bucket; no runtime reads)
        ├────────────────────────────► Existing BigQuery raw validation
        │                               (existing table + SQL release gate only)
        ▼
Deterministic extraction / joins / evidence classification
        │
        ▼
Reviewed versioned release-data bundle
  catalog.json
  map-context.geojson
  benchmark.json  ── structurally separate
  manifest.json
        │
        │ release build consumes only these pinned files
        ▼
One bounded container image in Artifact Registry
        │
        ▼
One public Cloud Run service, us-central1, min 0 / max 1
  ┌──────────────────────────────────────────────────────────┐
  │ One FastAPI/Uvicorn process, one application worker      │
  │  ├─ serves compiled React SPA and robots protections     │
  │  ├─ loads immutable release-data bundle                  │
  │  ├─ independently evaluates current/reference plans      │
  │  ├─ exposes isolated benchmark comparison                │
  │  └─ mediates bounded Gemini 3.6 Flash explanations       │
  └──────────────────────────────────────────────────────────┘
        ▲                         │
        │ same-origin HTTPS       └── Google Cloud publisher endpoint
        │                             global on-demand Gemini access via ADC
Browser SPA
  ├─ sessionStorage only
  ├─ direct configurable OSM tiles with attribution
  └─ neutral non-basemap fallback
~~~

## Source-to-Application Data Flow

Source preparation and release construction are separate operations.

1. A controlled, explicitly authorized acquisition step captures exact source
   bytes and metadata. It validates source identity, records SHA-256, and pins the
   Cloud Storage generation when an object is preserved there.
2. Deterministic extractors and transformations consume only those pinned inputs.
   They retain the all-37 governed universe, derive the locked 12-record family,
   materialize evidence role/availability/provenance, and keep benchmark data on a
   separate path.
3. Data validation reconciles 37 governed records / $327,970,000, the exact 12
   family records / $143,005,000, evidence coverage/missingness, geometry states,
   and benchmark identity. The existing BigQuery raw table and SQL quality suite
   are a release gate, not a runtime dependency and not a reason to create staging
   or curated warehouse tables.
4. Review promotes the outputs to a versioned release-data bundle. The bundle and
   exact manifest bytes are immutable for that `data_version`.
5. The release build consumes only the reviewed bundle. It must not contact live
   ArcGIS, City, FEMA, EAZ, OSM, or other data/source endpoints. A source changing
   or becoming unavailable cannot change or break the release build.
6. The built container loads the bundle at startup and fails closed on schema,
   checksum, reconciliation, release-tier, or identity mismatch.
7. At runtime, the browser requests governed application data from the same-origin
   API. The server resolves plan IDs to immutable catalog values and returns fresh
   deterministic results. Contextual GIS is already precomputed; no runtime
   spatial query occurs.

No release candidate may contain fixture evidence. A schema-valid fixture bundle
may unblock application development after schemas are locked, but the final
integration gate must replace it with the reviewed, pinned release-data bundle.

## Storage and Processing Boundaries

### Cloud Storage

Use the existing raw bucket for immutable exact source snapshots and their
generation-specific provenance. It is a controlled preparation input and recovery
asset. The Cloud Run runtime identity receives no bucket permission and the
application does not serve source data from the bucket.

### BigQuery

Retain the existing `raw.watershed_projects_2025_11_21` table and durable SQL
quality checks. Rerun those checks when the governed raw snapshot is used for a
release. Do not add staging, curated, benchmark, application, or session tables
merely for architectural symmetry. BigQuery is not queried by builds or runtime.

### Build-time application artifacts

Package the reviewed release-data bundle into the runtime image:

- `catalog.json`: all 37 governed records, locked family membership, evidence
  states, provenance, and non-geographic project handling;
- `map-context.geojson`: precomputed display geometry and contextual layer
  features with role, source, vintage, and caveat metadata;
- `benchmark.json`: separately sourced Historical City Recommendation data only;
- `manifest.json`: data contract, sources, checksums, transformations,
  reconciliations, coverage/missingness, and benchmark identity.

The exact normative fields and checksum rules are in
[data-contracts.md](data-contracts.md).

### Runtime and session state

Runtime data is immutable in-process application data. Current-session workflow
state is browser `sessionStorage`; the API keeps no plan/session record. In-memory
Gemini limiters are transient operational controls only.

## Contextual GIS and Map Defaults

All application-shipped geometry and contextual GIS associations are prepared and
validated before the release build. Runtime does not execute spatial joins or call
GIS services.

- Direct OpenStreetMap Standard tiles are the default small-demo basemap.
- Current RNA project display geometry is visible where available and is clearly
  labeled current/research-only with its limitations.
- FEMA contextual hazard is off by default and user-enabled through **Layers**.
- EAZ 2021 is off by default and user-enabled through **Layers**.
- Fully Developed FloodPro is not shipped in P0.
- Projects without geometry remain fully usable through Projects, Project Detail,
  Funding Plan, methodology, and Gemini explanation paths.
- Project `5789.150` is a citywide program. It receives no fabricated marker,
  point, centroid, or footprint and uses an explicit non-project-geography state.

For direct OSM use, the application must show visible attribution, preserve normal
browser `Referer` behavior, honor HTTP/browser cache controls, avoid cache-bypass
parameters, and perform no bulk download, prefetch, scraping, offline tile
generation, or proxying. The tile provider is configuration-driven. If tiles are
unavailable or direct use is no longer appropriate, the UI retains a neutral local
non-basemap background and every required non-map path.

The competition deployment includes `robots.txt` with `Disallow: /`, a
`noindex,nofollow,noarchive` meta directive, an equivalent `X-Robots-Tag`, and no
sitemap. These discourage crawler traffic; they are not access control.

## Runtime and Frontend Boundary

### Runtime backend requirement

A backend is required for three bounded responsibilities:

1. authoritative plan validation/arithmetic and independently recomputed
   current/reference comparisons;
2. isolated benchmark comparison against a freshly evaluated analyst plan; and
3. authenticated, grounded, rate-bounded Gemini access without a browser key.

FastAPI/Pydantic provides explicit contracts and reuses the project's Python data
tooling. One Uvicorn application worker runs in one process. Cloud Run maximum
instances remains one; do not add Redis, Firestore, or another rate-limit store.

### Frontend responsibilities

The React/TypeScript/Vite frontend owns rendering, accessible interaction,
presentation-only filters, map state, local pending edits, and the bounded session
workflow. It may display server results but does not author governed facts or
calculate authoritative totals. It never treats cached result fields as valid
after a reload or data-identity change until the server re-evaluates the stored
budget and IDs.

Leaflet is the P0 map library. The SPA and API are same-origin from one Cloud Run
service, avoiding a separate frontend deployment, public CORS surface, load
balancer, or CDN.

## Session-State Model

The browser stores only the current session and clears it when that browser tab's
session ends. The exact reducer/state shape is specified in
[data-contracts.md](data-contracts.md). The lifecycle is:

1. Start with an unconfirmed working plan under the $125,000,000 Historical
   Envelope context.
2. The first valid analyst-confirmed plan under that context becomes the immutable
   Session Reference Plan for the current session.
3. The analyst may create and confirm at most one What-If with a different budget,
   membership, or both.
4. Current Confirmed Plan points to the Session Reference Plan or the confirmed
   What-If. Attempted edits remain separate until valid confirmation.
5. Invalid, unknown-ID, duplicate, out-of-family, or over-budget attempts do not
   replace the last confirmed result.
6. Reviewed Draft binds to the exact server-evaluated plan fingerprint and is
   current-session, non-persistent, non-official state.
7. On restoration, the client submits stored budget and IDs for fresh server
   evaluation before showing a confirmed or reviewed result. A `data_version` or
   fingerprint mismatch invalidates the cached confirmation and requires visible
   review.

There are no users, accounts, durable workflow records, approvals, collaboration,
sharing, or persistence database in P0.

## Deterministic Funding Plan Trust Boundary

The client may submit only a contract version, expected data version, whole-dollar
budget, project IDs, and an optional expected fingerprint. It may submit separate
current and reference plan inputs in one request.

For both current and reference plans, the backend independently:

- rejects unknown IDs, duplicates, and governed IDs outside the active family;
- resolves each request amount from the immutable catalog;
- applies full-request inclusion only;
- computes included/not-included IDs, count, exact integer-dollar total,
  remaining amount, and over-budget state;
- computes a canonical fingerprint; and
- computes supported deltas only from the two freshly evaluated results.

Client-supplied totals, costs, remainders, deltas, scores, evidence values, or
other analytical values are forbidden and never authoritative. A fingerprint is a
verification hint, not authentication or an authoritative result lookup. This
same boundary applies to session restoration, benchmark comparison, Gemini
explanation grounding, and any later Gemini proposal.

The deterministic engine validates analyst membership; it never ranks projects,
selects membership, or searches for a preferred combination. No partial-funding
path exists.

## Historical Benchmark Isolation

The Historical City Recommendation follows its own raw source → extractor →
reviewed `benchmark.json` → benchmark repository/API → comparator → UI path.

The core catalog, family derivation, evidence contracts, and plan engine may not
import benchmark data. The benchmark comparator depends on a freshly evaluated
analyst plan; the plan engine never depends on benchmark data. Gemini may receive
benchmark material only for an explicitly benchmark-scoped explanation and may
not use it to explain or determine family membership, evidence, or analyst plan
membership.

## Runtime API Surface

All endpoints use same-origin HTTPS and `/api/v1` contracts. Details are in
[data-contracts.md](data-contracts.md).

| Endpoint | P0 purpose |
| --- | --- |
| `GET /healthz` | Health plus deployment/runtime identity; no dependency fan-out |
| `GET /api/v1/bootstrap` | Versioned catalog, map context, map defaults, evidence/source metadata, and UI configuration |
| `GET /api/v1/benchmark` | Separately loaded benchmark identity and published treatment |
| `POST /api/v1/plans/evaluate` | Independently evaluate current and optional reference inputs and return supported differences |
| `POST /api/v1/benchmark/compare` | Re-evaluate submitted analyst plan inputs, then compare to the isolated benchmark |
| `POST /api/v1/gemini/explain` | Required grounded P0 explanation of supported project, plan, benchmark, methodology, or provenance context |

`POST /api/v1/gemini/propose` is a post-core stretch endpoint. Manual Funding Plan
interaction must be complete without it. The endpoint remains feature-flagged,
cannot block release, and if implemented may only translate an explicit budget or
named-membership command into a pending action that still passes the normal plan
trust boundary after analyst confirmation.

No generic query API, runtime GIS endpoint, arbitrary SQL endpoint, CRUD/session
API, upload API, or administrative API is required.

## Gemini Grounding and Mediation

### Required capability and model access

- Use `gemini-3.6-flash` through the Google Cloud/Agent Platform publisher
  endpoint with global standard on-demand model access.
- Use the Cloud Run service account through workload identity/ADC. Do not use an
  AI Studio API key.
- Do not opt into Priority or Provisioned Throughput.
- Use `thinking_level=MINIMAL`.
- Use a non-streaming structured response and no automatic model fallback.
- Start with an approximately 2,000-token total constructed input limit. Increase
  toward 3,000 only if tests demonstrate that the required explanation quality
  cannot fit.
- Target about 350 visible output tokens and enforce a 400-token maximum.
- Make model calls only after explicit user action; never call Gemini on page load.
- `GEMINI_ENABLED=false` disables all model calls while deterministic/manual P0
  remains usable.

The server accepts context references and a bounded user question, then selects
the minimum governed fields from its own catalog. It re-evaluates any plan inputs,
constructs the grounding package, calls the model, validates the structured
response, rejects unknown citations or unsupported numeric claims, and renders
sanitized text. The model never receives authority to create facts, totals,
membership, scores, ranks, benefits, or missing evidence.

### Rate and abuse controls

Because P0 runs one FastAPI/Uvicorn worker, the primary in-memory global limiter
lives in one application process:

- approximately 2 model calls per minute sustained;
- burst 2;
- at most 2 concurrent Gemini calls;
- one bounded transient retry, which also consumes limiter capacity;
- Cloud Run maximum instances 1; and
- an additional bounded best-effort per-client/IP token bucket where practical.

The per-client/IP limiter uses bounded memory, does not persist raw IP addresses,
and resets on process restart. It is neither a security control nor a hard spend
guarantee. Process restarts also mean the in-memory global bound is operational,
not an account-level quota. Do not introduce Redis, Firestore, or another
persistence service for P0 rate limiting.

Structured logs may record request ID, operation, model, status, latency, retry
count, and provider-reported input, visible-output, reasoning/thinking, and total
token counts. They must not record prompts, responses, grounding packages, browser
session state, or raw IP addresses.

## Deployment Topology

- Region: `us-central1` for Cloud Run, Cloud Build execution, and Artifact
  Registry repository placement where configurable. Gemini uses its global
  publisher endpoint.
- One multi-stage, non-root runtime image containing only production Python
  dependencies, compiled SPA assets, API code, and the reviewed data bundle.
- One public Cloud Run service on its managed `run.app` URL.
- Request-based billing, minimum instances 0, maximum instances 1, one Uvicorn
  worker, 1 vCPU, and 512 MiB memory initially.
- No custom domain, load balancer, CDN, VPC connector, or separate frontend host.
- The runtime service account receives only the permission needed to invoke the
  selected publisher model. Standard output/error is captured by the Cloud Run
  platform; the application receives no extra data-service permission and no
  runtime BigQuery or Cloud Storage access.

Artifact Registry retention stays bounded. Use deployment/rollback labels or tags
for the current deployed image and one prior rollback image. After a successful
deployment, a cleanup policy removes older untagged, unneeded images after a short
safety period. Keep the runtime image below the 0.5 GiB Artifact Registry free-tier
allowance where practical.

## Reproducible Release and Runtime Identity

`manifest.json` describes data, not the deployment that contains it. It must not
contain a Git SHA for a commit that contains the manifest, and it must not contain
its own checksum. After the manifest bytes are final, release tooling computes
`manifest_sha256` externally.

Deployment/runtime identity separately exposes:

- `code_git_sha`;
- `data_version`;
- external `manifest_sha256`; and
- deployed container image digest plus a human-readable release identity.

The image digest is known only after image creation/push and is injected or bound
at deployment time; it is not embedded circularly into the image contents.
`GET /healthz`, the Cloud Run revision configuration, and release verification must
agree on all four identities. A mismatch blocks traffic promotion.

## Authentication, Security, and Configuration

P0 contains public, read-only decision-support data and current-session local
workflow state. It has no end-user login. Cloud Run permits unauthenticated access
to the application, while deployment and cloud administration remain IAM
protected.

- Use same-origin API calls, strict Pydantic input schemas, length/count limits,
  integer budget bounds, project-ID validation, and explicit response contracts.
- Set a restrictive Content Security Policy compatible with the configured tile
  and publisher-independent frontend needs, plus standard MIME, framing, referrer,
  and transport headers.
- Render source/model text as encoded or sanitized text, never trusted HTML.
- Do not store credentials in Git, images, source metadata, prompts, or browser
  code.
- ADC/workload identity means Gemini requires no application secret. Non-secret
  configuration such as `GEMINI_ENABLED`, model name, data identity, tile URL,
  attribution, and rate parameters uses validated environment variables.
- Do not add Secret Manager unless a later concrete secret exists.
- Before application-shipped City-derived layers are finalized, perform only a
  focused metadata/license/reuse confirmation and retain visible/source-level
  attribution and disclaimers. Do not reopen broad source reconnaissance.

## Observability and Error Handling

P0 observability is intentionally small:

- `GET /healthz` reports healthy startup and deployment identity without querying
  external services;
- built-in Cloud Run request, latency, instance, error, and resource metrics;
- bounded structured Cloud Logging for request IDs, route/status/latency, failure
  category, data/release identity, deterministic evaluation outcome category, and
  the non-content Gemini usage fields above; and
- deployment smoke tests before and after traffic promotion.

Do not add synthetic-monitoring infrastructure, elaborate dashboards, third-party
observability, or distributed tracing for P0 unless a concrete deployment failure
demonstrates the need. Errors remain local to the affected surface; a Gemini,
benchmark, tile, or contextual-layer failure never invalidates a successful plan
result.

## Testing and Release Verification

The later test plan must instantiate these locked layers:

1. **Schema/artifact tests:** JSON/GeoJSON contracts, exact checksums, source IDs
   and generations, evidence roles, missingness, release-tier, 37/$327,970,000 and
   12/$143,005,000 reconciliations, geometry/non-geometry states, benchmark
   identity, and forbidden-field scans.
2. **Deterministic unit/property tests:** all 4,096 subsets of the 12-record family,
   exact integer totals, boundary budgets, valid zero-project plan, duplicates,
   unknown/out-of-family IDs, partial/edit attempts, canonical fingerprints, and
   supported current/reference deltas.
3. **API contract tests:** current and reference are independently recomputed;
   client totals/analytical fields are rejected or ignored as invalid input;
   benchmark isolation; data-version mismatches; stable typed errors; health
   identity.
4. **Frontend reducer/component tests:** session lifecycle, restoration
   revalidation, stale identity, presentation/scenario separation, last-confirmed
   preservation, map defaults, non-map `5789.150`, Reviewed Draft binding, and
   Gemini-disabled behavior.
5. **Gemini mediation tests:** grounded payload selection, approximately 2,000
   input-token bound, output bound, structured validation, numeric/citation guard,
   refusal, kill switch, rate/concurrency limits, retry budget, redacted logs, and
   deterministic fallback. Provider calls are mocked except for a bounded release
   canary.
6. **Accessibility and end-to-end tests:** keyboard/focus/labels/contrast, every
   non-map path, manual three-minute core journey, errors/recovery, OSM attribution
   and fallback, and no proposal dependency.
7. **Build/deployment tests:** release build succeeds with source-service access
   absent, contains no fixture tier, uses the reviewed checksums, and reconciles
   code/data/manifest/image identity.

Deployment verification order:

1. validate the reviewed release bundle and external manifest checksum;
2. rerun the existing BigQuery raw SQL quality gate;
3. run the full repository test/build/check suite;
4. build without live source acquisition or source-service access;
5. push by immutable image digest and create a no-traffic Cloud Run revision;
6. reconcile `/healthz`, revision configuration, data manifest, and image digest;
7. run golden current/reference plan and benchmark-isolation checks;
8. run the complete manual core journey with `GEMINI_ENABLED=false`;
9. enable Gemini if authorized and run one grounded explanation canary;
10. inspect status/latency/token-count logs for that canary;
11. shift traffic, rerun core smoke tests, and retain the previous image/revision
    for rollback.

## Local Development Workflow

1. Install pinned Python and frontend dependencies in ignored local environments.
2. Validate schemas and build a clearly marked, schema-valid fixture release-data
   bundle from already governed facts. Fixture-only technical states may not be
   presented as analytical evidence and the UI must visibly identify fixture mode.
3. Develop the deterministic engine/API and frontend against the exact production
   schemas while the separate data track completes controlled curation.
4. Run the API and Vite development server locally, with same-origin proxying and a
   neutral map fallback available.
5. Keep Gemini disabled by default locally; use ADC and the same mediation path
   only for explicitly authorized integration checks.
6. Replace fixtures with the reviewed pinned release bundle for integration.
7. Run the complete release validation/build locally or in Cloud Build without
   live source acquisition.

No application implementation begins until the post-lock implementation, test,
and milestone plans are approved.

## GCP Services Used and Why

| Service/capability | P0 use |
| --- | --- |
| Cloud Storage | Existing immutable raw source preservation only |
| BigQuery | Existing governed raw-table validation and SQL release gate only |
| Cloud Build | Reproducible test/build/deploy pipeline |
| Artifact Registry | One bounded container repository with current + rollback retention |
| Cloud Run | Single public scale-to-zero SPA/API deployment |
| Gemini publisher endpoint | Required grounded explanation through `gemini-3.6-flash` |
| IAM/workload identity | Deployment authorization and keyless runtime model access |
| Cloud Logging and built-in Cloud Run metrics | Bounded operational and token-usage evidence |
| Cloud Billing controls | Existing alerts/budgets/spend caps where available, after inspection |

## Explicitly Rejected or Unnecessary for P0

- Cloud SQL, Firestore, Spanner, AlloyDB, Memorystore/Redis, or another application
  or rate-limit database;
- runtime BigQuery or Cloud Storage access;
- BigQuery staging/curated/benchmark/session tables created for completeness;
- Dataflow, Dataproc, Composer, Pub/Sub, Eventarc, Scheduler, or live ETL;
- Cloud Functions, GKE, Compute Engine, or App Engine;
- separate frontend hosting, API Gateway, load balancer, custom domain, CDN, VPC,
  or Cloud Armor;
- Identity Platform, user accounts, durable sessions, collaboration, or approval
  workflow;
- AI Studio keys, Priority/Provisioned Throughput, model fallback, RAG/vector
  databases, Agent Engine, or an open-ended agent;
- runtime GIS/source queries, Fully Developed FloodPro, tile proxying, bulk/offline
  OSM tiles, or fabricated geometry;
- synthetic monitors, elaborate dashboards, third-party observability, or a
  separate tracing stack; and
- scoring, ranking, weights, optimization, partial funding, beneficiary estimates,
  or any data field that implies them.

## Cost Expectations and Controls

Pricing assumptions were checked on 2026-09-01 and must be rechecked before
deployment.

### Expected normal demo cost

Ordinary spend should be near zero. With Cloud Run minimum instances 0 and a small
demo workload, compute is expected to remain inside the request-based free tier.
The small existing raw data, bounded image repository, Cloud Build minutes,
BigQuery validation queries, and logs are also expected to remain within their
respective free allowances. A few hundred Gemini explanations should cost well
under a few dollars under the current standard pricing, plus uncertain billable
thinking tokens.

### Free-tier assumptions

Current documentation lists monthly free allowances including 2 million Cloud Run
requests with compute allowances, 1 TiB of BigQuery on-demand query processing,
2,500 Cloud Build minutes, the first 0.5 GiB of Artifact Registry storage, and the
first 50 GiB of Cloud Logging ingestion. Cloud Storage for this small footprint is
only cents per GiB-month outside any allowance. Free tier eligibility, regions,
and billing-account aggregation must be verified rather than assumed.

### Gemini thinking-token uncertainty

Current Gemini 3.6 Flash standard global pricing is $0.75 per million input tokens
and $3.75 per million output/reasoning tokens through the published pricing period.
Reasoning/thinking tokens are billable. A 2,000-input/350-visible-output call is
approximately $0.00281 using visible tokens only; this is an estimate, not a
maximum. The earlier 3,000-input/400-visible-output shape is approximately $0.00375
using visible tokens only and likewise is not a maximum. Actual cost can be higher
because provider-reported reasoning tokens are billed even when not visible.

### Public-abuse risk and application controls

At a continuous 2 calls/minute, the theoretical steady-state exposure is about
2,880 calls/day, or approximately $8.10/day using the 2,000/350 visible-token
estimate before reasoning tokens and Cloud Run cost. Burst behavior, retries,
process restarts, and billable thinking mean this is not a hard ceiling. Maximum
instances 1, one worker, global burst/sustained/concurrency limits, bounded input
and output, per-client best-effort protection, the kill switch, and no automatic
calls reduce exposure but do not replace account-level billing controls.

### Billing controls

Inspect the project and billing account for existing budgets, alerts, quotas, and
available Spend Caps before creating or changing anything. Do not create duplicate
budgets. Reuse suitable existing notifications. If Cloud Billing Spend Caps are
available for this account, a small cap may be an additional guard, but Preview
Spend Caps are not a correctness or availability dependency. Billing budgets and
alerts notify; they do not themselves cap spend.

### Post-demo shutdown

After the evaluation window, set `GEMINI_ENABLED=false`, confirm Cloud Run minimum
instances remains zero, inspect Gemini token usage and billing, remove older
Artifact Registry images under the cleanup rule, and retain only the current and
rollback images while review continues. Making the service private or deleting it
is a separate authorized action because it changes the public submission surface.

The architecture target remains comfortably below the $300 Google Cloud credit,
but public abuse and thinking-token uncertainty mean credits are not treated as a
spend bound.

Official pricing/control references:

- [Cloud Run pricing](https://cloud.google.com/run/pricing)
- [BigQuery pricing](https://cloud.google.com/bigquery/pricing)
- [Cloud Storage pricing](https://cloud.google.com/storage/pricing)
- [Cloud Build pricing](https://cloud.google.com/build/pricing)
- [Artifact Registry pricing](https://cloud.google.com/artifact-registry/pricing)
- [Cloud Logging pricing](https://cloud.google.com/products/observability/pricing)
- [Gemini generative AI pricing](https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing)
- [Cloud Billing budgets](https://cloud.google.com/billing/docs/how-to/budgets)
- [Cloud Billing Spend Caps](https://cloud.google.com/billing/docs/how-to/budgets-spend-caps)
- [OpenStreetMap tile usage policy](https://operations.osmfoundation.org/policies/tiles/)

## Major Risks and Locked Responses

| Risk | Locked response |
| --- | --- |
| Evidence curation finishes late | Run data and application tracks after schema lock; integrate only the reviewed bundle; never ship fixtures |
| A live source changes or fails | Controlled snapshotting is separate; release builds consume pinned artifacts only |
| Missing or misleading geography | Precompute defensible display context, preserve non-map access, and give 5789.150 no fabricated geometry |
| Client tampers with plan results | Re-evaluate current and reference inputs independently from the server catalog |
| Benchmark leaks into analysis | Separate artifact, repository, API, comparator, and UI path; dependency is one-way from evaluated plan to comparator |
| Gemini invents or overspends | Server grounding/post-validation, bounded tokens/rates/concurrency, kill switch, token logs without content, and billing controls |
| Public crawler/tile traffic | Noindex/robots discouragement, direct compliant browser use, no prefetch, configurable provider, neutral fallback |
| Cloud Run cold start or external outage | Small image, no runtime data dependencies, manual core path, local failures, deployment canary and rollback |
| Identity drift | External manifest checksum plus separate code/data/image identity reconciled by `/healthz` and release verification |
| Deadline pressure | Core manual plan and required explanation first; cut Compare and proposal stretch before required contracts or QA |

## Implementation Work Units in Dependency Order

1. Persist this Architecture Lock and reconcile Product/Design/delivery/reference
   documentation. **This documentation-only unit.**
2. Create and approve architecture-informed implementation, test, and milestone
   plans. No application code begins before this gate.
3. Implement and lock versioned artifact, API, session, plan, benchmark, and Gemini
   schemas/contracts plus release validators.
4. After schema lock, run two coordinated tracks:

   **Data track**

   1. Perform focused reuse/license metadata confirmation for application-shipped
      City-derived layers.
   2. Run controlled acquisition only for already-approved benchmark, Problem
      Score, FEMA, and EAZ inputs; pin exact artifacts/generations.
   3. Extract the Historical City Recommendation on its isolated path.
   4. Materialize Problem Score, FEMA, and EAZ contextual evidence plus current RNA
      display geometry with explicit coverage/missingness and 5789.150 treatment.
   5. Produce and review the final versioned release-data bundle, manifest,
      checksums, provenance, and governed reconciliations.

   **Application track**

   1. Build a schema-valid, visibly marked fixture bundle containing governed facts
      and technical fixture states but no invented analytical claims.
   2. Implement the deterministic Funding Plan engine, both-input trust boundary,
      fingerprints, and exhaustive subset tests.
   3. Implement health, bootstrap, plan, and benchmark API contracts.
   4. Implement the frontend shell, session reducer, restoration revalidation, and
      non-map/manual Funding Plan workflow.
   5. Implement Project Detail, methodology/help, map shell/default behavior, and
      isolated Historical Benchmark against the locked contracts.

5. Integrate the reviewed pinned release-data bundle and remove fixture mode from
   the release candidate. Prove a release build has no live source dependency.
6. Complete manual Session Reference Plan, What-If, Reviewed Draft, recovery,
   accessibility, map defaults, OSM protections, and end-to-end core tests.
7. Implement required `POST /api/v1/gemini/explain`, grounding/post-validation,
   rate/concurrency controls, kill switch, usage logging, and failure behavior.
8. Implement container/Cloud Build/Artifact Registry cleanup/Cloud Run deployment,
   inspect existing billing controls, and run no-traffic verification.
9. Promote a core release candidate only after the reviewed-data, manual-core,
   required-explanation, identity, accessibility, and deployment gates pass.
10. Only if the core candidate and contingency remain intact, implement
    `POST /api/v1/gemini/propose` as feature-flagged post-core stretch. Failure or
    delay leaves the core candidate unchanged.
11. Rehearse, freeze, submit, verify links, and perform the authorized post-demo
    cost-control procedure.

The two tracks are parallel only after shared schemas are locked. Final integration
and all release gates are serialized on the reviewed release-data bundle.

## First Cuts Under Schedule Pressure

Cut in this order:

1. conditional exactly-two-project Compare (SP0-1);
2. natural-language Gemini proposal (`POST /api/v1/gemini/propose`, P0-9);
3. custom domain/CDN work, already unnecessary;
4. rich benchmark visualizations beyond required descriptive facts;
5. additional map styling, secondary filters, or layer polish;
6. multi-turn Gemini history or extra explanation intents; and
7. observability automation beyond health, built-in metrics, bounded logs, and
   smoke tests.

Do not cut deterministic plan validation/arithmetic, independent current/reference
evaluation, explicit evidence/missingness states, all-37 audit, non-map access,
5789.150 treatment, benchmark isolation, manual session behavior, the required
grounded explanation, accessibility/recovery, reproducible release identity, or
deployment verification.

## Change Control

Changes to the service topology, runtime trust boundary, persistence model,
authoritative data/API contracts, benchmark isolation, Gemini authority, map
defaults, release reproducibility, or deployment identity require an explicit
Architecture decision. A methodology change remains governed separately by
[p0-evidence-methodology.md](../methodology/p0-evidence-methodology.md).
