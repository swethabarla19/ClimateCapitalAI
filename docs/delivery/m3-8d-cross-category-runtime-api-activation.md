# M3.8D — Cross-Category Runtime Bundle and FastAPI Activation

**Checkpoint date:** 2026-09-06
**Historical decision snapshot:** January 21, 2026
**Predecessor runtime checkpoint:** M3.8A-C at commit `16b0809`
**Status:** Verified and runtime integration authorized

## Purpose

M3.8D completes the transition from the preserved Watershed-oriented v1 runtime
to the governed 106-project cross-category runtime-v2 model.

The analytical methodology is not reopened in this checkpoint. M3.8D implements
the already authorized M3.7F Funding Priority and M3.7D portfolio-selection
methodology through deterministic runtime contracts, artifacts, APIs, and tests.

## Activated analytical cohort

The runtime-v2 catalog contains exactly 106 governed analytical projects:

- Transportation: 9;
- Parks & Open Space: 22;
- Watershed: 37;
- Community Facilities: 38.

Governed model-request total: `$1,973,520,000`.

Program buckets, program allocations, and NOT_SCORED source decision units
remain governed provenance but do not enter the project-level runtime catalog.

## Portfolio behavior

The runtime executes
`PRIORITY_CONSTRAINED_ANALYST_GOVERNED_PORTFOLIO_CONSTRUCTION`.

Projects remain indivisible full-request units. Available Project Budget is
analyst supplied. Official PRB Funding Priority remains ordinal. Complete
higher-priority tiers are included automatically when feasible; unresolved
same-priority choices require analyst resolution rather than invented
analytical tiebreakers.

Summed-PRB utility optimization, score-per-dollar, cheapest-first,
maximum-project-count, maximum-budget-utilization, PRB-component tiebreaks,
and historical-recommendation matching remain prohibited.

## Governed runtime bundle

Runtime-v2 uses one deterministic release identity across:

- `data/governed/cross_category/runtime_v2/catalog.json`
- `data/governed/cross_category/runtime_v2/map-context.geojson`
- `data/governed/cross_category/runtime_v2/benchmark.json`
- `data/governed/cross_category/runtime_v2/manifest.json`

The manifest hashes and byte-sizes the catalog, map context, and benchmark.

Final activated release ID:

`efb3783b2f4c7568012fb9ae590ff40dbf5a46d18a3ff1942a22d424a4b52207`

## Geometry boundary

No governed cross-category project geometry is available for this runtime
checkpoint.

- mapped analytical projects: 0;
- unmapped analytical projects: 106;
- fabricated geometry: false;
- geometry is not required for model eligibility;
- geometry is not required for portfolio selection.

Council District evidence is not converted into project geometry or invented
centroids. Missing geometry does not remove a project from the analytical model.

## Historical benchmark

The January historical benchmark remains isolated from selection inputs.

- full Initial Draft Recommendation: $700,000,000;
- recommendation attached to the analytical cohort: $332,000,000;
- recommendation outside the analytical cohort: $368,000,000;
- analytical projects with January recommendation amounts: 20.

Project-level recommendation amounts are stored only in the benchmark artifact.
They do not enter the runtime catalog, Funding Priority, or portfolio evaluator.

## Standard FastAPI activation

The authoritative standard endpoints are now:

- `GET /api/v1/bootstrap` — 106-project catalog plus governed map context;
- `POST /api/v1/plans/evaluate` — governed cross-category portfolio evaluator;
- `GET /api/v1/benchmark` — isolated January historical benchmark.

`POST /api/v1/benchmark/compare` remains explicitly unavailable rather than
reusing the legacy Watershed comparison semantics.

Temporary `/api/v1/cross-category/bootstrap` and
`/api/v1/cross-category/plans/evaluate` routes are migration aliases to the
same runtime-v2 model.

## Runtime authority transition

M3.7 artifacts intentionally retain `runtime_integration_authorized=false`.
Those values record authority at their earlier checkpoints.

Only the M3.8 runtime-v2 release records
`runtime_integration_authorized=true`.

## Verification

- full repository: 440 passed;
- subtests: 137 passed;
- known warnings: one non-blocking Starlette/AnyIO deprecation warning;
- `pip check`: no broken requirements;
- schema verification: 29 schemas verified;
- runtime catalog regeneration: unchanged;
- runtime bundle regeneration: unchanged;
- `git diff --check`: clean.

## Exit state

M3.8 backend runtime activation is complete.

The next task is frontend integration against the authoritative 106-project API,
followed by end-to-end QA, feature freeze, deployment, and submission preparation.
