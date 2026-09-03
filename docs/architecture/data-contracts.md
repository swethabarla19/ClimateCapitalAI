# ClimateCapital AI P0 Data and Runtime Contracts

> **Status:** Approved and locked on 2026-09-01
> **Authority:** This document is normative for P0 release artifacts, deployment
> identity, runtime APIs, browser-session state, deterministic Funding Plan
> evaluation, benchmark isolation, and Gemini mediation. The system topology and
> operations are in [p0-architecture.md](p0-architecture.md); analytical meaning is
> governed by
> [p0-evidence-methodology.md](../methodology/p0-evidence-methodology.md).

## Contract Principles

1. Governed values and deterministic outputs are server-authoritative.
2. All money is exact integer dollars; no binary floating-point money enters an
   artifact, API, fingerprint, or reducer.
3. Project IDs are strings and never numeric values.
4. Missing, unsupported, not applicable, technical fixture state, and numeric zero
   are different states.
5. The all-37 governed universe remains auditable even though only the locked
   12-record family may enter a P0 Funding Plan.
6. Geometry availability is independent of family membership and plan usability.
7. Historical benchmark fields never enter the core project/evidence catalog or
   plan engine.
8. Release artifacts are immutable, checksummed inputs. Release builds never
   acquire live source data.
9. Client state is untrusted. Both current and reference plan inputs are evaluated
   independently by the backend.
10. Version or identity mismatches fail closed and remain visible.

## Initial Contract Versions

The first implementation uses these semantic identifiers:

| Contract | Initial version |
| --- | --- |
| Release manifest | `p0-release-manifest/1.0.0` |
| Project/evidence catalog | `p0-catalog/1.0.0` |
| Map context GeoJSON | `p0-map-context/1.0.0` |
| Historical benchmark | `p0-benchmark/1.0.0` |
| Funding Plan evaluation | `p0-funding-plan/1.0.0` |
| Browser session | `p0-browser-session/1.0.0` |
| Gemini grounding/response | `p0-gemini-explain/1.0.0` |
| HTTP API namespace | `/api/v1` |

An incompatible field, meaning, enum, or validation change requires a major
contract version. Additive optional metadata requires at least a minor version.
Corrections that do not change consumer behavior require at least a patch version
and a new `data_version` when artifact bytes change.

## Common Primitives

### Project identifier

- JSON type: string.
- Governed P0 format: digits, a literal period, and exactly three fractional
  digits, for example `5789.150`.
- Never parse, sort, compare, or serialize as a float.
- Unknown values fail validation; representational normalization is not a runtime
  lookup strategy.

### Money

- JSON type: integer.
- Unit: United States dollars.
- Minimum scenario budget: `$0`.
- Maximum scenario budget: `$1,000,000,000`.
- These limits are application validation and input-safety bounds only. They are
  not City funding policy, do not define project eligibility, and do not change
  the `$125,000,000` Historical Envelope. The maximum leaves ample headroom above
  the full governed 37-project / `$327,970,000` request universe.
- Scenario budgets and governed requests remain whole-dollar integers. Every
  accepted budget, request, total, remainder, overage, and delta must remain
  exactly representable throughout server and browser arithmetic.
- No cents, currency strings, `NaN`, infinity, negative values, implicit rounding,
  partial-request amount, or client-edited request amount.

Source-form currency text may be preserved as provenance, but authoritative
scenario arithmetic uses only the governed integer-dollar field.

### SHA-256

- JSON type: lowercase 64-character hexadecimal string, without a `sha256:` prefix
  inside checksum-valued contract fields.
- Calculated over exact file bytes.
- Artifact checksums in `manifest.json` cover `catalog.json`,
  `map-context.geojson`, and `benchmark.json`.
- `manifest_sha256` is calculated externally over exact `manifest.json` bytes and
  is never written into that manifest.

### Evidence role

The machine enum follows the Methodology Lock:

| Enum | Required public meaning |
| --- | --- |
| `FACT` | Show as **GOVERNED FACT** for source-governed values or **DERIVED FACT** for documented ClimateCapital derivations; `fact_kind` must distinguish them |
| `CONTEXTUAL_EVIDENCE` | Relevant context only; never benefit, eligibility, need, or priority |
| `RESEARCH_ONLY_EVIDENCE` | Available for caveated display/provenance only; never governed analysis |
| `UNAVAILABLE_UNSUPPORTED` | Missing, unavailable, or unsupported for the claimed use; never imputed or scored |

`fact_kind` is required when `evidence_role=FACT` and is one of
`SOURCE_GOVERNED` or `CLIMATE_CAPITAL_DERIVED`.

### Availability

| Enum | Meaning |
| --- | --- |
| `AVAILABLE` | A value/evidence item exists for its documented use |
| `MISSING` | The approved evidence type exists but has no project-level value or defensible association |
| `UNSUPPORTED` | The claimed metric/use has no governed basis in P0 |
| `NOT_APPLICABLE` | The concept does not apply to the record, with a governed reason |
| `NOT_EVALUATED_FIXTURE` | Technical development-fixture state only; not an analytical claim and forbidden in a release candidate |

Every non-`AVAILABLE` item requires a stable `reason_code` and visible explanation.
A numeric value of zero is permitted only with `availability=AVAILABLE` and source
provenance that establishes zero. It is never inferred from another availability
state.

### Source reference

Every displayed fact or evidence item resolves to one or more immutable source
references containing:

- `source_id` matching an approved release-manifest source ID;
- publisher and title;
- source vintage/published date when known;
- retrieval timestamp for mutable services when applicable;
- exact source checksum;
- pinned GCS URI and generation when applicable;
- historical-fit classification;
- license/reuse status and attribution text;
- known limitations; and
- transformation/join identifier when the displayed field is derived.

## Versioned Release-Data Bundle

The canonical logical layout is:

~~~text
release-data/<data_version>/
├── catalog.json
├── map-context.geojson
├── benchmark.json
└── manifest.json
~~~

File names are fixed. Serialization is deterministic: UTF-8, Unix newlines,
stable key ordering where the producer owns order, no timestamps generated during
the release build, and no non-finite numbers. A data-preparation run may stage
outputs elsewhere, but promotion makes the reviewed bundle immutable.

### Release tier

Every bundle declares one of:

- `FIXTURE`: local/application-development only; may use
  `NOT_EVALUATED_FIXTURE`; must be visibly labeled and must fail release-candidate
  validation.
- `REVIEWED_RELEASE`: pinned sources, completed evidence review, passed
  reconciliations, no fixture states, and eligible for a release build.

The four files use the same `data_version`, contract-version set, and release tier.
Cross-file mismatch fails startup.

## `manifest.json`

The release-data manifest describes data identity and reproducibility only. Its
required content is:

| Field | Contract |
| --- | --- |
| `contract_version` | `p0-release-manifest/1.0.0` initially |
| `data_version` | Immutable human-readable release-data version |
| `release_tier` | `FIXTURE` or `REVIEWED_RELEASE` |
| `contract_versions` | Exact catalog, map, benchmark, plan, session, and Gemini contract versions |
| `approved_source_ids` | Sorted unique list of every source ID permitted in the bundle |
| `sources` | For each approved source: checksum, source identity/vintage, historical fit, and pinned GCS object generation where applicable |
| `transformation_versions` | Exact extractor, join, geometry, classification, and serializer version identifiers |
| `artifacts` | Exact SHA-256 and byte size for `catalog.json`, `map-context.geojson`, and `benchmark.json` |
| `governed_reconciliations` | Counts, unique-ID checks, governed request totals, exact family IDs/count/total, and whole-dollar checks |
| `evidence_coverage_missingness` | Per evidence type/role availability, missing, unsupported, not-applicable, and fixture-state counts, with denominator/scope |
| `benchmark_identity` | Benchmark source ID, published identity/date, extraction version, and artifact identity |

For a source preserved in Cloud Storage, `sources` requires the exact bucket object
path, generation, exact-byte SHA-256, and byte size. A source without a GCS object
uses an explicit `gcs_object: null`; a missing generation must never be silently
interpreted as “latest.”

The governed reconciliations must include at least:

- governed universe: 37 unique project IDs and `$327,970,000`;
- active P0 family: the exact 12 locked IDs and `$143,005,000`;
- governed request values are positive integer dollars;
- all active-family IDs exist in the governed universe;
- citywide project `5789.150` has `NON_PROJECT_GEOGRAPHY` and no map feature;
- catalog/map project-ID coverage agreement without requiring every project to
  have geometry; and
- no benchmark field in the catalog or map artifacts.

The manifest must not contain:

- the Git SHA of a commit that contains the manifest;
- `manifest_sha256` or any checksum of its own bytes;
- container image digest or deployment release ID;
- mutable “latest” source pointers; or
- runtime/session state.

## External Deployment Identity

Deployment identity is generated outside `manifest.json` and contains:

| Field | Source of truth |
| --- | --- |
| `code_git_sha` | Exact source commit used by the build |
| `data_version` | Reviewed manifest and bundle |
| `manifest_sha256` | SHA-256 of final exact `manifest.json` bytes |
| `container_image_digest` | Artifact Registry digest after image push |
| `release_id` | Human-readable composition of immutable code/data/manifest identity; not a substitute for the digest |

The image build receives code/data/manifest identity as labels or files. The image
digest is bound in the Cloud Run revision configuration after push because putting
the digest into its own image would be circular. Release verification compares the
Cloud Run revision's deployed digest and configured identity with `/healthz`.

## `catalog.json`

### Root contract

Required root fields:

- `contract_version`;
- `data_version`;
- `release_tier`;
- `decision_context` with Historical Decision Snapshot and Historical Envelope;
- `governed_universe_summary`;
- `active_family_summary` including exact IDs;
- `source_references` keyed by approved source ID;
- `unsupported_metric_definitions`;
- `projects`, exactly 37 unique records; and
- `methodology_version` identifying the locked analytical specification.

The root contains no Historical City Recommendation membership or amount fields.

### Project record

Each project requires:

| Field | Type and authority |
| --- | --- |
| `project_id` | Governed string ID |
| `governed_name` | Source-governed name |
| `governed_request_dollars` | Source-governed positive integer dollars |
| `governed_request_source_text` | Source-form currency text for provenance |
| `source_row` | Source ID, page/order/map label, and Council-district source text |
| `purpose` | Derived purpose, `fact_kind=CLIMATE_CAPITAL_DERIVED`, confidence, evidence, ambiguity, and transformation version |
| `p0_family` | Boolean membership, rationale, and explicit statement that it is not City eligibility |
| `geography_status` | `DISPLAY_GEOMETRY_AVAILABLE`, `DISPLAY_GEOMETRY_MISSING`, or `NON_PROJECT_GEOGRAPHY` |
| `program_scope` | `DISCRETE_PROJECT` or `CITYWIDE_PROGRAM` |
| `evidence` | Typed evidence items described below |
| `provenance_refs` | References resolvable through root source metadata |

`5789.150` must have `program_scope=CITYWIDE_PROGRAM` and
`geography_status=NON_PROJECT_GEOGRAPHY`.

For a `FIXTURE`, `geography_status=DISPLAY_GEOMETRY_MISSING` may pair with RNA
evidence availability `NOT_EVALUATED_FIXTURE` when display-geometry curation has
not been completed. This says only that the fixture has not materialized the
display feature; it must not overwrite known source-match coverage with a
project-level `MISSING` claim. A reviewed release must resolve the evidence state
and still rejects every `NOT_EVALUATED_FIXTURE` value.

### Evidence item

Every evidence item requires:

- stable `evidence_id` and evidence type;
- `evidence_role` and, for facts, `fact_kind`;
- `availability` plus `reason_code` when not available;
- value plus unit/category only when available;
- source reference(s), source vintage, and historical fit;
- association/join method and transformation version when derived;
- coverage scope and limitations;
- confidence only for classification, association, or linkage strength, never
  need/priority; and
- public label/disclaimer text.

Required P0 evidence types include governed request/project identity, derived
purpose/family, Problem Score association context, current RNA display geometry
availability, current FEMA hazard context where defensible, EAZ 2021 context where
defensible, and explicit unsupported definitions for expected flood-reduction
benefit and ungoverned beneficiary estimates.

### Forbidden catalog fields

Schema and semantic scans reject fields or aliases representing:

- Funding Priority or project rank;
- Climate Risk, Community Vulnerability, Community Equity, or synthetic need score;
- Importance weights or an objective weight;
- optimizer membership, recommendation, objective value, tie-break, or preferred
  combination;
- expected flood-reduction benefit;
- imputed evidence, missingness penalty, or confidence-as-need;
- editable/partial request amount; and
- Historical City Recommendation inclusion/treatment or benchmark-derived
  evidence.

## `map-context.geojson`

The root is a GeoJSON `FeatureCollection` with these foreign members:

- `contract_version`;
- `data_version`;
- `release_tier`;
- `crs_contract` fixed to RFC 7946 WGS84 longitude/latitude output;
- `source_crs_and_transformations` preserving source CRS, transformation tool and
  version, validation, and limitations;
- `layer_definitions`; and
- standard `features`.

Permitted P0 `layer_id` values and defaults are:

| Layer | Role | Default | Contract |
| --- | --- | --- | --- |
| `rna_current_project_display` | `RESEARCH_ONLY_EVIDENCE` | Visible where geometry exists | Current display geometry; caveat required |
| `fema_current_hazard_context` | `CONTEXTUAL_EVIDENCE` | Off | User-enabled through Layers; no benefit inference |
| `eaz_2021_context` | `CONTEXTUAL_EVIDENCE` | Off | User-enabled through Layers; dated location context only |

Fully Developed FloodPro is forbidden in the P0 map artifact.

Every feature requires stable feature/source identity, `layer_id`, evidence role,
availability, source/vintage/historical-fit metadata, transformation version,
limitations, and geometry. RNA display features require exactly one governed
`project_id`. FEMA/EAZ context features may omit a project ID and must not claim
project beneficiaries or project benefit.

Do not create null-geometry placeholder features. Project geometry missingness and
citywide-program treatment live in `catalog.json`. No feature may use
`project_id=5789.150`.

## `benchmark.json`

This artifact has a separate schema and source path. Required root fields:

- `contract_version`, `data_version`, and `release_tier`;
- `benchmark_identity` identifying the January 2026 Historical City
  Recommendation and source snapshot;
- `source_references` containing benchmark-only provenance;
- published portfolio/allocation summary with explicit availability;
- published project treatment entries using City-specific terms;
- published amount/treatment fields with units and availability;
- extraction/transformation version and limitations; and
- reconciliation results against the publication.

Benchmark entries may refer to governed project IDs for supported overlap only.
They must not include or modify project evidence, P0-family membership, plan
membership, governed request amounts, or plan arithmetic. Published City amounts
remain published benchmark values even when they differ from full governed
requests.

## Fixture-Bundle Contract

A fixture bundle exists only to parallelize application work after schema lock.
It conforms to the exact same file and field schemas, with
`release_tier=FIXTURE`.

- Use already governed facts and locked methodology facts where possible.
- Never fabricate a project location, contextual association, score, beneficiary,
  benchmark treatment, or analytical claim.
- When evidence curation is not complete, use `NOT_EVALUATED_FIXTURE` as a
  technical state with no value; do not relabel it missing, low, or zero.
- Make fixture mode unmistakable in bootstrap configuration and UI chrome.
- Release validation rejects `FIXTURE`, any `NOT_EVALUATED_FIXTURE`, missing
  reviewed source pins, or placeholder benchmark identity.

Final integration must replace the fixture bytes with the reviewed pinned release
bundle. A release candidate cannot ship fixture evidence even if all application
tests pass.

## Deterministic Funding Plan Contract

### Input

A plan input contains exactly:

~~~json
{
  "contract_version": "p0-funding-plan/1.0.0",
  "data_version": "<expected-data-version>",
  "available_budget_dollars": 125000000,
  "project_ids": ["5789.075", "5789.107"],
  "expected_fingerprint": "<optional-lowercase-sha256>"
}
~~~

No request amount, total, remainder, score, evidence value, rank, delta, or result
field is accepted as input.

### Validation

The server validates each input independently:

1. contract and expected data version match runtime identity;
2. budget is a whole-dollar integer inside the documented bound;
3. project IDs are strings in governed format;
4. no duplicate project ID appears;
5. every ID exists in the all-37 catalog;
6. every ID belongs to the active 12-record family;
7. request amounts are resolved only from `catalog.json`;
8. each project contributes its complete governed request; and
9. confirmation eligibility requires included total not greater than budget.

An empty `project_ids` list is valid and produces a zero-project evaluated plan.
Unknown, duplicate, and out-of-family IDs are different typed errors. An
over-budget input may return its exact evaluated overage for correction, but is
not confirmable.

### Output

The server returns:

- contract/data version;
- canonical included IDs and not-included active-family IDs;
- included count;
- included governed request entries;
- exact included total;
- Available Budget;
- exact remainder when within budget or exact overage when over budget;
- `confirmation_status` of `VALID` or `OVER_BUDGET`;
- warnings limited to governed evidence/geometry availability context, never a
  membership recommendation; and
- server-computed plan fingerprint.

### Canonical fingerprint

The plan fingerprint is SHA-256 over a versioned canonical UTF-8 representation of:

- Funding Plan contract version;
- runtime `data_version`;
- whole-dollar Available Budget; and
- unique included project IDs sorted lexically by canonical string.

It excludes totals, project costs, evidence, labels, session name, confirmation
time, and benchmark data because the server deterministically derives them. An
expected-fingerprint mismatch is returned visibly and prevents silent restoration
of confirmed/reviewed state. The server result remains authoritative.

### Current/reference comparison

`POST /api/v1/plans/evaluate` accepts:

~~~json
{
  "current": {
    "contract_version": "p0-funding-plan/1.0.0",
    "data_version": "<expected-data-version>",
    "available_budget_dollars": 125000000,
    "project_ids": ["5789.075", "5789.107"],
    "expected_fingerprint": null
  },
  "reference": {
    "contract_version": "p0-funding-plan/1.0.0",
    "data_version": "<expected-data-version>",
    "available_budget_dollars": 125000000,
    "project_ids": ["5789.075"],
    "expected_fingerprint": "<optional-lowercase-sha256>"
  }
}
~~~

`reference` is optional; every field inside a supplied plan input follows the
exact input contract. The backend calls the same evaluator separately for
`current` and `reference`. It never accepts an evaluated reference result from the
client.

If both inputs are valid, supported comparison contains only:

- budget difference;
- included-total difference;
- remainder difference;
- included-count difference;
- IDs entering, leaving, and unchanged; and
- governed request-dollar sums associated with entering/leaving IDs.

Evidence coverage/context may be summarized transparently but not converted to a
numeric delta, score, benefit, or preference. No comparison is returned as
confirmable if either plan is invalid/over-budget.

## Historical Benchmark Comparison Contract

`POST /api/v1/benchmark/compare` accepts one complete untrusted plan input plus the
expected benchmark/data identity. The backend re-evaluates the plan from the core
catalog, then passes only that fresh result to the benchmark comparator.

Permitted output is published City allocation/treatment, City-included count where
supported, overlap IDs/count/dollars where semantics support the calculation, and
documented divergences. It uses City-specific language and never infers City
reasoning or treats the benchmark as truth. No benchmark output is accepted by or
returned from the plan engine.

## HTTP API Contracts

### General rules

- JSON UTF-8, same-origin HTTPS, explicit media type, no permissive unknown fields.
- Request body and string/list limits are enforced before expensive work.
- Every response includes `request_id`, `contract_version` where applicable,
  `data_version`, and `release_id`.
- Typed errors use a stable `error_code`, safe human message, affected field/path,
  retryability, and request ID. They never expose a stack trace, prompt, source
  bytes, filesystem path, credential, or raw provider response.

HTTP behavior is fixed:

- `200` for successfully parsed endpoint envelopes, including plan-side statuses
  `VALID`, `OVER_BUDGET`, or `INVALID` with typed semantic errors;
- `404` for an unknown route only, not for an unknown project ID inside a plan;
- `409` for request/runtime contract or data-version conflict;
- `413` for a body that exceeds the server limit;
- `422` for malformed JSON, unknown input fields, invalid primitive types, or a
  shape that cannot be evaluated;
- `429` for a Gemini rate limit;
- `503` for disabled/unavailable Gemini or another local optional dependency; and
- `500` for an unexpected server failure with a safe request-correlated response.

Plan comparison is present only when both independently evaluated sides are
`VALID`. An invalid reference never prevents the response from preserving the
fresh current-side evaluation.

### `GET /healthz`

Returns success only after the application has loaded and validated the reviewed
bundle. It does not contact Gemini, BigQuery, Cloud Storage, OSM, or source
services.

Required identity fields:

- `status`;
- `code_git_sha`;
- `data_version`;
- `manifest_sha256`;
- `container_image_digest`;
- `release_id`;
- relevant contract versions; and
- `gemini_enabled` without exposing configuration secrets.

Fixture tier is acceptable only in local/test health responses. A deployed release
candidate must report `REVIEWED_RELEASE`.

### `GET /api/v1/bootstrap`

Returns the catalog, map context, map default visibility, evidence/source metadata,
Historical Envelope context, active-family summary, fixture/release mode, public
configuration, and deployment identity. It contains no Historical City
Recommendation treatment.

The response may use strong ETag/cache validation keyed by data/release identity.
The client must invalidate restored confirmed state when identity changes.

### `GET /api/v1/benchmark`

Returns only the separately loaded benchmark artifact, its source identity,
limitations, and deployment/data identity. Failure is local and does not affect
bootstrap or Funding Plan evaluation.

### `POST /api/v1/plans/evaluate`

Uses the deterministic current/reference contract above. The endpoint is
stateless. The browser must call it before confirming, restoring, comparing, or
marking a plan reviewed.

### `POST /api/v1/benchmark/compare`

Uses the benchmark comparison contract above. The server does not accept
client-computed plan results.

### `POST /api/v1/gemini/explain`

Required request fields:

- Gemini contract/data version;
- `context_type`: `PROJECT`, `PLAN`, `SCENARIO_COMPARISON`, `BENCHMARK`,
  `METHODOLOGY`, or `PROVENANCE`;
- bounded context references such as project IDs or the relevant current/reference
  plan inputs;
- bounded user question; and
- optional expected fingerprints for verification.

The server resolves project evidence itself, independently evaluates supplied plan
inputs, and selects benchmark data only for `BENCHMARK` context. The client cannot
submit grounding facts, totals, evidence values, or free-form system instructions.

Successful output is a structured explanation with sanitized visible text,
validated source/evidence citations, explicit limitations, model identity, and
usage counts when the provider reports them. Visible output is capped at 400
tokens. Unsupported or unsafe questions return a bounded refusal. A disabled,
rate-limited, timed-out, or invalid model response is a local typed error and never
changes deterministic state.

### `POST /api/v1/gemini/propose` — post-core stretch

This endpoint is absent or disabled in the core release candidate. If implemented,
it accepts only a bounded explicit analyst command plus the current untrusted plan
input. Output is one pending structured action limited to a whole-dollar budget
change or named project add/remove operation. It changes no state. After explicit
analyst confirmation, the browser submits the resulting budget and IDs to the
normal plan evaluation endpoint.

The proposal endpoint cannot return request amounts, authoritative totals,
membership recommendations, scores, evidence values, or applied state.

## Browser Session Contract

The SPA reducer separates authoritative server results from untrusted/pending
inputs. The top-level `sessionStorage` object uses
`p0-browser-session/1.0.0` and contains:

- deployment/data identity last validated;
- presentation state: route, search/filter/sort, map extent, visible layers,
  selected project, and list position;
- unconfirmed working plan input;
- immutable Session Reference Plan input, last server result, and fingerprint;
- optional What-If input, last server result, fingerprint, and confirmation state;
- Current Confirmed Plan pointer (`REFERENCE` or `WHAT_IF`);
- dirty/unapplied attempted input and typed validation state;
- optional pending Gemini proposal, never applied state;
- Reviewed Draft binding to exactly one confirmed fingerprint;
- local request/loading/error states; and
- no prompt/response history beyond the current visible explanation if the UI
  retains it for the tab session.

The client may cache server result fields for rendering but never treats them as
authoritative after restoration. On load it submits the stored budget and IDs for
fresh evaluation and verifies data version/fingerprint before restoring confirmed
or Reviewed Draft indicators.

### State invariants

- Session Reference Plan is created once and then immutable for the session.
- At most one What-If exists.
- Current Confirmed Plan points only to a freshly validated confirmed result.
- Dirty/unapplied input never changes the header or last confirmed result.
- Invalid, over-budget, timeout, benchmark, tile, or Gemini failures preserve the
  last successful deterministic result.
- Replacing a reviewed What-If warns and clears its Reviewed Draft binding only
  after confirmed replacement.
- Presentation filters/layers never change family or plan membership.
- Closing Project Detail preserves Explore presentation state.
- `5789.150` is available in list/detail/plan but cannot create a selected map
  feature.
- A valid zero-project plan is a successful result, not an empty/error state.

No session cookie, user ID, server session key, durable scenario ID, or database
record is created.

## Gemini Grounding Contract

The server-built grounding package is allowlisted by context and contains only the
minimum required:

- deployment/data/contract identity;
- public methodology constraints and terminology;
- selected governed project facts and explicit evidence states/provenance;
- freshly evaluated plan results and supported differences;
- separately selected benchmark facts only for benchmark context; and
- the bounded user question.

The constructed input starts with an approximately 2,000-token application limit.
Increasing it toward 3,000 requires recorded test evidence. `thinking_level` is
`MINIMAL`; visible output targets about 350 tokens and may not exceed 400.

Post-validation requires:

- response matches the structured schema;
- cited evidence/source IDs exist in the supplied grounding;
- numeric claims are either exact strings from deterministic grounding or omitted;
- no project recommendation, rank, score, benefit, beneficiary, invented evidence,
  or missing-as-zero claim;
- no mutation/action in an explanation response; and
- safe text rendering.

A failed check discards the answer and returns a bounded unavailable/invalid-answer
state. It never falls back to an unvalidated model or text-only response.

## Configuration Contract

Validated non-secret runtime configuration includes:

- `GEMINI_ENABLED`;
- Gemini model fixed initially to `gemini-3.6-flash`;
- publisher endpoint/location fixed to global standard on-demand access;
- input/output/thinking/rate/concurrency/retry limits;
- `DATA_VERSION`, `MANIFEST_SHA256`, `CODE_GIT_SHA`,
  `CONTAINER_IMAGE_DIGEST`, and `RELEASE_ID`;
- OSM/configurable tile URL and exact attribution string; and
- environment label.

Production refuses missing identity values, invalid bounds, unknown model/location,
fixture release tier, or disagreement with manifest data version. ADC/workload
identity is the only model credential path; no API key variable exists.

## Validation and Release Gates

A `REVIEWED_RELEASE` bundle is accepted only if:

- all four files pass their exact schema and version contracts;
- artifact SHA-256/byte sizes match the manifest;
- external `manifest_sha256` matches the exact manifest bytes;
- every approved source ID is registered and every artifact source reference is
  approved;
- pinned GCS generations/checksums match where applicable;
- governed and family reconciliations pass exactly;
- evidence coverage/missingness totals reconcile by declared denominator;
- no `NOT_EVALUATED_FIXTURE` or fixture marker exists;
- the citywide/no-feature invariant passes;
- only approved map layers exist with locked defaults;
- benchmark identity and isolated-field scans pass;
- forbidden scoring/ranking/weights/optimizer/benefit/imputation fields are absent;
  and
- release build and runtime identity reconcile with the Cloud Run revision and
  immutable image digest.

Any failure blocks release construction or traffic promotion. It is never reduced
to a warning for deadline convenience.

## Change Control

Contract changes require a sequential decision in
[decisions.md](../decisions.md), version impact analysis for every producer and
consumer, fixture and reviewed-bundle migration, and fresh contract/release tests.
No API, artifact, or client migration may weaken the locked methodology or plan
trust boundary.
