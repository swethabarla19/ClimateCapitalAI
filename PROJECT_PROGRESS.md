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

- **Last updated:** 2026-08-31
- **Project stage:** Product and Design planning remains complete and locked through
  Stage 4. Architecture Planning began and is intentionally paused before
  Architecture Lock for controlled evidence reconnaissance; this is not a new
  project phase or product reset.
- **Current milestone:** Source-faithful 37-project Watershed raw table loaded to
  BigQuery and independently validated through warehouse SQL; awaiting user review
  before GIS matching or further evidence reconnaissance.
- **Next milestone:** After explicit approval, match all 37 official subproject IDs
  to available Austin GIS geometry while retaining unmatched records and documenting
  every match decision.
- **Working state:** Git repository on main, connected to the public
  swethabarla19/ClimateCapitalAI GitHub repository, with documentation, the source
  registry/fetch foundation, one pinned data-extraction dependency, a fail-closed
  Watershed table extractor, a Git-tracked 37-record source-universe CSV, one
  pinned BigQuery client dependency, a create-only raw loader, durable SQL quality
  checks, and focused validation tests. Two raw PDF snapshots remain ignored
  locally and preserved at their exact Cloud Storage paths; the source-universe CSV
  is preserved in one validated `raw` BigQuery table. No GIS matching, eligibility,
  production pipeline, application, Architecture Lock, or analytical methodology
  exists.
- **Most recent outcome:** Verified
  `climatecapital-ai.raw.watershed_projects_2025_11_21` in `us-central1` with the
  exact nine-column REQUIRED schema, 37 rows, 37 unique project IDs,
  $327,970,000, source-specific row associations, and a full ordered semantic
  fingerprint matching the committed CSV.

## Approved Locks

- **Stage 1 — Deadline and success:** Official deadline September 7, 2026 at
  10:00 a.m. CDT; internal submit window September 6 from 9:30–11:30 a.m. CDT;
  finalist-worthy deployed/tested P0; three-minute core demo expandable to five.
- **Stage 2 — Product definition:** Capital planning analyst persona, Austin
  Watershed historical simulation, January 2026 context, $125 million Projects
  sub-envelope, deterministic authority, rule-derived cohort, full-project
  selection, and strict City benchmark isolation.
- **Stage 3 — Backlog:** Twelve required P0 stories, conditional SP0-1 Compare as
  the first cut, ordered P1, Later scope, acceptance intent, and release gates.
- **Stage 4 — Product and Design Lock:** Required screens and contextual surfaces,
  navigation, UI states/recovery, low-fidelity wireframes, evidence gates, and
  three-minute demo sequence.

Stages 1–4 remain authoritative unless new source evidence creates a material
contradiction. Full details are in docs/product and docs/decisions.md.

The Architecture pause does not reopen ClimateCapital AI, the Austin Watershed P0
pilot, the January 21, 2026 context, the $125 million Projects sub-envelope, the
Map → Projects → Funding Plan journey, deterministic authority, benchmark
isolation, the Gemini boundary, or any other approved Product and Design Lock.

## Current Workstream

- **Goal:** Establish what authoritative, historically valid, comparable evidence
  exists for each of the 37 official Watershed projects before resuming
  Architecture Lock decisions.
- **Status:** The source-ingestion/provenance foundation, raw preservation,
  checksum-gated 37-record extraction, and independently validated source-faithful
  BigQuery raw copy are complete and awaiting review. Architecture Planning remains
  paused; no record has been declared eligible, matched to GIS, classified
  analytically, or used for scoring, optimization, or application work.
- **Owner:** User and Codex.
- **Required reading:** AGENTS.md, this file, the locked files under docs/product,
  docs/delivery/execution-plan.md, docs/decisions.md, and the non-authoritative
  docs/reference/technical-architecture-reference.md; reconnaissance must also use
  preserved authoritative sources with explicit provenance.
- **Exit condition:** A reviewed 37-project evidence matrix provides enough real
  evidence to decide processing boundaries, geospatial needs, data contracts,
  historical snapshot handling, benefit comparability, and methodology parameters;
  Architecture Planning may then resume. Approved architecture files still require
  explicit Architecture Lock.

## Next Actions

1. Review the hardened create-only BigQuery loader, exact live schema, 21 passing
   warehouse quality checks, source-specific rows, semantic fingerprint, tests,
   limitations, and Git diff.
2. Do not begin GIS matching, eligibility, additional evidence work, staging or
   curated tables, or benchmark ingestion until the user explicitly authorizes the
   next task.
3. After explicit authorization, match all 37 official project identifiers to
   available Austin GIS geometry,
   retaining unmatched projects and documenting every match decision.
4. Investigate historically valid project-level flood-hazard and problem-severity
   evidence.
5. Investigate building, structure, and population-exposure evidence.
6. Investigate equity and vulnerability evidence and defensible joins.
7. Build a project-by-project engineering and expected flood-reduction benefit
   evidence inventory without inferring benefit from project/floodplain
   intersection.
8. Determine which projects can defensibly participate in a common flood-priority
   model; preserve exclusions and limitations explicitly without inventing values.
9. Review the resulting 37-project evidence matrix and identify what remains
   incomparable, unavailable, or historically invalid.
10. Use reviewed findings to resume Architecture Planning and decide build-time
    versus runtime work, geospatial processing, data contracts, historical
    snapshots, benefit comparability, and parameters deferred to methodology.
11. Do not resume Architecture Lock, create approved architecture files, or begin
    production analytical implementation until the evidence findings are reviewed.
12. Separately verify organizer submission artifacts, judging criteria, finale
    date, and conditional live-demo format.

## Completed Milestones

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

- Architecture Lock is intentionally blocked pending review of the 37-project
  evidence matrix and, in particular, whether expected flood-reduction evidence is
  sufficiently available and comparable.
- No architecture is approved; this blocks architecture implementation, production
  data pipelines, analytical implementation, and final architecture documents.
- Evidence decisions block implementation of analytical claims, governed metrics,
  weights, confidence warnings, optimization, and default evidence visualizations.
- Official judging criteria, submission artifacts, and conditional live-demo
  details remain unconfirmed and block final submission-package planning.

## Active Risks

- Source-license/reuse terms remain unverified and are recorded as such in the
  source registry.
- BigQuery does not enforce project-ID uniqueness, source sequence, totals, or the
  semantic fingerprint as table constraints. The loader refuses an existing table,
  but any separately authorized mutation by another tool or user requires rerunning
  the durable SQL quality suite before the raw snapshot is trusted.
- The local Python 3.12 installation has no default CA bundle configured; verified
  HTTPS succeeded only when `SSL_CERT_FILE=/etc/ssl/cert.pem` selected the host CA
  bundle. Certificate verification was not disabled.
- Comparable project-level expected flood-reduction evidence may not exist across
  the 37-project universe; project/floodplain intersection cannot substitute for
  benefit evidence.
- Project identifiers, geometry, engineering evidence, hazard evidence, exposure,
  and equity joins may be inconsistent across sources or valid only for different
  historical vintages.
- The source says projects are sorted by project ID, but published row order places
  5789.150 before 5789.145 and 5789.146. Extraction preserves rather than repairs
  this source-level inconsistency.
- The current delivery baseline is at critical schedule risk because no
  Architecture Lock, evidence matrix, application, pipeline, or analytical
  implementation exists as of August 31.
- Required P0 remains ambitious for the September 2 feature freeze; optional scope
  must not erode testing or recovery time.
- Architecture and evidence work are now on the critical path and must stay bounded.
- The final rule-derived cohort, evidence coverage, and geometry may be less
  demo-friendly than expected and must not be manually tuned.
- Unresolved scoring, confidence, missingness, and optimization choices may become
  trust risks if rushed or presented as arbitrary.
- The Historical Decision Snapshot, Historical City Recommendation, current
  confirmed scenario, and immutable Historical Baseline may be confused if the
  locked terminology is not implemented consistently.
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

- What reuse and redistribution terms govern the two registered City documents?
- How stable are the 37 official subproject identifiers across GIS and later
  engineering/evidence sources?
- Which projects have authoritative geometry, and what evidence supports each
  identifier/geometry match?
- Which historically valid hazard, severity, exposure, engineering, benefit,
  equity, and vulnerability fields exist project by project?
- Is expected flood-reduction benefit comparable across enough projects for a
  common priority model, or must projects/metrics remain differentiated?
- Which governed scoring dimensions, transformations, score breakdown,
  optimization objective, and default/editable weights should P0 use?
- How should missing evidence, uncertainty, and confidence affect eligibility,
  scoring, ranking, optimization, and presentation?
- What is the final eligible cohort after documented rules are applied?
- Which evidence vintages and defensible project geometries are available?
- Which portfolio comparison measures are supported?
- What evidence is sufficient for a project-specific heat co-benefit?
- Are People Potentially Benefiting and Implementation Readiness supported metrics?
- Which supported analytical layers should be active in the default Explore map?

### Architecture

- Which architecture choices can be decided from current constraints, and which
  must remain parameterized until the evidence matrix is reviewed?
- What is the smallest low-cost deployable system that satisfies required P0?
- Which work is precomputed versus performed at runtime?
- What governed contract separates deterministic analysis, UI, Historical
  Benchmark, and Gemini?
- Which Google Cloud, Gemini, frontend, map, storage, and deployment options meet
  deadline, cost, security, and reliability constraints?
- What data-versioning, lineage, observability, and teardown approach is required?

### Submission

- What are the official submission artifacts, judging criteria, finale date, and
  live-demo format?

There are no unresolved Stage 4 screen, navigation, state, wireframe, or demo
sequence decisions.

## Technical Map

### Architecture

Not established. Architecture Planning is paused before lock for 37-project
evidence reconnaissance. The technical reference remains exploratory and does not
constitute an Architecture Lock.

### Evidence Repository

The minimal foundation is established:

- data/metadata/source_registry.csv — canonical Git-tracked source metadata with
  the two authoritative sources, roles, vintages, caveats, retrieval timestamps,
  and exact-byte SHA-256 checksums.
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
- data/staging/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf —
  ignored local raw source-universe snapshot.
- data/staging/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf —
  ignored local benchmark-only snapshot.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/watershed_bond_projects/2025-11-21/source.pdf#1788210198102506 — verified cloud source-universe snapshot, 1,151,348 bytes, SHA-256 `d1c2731cc12ecb3938569d29ec0c92d0966d7706af919e0a519b48329493d88e`.
- gs://climatecapital-ai-raw-swetha/raw/city_austin/initial_draft_recommendation/2026-01-21/source.pdf#1788210202820922 — verified cloud benchmark-only snapshot, 412,820 bytes, SHA-256 `da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359`.
- climatecapital-ai.raw.watershed_projects_2025_11_21 — source-faithful BigQuery
  raw table in `us-central1`, with 37 REQUIRED-schema rows and 21 passing SQL
  quality checks.

The ordered raw-table schema is `source_id STRING REQUIRED`,
`source_pdf_page INTEGER REQUIRED`, `source_table_row_order INTEGER REQUIRED`,
`map_label STRING REQUIRED`, `subproject_id STRING REQUIRED`,
`project_name STRING REQUIRED`,
`current_funding_request_estimate_source STRING REQUIRED`,
`current_funding_request_estimate_dollars INTEGER REQUIRED`, and
`council_districts_source STRING REQUIRED`.

The 37 official source rows above have been extracted and loaded only to the raw
table. No eligibility result, GIS match, analytical classification, evidence
matrix, score, optimization result, staging/curated table, or benchmark table has
been created. No Cloud Storage objects beyond the two raw source objects above have
been created. Benchmark isolation remains explicit.

### Repository Structure

- AGENTS.md — repository rules and task-start routing.
- PROJECT_PROGRESS.md — sole current state/progress/handoff document.
- README.md — repository landing page and documentation map.
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
- scripts/data/fetch_sources.py — minimal reproducible source downloader.
- scripts/data/extract_watershed_projects.py — deterministic source-universe
  extractor and reconciliation CLI.
- scripts/data/load_watershed_projects_bigquery.py — guarded raw BigQuery loader.
- sql/quality/watershed_projects_raw_checks.sql — read-only warehouse data-quality
  suite.
- tests/test_source_ingestion.py — lightweight source-ingestion validation suite.
- tests/test_watershed_project_extraction.py — source extraction and failure-path
  validation suite.
- tests/test_watershed_bigquery_loader.py — non-destructive raw-loader contract and
  safety tests.
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
  has the exact governed schema and 37 rows. No existing cloud data, infrastructure,
  IAM, dataset/bucket settings, or credentials were changed; staging, curated, and
  benchmark datasets/tables were not inspected.
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
- D-067 pauses Architecture Lock for controlled evidence reconnaissance without
  reopening the approved product.
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
- Next available decision ID: **D-073**.

## Verification Record

Record only checks that were actually run. Newest entries go first.

| Date | Scope | Command or Check | Result |
| --- | --- | --- | --- |
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
- **Completed:** Defined the January 2026 Historical Baseline, $125 million Projects
  constraint, scenario terminology, rule-derived cohort, binary funding assumption,
  ranking-versus-portfolio distinction, source-vintage policy, City benchmark
  isolation, Gemini boundary, editable inputs, and deferred later-stage decisions.
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
