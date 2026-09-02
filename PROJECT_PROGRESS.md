# ClimateCapitalAI Project Progress

> **Canonical role:** Current state, stage, progress, blockers, active risks, open
> questions, milestones, and cross-task handoff. Detailed specifications and
> decision history live in the linked authoritative documents below.

## How to Maintain This File

At the start of every task:

1. Read this file completely.
2. Reconcile it with the repository; repository state wins if they differ.
3. Read the authoritative documents listed for the active task.
4. Begin with the first unblocked item in **Next Actions** unless the user changes
   priority.

At the end of every task:

1. Update the current snapshot, workstream, next actions, milestones, blockers,
   active risks, open questions, verification record, technical map, and session
   log wherever the task changed them.
2. Keep the session log newest-first and preserve historical entries.
3. Record detailed durable decisions in
   [docs/decisions.md](docs/decisions.md) using the next sequential ID.
4. Update a purpose-specific specification only when an approved change
   legitimately affects it; do not duplicate the same detail here.

Never record secrets, credentials, tokens, or sensitive personal data. Do not
create docs/delivery/progress.md; this file is the only progress/status tracker.

## Source-of-Truth Map

| Subject | Authoritative source |
| --- | --- |
| Repository working rules and task startup | [AGENTS.md](AGENTS.md) |
| Current state, progress, blockers, risks, and handoff | This file |
| Locked P0 evidence roles, analytical family, missingness, and deterministic Funding Plan method | [docs/methodology/p0-evidence-methodology.md](docs/methodology/p0-evidence-methodology.md) |
| Product vision, scope, principles, workflow, and non-goals | [docs/product/product-plan.md](docs/product/product-plan.md) |
| Prioritized stories and acceptance intent | [docs/product/user-stories.md](docs/product/user-stories.md) |
| Screens, navigation, UI behavior, states, recovery, and wireframes | [docs/product/screen-spec.md](docs/product/screen-spec.md) |
| Initial delivery sequencing, deadline, and release gates | [docs/delivery/execution-plan.md](docs/delivery/execution-plan.md) |
| Durable decision history | [docs/decisions.md](docs/decisions.md) |
| Architecture-planning reference; not an approved design | [docs/reference/technical-architecture-reference.md](docs/reference/technical-architecture-reference.md) |
| Approved architecture after explicit Architecture Lock | docs/architecture/ — intentionally absent |
| Architecture-informed implementation and test plans | docs/delivery/implementation-plan.md, test-plan.md, and milestones.md — intentionally absent |

Git is the version history for all repository memory. Fresh tasks must not depend on
access to prior chat conversations.

## Current Snapshot

- **Last updated:** 2026-09-01
- **Project stage:** Methodology Lock is complete and reviewed. Product and Design
  have been reconciled with the evidence result. Architecture Planning remains
  paused before Architecture Lock until separately authorized; this is not
  application implementation.
- **Current milestone:** Final P0 evidence and methodology lock: evidence-first
  funding decision support, one derived 12-record local
  flood/local drainage family, no synthetic priority model, and analyst-controlled
  full-request scenarios with deterministic budget arithmetic.
- **Next milestone:** After separate authorization, resume Architecture
  Planning against the locked methodology and reconciled Product/Design documents.
- **Working state:** Git repository on main, connected to the public
  swethabarla19/ClimateCapitalAI GitHub repository, with documentation, the source
  registry/fetch foundation, one pinned data-extraction dependency, a fail-closed
  Watershed table extractor, a Git-tracked 37-record source-universe CSV, one
  pinned BigQuery client dependency, a create-only raw loader, durable SQL quality
  checks, focused validation tests, a native ArcGIS acquisition/matching workflow,
  and Git-tracked snapshot provenance and match artifacts. The raw PDFs and GIS
  responses remain ignored locally and are preserved at exact generation-verified
  Cloud Storage paths; the source-universe CSV remains in one validated `raw`
  BigQuery table. The repository now also contains one authoritative P0 methodology
  document and reconciled Product/Design handoff documents. No production
  pipeline, application, approved architecture, score, rank, weight model, or
  optimizer exists.
- **Most recent outcome:** Closed evidence feasibility without manufacturing a
  common severity/benefit model. The governed universe remains 37 projects /
  $327,970,000; the 24-project / $233,380,000 broad flood-related family is not
  coherent under one method; the provisional P0 analytical family is 12 local
  flood/local drainage records / $143,005,000. Problem Score and FEMA are
  contextual, RNA and Fully Developed FloodPro are research-only for governed
  analysis, expected flood-reduction benefit is unsupported, and EAZ 2021 is
  contextual for only 5/12 projects. Product decisions that assumed scores,
  weights, ranking, or optimizer-authoritative membership were explicitly reopened.

## Approved Locks

- **Stage 1 — Deadline and success:** Official deadline September 7, 2026 at
  10:00 a.m. CDT; internal submit window September 6 from 9:30–11:30 a.m. CDT;
  finalist-worthy deployed/tested P0; three-minute core demo expandable to five.
- **Stage 2 — Product definition:** Capital planning analyst persona, Austin
  Watershed historical simulation, January 2026 context, $125 million Projects
  sub-envelope, full-request treatment, and strict City benchmark isolation remain.
  The former rule-derived cohort, score/rank, weight, and optimizer implications
  are superseded by Methodology Lock.
- **Stage 3 — Backlog:** Twelve required P0 stories, conditional SP0-1 Compare as
  the first cut, ordered P1, Later scope, acceptance intent, and release gates.
- **Stage 4 — Product and Design Lock:** Required screens and contextual surfaces,
  navigation, UI states/recovery, low-fidelity wireframes, evidence gates, and
  three-minute demo sequence remain, reconciled to analyst-controlled Funding Plan
  membership and evidence-first terminology.
- **Methodology Lock — Evidence-first P0:** All 37 source records remain governed;
  the all-37 purpose classification and provisional 12-record / $143,005,000
  analytical family
  are explicit ClimateCapital derivations; evidence roles and missingness are
  governed; P0 has no Funding Priority score, rank, Importance weights, quantitative
  risk/equity score, expected flood-reduction benefit, or optimizer.

Unchanged portions of Stages 1–4 remain authoritative. The empirical evidence gate
materially contradicted and reopened the optimizer-authoritative assumptions; the
historical record and exact replacements are preserved in docs/decisions.md. Full
current detail is in docs/methodology and docs/product.

The evidence-driven reopening does not change ClimateCapital AI, the Austin
Watershed P0 pilot, January 21, 2026 context, Map → Projects → Funding Plan journey,
full-request treatment, benchmark isolation, current-session plan limit,
Reviewed Draft, accessibility, or recovery behavior. It narrows deterministic
authority to facts, evidence states, validation, arithmetic, and supported
comparison; the $125 million figure is historical/default context, not eligibility.

## Current Workstream

- **Goal:** Preserve the locked P0 evidence-first methodology and its explicit
  reconciliation of earlier Product/Design assumptions for the Architecture handoff.
- **Status:** The final evidence-feasibility gate and documentation reconciliation
  are complete and reviewed. The work establishes a
  derived purpose family, not City eligibility, and makes no score, rank, weight,
  optimization, application, architecture, or cloud change.
- **Owner:** User and Codex.
- **Required reading:** AGENTS.md, this file,
  docs/methodology/p0-evidence-methodology.md, the reconciled files under
  docs/product, docs/delivery/execution-plan.md, docs/decisions.md, and the
  non-authoritative docs/reference/technical-architecture-reference.md.
- **Exit condition:** Achieved. Architecture Planning may resume only in a later
  authorized task; approved architecture files still require explicit Architecture
  Lock.

## Next Actions

1. Do not perform another broad source hunt, inspect SVI, manufacture project
   geography, or reintroduce expected benefit, scores, ranks, weights, or an
   optimization objective without a later explicit methodology revision.
2. After separate authorization, resume Architecture Planning using
   the reconciled handoff; design only the smallest contracts needed for governed
   facts/evidence states, analyst membership, validation, integer-dollar arithmetic,
   supported comparison, and bounded Gemini interaction.
3. After explicit Architecture Lock, create the architecture-informed
   implementation, test, and milestone plans before application implementation.
4. Separately verify organizer submission artifacts, judging criteria, finale
   date, and conditional live-demo format.

## Completed Milestones

- **2026-09-01 — P0 Methodology Lock completed and reviewed:** Closed the final
  evidence-feasibility gate; preserved the 37-project governed universe and derived
  all-37 purpose audit; locked the 12-record local flood/local drainage family;
  classified Problem Score, RNA/FloodPro, expected benefit, and EAZ evidence by
  role and historical fit; removed unsupported scores/weights/ranking/optimization;
  and reconciled Product/Design to analyst-controlled scenarios and deterministic
  budget arithmetic without application, architecture, cloud, or push changes.
- **2026-09-01 — Live RNA layer-8 geometry reconnaissance completed:** Preserved a
  stable 577-feature native ArcGIS JSON snapshot with exact-byte and semantic
  fingerprints, exact numeric-token ID handling, native CRS/geometry audit, and
  create-only generation-verified GCS storage; tested all 37 governed IDs and
  retained 15 single matches, 22 zero matches, and no multiple matches without
  inferring historical validity, eligibility, exposure, or benefit.
- **2026-08-31 — Raw BigQuery ingestion and quality checkpoint completed:**
  Reviewed and hardened the manual loader without replacing its core approach;
  verified the existing `us-central1` table's exact schema and 37 rows; passed 21
  independent SQL checks including $327,970,000, full source sequence, row-level
  spot checks, and an ordered semantic fingerprint; changed no existing cloud
  data, dataset configuration, IAM, architecture, methodology, or benchmark state.
- **2026-08-31 — Official 37-project source universe extracted:** Added a pinned
  data-only PDF parser, checksum-gated fail-closed extractor, deterministic tracked
  CSV, and source-verified tests; reconciled 37 unique records and $327,970,000
  across row amounts, the table total, and memorandum request; preserved source
  order and made no eligibility, GIS, analytical, benchmark, or cloud change.
- **2026-08-31 — Two raw source snapshots preserved in Cloud Storage:** Confirmed
  local and registry checksums, authenticated project/bucket access, absence of both
  destination objects, and create-only upload support; uploaded exactly two PDFs;
  verified sizes, generations, and generation-specific streamed SHA-256 values;
  changed no infrastructure, IAM, bucket settings, credentials, BigQuery, or
  analytical state.
- **2026-08-31 — Minimal source-ingestion foundation implemented:** Added the
  canonical source registry, deterministic immutable local fetcher, Git protections,
  and validation tests; downloaded and independently reconciled both authoritative
  PDFs; performed no extraction, upload, BigQuery work, cloud provisioning,
  architecture, methodology, or application work.
- **2026-08-31 — Architecture Lock paused for evidence reconnaissance:** Preserved
  the approved product/design boundary, identified evidence comparability as an
  Architecture dependency, and established the 37-project authoritative-source
  reconnaissance sequence before Architecture Planning resumes.
- **2026-08-27 — Documentation architecture normalized:** Created authoritative
  product, story, screen, delivery, and decision documents plus a clearly
  non-authoritative technical reference; reduced this tracker to current status and
  pointers; added fresh-task reading rules.
- **2026-08-26 — Stage 4 Product and Design Lock approved:** Locked screen
  inventory, navigation, contextual surfaces, screen requirements, important
  states/recovery, wireframes, demo sequence, assumptions, dependencies, and risks.
- **2026-08-26 — Stage 3 backlog approved:** Locked 12 required P0 stories,
  conditional SP0-1, P1/Later, acceptance intent, terminology, and scope boundaries.
- **2026-08-25 — Deadline plan approved:** Protected an August 27 Product and
  Design Lock, September 2 feature freeze, testing, and submission contingency.
- **2026-08-25 — Stage 1 and Stage 2 checkpoint published:** Connected the public
  GitHub repository and published the approved product-context baseline.
- **2026-08-25 — Stage 2 product definition locked:** Locked the user, problem,
  value, historical context, scope, scenario terminology, and analytical
  boundaries.
- **2026-08-24 — Stage 1 deadline and success baseline approved:** Locked deadline,
  capacity, audience assumption, demo target, and success bar.
- **2026-08-24 — Cross-session continuity initialized:** Added repository guidance
  and a canonical progress tracker.

## Delivery Checkpoints

The detailed plan and sequencing rationale are authoritative in
[docs/delivery/execution-plan.md](docs/delivery/execution-plan.md).

- **Sep 2:** Required-P0 feature freeze.
- **Sep 3:** Public release candidate.
- **Sep 4:** Quality and three-minute demo gates.
- **Sep 5:** Final freeze.
- **Sep 6:** Internal submission and link verification.
- **Sep 7, 10:00 a.m. CDT:** Official deadline.

A missed gate cuts or freezes scope; it does not consume testing/submission
contingency. Conditional SP0-1 Compare is the first cut. P1 cannot begin early
unless required P0 is at least 24 hours ahead and 10 contingency hours remain.

The August 31 analytics-core checkpoint is not authorized while Architecture Lock
is paused. The September 2 required-P0 feature-freeze gate is therefore at critical
schedule risk; this status update does not revise the approved deadline or silently
authorize implementation.

## Blockers

- Architecture Planning remains paused until separately authorized. The reviewed
  Methodology Lock and Product/Design reconciliation are complete, and evidence
  feasibility is no longer an open Architecture dependency.
- No architecture is approved; this blocks architecture implementation, production
  data pipelines, application implementation, and final architecture documents.
- Architecture-informed implementation, test, and milestone plans do not yet
  exist, so implementation remains unauthorized after review alone.
- Official judging criteria, submission artifacts, and conditional live-demo
  details remain unconfirmed and block final submission-package planning.

## Active Risks

- Source-license/reuse terms remain unverified and are recorded as such in the
  source registry.
- RNA Projects layer 8 and the current FloodPro services do not establish their
  January 2026 geometry/data state. RNA geometry is research-only for governed
  analysis; FEMA is current contextual hazard evidence only.
- Twenty-two of the 37 governed projects, including 7/12 local-drainage family
  records, have no exact ID geometry match in the captured live RNA snapshot.
  Missing geometry is not evidence of low need and does not remove a family record.
- Three of the 15 exact-ID GIS matches have non-identical project names. Names were
  retained as evidence but did not affect matching; project identity still needs
  source-specific review wherever later analytical use is contemplated.
- Layer-8 features are source polygons in ESRI:102739/EPSG:2277. The acquisition
  preserves them without transformation, simplification, curve densification, or
  repair, and polygon semantics have not been validated as project footprints or
  benefit areas.
- Fully Developed FloodPro contains relevant invalid source geometries and remains
  research/context only; repaired geometry must not become governed source truth.
- Problem Score project/problem association strength is provenance, not severity,
  and no reproducible January 2026 Local Flood numeric score covers the family.
- EAZ 2021 is a 2019-ACS-based Austin Transportation vulnerability snapshot with
  defensible project-level location context for only 5/12 family records. It is not
  current-2026 vulnerability or a project-beneficiary measure.
- Project 5789.150 is a citywide renewal program. Treating it like one discrete
  footprint would create false location, hazard, vulnerability, or beneficiary
  precision.
- BigQuery does not enforce project-ID uniqueness, source sequence, totals, or the
  semantic fingerprint as table constraints. The loader refuses an existing table,
  but any separately authorized mutation by another tool or user requires rerunning
  the durable SQL quality suite before the raw snapshot is trusted.
- The local Python 3.12 installation has no default CA bundle configured; verified
  HTTPS succeeded only when `SSL_CERT_FILE=/etc/ssl/cert.pem` selected the host CA
  bundle. Certificate verification was not disabled.
- Comparable project-level expected flood-reduction evidence is unsupported for
  P0; project/floodplain intersection cannot substitute for benefit evidence.
- Project identifiers, geometry, engineering evidence, hazard evidence, exposure,
  and equity joins may be inconsistent across sources or valid only for different
  historical vintages.
- The source says projects are sorted by project ID, but published row order places
  5789.150 before 5789.145 and 5789.146. Extraction preserves rather than repairs
  this source-level inconsistency.
- The current delivery baseline is at critical schedule risk because no
  Architecture Lock, application, production pipeline, or implementation plan
  exists as of September 1.
- Required P0 remains ambitious for the September 2 feature freeze; optional scope
  must not erode testing or recovery time.
- Architecture work is now on the critical path and must implement the locked
  narrow method without reopening evidence reconnaissance.
- Product language or contracts could silently reintroduce a Funding Priority,
  ranking, Importance weights, optimizer, recommendation, or missing-evidence
  penalty even though no defensible objective supports them.
- Analyst-controlled membership could be misrepresented as a ClimateCapital or
  City recommendation; provenance and confirmation labels must remain explicit.
- The Historical Decision Snapshot, Historical Envelope, Historical City
  Recommendation, Current Confirmed Plan, and Session Reference Plan may be
  confused if the locked terminology is not implemented consistently.
- Gemini or map work could consume disproportionate effort; deterministic/manual
  paths and non-map access remain release priorities.
- Failed recalculation must not overwrite the last successful deterministic result.
- The process-job Stop hook still exits with code 127 because node is unavailable;
  process-job completion checks remain unreliable until its runtime/configuration is
  fixed.
- Current cloud pricing, quotas, program requirements, and source licensing have not
  been verified.

## Open Questions

### Evidence and methodology

- No evidence or methodology decision remains open for P0. Source licensing/reuse
  remains unverified operational metadata, not a reason to broaden reconnaissance.
- Any later metric proposal requires an explicit methodology revision documenting
  source, vintage, historical fit, coverage, comparability, missingness,
  transformation, and effect; it is not part of the current handoff.
- Architecture/Product presentation must still decide which contextual or
  research-only map layers, if any, are visible by default without changing their
  locked analytical roles.

### Architecture

- What is the smallest low-cost deployable system that satisfies required P0?
- Which work is precomputed versus performed at runtime?
- What governed contracts preserve all-37 source facts, the derived 12-record
  family, evidence roles/missingness, analyst membership, integer-dollar arithmetic,
  Historical Benchmark isolation, and Gemini boundaries?
- Which Google Cloud, Gemini, frontend, map, storage, and deployment options meet
  deadline, cost, security, and reliability constraints?
- What data-versioning, lineage, observability, and teardown approach is required?

### Submission

- What are the official submission artifacts, judging criteria, finale date, and
  live-demo format?

There are no unresolved P0 scoring, weighting, ranking, optimization, or evidence-
imputation decisions. Existing Stage 4 screen/navigation structure remains locked;
its evidence-driven terminology and Funding Plan behavior are reconciled in
docs/product.

## Technical Map

### Architecture

Not established. Architecture Planning is paused before lock until separately
authorized. The technical reference has been reconciled as a handoff but remains
exploratory and does not constitute an Architecture Lock.

### Evidence Repository

The minimal foundation is established:

- data/metadata/source_registry.csv — canonical Git-tracked source metadata for
  two authoritative PDFs and one live/current research-only GIS source, with
  roles, historical-fit caveats, retrieval timestamps, and exact-byte SHA-256
  checksums. The GIS source's January 2026 fit remains uncertain.
- scripts/data/fetch_sources.py — standard-library HTTPS fetcher with deterministic
  paths, PDF-byte validation, exact-byte persistence, and overwrite refusal.
- tests/test_source_ingestion.py — registry, checksum, HTTPS, metadata-update, and
  immutable-snapshot validation.
- requirements-data.txt — pinned local data-tool dependency declaration containing
  only pypdf 6.16.2.
- scripts/data/extract_watershed_projects.py — checksum-gated fail-closed extractor
  for the November named-project table; it records 1-based physical PDF pages,
  preserves published source order and strings, reconciles totals, and refuses
  differing-artifact overwrite.
- data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv —
  Git-tracked nine-column, 37-record official source universe; presence in this
  artifact does not establish analytical eligibility.
- tests/test_watershed_project_extraction.py — source-verified row-association,
  boundary, anomaly, schema, reconciliation, failure-path, and deterministic-output
  validation.
- requirements-cloud.txt — pinned local BigQuery client declaration containing
  only google-cloud-bigquery 3.44.0.
- scripts/data/load_watershed_projects_bigquery.py — exact-artifact and CSV-contract
  preflight plus explicit-schema, `us-central1`, `WRITE_EMPTY` raw loader; it
  refuses an existing target and validates schema/location/count after creation.
- tests/test_watershed_bigquery_loader.py — non-destructive local checks for target,
  schema, encoding, header, artifact checksum, location, overwrite refusal, and
  post-load metadata validation.
- sql/quality/watershed_projects_raw_checks.sql — 21 read-only warehouse checks
  covering schema, identity, completeness, totals, strings, source-specific row
  associations, and the full ordered semantic fingerprint.
- scripts/data/fetch_rna_projects_gis.py — layer-8-only native ArcGIS JSON
  acquisition and create-only GCS preservation CLI with exact numeric-token
  parsing, frozen pre/post OBJECTID checks, schema/CRS/geometry audits, raw and
  semantic fingerprints, and generation-specific cloud-byte verification.
- scripts/data/match_watershed_projects_rna.py — deterministic exact-ID matcher
  covering the complete governed source universe, preserving explicit zero- and
  multi-match states and reconciling governed project counts and request dollars.
- tests/test_rna_projects_gis_reconnaissance.py — focused source-fidelity,
  Decimal-ID, OBJECTID consistency, geometry/CRS, manifest, matching,
  reconciliation, create-only GCS, cloud-byte, and tracked-artifact validation.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/20260901T183323Z/manifest.json —
  Git-tracked acquisition manifest for the immutable native snapshot; the ID is a
  UTC retrieval timestamp, not a source vintage.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/20260901T183323Z/gcs_receipt.json —
  Git-tracked GCS object generations, byte sizes, local checksums, and independently
  streamed generation-specific cloud checksums; the receipt itself is not uploaded.
- data/reconnaissance/city_austin/rna_projects/layer_8/20260901T183323Z/project_id_geometry_matches.csv —
  Git-tracked 37-project exact-ID match artifact with 15 single matches, 22 zero
  matches, and no multiple matches in the captured live snapshot.
- data/staging/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf —
  ignored local raw source-universe snapshot.
- data/staging/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf —
  ignored local benchmark-only snapshot.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf#1788210198102506 — verified cloud source-universe snapshot, 1,151,348 bytes, SHA-256 `d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e`.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf#1788210202820922 — verified cloud benchmark-only snapshot, 412,820 bytes, SHA-256 `da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359`.
- climatecapital-ai.raw.watershed_projects_2025_11_21 — source-faithful BigQuery
  raw table in `us-central1`, with 37 REQUIRED-schema rows and 21 passing SQL
  quality checks.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/ —
  six create-only raw/provenance objects (`service.json`, `layer.json`, pre/post
  OBJECTID responses, `features.arcgis.json`, and `manifest.json`) whose exact
  local bytes were verified against generation-specific cloud streams.

The ordered raw-table schema is `source_id STRING REQUIRED`,
`source_pdf_page INTEGER REQUIRED`, `source_table_row_order INTEGER REQUIRED`,
`map_label STRING REQUIRED`, `subproject_id STRING REQUIRED`,
`project_name STRING REQUIRED`,
`current_funding_request_estimate_source STRING REQUIRED`,
`current_funding_request_estimate_dollars INTEGER REQUIRED`, and
`council_districts_source STRING REQUIRED`.

The 37 official source rows above have been extracted, loaded only to the raw
table, and tested against one immutable live/current GIS snapshot. No GIS match is
an eligibility result, and the snapshot does not establish January 2026 geometry.
The all-37 purpose classification and exact provisional 12-record P0 analytical
family are documented derivations in the Methodology Lock; they are not persisted
analytical tables or a City taxonomy. No flood/exposure/benefit score, optimization result,
staging/curated table, or benchmark table has been created. Benchmark isolation
remains explicit.

### Repository Structure

- AGENTS.md — repository rules and task-start routing.
- PROJECT_PROGRESS.md — sole current state/progress/handoff document.
- README.md — repository landing page and documentation map.
- docs/methodology/p0-evidence-methodology.md — authoritative locked P0 evidence
  roles, family, missingness treatment, and deterministic Funding Plan method.
- docs/product/product-plan.md — approved product-level Product and Design Lock.
- docs/product/user-stories.md — authoritative prioritized backlog and acceptance
  intent.
- docs/product/screen-spec.md — authoritative UI, state, and wireframe specification.
- docs/delivery/execution-plan.md — initial approved delivery sequencing and gates.
- docs/decisions.md — authoritative durable decision history.
- docs/reference/technical-architecture-reference.md — exploratory Architecture
  planning reference.
- .gitignore — raw/staging, PDF, GeoJSON, temporary-response, Python, and common
  credential-file protections.
- requirements-data.txt — pinned dependency for local source extraction only.
- requirements-cloud.txt — pinned BigQuery client dependency for the manual raw
  load/checkpoint workflow only.
- data/metadata/source_registry.csv — canonical source and provenance registry.
- data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv —
  tracked official source-universe extraction.
- data/metadata/source_snapshots/austin_rna_projects_layer_8_live/ — tracked
  timestamped GIS acquisition manifests and post-upload GCS receipts.
- data/reconnaissance/city_austin/rna_projects/layer_8/ — tracked timestamped
  complete-universe project-ID/geometry match artifacts.
- scripts/data/fetch_sources.py — minimal reproducible source downloader.
- scripts/data/extract_watershed_projects.py — deterministic source-universe
  extractor and reconciliation CLI.
- scripts/data/load_watershed_projects_bigquery.py — guarded raw BigQuery loader.
- scripts/data/fetch_rna_projects_gis.py — immutable layer-8 acquisition and
  create-only verified GCS upload CLI.
- scripts/data/match_watershed_projects_rna.py — complete-universe exact-ID GIS
  matcher and governed funding reconciliation CLI.
- sql/quality/watershed_projects_raw_checks.sql — read-only warehouse data-quality
  suite.
- tests/test_source_ingestion.py — lightweight source-ingestion validation suite.
- tests/test_watershed_project_extraction.py — source extraction and failure-path
  validation suite.
- tests/test_watershed_bigquery_loader.py — non-destructive raw-loader contract and
  safety tests.
- tests/test_rna_projects_gis_reconnaissance.py — native source, provenance,
  matching, reconciliation, and cloud-preservation tests.
- docs/architecture/ — intentionally absent until explicit Architecture Lock.
- docs/delivery/implementation-plan.md, test-plan.md, and milestones.md —
  intentionally absent until post-Architecture delivery planning.

Local branch: main. Public GitHub remote:
https://github.com/swethabarla19/ClimateCapitalAI.git.

### Environments and External Services

- Verified Google Cloud context: configured project `climatecapital-ai`, active
  gcloud authentication and ADC, and existing raw-data bucket
  `gs://climatecapital-ai-raw-swetha/`. The existing `raw` BigQuery dataset and
  `watershed_projects_2025_11_21` table were inspected in `us-central1`; the table
  has the exact governed schema and 37 rows. Six create-only objects for the
  20260901T183323Z RNA layer-8 snapshot were added under the authorized raw-data
  prefix and independently verified from generation-specific streams. No existing
  cloud object, infrastructure, IAM, dataset/bucket setting, or credential was
  changed; staging, curated, and benchmark datasets/tables were not inspected.
- Current local data runtime verified with Python 3.14.7, pypdf 6.16.2, and
  google-cloud-bigquery 3.44.0 in the ignored `.venv`. BigQuery access used local
  ADC; no credential material is stored in the repository. The earlier Python 3.12
  source-fetch runtime lacked a default CA bundle; `/etc/ssl/cert.pem` was used for
  verified HTTPS without disabling certificate verification.
- No application environment is established.
- The local process-job Stop hook lacks the node runtime it expects.

### Common Commands

- git status --short --branch — verify working tree and upstream.
- git log --oneline --decorate --max-count=8 — inspect checkpoints.
- git diff --check — validate documentation whitespace.
- python3 -m venv .venv — create the ignored local data-tool environment.
- .venv/bin/python -m pip install -r requirements-data.txt — install the pinned
  local data-extraction dependency.
- .venv/bin/python -m pip install -r requirements-cloud.txt — install the pinned
  BigQuery client dependency in the same ignored environment.
- .venv/bin/python -m unittest discover -s tests -v — run ingestion, extraction,
  and non-destructive raw-loader validation.
- .venv/bin/python scripts/data/extract_watershed_projects.py — verify the source
  checksum, extract/reconcile the 37 rows, and create or confirm the deterministic
  source-universe CSV.
- .venv/bin/python scripts/data/load_watershed_projects_bigquery.py — create the raw
  table only when absent; current reruns refuse the existing historical target.
- SSL_CERT_FILE=/etc/ssl/cert.pem .venv/bin/python
  scripts/data/fetch_rna_projects_gis.py acquire --max-attempts 3 — acquire a new
  UTC-timestamped layer-8 native snapshot after frozen-OBJECTID consistency,
  source-contract, numeric-ID, geometry, and manifest validation.
- .venv/bin/python scripts/data/match_watershed_projects_rna.py --snapshot-id
  20260901T183323Z — create or confirm the deterministic complete-universe exact-ID
  match artifact and funding reconciliation for the preserved snapshot.
- .venv/bin/python scripts/data/fetch_rna_projects_gis.py upload --snapshot-id
  20260901T183323Z --bucket gs://climatecapital-ai-raw-swetha/ — preserve the
  validated raw snapshot create-only and write/confirm the Git-tracked
  generation-specific verification receipt; requires existing authenticated
  gcloud access.
- bq --project_id=climatecapital-ai query --use_legacy_sql=false
  --location=us-central1 < sql/quality/watershed_projects_raw_checks.sql — rerun the
  read-only warehouse quality suite using local authenticated tooling.
- python3 scripts/data/fetch_sources.py — fetch both registered sources when the
  Python environment has a working default CA bundle.
- SSL_CERT_FILE=/etc/ssl/cert.pem python3 scripts/data/fetch_sources.py — verified
  fetch command for the current local Python installation.
- Add verified setup, test, lint, build, migration, and deploy commands only when
  tooling exists.

## Decision Summary

The authoritative history is [docs/decisions.md](docs/decisions.md).

- D-001–D-063 preserve all Stage 1–4 and repository decisions.
- D-064 establishes the purpose-specific repository-memory hierarchy.
- D-065 keeps the technical reference non-authoritative until Architecture Lock.
- D-066 keeps PROJECT_PROGRESS.md as the only progress file and defers
  architecture-informed delivery plans.
- D-067 pauses Architecture Lock for controlled evidence reconnaissance; the
  evidence dependency and Methodology Lock review are now complete, while
  Architecture requires separate authorization before it resumes.
- D-068 establishes the 37-project source-universe path and structurally separate
  Historical City Recommendation benchmark path.
- D-069 establishes the canonical registry and immutable raw-fetch/provenance
  contract without selecting a production pipeline or architecture.
- D-070 establishes create-only two-object cloud preservation with independent
  generation-specific SHA-256 verification.
- D-071 establishes checksum-gated, fail-closed, source-faithful extraction of the
  complete 37-record Watershed reconnaissance universe without deciding analytical
  eligibility.
- D-072 establishes the exact-schema, create-only, independently checked BigQuery
  raw warehouse contract without selecting a production pipeline or analytical
  architecture.
- D-073 establishes live RNA layer 8 as the sole canonical GIS source for this
  bounded work unit, with native immutable acquisition, exact numeric-ID matching,
  explicit missingness, and uncertain historical fit.
- D-074 closes evidence feasibility and governs the four evidence roles and final
  P0 treatment of Problem Score, RNA/FloodPro, expected benefit, and EAZ 2021.
- D-075 preserves the all-37 universe, all-37 derived purpose audit, incoherent
  24-record broad flood family, exact provisional 12-record P0 analytical family,
  and separate citywide treatment for 5789.150.
- D-076 removes unsupported scores, ranks, weights, expected benefit, optimization,
  imputation, missingness penalties, and confidence-as-need.
- D-077 reopens Funding Plan membership to analyst control with deterministic
  validation/arithmetic and non-recommendation terminology.
- D-078 separates the $125 million Historical Envelope from the analyst-created
  Session Reference Plan and Current Confirmed Plan, supports analyst-defined
  Available Budget What-If scenarios, and structurally isolates the Historical
  City Recommendation benchmark.
- D-079 limits Gemini to grounded explanation and confirmed translation of explicit
  analyst commands; it cannot originate facts, membership, or recommendations.
- Next available decision ID: **D-080**.

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
| 2026-09-01 | Reviewed Methodology Lock commit gate | Confirmed the exact documentation-only working-tree boundary; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, and staged-scope validation | Passed: 46 tests; only the ten intended methodology, Product/Design, delivery, reference, repository-routing, and current-state Markdown files are included; no application, data, cloud, architecture, or push change |
| 2026-09-01 | Final Methodology Lock semantic audit | Audited Historical Envelope versus analyst plan terminology, Historical City Recommendation isolation, provisional analytical-family versus eligibility language, and active-family/full-request/deterministic-membership boundaries; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, exact source/family/broad reconciliation, obsolete-current-term guards, D-001–D-079 continuity/supersession checks, and Markdown link/fence validation | Passed: 46 tests; $125 million is only Historical Envelope context; Session Reference Plan and Current Confirmed Plan are distinct analyst-plan terms; City benchmark is structurally isolated; 12 projects / $143,005,000 remain a provisional analytical family inside the visible 37-project / $327,970,000 universe; membership is active-family-only and full-request; deterministic logic validates but does not select; no commit or push |
| 2026-09-01 | P0 evidence and Methodology Lock | Reviewed the interrupted working-tree diff and all authoritative handoff files; ran `.venv/bin/python -m unittest discover -s tests -v`, `git diff --check`, exact CSV/methodology reconciliation, all-37 and family name/ID/request checks, broad-family total check, D-001–D-079 continuity, relative Markdown-link and fence validation, stale-current-language guards, and deferred-file boundary checks | Passed: 46 tests; 37 projects / $327,970,000; exact 12 records / $143,005,000; exact broad 24 / $233,380,000; official names and requests reconcile; 79 continuous unique decisions; 13 Markdown files have valid relative links and balanced fences; no stale optimizer/weight/recommendation contract in current handoff; no application, architecture, cloud, commit, or push change |
| 2026-09-01 | RNA layer-8 GIS reconnaissance | Acquired the live service/layer metadata, frozen pre-ID set, exact feature response, and post-ID set; ran the matcher twice for created/identical behavior; uploaded six create-only objects and streamed each generation-specific cloud object for independent SHA-256; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, `pip check`, manifest/match/receipt reconciliation, `git diff --check`, credential scan, and tracked/ignored status review | Passed: 577/577 stable OBJECTIDs and polygon geometries, exact 11-field schema, native 102739/2277 CRS, no transfer-limit flag, no missing/unexpected IDs, 577 safe numeric ID tokens, no true curves, 15 single/22 zero/0 multiple governed matches, $163,975,000 matched plus $163,995,000 unmatched equals 37 projects and $327,970,000; local/cloud bytes and SHA-256 match for all six objects; no benchmark, BigQuery, infrastructure, IAM, architecture, methodology, commit, or push change |
| 2026-08-31 | Raw BigQuery ingestion and warehouse quality | Inspected dataset/table metadata; ran the final `sql/quality/watershed_projects_raw_checks.sql` in `us-central1`; exercised the loader's existing-target refusal; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, `pip check`, `git diff --check`, credential scan, and tracked/ignored status review | Passed: exact nine-column ordered REQUIRED STRING/INT64 schema; 21/21 warehouse checks; 37 rows and unique IDs; $327,970,000; page/source/order/district/spot checks and semantic SHA-256 match; 29 tests; loader refused the existing table before load submission; no cloud data/configuration or credentials changed |
| 2026-08-31 | Official Watershed source-universe extraction | Verified the raw checksum against the registry; inspected rendered source table pages; ran the extractor twice for created/identical behavior; ran `.venv/bin/python -m unittest discover -s tests -v`, `py_compile`, an independent standard-library CSV count/sum/spot-check read, and `git diff --check` | Passed: 19 tests; 37 unique source records; row sum, independently parsed table total, and memorandum program request all equal $327,970,000; first/last, page boundary, multi-district, and 5789.150/5789.145/5789.146 order checks passed; ambiguous structure, checksum mismatch, unparseable row, missing total, and differing-output paths fail closed |
| 2026-08-31 | Two-object Cloud Storage raw preservation | Confirmed local existence, byte sizes, independent SHA-256, and registry agreement; verified configured project, active gcloud auth, ADC, bucket access, initial object 404s, and create-only generation support; uploaded with `--if-generation-match=0`; described both objects; streamed each generation-specific object through independent SHA-256; ran `git diff --check`, credential scan, tracked/ignored status review, and repository-file review | Passed: exactly two objects created at the authorized paths; local, registry, expected, and cloud-streamed SHA-256 values and byte sizes match; generations 1788210198102506 and 1788210202820922 verified; raw PDFs remain ignored/untracked; no credentials, infrastructure, IAM, bucket settings, BigQuery, extraction, commit, or push changed |
| 2026-08-31 | Minimal source-ingestion and provenance foundation | Ran `python3 -m unittest discover -s tests -v`, `python3 -m py_compile`, canonical-registry validation, `wc -c`, independent `shasum -a 256`, PDF file-type inspection, `git diff --check`, trailing-whitespace scan, `git check-ignore`, and tracked/ignored status review; fetched both sources over verified HTTPS using the host CA bundle | Passed: 9 tests; 2 valid registry rows; both HTTP 200 downloads reconciled byte-for-byte to registry checksums; raw PDFs and Python cache files are ignored; no cloud upload, BigQuery load, extraction, architecture, methodology, application, commit, or push occurred |
| 2026-08-31 | Architecture pause and evidence-reconnaissance handoff | Reviewed the complete documentation diff; ran `git diff --check`; confirmed 68 continuous decision rows through D-068, next ID D-069, removal of stale “not started”/“ready” status, and preservation of the Product and Design Lock boundary | Passed; only PROJECT_PROGRESS.md, README.md, and docs/decisions.md changed; no architecture, methodology, source data, pipeline, application, cloud, or approved product specification changed |
| 2026-08-27 | Documentation architecture normalization | Reviewed all repository documentation and the complete changed-file set; ran git diff --check; validated relative Markdown links, required/forbidden file boundaries, 12 required P0 plus one SP0-1 and 13 acceptance blocks, continuous D-001–D-066, required Stage 4 state coverage, balanced fences, and preservation of historical verification/session content | Passed; detailed planning now has purpose-specific authoritative homes, PROJECT_PROGRESS.md remains the only progress tracker, deferred architecture/delivery files are absent, and no application or architecture implementation changed |
| 2026-08-26 | Stage 4 Product and Design Lock closeout | Reviewed the complete documentation diff; ran `git diff --check`; confirmed the changed-file boundary, Stage 4 section coverage, 20 continuous decisions from D-044 through D-063, current-state terminology, and balanced Markdown code fences | Passed; only `PROJECT_PROGRESS.md` and `README.md` changed, Stage 1–3 remain unchanged in meaning, and no application or technical implementation was introduced |
| 2026-08-26 | Stage 3 documentation checkpoint | Read all repository guidance and canonical documentation; ran `git diff --check`; counted 12 P0 stories, one stretch P0 story, and 13 acceptance-criteria blocks; checked decision-log continuity, stale terminology, branch, status, and remotes | Passed; only `PROJECT_PROGRESS.md` and `README.md` are modified, Stage 4 remains unstarted, and no commit or push was made |
| 2026-08-25 | Local/remote tracker reconciliation | Compared local `main` and GitHub commit history, remote URL, branch tracking, working-tree state, milestones, blockers, risks, decisions, technical map, and next actions | Passed; remote head matched local head before this tracker update |
| 2026-08-25 | GitHub checkpoint publication | Verified repository ownership and public visibility, inspected and preserved the remote README commit, merged histories, and pushed `main` | Passed; local `main` tracks `origin/main` |
| 2026-08-25 | Git and Stop-hook checkpoint | Verified repository root, `main` branch, author configuration, status, remotes, hook registration, and executable availability | Local Git ready; GitHub remote absent; process-jobs Stop hook lacks `node` |
| 2026-08-25 | Stage 2 product definition | Checked the locked context against all 12 requested clarifications and confirmed that deferred scoring and cohort choices remain open | Passed |
| 2026-08-24 | P0 hazard and equity framing | Reconciled the selected option with the current watershed scope and Map → projects → portfolio journey | Passed |
| 2026-08-24 | Progress system | Manual review of required handoff sections and repository instructions | Passed |

## Session Log

Add new entries immediately below this guidance so the newest session is first.

### 2026-09-01 — Lock the P0 evidence-first methodology

- **Objective:** Persist the closed evidence-feasibility findings, reconcile their
  consequences with the prior Product and Design Lock, and lock the smallest
  defensible P0 method without application or architecture implementation.
- **Methodology result:** Retained all 37 governed projects / $327,970,000 and the
  all-37 derived purpose classification with official name, evidence, confidence,
  and ambiguity. Recorded the 24-project / $233,380,000 broad flood-related family
  as analytically incoherent and locked the exact 12-record local flood/local
  drainage analytical family / $143,005,000, with 5789.150 retained as a citywide
  program requiring separate geography/evidence treatment.
- **Evidence treatment:** Locked FACT, CONTEXTUAL EVIDENCE, RESEARCH-ONLY EVIDENCE,
  and UNAVAILABLE / UNSUPPORTED. Problem Score and FEMA remain contextual; current
  RNA and Fully Developed FloodPro are research-only for governed analytical use;
  EAZ 2021 is contextual for 5/12 and unavailable at project level for 7/12;
  expected flood-reduction benefit and a cohort-wide numeric risk/equity model are
  unsupported.
- **Product reconciliation:** Explicitly removed Funding Priority, rank, Importance
  weights, expected benefit, missingness penalties/imputation, and optimization.
  Reopened Funding Plan inclusion/removal as an analyst-controlled input; limited
  deterministic authority to governed facts/evidence states, validation,
  integer-dollar arithmetic, and supported comparison; limited Gemini to grounded
  explanation and confirmed translation of explicit analyst commands. Retained
  $125 million as Historical Envelope context, not family or eligibility logic.
- **Decision history:** Added D-074–D-079 and marked the original conflicting
  decision text superseded, narrowed, or resolved rather than overwriting it.
- **Final semantic audit:** Reserved Historical Envelope for the $125 million
  historical context; renamed the first analyst-confirmed plan Session Reference
  Plan and the active plan Current Confirmed Plan; made City benchmark isolation,
  active-family-only membership, full-request treatment, and deterministic
  non-selection authority explicit throughout the affected handoff.
- **Files changed:** Added docs/methodology/p0-evidence-methodology.md; updated
  AGENTS.md, PROJECT_PROGRESS.md, README.md, docs/decisions.md,
  docs/product/product-plan.md, docs/product/user-stories.md,
  docs/product/screen-spec.md, docs/delivery/execution-plan.md, and
  docs/reference/technical-architecture-reference.md.
- **Verification:** The full 46-test suite and `git diff --check` passed. Independent
  documentation checks reconciled the exact governed/family/broad counts and
  dollars to the source CSV, matched all 37 names and family requests, confirmed
  continuous D-001–D-079, validated 13 Markdown files' relative links/fences, and
  found no stale current optimizer/weight/recommendation contract. The final
  semantic audit also passed explicit guards for Historical Envelope/session-plan
  separation, City benchmark isolation, provisional-family/non-eligibility
  treatment, and active-family-only full-request membership with deterministic
  validation rather than selection.
- **Boundaries:** No new source reconnaissance, Buildings/SVI ingestion, geometry,
  score, weights, optimization, application code, production pipeline, architecture,
  cloud resource, or push occurred. The reviewed documentation checkpoint was
  authorized for commit.
- **Handoff:** Review is complete. In a separately authorized task, resume
  Architecture Planning against the locked methodology and reconciled
  Product/Design handoff.

### 2026-09-01 — Acquire and match Austin RNA Projects layer 8

- **Objective:** Preserve one reproducible native snapshot of the canonical live
  RNA Projects layer 8, test all governed memo IDs without fuzzy/name matching,
  and quantify current GIS evidence coverage without inferring analytical use.
- **Acquisition:** Captured service/layer metadata, 577 pre-acquisition OBJECTIDs,
  the exact frozen-ID feature response with geometry, and 577 post-acquisition
  OBJECTIDs under snapshot `20260901T183323Z`. Pre/post sets matched, all requested
  features returned exactly once, no unexpected features or transfer-limit flag
  occurred, and the semantic feature fingerprint is
  `sha256:3d81feb35841e816c0ce5bab5e2abbca05b46a903f98c1ea3b16c8cf604b940f`.
- **Source fidelity:** Parsed native JSON numeric tokens without binary-float
  conversion. All 577 `SUB_PROJECT_ID` values mapped exactly to the governed
  three-decimal domain by representational zero-padding only; 548 canonical IDs
  are unique in the full layer and source duplicates remain visible. The exact
  11-field schema and native ESRI:102739/EPSG:2277 polygon CRS passed validation.
- **Geometry:** All 577 features contain native polygon geometry; no true curves
  were observed. No reprojection, simplification, densification, repair,
  precision/offset setting, or quantization was applied.
- **Match result:** The complete-universe artifact retains all 37 official projects
  and derives 15 single matches, 22 zero matches, and no multiple matches by exact
  canonical ID only. Three matching GIS names differ from the memo names, which is
  retained as evidence and does not affect matching. Matched governed requests are
  $163,975,000 and unmatched requests are $163,995,000, reconciling to 37 and
  $327,970,000.
- **Cloud preservation:** Created exactly six objects below
  `gs://climatecapital-ai-raw-swetha/raw/city_austin/rna_projects/layer_8/20260901T183323Z/`.
  Every generation-specific cloud byte stream matched its local size and exact-byte
  SHA-256. The finalized manifest was uploaded; the non-circular GCS receipt is
  Git-tracked only.
- **Files:** Added the two focused CLIs, one focused test module, the timestamped
  manifest/receipt/match artifacts, and D-073; updated the source registry,
  registry validation, README, and this progress handoff. Raw HTTP/GIS responses
  remain ignored and untracked.
- **Verification:** The full repository suite, Python compilation, dependency
  check, independent manifest/match/receipt reconciliation, diff check, credential
  scan, and Git tracked/ignored review passed. The matcher also confirmed
  identical-output behavior on rerun.
- **Boundaries:** Layer 8 is live/current and remains `historical_fit=uncertain`,
  `analytical_role=research-only`; the snapshot does not establish January 2026
  geometry. A match does not establish eligibility, project footprint semantics,
  hazard, exposure, benefit, or analytical comparability. No additional GIS,
  benchmark, BigQuery, methodology, Architecture, application, commit, or push
  work occurred.
- **Handoff:** Review this bounded GIS checkpoint, then explicitly authorize the
  next analytical-feasibility evidence work unit. Architecture Planning remains
  paused before lock.

### 2026-08-31 — Validate and harden raw BigQuery ingestion

- **Objective:** Complete the raw warehouse checkpoint by reviewing the manual
  loader, validating the existing table without overwriting it, adding durable SQL
  quality checks, and preserving the result without beginning GIS or architecture.
- **Manual implementation review:** Retained the correct project/dataset/table,
  explicit nine-column schema, STRING project IDs and district source text,
  INTEGER page/order/dollar fields, UTF-8/header handling, `us-central1` job
  location, local ADC, and `WRITE_EMPTY` behavior. Hardened only material gaps:
  repository-anchored CSV resolution, exact CSV checksum and contract preflight,
  dataset-location and existing-target checks, explicit load options, post-load
  schema/location/count validation, and human-readable failures.
- **Warehouse result:** Verified the existing
  `climatecapital-ai.raw.watershed_projects_2025_11_21` table and its `raw` dataset
  are in `us-central1`. All nine ordered columns and REQUIRED modes match the
  governed schema; `subproject_id` and source fields are STRING, while page, row
  order, and normalized dollars are INTEGER. The table has 37 rows.
- **Data-quality result:** All 21 final read-only SQL checks passed: 37 unique IDs,
  no duplicates or governed NULLs, one expected source ID, contiguous order 1–37,
  exact A–AK sequence, page 4/5 domain and 19/18 counts, positive/reconciled
  funding values totaling $327,970,000, valid source-form district strings, exact
  first/boundary/multi-district/final rows, preserved 5789.150/5789.145/5789.146
  order, and full ordered semantic SHA-256
  `c9091117734b2f793ed5f396dba3b8897169ad168659df0fe4f97cd92aeb072a`.
- **Tests and safety:** The full 29-test suite, `py_compile`, `pip check`, and
  `git diff --check` passed; the credential-pattern scan found no matches. A live
  loader preflight refused the already-existing table before load submission.
  Authentication used local ADC; no credentials or credential paths were added.
- **Files changed:** Retained the manually added requirements-cloud.txt; hardened
  scripts/data/load_watershed_projects_bigquery.py; added
  tests/test_watershed_bigquery_loader.py and
  sql/quality/watershed_projects_raw_checks.sql; updated PROJECT_PROGRESS.md,
  README.md, and docs/decisions.md; recorded D-072.
- **Limitations:** The live schema/data prove the current warehouse copy is
  source-faithful, but the hardened code cannot retroactively prove the exact
  configuration of the already-completed manual load job. BigQuery does not enforce
  the SQL semantic contracts as constraints, so the suite must be rerun after any
  separately authorized mutation. Source reuse terms remain unresolved.
- **Boundaries preserved:** No existing table or other cloud state was recreated,
  overwritten, or changed. No staging/curated/benchmark table, January benchmark
  inspection, GIS work, eligibility, evidence inference, scoring, optimization,
  Product/Design change, Architecture Planning, commit, or push occurred.
- **Handoff:** Await review. The recommended next separately authorized work unit
  is complete 37-ID Austin GIS geometry matching with retained unmatched records
  and explicit match evidence; do not begin it in this task.

### 2026-08-31 — Extract the official Watershed source universe

- **Objective:** Derive and validate only the complete named-project source universe
  from the checksum-governed November 21, 2025 memo without deciding eligibility,
  geometry, project type, flood evidence, methodology, or architecture.
- **Completed:** Pinned pypdf 6.16.2 as a local data-only dependency; added a
  checksum-gated extractor that requires table anchors and columns, parses each row
  without crossing row boundaries, records 1-based physical PDF pages, preserves
  official IDs and published order as strings, retains source currency alongside
  integer dollars, reconciles totals, and refuses differing-artifact overwrite;
  generated the deterministic 37-record CSV; recorded D-071.
- **Data result:** Extracted 19 records from physical PDF page 4 and 18 from page 5.
  All 37 map labels and subproject IDs are unique. The row sum, separately parsed
  table total, and memorandum program request each equal $327,970,000. Presence in
  the artifact does not establish ClimateCapital eligibility.
- **Schema:** `source_id`, `source_pdf_page`, `source_table_row_order`, `map_label`,
  `subproject_id`, `project_name`, `current_funding_request_estimate_source`,
  `current_funding_request_estimate_dollars`, `council_districts_source`.
- **Tests and results:** The focused 10-test extraction suite and full 19-test
  repository suite passed. Source-verified first/last, page-4/page-5 boundary,
  multi-district, and 5789.150/5789.145/5789.146 anomaly checks passed; checksum,
  anchor, column, row, total, and overwrite failure paths passed; `py_compile`, an
  independent CSV count/sum read, and `git diff --check` passed; a repeated CLI run
  reported the artifact as identical.
- **Files changed:** Added requirements-data.txt,
  scripts/data/extract_watershed_projects.py,
  data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv,
  and tests/test_watershed_project_extraction.py; updated
  data/metadata/source_registry.csv, PROJECT_PROGRESS.md, README.md, and
  docs/decisions.md.
- **Issues and risks:** The source claims project-ID sorting but places 5789.150
  before 5789.145 and 5789.146; the artifact preserves that published order. PDF
  line-wrap whitespace was collapsed while punctuation, spelling, and displayed
  currency were retained. Source reuse and redistribution terms remain unresolved.
- **Boundaries preserved:** The January benchmark PDF was not inspected or used.
  No GIS matching, eligibility, project-type classification, flood-benefit
  inference, BigQuery table, scoring, optimization, application, cloud mutation,
  Architecture Planning, commit, or push occurred.
- **Handoff:** Await user review. Do not begin GIS matching or further evidence work
  until separately authorized.

### 2026-08-31 — Preserve the two raw snapshots in existing Cloud Storage

- **Objective:** Upload only the two governed local raw PDFs to their exact paths in
  the existing bucket without changing infrastructure or silently overwriting an
  object, then independently verify cloud bytes against local and registry SHA-256.
- **Completed:** Verified local existence, sizes, expected and registry checksums,
  configured project `climatecapital-ai`, active gcloud authentication, ADC, and
  access to `gs://climatecapital-ai-raw-swetha/`; confirmed both destination objects
  were absent; uploaded each with `--if-generation-match=0`; recorded D-070.
- **Cloud results:** The Watershed source object is generation
  `1788210198102506`, 1,151,348 bytes. The benchmark object is generation
  `1788210202820922`, 412,820 bytes. Both have metageneration 1 and content type
  application/pdf.
- **Integrity verification:** Streamed each generation-specific GCS object through
  an independent SHA-256 calculation. Each cloud byte size and SHA-256 matched the
  corresponding local file, expected digest, and canonical registry checksum.
  GCS CRC32C and MD5 metadata were observed but were not treated as SHA-256.
- **Files changed:** Updated PROJECT_PROGRESS.md and docs/decisions.md for durable
  external-state handoff. No source metadata, raw local file, code, test, product,
  design, architecture, or analytical file changed.
- **Issues and warnings:** Sandboxed gcloud version/help checks could not write SDK
  logs under the local gcloud configuration directory; authenticated commands were
  executed with approved access and succeeded. No cloud conflict or integrity
  warning occurred, and no token or credential content was printed or stored.
- **Boundaries preserved:** No infrastructure, IAM, bucket setting, service account,
  credential file, additional object, BigQuery resource, extraction, project table,
  methodology, Architecture Planning, or push.
- **Handoff:** Await user review. Do not extract the 37 projects or perform further
  cloud work until separately authorized.

### 2026-08-31 — Implement the minimal source-ingestion foundation

- **Objective:** Establish only the reproducible source registry, immutable local
  fetch, provenance metadata, tests, and Git protections required to preserve the
  first two authoritative City documents.
- **Completed:** Added the exact 15-column canonical registry and registered the
  November 21 source-universe memo as analytical and the January 21 recommendation
  as benchmark-only; added a standard-library HTTPS fetcher with deterministic
  paths, exact-byte SHA-256, UTC retrieval metadata, PDF/header checks, and
  differing-snapshot overwrite refusal; downloaded both PDFs; added nine focused
  tests and raw/temporary/credential Git protections; recorded D-069.
- **Tests and results:** `python3 -m unittest discover -s tests -v` passed 9/9;
  `python3 -m py_compile` passed; registry validation found two valid unique rows;
  independent byte counts and `shasum -a 256` values matched the registry; both
  files were recognized as PDF 1.7; `git diff --check` and the trailing-whitespace
  scan passed; `git check-ignore` and status confirmed both raw PDFs are ignored.
- **Files changed:** Added .gitignore, data/metadata/source_registry.csv,
  scripts/data/fetch_sources.py, and tests/test_source_ingestion.py; updated
  PROJECT_PROGRESS.md, README.md, and docs/decisions.md. The two downloaded PDFs
  exist only in ignored data/staging paths.
- **Deviations and issues:** The sandboxed attempt could not resolve the host. The
  unrestricted Python retry then exposed a missing default CA bundle; verified
  HTTPS succeeded with `SSL_CERT_FILE=/etc/ssl/cert.pem`. Certificate verification
  was never disabled. License/reuse terms remain unverified. The exact existing GCS
  bucket name was not supplied, so no upload was attempted.
- **Boundaries preserved:** No PDF extraction, OCR, 37-project derivation,
  eligibility, analytical evidence, scoring, optimization, Gemini, application,
  BigQuery table/load, cloud provisioning, Architecture Lock, commit, or push.
- **Handoff:** Await user review. If Cloud Storage upload is requested, obtain the
  exact existing bucket name first. Otherwise, the recommended next separately
  authorized milestone is source-only derivation of the 37 project records without
  eligibility or analytical inference.

### 2026-08-31 — Pause Architecture Lock for evidence reconnaissance

- **Objective:** Record the controlled Architecture Planning dependency-resolution
  step needed to test the 37 official Watershed projects against authoritative,
  historically valid evidence before architecture or methodology is locked.
- **Completed:** Preserved every approved Product and Design Lock; paused
  Architecture Planning before lock; made the 37-project evidence repository and
  matrix the immediate objective; recorded the source-universe and benchmark-only
  separation; updated blockers, risks, open questions, Next Actions, and the
  Architecture handoff; added D-067 and D-068.
- **Files changed:** PROJECT_PROGRESS.md, README.md, and docs/decisions.md. No
  product specification, architecture file, methodology, source dataset, pipeline,
  application code, dependency, Gemini integration, or cloud resource changed.
- **Verification:** Reviewed the complete diff; `git diff --check` passed; confirmed
  68 continuous decision rows through D-068, next ID D-069, and no stale current
  status claiming Architecture Planning is unstarted or ready to lock.
- **Handoff:** Begin with the November 21, 2025 source memo, preserve all 37 source
  projects, keep the January 21, 2026 City recommendation structurally separate,
  and build the evidence matrix without inventing benefit, geometry, exclusions,
  or methodology. Resume Architecture Planning only after findings are reviewed.

### 2026-08-27 — Normalize durable planning documentation

- **Objective:** Move detailed approved planning out of the monolithic progress
  tracker into purpose-specific repository memory that can support a fresh
  Architecture task without chat history.
- **Completed:** Created authoritative product plan, user-story backlog, screen
  specification, initial execution plan, and decision history; created a
  comprehensive but explicitly non-authoritative technical reference; updated
  repository working rules and README navigation; reduced PROJECT_PROGRESS.md to
  current status, milestones, blockers, risks, questions, pointers, verification,
  and session history; recorded D-064–D-066.
- **Files changed:** AGENTS.md, PROJECT_PROGRESS.md, README.md. Created
  docs/product/product-plan.md, docs/product/user-stories.md,
  docs/product/screen-spec.md, docs/delivery/execution-plan.md,
  docs/decisions.md, and
  docs/reference/technical-architecture-reference.md. No application,
  architecture, data, cloud, dependency, or UI implementation changed.
- **Verification:** git diff --check passed; all relative Markdown links resolve;
  required closeout files exist; deferred architecture, implementation, test,
  milestone, and duplicate progress files are absent; story and decision sequences
  are complete; key Stage 4 states remain represented; historical verification and
  session content was preserved.
- **Handoff:** Ready for a fresh Architecture planning task using the required
  reading set in AGENTS.md and Current Workstream. No Architecture Lock or
  implementation has begun.

### 2026-08-26 — Lock Stage 4 Product and Design documentation

- **Objective:** Persist the approved final Product and Design Lock using the
  repository's existing documentation structure without beginning application or
  technical implementation.
- **Completed:** Marked Stage 4 complete; recorded the required screens, navigation
  and contextual surfaces, screen requirements, important state/recovery model,
  low-fidelity wireframes, demo sequence, assumptions, dependencies, risks, and
  evidence deferrals; kept Compare conditional SP0-1; and added D-044 through
  D-063 while preserving the Stage 1–3 locks.
- **Files changed:** `PROJECT_PROGRESS.md`, `README.md`. No files were created, and
  no application, architecture, data, analytics, Gemini, cloud, or dependency work
  was performed.
- **Verification:** Reviewed the complete documentation diff; `git diff --check`
  passed; confirmed only the two intended documentation files changed, all 20 new
  decisions appear once and in sequence, required Stage 4 content is present,
  current-state language is updated, and Markdown code fences are balanced.
- **Handoff:** The next planned work item is a separately authorized technical
  execution-readiness plan, followed by evidence-stage decisions. Neither has
  begun.

### 2026-08-26 — Prepare the locked Stage 3 documentation checkpoint

- **Objective:** Persist all approved planning through Stage 3 in the existing
  canonical repository structure without beginning Stage 4 or application work.
- **Completed:** Reconciled `AGENTS.md`, `PROJECT_PROGRESS.md`, and `README.md`;
  recorded the locked P0/P1/Later backlog and acceptance criteria, deadline and
  release gates, terminology, scope and scenario rules, deferred decisions, risks,
  milestones, decision log, and Stage 4 handoff; expanded the README only as a
  concise pointer to the canonical tracker.
- **Files changed:** `PROJECT_PROGRESS.md`, `README.md`. No files were created.
- **Verification:** `git diff --check` passed; confirmed 12 required P0 stories,
  one conditional stretch P0 story, 13 acceptance-criteria blocks, continuous
  decisions through D-043, no targeted stale-current-state phrases, branch `main`,
  upstream tracking, and the configured `origin` remote.
- **Handoff:** Await user review. Do not commit, push, or begin Stage 4 until the
  user explicitly approves the checkpoint.

### 2026-08-25 — Reconcile the local and remote progress tracker

- **Objective:** Ensure the canonical tracker reflects all approved product work,
  the local checkpoint, GitHub publication, current operational issue, and the next
  planning stage.
- **Completed:** Confirmed Stage 1 and Stage 2 milestones and constraints; verified
  the public repository and commit history; updated the current snapshot,
  workstream, risks, technical map, verified Git commands, and next-action handoff.
- **Files changed:** `PROJECT_PROGRESS.md`.
- **Verification:** Compared the local `main` history and clean upstream state with
  GitHub's reported commits and reviewed every required tracker section for current
  accuracy.
- **Handoff:** Start Stage 3 by defining and prioritizing P0, P1, and Later user
  stories with testable acceptance criteria; preserve the locked Stage 2
  constraints.

### 2026-08-25 — Publish the Stage 1 and Stage 2 checkpoint to GitHub

- **Objective:** Connect the authorized public GitHub repository and publish all
  completed documentation before Stage 3.
- **Completed:** Verified `swethabarla19/ClimateCapitalAI` ownership and public
  visibility; added it as `origin`; inspected and preserved its one-line README
  commit; merged the histories; and pushed the Stage 1 and locked Stage 2
  checkpoint to `main`.
- **Files changed:** `README.md` added from the remote history;
  `PROJECT_PROGRESS.md` updated with the current repository state.
- **Verification:** Confirmed GitHub admin and push permissions, fetched and
  inspected `origin/main`, completed a non-destructive merge, pushed successfully,
  and configured local `main` to track `origin/main`.
- **Handoff:** Begin Stage 3 with the locked Stage 2 constraints and checkpointed
  documentation.

### 2026-08-25 — Diagnose Stop hook and create documentation checkpoint

- **Objective:** Verify Git/GitHub state, diagnose the exit-127 Stop hook, and
  checkpoint the approved Stage 1 and Stage 2 documentation before Stage 3.
- **Completed:** Identified the `codex-process-jobs` Stop hook's unavailable `node`
  runtime; verified the local repository, `main` branch, author configuration, and
  absent remote; captured `AGENTS.md` and `PROJECT_PROGRESS.md` in the initial local
  checkpoint.
- **Files changed:** `PROJECT_PROGRESS.md`; `AGENTS.md` and `PROJECT_PROGRESS.md`
  added to local version control.
- **Verification:** Reproduced exit 127 for unavailable `node`; inspected hook
  registration and command; checked Git root, branch, status, author, history,
  remotes, and GitHub CLI availability.
- **Handoff:** Obtain an existing GitHub repository URL or explicit authorization
  to create one before adding `origin` or pushing; then begin Stage 3.

### 2026-08-25 — Lock Stage 2 product definition

- **Objective:** Incorporate the historical decision context and analytical
  boundaries, then lock Stage 2 before backlog prioritization.
- **Completed:** Defined the then-named January 2026 Historical Baseline, $125
  million Projects constraint, scenario terminology, rule-derived cohort, binary funding assumption,
  ranking-versus-portfolio distinction, source-vintage policy, City benchmark
  isolation, Gemini boundary, editable inputs, and deferred later-stage decisions.
  D-078 later superseded the plan terminology with Session Reference Plan.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Reconciled the canonical snapshot, next actions, open questions,
  risks, decisions, and handoff against the 12 approved clarifications.
- **Handoff:** Begin Stage 3 by prioritizing P0, P1, and Later user stories with
  acceptance criteria; do not silently reopen the locked Stage 2 constraints.

### 2026-08-24 — Choose the P0 hazard and equity framing

- **Objective:** Decide whether the watershed pilot should prove multi-hazard
  breadth or a coherent first decision domain.
- **Completed:** Selected flood plus equity as the P0 core; kept urban heat as
  optional context or a clearly labeled, evidence-backed co-benefit.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Checked the choice against the existing watershed scope and
  Map → projects → portfolio decision.
- **Handoff:** Define the flood and vulnerability inputs and the evidence threshold
  for displaying a heat co-benefit.

### 2026-08-24 — Select the P0 product journey

- **Objective:** Clarify the primary product journey and how it can expand beyond
  watershed projects.
- **Completed:** Selected Map → projects → portfolio; established that users
  enter inputs before receiving a recommendation; scoped P0 to watershed projects
  and parks as a candidate P1 type.
- **Files changed:** `PROJECT_PROGRESS.md`
- **Verification:** Reconciled the decisions with the repository; no application
  implementation exists yet.
- **Handoff:** Define the P0 map inputs, watershed-project data model, and portfolio
  recommendation rules before choosing the implementation architecture.

### 2026-08-24 — Initialize cross-session project tracking

- **Objective:** Create durable project context that can bridge multiple sessions.
- **Completed:** Created the canonical progress file and agent maintenance rules.
- **Files changed:** `PROJECT_PROGRESS.md`, `AGENTS.md`
- **Verification:** Reviewed the documents for startup guidance, current status,
  actions, decisions, blockers, risks, technical context, and session history.
- **Handoff:** Start with **Project Definition**, then revise **Current Snapshot** and
  **Next Actions** to reflect the agreed direction.
