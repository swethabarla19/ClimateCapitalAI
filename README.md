
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

## Evidence and Analytical Boundaries

The P0 methodology intentionally distinguishes facts from contextual or incomplete evidence.

### Governed project universe

- **37 projects**
- **$327,970,000** total historical Department Requests

### P0 analytical family

- **12 projects**
- **$143,005,000** total governed requests
- Full-request treatment only
- Analyst-controlled Funding Plan membership

### Historical decision context

- Historical decision snapshot: **January 21, 2026**
- Historical Watershed Projects envelope: **$125,000,000**
- Historical simulation only
- Not an official City funding decision

### Geospatial evidence

Current RNA geometry is treated as **research-only current evidence**, not historical eligibility or project-worth evidence.

Projects without defensible geometry remain usable through non-map application paths.

Project `5789.150` is explicitly treated as a **citywide program** and receives no fabricated point, centroid, footprint, or project-level map feature.

FEMA flood-hazard and EAZ 2021 information are contextual evidence only and do not determine Funding Plan membership.

---

## System Architecture

The locked P0 architecture uses one small same-origin application:

```text
Reviewed release-data bundle
        |
        v
FastAPI / deterministic backend
        |
        +-- health / bootstrap
        +-- Funding Plan evaluation
        +-- isolated Historical Benchmark
        +-- bounded Gemini mediation (later milestone)
        |
        v
React + TypeScript + Vite + Leaflet SPA
        |
        +-- Explore
        +-- Project Detail
        +-- Funding Plan
        +-- Data & Methodology
        +-- Help & Resources
        +-- browser sessionStorage only
