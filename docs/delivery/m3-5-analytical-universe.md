# M3.5 Cross-Category Analytical Universe

Status: APPROVED
Approval date: 2026-09-03
Historical decision snapshot: 2026-01-21

## Purpose

M3.5 establishes the governed cross-category analytical universe for the
Austin 2026 Bond Portfolio Simulator using the January 21, 2026 historical
decision snapshot.

The PRB source material contains both individual projects and broader
programmatic decision units. A PRB score alone does not establish
project-level analytical eligibility.

## Governed Universe

Total PRB source rows: 136

- ANALYTICAL_PROJECT: 106
- PROGRAM_BUCKET: 23
- PROGRAM_ALLOCATION: 4
- NOT_SCORED: 3

### Analytical projects by presentation group

- Transportation: 9
- Parks & Open Space: 22
- Watershed: 37
- Community Facilities: 38

Total: 106

## Classification Semantics

### ANALYTICAL_PROJECT

An individually identifiable project or facility that is structurally valid
as a project-level decision unit.

ANALYTICAL_PROJECT does not automatically mean that the project has sufficient
evidence to participate in the ClimateCapital model.

The following concepts remain separate:

- analytical unit status
- evidence feasibility status
- model eligibility

### PROGRAM_BUCKET

A broad scored programmatic decision unit that cannot be treated as an
individual project without January 21, 2026-or-earlier evidence resolving it
into individually identifiable and costed projects.

PROGRAM_BUCKET records remain governed historical records but are excluded
from project-level optimization.

### PROGRAM_ALLOCATION

A broad funding allocation without an individual project scope.

The four Parks program allocation rows are retained for historical provenance
and allocation hierarchy but excluded from project-level optimization.

### NOT_SCORED

A decision unit explicitly identified by the City as Not Scored.

NOT_SCORED means the PRB score is null/not applicable. It must never be
interpreted as a score of zero.

The three quarantined NOT_SCORED records are:

1. Neighborhood Partnering Program
2. Open Space Acquisition
3. Affordable Housing

These records remain available for historical benchmarking, provenance, and
methodology but cannot participate in scored project-level optimization.

## Transportation

Transportation contains:

- 18 official PRB decision units
- 17 scored units
- 9 ANALYTICAL_PROJECT units
- 8 PROGRAM_BUCKET units
- 1 NOT_SCORED unit

A PRB score alone does not establish project-level analytical eligibility.

## Parks & Open Space

Parks contains:

- 34 PRB source rows
- 22 ANALYTICAL_PROJECT units
- 8 PROGRAM_BUCKET units
- 4 PROGRAM_ALLOCATION units

Parent/program allocation rows and underlying project rows must not be summed
as independent project requests where doing so would double count a funding
hierarchy.

## Watershed

The existing governed Watershed project universe remains unchanged:

- 37 ANALYTICAL_PROJECT units
- canonical identity derived from the November 21, 2025 Watershed project
  universe and official subproject IDs

The following remain PROGRAM_BUCKET units:

- Small Scale Stormwater & Drainage Asset Management Opportunities
- Stormwater & Drainage Partnership Opportunities
- Stormwater Resilience Program
- Watershed Protection - Facility for Operations

Open Space Acquisition is NOT_SCORED and quarantined.

The authoritative modeled Watershed named-project budget remains the
$125 million project sub-envelope within the January 21, 2026 $160 million
Watershed recommendation.

The November 21 source-universe identity must not be overwritten by January
PRB presentation names or values.

Source-version differences must be retained explicitly, including the known
request discrepancy for subproject 5754.149:

- November 21 source request: $2,500,000
- January PRB request: $2,625,000

## Community Facilities

Community Facilities is a ClimateCapital presentation grouping.

It does not replace or overwrite authoritative source provenance.

Projects displayed under Community Facilities must retain their actual:

- source_department
- source_domain

The presentation group includes facility-type projects originating from
departments including Public Safety, Libraries, Cultural/ACME, Public Health,
Fleet Services, Animal Services, Homeless Strategy Office, Municipal Court,
and related facility-owning departments.

Libraries, Cultural/ACME, Public Health, and other underlying source domains
remain analytically distinguishable.

## Cost and Historical Recommendation Semantics

department_request and historical_recommendation_amount are different fields.

Historical recommendation amounts may represent partial funding or a project
stage and must not silently replace the analytical project request/cost.

Source-version conflicts or changes must be preserved explicitly rather than
resolved by silently overwriting earlier governed values.

## Historical Cutoff

The analytical universe is frozen to the January 21, 2026 historical decision
snapshot.

Later 2026 bond recommendations or decisions must not be used to construct the
historical analytical universe because doing so would introduce future
information into the simulation.

## Approval

M3.5 analytical-universe semantics were approved on 2026-09-03.

This document is the governance checkpoint for subsequent cross-category
dataset, schema, validation, and implementation work.