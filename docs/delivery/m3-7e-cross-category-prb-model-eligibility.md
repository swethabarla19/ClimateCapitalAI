# M3.7E — Cross-Category PRB Evidence Feasibility and Model Eligibility

**Checkpoint date:** 2026-09-04
**Historical decision snapshot:** January 21, 2026
**Status:** Implementation and verification complete; checkpoint approval pending.

## Purpose

M3.7E determines whether the governed project-level analytical universe can
participate in a common PRB-based analytical model without inventing missing
evidence or using the January Initial Recommendation as an analytical input.

M3.7E does not authorize cross-category Funding Priority ranking, portfolio
selection, optimization, or runtime integration.

## Governed analytical universe

M3.6 contains 106 `ANALYTICAL_PROJECT` units:

- Transportation: 9
- Parks & Open Space: 22
- Watershed: 37
- Community Facilities: 38

Program buckets, program allocations, and explicitly `NOT_SCORED` records remain
outside project-level model eligibility.

## M3.7E-A — Cross-category PRB reconciliation

The January 21, 2026 Project Review Board scoring matrix contains the same six
official score components across the analytical categories:

1. Strategic Alignment
2. Critical Asset
3. Community Consideration
4. Efficiency
5. Timeliness & Readiness
6. Climate Resilience

The remaining 69 non-Watershed analytical projects were found on physical PDF
pages 5–7:

- Page 5: 19
- Page 6: 29
- Page 7: 21

All 69 governed January names reconcile exactly to one scoring row. Combined with
the previously governed 37-project Watershed reconciliation, M3.7E-A establishes:

- 106/106 reconciled analytical projects
- 106/106 complete six-component PRB vectors
- 106/106 component sums reproducing the official PRB Grand Total
- zero ambiguous or unmatched analytical projects
- three projects containing legitimate half-point score values

The half-point projects are:

- `community-facilities/ems/station-03` — Grand Total 54.5
- `community-facilities/ems/station-14` — Grand Total 53.5
- `community-facilities/fleet/consolidated-service-center` — Grand Total 50.5

No score rounding or normalization is introduced.

## Identity and request authority

Identity authority remains category-specific.

For Watershed, the November 21, 2025 canonical subproject identity remains
authoritative and the governed M3.7A reconciliation is reused.

For Transportation, Parks & Open Space, and Community Facilities,
`decision_unit_id` remains the stable governed project identity. No artificial
canonical project IDs are created.

Request authority also remains source-specific:

- Watershed model request: canonical November 21, 2025 request
- Non-Watershed model request: governed January request in the M3.6
  cross-category universe

The resulting governed model-request total is:

**$1,973,520,000**

The January request overlay totals:

**$1,973,645,000**

The $125,000 difference is entirely the previously governed Watershed
`5754.149` request-version conflict:

- canonical November request: $2,500,000
- January request overlay: $2,625,000

The two non-Watershed historical request conflicts also remain explicit:

- George Washington Carver Museum: governed January request $12,000,000
- Colony Park Branch Library: governed January request $58,000,000

Source-version conflicts are provenance, not automatic analytical exclusions.

## Historical recommendation isolation

Twenty of the 106 analytical projects have a January project-level recommendation.
The project-level recommendation total is $332,000,000:

- non-Watershed analytical projects: $207,000,000
- Watershed named projects: $125,000,000

This does not equal the complete historical Initial Recommendation because
program buckets, allocations, and other non-project decision units remain outside
the 106-project analytical cohort.

January Initial Recommendation remains benchmark/outcome-only and is not used to
establish evidence feasibility or model eligibility.

## M3.7E-B — Cross-category model eligibility

The scoped model is:

`CROSS_CATEGORY_PRB_PROJECT_MODEL`

A project is model eligible when all of the following are true:

- it is a governed `ANALYTICAL_PROJECT`;
- its governed identity reconciles to official PRB scoring evidence;
- all six official PRB components are present;
- the component sum reproduces the governed PRB Grand Total; and
- a positive governed model request is available.

Under this rule:

- 106/106 projects are evidence `FEASIBLE`
- 106/106 projects are model eligible
- 0 projects are model ineligible
- 3 eligible projects retain source-version conflicts
- 86 eligible projects have no January recommendation

The recommendation-independent result is direct evidence that historical outcome
membership is not being used as an eligibility criterion.

## Authority boundary

M3.7E establishes evidence feasibility and scoped model eligibility only.

The following remain explicitly unauthorized:

- `cross_category_ranking_authorized=false`
- `portfolio_selection_authorized=false`
- `runtime_integration_authorized=false`

In particular, M3.7E does not establish that the same raw PRB Grand Total has
sufficient analytical comparability across Transportation, Parks & Open Space,
Watershed, and Community Facilities to support one global Funding Priority rank.

That comparability question must be resolved before cross-category ranking or
portfolio optimization is authorized.

## Governed artifacts

- `data/reconnaissance/city_austin/initial_draft_recommendation/2026-01-21/non_watershed_prb_scores.csv`
- `data/governed/cross_category/reconciliation/cross-category-prb-reconciliation.json`
- `data/governed/cross_category/model_eligibility/cross-category-prb-model-eligibility.json`

## Reproducibility scripts

Discovery and evidence audits:

- `scripts/data/inspect_cross_category_prb_pages.py`
- `scripts/data/audit_cross_category_prb_name_coverage.py`
- `scripts/data/audit_cross_category_prb_component_parse.py`

Governed extraction/build:

- `scripts/data/extract_non_watershed_prb_scores.py`
- `scripts/data/build_cross_category_prb_reconciliation.py`
- `scripts/data/build_cross_category_prb_model_eligibility.py`

## Verification

M3.7E focused tests:

- 25 passed

Combined M3.7A/B/C/E regression:

- 69 passed

Full repository:

- 276 passed
- 137 subtests passed
- 1 known non-blocking Starlette TestClient / AnyIO deprecation warning

Dependency verification:

- `pip check`: no broken requirements

Determinism:

- non-Watershed PRB extraction: `unchanged`
- cross-category PRB reconciliation: `unchanged`
- cross-category model eligibility: `unchanged`

No runtime model integration, cross-category ranking, or portfolio selection is
authorized by this checkpoint.
