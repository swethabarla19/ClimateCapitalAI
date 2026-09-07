# M3.8A — Cross-Category Runtime Contract and Data-Integration Design

**Design date:** 2026-09-06
**Historical decision snapshot:** January 21, 2026
**Predecessor:** M3.7D at commit `5f2256f`
**Status:** Runtime-integration design; deterministic implementation not yet authorized as integrated.

## Purpose

M3.8A reconciles the previously implemented Watershed-oriented runtime contracts
with the governed 106-project cross-category analytical model established through
M3.7E, M3.7F, and M3.7D.

This checkpoint changes runtime/data-contract design only.

It does not reopen analytical methodology.

Authority entering M3.8A:

- `cross_category_ranking_authorized=true`
- `portfolio_selection_authorized=true`
- `runtime_integration_authorized=false`

## Existing runtime incompatibilities

The current v1 runtime is intentionally preserved until v2 integration passes.

Current v1 assumptions that cannot govern the 106-project model include:

1. `ProjectId` accepts Watershed-style numeric subproject IDs only.
2. `catalog.json` is locked to the 37-project Watershed universe and 12-project
   active family.
3. Funding Plan input is arbitrary membership over at most 12 family projects.
4. Funding Plan result partitions the exact 12-project active family.
5. Browser session state hardcodes the old $125M Historical Envelope for the
   Session Reference Plan.
6. Map feature project linkage uses the Watershed project-ID format.
7. Gemini request contracts use the old `ProjectId` and `PlanInput` semantics.
8. Existing manifest reconciliations are based on the 37/12 Watershed model.

These contracts remain valid for the currently implemented v1 runtime but are
not the target cross-category runtime contract.

## Migration strategy

Do not mutate v1 semantics incrementally while the current runtime is still active.

Introduce cross-category v2 contracts in parallel.

Only switch runtime/API consumers after:

- v2 contract tests pass;
- reviewed cross-category runtime data validates;
- the M3.7D portfolio state machine is implemented;
- API integration tests pass; and
- frontend integration passes.

Until that gate:

`runtime_integration_authorized=false`

## API namespace

Keep:

`/api/v1`

The HTTP namespace does not need to change.

Semantic contract versions identify the incompatible payload changes.

## Release bundle topology

Keep the existing four-file logical release bundle:

```text
release-data/<data_version>/
├── catalog.json
├── map-context.geojson
├── benchmark.json
└── manifest.json

## Activation outcome — 2026-09-06

The migration gate defined above has now been satisfied.

M3.8 implementation completed the parallel v2 path and then activated it only
after the governed runtime catalog, portfolio evaluator, release bundle, and
FastAPI integration passed their verification gates.

Final activated runtime state:

- analytical projects: 106;
- governed request total: $1,973,520,000;
- runtime catalog contract: cross-category v2;
- governed project geometry coverage: 0/106;
- fabricated geometry: false;
- historical benchmark analytical projects: 20;
- historical matched-cohort recommendation: $332,000,000;
- `cross_category_ranking_authorized=true`;
- `portfolio_selection_authorized=true`;
- `runtime_integration_authorized=true`;
- activated release ID:
  `efb3783b2f4c7568012fb9ae590ff40dbf5a46d18a3ff1942a22d424a4b52207`.

The earlier statements in this document that runtime integration was
unauthorized describe the M3.8A entry condition and migration gate. They are not
rewritten. Earlier M3.7 governed artifacts likewise retain
`runtime_integration_authorized=false` as historical checkpoint provenance.

The standard FastAPI runtime now serves the cross-category v2 model through
`/api/v1/bootstrap`, `/api/v1/plans/evaluate`, and `/api/v1/benchmark`.
Historical benchmark data remains outcome-only and absent from the analytical
runtime catalog. `/api/v1/benchmark/compare` remains explicitly unavailable
rather than reusing the retired Watershed comparison semantics.
