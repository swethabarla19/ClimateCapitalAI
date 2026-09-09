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

- **Last updated:** 2026-09-09
**Project stage:** F6, F7A, F7A.1, F7B.1, and F7B.2 are complete and accepted.
  F7B remains paused until the accepted F7B.2 correction is published at a new
  exact frozen SHA.
- **Current milestone:** F7B.2 production Gemini logging remediation is complete
  and accepted. Existing cloud candidates remain private and superseded for final
  production.
- **Next gate:** Resume F7B only from the exact Git SHA containing the accepted
  F7B.2 correction. One replacement Vertex canary is authorized solely to verify
  repaired Cloud Logging/token metadata. F7C has not begun.
- **Working state:** The prior deployment SHA
  `ed4f14b94f0ba469ccc4ef04c3c3d7552abfbd1f` is superseded for final production
  by the accepted F7B.2 logging correction. F7B must rebuild from the exact Git
  SHA produced when this correction is published. `.node-version` remains
  untouched.
- **Delivery context:** The completed/deployed application remains the delivery goal. Geometry promotion changes map evidence only and does not change Product methodology, analytical authority, Funding Plan, Funding Priority, requests, PRB values, or Historical Benchmark.

- **Data/methodology state:** All 106 projects remain model-eligible and ordinally ranked by official PRB Grand Total. M3.7D authorizes Priority-Constrained Analyst-Governed Portfolio Construction using full-request project costs and analyst-supplied Available Project Budget. The $332M matched-cohort amount is a benchmark scenario; $700M and $750M remain broader historical references.
- **Runtime boundary:** `cross_category_ranking_authorized=true`; `portfolio_selection_authorized=true`; `runtime_integration_authorized=true` for active runtime-v3. Runtime-v2 remains immutable historical release provenance; earlier M3.7 artifacts correctly retain `runtime_integration_authorized=false`.
- **M3 runtime state:** Standard `/api/v1/bootstrap` serves the unchanged 106-project catalog plus D-116 runtime-v3 map context; `/api/v1/plans/evaluate` executes the unchanged M3.7D state machine; `/api/v1/benchmark` serves the byte-identical isolated January historical outcome. `/api/v1/benchmark/compare` remains explicitly unavailable.
- **Most recent verification:** The new production-style regression first failed
  with zero emitted records, then passed after centralized configuration. All 50
  focused Gemini and deployment-readiness tests pass with two known dependency
  warnings. The captured stderr record appears exactly once with request, surface,
  model, status, latency/retry/token metadata and no prompt, response, grounding,
  raw client key, or hidden instruction content; Uvicorn/root logger state is
  unchanged and the application logger is restored after shutdown.

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
- **Methodology Lock — M3.7D cross-category portfolio construction:** All 106 governed
  analytical projects remain ranked by official ordinal PRB Funding Priority.
  Portfolio construction now uses indivisible full-request projects, analyst-supplied
  Available Project Budget, complete-tier inclusion when feasible, boundary-tier
  budget feasibility, and explicit analyst resolution where multiple equal-priority
  alternatives remain feasible. Cardinal PRB optimization, score-per-dollar,
  cheapest-first, project-count maximization, budget-utilization maximization,
  unsupported category quotas, and hidden analytical tiebreakers are prohibited.
  Cross-category ranking and portfolio-selection methodology are authorized;
  runtime integration is authorized through the immutable runtime release.
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

- **Goal:** Complete F7 sequentially without changing locked product, methodology,
  governed data, deterministic Funding Plan behavior, or Gemini authority.
- **Status:** F7B.2 passes locally. F7B remains paused until this source patch is
  reviewed, committed, pushed, frozen, rebuilt, and privately reverified.
- **Readiness boundary:** The user explicitly authorized bucket-only
  `roles/storage.objectViewer` for the effective build account, and the already-
  authorized repository-only Artifact Registry Writer grant was applied after its
  exact push denial. The subsequent build passed. Cloud Run rejected `--no-traffic`
  for first-service creation, so the core revision was created with 100% private
  traffic and Invoker IAM enforcement; anonymous access returns 403.
- **Authority:** F7B.2 changes only centralized production application logging,
  one focused test, and this progress record. It does not change the Gemini event,
  authority/model/methodology, Uvicorn behavior, governed data, cloud state,
  credentials, commit, or push.
- **Exit condition:** Stop for manual review/commit/push and a new frozen SHA. Do
  not rebuild/deploy or use the one replacement canary until F7B resumes.

## Next Actions

1. Manually review the narrow F7B.2 production logging patch and verification.
2. Commit/push the accepted patch, confirm `HEAD == origin/main`, and freeze the
   new exact SHA before resuming F7B. Use at most the one explicitly authorized
   replacement canary solely for end-to-end Cloud Logging/token verification.
3. Begin F7C only after F7B passes; complete F8 submission materials
   only after the applicable release gates.


## Active Implementation Checkpoint

### 2026-09-09 — F7B.2 production Gemini logging remediation

- **Starting state:** Preserved `main`, `HEAD`, and `origin/main` at
  `ed4f14b94f0ba469ccc4ef04c3c3d7552abfbd1f`, the accurate F7B blocked progress
  record, and untouched `.node-version`. No cloud or Vertex action occurred.
- **Correction:** Centralized production application logging in the FastAPI
  lifespan. Production installs one INFO-level stderr handler for only the
  `climatecapital` namespace, disables propagation there to prevent duplicates,
  and restores prior logger state on shutdown. Root/Uvicorn configuration and the
  existing bounded Gemini completion message are unchanged; DEBUG is not enabled.
- **Verification:** A production-mode regression using the real application
  lifespan and captured stderr, without `caplog` or a test logger-level override,
  first reproduced zero output and now proves exactly one completion record. It
  contains request ID, surface, model, status, latency, retry count, and all token
  fields while excluding prompt, response, grounding, raw client key, and hidden
  instructions. All 50 focused Gemini/deployment tests pass with only the two
  known dependency deprecations; `git diff --check` passes.
- **Handoff:** **PASS locally.** No GCP mutation, build/deploy, Vertex call,
  commit, push, model/authority/methodology change, or F7C work occurred. Manual
  review/commit/push and a new exact frozen SHA are mandatory before F7B resumes.
  One replacement live canary is authorized only to verify repaired completion
  and token metadata in Cloud Logging.

### 2026-09-09 — Resumed F7B blocked on production Gemini completion logging

- **Frozen build:** Reconciled clean `main`, `HEAD`, `origin/main`, and merge base
  at `ed4f14b94f0ba469ccc4ef04c3c3d7552abfbd1f`; only `.node-version` was
  untracked and untouched. Recomputed the unchanged runtime-v3 data version,
  manifest SHA, release ID, 106 projects, 74 mapped contexts, and
  `fixture_mode=false`. An exact `git archive` plus reviewed upload allowlist sent
  87 files / 1.2 MiB with all forbidden local/raw/fixture material excluded.
- **Image and candidates:** Cloud Build
  `d429898d-0b21-48ad-a7e6-48d7bc4b1052` passed in 84.45 seconds under the
  existing Compute build identity and pushed 62,140,474-byte immutable digest
  `sha256:df9e1ed9783f264d3f1b98dc2527f7bae5c2f1f326828f633b4ae6ef5431dd49`.
  Zero-traffic private revisions `climatecapital-ai-core-ed4f14b` and
  `climatecapital-ai-gemini-ed4f14b` use that same digest, the dedicated runtime
  account, 1 CPU / 512 MiB, min 0 / max 1, concurrency 20, and exact identities.
- **Private verification:** Both candidates passed authoritative `/health`, root,
  JS/CSS, favicon, robots, bootstrap, strict API 404, disabled docs/OpenAPI,
  locked headers, exact identity, 106/74/false, and the deterministic 18-project
  `$331,825,000` selected / `$175,000` remaining result. Logs show one PID-1
  Uvicorn worker on `0.0.0.0:8080`, a one-attempt startup probe, and no error loop.
- **Single canary:** Exactly one methodology request returned HTTP 200/COMPLETE
  from `gemini-3.5-flash` in 4.761 seconds, request ID
  `cb2920c3-ef03-4a9d-b44c-59dafceaa3ec`, grounded only in
  `GOVERNED_METHODOLOGY`. Its response kept Gemini explanation-only and denied
  funding decisions, recommendations, alterations, and optimization. A temporary
  wrapper exited nonzero only because it tested the exact substring `explain`
  rather than accepting `explanation`; the provider result itself passed and was
  not repeated.
- **Blocker/handoff:** **BLOCKED — SOURCE REMEDIATION REQUIRED.** Cloud Logging
  recorded the 200 request and an SDK advisory but no `Gemini explanation
  completed` application entry, so latency/retry/token metadata and content-free
  logging cannot be verified. The service remains private; both new candidates
  remain at zero traffic and old `fda9176` remains private evidence only. No new
  IAM, public access, promotion, commit, push, or F7C work occurred.

### 2026-09-09 — F7B.1 Cloud Run-safe health endpoint remediation

- **Starting state and issue:** Preserved `main`, `HEAD`, and `origin/main` at
  `fda9176bc7eaf05dd1951744c94a24ad5e408517`, the accurate F7B blocked progress
  change, and untouched `.node-version`. Build
  `c9c52f26-0f9c-4c11-837c-cbb852eff1b7` and digest
  `sha256:aeeddd6438ada123b6b924dda298f437c4280d4f015c678b02acc32e30039a64`
  remain valid evidence for the superseded source, and the private core revision
  proved container startup, injected port, root, assets, favicon, and robots.
  Cloud Run intercepted `/healthz` as a reserved z-ending path before FastAPI.
- **Correction:** Added authoritative `GET /health`, retained `GET /healthz` as a
  local/backward-compatible alias, and routed both through one unchanged
  runtime-v3 health constructor with truthful endpoint values. The strict success
  contract and generated schemas permit exactly `/health` and `/healthz`;
  production deployment instructions now use `/health`.
- **Verification:** 57 focused health/API/deployment tests passed with only two
  known dependency deprecations; all 31 generated schemas match. Production-mode
  Uvicorn returned 200/READY for `/health` and 200 for `/healthz` with equivalent
  stable health semantics, all locked security headers, and the expected explicit
  safe local deployment identity. Bootstrap returned 106 projects, 74 mapped,
  `fixture_mode=false`, and the same runtime-v3 data version. Root, robots, and the
  production JS asset returned 200; an unknown `/api/v1/...` remained a JSON 404.
- **Handoff:** **PASS locally; F7B remains blocked pending publication.** No Cloud
  Build, deploy, IAM/resource/public-access/traffic mutation, Vertex call, commit,
  push, or F7C work occurred during F7B.1. The user must review, commit, push, and
  freeze a new exact SHA before F7B resumes. The old `fda9176` image and revision
  must never be promoted as the final release.

### 2026-09-09 — F7B built and privately deployed; blocked on `/healthz`

- **Frozen gate:** Confirmed `main`, `HEAD`, `origin/main`, and merge base at exact
  `fda9176bc7eaf05dd1951744c94a24ad5e408517`; no tracked/staged change existed and
  only the untouched `.node-version` was untracked. Recomputed runtime-v3 identity:
  data version `climatecapital-austin-2026-01-21-cross-category-v2`, release ID
  `3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1`,
  manifest SHA-256
  `089d8f54108530d3a2483b25239b446bda236d98b4d554a8dd25cdd2934c3d8a`,
  106 projects, 74 mapped, and `fixture_mode=false`.
- **Authorized setup:** Enabled only Cloud Run, Artifact Registry, and Cloud Build;
  created the one `us-central1` Docker repository and keyless
  `climatecapital-runtime` service account; granted only `roles/aiplatform.user`.
  Direct permission testing confirmed the deployer already has runtime-account
  `iam.serviceAccounts.actAs`, so no Service Account User grant or JSON key was
  added.
- **Build boundary/result:** Built a temporary context from `git archive` of the
  exact SHA and listed its 87-file/1.2 MiB upload set. A temporary upload-only rule
  included the frozen Dockerfile and `.dockerignore`; forbidden local, credential,
  fixture, raw/staging, Git, virtualenv, node_modules, and build-output paths were
  absent. The user explicitly authorized bucket-only `roles/storage.objectViewer`
  for the effective Compute build account. Build `4622278e...` then built the image
  but proved the expected repository upload denial; repository-only
  `roles/artifactregistry.writer` was applied under the original F7B authority.
  Retry build `c9c52f26-0f9c-4c11-837c-cbb852eff1b7` passed in 89.45 seconds and
  pushed `app:git-fda9176` at digest
  `sha256:aeeddd6438ada123b6b924dda298f437c4280d4f015c678b02acc32e30039a64`.
- **Private core/result:** Cloud Run does not support `--no-traffic` for the first
  service. The bounded fallback created `climatecapital-ai-core-fda9176` with the
  Invoker IAM check enforced; unauthenticated access returns 403. The container
  became healthy, listened on `0.0.0.0:8080`, and served root, JS/CSS, favicon,
  and robots with 200. Exact `/healthz` instead returned Google Frontend HTML 404
  before reaching the container; no corresponding application/request log exists.
- **Handoff:** **BLOCKED — SOURCE REMEDIATION REQUIRED.** Cloud Run reserves this
  path, so the accepted public health gate cannot pass without a source route/test
  correction and new frozen SHA. No Gemini revision, Vertex canary, public access,
  final promotion, commit, push, service-account key, or F7C work occurred.

### 2026-09-09 — F7A.1 pre-deployment remediation and local production verification

- **Starting state:** Began from frozen `1e30c2d` with only the accepted F7A
  `PROJECT_PROGRESS.md` change plus the pre-existing untouched `.node-version`.
- **Six bounded corrections:** Added same-process compiled-SPA serving; made
  governed runtime-v3 authoritative for startup, response identity, and health;
  added fail-closed five-value production identity; added the pinned multi-stage
  non-root Dockerfile and whitelist `.dockerignore`; added robots/noindex,
  production security headers, and production-disabled FastAPI docs/OpenAPI; and
  added bounded Gemini retry/token logs plus focused tests, regenerated schemas,
  and the narrow IAM/ADC handoff note.
- **Verification:** Passed 73 focused tests and a final 48-test affected rerun;
  506 full pytest tests plus 137 subtests; 152 legacy unittest tests; 31 schemas;
  explicit fixture validation; Python compilation/import/runtime-v3 checks;
  `pip check`; 9 frontend files / 108 tests; ESLint; and the 79-module build under
  exact Node 22.23.2/npm 11.19.1. Git whitespace, secret, artifact, and ignored-
  output checks pass. A real production-mode Uvicorn smoke returned 200 for the
  built SPA, robots, health, bootstrap, and the unchanged `$332M` plan; reported
  106/74/false runtime facts; emitted all required headers; and returned 404 for
  docs, ReDoc, and OpenAPI.
- **Container limitation:** Docker is not installed on this host, so no local
  image build/run occurred. The exact official Node and Python base tags exist;
  F7B Cloud Build must perform the authoritative image build, non-root/PORT smoke,
  and final image-content inspection.
- **Handoff:** **PASS**. No cloud/IAM mutation, deployment, commit, or push
  occurred. The user must manually review, commit, and push; F7B remains pending
  until that publication produces a new exact frozen SHA.

### 2026-09-09 — F7A GCP deployment-readiness and configuration audit

- **Frozen baseline:** Confirmed `main`, `HEAD`, and `origin/main` at
  `1e30c2dd62729bfec2a487cb30d43d4ac18260ad`; the initial tracked tree was clean,
  `git diff --check` passed, and only the pre-existing `.node-version` was
  untracked and untouched.
- **Selected architecture:** Retained D-080's one public request-billed Cloud Run
  service in `us-central1`: one non-root multi-stage image, one FastAPI/Uvicorn
  worker serving the compiled Vite SPA and relative `/api/v1` calls, runtime-v3
  packaged in the image, minimum 0 / maximum 1 instance, 1 vCPU / 512 MiB, no
  runtime database/BigQuery/GCS/GIS dependency, and keyless Vertex ADC through a
  dedicated runtime service account.
- **Cloud audit:** Active account `swethabarla08@gmail.com` has the existing Owner
  role; project `climatecapital-ai` is active and billed; ADC refresh succeeds;
  Vertex AI, Logging, Monitoring, BigQuery, and Storage APIs are enabled. Cloud
  Run, Artifact Registry, Cloud Build, Secret Manager, and Billing Budget APIs are
  disabled. No Cloud Run service, Artifact Registry repository, Cloud Build
  history, Secret Manager dependency, or user-managed service account is present.
  The existing `us-central1` raw bucket and 37-row BigQuery raw table remain
  preparation-only and require no runtime IAM.
- **P1 findings:** The current FastAPI root returns 404 and does not serve
  `frontend/dist`; no Dockerfile, `.dockerignore`, or tracked `robots.txt` exists.
  No Cloud Build config exists, but F7B can use the Dockerfile directly with
  `gcloud builds submit`. `/healthz` returns the legacy
  `m2b-development-fixture-1` identity with `FIXTURE` tier and zero Git/image
  values while bootstrap returns runtime-v3 with `fixture_mode=false`. Framework
  docs/OpenAPI are public, locked crawler/security headers are absent, and Gemini
  provider token counts are collected but omitted from the bounded completion log.
  These require a small separately authorized pre-deployment correction.
- **P2 configuration:** Enable only Cloud Run, Artifact Registry, and Cloud Build;
  create one regional Docker repository and one runtime service account with only
  `roles/aiplatform.user`; build and push from the exact frozen corrected tree;
  deploy the immutable digest to a tagged no-traffic revision with production
  identity/Gemini environment values; verify health, core APIs, same-origin SPA,
  and one Vertex canary before promotion. Secret Manager, runtime BigQuery/GCS,
  VPC, load balancer, CDN, database, and separate frontend hosting are not needed.
- **Verification:** Direct TestClient evidence reproduced the 404 root and
  fixture/runtime identity split; `/docs`, `/redoc`, and `/openapi.json` returned
  200, while `/robots.txt` returned 404 and required security headers were absent.
  The 53 focused runtime/standard-API/Gemini tests passed with two known dependency
  deprecations. The production frontend build passed at 79 modules under the exact
  Node 22.23.2/npm 11.19.1 toolchain after the known signed-host Node mismatch was
  isolated. Runtime-v3's manifest SHA-256 is
  `089d8f54108530d3a2483b25239b446bda236d98b4d554a8dd25cdd2934c3d8a`.
- **Cost/security:** Request-based minimum-zero Cloud Run and low demo traffic
  should remain near zero compute cost; one small image should remain within or
  near Artifact Registry's 0.5 GiB allowance; one short build should remain within
  Cloud Build's monthly free minutes. Gemini is the material variable cost and
  retains explicit action, bounded input/output, concurrency/rate limits, and a
  kill switch. No hard-coded secret, tracked credential, API key, service-account
  JSON, or browser cloud credential was found.
- **Result/handoff:** **READY WITH PRE-DEPLOYMENT FIXES; F7B NOT READY** until the
  P1 corrections are implemented, verified, and frozen. No deployment, API enable,
  resource creation, IAM grant, cloud mutation, application change, commit, or push
  occurred.

### 2026-09-09 — F6D final regression and F6 closeout

- **Candidate reconciliation:** Confirmed `main`, `HEAD`, `origin/main`, and the
  merge base at `be78a783c125b943d4da4441f9a290a1c875bc15`. The only tracked
  candidate changes are this canonical F6 record and the accepted one-line
  `frontend/index.html` title correction. Nothing is staged; the pre-existing
  untracked `.node-version` remains untouched; no test/browser artifact, log,
  credential, secret, environment file, or unrelated change is present.
- **Full regression:** Passed 486 pytest tests plus 137 subtests and 152 legacy
  unittest tests; verified 31 generated schemas; validated the explicit
  development fixture and manifest checksum; passed Python compilation, corrected
  public-module imports, `pip check`, 9 frontend files / 108 tests, ESLint, the
  79-module TypeScript/Vite production build, and Git whitespace/status checks.
  The known two Python dependency deprecations and non-writable pip-cache warning
  remain non-blocking.
- **Environment classification:** An initial import probe named nonexistent
  `create_app`; the corrected public `app`/runtime imports passed. Frontend commands
  first inherited the signed automation host's Node 24, which could not load native
  Rolldown under macOS library validation. After diagnosing and removing a
  temporary ignored WASI fallback, the entire frontend surface passed using the
  pinned Node 22.23.2/npm 11.19.1 child PATH. No manifest, lockfile, source, or
  final working-tree change resulted.
- **Critical-path smoke:** The real FastAPI/Vite runtime returned 200 for health,
  bootstrap, plan evaluation, Gemini explanation, and benchmark. Safari showed
  106 projects and 74 mapped contexts; opened Barton Springs Bridge with its
  governed `$12M`, Priority 80/rank 2 evidence; completed the `$332M` plan with 18
  projects, `$331,825,000` selected, and `$175,000` remaining; and received one
  live Vertex explanation that correctly stated Gemini neither selected nor
  changed projects. Closing Gemini preserved plan/detail state; Explore ↔ Funding
  Plan and Historical Benchmark navigation remained usable.
- **Health and closeout:** The served title was exactly `ClimateCapital AI`, the
  bootstrap release was runtime-v3 with `fixture_mode=false`, and no application
  error surface, backend exception, runaway call, contract mismatch, or exposed
  secret was observed. All services stopped cleanly. The SDK emitted one
  non-blocking advisory about direct automatic-function-calling invocation even
  though the bounded product request completed successfully. No additional F6D
  defect or implementation fix was required. F6 is complete; F7 remains
  unauthorized and undeployed.

### 2026-09-09 — F6C Gemini and cross-feature live acceptance

- **Runtime:** Reused the real FastAPI service at `http://127.0.0.1:8000` and
  Vite frontend at `http://127.0.0.1:5173`. `/healthz` returned 200/SUCCESS with
  Gemini enabled; bootstrap returned the governed 106-project runtime-v3 release.
  The configured ADC-backed Vertex Gemini path was live; no secret was recorded.
- **Gemini acceptance:** Live responses rendered for product/methodology, mapped
  Barton Springs Bridge, unmapped Building Renovation and Replacement Program -
  Bolm Maintenance Center, and evaluated `$700M` Funding Plan contexts. Gemini
  preserved project identity, request/Priority facts, Bolm's explicit `Location
  unavailable` state, plan totals, and analyst-controlled deterministic authority.
- **Plan and boundaries:** The real plan completed with 31 projects,
  `$699,975,000` selected, and `$25,000` remaining after explicit analyst boundary
  resolution. Gemini explained the total, remaining budget, and Canyon Creek
  Northwest Substation's role without changing membership; it declined requests
  to change an official PRB score, fabricate geometry, optimize membership, add
  weights, or present its explanation as an official City recommendation.
- **State, recovery, and visual health:** Project-to-project and
  project-to-plan transitions updated Gemini context without stale attribution or
  state loss. Empty submit remained disabled; the live pending state disabled
  duplicate submission; implemented user-safe error/retry presentation was
  inspected because inducing a Vertex failure would have required prohibited
  credential/configuration sabotage. Desktop and a narrower effective Safari
  viewport kept the drawer, input, scrolling, and close control usable.
- **Runtime health/scope:** Observed Gemini and plan requests returned 200; browser
  console evidence contained only the standard React development notice, and
  frontend/backend logs showed no uncaught exception, runaway call, contract
  mismatch, or exposed secret. Intermittent Chrome/Safari automation detachment
  was tooling-only and did not reproduce as an application fault. No F6C product
  defect or code fix was required; no targeted automated rerun was therefore
  needed. F6D, deployment, commit, and push did not begin.

### 2026-09-08 — F6B core live browser product acceptance

- **Runtime:** Started the repository's real FastAPI backend on
  `http://127.0.0.1:8000` and Vite frontend on `http://127.0.0.1:5173` with the
  existing Python environment and pinned Node 22.23.2/npm 11.19.1 toolchain.
  Health, bootstrap, benchmark, and plan-evaluation requests succeeded.
- **Core acceptance:** Chrome exercised the global primary/reference navigation,
  compact 106-project Explore summary, all-category catalog, 74 supported map
  locations, 32 explicit unavailable-location states, search/reset, mapped and
  unmapped project details, project switching/closing, map legend and zoom,
  deterministic `$332M` and `$700M` Funding Plans, invalid budget input, analyst
  resolution, and plan persistence across supporting-page navigation.
- **Supporting and responsive acceptance:** Historical Benchmark, Data &
  Methodology, and Help & Resources loaded with correct headings and readable
  content. Desktop plus 831px and 390px responsive emulation showed coherent
  reflow without observed clipping, overlap, or horizontal overflow; the desktop
  sticky shell retained the profile control while workspace content scrolled.
- **Runtime health:** Chrome DevTools showed no application console errors or
  issues; only the expected React development-tools notice was present. Backend
  logs showed successful 200 responses without exceptions or repeated failures.
- **Defect/fix:** Corrected the low-severity stale browser-tab title from
  `frontend` to `ClimateCapital AI` in `frontend/index.html`. No other defect was
  found. Focused App tests (16), the production build (79 modules), live HTML
  title check, backend health check, and Git whitespace check passed.
- **Scope/handoff:** No Gemini conversation, methodology, governed data,
  architecture, product-scope, dependency, deployment, F6C/F6D/F7, commit, or push
  work occurred. F6C remains subject to separate authorization.

### 2026-09-08 — F6A baseline and automated full regression

- **Baseline:** Confirmed `main` at `be78a783c125b943d4da4441f9a290a1c875bc15`,
  exactly matching `origin/main` and the accepted F5B publication commit. The only
  initial working-tree difference was the documented untracked `.node-version`;
  it remained untouched.
- **Regression:** Passed 486 pytest tests plus 137 subtests, including source/data,
  application/API, Gemini mock, contract, runtime, and release coverage. The
  legacy documented unittest discovery command also passed its 152 collected
  tests. Verified all 31 generated schemas, Python compilation, package imports,
  dependency integrity, explicit development-fixture CLI validation, 9 frontend
  files / 108 tests, ESLint, and the 79-module TypeScript/Vite production build.
- **Warnings:** Retained the known Starlette/AnyIO and google-genai/Python 3.14
  deprecation warnings plus the environment-only non-writable pip-cache warning.
  None affects F6A acceptance.
- **Defects/changes:** No regression was found and no implementation fix was
  required. The initial direct backend import omitted the repository's required
  `PYTHONPATH=backend`; the corrected import passed. The shell's default Node/npm
  differed from the pinned frontend toolchain, so frontend checks used the
  existing Node 22.23.2/npm 11.19.1 binaries and passed.
- **Scope/handoff:** No browser acceptance, real Vertex call, service start,
  deployment, F7 work, commit, or push occurred. F6B is ready only after explicit
  user authorization.

### 2026-09-08 — F5B mandatory Gemini on Vertex AI integration

- **Backend/API:** Implemented `POST /api/v1/gemini/explain` with strict request
  and response contracts, current-runtime identity checks, bounded history,
  surface-specific validation, authoritative grounding, structured provider
  output, safe error mapping, timeout, concurrency and application rate limits,
  and lazy Vertex initialization. One user request consumes one application rate
  token; the internal one-time provider retry does not consume another token.
- **Grounding:** PROJECT resolves up to two governed decision units and only their
  approved runtime-v3 geometry role/provenance or explicit location-unavailable
  state. FUNDING_PLAN and BOUNDARY re-run the deterministic evaluator from the
  authoritative input; BOUNDARY requires an unresolved authoritative boundary.
  BENCHMARK loads the isolated January benchmark in the backend. METHODOLOGY uses
  a small canonical governed context. Browser-supplied results, coordinates, later
  facts, external knowledge, Search, Maps, tools, and function calling are absent.
- **Frontend/acceptance refinements:** Activated the compact Ask Gemini control and
  context-bound drawer/sheet with starter questions, bounded in-memory follow-up,
  grounding markers, disclaimer, reset and localized failure states. Split desktop
  sidebar navigation into primary and reference groups, pinned the profile while
  the workspace scrolls, compressed Explore totals into a side summary, removed
  the dominant map overlay while retaining its legend caveat, and coordinated
  Project Detail with Gemini as non-overlapping desktop panes and a context-rich
  responsive sheet.
- **Live acceptance:** Real Vertex calls through the running application passed for
  mapped PROJECT, `$332M` FUNDING_PLAN, `$700M` BOUNDARY, BENCHMARK, and the earlier
  METHODOLOGY smoke. The boundary call received authoritative rank 28 / Funding
  Priority 67 evidence, explained the `$108.275M` versus `$113M` boundary, required
  analyst judgment, and selected no candidate. The benchmark explanation remained
  retrospective. Chrome DevTools reported no application console errors.
- **Verification:** 28 focused Gemini backend tests; 486 full Python tests with two
  dependency deprecation warnings; 31 schemas; clean `pip check`; 9 frontend files
  / 108 tests; passing production build and ESLint. Chrome/DevTools checks at
  desktop, 900px, and exact 390px reported no document overflow, a fixed
  full-height desktop sidebar, and non-overlapping 420px Project Detail / 440px
  Gemini panes. Git whitespace checks pass.
- **Scope/handoff:** No deterministic methodology, project universe, request,
  official PRB value, Funding Priority/rank, evaluator rule, benchmark meaning,
  governed geometry, deployment, stage, commit, or push changed. F5B is ready for
  user approval and publication; F6 has not started.

### 2026-09-08 — Frontend runtime-v3 governed map integration

- **Work completed:** Added the typed map-context v3 frontend contract and
  fail-closed client parsing, including feature identity, catalog membership,
  uniqueness, geometry structure/range, role/type agreement, counts, and release
  hashes. The runtime-v3 bootstrap fixture now contains the governed 74-feature
  mix: 64 points, 9 polygons, and 1 multipolygon.
- **Explore/map behavior:** Renders only governed source-native geometry, styles
  Project location, Facility/site context, and Park/site context distinctly,
  exposes the roles and construction-footprint caveat in the legend, and raises
  selected geometry above the other features. Search/category/priority/request
  filters update both map and list; a map selection selects and scrolls the
  corresponding project row; a list selection opens Project Detail and focuses
  its mapped point or polygon.
- **Unmapped behavior:** All 32 projects without governed geometry remain in the
  list and Project Detail with explicit `Location unavailable` / `Map location
  unavailable` evidence. Selecting them opens detail but does not move the map or
  fabricate a point, footprint, address-derived location, or other proxy.
- **Responsive/browser QA:** Chrome DevTools covered the actual running frontend
  and runtime-v3 API at desktop and 400×748 responsive widths. Verified OSM
  tiles/attribution, 74/32 counts, feature-role styling and legend, filtered map/
  list synchronization, mapped polygon focus/detail, unmapped no-movement/detail,
  responsive stacking, and console state. No application console errors were
  present; the only visible console content was React's development-tools tip.
- **Verification:** The complete frontend suite passes 8 files / 80 tests,
  including client contract regressions and dedicated map interaction/focus/
  no-movement tests. ESLint, the TypeScript/Vite production build (78 modules),
  and `git diff --check` pass under Node 22.23.2. The live bootstrap reports
  runtime-v3 release
  `3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1`,
  106 analytical projects, 74 mapped, 32 location unavailable, and
  `fabricated_geometry=false`.
- **Scope:** No backend methodology, governed artifact, Funding Priority, Funding
  Plan, benchmark, cloud, deployment, `.node-version`, staging, commit, or push
  change. No new durable decision was required; implementation follows D-116.
- **Recommended next milestone:** Review/approve and publish this checkpoint, then
  immediately begin F5B mandatory Gemini explanation integration.

### 2026-09-08 — D-116 cross-category project geometry governance

- **Decision:** Reviewed all 74 governance-eligible candidates individually and
  promoted all 74 because each has HIGH-confidence, source-native official
  geometry with a unique project/facility/park/parcel/asset linkage and a truthful
  display role. Kept the other 32 explicitly unmapped.
- **Coverage:** Watershed 35/37, Parks & Open Space 21/22, Transportation 1/9,
  and Community Facilities 17/38. The governed map contains 64 points, 9
  polygons, and 1 multipolygon: 42 `PROJECT_DISPLAY_POINT`, 22 `FACILITY_SITE_CONTEXT`, 8
  `PARK_SITE_CONTEXT`, 1 `PROJECT_SITE`, and 1 `PROJECT_PARCEL`.
- **Held/rejected:** Watershed `5789.127` retains its scope/name conflict;
  citywide `5789.150` has no feature; EMS Demand 1/2 retain conflicting official
  locations; Bolm Maintenance Center retains its overbroad whole-park mismatch;
  all remaining medium, low, address-only, and no-match cases remain unmapped.
  Exact per-project dispositions are in the D-116 governance artifact and
  [governance report](docs/delivery/cross-category-project-geometry-governance-2026-09-08.md).
- **Historical fit:** Thirty-five WPD display points use the exact snapshot date,
  18 features are supported by pre-snapshot sources, and 21 later-refreshed
  features are governed only for stable-location context. Later project status,
  scope, budget, schedule, and other facts are excluded.
- **Runtime/contracts:** Added strict geometry-governance, map-context v3, and
  manifest v3 contracts/schemas; created immutable runtime-v3; activated the
  standard backend loader against it; and preserved runtime-v2 unchanged.
  Runtime-v3 catalog and benchmark bytes exactly equal runtime-v2. Narrow
  `.gitignore` exceptions expose only the governed runtime-v3 map and the labeled
  candidate source-geometry snapshot for durable review.
- **Verification:** 51 focused governance/runtime/API tests pass. Full Python
  regression passes 458 tests plus 137 subtests. Deterministic builders are
  idempotent; schema generation/check, compilation, dependency check, Markdown
  checks, and `git diff --check` are recorded in the Verification Record.
- **Scope:** No frontend, Funding Priority, Funding Plan evaluator, analytical
  universe, governed requests, PRB scores/ranks, Historical Benchmark semantics,
  `.node-version`, cloud, stage, commit, push, or deployment change.

### 2026-09-08 — External GIS evidence investigation for all 106 projects

- **Work completed:** Reconciled every governed `decision_unit_id` against
  authoritative City of Austin project, departmental GIS, facility, park,
  station, library, capital-project, and parcel sources. Added one candidate CSV
  row per project, a machine-readable summary, and a detailed research report;
  all are conspicuously labeled `CANDIDATE / RESEARCH / NOT YET GOVERNED`.
- **Result:** 76 HIGH source-native geometry candidates, 0 HIGH official-address-
  derived geometries, 13 MEDIUM candidates, 2 LOW candidates, and 15 NO_MATCH.
  Seventy-four can proceed to explicit governance review; 32 remain held or
  unmapped. Primary representations are 68 points, 12 polygons, 1 address-only,
  and 25 with no geometry. No trustworthy project line was found.
- **Watershed:** The official WPD “Points for display only” layer reconciles all
  37 exact canonical CIP IDs and carries a January 21, 2026 feature FME timestamp.
  Twenty-nine have one or more later polygon representations in CPE/RNA. Exact-ID
  source/name conflict `5789.127` and citywide-program display semantics for
  `5789.150` remain held; later polygons remain secondary candidates.
- **Other categories:** Parks has 21 HIGH site/asset/project candidates and one
  MEDIUM whole-park/context mismatch; Transportation has one HIGH CPE bridge
  polygon and eight MEDIUM official corridor/asset matches without geometry;
  Community Facilities has 17 HIGH, 4 MEDIUM, 2 LOW, and 15 NO_MATCH, including a
  uniquely proven Canyon Creek APD parcel and unresolved EMS Demand 1/2 conflicts.
- **Historical fit:** WPD display points, APR CIP, fire, EMS, library, and Canyon
  Creek evidence align at or before the snapshot. CPE, RNA, park/PARD, and AFM
  sources have post-snapshot refreshes; only stable location may be considered,
  and later project attributes/geometry evolution require isolation and review.
- **Verification/scope:** Asserted 106 rows and 106 unique IDs, exact category,
  confidence, geometry, ambiguity, multiple-feature, eligibility, and not-governed
  labeling totals; inspected final CSV/JSON/report and Git scope. Governed runtime
  remains 0 mapped / 106 unmapped with `fabricated_geometry=false`. No runtime,
  backend, methodology, contract, Funding Plan, Funding Priority, benchmark,
  `.node-version`, staging, commit, push, or deployment change. No durable decision
  ID was created because no geometry was approved.
- **Recommended next step:** User governance review of the candidate report before
  any promotion; otherwise resume F5B from the published/locally refined frontend
  baseline.

### 2026-09-07 — Focused post-F5A frontend visual refinement

- **Work completed:** Recast the application as a compact historical decision
  workspace with the approved dark navigation shell, branded route-aware header,
  stronger card hierarchy, consistent purple/green status accents, iconography,
  analyst context, and responsive stacking. Refined Explore, Project Detail,
  Funding Plan, Historical Benchmark, methodology, and help surfaces without
  changing governed product content or analytical behavior.
- **Explore/map:** Added the configured OpenStreetMap Austin basemap through
  Leaflet, tile attribution, zoom controls, neutral fallback styling, a responsive
  layers disclosure, map/list split, compact project rows, clear selection state,
  fixed detail drawer, visible filter reset, and current-plan summary strip. The
  runtime contract reports 0 mapped and 106 unmapped projects, so the map renders
  no pins and explicitly explains that project coordinates are unavailable.
- **Funding/benchmark:** Added a compact plan utilization bar and restyled budget
  presets, summaries, boundary states, selected projects, historical package
  reconciliation, category comparisons, and project evidence as approved-style
  decision cards. Existing plan evaluation and benchmark isolation are unchanged.
- **Tests/results:** 7 frontend test files and 69 tests pass; `npm run lint`,
  `npm run build`, and `git diff --check` pass with Node 22.23.2/npm 11.19.1.
  Focused Explore/App tests pass 19/19.
- **Browser verification:** Chrome DevTools covered full-width and responsive
  400px layouts, map tile rendering/attribution, zero-marker state, filters and
  reset, layers disclosure, project selection/detail/close, the $332M governed
  reference evaluation (18 projects, $331,825,000 selected, $175,000 remaining),
  Historical Benchmark navigation/content, and console state. No application
  errors were present; the only console message was React's development-tools tip,
  and the final DevTools Issues audit reported 0 page errors, 0 breaking changes,
  and 0 possible improvements.
- **Scope/deviations:** No backend, methodology, data contract, project facts,
  Funding Priority logic, plan-selection behavior, benchmark authority, cloud,
  deployment, `.node-version`, commit, push, or staging change. No durable decision
  ID was required.
- **Recommended next milestone:** F5B mandatory Gemini explanation integration.

### 2026-09-07 — Frontend F4 January 21 Historical Benchmark

- **Work completed:** Added a dedicated, lazy-loaded Historical Benchmark route
  backed only by `GET /api/v1/benchmark`. Presented the API-sourced $700M full
  package, $332M matched project cohort, $368M outside-cohort amount, 20 historical
  analytical projects, explicit arithmetic, governed outcome flags, provenance,
  and runtime identity.
- **Category/project context:** Rendered the four API category summaries alongside
  bootstrap-derived governed request totals. Joined all 20 recommended outcomes to
  catalog evidence by `decision_unit_id`, with historical recommendation dollars
  visibly separate from governed request and Funding Priority score/rank. Display
  order is category/name only and is labeled non-analytical.
- **Isolation/comparison:** Benchmark state is component-local, unpersisted, and
  loaded only when its route is entered. Failure does not affect Explore or Funding
  Plan. A current-plan overlap count uses only already-loaded benchmark membership
  and the authoritative current plan; it is labeled presentation-only and never
  enters plan evaluation or boundary state.
- **Contract limitation:** The frozen category summaries expose matched-cohort
  recommendation totals and counts, not per-category full-package/outside-cohort
  amounts. The UI states this and does not hard-code or invent the missing category
  partition; the $368M outside-cohort amount remains citywide.
- **Tests/results:** 7 frontend test files and 67 tests pass, including 10 focused
  Historical Benchmark tests; `npm run build` and `npm run lint` pass under Node
  22.23.2/npm 11.19.1. The targeted backend runtime-bundle/standard-API suites pass
  33 tests with one known Starlette/AnyIO deprecation warning.
- **Deviations/unresolved issues:** No backend or methodology change. The browser
  runtime exposed no available connection, so screenshot-based visual QA remains
  deferred to F6 live visual/functional QA.
- **Decisions:** No durable decision ID created; F4 implements the frozen governed
  benchmark contract and explicit user scope.
- **Recommended next milestone:** F5A product completion and frontend quality/polish,
  followed immediately by mandatory F5B Gemini explanation integration.

### 2026-09-07 — Frontend F3 governed Funding Plan workspace

- **Work completed:** Replaced the transition surface with an analyst-facing
  Funding Plan workspace driven exclusively by `POST /api/v1/plans/evaluate`.
  Added the three explanatory reference presets, validated custom whole-dollar
  budgets, authoritative result summaries, selected-project catalog joins, warnings,
  applied analyst resolutions, and readable selection-source labels.
- **Boundary workflow:** Added an explicit equal-priority boundary panel showing all
  candidates and backend feasibility, a running analyst-selected amount, local
  prevention of plainly over-budget choices, and the exact conditional same-tier
  advancement acknowledgement. Each choice is sent back to the backend with the
  current budget and accumulated resolutions. Exact-input retries preserve the
  expected fingerprint, while changed boundary inputs clear it because they produce
  a new deterministic evaluation; the frontend never completes or constructs the
  portfolio locally.
- **Session/error boundary:** Safe persisted input contains budget and boundary
  resolutions but never treats a stored evaluation as current. Budget/runtime
  changes clear stale resolution and fingerprint state. Abort/generation ordering
  remains active, structured API/network/malformed-response failures have distinct
  recovery, and version conflicts reload the active governed runtime.
- **Tests/results:** 6 frontend test files and 53 tests pass, including 13 focused
  Funding Plan tests; `npm run build` and `npm run lint` pass under Node
  22.23.2/npm 11.19.1. The two targeted backend evaluator/standard-API suites pass
  26 tests with one known Starlette/AnyIO deprecation warning.
- **Deviations/unresolved issues:** No backend or methodology change. Restored safe
  inputs require an explicit new evaluation rather than automatically posting on
  reload. Historical benchmark presentation remains absent by F3 scope. The in-app
  browser runtime exposed no available browser connection, so no screenshot-based
  visual QA was possible.
- **Decisions:** No durable decision ID created; F3 implements the already-governed
  evaluator contract and explicit user scope.
- **Recommended next milestone:** F4 historical benchmark presentation after
  explicit authorization.

### 2026-09-07 — Frontend F2 governed cross-category Explore

- **Work completed:** Replaced the bootstrap placeholder with a project-first
  Explore experience for all 106 governed analytical projects. Added project-name
  search; presentation-category, competition-rank, and non-overlapping governed-
  request filters; four explicitly presentational sorts; visible result/request
  totals; clear/reset behavior; and `decision_unit_id`-keyed selection.
- **Project evidence:** Added focused detail for governed identity/source, request,
  official PRB total and competition rank, tie state, all six official PRB
  components against their own 8/8/20/20/24/20 maxima, Council District and O&M
  context, authority/source identifiers, provenance, optional canonical ID, and
  request-version-conflict disclosure.
- **Geometry/method boundary:** No map or project pin is rendered. Explore states
  the governed 0 mapped/106 unmapped coverage directly and explains that projects
  remain available for evidence review and Funding Plan analysis. Sorting/filtering
  is presentational only; equal scores retain shared ranks and use
  `decision_unit_id` only for deterministic within-tie display.
- **Session/application:** Reused the F1 bootstrap and version-bound session state;
  search, filters, sort, and selected decision unit persist through the existing
  storage seam. Added retry to the existing fail-closed bootstrap error surface.
- **Tests/results:** 5 frontend test files and 36 tests pass, including 9 focused
  Explore tests. `npm run build` and `npm run lint` pass with Node 22.23.2/npm
  11.19.1. Focused coverage proves the 106-project/category facts, combined
  discovery, sorts, tied rank, half-point score, identity selection, PRB maxima,
  zero-geometry/no-pin state, no-results recovery, and reset behavior.
- **Deviations/unresolved issues:** No backend or methodology change. Source-
  department/domain filtering was intentionally omitted to keep discovery focused;
  these fields remain visible in summary/detail. The in-app browser runtime had no
  available browser connection, so no screenshot-based visual QA was possible.
  Funding Plan interaction and benchmark presentation remain intentionally absent.
- **Decisions:** No durable decision ID created; F2 implements the explicit user
  scope and already-governed runtime semantics.
- **Recommended next milestone:** F3 Funding Plan after explicit authorization.

### 2026-09-07 — Frontend F1 cross-category API, contract, and session integration

- **Work completed:** Replaced legacy Watershed v1 transport definitions with the
  activated cross-category v2 bootstrap, Funding Plan, map-context, benchmark, and
  typed error envelopes. Added defensive standard-endpoint clients for
  `/api/v1/bootstrap`, `/api/v1/plans/evaluate`, and `/api/v1/benchmark`; no alias or
  benchmark-compare client exists.
- **Session migration:** Replaced the v1 12-project/current-reference browser model
  with runtime identity, analyst budget, boundary-resolution input, latest backend
  result, fingerprint, and structured request state. A new v2 session-storage key
  ignores legacy state; same-release restoration retains safe inputs but discards
  evaluated output, while identity changes reset plan state.
- **Concurrency/error handling:** Added AbortController plus generation-based late
  response suppression. Structured API status, code, field path, retryability, and
  response identity survive client errors; network and malformed-success failures
  are distinct.
- **Application wiring:** Bootstrap now initializes directly from runtime-v2 without
  map defaults, deployment identity, active-family summaries, or legacy context
  layers. The old Funding Plan UI is replaced by an explicit F1 transition surface;
  full analyst interaction remains F3.
- **Tests/results:** 4 frontend test files and 26 tests pass. `npm run build` and
  `npm run lint` pass under Node 22.23.2/npm 11.19.1. Tests cover 106 projects,
  9/22/37/38 category counts, `$1,973,520,000`, zero mapped/106 unmapped, no
  fabricated geometry, `decision_unit_id`, half-point scores, benchmark isolation,
  typed failures, safe restoration, and stale-response suppression.
- **Files/components:** `frontend/src/api/`; `frontend/src/session/`; minimum
  `frontend/src/App.tsx` wiring; transitional `frontend/src/features/FundingPlan.tsx`;
  and cross-category frontend fixtures/tests. Obsolete v1 scenario, confirmed-plan
  restoration, and ScenarioSettings modules/tests were removed.
- **Deviations/unresolved issues:** No backend or methodology change. Explore,
  Funding Plan controls, and benchmark presentation remain intentionally absent.
  The host default Node 24 binary cannot load the existing signed Rolldown native
  binding; verification therefore used the repository-declared Node 22.23.2 binary.
- **Decisions:** No durable decision ID created; F1 implements already-governed
  runtime contracts and explicit user scope.
- **Recommended next milestone:** F2 Explore after explicit authorization.

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

- **2026-09-09 — F6D final regression and F6 closeout complete:** The exact
  current-tree candidate passed 486 pytest tests plus 137 subtests, 152 legacy
  unittest tests, 31 schemas, explicit fixture validation, compilation/import and
  dependency checks, 9 frontend files / 108 tests, ESLint, the 79-module build,
  Git hygiene, and a real critical-path browser/Vertex smoke. The only reconciled
  F6 product fix remains the accepted `ClimateCapital AI` browser title. F6 is
  complete and ready for separately authorized F7 deployment work.

- **2026-09-09 — F6C Gemini and cross-feature live acceptance complete:** The
  real ADC-backed Vertex path passed general, methodology, mapped/unmapped project,
  evaluated Funding Plan, cross-feature, product-boundary, supported recovery,
  responsive, console, request, and backend-log acceptance. The completed `$700M`
  plan remained 31 projects / `$699.975M` selected / `$25K` remaining throughout
  Gemini explanations. No implementation defect or F6C code fix was required;
  F6D remains separately authorized.

- **2026-09-08 — F6B core live browser acceptance complete with one narrow fix:**
  The real local backend/frontend passed non-Gemini shell, Explore, map/project,
  detail, Funding Plan, benchmark, methodology, help, responsive, console,
  network, and backend-log acceptance. Replaced only the stale browser-tab title
  `frontend` with `ClimateCapital AI`; 16 focused App tests, the 79-module build,
  live title/health checks, and Git whitespace checks pass. F6C subsequently
  completed without an additional fix.

- **2026-09-08 — F6A baseline and automated full regression complete:** Frozen
  baseline `be78a78` passed 486 pytest tests plus 137 subtests, 152 legacy
  unittest-discovered tests, 31-schema parity, compilation, imports, dependency
  integrity, explicit fixture validation, 9 frontend files / 108 tests, ESLint,
  the 79-module production build, and Git whitespace checks. No defect or source
  fix was required; F6B subsequently completed with its narrow title fix.

- **2026-09-08 — F5B mandatory Gemini on Vertex AI integration completed
  and published at `be78a78`:** Added the real server-side `google-genai` Vertex provider, bounded
  governed grounding, structured contracts/errors, runtime guard, deterministic
  evaluator re-runs, isolated benchmark/methodology context, and the accessible
  context-aware frontend drawer/sheet. The five requested UI acceptance
  refinements and live Project/Plan/Boundary/Benchmark/Methodology checks pass.
  Final verification is 486 Python tests, 31 schemas, clean dependencies, 9
  frontend files / 108 tests, build, lint, browser QA, security scan, and Git
  whitespace checks.

- **2026-09-08 — Frontend runtime-v3 map integration completed locally:** The
  frontend consumes the active v3 contract, validates and renders all 74 governed
  point/polygon features, synchronizes filters and map/list/detail selection,
  distinguishes project, facility, and park/site evidence, and preserves all 32
  unavailable-location paths without map movement or fabricated geometry. Chrome
  desktop/responsive interaction QA, 8 files / 80 tests, lint, build, and diff
  checks pass. Review/commit/push remains pending before F5B.

- **2026-09-07 — Frontend F5A published and focused visual refinement completed
  locally:** F5A product completion is published at `fe66a49`. The follow-on
  refinement aligns the governed 106-project experience with the approved visual
  direction across the shell, Explore, Project Detail, Funding Plan, Historical
  Benchmark, and responsive layouts. A configured Austin OSM basemap is present,
  but the frozen runtime's 0/106 trustworthy-geometry state is honored with no
  fabricated pins. Chrome interaction/responsive QA, 69 tests, lint, build, and
  diff checks pass; F5B remains next.

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
The frozen backend runtime, frontend F1–F5A, focused visual/map work, and F5B
Gemini explanation are implemented and published. F6A automated regression, F6B
core browser acceptance, F6C Gemini/cross-feature acceptance, and F6D final
closeout are complete. F7 deployment remains on the critical path and requires
separate authorization.

## Blockers

- F7B.2 has corrected production Gemini INFO-log emission locally. F7B remains
  paused until manual review/commit/push produces a new exact frozen SHA for build,
  private verification, and the one authorized replacement canary.
- Official judging criteria, submission artifacts, and conditional live-demo
  details remain unconfirmed. They urgently block submission-dependent work and
  final submission-package planning. They did not block M1 and do not silently
  authorize or redefine either post-schema track.

## Active Risks

- Neither `ed4f14b` candidate may be promoted as final because it lacks production
  completion-log evidence. The superseded `fda9176` image/revision also remains
  evidence only. F7B.2 requires review, commit/push, a new exact SHA/digest, and
  one replacement canary solely for repaired log verification.
- D-116 governs 74 source-native project map features, but later-refreshed CPE,
  park/PARD, and AFM features are authoritative only for stable-location display.
  A silent source refresh could import post-snapshot shape or project-fact changes;
  new bytes require a new governance review.
- Official park boundaries, facility points, and the Canyon Creek parcel are
  contextual representations, not necessarily construction footprints. Frontend
  rendering must retain explicit `display_role` labels and support mixed points
  and polygons rather than normalizing everything into pins.
- Thirty-two decision units remain explicitly unmapped, including eight
  Transportation rows without official geometry, 15 Community Facilities
  NO_MATCH rows, two LOW facility-campus contexts, four MEDIUM Community
  candidates, Bolm Maintenance Center, and Watershed `5789.127`/`5789.150`.
  Visual completeness is not authority to infer a location.
- Source-license/reuse terms remain explicitly `UNVERIFIED` for the governed
  sources, including RNA, FEMA layer 8, EAZ 2021, and Problem Score documentary
  context. The focused review and canonical metadata agree; reviewed-release use
  remains blocked until supported confirmation exists, without broad source
  reconnaissance or invented verification.
- RNA Projects layer 8 and the current FloodPro services do not establish their
  January 2026 geometry/data state. RNA geometry is research-only for governed
  analysis; FEMA is current contextual hazard evidence only.
- Twenty-two of the 37 Watershed projects still have no exact-ID polygon match in
  the captured live RNA snapshot. D-116 instead governs 35 exact-ID official WPD
  points strictly as `PROJECT_DISPLAY_POINT`; they are not engineering footprints.
  `5789.127` and `5789.150` remain unmapped. Missing richer geometry is not
  evidence of low need.
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
- Project 5789.150 is a citywide renewal program. D-116 explicitly rejects its
  otherwise exact-ID official display point because a single feature would create
  false location, hazard, vulnerability, or beneficiary precision.
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
- The current delivery remains at critical schedule risk: the backend runtime,
  frontend F1–F5B, and targeted F5B acceptance exist, while F6 regression,
  deployment, and final release verification remain.
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
- Gemini provider availability, application restart-local limits, and live-call
  cost remain operational risks; deterministic/manual paths and all governed
  evidence remain usable when Gemini is disabled or unavailable.
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
- Code/data/manifest/image identity could drift unless `/health`, the Cloud Run
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

- No analytical-methodology or current map-governance decision remains open for
  P0. D-116 governs 74 source-native features with explicit roles and keeps 32
  projects unmapped. Any future promotion among those 32 or refresh of governed
  source bytes requires new official evidence and a new review.
- Source licensing/reuse remains unverified operational metadata, not authority to
  promote the candidate sources.
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
- server-evaluated cross-category Funding Plans with exact integer arithmetic,
  analyst-supplied budget and boundary-resolution inputs, isolated Historical
  Benchmark, and no client-authoritative analytical results;
- governed runtime-v3 map context with 74 source-native project features and 32
  explicitly unmapped analytical projects; mixed points/polygons, contextual
  display roles, and no fabricated, geocoded, inferred, or centroid geometry;
- implemented bounded Gemini explanation through the global standard on-demand
  Vertex endpoint and ADC, with no browser credentials or provider tools; and
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
- data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_project_geometry_reconciliation.csv —
  research-only all-106 external-GIS candidate table keyed by `decision_unit_id`;
  it records source IDs/features, geometry role/origin, vintage, historical fit,
  matching evidence, confidence, ambiguity, and governance eligibility and is not
  consumed by runtime.
- data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_summary.json —
  machine-readable reconciliation totals proving exact 106-project coverage while
  recording the pre-governance 0 mapped / 106 unmapped state.
- data/reconnaissance/external_gis/2026-09-08/CANDIDATE_NOT_GOVERNED_source_geometries.geojson —
  research-only snapshot of the 80 candidate source-native features used for
  D-116 review, with source-payload checksums; it is not itself a governed runtime
  artifact.
- docs/reference/CANDIDATE-external-gis-evidence-investigation-2026-09-08.md —
  evidence report, category findings, source-vintage assessment, explicit unmapped
  set, and mixed-geometry recommendation; research only, not an approved spec.
- data/governed/cross_category/reconciliation/project-geometry-governance.json —
  D-116 all-106 promotion/hold/rejection decisions with source/feature identity,
  historical fit, display roles, caveats, and pinned research hashes.
- data/governed/cross_category/runtime_v3/ — immutable active four-file runtime
  bundle with 74 mapped / 32 unmapped; catalog and benchmark bytes are identical
  to runtime-v2, while map-context and manifest advance to version 3 contracts.
- docs/delivery/cross-category-project-geometry-governance-2026-09-08.md — detailed
  authoritative D-116 reconciliation and all 32 unmapped dispositions.
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
- contracts/schemas/ — 32 generated versioned JSON Schemas, including D-116
  geometry-governance, map-context v3, and manifest v3 contracts.
- scripts/release/generate_schemas.py — generate/check tracked schema bytes.
- scripts/release/validate_bundle.py — reviewed-release-default validator CLI with
  an explicit development-fixture mode.
- release-data/fixture/ — conspicuous four-file M2B development fixture; not a
  reviewed release.
- backend/climatecapital/plans/ — deterministic M2B Funding Plan evaluator.
- tests/application/ and tests/release/ — contract, evaluator, validator, and
  direct persistent-fixture tests.
- scripts/data/build_cross_category_geometry_governance.py — deterministic,
  explicit-allowlist builder for the all-106 D-116 reconciliation.
- scripts/data/build_cross_category_geometry_runtime_bundle.py — create-only
  runtime-v3 builder that imports only promoted source-native features and copies
  the protected runtime-v2 catalog/benchmark bytes unchanged.
- data/governed/cross_category/runtime_v3/ — active immutable map-governance
  release with 74 mapped / 32 unmapped and pinned artifact identities.
- frontend/src/api/ and frontend/src/session/ — activated cross-category v2
  standard-endpoint transport, defensive parsing, version-bound browser state,
  and stale plan-response protection.
- frontend/src/features/Explore.tsx and frontend/src/components/ProjectDetail.tsx
  — project-first governed discovery and evidence review for all 106 projects,
  with non-map access preserved; D-116 feature rendering is intentionally deferred
  to a separate frontend checkpoint.
- frontend/src/components/AustinContextMap.tsx and frontend/src/components/AppIcon.tsx
  — configured Austin OSM context map plus the lightweight navigation/map icon
  system used by the approved-style workspace; mixed D-116 point/polygon rendering
  and contextual role labels are not implemented by this governance checkpoint.
- frontend/src/features/FundingPlan.tsx and frontend/src/components/BoundaryResolution.tsx
  — server-evaluated analyst budgets, authoritative plan presentation, and exact
  equal-priority boundary resolution without client-side portfolio construction.
- frontend/src/features/HistoricalBenchmark.tsx — independently loaded historical
  outcome summary, category/project context, and presentation-only current-plan
  overlap with explicit benchmark isolation.

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
- The backend application contract environment is pinned to Python 3.14.7 and
  Pydantic 2.13.5 in the ignored `.venv`; dependency integrity passes. The local
  frontend is React/TypeScript/Vite with Node 22.23.2 and npm 11.19.1 declared in
  `frontend/package.json`; F1 transport/session, F2 Explore, F3 Funding Plan, and
  F4 Historical Benchmark checks pass locally.
- Local ADC, billing, the Vertex AI API, and quota project were verified for
  `climatecapital-ai`; the application uses `global` and configurable
  `gemini-3.5-flash`. A bounded real application call returned HTTP 200 and a
  structured governed explanation. No credential file or API key is stored in the
  repository or React, and no Cloud Run, Artifact Registry, Cloud Build, service
  account/IAM, billing-control, or deployment change has been made.
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
- D-097–D-116 govern the cross-category analytical universe, PRB reconciliation,
  model eligibility, Funding Priority, portfolio construction, runtime-v2/API
  activation, and runtime-v3 project geometry.
- Next available decision ID: **D-119**.

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-09-09 | F7B.2 production Gemini logging remediation | Added a production-mode stderr regression without `caplog`/logger-level override; reproduced zero emitted records; configured one lifecycle-scoped INFO stderr handler for only `climatecapital`; reran the focused Gemini and deployment-readiness suites; inspected content exclusion, logger restoration, Git scope, and whitespace | PASS: the regression now emits exactly one unchanged completion record containing request/surface/model/status/latency/retry/token metadata and no prompt, response, grounding, raw client key, or hidden instructions; all 50 focused tests pass with two known dependency warnings; root/Uvicorn behavior is preserved. No GCP mutation, build/deploy, Vertex call, commit, push, or F7C work |
| 2026-09-09 | Resumed F7B exact-SHA build, private candidates, and single Vertex canary | Reconciled clean `ed4f14b` source/runtime identity; listed the exact 87-file upload; built and resolved the immutable image; deployed Gemini-off and Gemini-on zero-traffic private revisions; authenticated-smoked `/health`, SPA/static, bootstrap, `$332M` plan, security/docs, and identity; issued exactly one methodology canary; inspected exact revision/request/error/completion logs | BLOCKED — SOURCE REMEDIATION REQUIRED: build `d429898d-0b21-48ad-a7e6-48d7bc4b1052`, digest `sha256:df9e1ed9…1dd49`, core, deterministic Gemini smoke, and one HTTP 200/COMPLETE grounded canary pass. The production logger emits no INFO completion entry, so retry/token/content-free completion evidence cannot be verified. Both new revisions remain private at zero traffic; no IAM, public access, promotion, commit, push, second canary, or F7C work occurred |
| 2026-09-09 | F7B.1 Cloud Run-safe health endpoint remediation | Ran focused health/API/contract/deployment tests, regenerated and checked affected schemas through the repository generator, started production-mode Uvicorn with explicit safe identity values and the compiled frontend, checked `/health`, `/healthz`, bootstrap, root, robots, production JS, security headers, and an unknown API path, then stopped the server and checked Git whitespace/status | PASS: 57 focused tests; 31 schemas match; `/health` returns 200/READY with endpoint `/health`, validated runtime-v3 deployment identity, and locked production headers; `/healthz` returns 200 with equivalent stable semantics and endpoint `/healthz`; bootstrap remains 106 projects / 74 mapped / `fixture_mode=false`; root/robots/asset return 200 and unknown API remains JSON 404. No cloud mutation, build/deploy, Vertex call, commit, push, or F7C work |
| 2026-09-09 | F7B frozen-source build and private core deployment gate | Reconciled Git/runtime identity; applied explicitly authorized bucket-only source Viewer and demonstrated repository-only Writer grants; built exact SHA `fda9176`; resolved its immutable digest; handled first-service no-traffic rejection by retaining Invoker IAM enforcement; tested anonymous denial and authenticated root/assets/favicon/robots; inspected exact revision startup/request logs and `/healthz` response | BLOCKED — SOURCE REMEDIATION REQUIRED: build `c9c52f26-0f9c-4c11-837c-cbb852eff1b7` succeeded and private core revision `climatecapital-ai-core-fda9176` is healthy on port 8080, but Cloud Run intercepts `/healthz` with a Google-generated 404 before FastAPI. No Gemini revision, Vertex call, public access, promotion, commit, push, or F7C work occurred |
| 2026-09-09 | F7A.1 bounded pre-deployment remediation | Added and ran focused deployment/runtime/static/security/Gemini tests; ran full pytest and legacy unittest; regenerated/checked 31 schemas; validated the explicit fixture; ran compilation, imports, runtime-v3 checks, and `pip check`; ran all frontend tests, lint, and production build under exact Node 22.23.2/npm 11.19.1; started production-mode Uvicorn against the actual compiled SPA and checked root, robots, health, bootstrap, `$332M` plan, headers, and disabled docs; inspected Git/secret/artifact hygiene and Docker availability | PASS: 73 focused tests, 506 pytest tests plus 137 subtests, 152 legacy tests, 31 schemas, fixture/compilation/import/dependency checks, 9 frontend files / 108 tests, lint, and 79-module build all pass. Production smoke reports 106 projects, 74 mapped, `fixture_mode=false`, and unchanged 18 / `$331.825M` / `$175K` plan facts. Docker is not installed, so local image build/run is unavailable and F7B Cloud Build remains authoritative. No cloud mutation, deployment, commit, push, governed-data change, or `.node-version` change |
| 2026-09-09 | F7A GCP deployment-readiness and configuration audit | Reconciled frozen Git baseline and deployment docs/source; inspected container/build/static/routing/configuration/runtime-v3/Gemini/security surfaces; queried gcloud account/project/billing/API/resource/IAM/ADC state read-only; checked current official Cloud Run, Artifact Registry, Cloud Build, Vertex pricing/IAM guidance; directly probed health/bootstrap/root/docs/robots/security headers; ran 53 focused backend tests and the production frontend build with exact Node/npm; checked manifest identity and Git hygiene | READY WITH PRE-DEPLOYMENT FIXES: locked one-service Cloud Run topology remains correct, project/ADC/Vertex are ready, and frontend/runtime/Gemini checks pass, but root is 404, health reports legacy `FIXTURE` plus zero identities while bootstrap is runtime-v3, required container and release web controls are absent, and token counts are not logged. Cloud Run/Artifact Registry/Cloud Build APIs, repository, runtime service account, and service are expected F7B setup. No cloud mutation, deployment, product/data change, commit, push, or `.node-version` change |
| 2026-09-09 | F6D final regression and release-candidate smoke | Reconciled branch/HEAD/upstream/diff/untracked scope; ran `.venv/bin/python -m pytest -q`, legacy unittest discovery, 31-schema parity, explicit fixture validation, `compileall`, public backend imports, `pip check`, full frontend tests, ESLint, and the TypeScript/Vite build under pinned Node 22.23.2/npm 11.19.1; ran Git hygiene checks; started the real FastAPI/Vite runtime and smoke-tested Explore/Barton Springs detail, a `$332M` plan, one live plan-grounded Gemini explanation, Explore/Funding Plan navigation, Historical Benchmark, health/bootstrap/title, request outcomes, and backend logs | PASS: 486 pytest tests plus 137 subtests; 152 legacy tests; 31 schemas; valid explicit fixture; compilation/import/dependencies clean; 9 frontend files / 108 tests; lint; 79-module build; diff check. Live health/bootstrap/plan/Gemini/benchmark requests returned 200; runtime-v3 served 106 projects / 74 map features with `fixture_mode=false`; title was `ClimateCapital AI`; `$332M` produced 18 projects / `$331.825M` selected / `$175K` remaining; Gemini stated it did not select or change projects and product state persisted. Initial `create_app` probe and signed-host Node/WASI failures were verification-environment issues; corrected public imports and pinned child PATH passed. Temporary ignored packages were removed. No additional defect, artifact, secret, deployment, commit, or push |
| 2026-09-09 | F6C Gemini and cross-feature live acceptance | Reconciled the interrupted working tree; reused FastAPI at `127.0.0.1:8000` and Vite at `127.0.0.1:5173`; checked `/healthz` and bootstrap; exercised real ADC-backed Vertex Gemini in product/methodology, mapped Barton Springs Bridge, unmapped Bolm Maintenance Center, and completed `$700M` Funding Plan contexts; tested project/plan transitions, official-score/location/optimization/recommendation boundaries, empty and pending submission behavior, desktop and narrower effective Safari layouts, browser console, request outcomes, and backend logs; inspected the existing safe error/retry presentation rather than sabotaging credentials | PASS: live Gemini responses preserved governed facts, explicit unavailable geometry, deterministic plan authority, and the 31-project `$699.975M` / `$25K` plan state; unsupported score, geometry, optimization, weighting, and official-recommendation requests were not claimed as actions; context updated without stale attribution or state corruption; observed Gemini and plan requests returned 200; no application console error, exception, runaway call, contract mismatch, secret exposure, implementation defect, or F6C code change. Browser-control detachment was tooling-only; F6D/deployment/commit/push not started |
| 2026-09-08 | F6B core live browser acceptance | Started FastAPI at `127.0.0.1:8000` and Vite at `127.0.0.1:5173`; exercised the non-Gemini shell, Explore/filter/reset, mapped and unavailable-location projects, detail switching, map legend/zoom, deterministic `$332M` and `$700M` plan paths including analyst resolution and invalid input, all three supporting pages, desktop/831px/390px responsive states, Chrome console, request/backend logs, and title retest; ran `npm test -- src/App.test.tsx`, `npm run build`, live health/title checks, `git diff --check`, and status review | PASS WITH FIXES: all core journeys passed; 106 projects, 74 supported map locations, and 32 unavailable-location paths rendered coherently; `$332M` completed at `$331.825M` / 18 projects and `$700M` completed at `$699.975M` / 31 projects after explicit rank-28 analyst resolution; bootstrap, benchmark, and plan requests returned 200; console had only the standard React development notice; corrected only `<title>frontend</title>` to `ClimateCapital AI`; 16 focused tests and 79-module build passed; `.node-version` untouched; no Gemini conversation, deployment, commit, or push |
| 2026-09-08 | F6A frozen-baseline and automated full regression | Confirmed `main`, `HEAD`, `origin/main`, commit `be78a78`, and initial working tree; ran `.venv/bin/python -m pytest -q`, legacy `.venv/bin/python -m unittest discover -s tests -v`, schema parity, Python compilation, direct backend/package imports, `pip check`, explicit fixture CLI validation, frontend `npm test`, ESLint, the TypeScript/Vite production build under Node 22.23.2/npm 11.19.1, and Git whitespace/status checks | Passed: HEAD exactly equals `be78a78` and `origin/main`; initial tree contained only the documented untracked `.node-version`; 486 pytest tests plus 137 subtests and 152 unittest-discovered tests passed; 31 schemas verified; imports, compilation, dependencies, fixture validation, 9 frontend files / 108 tests, lint, 79-module build, and whitespace checks passed. Only the two known dependency deprecations and the environment-only pip-cache warning remain. No browser, real Vertex, deployment, commit, push, or implementation change; only this required progress record changed |
| 2026-09-08 | F5B mandatory Gemini on Vertex AI integration and acceptance refinements | Ran 28 focused Gemini tests and all 486 Python tests; checked all 31 generated schemas and dependencies; ran 9 frontend files / 108 tests, ESLint, and the production build; exercised Project, `$332M` Plan, `$700M` Boundary, Benchmark, and Methodology contexts in the running application; used Chrome DevTools for the full boundary text/safeguard, console, 1440/900/390 layout metrics, independent workspace scroll, fixed sidebar/profile, pane geometry, and overflow checks; reviewed security and Git state | Passed: four bounded live calls in this session plus the earlier real Methodology smoke used Vertex AI `gemini-3.5-flash`; Project and plan explanations were governed; the Boundary response used rank 28 / score 67, required analyst judgment, and matched no project-selection/recommendation pattern; Benchmark remained retrospective; 486 tests passed with only the Starlette/AnyIO and google-genai/Python 3.14 deprecation warnings; 31 schemas verified; no broken requirements; 108 frontend tests, build, lint, and Git whitespace checks pass; no console application error or horizontal overflow; `.node-version` untouched; nothing staged, committed, pushed, or deployed; F6 not started |
| 2026-09-08 | Frontend runtime-v3 governed map integration | Exercised the actual running frontend/API in Chrome DevTools at desktop and 400×748 responsive widths; checked the live bootstrap identity/counts/types, OSM tiles/attribution, legend/role styling, filter synchronization, mapped list selection/polygon focus/detail, unmapped list selection/no map movement/detail, responsive stacking, and console; ran all frontend tests, ESLint, TypeScript/Vite production build, and `git diff --check` under Node 22.23.2 | Passed: live release `3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1`; 106 projects, 74 mapped, 32 location unavailable, 64 points, 9 polygons, 1 multipolygon, `fabricated_geometry=false`; 8 test files / 80 tests; lint; 78-module build; diff check; no application console errors. No backend methodology, governed artifact, Funding Priority, Funding Plan, benchmark, `.node-version`, stage, commit, push, or deployment change |
| 2026-09-08 | D-116 cross-category project geometry governance | Validated all 106 governance decisions and the 80-feature candidate source snapshot; regenerated governed reconciliation and runtime-v3 deterministically; checked exact category/geometry/display-role/status/reason totals, source and governance hashes, runtime-v2 immutability, runtime-v3 catalog/benchmark byte equality, map/catalog identity, citywide exclusion, Austin-region coordinates, role/type failures, runtime cross-artifact drift rejection, standard API activation, and protected plan/benchmark regressions; ran focused/full pytest, schema generation/check, Python compilation, `pip check`, Markdown checks, Git scope/status, and `git diff --check` | Passed: 74 promoted and 32 unmapped; 64 points, 9 polygons, and 1 multipolygon; 51 focused tests; 458 full tests plus 137 subtests; 32 schemas match; deterministic builders are idempotent; runtime-v2 remains 0/106; active release `3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1`; no frontend, analytical, Funding Priority, Funding Plan, request, PRB, benchmark, `.node-version`, cloud, stage, commit, push, or deployment change |
| 2026-09-08 | External GIS evidence investigation for governed 106-project universe | Reconciled catalog identities against official City CPE, WPD/RNA, PARD/APR, AFM, fire, EMS, library, bridge/ACT, APD design, and TCAD parcel evidence; generated and re-read candidate CSV/JSON; asserted row/ID/category/confidence/geometry/eligibility totals; inspected source IDs, feature IDs, vintages, historical fit, report links, runtime geometry contract, Git diff/status, and whitespace | Passed: 106 rows and 106 unique `decision_unit_id`; exact 9/22/37/38 category coverage; 76 HIGH source-native, 0 HIGH address-derived, 13 MEDIUM, 2 LOW, 15 NO_MATCH; 68 point, 12 polygon, 1 address-only, 25 no geometry; 74 eligible for governance review and 32 held/unmapped. Every row is candidate/not-governed; runtime remains 0 mapped / 106 unmapped and `fabricated_geometry=false`; no governed data, backend, methodology, Funding Priority, Funding Plan, benchmark, `.node-version`, staging, commit, push, or deployment change |
| 2026-09-07 | Focused post-F5A frontend visual refinement | Inspected the application repeatedly in Chrome DevTools at full width, docked/tablet width, and 400×748 responsive emulation; exercised Explore filters/reset, layers, project detail open/close, Funding Plan $332M evaluation, Historical Benchmark navigation/content, OSM tiles/attribution, and console; ran focused and complete frontend tests, ESLint, TypeScript/Vite production build, Git whitespace/status review | Passed: 19/19 focused Explore/App tests and 7 files/69 tests overall; `npm run lint`; `npm run build` (78 modules); `git diff --check`. Austin tiles and attribution rendered; no project markers rendered for the governed 0 mapped/106 unmapped contract; $332M evaluation completed with 18 projects, $331,825,000 selected, and $175,000 remaining; responsive shell/map/list/drawer reflowed without horizontal content overflow; console had no application errors. No backend, methodology, contract, data, `.node-version`, stage, commit, push, or deployment change |
| 2026-09-07 | Frontend F4 January 21 Historical Benchmark | Ran 10 focused Historical Benchmark tests, the complete frontend suite, TypeScript/Vite production build, ESLint, targeted backend runtime-bundle/standard-API suites, contract/route/isolation scans, direct responsive-source review, and Git whitespace/status checks with Node 22.23.2/npm 11.19.1; attempted rendered browser verification | Passed: 7 frontend test files and 67 tests; 10 focused benchmark tests; `npm run build` (32 modules); `npm run lint`; 33 targeted backend tests with one known Starlette/AnyIO deprecation warning. Covered lazy standard-endpoint loading, 700/332/368 reconciliation, four categories, 20 decision-unit joins, outcome/Priority separation, false input flags, local failure/retry, runtime identity, plan/boundary isolation, and presentation-only overlap. Browser runtime exposed no available connection, so no screenshot-based visual check. No backend, `.node-version`, staging, commit, or remote change |
| 2026-09-07 | Frontend F3 governed Funding Plan workspace | Ran 13 focused Funding Plan tests, the complete frontend suite, TypeScript/Vite production build, ESLint, two targeted backend evaluator/standard-API suites, prohibited-language/endpoint scans, direct source/status review, and `git diff --check` with Node 22.23.2/npm 11.19.1 | Passed: 6 frontend test files and 53 tests; 13 focused Funding Plan tests; `npm run build` (31 modules); `npm run lint`; 26 targeted backend tests with one known Starlette/AnyIO deprecation warning. Covered exact 332M/700M/750M scenarios, custom input, decision-unit joins, shared ranks, boundary choices and acknowledgement, repeated boundaries, stale-response suppression, structured recovery, safe persistence, and no arbitrary membership or benchmark selection input. No backend, `.node-version`, staging, commit, or remote change |
| 2026-09-07 | Frontend F2 governed cross-category Explore | Ran the focused Explore/App suites, complete frontend suite, TypeScript/Vite production build, ESLint, direct source/contract and stale-term scans, scope/status review, and `git diff --check` with Node 22.23.2/npm 11.19.1; attempted rendered browser verification | Passed: 5 test files and 36 tests, including 9 focused Explore tests; `npm run build`; `npm run lint`; governed 106 and 9/22/37/38 facts, combined filtering, all required sorts, shared rank, half-point display, decision-unit selection, six rubric maxima, zero geometry/no pins, no-results recovery, and bootstrap retry covered. Browser runtime exposed no available connection, so no screenshot-based visual check. No backend, `.node-version`, staging, commit, or remote change |
| 2026-09-07 | Frontend F1 cross-category API/contract/session integration | Ran the four focused/full frontend test files, TypeScript production build, ESLint, stale v1 term/route scans, direct source/status review, and `git diff --check` using the declared Node 22.23.2/npm 11.19.1 toolchain | Passed: 4 test files and 26 tests; `npm run build`; `npm run lint`; no active v1 project-family, fixed-budget, arbitrary-membership, legacy route, or benchmark-compare dependency remains; only expected negative-test references matched the stale scan; no backend, `.node-version`, staging, commit, or remote change |
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

### 2026-09-09 — Complete F7B.2 production Gemini logging remediation

- **Correction:** Added one production-lifespan INFO stderr handler for the
  `climatecapital` logger namespace, disabled propagation to prevent duplicate
  records, and restored prior application-logger state at shutdown. The existing
  completion message and Uvicorn/root logging remain unchanged.
- **Evidence:** The no-`caplog` production regression failed with zero records
  before the correction and now captures exactly one bounded content-free event.
  All 50 focused Gemini/deployment-readiness tests and `git diff --check` pass.
- **Stop:** No cloud mutation, build/deploy, Vertex call, commit, push, or F7C work
  occurred. F7B awaits manual review/publication/new SHA; one replacement canary
  is authorized only for repaired Cloud Logging/token verification.

### 2026-09-09 — Resume F7B and stop at Gemini completion-log blocker

- **Build/deploy:** Preserved clean frozen `ed4f14b`, submitted only the 87-file
  exact-SHA context, and completed build `d429898d-0b21-48ad-a7e6-48d7bc4b1052`
  at immutable digest `sha256:df9e1ed9…1dd49`. Created private zero-traffic core
  and Gemini revisions on the same image and locked runtime configuration.
- **Evidence:** Both candidates passed `/health`, release identity, static/API,
  security/docs, 106/74/false, and exact `$332M` deterministic checks. The sole
  canary returned 200/COMPLETE in 4.761 seconds, used the governed methodology
  surface, and preserved explanation-only authority.
- **Stop:** The existing bounded completion logger is INFO-level but production
  emits no application INFO record; exact Cloud Logging searches found only the
  request/access record and SDK advisory. Token/retry and content-free completion
  evidence cannot pass. No new IAM, public access, traffic promotion, second
  canary, source change, commit, push, or F7C work occurred.

### 2026-09-09 — Complete F7B.1 Cloud Run-safe health remediation

- **Correction:** Added `/health` as the authoritative production route while
  retaining `/healthz` as a local/backward-compatible alias. Both routes share
  the unchanged validated runtime-v3 health construction and report their exact
  endpoint. Updated only the strict health contract, affected generated schemas,
  focused tests, production-health documentation, D-118, and this handoff.
- **Evidence:** 57 focused tests and all 31 schema parity checks passed.
  Production-mode Uvicorn returned 200/READY for `/health`, 200 for `/healthz`,
  equivalent stable health semantics, the locked headers, 106 projects, 74 mapped
  contexts, `fixture_mode=false`, working root/robots/assets, and JSON 404 for an
  unknown API route.
- **Stop:** No cloud mutation, build/deploy, Vertex call, commit, push, or F7C work
  occurred. Manual review/commit/push and a new frozen SHA are mandatory before
  F7B resumes; the `fda9176` image/revision must not be promoted as final.

### 2026-09-09 — Resume F7B and stop at Cloud Run `/healthz` blocker

- **Execution:** Preserved frozen `fda9176`; applied only the newly authorized
  Cloud Build bucket Viewer binding and the previously authorized repository-only
  Writer binding after its exact demonstrated denial; completed the immutable
  image build and created one private Gemini-disabled core revision.
- **Evidence:** Build and startup passed; the container listens on port 8080 and
  the compiled SPA/static surface works. The first-service no-traffic command was
  rejected before creation, so the supported fallback kept Invoker IAM enabled;
  unauthenticated access is denied. Cloud Run itself intercepts `/healthz` with a
  Google HTML 404, and revision logs prove the request never reaches FastAPI.
- **Stop:** Source remediation and a new frozen SHA are required. No Gemini
  revision, Vertex canary, public-access enablement, final promotion, application
  change, commit, push, key, or F7C work occurred.

### 2026-09-09 — Complete F7A.1 pre-deployment remediation

- **Continuity:** Preserved frozen `1e30c2d`, the accepted F7A progress checkpoint,
  and untouched `.node-version`; inspected the existing tree before editing.
- **Implementation:** Completed only the six bounded P1 deployment corrections:
  same-origin SPA serving, runtime-v3 health/identity authority and fail-closed
  production identity, pinned non-root multi-stage container boundary, crawler/
  security/docs controls, content-free Gemini usage logs, and related tests,
  schemas, and IAM/ADC documentation.
- **Verification/handoff:** All focused/full backend, legacy, schema, fixture,
  compile/import/dependency, frontend test/lint/build, hygiene, and real local
  production Uvicorn smoke checks pass with the counts above. Docker is not
  installed, so F7B Cloud Build must supply the remote image evidence. No cloud
  or IAM mutation, deployment, commit, or push occurred. Stop for user review,
  manual publication, and freezing a new exact SHA before F7B.

### 2026-09-09 — Complete F7A deployment-readiness audit

- **Audit:** Verified frozen `1e30c2d`, inspected only the deployment/runtime
  surface, queried GCP read-only, and retained the locked one-container Cloud Run
  design. Project billing, local auth/ADC, and Vertex are ready; the expected
  Cloud Run, Artifact Registry, Cloud Build, repository, runtime identity, and
  service setup does not yet exist.
- **Finding:** Classified no P0 blocker, a bounded set of P1 source/configuration
  fixes, normal P2 cloud setup, and optional later billing/image-retention polish.
  Direct probes proved the missing SPA root, legacy fixture health identity,
  exposed framework docs, absent crawler/security controls, and missing token-count
  logging; focused backend tests and the exact-toolchain frontend build passed.
- **Handoff:** Do not deploy `1e30c2d` as-is. After separate authorization, apply
  and verify only the P1 correction, freeze its true Git SHA, then execute the
  documented F7B no-traffic build/deploy/verify/promote sequence. No cloud or
  application mutation, deployment, commit, or push occurred in F7A.

### 2026-09-09 — Complete F6D final regression and F6 closeout

- **Reconciliation:** Confirmed `main`, `HEAD`, `origin/main`, and merge base at
  `be78a783c125b943d4da4441f9a290a1c875bc15`. Accounted for only the accepted
  F6 progress record and one-line browser-title fix; kept `.node-version`
  untouched and found no staged, secret, temporary, generated, or unrelated path.
- **Automated closeout:** Passed the complete current-tree Python, legacy unittest,
  schema/release/fixture, compilation/import/dependency, frontend test/lint/build,
  and Git-hygiene surfaces with the exact counts recorded above. A mistaken import
  symbol and the signed host's native-module restriction were environment/probe
  issues; the correct public imports and pinned Node 22 child PATH passed. All
  temporary ignored fallback files were removed.
- **Live smoke:** Verified real local health/bootstrap/title, 106/74 Explore data,
  representative Barton Springs detail, the deterministic `$332M` plan, one live
  explanation-only Vertex response, Explore/Funding Plan navigation, Historical
  Benchmark, and successful request/backend health. Product state remained intact
  after Gemini closed; services stopped cleanly.
- **Result/handoff:** No additional F6D defect or implementation fix was required.
  F6A PASS, F6B PASS WITH FIXES, F6C PASS, and F6D PASS make F6 complete. F7 is
  ready only after explicit authorization; nothing was deployed, committed, or
  pushed.

### 2026-09-09 — Complete F6C Gemini and cross-feature live acceptance

- **Continuity:** Resumed the interrupted F6C run without repeating accepted F6A,
  F6B, or completed F6C checks. Confirmed the worktree still contained only this
  intentional progress change, the accepted F6B `frontend/index.html` title fix,
  and the untouched pre-existing `.node-version`.
- **Live completion:** Finished the unmapped Bolm location-grounding path, a real
  analyst-resolved `$700M` Funding Plan, project/plan cross-feature transitions,
  product-authority boundary prompts, safe supported recovery checks, narrower
  Gemini layout inspection, and final console/request/backend-log review. The
  Vertex-backed responses and application state remained coherent and governed.
- **Result:** F6C passed with no implementation defect or F6C code change.
  Browser-automation detachment was an external tooling issue, not an application
  failure. No targeted automated tests were required because no code changed.
- **Scope/handoff:** No methodology, governed data, deterministic plan semantics,
  Gemini architecture, dependency, deployment, F6D/F7, commit, or push work
  occurred. F6D is ready only after explicit user authorization.

### 2026-09-08 — Complete F6B core live browser product acceptance

- **Continuity:** Continued from accepted F6A without repeating it, retained
  `main` at `be78a78`, preserved the intentional F6A progress change, and left the
  pre-existing untracked `.node-version` untouched.
- **Live acceptance:** Ran the real backend/frontend and exercised the non-Gemini
  product in Chrome. Verified the primary/reference shell, compact Explore totals,
  all-category project data, filters/reset, 74 supported map contexts, explicit
  unavailable-location behavior, representative detail/provenance and project
  switching, map controls/legend, deterministic plan construction, analyst
  resolution, invalid input, benchmark, methodology, help, responsive reflow,
  desktop profile/sticky shell, console, network calls, and backend logs.
- **Defect correction:** Found the browser tab exposed the development placeholder
  title `frontend`. Changed only `frontend/index.html` to use
  `ClimateCapital AI`, then verified the served title, 16 focused App tests, and
  the 79-module production build. No other implementation defect was found.
- **Scope/handoff:** No Gemini conversation, F6C/F6D, methodology, architecture,
  governed data, product-scope, dependency, deployment, F7, commit, or push work
  occurred. F6C is ready only after explicit user authorization.

### 2026-09-08 — Complete F6A baseline and automated full regression

- **Baseline:** Verified `main` and `origin/main` at frozen accepted F5 commit
  `be78a783c125b943d4da4441f9a290a1c875bc15`. Initial status contained only the
  previously documented untracked `.node-version`, which remained untouched.
- **Automated evidence:** Passed 486 pytest tests plus 137 subtests and the legacy
  152-test unittest discovery command; verified 31 schemas, Python compilation,
  backend/package imports, dependency integrity, the development-fixture CLI, 9
  frontend files / 108 tests, ESLint, and the 79-module TypeScript/Vite build.
- **Classification:** No application regression or defect was found. A failed
  preflight import was an invocation setup issue corrected by using the repository
  source path. The default shell Node/npm mismatch was avoided by using the
  existing pinned Node 22.23.2/npm 11.19.1 toolchain. Known dependency
  deprecations and the disabled pip-cache warning remain non-blocking.
- **Scope/handoff:** Changed only this required canonical progress record. Did not
  start services, perform browser/manual acceptance, call Vertex, alter product or
  analytical behavior, deploy, commit, or push. F6B core live browser product
  acceptance is ready only after explicit user authorization.

### 2026-09-08 — Complete F5B Gemini/Vertex integration and acceptance

- **Continuity:** Resumed the interrupted unstaged F5B tree at published baseline
  `851aa0b`. Preserved the existing architecture and the manual correction that
  acquires one application rate-limit token before the provider retry loop. Added
  a regression proving an internal retry cannot consume a second user token.
- **Implementation closeout:** Completed the five requested UI refinements:
  primary/reference sidebar grouping, viewport-pinned desktop sidebar/profile,
  compact side-oriented Explore snapshot, removal of the large redundant map
  overlay, and coordinated Project Detail + Gemini layouts. Mobile keeps selected
  project category/request/Priority/rank and governed location status inside the
  full-width assistant sheet.
- **Browser/live QA:** The running app preserved `$332M` as COMPLETE with 18
  projects, `$331,825,000` selected, and `$175,000` remaining; `$700M` remained
  ANALYST_RESOLUTION_REQUIRED at rank 28 / score 67. Real Vertex explanations
  passed for mapped Project, Funding Plan, Boundary, Historical Benchmark, and
  the previously completed Methodology smoke. Chrome DevTools confirmed the
  boundary answer required analyst judgment and selected no project; the console
  contained only React's development-tools notice. Exact 1440/900/390 metrics
  showed no document overflow, desktop pane overlap, or sidebar/profile drift.
- **Verification:** 28 Gemini backend tests and all 486 Python tests pass with the
  two known dependency deprecations; 31 schemas verify; `pip check` reports no
  broken requirements; all 9 frontend files / 108 tests, build, and lint pass.
  Git whitespace and security checks pass.
- **Scope/handoff:** No analytical method, governed project/request/PRB/rank,
  deterministic evaluator, benchmark semantics, or geometry governance changed.
  `.node-version` is untouched; nothing is staged, committed, pushed, or deployed.
  F5B is ready for user approval. F6 has not started.

### 2026-09-08 — Finish frontend runtime-v3 governed map integration

- **Objective/continuity:** Resumed the partially completed uncommitted frontend
  checkpoint from disk after `71d92e3`; inspected Git, the active runtime-v3 map
  contract/data, governing product/architecture decisions, and existing frontend
  implementation. Preserved the prior work and untouched untracked `.node-version`.
- **Implementation:** Finished strict client validation and release fixtures;
  governed point, polygon, and multipolygon rendering; distinct project,
  facility/site, and park/site styles; legend and caveat; selected geometry focus;
  filter-aware map/list synchronization; map-to-row scrolling; list-to-detail/map
  selection; Project Detail evidence/unavailable states; and responsive map/card
  reflow. Updated obsolete 0/106 frontend expectations to 74/32 and added focused
  client, map interaction/focus/no-movement, and Explore detail regressions.
- **Browser QA:** Against the live runtime-v3 application, Chrome DevTools showed
  74 governed features and 32 unavailable locations with OSM attribution. Verified
  a mapped project-site polygon focuses and exposes governed source/caveat detail;
  an unmapped project opens `Map location unavailable` without changing map
  extent; project search reduces map and list together; the role legend is
  legible; and desktop plus 400×748 layouts avoid horizontal overflow. No
  application console errors appeared.
- **Verification:** `npm test -- --run` passes 8 files / 80 tests; `npm run lint`
  passes; `npm run build` passes with 78 modules; `git diff --check` passes. Live
  `/api/v1/bootstrap` identity is
  `3a626c11d7e9af503c49be7f9b9cc67ead5c42ac998da7b9bcdcb09172feade1`
  with 106 projects, 74 mapped, 32 unavailable, 64 points, 9 polygons, 1
  multipolygon, and no fabricated geometry.
- **Scope/handoff:** No backend, methodology, governed data, Funding Priority,
  Funding Plan, benchmark, cloud, stage, commit, push, or deployment change. The
  checkpoint is ready for review/commit/push, followed immediately by F5B.

### 2026-09-08 — Govern cross-category project map evidence under D-116

- **Objective:** Review every governance-eligible candidate conservatively,
  promote only defensible project map evidence, preserve all analytical contracts,
  and stop before frontend rendering.
- **Continuity:** Inspected and preserved the existing frontend refinement,
  candidate investigation artifacts, and untracked `.node-version`. Reused the
  completed official-source research without repeating acquisition or matching.
- **Decision:** Promoted 74 HIGH-confidence source-native features: 35 Watershed,
  21 Parks & Open Space, 17 Community Facilities, and 1 Transportation. Governed
  roles are 42 project display points, 22 facility-site context points, 8
  park-site context polygons, 1 project-site polygon, and 1 project parcel.
- **Unmapped:** Kept 32 projects unmapped. This includes both disputed Watershed
  rows, both conflicting EMS Demand locations, the overbroad Bolm Maintenance
  polygon, every unresolved Transportation corridor/asset, all low-confidence
  campus context, all address-only/no-match candidates, and the ambiguous
  Elisabet Ney representations.
- **Implementation:** Added an all-106 governance contract/artifact, captured the
  80 candidate source geometries as an explicitly research-only snapshot, added
  map-context/manifest v3 contracts and schemas, created immutable runtime-v3,
  strengthened runtime cross-artifact validation, and activated the standard API
  against runtime-v3. Added narrow Git allowlist exceptions for the two required
  GeoJSON artifacts. Runtime-v2 remains unchanged.
- **Protected behavior:** Runtime-v3 catalog and benchmark are byte-identical to
  runtime-v2. Funding Priority, ranks, requests, plan evaluator/state machine,
  analytical universe, and Historical Benchmark are unchanged. No fabricated,
  geocoded, inferred, or centroid geometry exists.
- **Verification:** 51 focused tests and the 458-test full Python suite plus 137
  subtests pass; 32 generated schemas match; builders reproduce exact bytes and
  are idempotent; compilation, dependency integrity, Markdown checks, and diff
  checks pass. The known Starlette/AnyIO deprecation warning remains non-failing.
- **Handoff:** Review D-116. Map rendering is a separate frontend checkpoint and
  must support points/polygons plus contextual role labeling while leaving all 32
  unmapped projects accessible through list/detail/plan paths.

### 2026-09-08 — Investigate external GIS evidence for all 106 projects

- **Objective:** Resume the interrupted evidence investigation without repeating
  completed work, determine trustworthy project-specific map candidates, and stop
  before any governed/runtime promotion.
- **Continuity:** Inspected the working tree first; preserved the complete unstaged
  post-F5A frontend refinement, untouched untracked `.node-version`, and the prior
  temporary official-source downloads/queries. Continued from the unresolved
  source-vintage, unmatched-project, and all-project artifact step.
- **Investigation:** Queried official City CPE and ArcGIS services; reconciled WPD
  CIP, RNA, park boundaries, PARD facilities, APR capital projects, AFM facilities,
  fire, EMS, libraries, official bridge/ACT and facility records, APD design
  evidence, and the TCAD parcel service. Avoided inferred coordinates and generic
  geographic proxies.
- **Key finding:** Decimal canonicalization resolves trailing-zero IDs in the City
  APIs. All 37 Watershed IDs have one exact official display point on the January
  21 snapshot date; 29 also have later polygon representations. `5789.127` remains
  held for a source-name/scope conflict, and citywide `5789.150` remains held so a
  display point cannot imply false program extent.
- **Artifacts/result:** Added a 106-row candidate CSV, summary JSON, and detailed
  report. Totals are 76 HIGH source-native, 0 HIGH official-address-derived, 13
  MEDIUM, 2 LOW, and 15 NO_MATCH; 74 may proceed to explicit governance review and
  32 remain held/unmapped. Primary representations are 68 points, 12 polygons, 1
  address-only, and 25 no geometry.
- **Verification/scope:** Re-read and asserted all artifact totals and unique IDs,
  inspected source/feature metadata and historical-fit notes, checked documentation
  and Git scope, and confirmed runtime geometry remains 0/106 with no fabricated
  coordinates. No source promotion, production pins, analytical change, backend,
  `.node-version`, staging, commit, push, or deployment action occurred.
- **Handoff:** Stop here for user review. A later governance task should define
  accepted geometry roles and snapshot isolation before importing any of the 74
  eligible candidates; the other 32 must remain explicitly unmapped meanwhile.

### 2026-09-07 — Refine the published F5A frontend against approved designs

- **Objective:** Compare the published F5A application at `fe66a49` with the
  approved design screenshots, implement a focused frontend visual refinement,
  and preserve the governed 106-project product and all analytical contracts.
- **Implementation:** Added a dark compact navigation shell, route-aware workspace
  header, analyst profile, icon system, denser decision cards, approved purple and
  green visual language, responsive layouts, a fixed Project Detail drawer,
  clearer Explore/filter/list states, Funding Plan utilization treatment, and
  stronger Historical Benchmark presentation. Added stable form IDs/names after a
  DevTools accessibility/autofill audit.
- **Map evidence:** Reconciled the repository and runtime contract before coding.
  The API reports `NO_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE`, zero mapped projects,
  106 unmapped projects, empty features, and `fabricated_geometry=false`. Added the
  configured Austin OSM context map and attribution with no project pins; the UI
  states the limitation in both the map overlay and layers disclosure. Historical
  RNA matches remain research-only and were not promoted or transformed.
- **Browser verification:** Repeated Chrome DevTools checks covered full-width,
  docked/tablet, and 400×748 responsive layouts; map rendering and zoom controls;
  layers; active filter reset; project selection/detail/close; governed $332M plan
  evaluation; Historical Benchmark navigation/content; and console output. No
  application console errors occurred; the final Issues audit was 0/0/0.
- **Automated verification:** Focused Explore/App tests pass 19/19; the full suite
  passes 7 files/69 tests; ESLint, TypeScript/Vite build, and `git diff --check`
  pass with Node 22.23.2/npm 11.19.1.
- **Handoff:** Proceed to F5B. All refinement changes remain unstaged and
  uncommitted; no backend, methodology, data, cloud, deployment, `.node-version`,
  push, or durable decision change occurred.

### 2026-09-07 — Implement frontend F4 January Historical Benchmark

- **Objective:** Add the isolated January 21, 2026 historical outcome experience
  without beginning Gemini, deployment, final release work, or backend changes.
- **Implementation:** Added a dedicated navigation route and component-local
  benchmark loader with retry and runtime/catalog identity validation. Presented
  API-sourced package reconciliation, false ranking/selection input flags, four
  historical category summaries, 20 catalog-joined recommended outcomes, source
  provenance, and a restrained CSS composition treatment.
- **Isolation:** The benchmark is not persisted, does not gate bootstrap or Funding
  Plan, and never enters evaluator requests or boundary resolutions. Optional
  current-plan overlap is a count-only, presentation-only set intersection from
  already authoritative client data.
- **Contract boundary:** The API does not expose per-category full-package or
  outside-cohort dollars. F4 displays matched category outcomes and governed catalog
  requests, explicitly keeps the outside-cohort amount citywide, and invents no
  missing partition.
- **Verification:** 7 frontend test files/67 tests, including 10 focused benchmark
  tests, build, and lint pass under Node 22.23.2/npm 11.19.1. Targeted backend
  runtime-bundle/standard-API suites pass 33 tests with one known warning. Direct
  route, isolation, responsive-source, and prohibited-language scans pass. No
  browser connection was available for screenshot-based visual QA.
- **Handoff:** Stop for F4 review. F5 is the next separately authorized checkpoint.
  Frontend remains untracked/unstaged, `.node-version` is untouched, and no commit
  or push occurred.

### 2026-09-07 — Implement frontend F3 governed Funding Plan

- **Objective:** Build the priority-constrained analyst Funding Plan workflow on the
  standard evaluator without starting benchmark presentation, Gemini, deployment,
  or backend work.
- **Implementation:** Added 332M, 700M, and 750M reference presets, custom budget
  validation, authoritative plan summaries, selected-project joins, readable
  warnings/selection sources, and a responsive boundary-resolution panel. Boundary
  submissions use the exact backend resolution structure and accumulated decisions.
  Exact-input retries retain the expected fingerprint; changed analyst decisions
  clear it before their new deterministic evaluation. Same-tier advancement is
  never acknowledged silently.
- **Method boundary:** Added no project-membership editor, local portfolio logic,
  score-per-dollar measure, hidden tiebreak, optimization claim, or benchmark input.
  Equal official ranks remain equal, and remaining budget is reported neutrally.
- **Session/error behavior:** Persisted inputs are version-bound while evaluation
  results are re-requested. New budgets clear prior resolutions; runtime conflicts
  reload governed bootstrap; fingerprint conflicts re-evaluate safely; and existing
  abort/generation guards prevent older responses replacing newer analyst input.
- **Verification:** 6 frontend test files/53 tests, including 13 focused Funding Plan
  tests, build, and lint pass under Node 22.23.2/npm 11.19.1. The two targeted
  backend suites pass 26 tests with one known deprecation warning. Direct route,
  language, source, and scope scans pass. No browser connection was available for
  screenshot-based visual QA.
- **Handoff:** Stop for F3 review. F4 is the next separately authorized checkpoint.
  Frontend remains untracked/unstaged, `.node-version` is untouched, and no commit
  or push occurred.

### 2026-09-07 — Implement frontend F2 governed Explore

- **Objective:** Build a polished, project-first Explore experience for the
  activated 106-project runtime, without beginning Funding Plan interaction,
  benchmark presentation, Gemini, deployment, or backend work.
- **Implementation:** Added search, category/rank/request filtering, four governed-
  field sorts, result and request totals, clear/no-results states, accessible
  project cards, and a responsive project-detail surface keyed by
  `decision_unit_id`. Detail presents the governed request, official Funding
  Priority/tie semantics, six components on their own rubric maxima, source and
  context fields, optional canonical provenance, and request-conflict disclosure.
- **Geometry/method:** Rendered no project map or pins and explicitly communicates
  0 mapped/106 unmapped. No new score, weighting, optimizer, historical-outcome
  influence, geocoding, or analytical tiebreak was introduced.
- **Session/application:** Reused F1 bootstrap and persistence; no second fetch or
  state framework. Added same-loader bootstrap retry. Explore inputs and selected
  decision unit restore only within the F1 runtime-identity boundary.
- **Verification:** 5 test files/36 tests, build, and lint pass under declared Node
  22.23.2/npm 11.19.1. Direct scope/stale-term review and repository checks pass.
  Browser-based rendering was attempted, but no browser connection was available.
- **Handoff:** Stop for F2 review. F3 is the next separately authorized checkpoint.
  Frontend remains untracked/unstaged, `.node-version` is untouched, and no commit
  or push occurred.

### 2026-09-07 — Implement frontend F1 cross-category integration

- **Objective:** Replace the legacy Watershed frontend data/API/session layer with
  the activated 106-project runtime-v2 integration, without beginning F2–F4 or
  changing the frozen backend.
- **Implementation:** Added schema-aligned bootstrap, project, map, Funding Plan,
  benchmark, response-identity, and error types; defensive same-origin standard API
  clients; version-bound session storage; safe input-only restoration; structured
  request state; and abort/generation request-order protection.
- **Application boundary:** Updated only enough application wiring to initialize
  from runtime-v2 and hold all 106 projects. Replaced the incompatible v1 Funding
  Plan interaction with a clearly marked transition surface pending F3. No Explore
  list/detail/filter, map UX, budget presets, boundary controls, or benchmark cards
  were implemented.
- **Verification:** 4 test files and 26 tests pass; production build and lint pass;
  stale-contract scan has only deliberate negative-test matches; `git diff --check`
  passes. The package commands used the declared Node 22.23.2/npm 11.19.1 toolchain
  because the host-default Node 24 process cannot load the existing signed Rolldown
  native binding.
- **Handoff:** Stop for F1 review. F2 is the next separately authorized checkpoint.
  Frontend remains untracked/unstaged, `.node-version` is untouched, and no commit
  or push occurred.

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
