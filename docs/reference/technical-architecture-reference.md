# ClimateCapital AI Technical Architecture Reference

> **Status:** Superseded pre-lock reference material — not authoritative
> **Created:** 2026-08-27
> **Superseded:** 2026-09-01 by
> [p0-architecture.md](../architecture/p0-architecture.md) and
> [data-contracts.md](../architecture/data-contracts.md)
> **Authority boundary:** This file preserves the planning frame that existed
> before Architecture Lock. Where it describes a candidate or unresolved question,
> the approved architecture documents now control.

## Why This Document Exists

This brief gave the Architecture planning task durable pre-lock context for
investigating a small, low-cost design without depending on chat history. It is
retained to show the planning frame and alternatives, not as a current design.

The repository did not contain a detailed candidate architecture, service
selection, data model, ingestion design, or cloud cost model at the time of this
closeout. Therefore, this document does not claim to recover an approved or
previously complete technical proposal. Its candidate material remains historical;
the 2026-09-01 Architecture Lock resolved it.

## Approved Resolution

The Architecture Lock selected:

- one React/TypeScript/Vite and FastAPI container on public Cloud Run in
  `us-central1`, request-billed with minimum instances 0, maximum instances 1, and
  one Uvicorn worker;
- a reviewed, pinned four-file release-data bundle packaged in the image, with no
  live source acquisition during release builds and no runtime BigQuery, Cloud
  Storage, or GIS queries;
- browser `sessionStorage` only, no application database or server session store;
- independent server evaluation of both current and reference plan inputs;
- a structurally separate Historical Benchmark path;
- current RNA display geometry on where available, FEMA and EAZ 2021 off by
  default, no Fully Developed FloodPro, direct compliant configurable OSM tiles,
  and no fabricated geography;
- required grounded `POST /api/v1/gemini/explain` using Gemini 3.6 Flash through
  the global standard on-demand Google Cloud publisher endpoint with ADC, while
  natural-language proposal is post-core stretch;
- externally checksummed data manifest plus separate code/data/manifest/image
  deployment identity; and
- health, built-in Cloud Run metrics, bounded structured logs, smoke tests,
  scale-to-zero cost controls, and bounded image retention.

The exact topology, cost assumptions, dependency order, rejection list, release
gates, artifact schemas, API contracts, browser state, and trust boundaries are in
the two authoritative architecture documents linked above.

## Current Repository Reality

- The repository has no application implementation, but it now contains governed
  documentation, a source registry, reproducible source/GIS reconnaissance tools,
  tests, a 37-record source-universe artifact, RNA snapshot provenance/matches,
  and one validated raw BigQuery table.
- Architecture is approved and locked in `docs/architecture/`; application
  implementation and architecture-informed delivery plans have not begun.
- Existing raw preservation and raw BigQuery resources remain reconnaissance/release
  validation state, not runtime dependencies. The selected application, Gemini,
  map, deployment, and session choices are recorded in the Architecture Lock.
- The public Git remote is recorded in PROJECT_PROGRESS.md.
- A local process-job Stop hook is known to fail because the node executable is
  unavailable; this is an environment issue, not an application architecture
  decision.

## Approved Product Constraints with Technical Consequences

The constraints below are approved. Their technical implications must be addressed
by Architecture, but the implementation mechanisms are not selected here.

| Approved constraint | Consequence Architecture must satisfy |
| --- | --- |
| Austin Watershed historical simulation is the P0 pilot | Data and UI must preserve dated historical context and disclaimers. |
| $125 million Projects sub-envelope is the default Historical Envelope context | Plan inputs/results need explicit budget provenance without treating an analyst plan as historical. |
| All 37 records are governed and the provisional 12-record P0 analytical family is a derived ClimateCapital purpose classification | Family derivation, confidence, ambiguity, and the 25 records outside the family must remain reproducible, visible, and auditable. |
| Historical City Recommendation is descriptive only | City treatment must be structurally isolated from project evidence, analytical-family definition, analyst membership, validation, and scenario arithmetic. |
| External evidence may use defensible vintages | Provenance must be field/dataset-aware rather than forcing one global date. |
| Deterministic logic is authoritative | Facts, evidence roles, family derivation, scenario validation, budget arithmetic, and supported comparison require a testable deterministic path. |
| P0 has no score, rank, weight, or optimizer | Contracts must not contain placeholder priority fields, hidden objectives, imputation, or automatic membership. |
| Full-request inclusion/exclusion only | Analyst membership controls must not silently introduce partial funding or editable request amounts. |
| One immutable Session Reference Plan and at most one active What-If | State management can remain bounded; saved scenario storage is out of P0. |
| Scenario inputs are Available Budget and analyst project membership only | Validation must reject unknown IDs and governed IDs outside the active analytical family, duplicates, edited request amounts, partial funding, and over-budget confirmation. |
| Manual changes and Gemini-translated explicit commands share one path | One validated scenario command/recalculation contract must serve both interfaces. |
| Gemini is explanation/interaction only | The AI layer consumes governed facts and translates explicit analyst commands into pending allowed inputs; it never authors analytical facts or outcomes. |
| Reviewed Draft is current-session only | No account, workflow, or durable draft persistence is required in P0. |
| Presentation filters do not change analysis | UI query/filter state must remain separate from scenario/analytical state. |
| Missing geometry does not remove family membership | Map representation and P0 family/Funding Plan access must be decoupled. |
| Missing is not zero | Data representation must distinguish absent, unsupported, not applicable, and numeric zero where the methodology requires it. |
| Failed recalculation preserves the last successful result | Confirmed and attempted scenario state require separate representation. |
| Gemini failure is local | Deterministic evidence/results and manual controls cannot depend on AI availability. |
| Desktop-first, tablet-usable, accessible UI | Technology choices must support keyboard, focus, labels, contrast, and non-map equivalents. |
| Very low cloud spending | Architecture must model idle and demo-period cost and avoid unnecessary always-on resources. |

Authoritative product detail:

- [Product plan](../product/product-plan.md)
- [User stories](../product/user-stories.md)
- [Screen specification](../product/screen-spec.md)
- [Decision history](../decisions.md)

## Pre-Lock Candidate Logical System Shape — Historical

A future Architecture task may evaluate a flow such as:

~~~text
Governed source records and evidence
        │
        ▼
Versioned raw/staged inputs
        │
        ▼
Purpose classification + P0 analytical-family derivation
        │
        ├── provenance / quality / missingness
        ▼
Evidence-role and missingness contract
        │
        ▼
Analyst-controlled full-request membership
        │
        ▼
Deterministic validation and budget arithmetic
        │
        ├── immutable confirmed Session Reference Plan
        └── confirmed active What-If scenario
        │
        ▼
Governed result contract
        ├── Explore / Project Detail / Funding Plan
        ├── separately sourced Historical Benchmark adapter (comparison only)
        └── bounded Gemini grounding and proposal validation
~~~

This diagram is a responsibility map, not approval of separate services,
deployment units, storage systems, batch jobs, or APIs. The smallest MVP may
combine several responsibilities if reproducibility, testability, and scope
boundaries remain intact.

## Pre-Lock Architecture Choice Areas — Historical

### Application shape considered before lock

Candidate patterns to compare:

- Static or client-rendered web interface plus a small managed API.
- Server-rendered/full-stack web application in one deployable unit.
- Single container serving UI assets and API behavior.
- Precomputed governed artifacts with minimal runtime recalculation.
- Hybrid precomputation for baseline results plus bounded runtime What-If
  calculation.

Evaluation criteria:

- Ability to finish and test before the deadline.
- Clear separation of presentation state, scenario inputs, deterministic analysis,
  benchmark data, and Gemini.
- Cold-start and demo reliability.
- Low idle cost and simple deployment.
- Ease of reproducing every displayed result.
- Accessibility and map-library compatibility.

This reference selected no pattern. The Architecture Lock now selects the single
Cloud Run container described in its Approved Resolution.

### Google Cloud and hosting options considered before lock

The Architecture task may evaluate managed serverless compute, static hosting,
object storage, a managed analytical store, a lightweight transactional store, and
managed AI access as categories. Candidate Google Cloud products must be checked
against current pricing, quotas, regions, deployment complexity, and program rules
at Architecture time.

Questions to resolve:

- Can all governed data/results be packaged as versioned static artifacts, or does
  What-If recalculation require a runtime service?
- Does the MVP need durable application data beyond versioned input/output
  artifacts?
- Can Reviewed Draft and active What-If state remain browser-session state?
- What is the smallest public deployment boundary that supports a reliable demo?
- Which resources incur idle charges, minimum capacity, egress, or request costs?
- What budget cap, alert, quota, or shutdown practice is appropriate?

No Google Cloud resource or service was approved by this reference. The
Architecture Lock now governs the selected services.

### Frontend and map considerations before lock

The interface needs:

- Large synchronized map/list Explore workspace.
- Layer/legend controls with evidence-backed defaults.
- Shared Project Detail across list and marker paths.
- Dedicated Funding Plan and contextual drawers/dialogs.
- Keyboard and non-map equivalents.
- Local failure containment and last-successful-result behavior.

This reference required comparison of UI and mapping approaches. The Architecture
Lock selects React/TypeScript/Vite, Leaflet, direct configurable OSM tiles, and a
neutral fallback under the approved evidence defaults and usage constraints.

## Data and Ingestion Considerations

### Source layers

The data design is expected to distinguish at least:

- Capital-project source records.
- Derived purpose classification, confidence, ambiguity, broad-family treatment,
  and provisional 12-record P0 analytical-family membership.
- Project geometry/display geometry.
- Problem Score association context and current FEMA hazard context.
- EAZ 2021 contextual vulnerability evidence where defensible geography exists.
- Project costs/Department Request.
- Historical City Recommendation treatment and amounts.
- Dataset- and field-level source/vintage metadata.
- Evidence roles, association/classification confidence, explicit missingness,
  analyst scenario membership, budget validation, and arithmetic results.

The exact datasets, fields, identifiers, vintages, and joins are unresolved
evidence-stage decisions.

### Candidate ingestion pattern considered before lock

The Architecture task may consider:

1. Preserve immutable raw source snapshots with provenance.
2. Normalize stable project identifiers and source-field names.
3. Apply the documented purpose classification and retain all 37 source records,
   including confidence, ambiguity, broad-family, and P0-family treatment.
4. Join defensible evidence using documented spatial or identifier logic.
5. Preserve geometry availability separately from purpose and P0-family treatment.
6. Materialize governed facts and contextual/research/unsupported evidence states
   with explicit missingness.
7. Produce reproducible scenario-input, arithmetic, and isolated benchmark
   artifacts.
8. Validate schemas, counts, money units, geometry, provenance, and deterministic
   reruns.

This reference did not decide their implementation. The Architecture Lock now
separates controlled acquisition/curation from source-independent release builds
and packages the reviewed artifacts in the runtime image.

### Data-version and lineage needs

Architecture must make it possible to trace a displayed or Gemini-cited value
through:

source record → source vintage → derived purpose/family decision → evidence join
→ evidence role/missingness → analyst membership → budget validation/arithmetic →
scenario result.

The later approved data-lineage document should define:

- Artifact/version identifiers.
- Dataset and field provenance.
- Transformation ownership.
- Validation and reconciliation points.
- Historical benchmark isolation.
- Rebuild/reproducibility procedure.
- Treatment of corrections without rewriting prior snapshots.

## Locked Methodology and Funding-Plan Considerations

Approved:

- Deterministic code is authoritative for facts, family derivation, evidence
  states, validation, integer-dollar arithmetic, and supported comparison.
- P0 has no Funding Priority score, project rank, Importance weights, quantitative
  risk/equity score, expected flood-reduction benefit, or optimization objective.
- P0 uses analyst-controlled full-request inclusion/removal within the active
  12-record analytical family; only a later governed methodology decision may
  change that family contract.
- Available Budget and project membership are the only scenario inputs.
- The same confirmed inputs must reproduce included/not-included IDs, total,
  remainder, count, and supported deltas.
- Invalid or over-budget attempts preserve the last confirmed result.

Architecture must require a small reproducible scenario contract, input/output
versioning, exact money-unit handling, and tests for active-family membership,
unknown/out-of-family and duplicate IDs, governed request integrity, full-request
membership, over-budget rejection, valid zero-project plans, and
last-successful-state preservation. It must not add placeholder scoring fields or
choose a synthetic objective.

## Gemini and AI Integration Considerations

### Approved boundary

Gemini may:

- Explain governed project evidence roles, missingness, analyst-confirmed Funding
  Plan membership, budget constraints/arithmetic, and supported scenario changes.
- Translate one explicit analyst command for Available Budget or named project
  inclusion/removal into a pending structured proposal.
- Communicate governed uncertainty and limitations.
- Decline unsupported City reasoning or out-of-scope analysis.

Gemini may not:

- Invent or calculate analytical facts.
- Originate a funding recommendation or change source data, purpose/family
  classification, evidence roles, request amounts, constraints, or confirmed
  membership.
- Apply a proposal without explicit confirmation.
- Become a dependency for deterministic content or manual scenario control.

### Candidate integration pattern considered before lock

The Architecture task may consider a bounded grounding package containing only
the governed fields needed for the current screen/context, a structured proposal
schema for allowed inputs, server-side or shared validation, and a post-response
check that rejects unsupported fields or numerical contradictions.

Choices to resolve:

- Where prompt construction and grounding validation run.
- Whether responses stream.
- How citations/provenance are represented in the UI contract.
- How token use, latency, retries, quotas, and cost are bounded.
- What is logged without retaining sensitive or unnecessary content.
- How deterministic fallbacks and unavailable states are triggered.
- Which Gemini model and API surface meet current program, cost, latency, and
  deployment requirements.

This reference approved no integration. The Architecture Lock now governs the
model, endpoint, ADC, API, grounding, rate, token, logging, and kill-switch
boundaries.

## State and Interface Boundaries to Preserve

Architecture should model these as distinct concepts even if implemented in one
process:

- Decision context.
- Historical Benchmark data.
- Immutable Session Reference Plan inputs/results.
- Current Confirmed Plan identity and result.
- Dirty/unapplied scenario controls.
- Gemini proposal awaiting confirmation.
- Presentation-only Explore filters and map state.
- Last successful deterministic Funding Plan.
- Current-session Reviewed Draft binding.
- P0 analytical family versus current presentation matches.
- Project-level missingness versus unsupported metrics.
- Over-budget/invalid attempted state versus genuine system failure.

No external API schema or persistence model was approved by this reference. The
Architecture Lock now approves the `/api/v1` surface and browser-session-only
model.

## Security and Privacy Considerations

The current product concept appears to use public-sector project and geographic
evidence, but source licensing, sensitivity, and privacy have not been verified.
Architecture must still evaluate:

- Source license and redistribution restrictions.
- Whether any source includes personal, protected, or sensitive location data.
- Least-privilege service identities and secrets handling.
- Public read surface versus protected administrative/deployment actions.
- Input validation for scenario controls and Gemini requests.
- Prompt-injection/data-exfiltration risks in retrieved or source-provided text.
- Output encoding, dependency risk, and content security controls.
- Logging redaction, retention, and access.
- Abuse/rate controls for a public demo.
- Reproducible builds and separation of local credentials from Git.

Do not assume “public data” eliminates security or privacy obligations.

## Cost-Control Considerations

Architecture must produce an explicit low-cost plan covering:

- Expected idle, development, demo, and short-burst usage.
- Compute requests, memory/time, and minimum-instance settings.
- Storage, analytical queries, map tiles, network egress, logging, and Gemini
  usage.
- Free-tier or program-credit assumptions, verified at decision time.
- Budget alerts/quotas and a manual shutdown or scale-to-zero procedure.
- Local/precomputed work that can reduce cloud processing without undermining the
  demonstration of real analytics and data engineering.
- Cost risks from retries, public traffic, logs, or unconstrained Gemini prompts.

This reference approved no cost estimate. The Architecture Lock records the
verified-at-lock assumptions, uncertainty, abuse exposure, controls, and shutdown
procedure.

## Observability and Operational Considerations

The smallest useful operational surface may need:

- Deployment health and version identifier.
- Data/artifact version used by the running application.
- Deterministic calculation duration and failure category.
- Gemini request availability, latency, failure category, and bounded usage.
- Client-visible error correlation without exposing secrets.
- Budget/usage visibility.
- A way to verify that displayed and cited numbers match governed output.

Architecture should minimize operational complexity while preserving enough
evidence to diagnose a failed demo. The Architecture Lock selects `/healthz`,
built-in Cloud Run metrics, bounded structured logging, and smoke tests only.

## Testing Considerations

Future test planning must cover:

- All-37 purpose classification, confidence/ambiguity, and exact provisional
  12-record analytical family.
- Missing geometry without family exclusion.
- Missing, unsupported, zero, and not-applicable values.
- Exact budget arithmetic, governed request integrity, duplicate/unknown-ID
  rejection, full-request inclusion, over-budget rejection, and valid zero-project
  outcomes.
- Separation of analyst plan membership and Historical City treatment.
- Manual/Gemini proposal parity and confirmation boundaries.
- Last-successful-result preservation after invalid, over-budget, or failed runs.
- Gemini grounding, numerical consistency, refusal, outage, and deterministic
  fallback.
- Presentation filters not affecting analytical state.
- Keyboard, focus, labels, contrast, and non-map access.
- Source/vintage and lineage traceability.
- Public deployment smoke test, cost safeguards, and three-minute demo path.

The approved test plan remains the next delivery-planning artifact after the now
completed Architecture Lock.

## Pre-Lock Alternatives and Tradeoffs — Historical

| Choice | Tradeoff to evaluate |
| --- | --- |
| Precomputed reference inputs vs runtime computation | Simplicity/reliability versus interactive transparency and scenario flexibility |
| Browser-local vs server-side What-If calculation | Cost/latency versus governed-code control, consistency, and exposure |
| Static artifacts vs database | Low cost/reproducibility versus query flexibility and update workflow |
| One deployable unit vs split frontend/API | Simplicity versus isolation and independent scaling |
| Batch pipeline vs on-demand ingestion | Reproducibility and deadline safety versus freshness |
| Hosted basemap/layers vs packaged assets | Usability and licensing/cost/network dependencies |
| Direct model call vs mediated AI service | Simplicity versus security, validation, cost control, and observability |
| Client session state vs durable scenario storage | P0 simplicity versus features explicitly deferred to P1 |

These were investigation axes, not recommendations. Their approved resolutions are
recorded in the Architecture Lock.

## Pre-Lock Architecture Questions — Resolved

1. What is the smallest deployable application boundary that satisfies required P0?
2. Which language/framework choices best fit the deadline and existing environment?
3. Which data stays static and versioned, and which calculations must occur at
   runtime?
4. Where do deterministic family derivation, evidence-state materialization,
   scenario validation, and budget arithmetic run?
5. What governed input/output contract separates analysis from UI and Gemini?
6. How are historical benchmark data and ClimateCapital analytical data isolated?
7. What is the source-of-truth and rebuild strategy for raw, normalized, and
   derived artifacts?
8. What persistence, if any, is required beyond browser-session state?
9. Which map approach supports the approved layers, accessibility, terms, and
   budget?
10. Which current Google Cloud and Gemini options meet cost, latency, quota, and
    program constraints?
11. What security boundary is required for a public demo?
12. What observability is essential for demo reliability without excessive cost?
13. How will local and cloud validation prove deterministic/UI/Gemini agreement?
14. How will deployment and resource teardown avoid post-demo spend?

Evidence-methodology questions remain separate and are listed in
[PROJECT_PROGRESS.md](../../PROJECT_PROGRESS.md).

All 14 questions above were resolved by the approved topology, data/runtime
contracts, security/observability/cost plan, and verification/dependency order in
the Architecture Lock. They are preserved here as the pre-lock checklist.

## Architecture Task Exit Criteria — Achieved

The Architecture task was required to:

- Reconcile this reference with the current repository and authoritative product
  specifications.
- Investigate current service/pricing/program facts where relevant.
- Present a decision-complete candidate architecture with explicit alternatives and
  tradeoffs.
- Define system boundaries, data flow, authoritative contracts, data design,
  deployment, security, observability, testing implications, and a cloud cost plan.
- Show how every approved product constraint is satisfied.
- Preserve the locked methodology and keep only genuinely unresolved architecture
  or presentation choices explicit rather than silently reopening evidence work.
- Obtain explicit user approval before creating/finalizing approved documents under
  docs/architecture.

The user approved the proposal and final implementation-precision corrections on
2026-09-01. The resulting authoritative documents satisfy this exit checklist.

## Source Hierarchy

If this reference conflicts with an approved source, the approved source wins:

1. [Repository working rules](../../AGENTS.md)
2. [Current status and handoff](../../PROJECT_PROGRESS.md)
3. [P0 evidence and methodology lock](../methodology/p0-evidence-methodology.md)
4. [Approved product plan](../product/product-plan.md)
5. [Approved user stories](../product/user-stories.md)
6. [Approved screen specification](../product/screen-spec.md)
7. [Approved decision history](../decisions.md)
8. [Execution plan](../delivery/execution-plan.md)
9. [P0 Architecture Lock](../architecture/p0-architecture.md)
10. [P0 data and runtime contracts](../architecture/data-contracts.md)
11. This superseded non-authoritative reference
