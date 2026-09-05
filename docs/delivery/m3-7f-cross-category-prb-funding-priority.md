# M3.7F — Cross-Category PRB Funding Priority

**Checkpoint date:** 2026-09-04
**Historical decision snapshot:** January 21, 2026
**Status:** Implementation and verification complete; authorized for checkpoint publication.

## Decision

Official PRB Grand Total is authorized as the common cross-category
`Funding Priority Score` for the 106 governed analytical projects.

The score is interpreted only as an **ordinal PRB-based priority measure**.

It is not authorized as:

- cardinal public benefit;
- cost effectiveness;
- benefit/cost ratio;
- historical recommendation probability; or
- additive portfolio utility.

## Comparability evidence

The governed analytical cohort contains:

- Transportation: 9
- Parks & Open Space: 22
- Watershed: 37
- Community Facilities: 38
- Total: 106

M3.7E established:

- 106/106 reconciled governed identities;
- 106/106 complete six-component PRB vectors;
- 106/106 valid PRB Grand Totals; and
- 106/106 model-eligible projects.

M3.7F additionally audited the official PRB baseline criteria.

Results:

- 106 analytical projects
- 106 satisfy at least one baseline criterion
- 0 baseline failures
- 30 have Local/State/Federal Requirement = Yes
- 105 have City Owned = Yes

Baseline combinations:

- Requirement No / City Owned Yes: 76
- Requirement Yes / City Owned No: 1
- Requirement Yes / City Owned Yes: 29

## Funding Priority methodology

`Funding Priority Score = official PRB Grand Total`

Rules:

- higher score means higher Funding Priority;
- descending competition rank is used;
- equal scores share the same substantive rank;
- `decision_unit_id` ascending is deterministic display order only;
- display ordering inside ties has no analytical meaning;
- half-point scores are preserved exactly.

No category normalization, z-score normalization, percentile normalization,
score-per-dollar transformation, or ClimateCapital-created weighting is allowed.

## Ranking result

Across the 106 projects:

- score range: 40–83
- unique Funding Priority scores: 35
- tied score groups: 24
- projects participating in tied score groups: 95
- half-point Funding Priority scores: 3

The three half-point values remain:

- EMS Station 03: 54.5
- EMS Station 14: 53.5
- Fleet Consolidated Service Center: 50.5

## Authority boundary

M3.7F changes analytical ranking authority only:

- `cross_category_ranking_authorized=true`
- `portfolio_selection_authorized=false`
- `runtime_integration_authorized=false`

The ranking does not itself determine which projects enter a Funding Plan.

In particular, M3.7F does not authorize maximizing the sum of PRB Grand Totals,
taking projects strictly top-to-bottom until budget is exhausted, or treating PRB
points as additive public-value units.

Portfolio-selection methodology is the next analytical gate.

## Governed artifacts

- `scripts/data/audit_cross_category_prb_baseline_criteria.py`
- `scripts/data/build_cross_category_prb_funding_priority.py`
- `data/governed/cross_category/funding_priority/cross-category-prb-funding-priority.json`
- `tests/application/test_cross_category_prb_funding_priority.py`

## Verification

Focused M3.7F:

- 26 passed

Combined M3.7A/B/C/E/F:

- 95 passed

Full repository:

- 302 passed
- 137 subtests passed
- 1 known non-blocking Starlette TestClient / AnyIO deprecation warning

Dependency verification:

- `pip check`: no broken requirements

Determinism:

- governed cross-category Funding Priority artifact regenerates as `unchanged`
