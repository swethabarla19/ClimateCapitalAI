# M3.6 Governed Cross-Category Dataset and Schema

Status: COMPLETE
Completion date: 2026-09-04
Historical decision snapshot: 2026-01-21
Governance prerequisite: M3.5 APPROVED

## Purpose

M3.6 implements the governed cross-category analytical universe established
by M3.5.

This work converts the approved January 21, 2026 historical PRB universe from
a governance decision into a strict, machine-validatable dataset and contract.

M3.6 does not replace or expand the existing 37-project Watershed runtime
catalog used by the M2/M3 plan engine.

The cross-category universe is a separate governed source artifact from which
future analytical and model-eligible subsets may be derived.

## Governed Artifact

Primary artifact:

`data/governed/cross_category/cross-category-universe.json`

Contract:

`backend/climatecapital/contracts/cross_category.py`

Generated JSON Schema:

`contracts/schemas/cross-category-universe-1.0.0.schema.json`

Contract version:

`p0-cross-category-universe/1.0.0`

## Exact Universe Reconciliation

The completed artifact contains exactly 136 PRB source decision units:

- 106 `ANALYTICAL_PROJECT`
- 23 `PROGRAM_BUCKET`
- 4 `PROGRAM_ALLOCATION`
- 3 `NOT_SCORED`

Analytical projects by ClimateCapital presentation group:

- Transportation: 9
- Parks & Open Space: 22
- Watershed: 37
- Community Facilities: 38

Total analytical projects: 106

Source rows by presentation group:

- Transportation: 18
- Parks & Open Space: 34
- Watershed: 42
- Community Facilities: 41
- Affordable Housing: 1

Total source rows: 136

## Quarantined NOT_SCORED Records

The exact three `NOT_SCORED` records are:

1. Neighborhood Partnering Program
2. Open Space Acquisition
3. Affordable Housing

`NOT_SCORED` uses a null PRB score and must never be interpreted as score zero.

These records are preserved for historical provenance and benchmark
reconciliation only and cannot participate in project-level optimization.

## Analytical Eligibility Semantics

The implementation keeps the following concepts separate:

- structural analytical-project status
- evidence feasibility
- model eligibility

An `ANALYTICAL_PROJECT` is an individually identifiable project-level
decision unit.

It is not automatically eligible for the ClimateCapital model.

M3.6 therefore initializes cross-category analytical projects with:

- `evidence_feasibility_status = NOT_EVALUATED`
- `model_eligible = false`

Future evidence-feasibility work must explicitly promote or exclude projects.

Program buckets, program allocations, and NOT_SCORED records cannot be model
eligible.

## Presentation and Source Provenance

`presentation_category` is separate from authoritative source provenance.

Facility-type projects may be displayed under:

`Community Facilities`

while preserving their actual:

- `source_department`
- `source_domain`

Community Facilities therefore retains analytically distinct source domains
including:

- Cultural / ACME
- Libraries
- Public Health
- Emergency Medical Services
- Fire
- Fleet Services
- Homeless Strategy
- Police
- Animal Services
- Municipal Court

## Cost and Recommendation Semantics

The implementation preserves:

- `department_request_dollars`
- `historical_recommendation_amount_dollars`

as separate fields.

Historical recommendations may represent partial funding and never silently
replace project request values.

## Watershed Canonical Authority

The existing November 21, 2025 Watershed source universe remains canonical
for the 37 Watershed analytical projects.

The cross-category artifact preserves:

- exact canonical 37-project IDs
- canonical project request total: $327,970,000
- January PRB project request overlay: $328,095,000
- January historical named-project recommendation: $125,000,000

The known request conflict for subproject `5754.149` is preserved explicitly:

- November 21 source: $2,500,000
- January 21 PRB source: $2,625,000

No January value overwrites the November canonical record.

## Historical Source-Version Preservation

The July 31, 2025 Initial Project Request List was registered as governed
historical source-version evidence.

The implementation preserves verified July-to-January differences including:

- George Washington Carver Museum request: $6M to $12M
- Colony Park Branch Library request: $58.8M to $58M
- Safe & Ready Libraries Project renamed Safe & Secure Libraries Project

Source-version differences are retained rather than silently resolved.

## Architecture Boundary

The existing:

`release-data/fixture/catalog.json`

remains the governed 37-project Watershed runtime catalog used by the current
M2/M3 application and deterministic plan engine.

M3.6 does not expand that runtime catalog to 136 rows.

The intended architecture is:

M3.5 governed source universe
→ M3.6 136-row cross-category artifact
→ 106 structural analytical projects
→ future evidence-feasibility filtering
→ future model-eligible/runtime subset

This prevents source-universe membership from being confused with model
eligibility.

## Source-Row Slices

The assembled artifact is built from governed category slices:

- `source_rows/transportation.json`
- `source_rows/parks.json`
- `source_rows/watershed.json`
- `source_rows/community_facilities.json`
- `source_rows/affordable_housing.json`

Builder scripts preserve deterministic assembly and source-version semantics.

## Verification

Focused M3.6 cross-category tests:

- 38 passed

Application suite:

- 109 passed
- 23 subtests passed
- 1 third-party deprecation warning

Full repository suite:

- 197 passed
- 58 subtests passed
- 1 third-party deprecation warning

Schema generation:

- 23 schemas generated successfully

The generated cross-category schema is exercised through the strict Pydantic
contract and persistent artifact tests.

A separate `jsonschema` package validation command was not used because
`jsonschema` is not a declared project dependency. No new dependency was
introduced solely for a redundant one-off validation step.

`git diff --check` passed.

## Durable Implementation Rule

M3.6 completion is recorded in repository artifacts, contracts, tests,
documentation, and local Git commits.

Chat discussion or memory is not the durable authority for this implementation.

## Result

M3.6 is complete.

The repository now contains a governed, reproducible, strict-schema
cross-category historical universe suitable for the next analytical
feasibility and model-subset implementation work.