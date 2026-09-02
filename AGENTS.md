# Repository Instructions

## Repository Memory Model

Treat Markdown in this repository as durable memory between otherwise independent
Codex tasks. Git is the version history; chat history is not a source of truth.

Source hierarchy:

- **AGENTS.md** — repository-wide working rules and task-start instructions.
- **PROJECT_PROGRESS.md** — canonical current state, stage, progress, blockers,
  current risks, open questions, milestones, and handoff.
- **docs/methodology/** — authoritative analytical methodology only after explicit
  Methodology Lock.
- **docs/product/** — authoritative approved product and design specifications.
- **docs/architecture/** — authoritative architecture only after explicit
  Architecture Lock.
- **docs/delivery/** — approved implementation, testing, sequencing, and milestone
  plans.
- **docs/reference/** — supporting material that is not authoritative unless an
  approved document explicitly adopts it.
- **docs/decisions.md** — authoritative durable decision history.
- Git — version history for all of the above.

Do not create **docs/delivery/progress.md** or any second progress tracker.

## Cross-Session Continuity

Before planning or changing the project:

1. Read **PROJECT_PROGRESS.md** completely.
2. Reconcile it with the actual repository; repository state wins if they differ.
3. Read the authoritative files linked for the active task.
4. Use **Next Actions** as the default priority unless the user says otherwise.

Task-specific minimum reading:

- **Architecture planning:** AGENTS.md, PROJECT_PROGRESS.md, docs/methodology/,
  docs/product/, docs/delivery/execution-plan.md, docs/decisions.md, and
  docs/reference/technical-architecture-reference.md.
- **Delivery planning after Architecture Lock:** all relevant approved files under
  docs/, plus AGENTS.md and PROJECT_PROGRESS.md.
- **Implementation milestones:** AGENTS.md, PROJECT_PROGRESS.md,
  docs/delivery/implementation-plan.md, docs/delivery/test-plan.md,
  docs/delivery/milestones.md, and the relevant approved methodology, product, and
  architecture specifications.

Before ending a work session, update PROJECT_PROGRESS.md wherever the session
changed the current snapshot, workstream, next actions, milestones, blockers,
risks, open questions, verification record, technical map, or session log. Keep
the session log newest-first and preserve historical entries.

Record durable decisions in docs/decisions.md using the next sequential ID. Do not
renumber existing decisions. Update a purpose-specific authoritative document only
when the work legitimately changes its approved specification; do not duplicate
the same detailed material into PROJECT_PROGRESS.md.

After an implementation milestone, record in PROJECT_PROGRESS.md:

- work completed;
- tests and results;
- files/components changed;
- deviations from plan;
- unresolved issues and new risks;
- decision IDs created, if any; and
- recommended next milestone.

Never record secrets, credentials, tokens, or sensitive personal data in
repository documentation.
