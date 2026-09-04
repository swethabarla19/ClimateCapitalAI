# M3.7A — Watershed PRB Score Reconciliation

**Historical decision snapshot:** January 21, 2026
**Status:** Implementation and verification complete; pending checkpoint approval/commit.

## Objective

M3.7A tests whether the governed 37-project Watershed universe can be
defensibly reconciled to the January 21, 2026 Project Review Board scoring
matrix without changing canonical November 21, 2025 project identity.

This checkpoint does not determine model eligibility, create Funding Priority,
rank projects, or implement portfolio optimization.

## Canonical Authority

The November 21, 2025 Watershed project source remains canonical for:

- project identity
- canonical subproject ID
- canonical project name
- canonical request amount

The January 21, 2026 PRB source is preserved as an overlay for:

- January source name
- six official PRB component scores
- PRB Grand Total
- January department request
- January Initial Recommendation

January values do not overwrite canonical November identity or request values.

## PRB Components

The January PRB table provides six quantitative project-evaluation components:

1. Strategic Alignment
2. Critical Asset
3. Community Consideration
4. Efficiency
5. Timeliness and Readiness
6. Climate Resilience

The six components sum exactly to the official PRB Grand Total for all 37
Watershed analytical projects.

## Source Extraction

The registered January source:

`austin_2026_bond_initial_draft_2026_01_21`

was retrieved from the already preserved GCS snapshot.

Verified SHA-256:

`da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359`

The Watershed PRB project rows occur on physical PDF pages 8–10.

A deterministic fail-closed extractor produces:

`data/reconnaissance/city_austin/initial_draft_recommendation/2026-01-21/watershed_prb_scores.csv`

The extraction is idempotent and refuses to overwrite a differing derived
artifact.

## Reconciliation Result

All 37 governed Watershed analytical projects reconcile defensibly.

- canonical Watershed projects: 37
- reconciled projects: 37/37
- complete six-component PRB vectors: 37/37
- valid PRB Grand Totals: 37/37
- ambiguous matches: 0
- unmatched projects: 0
- exact November/January name matches: 7
- governed source-version name matches: 30
- request-version conflicts: 1

The 30 name differences are governed source-version naming differences, not
ambiguous project identities.

## Preserved Request Conflict

Subproject `5754.149` remains the only governed request-version conflict:

- November 21 request: $2,500,000
- January 21 request: $2,625,000

The project identity remains reconciled; the amount conflict is retained
separately and is not treated as an identity ambiguity.

## Financial Reconciliation

- canonical November project requests: $327,970,000
- January PRB project requests: $328,095,000
- January named-project Initial Recommendation: $125,000,000

Request values and recommendation values remain separate.

## Authority Boundary

The January 21 PDF currently remains registered as a benchmark source because
it contains the historical Initial Recommendation outcome.

M3.7A does not promote the entire source to analytical authority.

Instead, M3.7 establishes the required semantic separation:

- PRB component scores and Grand Total are source-governed historical
  decision evidence and may be evaluated for analytical use in M3.7B/C.
- Initial Recommendation remains benchmark/outcome evidence and must never
  become an optimization input.

This prevents recommendation leakage into ClimateCapital ranking or portfolio
selection.

## Watershed Contextual Evidence

Existing Watershed evidence remains valid and unchanged:

- RNA geometry
- FEMA floodplain context
- Equity Analysis Zones
- Watershed Problem Score documentary associations
- purpose/family classifications
- evidence confidence and provenance

M3.7A does not convert those contextual datasets into invented quantitative
ranking inputs.

## Files

Added:

- `scripts/data/extract_watershed_prb_scores.py`
- `scripts/data/build_watershed_prb_reconciliation.py`
- `data/reconnaissance/city_austin/initial_draft_recommendation/2026-01-21/watershed_prb_scores.csv`
- `data/governed/cross_category/reconciliation/watershed-prb-reconciliation.json`
- `tests/test_watershed_prb_score_extraction.py`
- `tests/application/test_watershed_prb_reconciliation.py`

## Verification

M3.7A focused extraction tests:

- 10 passed
- 79 subtests passed

Combined Watershed regression checkpoint:

- 38 passed
- 84 subtests passed

Full repository:

- 216 passed
- 137 subtests passed
- one existing Starlette/AnyIO deprecation warning only

Dependency integrity:

- `python -m pip check`
- No broken requirements found.

## M3.7A Conclusion

The hypothesis is confirmed:

> The governed 37-project Watershed universe has complete and reproducible
> official PRB project-level scoring evidence for all 37 projects.

M3.7A therefore removes PRB score completeness and project reconciliation as
blockers to the next model-eligibility review.

It does not itself authorize ranking or optimization.

## Next

M3.7B must determine whether the complete official PRB evidence is sufficient
to promote the 37 Watershed analytical projects from:

- `evidence_feasibility_status = NOT_EVALUATED`
- `model_eligible = false`

into a governed PRB-based model-eligible cohort.

M3.7C may then separately evaluate PRB Grand Total as deterministic Funding
Priority.

M3.7D must separately govern the $125M portfolio objective before any optimizer
is implemented.
