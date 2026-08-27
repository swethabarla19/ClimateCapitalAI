# ClimateCapital AI Screen Specification

> **Status:** Approved and locked through Stage 4
> **Locked:** 2026-08-26
> **Authority:** This is the authoritative Product and Design Lock for navigation,
> screens, contextual surfaces, interaction behavior, important UI states,
> recovery, and low-fidelity layout. It does not approve visual styling, technical
> architecture, datasets, analytical methodology, or implementation.

Every project name, count, dollar amount, date, rank, benchmark value, and outcome
inside the wireframes is an illustrative placeholder. Examples are not source
evidence, implementation constants, or analytical decisions.

## Experience Contract

- The experience is desktop-first and remains usable on a tablet.
- A narrow primary sidebar contains **Explore**, **Funding Plan**, **Data &
  Methodology**, and **Help & Resources**.
- **Compare** remains conditional SP0-1. It is reached from existing list or detail
  paths only if it survives the release gates and is not a required primary
  destination.
- The global header shows **Decision: [current decision context]**,
  **Scenario: [current confirmed scenario]**, and **Available Budget: [amount]**.
- The Historical Benchmark is never labeled as a scenario. The current confirmed
  scenario, immutable Historical Baseline reference, and Historical Benchmark
  remain distinct.
- Search, sorting, and filters on Explore affect only visible map/list results.
  They never change eligibility, scores, ranks, scenario inputs, optimization, or
  Funding Plan membership.
- Progressive disclosure hides controls and secondary detail until invoked.
  Project Detail is not permanently open, Scenario Settings opens only from
  **Adjust Scenario**, and the Layers popover is closed by default.
- A closed Layers popover does not mean every analytical layer is off. The
  evidence stage determines the defensible default map visualization.
- All required information and actions remain available without Gemini.
- Project inspection, scenario changes, and recovery must be keyboard-operable,
  visibly focused, programmatically labeled, and available through non-map paths.

## Primary Navigation and Journey

Begin in Explore; inspect a Recommended Projects row directly in the shared Project
Detail panel or use marker preview → Project Detail; close detail without losing
Explore state; use **View Funding Plan** to enter the dedicated Funding Plan
workspace; invoke Scenario Settings, Historical Benchmark, Reviewed Draft
confirmation, or compact Gemini from that workspace; and use anchored links to Data
& Methodology or the primary sidebar without changing the confirmed scenario.

Help & Resources remains independently available from the sidebar. The
three-minute demo follows this flow but does not remove direct access to any primary
destination.

## Required Screen Inventory

### Explore

**Purpose:** Spatially orient the analyst, reveal patterns, and provide a fast path
from candidate evidence to the current Funding Plan without turning Explore into a
full portfolio workspace.

**Required information:**

- Current decision context, current confirmed scenario, and Available Budget.
- Compact summary metrics only when their underlying measures are approved.
- Large immersive map with defensible candidate geography, supported analytical
  visualization, legend access, pan, zoom, and a click/tap Layers control.
- Search and presentation-only filters.
- Synchronized compact **Recommended Projects** list.
- Separate presentation-match and eligible-total counts, using wording such as
  **[matching count] matching · [eligible total] eligible total**.
- Slim current Funding Plan status, such as projects recommended and budget use,
  with **View Funding Plan**.
- A small proactive Gemini insight grounded in the current extent, active
  filters/layers, and visible projects.

**User actions:**

- Pan and zoom the map.
- Open the Layers popover and inspect the legend.
- Search, filter, or sort visible projects without changing analytical state.
- Select a map marker to open its lightweight preview.
- Select a Recommended Projects row to open Project Detail directly.
- Open the full Funding Plan.
- Expand or collapse the grounded Explore insight.

**Explicit exclusions:** The full Funding Plan, Reviewed Draft workflow, Scenario
Settings, Historical Benchmark, and permanently open Project Detail do not appear
on Explore.

### Funding Plan

**Purpose:** Give the deterministic portfolio recommendation, governed scenario
workflow, descriptive City benchmark, explanation, and Reviewed Draft state enough
space to remain legible.

**Required information:**

- Current confirmed scenario.
- Budget used, Available Budget, remainder, and recommended project count.
- Applied constraints and the later-approved optimization objective.
- Separate **Recommended** and **Not Included** groups containing every eligible
  project.
- Department Request, Funding Priority/rank, Funding Plan membership, and supported
  reasons or constraints.
- Supported deltas from the immutable Historical Baseline for a confirmed What-If.
- Clear distinction between individual Funding Priority and constrained plan
  membership.
- Current-session Reviewed Draft status and draft/non-official disclaimer.
- Compact, on-demand Gemini explanation.

**User actions:**

- Inspect Recommended and Not Included candidates.
- Open shared Project Detail.
- Invoke **Adjust Scenario**.
- Open the secondary Historical Benchmark.
- Request a bounded grounded explanation.
- Invoke **Mark as Reviewed Draft**.

**Constraints:** Membership is optimizer-controlled. P0 has no manual project
override.

### Data & Methodology

**Purpose:** Make the analytical chain, provenance, eligibility audit, and
limitations inspectable without creating a separate full audit workspace.

**Required anchored sections:**

1. Decision context and terminology.
2. Eligibility rules.
3. Eligible-candidate and excluded-source-record counts.
4. Excluded records and documented reasons, without assuming every record is a
   project.
5. Evidence sources and vintages.
6. Source versus derived fields.
7. Later-approved transformations, scoring, ranking, confidence, and optimization
   method.
8. Missing-data treatment and limitations.
9. Full-project inclusion/exclusion assumption.
10. Isolation of the Historical City Recommendation from ClimateCapital's
    analytical pipeline.

The page supports anchored links from Project Detail, Funding Plan, states, and
Help & Resources.

### Help & Resources

**Purpose:** Provide compact, non-AI-dependent orientation without duplicating the
full methodology.

**Required information:**

- Quick guide to the Historical Decision Snapshot, Historical City
  Recommendation, ClimateCapital Historical Baseline Scenario, and What-If
  Scenario.
- How to use Explore and Funding Plan.
- What Gemini can and cannot do.
- How to interpret confidence and missingness once the methodology is approved.
- Accessibility/help guidance.
- Historical-simulation, draft, and non-official disclaimers.
- Link to Data & Methodology for detailed provenance.

### Compare — Conditional SP0-1

**Purpose:** If retained, help the analyst inspect exactly two candidates side by
side without creating a new analytical path.

**Required behavior:**

- Select exactly two candidates from existing list or detail paths.
- Reuse existing governed Department Request, score/rank, evidence, confidence,
  portfolio status, missingness, provenance, and grounded explanations.
- Explain only supported ranking or portfolio-status differences.
- Do not introduce separate calculations, custom metrics, saved comparisons,
  exports, or comparison of three or more projects.

## Required Contextual Surfaces

### Layers popover

- Opens on click/tap, never hover-only.
- Lists only supported layers and mirrors the current map visualization state.
- Provides a legend or direct legend access.
- Closes without resetting layer or project selections.
- Is closed by default, while the separately approved default visualization may
  remain active.

### Map-marker preview

- Appears only after selecting a map marker.
- Shows project name, Department Request, concise supported status/evidence, and
  **View Project Details**.
- Does not duplicate the full detail panel.

### Shared Project Detail panel

- A Recommended Projects row opens Project Detail directly.
- A marker reaches it through the lightweight preview.
- Both paths use the same component and preserve Explore map extent, filters,
  layers, selected project, and list scroll.
- Required information includes source versus derived values, Department Request,
  Funding Priority/rank, Funding Plan status, and supported Importance, Climate
  Risk, Community Vulnerability, and Community Equity measures.
- It also shows methodology-driven confidence, sources/vintages, limitations,
  explicit missingness, and bounded Gemini actions.
- A measure appears only when its underlying metric is approved.

### Explore Gemini insight

- Is compact and proactively visible because spatial interpretation is central to
  Explore.
- Is grounded only in the current extent, active filters/layers, and visible
  governed projects.
- Expands in the same contextual region and never hides deterministic content.

### Scenario Settings

- Opens as a Funding Plan drawer through **Adjust Scenario**.
- Edits only Available Budget and later-approved weights.
- Shows current versus proposed values and validation.
- Requires explicit recalculation/confirmation before replacing the active
  What-If.
- Unapplied edits never change the header context or visible current result.

### Gemini scenario proposal

P0-9 is approved. Gemini may produce one atomic structured proposal affecting only
budget and approved weights. The proposal shows before/after values and
confirm/cancel actions. Confirmation uses the same validation and deterministic
recalculation path as manual controls. Gemini never edits facts, scores, ranks,
constraints, or portfolio membership directly.

### Historical Benchmark

- Is a secondary Funding Plan view of the published January 2026 Historical City
  Recommendation.
- Uses City-specific inclusion terms and preserves published amounts/treatment.
- Shows only evidence-supported overlap and divergence.
- Does not infer City reasoning or characterize either result as correct.
- Is never a scenario input, target, score, or ground truth.

### Reviewed Draft confirmation

- Appears in place over the Funding Plan.
- Identifies the exact current confirmed scenario, budget, weights, and supported
  outcomes.
- States that the designation is current-session, draft, non-persisted, and
  non-official.
- Offers cancel and confirm.
- Does not create a saved scenario, formal approval, export, or persistence
  workflow.

### Funding Plan Gemini

- Is compact by default and expands only when invoked.
- Explains governed project, rank, membership, constraint, or scenario results.
- Never blocks or replaces deterministic results.

## Evidence and Terminology Gates

- People Potentially Benefiting and Implementation Readiness are not guaranteed
  fields. Omit either if its metric is unsupported.
- If an approved metric is missing for one project, show explicit project-level
  missingness and never treat or describe it as zero.
- Community Equity and Community Vulnerability remain distinct when they represent
  different underlying measures.
- Low-confidence warnings appear only when required by the later-approved
  confidence methodology and threshold. The UI does not make an independent
  confidence judgment.
- Use public-facing terms where supported: Funding Priority, Available Budget,
  Funding Plan, Importance, Recommended Projects, Climate Risk, Community
  Vulnerability, Community Equity, and People Potentially Benefiting.
- Explore filters affect presentation only. Funding Plan membership changes only
  after a confirmed valid scenario recalculation.

## Important UI State and Recovery Model

Never collapse the following into a generic “no results” state.

| Context | Required states and recovery |
| --- | --- |
| **Explore counts and filters** | Keep the eligible cohort separate from presentation matches. With active filters, show **[matching count] matching · [eligible total] eligible total**. Zero matches keeps filters, eligible total, and map/list frame visible and offers **Clear filters**. |
| **No eligible projects** | State that documented eligibility produced no candidates, suppress ranking and Funding Plan claims, and link to the eligibility audit. It is not a filter result or system failure. |
| **Missing project geometry** | Keep the eligible project in list, ranking, detail, and Funding Plan; label **Map location unavailable** and provide non-map access. Never invent a marker. |
| **Approved-field missingness** | Show explicit project-level missingness and the methodology-defined effect. Missing is never zero. Unsupported metrics are omitted instead. |
| **Eligible but not in plan** | Show **Eligible · Not Included in Funding Plan** separately from rank and explain only the supported deterministic reason. Do not imply ineligibility, low Importance, or a City decision. |
| **Valid zero-project plan** | Present a successful deterministic result with its applicable constraint explanation. Distinguish it from infeasibility and system failure. |
| **No feasible optimized Funding Plan** | Show analytical infeasibility and a path to Scenario Settings. Preserve the last successful result and mark attempted inputs not applied. If no prior result exists, show a dedicated unavailable plan state without fabricating membership. |
| **Genuine system error** | Name the affected surface, preserve unaffected deterministic content, provide retry guidance, and do not imply an analytical result. Contain errors locally where possible. |
| **Project Detail** | Support closed, loading, loaded, approved-field-missing, geometry-missing, locally unavailable, and retry states. Closing/retrying never resets Explore state. Only marker selection uses preview first. |
| **Funding Plan** | Support initial loading, successful baseline/default result, successful confirmed What-If, valid zero-project result, analytical infeasibility, local/system error, and Reviewed Draft indicators. |
| **Scenario Settings** | Support pristine, dirty/unapplied, invalid, ready, recalculating, replacement confirmation, success, infeasible, and failure. Dirty inputs never change the current result. Failed/infeasible inputs remain editable but not applied. |
| **Historical Benchmark** | Support closed, loading, available, partially supported/missing published fields, unavailable, and retry. Missing benchmark data never changes ClimateCapital results. |
| **Reviewed Draft** | Support not reviewed, confirmation open, marked, and cleared. The designation binds to the exact confirmed result. Unapplied edits and failed recalculation do not clear it. Confirming a replacement of an accepted What-If warns and clears that designation. |
| **Gemini explanation** | Support compact/idle, expanded, loading, grounded answer, bounded refusal, unavailable, and retry. No required action depends on Gemini. |
| **Gemini proposal** | Support proposal-ready, validation error, confirmation pending, cancelled, deterministic recalculation, applied, infeasible, and failed. Nothing changes before confirmation. |
| **Data & Methodology** | Support complete page, anchored focus, local section loading, approved-field/source missingness, local section failure, and retry. The rest of the page and originating screen remain intact. |
| **Help & Resources** | Remain readable without Gemini. If a deep link fails, keep the guide usable and offer retry or the Data & Methodology landing page. |

## Low-Fidelity Wireframes

These diagrams establish hierarchy and behavior only.

### Explore

~~~text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ ClimateCapital│ Decision: [decision context]                                 │
│              │ Scenario: [current confirmed scenario]                        │
│ Explore      │ Available Budget: [amount]                                    │
│ Funding Plan ├───────────────────────────────────────────────────────────────┤
│ Data & Method│ [approved summary] [approved summary] [plan status]            │
│ Help         │ [Search] [Presentation filters] [Layers]                       │
│              ├───────────────────────────────┬───────────────────────────────┤
│              │                               │ Recommended Projects          │
│              │        IMMERSIVE MAP          │ [count] matching · [count]    │
│              │        + legend               │ eligible total                │
│              │                               │ [project row]                 │
│              │                               │ [project row]                 │
│              ├───────────────────────────────┴───────────────────────────────┤
│              │ Funding Plan: [count] recommended · [budget use] [View Plan]  │
│              │ Gemini insight: [grounded observation] [Expand]               │
└──────────────┴───────────────────────────────────────────────────────────────┘
~~~

### Layers popover

~~~text
[Layers ▾]
┌──────────────────────────────┐
│ Map layers                   │
│ [current supported layer]    │
│ [current supported layer]    │
│ [Legend / layer explanation] │
└──────────────────────────────┘
~~~

The control is closed by default. Active states mirror the separately approved
default visualization; Stage 4 does not force every overlay off.

### Marker preview and Project Detail

~~~text
Marker click → ┌──────────────────────────┐
               │ [Project name]           │
               │ Request: [amount]        │
               │ [supported brief status] │
               │ [View Project Details]   │
               └──────────────────────────┘

Row click ───────────────────────────────┐
Marker preview → View Project Details ───┤
                                        ▼
                         ┌─────────────────────────────────┐
                         │ Project Detail              [×] │
                         │ [source and derived values]     │
                         │ Funding Priority: [rank/score]  │
                         │ Funding Plan: [status]          │
                         │ [supported evidence/confidence] │
                         │ [missingness and limitations]   │
                         │ [sources and vintages]          │
                         │ [bounded Gemini action]         │
                         └─────────────────────────────────┘
~~~

### Explore Gemini insight

~~~text
Compact:  ┌───────────────────────────────────────────────┐
          │ What stands out here: [grounded insight]       │
          │ [Expand]                                       │
          └───────────────────────────────────────────────┘

Expanded: ┌───────────────────────────────────────────────┐
          │ Based on [extent / filters / layers / projects]│
          │ [grounded explanation + limitations]           │
          │ [Collapse]                                     │
          └───────────────────────────────────────────────┘
~~~

### Funding Plan and Scenario Settings

~~~text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Navigation   │ Funding Plan · [current confirmed scenario]                  │
│              │ [budget used] [Available Budget] [remainder] [project count] │
│              │ [Adjust Scenario] [Historical Benchmark] [Mark Reviewed Draft]│
│              ├──────────────────────────────┬────────────────────────────────┤
│              │ Recommended                 │ Not Included                   │
│              │ [project / request / rank]  │ [project / request / rank]     │
│              │ [project / request / rank]  │ [supported reason/status]      │
│              ├──────────────────────────────┴────────────────────────────────┤
│              │ [constraints/objective] [baseline-supported deltas]          │
│              │ Gemini explanation [Ask / Expand]                            │
└──────────────┴───────────────────────────────────────────────────────────────┘

Adjust Scenario → ┌─────────────────────────────────────────┐
                  │ Scenario Settings                   [×] │
                  │ Available Budget [current → proposed]   │
                  │ Approved weights [current → proposed]   │
                  │ [validation / unapplied status]         │
                  │ [Cancel] [Recalculate and Confirm]      │
                  └─────────────────────────────────────────┘
~~~

### Reviewed Draft confirmation

~~~text
┌─────────────────────────────────────────────────────┐
│ Mark this result as the Reviewed Draft?             │
│ Scenario: [current confirmed scenario]              │
│ Budget / weights / outcomes: [governed summary]     │
│ Current-session only · Draft · Not an official plan │
│                              [Cancel] [Mark Draft]   │
└─────────────────────────────────────────────────────┘
~~~

### Historical Benchmark

~~~text
┌───────────────────────────────────────────────────────────────┐
│ Historical City Recommendation · [published benchmark date]   │
│ Descriptive benchmark only · Not a ClimateCapital scenario    │
│ [City allocation] [City-included count] [supported overlap]    │
│ City-included            │ Not City-included                   │
│ [published treatment]    │ [published treatment]               │
│ [supported divergence; no inferred City reasoning]             │
└───────────────────────────────────────────────────────────────┘
~~~

### Data & Methodology

~~~text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Page anchors │ Data & Methodology                                            │
│ Context      │ [decision/scenario/benchmark terminology]                     │
│ Eligibility  │ [rules] [eligible count] [excluded-record count + reasons]    │
│ Evidence     │ [sources/vintages] [source vs derived] [missingness]           │
│ Scoring      │ [approved transformations/weights/ranking/confidence]          │
│ Portfolio    │ [constraint/objective/full-project assumption]                │
│ Limitations  │ [limits and City benchmark isolation]                         │
└──────────────┴───────────────────────────────────────────────────────────────┘
~~~

### Help & Resources

~~~text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ Navigation   │ Help & Resources                                              │
│              │ [Decision-context and scenario quick guide]                   │
│              │ [How to Explore] [How to review a Funding Plan]               │
│              │ [What Gemini can/cannot do] [Confidence/missingness guide]     │
│              │ [Accessibility/help] [Historical simulation disclaimer]       │
│              │ [Open Data & Methodology]                                     │
└──────────────┴───────────────────────────────────────────────────────────────┘
~~~

### Compare — Conditional SP0-1

~~~text
┌───────────────────────────────────────────────────────────────┐
│ Compare exactly two projects                                  │
│ [Project A]                       │ [Project B]                │
│ [existing governed fields]        │ [existing governed fields]│
│ [evidence/confidence/missingness]  │ [evidence/confidence]     │
│ [bounded supported explanation]                                │
└───────────────────────────────────────────────────────────────┘
~~~

## Demo-Relevant UI Sequence

The core UI sequence must fit three minutes:

1. Orient with the historical decision context, current confirmed scenario,
   Available Budget, and simulation disclaimer.
2. Use the map and synchronized list to reveal one supported flood/equity pattern
   and the grounded Explore insight.
3. Inspect one Project Detail and show evidence, Funding Priority,
   confidence/missingness, and Funding Plan status.
4. Open Funding Plan and show the full-project recommendation, budget constraint,
   and distinction between rank and membership.
5. Change only budget or approved weights, confirm deterministic recalculation, and
   show supported Historical Baseline deltas.
6. Invoke one grounded explanation and mark the exact result as the current-session
   Reviewed Draft.

A five-minute expansion may add Historical Benchmark, deeper methodology,
recovery, a second project, or Compare if SP0-1 survives.

## Unresolved Evidence Dependencies

This specification deliberately does not decide:

- Final eligible project count or defensible project geometries.
- Scoring dimensions, transformations, breakdown, or normalization.
- Default or editable weight values.
- Confidence methodology or warning threshold.
- Optimization objective and supported portfolio-comparison metrics.
- Missing-evidence effect on eligibility, scores, ranks, and optimization.
- Evidence vintages or default analytical map visualization.
- Support for People Potentially Benefiting or Implementation Readiness.
- Threshold for a project-specific heat co-benefit.

## Related Sources of Truth

- [Product plan](product-plan.md)
- [User stories and acceptance intent](user-stories.md)
- [Delivery and release gates](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
