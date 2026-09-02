# ClimateCapital AI Screen Specification

> **Status:** Approved Product and Design Lock, reconciled with Methodology Lock
> **Locked:** 2026-08-26; evidence-driven reconciliation 2026-09-01
> **Authority:** This is the authoritative Product and Design Lock for navigation,
> screens, contextual surfaces, interaction behavior, important UI states,
> recovery, and low-fidelity layout. It does not approve visual styling, technical
> architecture, datasets, analytical methodology, or implementation.

Every project name, count, dollar amount, date, benchmark value, and outcome
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
  **Plan: [Current Confirmed Plan]**, and **Available Budget: [amount]**.
- The Historical Benchmark is never labeled as a plan or scenario. The Current
  Confirmed Plan, immutable Session Reference Plan, and Historical Benchmark
  remain distinct.
- Search, sorting, and filters on Explore affect only visible map/list results.
  They never change the P0 analytical family, scenario inputs, confirmed
  membership, or budget arithmetic.
- Progressive disclosure hides controls and secondary detail until invoked.
  Project Detail is not permanently open, Scenario Settings opens only from
  **Adjust Scenario**, and the Layers popover is closed by default.
- A closed Layers popover does not mean every contextual layer is off. The default
  map visualization must preserve the locked evidence roles.
- All required information and actions remain available without Gemini.
- Project inspection, scenario changes, and recovery must be keyboard-operable,
  visibly focused, programmatically labeled, and available through non-map paths.

## Primary Navigation and Journey

Begin in Explore; inspect a Projects row directly in the shared Project
Detail panel or use marker preview → Project Detail; close detail without losing
Explore state; use **View Funding Plan** to enter the dedicated Funding Plan
workspace; invoke Scenario Settings, Historical Benchmark, Reviewed Draft
confirmation, or compact Gemini from that workspace; and use anchored links to Data
& Methodology or the primary sidebar without changing the Current Confirmed Plan.

Help & Resources remains independently available from the sidebar. The
three-minute demo follows this flow but does not remove direct access to any primary
destination.

## Required Screen Inventory

### Explore

**Purpose:** Spatially orient the analyst, reveal patterns, and provide a fast path
from candidate evidence to the current Funding Plan without turning Explore into a
full portfolio workspace.

**Required information:**

- Current decision context, Current Confirmed Plan, and Available Budget.
- Compact summary metrics only when their underlying measures are approved.
- Large immersive map with defensible candidate geography, supported analytical
  visualization, legend access, pan, zoom, and a click/tap Layers control.
- Search and presentation-only filters.
- Synchronized compact **Projects** list for the provisional 12-record P0
  analytical family.
- Separate presentation-match and family-total counts, using wording such as
  **[matching count] matching · [family total] P0 family**.
- Slim current Funding Plan status, such as projects included and budget use,
  with **View Funding Plan**.
- A small proactive Gemini insight grounded in the current extent, active
  filters/layers, and visible projects.

**User actions:**

- Pan and zoom the map.
- Open the Layers popover and inspect the legend.
- Search, filter, or sort visible projects without changing analytical state.
- Select a map marker to open its lightweight preview.
- Select a Projects row to open Project Detail directly.
- Open the full Funding Plan.
- Expand or collapse the grounded Explore insight.

**Explicit exclusions:** The full Funding Plan, Reviewed Draft workflow, Scenario
Settings, Historical Benchmark, and permanently open Project Detail do not appear
on Explore.

### Funding Plan

**Purpose:** Give analyst-controlled full-request membership, deterministic budget
arithmetic, the governed scenario workflow, descriptive City benchmark,
explanation, and Reviewed Draft state enough space to remain legible.

**Required information:**

- Current Confirmed Plan.
- Included total, Available Budget, remainder, and included project count.
- Applied full-request and budget constraints; no optimization objective.
- Separate **Included in Plan** and **Available Projects** groups containing every
  record in the active 12-record P0 analytical family.
- Department Request, purpose, evidence-state summary, scenario membership, and
  supported limitations.
- Supported deltas from the immutable Session Reference Plan for a confirmed
  What-If.
- Clear statement that membership is analyst-controlled and is not a system rank,
  recommendation, eligibility decision, or City result.
- Current-session Reviewed Draft status and draft/non-official disclaimer.
- Compact, on-demand Gemini explanation.

**User actions:**

- Add or remove complete governed requests and inspect Included in Plan and
  Available Projects.
- Open shared Project Detail.
- Invoke **Adjust Scenario**.
- Open the secondary Historical Benchmark.
- Request a bounded grounded explanation.
- Invoke **Mark as Reviewed Draft**.

**Constraints:** Membership is analyst-controlled only within the active 12-record
analytical family unless a later governed methodology decision changes that
contract. Confirmation is deterministic and unavailable while the included total
exceeds Available Budget. Unknown IDs, IDs outside the active family, duplicates,
and edited governed request amounts are rejected. Partial funding is unsupported.

### Data & Methodology

**Purpose:** Make the analytical chain, provenance, all-37 purpose/family audit,
and limitations inspectable without creating a separate full audit workspace.

**Required anchored sections:**

1. Decision context and terminology.
2. Governed universe and derived purpose-family method.
3. All-37, broad-flood-family, and 12-record P0-family counts and funding totals.
4. All 37 purpose classifications, confidence, ambiguity, and family treatment.
5. Evidence sources and vintages.
6. Source versus derived fields.
7. Evidence-state contract, classification/association confidence, analyst
   membership, budget validation/arithmetic, and unsupported metrics.
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
  Recommendation, Historical Envelope, Session Reference Plan, Current Confirmed
  Plan, and What-If Scenario.
- How to use Explore and Funding Plan.
- What Gemini can and cannot do.
- How to interpret confidence and missingness under the locked methodology.
- Accessibility/help guidance.
- Historical-simulation, draft, and non-official disclaimers.
- Link to Data & Methodology for detailed provenance.

### Compare — Conditional SP0-1

**Purpose:** If retained, help the analyst inspect exactly two candidates side by
side without creating a new analytical path.

**Required behavior:**

- Select exactly two candidates from existing list or detail paths.
- Reuse existing governed Department Request, purpose, evidence roles, confidence,
  scenario status, missingness, provenance, and grounded explanations.
- Explain only supported evidence or scenario-status differences.
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

- A Projects row opens Project Detail directly.
- A marker reaches it through the lightweight preview.
- Both paths use the same component and preserve Explore map extent, filters,
  layers, selected project, and list scroll.
- Required information includes source versus derived facts, Department Request,
  derived purpose and confidence, current scenario status, and available Problem
  Score association, geometry, FEMA, and EAZ context.
- Every item is labeled FACT, CONTEXTUAL EVIDENCE, RESEARCH-ONLY EVIDENCE, or
  UNAVAILABLE / UNSUPPORTED and includes sources/vintages, limitations, explicit
  missingness, and bounded Gemini actions.
- P0 shows no Funding Priority, rank, Importance, numeric Climate Risk, cohort-wide
  Community Vulnerability/Equity, or expected flood-reduction benefit.

### Explore Gemini insight

- Is compact and proactively visible because spatial interpretation is central to
  Explore.
- Is grounded only in the current extent, active filters/layers, and visible
  governed projects.
- Expands in the same contextual region and never hides deterministic content.

### Scenario Settings

- Opens as a Funding Plan drawer through **Adjust Scenario**.
- Edits Available Budget; project inclusion/removal occurs in Funding Plan.
- Shows current versus proposed values and validation.
- Requires explicit recalculation/confirmation before replacing the active
  What-If.
- Unapplied edits never change the header context or visible current result.

### Gemini scenario proposal

P0-9 is approved as an interaction aid. Gemini may translate one explicit analyst
command affecting Available Budget or named project inclusion/removal into an
atomic structured proposal. The proposal shows before/after values and
confirm/cancel actions. Confirmation uses the same validation and deterministic
scenario path as manual controls. Gemini may not originate membership, facts,
evidence roles, request amounts, priorities, or recommendations.

### Historical Benchmark

- Is a secondary Funding Plan view of the published January 2026 Historical City
  Recommendation.
- Is structurally isolated from project evidence, analytical-family definition,
  analyst membership, validation, and scenario arithmetic.
- Uses City-specific inclusion terms and preserves published amounts/treatment.
- Shows only evidence-supported overlap and divergence.
- Does not infer City reasoning or characterize either result as correct.
- Is never a scenario input, target, score, or ground truth.

### Reviewed Draft confirmation

- Appears in place over the Funding Plan.
- Identifies the exact Current Confirmed Plan, budget, project membership, and
  supported arithmetic outcomes.
- States that the designation is current-session, draft, non-persisted, and
  non-official.
- Offers cancel and confirm.
- Does not create a saved scenario, formal approval, export, or persistence
  workflow.

### Funding Plan Gemini

- Is compact by default and expands only when invoked.
- Explains governed project evidence, missingness, analyst-confirmed membership,
  budget constraints, or scenario results.
- Never blocks or replaces deterministic results.

## Evidence and Terminology Gates

- People Potentially Benefiting, Structures Benefited, and Implementation Readiness
  are unavailable/unsupported for locked P0 and are omitted unless a later explicit
  methodology revision governs the metric.
- If an approved metric is missing for one project, show explicit project-level
  missingness and never treat or describe it as zero.
- EAZ 2021 may appear only as dated vulnerability context where project geography
  permits association. It is not a Watershed-specific or cohort-wide Community
  Vulnerability/Equity metric.
- Confidence describes only the strength of a documented classification,
  association, or source linkage. The UI never converts it into need, severity,
  benefit, priority, or an independent warning about project worthiness.
- Use public-facing terms supported by the lock: Available Budget, Funding Plan,
  Projects, Included in Plan, Available Projects, evidence context, and evidence
  unavailable. Reserve Historical City Recommendation for the isolated benchmark.
- Explore filters affect presentation only. Funding Plan membership changes only
  after an analyst confirms a valid scenario action.

## Important UI State and Recovery Model

Never collapse the following into a generic “no results” state.

| Context | Required states and recovery |
| --- | --- |
| **Explore counts and filters** | Keep the 12-record P0 analytical family separate from presentation matches. With active filters, show **[matching count] matching · 12 P0 family**. Zero matches keeps filters, family total, and map/list frame visible and offers **Clear filters**. |
| **No P0 analytical-family records** | If governed family derivation produces no records in a later methodology version, suppress Funding Plan claims and link to the all-source purpose audit. It is not a filter result or system failure. |
| **Missing project geometry** | Keep the family record in the list, detail, and Funding Plan; label **Map location unavailable** and provide non-map access. Never invent a marker. |
| **Approved-field missingness** | Show explicit project-level missingness and the methodology-defined effect. Missing is never zero. Unsupported metrics are omitted instead. |
| **Family record not in plan** | Show **Available Project · Not Included in Plan** as analyst scenario state. Do not imply ineligibility, low need, low confidence, a system recommendation, or a City decision. |
| **Valid zero-project plan** | Present a successful deterministic result with its applicable constraint explanation. Distinguish it from invalid/over-budget attempts and system failure. |
| **Over-budget or otherwise invalid attempted plan** | Show exact validation errors and a path to adjust budget or membership. Preserve the last confirmed result and mark attempted inputs not applied. If no prior result exists, keep the working plan unconfirmed. |
| **Genuine system error** | Name the affected surface, preserve unaffected deterministic content, provide retry guidance, and do not imply an analytical result. Contain errors locally where possible. |
| **Project Detail** | Support closed, loading, loaded, approved-field-missing, geometry-missing, locally unavailable, and retry states. Closing/retrying never resets Explore state. Only marker selection uses preview first. |
| **Funding Plan** | Support initial loading, unconfirmed working plan, confirmed Session Reference Plan, confirmed What-If, valid zero-project result, over-budget/invalid attempt, local/system error, and Reviewed Draft indicators. |
| **Scenario Settings** | Support pristine, dirty/unapplied, invalid, ready, validating, replacement confirmation, success, over-budget, and failure. Dirty inputs never change the current result. Invalid inputs remain editable but not applied. |
| **Historical Benchmark** | Support closed, loading, available, partially supported/missing published fields, unavailable, and retry. Missing benchmark data never changes ClimateCapital results. |
| **Reviewed Draft** | Support not reviewed, confirmation open, marked, and cleared. The designation binds to the exact confirmed result. Unapplied edits and failed recalculation do not clear it. Confirming a replacement of an accepted What-If warns and clears that designation. |
| **Gemini explanation** | Support compact/idle, expanded, loading, grounded answer, bounded refusal, unavailable, and retry. No required action depends on Gemini. |
| **Gemini proposal** | Support proposal-ready, validation error, confirmation pending, cancelled, deterministic validation, applied, over-budget/invalid, and failed. Nothing changes before confirmation. |
| **Data & Methodology** | Support complete page, anchored focus, local section loading, approved-field/source missingness, local section failure, and retry. The rest of the page and originating screen remain intact. |
| **Help & Resources** | Remain readable without Gemini. If a deep link fails, keep the guide usable and offer retry or the Data & Methodology landing page. |

## Low-Fidelity Wireframes

These diagrams establish hierarchy and behavior only.

### Explore

~~~text
┌──────────────┬───────────────────────────────────────────────────────────────┐
│ ClimateCapital│ Decision: [decision context]                                 │
│              │ Plan: [Current Confirmed Plan]                                │
│ Explore      │ Available Budget: [amount]                                    │
│ Funding Plan ├───────────────────────────────────────────────────────────────┤
│ Data & Method│ [approved summary] [approved summary] [plan status]            │
│ Help         │ [Search] [Presentation filters] [Layers]                       │
│              ├───────────────────────────────┬───────────────────────────────┤
│              │                               │ Projects                      │
│              │        IMMERSIVE MAP          │ [count] matching · 12 P0      │
│              │        + legend               │ family                        │
│              │                               │ [project row]                 │
│              │                               │ [project row]                 │
│              ├───────────────────────────────┴───────────────────────────────┤
│              │ Funding Plan: [count] included · [budget use] [View Plan]     │
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
default visualization; the locked evidence roles do not force every contextual
overlay off.

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
                         │ Purpose / confidence            │
                         │ Funding Plan: [scenario status] │
                         │ [evidence role / context]       │
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
│ Navigation   │ Funding Plan · [Current Confirmed Plan]                      │
│              │ [budget used] [Available Budget] [remainder] [project count] │
│              │ [Adjust Scenario] [Historical Benchmark] [Mark Reviewed Draft]│
│              ├──────────────────────────────┬────────────────────────────────┤
│              │ Included in Plan            │ Available Projects             │
│              │ [project / request / remove]│ [project / request / add]      │
│              │ [evidence-state summary]    │ [missingness / status]         │
│              ├──────────────────────────────┴────────────────────────────────┤
│              │ [full-request/budget validation] [supported deltas]          │
│              │ Gemini explanation [Ask / Expand]                            │
└──────────────┴───────────────────────────────────────────────────────────────┘

Adjust Scenario → ┌─────────────────────────────────────────┐
                  │ Scenario Settings                   [×] │
                  │ Available Budget [current → proposed]   │
                  │ Membership edited in Funding Plan      │
                  │ [validation / unapplied status]         │
                  │ [Cancel] [Recalculate and Confirm]      │
                  └─────────────────────────────────────────┘
~~~

### Reviewed Draft confirmation

~~~text
┌─────────────────────────────────────────────────────┐
│ Mark this result as the Reviewed Draft?             │
│ Plan: [Current Confirmed Plan]                       │
│ Budget / membership / arithmetic: [governed summary]│
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
│ Family       │ [all 37] [purpose method] [24 broad] [12 P0 + limitations]     │
│ Evidence     │ [sources/vintages] [source vs derived] [missingness]           │
│ Evidence     │ [roles] [coverage] [confidence meaning] [unsupported metrics]  │
│ Funding Plan │ [analyst membership/full-request/budget arithmetic]            │
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

1. Orient with the historical decision context, Current Confirmed Plan,
   Available Budget, and simulation disclaimer.
2. Use the map and synchronized list to reveal one supported flood/equity context
   and its limitations.
3. Inspect one Project Detail and show evidence roles, confidence/missingness, and
   current scenario status.
4. Open Funding Plan, add or remove one complete request, and show exact budget
   validation and arithmetic without implying a recommendation.
5. Change budget and/or membership, confirm deterministic validation, and show
   supported Session Reference Plan deltas.
6. Invoke one grounded explanation and mark the exact result as the current-session
   Reviewed Draft.

A five-minute expansion may add Historical Benchmark, deeper methodology,
recovery, a second project, or Compare if SP0-1 survives.

## Remaining Presentation Dependencies

The Methodology Lock decides the all-37 universe, provisional 12-record P0
analytical family, evidence roles, missingness treatment, unsupported metrics,
analyst-controlled membership, and budget arithmetic. This screen specification
still does not decide:

- the default combination of contextual map layers;
- visual styling for evidence roles and classification confidence;
- whether People Potentially Benefiting, Implementation Readiness, or a heat
  co-benefit can appear in a later methodology revision; or
- architecture and implementation details.

## Related Sources of Truth

- [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
- [Product plan](product-plan.md)
- [User stories and acceptance intent](user-stories.md)
- [Delivery and release gates](../delivery/execution-plan.md)
- [Decision history](../decisions.md)
- [Current project status](../../PROJECT_PROGRESS.md)
