# ClimateCapital AI Technical Architecture Reference

> **Status:** Reference material only — not an approved Architecture Lock
> **Created:** 2026-08-27
> **Authority boundary:** Approved product constraints are identified explicitly
> and linked to their sources. Every architecture, service, storage, data,
> deployment, security, observability, and testing approach below is a candidate
> consideration or unresolved question until the user explicitly approves the
> Architecture Lock.

## Why This Document Exists

This brief gives a fresh Architecture planning task enough durable context to
investigate a small, low-cost design without depending on an earlier chat. It
consolidates technical implications of the approved Product and Design Lock and
organizes the choices the Architecture task must resolve.

The repository did not contain a detailed candidate architecture, service
selection, data model, ingestion design, or cloud cost model at the time of this
closeout. Therefore, this document does not claim to recover an approved or
previously complete technical proposal. Its candidate material is an exploratory
planning frame derived from the locked product requirements.

## Current Repository Reality

- The repository is documentation-only.
- No application source, tests, manifests, dependencies, datasets, pipelines,
  schemas, cloud configuration, deployment configuration, or generated artifacts
  exist.
- Architecture is not established.
- No Google Cloud service, Gemini model/API pattern, database, map library,
  framework, language, or optimization library has been selected.
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
| $125 million Projects sub-envelope is the Historical Baseline constraint | Scenario inputs/results need explicit budget provenance and validation. |
| Candidate cohort is rule-derived | Eligibility must be reproducible and auditable; manual demo curation is prohibited. |
| Historical City Recommendation is descriptive only | City treatment must be isolated from ClimateCapital feature, score, rank, weight, objective, and selection inputs. |
| External evidence may use defensible vintages | Provenance must be field/dataset-aware rather than forcing one global date. |
| Deterministic logic is authoritative | Eligibility, transformations, scores, ranks, constraints, and portfolio results require a testable deterministic path. |
| Ranking and constrained portfolio selection are separate | Outputs and interfaces must preserve distinct artifacts and explanations. |
| Full-project inclusion/exclusion only | Optimization must not silently introduce partial funding. |
| One immutable baseline and at most one active What-If | State management can remain bounded; saved scenario storage is out of P0. |
| Scenario inputs are budget and approved weights only | Validation and interfaces must reject or omit other editable analytical inputs. |
| Manual and Gemini-originated changes share one path | One validated scenario command/recalculation contract must serve both interfaces. |
| Gemini is explanation/interaction only | The AI layer consumes governed facts and proposes allowed inputs; it never authors analytical facts or outcomes. |
| Reviewed Draft is current-session only | No account, workflow, or durable draft persistence is required in P0. |
| Presentation filters do not change analysis | UI query/filter state must remain separate from scenario/analytical state. |
| Missing geometry does not imply ineligibility | Map representation and analytical eligibility must be decoupled. |
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

## Candidate Logical System Shape — Not Approved

A future Architecture task may evaluate a flow such as:

~~~text
Source records and evidence
        │
        ▼
Versioned raw/staged inputs
        │
        ▼
Eligibility + evidence transformation
        │
        ├── provenance / quality / missingness
        ▼
Deterministic scoring and ranking
        │
        ▼
Constrained full-project portfolio calculation
        │
        ├── immutable Historical Baseline result
        └── confirmed active What-If result
        │
        ▼
Governed result contract
        ├── Explore / Project Detail / Funding Plan
        ├── Historical Benchmark adapter
        └── bounded Gemini grounding and proposal validation
~~~

This diagram is a responsibility map, not approval of separate services,
deployment units, storage systems, batch jobs, or APIs. The smallest MVP may
combine several responsibilities if reproducibility, testability, and scope
boundaries remain intact.

## Architecture Choice Areas

### Application shape

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

No pattern is selected in this document.

### Google Cloud and hosting options

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

No Google Cloud resource or service is approved here.

### Frontend and map

The interface needs:

- Large synchronized map/list Explore workspace.
- Layer/legend controls with evidence-backed defaults.
- Shared Project Detail across list and marker paths.
- Dedicated Funding Plan and contextual drawers/dialogs.
- Keyboard and non-map equivalents.
- Local failure containment and last-successful-result behavior.

Architecture must compare candidate UI and mapping approaches for bundle size,
accessibility, supported geometry/layers, public basemap terms/costs, offline/static
artifact compatibility, and implementation speed. No framework, component system,
or map provider is selected.

## Data and Ingestion Considerations

### Source layers

The data design is expected to distinguish at least:

- Capital-project source records.
- Eligibility inputs and exclusion reasons.
- Project geometry/display geometry.
- Flood exposure and flood-reduction evidence.
- Social vulnerability and any separately supported Community Equity evidence.
- Project costs/Department Request.
- Historical City Recommendation treatment and amounts.
- Dataset- and field-level source/vintage metadata.
- Derived evidence, confidence/quality signals, scores, ranks, and portfolio
  results.

The exact datasets, fields, identifiers, vintages, and joins are unresolved
evidence-stage decisions.

### Candidate ingestion pattern — not approved

The Architecture task may consider:

1. Preserve immutable raw source snapshots with provenance.
2. Normalize stable project identifiers and source-field names.
3. Apply documented eligibility rules and retain both eligible records and
   excluded source records with reasons.
4. Join defensible evidence using documented spatial or identifier logic.
5. Preserve geometry availability separately from analytical eligibility.
6. Materialize governed analytical inputs with explicit missingness.
7. Produce reproducible baseline and benchmark artifacts.
8. Validate schemas, counts, money units, geometry, provenance, and deterministic
   reruns.

Whether these are scripts, jobs, queries, build steps, or services is not decided.

### Data-version and lineage needs

Architecture must make it possible to trace a displayed or Gemini-cited value
through:

source record → source vintage → eligibility decision → evidence join →
transformation → score/rank → constraint/objective → portfolio result.

The later approved data-lineage document should define:

- Artifact/version identifiers.
- Dataset and field provenance.
- Transformation ownership.
- Validation and reconciliation points.
- Historical benchmark isolation.
- Rebuild/reproducibility procedure.
- Treatment of corrections without rewriting prior snapshots.

## Scoring and Optimization Considerations

Approved:

- Deterministic code is authoritative.
- Ranking is separate from constrained portfolio selection.
- P0 uses full-project inclusion/exclusion.
- Available Budget and approved weights are the only scenario inputs.
- The same confirmed inputs must reproduce the same result.

Unresolved:

- Scoring dimensions and source evidence.
- Transformations and normalization.
- Default and editable weight values and valid-sum/range rules.
- Score breakdown/contribution representation.
- Confidence methodology and whether/how it affects analysis.
- Missing-evidence treatment.
- Optimization objective, tie-breaking, and supported constraints.
- Feasibility rules and valid zero-project behavior.
- Supported baseline/What-If and City benchmark comparison metrics.

Architecture should require a pure or otherwise reproducible analytical contract,
input/output versioning, deterministic tie handling, money-unit precision, and
tests that prove budget and full-project constraints. It must not choose the
methodology on behalf of the evidence stage.

## Gemini and AI Integration Considerations

### Approved boundary

Gemini may:

- Explain governed project evidence, scores/ranks, Funding Plan membership,
  constraints, and supported scenario changes.
- Produce one structured proposal containing only Available Budget and approved
  weight changes.
- Coordinate multiple approved-weight changes within one atomic proposal when
  required for a valid configuration.
- Communicate governed uncertainty and limitations.
- Decline unsupported City reasoning or out-of-scope analysis.

Gemini may not:

- Invent or calculate analytical facts.
- Change source data, eligibility, evidence, score, rank, constraints, objective,
  or portfolio membership.
- Apply a proposal without explicit confirmation.
- Become a dependency for deterministic content or manual scenario control.

### Candidate integration pattern — not approved

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

No model, SDK, prompt, API, or cloud integration is approved here.

## State and Interface Boundaries to Preserve

Architecture should model these as distinct concepts even if implemented in one
process:

- Decision context.
- Historical Benchmark data.
- Immutable Historical Baseline inputs/results.
- Current confirmed scenario and result.
- Dirty/unapplied scenario controls.
- Gemini proposal awaiting confirmation.
- Presentation-only Explore filters and map state.
- Last successful deterministic Funding Plan.
- Current-session Reviewed Draft binding.
- Eligible cohort versus current presentation matches.
- Project-level missingness versus unsupported metrics.
- Analytical infeasibility versus genuine system failure.

No external API schema or persistence model has been approved.

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

No cost estimate is approved until architecture choices and current pricing are
verified.

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
evidence to diagnose a failed demo. No monitoring product is selected.

## Testing Considerations

Future test planning must cover:

- Eligibility inclusion/exclusion and audit reasons.
- Missing geometry without analytical exclusion.
- Missing, unsupported, zero, and not-applicable values.
- Score/rank reproducibility and approved contribution display.
- Budget constraint, full-project inclusion, tie behavior, feasibility, and valid
  zero-project outcomes.
- Separation of rank, plan membership, and Historical City treatment.
- Manual/Gemini proposal parity and confirmation boundaries.
- Last-successful-result preservation after invalid, infeasible, or failed runs.
- Gemini grounding, numerical consistency, refusal, outage, and deterministic
  fallback.
- Presentation filters not affecting analytical state.
- Keyboard, focus, labels, contrast, and non-map access.
- Source/vintage and lineage traceability.
- Public deployment smoke test, cost safeguards, and three-minute demo path.

The approved test plan will be created after Architecture Lock.

## Alternatives and Tradeoffs for Architecture to Investigate

| Choice | Tradeoff to evaluate |
| --- | --- |
| Precomputed baseline vs runtime computation | Simplicity/reliability versus interactive transparency and scenario flexibility |
| Browser-local vs server-side What-If calculation | Cost/latency versus governed-code control, consistency, and exposure |
| Static artifacts vs database | Low cost/reproducibility versus query flexibility and update workflow |
| One deployable unit vs split frontend/API | Simplicity versus isolation and independent scaling |
| Batch pipeline vs on-demand ingestion | Reproducibility and deadline safety versus freshness |
| Hosted basemap/layers vs packaged assets | Usability and licensing/cost/network dependencies |
| Direct model call vs mediated AI service | Simplicity versus security, validation, cost control, and observability |
| Client session state vs durable scenario storage | P0 simplicity versus features explicitly deferred to P1 |

These are investigation axes, not recommendations.

## Unresolved Architecture Questions

1. What is the smallest deployable application boundary that satisfies required P0?
2. Which language/framework choices best fit the deadline and existing environment?
3. Which data stays static and versioned, and which calculations must occur at
   runtime?
4. Where do deterministic eligibility, scoring, ranking, and optimization run?
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

## Architecture Task Exit Criteria

Before an Architecture Lock can be approved, the fresh Architecture task should:

- Reconcile this reference with the current repository and authoritative product
  specifications.
- Investigate current service/pricing/program facts where relevant.
- Present a decision-complete candidate architecture with explicit alternatives and
  tradeoffs.
- Define system boundaries, data flow, authoritative contracts, data design,
  deployment, security, observability, testing implications, and a cloud cost plan.
- Show how every approved product constraint is satisfied.
- Keep unresolved evidence-methodology choices parameterized rather than silently
  resolving them.
- Obtain explicit user approval before creating/finalizing approved documents under
  docs/architecture.

## Source Hierarchy

If this reference conflicts with an approved source, the approved source wins:

1. [Repository working rules](../../AGENTS.md)
2. [Current status and handoff](../../PROJECT_PROGRESS.md)
3. [Approved product plan](../product/product-plan.md)
4. [Approved user stories](../product/user-stories.md)
5. [Approved screen specification](../product/screen-spec.md)
6. [Approved decision history](../decisions.md)
7. [Execution plan](../delivery/execution-plan.md)
8. This non-authoritative reference
