# M3.7B — Watershed PRB Model Eligibility

**Historical decision snapshot:** January 21, 2026
**Status:** Implementation and verification complete; checkpoint approval pending
**Model scope:** `WATERSHED_PRB_PROJECT_MODEL`

## Decision

M3.7B evaluates the 37 governed Watershed `ANALYTICAL_PROJECT` records for participation in a PRB-based project model. A project is evidence-feasible when its canonical identity is reconciled to the January PRB row, all six official PRB components are present, and those components reproduce the governed PRB Grand Total. It is model-eligible when it is also an analytical project with a positive usable canonical November request.

RNA geometry, FEMA floodplain context, EAZ 2021 context, and Watershed Problem Score context remain useful contextual evidence but do not gate base PRB-model eligibility. Missing geometry or contextual flood/equity evidence therefore does not remove an otherwise valid project.

The January Initial Recommendation remains benchmark/outcome-only and is not an eligibility input. Twenty-five of the 37 eligible projects have no January recommendation amount.

Project `5754.149` remains eligible despite its request-version conflict. The canonical November request of `$2,500,000` remains the modeling cost authority while the January `$2,625,000` amount remains a preserved source-version conflict.

## Result

- analytical projects: **37**
- evidence-feasible: **37/37**
- PRB-model eligible: **37/37**
- PRB-model ineligible: **0**
- eligible with request-version conflict: **1**
- eligible without January recommendation: **25**

Required evidence reasons are `RECONCILED_CANONICAL_IDENTITY`, `COMPLETE_PRB_COMPONENT_VECTOR`, and `VALID_PRB_GRAND_TOTAL`. Required model reasons are `ANALYTICAL_PROJECT`, `EVIDENCE_FEASIBLE`, and `USABLE_CANONICAL_REQUEST`. No current project has a blocking reason.

## Artifact and boundary

The governed overlay is:

`data/governed/cross_category/model_eligibility/watershed-prb-model-eligibility.json`

Artifact version: `m3.7b-watershed-prb-model-eligibility/1.0.0`.

M3.7B does not rewrite the M3.6 structural universe. The overlay records `runtime_integration_authorized = false`, so the existing 12-project runtime family is unchanged.

M3.7B does not define Funding Priority, ranking, tie-breaking, portfolio optimization, cross-category eligibility, or runtime activation of the 37-project cohort. The `$125M` Watershed envelope remains a later historical validation scenario rather than the final cross-category optimization budget.

## Verification

- focused M3.7B: **17 passed**
- combined Watershed regression: **55 passed, 84 subtests passed**
- full repository: **233 passed, 137 subtests passed**
- `pip check`: no broken requirements
- governed artifact regeneration: `unchanged`
- `git diff --check`: passes

One known Starlette TestClient/AnyIO deprecation warning remains non-blocking.

## Next

M3.7C evaluates deterministic PRB Funding Priority and tie methodology. Cross-category model eligibility will be extended before final portfolio optimization methodology is locked.
