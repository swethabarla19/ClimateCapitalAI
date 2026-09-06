# M3.7D — Cross-Category Portfolio Methodology

**Checkpoint date:** 2026-09-06
**Historical decision snapshot:** January 21, 2026
**Status:** Methodology implementation and verification complete; portfolio-selection methodology authorized, runtime integration not yet authorized.

## Purpose

M3.7D governs how ClimateCapital may construct a Funding Plan from the 106
model-eligible cross-category analytical projects after M3.7F authorized official
PRB Grand Total as an ordinal Funding Priority measure.

The result is deliberately not a cardinal knapsack optimizer.

## M3.7D-A — Budget authority

The governed 106-project cohort contains:

- 106 analytical projects
- $1,973,520,000 in governed full-project requests

Historical references are kept separate:

- $332,000,000 — historical recommendation dollars attached to the same
  106-project analytical cohort; authorized as the matched-cohort benchmark scenario
- $700,000,000 — full January Initial Draft Recommendation; benchmark/outcome reference
- $750,000,000 — pre-snapshot citywide financial-capacity reference; not a
  106-project project-budget cap

Available Project Budget is an analyst-supplied scenario input.

Historical category allocations are not hard ClimateCapital model constraints.

## M3.7D-B0 — Portfolio-constraint feasibility

Machine-operational inputs are:

- model eligibility
- official ordinal PRB Funding Priority
- governed `model_request_dollars`
- analyst-supplied Available Project Budget

Structured January source coverage found:

- O&M Impact: 74 No, 32 Yes
- Council District: 85 single-district, 12 multi-district, 1 citywide,
  8 unspecified

Council District distribution is analyst review/reporting rather than a numeric
machine quota.

O&M is context/warning rather than a portfolio cap.

Six-year deliverability and preventative-maintenance considerations remain analyst
review because the 106-project cohort lacks a reproducible project-level capacity
or avoided-cost model.

Matching/outside funding and Strategic Alignment must not be added again as new
portfolio preferences because those concepts are already represented within the
official PRB framework.

Historical category allocations and historical recommendation membership remain
benchmark/outcome-only.

## M3.7D-B — Authorized methodology

Methodology:

`PRIORITY_CONSTRAINED_ANALYST_GOVERNED_PORTFOLIO_CONSTRUCTION`

Projects are indivisible full-request units.

Every Funding Plan must satisfy:

`sum(selected model_request_dollars) <= Available Project Budget`

Priority tiers are processed from highest official PRB Funding Priority to lowest.

Selection behavior:

1. If the complete next priority tier fits, include the complete tier.
2. If the complete tier does not fit, it becomes the boundary priority tier.
3. If no project in the boundary tier fits, no project from that tier can be
   automatically included under the current budget.
4. If exactly one tied project is budget-feasible, budget feasibility uniquely
   resolves that project and it may be auto-included.
5. If multiple equal-priority projects are feasible while the complete tier does
   not fit, analyst resolution is required.
6. If an unselected same-tier project can still fit after analyst resolution,
   ClimateCapital warns before descending to a lower-priority tier.
7. Advancing to a lower tier while a feasible higher-priority project remains
   requires explicit analyst override.

## Prohibited machine objectives

ClimateCapital does not automatically:

- maximize the sum of PRB Grand Totals
- maximize score per dollar
- choose the cheapest tied project
- maximize project count
- maximize budget utilization
- choose by an individual PRB component
- normalize categories
- reproduce historical recommendation membership
- use Council District, O&M, GIS/context evidence, name, ID, or source-row order
  as hidden analytical tiebreakers

PRB score remains ordinal rather than additive portfolio utility.

## Boundary-frontier evidence

At the historical matched-cohort $332M scenario:

- complete higher-priority tiers through score 73 cost $281.95M
- $50.05M remains
- the score-72 tier costs $91M
- one tied project costs $51M and cannot fit
- one tied project costs $40M and can fit
- budget feasibility therefore uniquely resolves the boundary

At $700M:

- the boundary score is 67
- five equal-priority projects individually fit
- the complete tier does not fit
- analyst resolution is therefore required

At $750M:

- the boundary score is 65
- eight equal-priority projects individually fit
- the complete tier does not fit
- analyst resolution is therefore required

These examples prove why deterministic display order, cheapest-first selection,
budget-utilization maximization, or other invented tiebreakers cannot substitute
for analyst judgment.

## Authority state

After M3.7D:

- `cross_category_ranking_authorized=true`
- `portfolio_selection_authorized=true`
- `runtime_integration_authorized=false`

The methodology is now authorized for implementation.

The existing FastAPI runtime has not yet been changed to execute the new
cross-category portfolio state machine.

## Governed artifacts

- `scripts/data/audit_cross_category_portfolio_budget_structure.py`
- `scripts/data/audit_cross_category_rank_cost_frontier.py`
- `scripts/data/audit_cross_category_official_portfolio_constraints.py`
- `scripts/data/build_cross_category_portfolio_methodology.py`
- `data/governed/cross_category/portfolio_methodology/cross-category-portfolio-methodology.json`
- `tests/application/test_cross_category_portfolio_methodology.py`

## Verification

Focused M3.7D:

- 29 passed

Combined M3.7A/B/C/E/F/D regression:

- 124 passed

Full repository:

- 331 passed
- 137 subtests passed
- 1 known non-blocking Starlette TestClient / AnyIO deprecation warning

Dependency verification:

- `pip check`: no broken requirements

Determinism:

- governed M3.7D methodology artifact regenerates as `unchanged`
- `git diff --check` passes
