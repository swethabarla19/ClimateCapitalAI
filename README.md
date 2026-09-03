
# ClimateCapital AI

**ClimateCapital AI** is an evidence-first decision-support prototype for exploring climate-relevant capital investments and building transparent funding scenarios.

The P0 pilot uses a **historical Austin Watershed planning context** to demonstrate how governed public-sector evidence, deterministic budget validation, geospatial context, and bounded AI explanation can support an analyst without pretending to produce an official recommendation.

> **Current status — September 3, 2026:** M0 through M3 are complete and explicitly approved. The deterministic backend and core APIs are implemented and verified. **M4 frontend implementation is now underway.**

---

## What ClimateCapital AI Does

ClimateCapital AI is designed around a simple principle:

**AI may explain governed evidence, but deterministic software remains authoritative for facts, membership validation, and budget arithmetic.**

For the Austin Watershed P0 pilot:

- The governed source universe contains **37 Watershed projects** with **$327,970,000** in historical Department Requests.
- A documented methodology derives an exact **12-project P0 analytical family** totaling **$143,005,000**.
- The historical **$125,000,000 Watershed Projects envelope** provides the default decision context.
- Analysts control which complete project requests are included in a Funding Plan.
- Server-side deterministic logic validates project membership and calculates exact totals, remainder, overage, fingerprints, and supported scenario differences.
- The published January 2026 **Historical City Recommendation** is kept structurally separate and used only as a descriptive benchmark.

ClimateCapital AI does **not** currently produce a Funding Priority score, project rank, Importance weight, optimizer-selected portfolio, expected flood-reduction benefit, or beneficiary estimate because the governed evidence does not support those claims consistently enough for P0.

---
# Google Cloud Integration

Google Cloud is part of the project architecture from source governance through final deployment.

The project deliberately separates:

1. **controlled data preparation and validation**, and
2. **the eventual application runtime**.

That means Google Cloud services are used where they provide a clear architectural purpose rather than being added simply for breadth.

## Google Cloud services used so far

| Google Cloud service | Current use |
| --- | --- |
| **BigQuery** | Governed raw Watershed project data validation, reconciliation, and deterministic SQL quality gates |
| **Cloud Storage** | Immutable, checksum-verified preservation of controlled source snapshots and approved source artifacts |

### BigQuery

BigQuery is used as a governed validation layer for the historical Watershed project source data.

The project has already:

- loaded the governed **37-project source universe** into the existing raw BigQuery environment;
- validated the exact **37 rows**;
- reconciled the exact **$327,970,000** historical request total;
- run persistent SQL quality checks;
- verified source sequence and project-level facts;
- used deterministic semantic fingerprints to detect unexpected changes.

BigQuery is intentionally **not** queried by the application at runtime.

That separation prevents a live warehouse change from silently changing the behavior of a released decision-support application.

### Cloud Storage

Google Cloud Storage is used for immutable preservation of controlled source material.

The project has already used Cloud Storage to preserve approved source snapshots with:

- exact source identity;
- SHA-256 checksums;
- object generations;
- create-only preservation behavior;
- provenance metadata;
- deterministic verification against local source bytes.

Cloud Storage is also intentionally **not** a runtime application dependency.

The final application will consume a reviewed, immutable release-data bundle rather than querying live source storage.

---

## Locked Google Cloud deployment path

Additional Google Cloud services are already part of the approved architecture and will be introduced only in their dependency-ordered milestones.

| Google Cloud service | Planned P0 role | Milestone |
| --- | --- | --- |
| **Cloud Run** | One public, scale-to-zero service hosting the React SPA and FastAPI API | M9 |
| **Artifact Registry** | Immutable storage for the built application container image | M9 |
| **Cloud Build** | Reproducible test, build, container, and deployment workflow | M9 |
| **Gemini on Google Cloud** | Grounded, bounded explanation of governed project/plan evidence | M8 |
| **IAM / Workload Identity** | Keyless authorization for the Cloud Run service to invoke Gemini | M8–M9 |
| **Cloud Logging** | Bounded operational and Gemini token-usage telemetry | M9 |


---

## Current Implementation

### Completed

**M0 — Delivery and architecture-informed implementation planning**
- Approved implementation, test, milestone, and execution plans.

**M1 — Versioned contracts and fail-closed release validation**
- Strict Pydantic artifact, API, plan, session, benchmark, and Gemini contracts.
- 22 generated JSON/GeoJSON schemas.
- Fail-closed four-file release-bundle validation.
- Cross-file identity, checksum, provenance, reconciliation, missingness, benchmark-isolation, and forbidden-field enforcement.

**M2A — Controlled data prerequisites**
- Governed provenance and source metadata for the Watershed project source universe and approved contextual/benchmark inputs.
- Explicit historical-fit, evidence-role, limitation, and reuse metadata.

**M2B — Development fixture and deterministic Funding Plan engine**
- Conspicuous four-file `FIXTURE` release bundle:
  - `catalog.json`
  - `map-context.geojson`
  - `benchmark.json`
  - `manifest.json`
- Exact all-37 governed universe and exact 12-project P0 family.
- Deterministic plan evaluator tested across all **4,096 subsets** of the active family.
- No geometry-derived membership, fabricated evidence, score, ranking, or optimization logic.

**M3 — Core FastAPI APIs**
- `GET /healthz`
- `GET /api/v1/bootstrap`
- `POST /api/v1/plans/evaluate`
- `GET /api/v1/benchmark`
- `POST /api/v1/benchmark/compare`
- Fail-closed core startup validation.
- Independent current/reference plan evaluation.
- One-way Historical Benchmark dependency.
- Local benchmark failure containment.
- Typed API errors and bounded request bodies.

### In progress

**M4 — Application-track frontend and required product surfaces**

The next implementation layer is the React/TypeScript/Vite/Leaflet application, including:

- Explore
- Funding Plan
- Project Detail
- Scenario/session lifecycle
- Data & Methodology
- Help & Resources
- map layers and non-map fallback behavior
- isolated Historical Benchmark
- accessible keyboard-first interaction
- conspicuous fixture-mode presentation during development

Gemini integration, reviewed-data release integration, containerization, and deployment belong to later milestones and have not been prematurely added.

---


        +-- browser sessionStorage only
