#!/usr/bin/env python3
"""Build the governed M3.7B Watershed PRB-model eligibility overlay."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

MODEL_SCOPE = "WATERSHED_PRB_PROJECT_MODEL"
ARTIFACT_VERSION = "m3.7b-watershed-prb-model-eligibility/1.0.0"

EXPECTED_PROJECT_COUNT = 37
EXPECTED_ELIGIBLE_COUNT = 37
EXPECTED_REQUEST_CONFLICT_ELIGIBLE_COUNT = 1
EXPECTED_NO_RECOMMENDATION_ELIGIBLE_COUNT = 25

ALLOWED_RECONCILIATION_STATUSES = {
    "EXACT_NAME_MATCH",
    "GOVERNED_SOURCE_VERSION_MATCH",
}

COMPONENT_FIELDS = (
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
)

DEFAULT_WATERSHED_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "source_rows"
    / "watershed.json"
)

DEFAULT_RECONCILIATION_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "watershed-prb-reconciliation.json"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "watershed-prb-model-eligibility.json"
)


class EligibilityError(RuntimeError):
    """Raised when eligibility cannot be evaluated without guessing."""


class DerivedArtifactConflictError(EligibilityError):
    """Raised when a differing governed eligibility artifact exists."""


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def load_analytical_projects(
    watershed_path: Path,
) -> dict[str, dict[str, object]]:
    rows = load_json(watershed_path)

    if not isinstance(rows, list):
        raise EligibilityError(
            "Watershed source-row artifact must contain a JSON list."
        )

    projects = {}

    for row in rows:
        if row["analytical_unit_type"] != "ANALYTICAL_PROJECT":
            continue

        project_id = row.get("canonical_project_id")

        if not project_id:
            raise EligibilityError(
                "Watershed analytical project is missing canonical_project_id."
            )

        if project_id in projects:
            raise EligibilityError(
                f"Duplicate canonical project ID: {project_id}"
            )

        projects[project_id] = row

    if len(projects) != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_PROJECT_COUNT} Watershed analytical "
            f"projects; found {len(projects)}."
        )

    return projects


def load_reconciliation(
    reconciliation_path: Path,
) -> dict[str, dict[str, object]]:
    artifact = load_json(reconciliation_path)

    if not isinstance(artifact, dict):
        raise EligibilityError(
            "M3.7A reconciliation artifact must contain a JSON object."
        )

    if artifact.get("governance_checkpoint") != "M3.7A":
        raise EligibilityError(
            "Eligibility requires the governed M3.7A reconciliation artifact."
        )

    records = artifact.get("records")

    if not isinstance(records, list):
        raise EligibilityError(
            "M3.7A reconciliation artifact has no record list."
        )

    by_id = {}

    for record in records:
        project_id = record["canonical_project_id"]

        if project_id in by_id:
            raise EligibilityError(
                f"Duplicate reconciliation canonical ID: {project_id}"
            )

        by_id[project_id] = record

    if len(by_id) != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_PROJECT_COUNT} reconciliation records; "
            f"found {len(by_id)}."
        )

    return by_id


def evaluate_project(
    project: dict[str, object],
    reconciliation: dict[str, object] | None,
) -> dict[str, object]:
    project_id = str(project["canonical_project_id"])

    evidence_reason_codes: list[str] = []
    model_reason_codes: list[str] = []
    blocking_reason_codes: list[str] = []

    # Evidence feasibility:
    # 1. governed identity must reconcile,
    # 2. all six official PRB components must exist,
    # 3. components must reproduce the governed PRB Grand Total.
    identity_reconciled = (
        reconciliation is not None
        and reconciliation.get("reconciliation_status")
        in ALLOWED_RECONCILIATION_STATUSES
    )

    if identity_reconciled:
        evidence_reason_codes.append(
            "RECONCILED_CANONICAL_IDENTITY"
        )
    else:
        blocking_reason_codes.append(
            "UNRECONCILED_CANONICAL_IDENTITY"
        )

    complete_components = (
        reconciliation is not None
        and all(
            reconciliation.get(field) is not None
            for field in COMPONENT_FIELDS
        )
    )

    if complete_components:
        evidence_reason_codes.append(
            "COMPLETE_PRB_COMPONENT_VECTOR"
        )
    else:
        blocking_reason_codes.append(
            "INCOMPLETE_PRB_COMPONENT_VECTOR"
        )

    valid_grand_total = False

    if complete_components and reconciliation is not None:
        component_sum = sum(
            int(reconciliation[field])
            for field in COMPONENT_FIELDS
        )

        reconciled_total = reconciliation.get(
            "prb_grand_total"
        )

        governed_total = project.get("prb_score")

        valid_grand_total = (
            reconciled_total is not None
            and governed_total is not None
            and component_sum == int(reconciled_total)
            and int(reconciled_total) == int(governed_total)
        )

    if valid_grand_total:
        evidence_reason_codes.append(
            "VALID_PRB_GRAND_TOTAL"
        )
    else:
        blocking_reason_codes.append(
            "INVALID_PRB_GRAND_TOTAL"
        )

    evidence_feasible = (
        identity_reconciled
        and complete_components
        and valid_grand_total
    )

    evidence_feasibility_status = (
        "FEASIBLE"
        if evidence_feasible
        else "INFEASIBLE"
    )

    # Model eligibility:
    # The record must be an analytical project, evidence-feasible,
    # and have a usable canonical November request amount.
    analytical_project = (
        project.get("analytical_unit_type")
        == "ANALYTICAL_PROJECT"
        and project.get("analytical_unit") is True
    )

    if analytical_project:
        model_reason_codes.append(
            "ANALYTICAL_PROJECT"
        )
    else:
        blocking_reason_codes.append(
            "NOT_ANALYTICAL_PROJECT"
        )

    if evidence_feasible:
        model_reason_codes.append(
            "EVIDENCE_FEASIBLE"
        )

    canonical_request = (
        reconciliation.get("november_request_dollars")
        if reconciliation is not None
        else None
    )

    usable_canonical_request = (
        canonical_request is not None
        and int(canonical_request) > 0
    )

    if usable_canonical_request:
        model_reason_codes.append(
            "USABLE_CANONICAL_REQUEST"
        )
    else:
        blocking_reason_codes.append(
            "MISSING_USABLE_CANONICAL_REQUEST"
        )

    model_eligible = (
        analytical_project
        and evidence_feasible
        and usable_canonical_request
    )

    request_version_conflict = (
        bool(reconciliation.get("request_version_conflict"))
        if reconciliation is not None
        else False
    )

    january_recommendation_present = (
        reconciliation is not None
        and reconciliation.get(
            "january_recommendation_dollars"
        )
        is not None
    )

    return {
        "canonical_project_id": project_id,
        "model_scope": MODEL_SCOPE,
        "evidence_feasibility_status": (
            evidence_feasibility_status
        ),
        "model_eligible": model_eligible,
        "evidence_reason_codes": evidence_reason_codes,
        "model_eligibility_reason_codes": (
            model_reason_codes
        ),
        "blocking_reason_codes": (
            sorted(set(blocking_reason_codes))
        ),
        "canonical_request_dollars": (
            int(canonical_request)
            if canonical_request is not None
            else None
        ),
        "prb_grand_total": (
            int(reconciliation["prb_grand_total"])
            if reconciliation is not None
            and reconciliation.get("prb_grand_total")
            is not None
            else None
        ),
        "request_version_conflict": (
            request_version_conflict
        ),
        "january_recommendation_present": (
            january_recommendation_present
        ),
    }


def build_records(
    projects: dict[str, dict[str, object]],
    reconciliation: dict[str, dict[str, object]],
) -> tuple[dict[str, object], ...]:
    project_ids = set(projects)
    reconciliation_ids = set(reconciliation)

    if project_ids != reconciliation_ids:
        raise EligibilityError(
            "Watershed analytical-project IDs do not exactly match "
            "M3.7A reconciliation IDs. "
            f"Missing reconciliation="
            f"{sorted(project_ids - reconciliation_ids)}; "
            f"unexpected reconciliation="
            f"{sorted(reconciliation_ids - project_ids)}"
        )

    return tuple(
        evaluate_project(
            projects[project_id],
            reconciliation.get(project_id),
        )
        for project_id in projects
    )


def validate_records(
    records: tuple[dict[str, object], ...],
) -> dict[str, int]:
    if len(records) != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_PROJECT_COUNT} eligibility records; "
            f"found {len(records)}."
        )

    ids = [
        str(record["canonical_project_id"])
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise EligibilityError(
            "Eligibility canonical project IDs are not unique."
        )

    evidence_feasible_count = sum(
        record["evidence_feasibility_status"]
        == "FEASIBLE"
        for record in records
    )

    eligible_count = sum(
        record["model_eligible"] is True
        for record in records
    )

    ineligible_count = (
        len(records) - eligible_count
    )

    eligible_with_request_conflict_count = sum(
        record["model_eligible"] is True
        and record["request_version_conflict"] is True
        for record in records
    )

    eligible_without_recommendation_count = sum(
        record["model_eligible"] is True
        and record["january_recommendation_present"] is False
        for record in records
    )

    if evidence_feasible_count != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            "Current governed Watershed evidence does not produce "
            "37/37 FEASIBLE projects."
        )

    if eligible_count != EXPECTED_ELIGIBLE_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_ELIGIBLE_COUNT} PRB-model eligible "
            f"projects; found {eligible_count}."
        )

    if (
        eligible_with_request_conflict_count
        != EXPECTED_REQUEST_CONFLICT_ELIGIBLE_COUNT
    ):
        raise EligibilityError(
            "Request-conflict eligibility count changed unexpectedly."
        )

    if (
        eligible_without_recommendation_count
        != EXPECTED_NO_RECOMMENDATION_ELIGIBLE_COUNT
    ):
        raise EligibilityError(
            "Recommendation-independent eligibility count changed "
            "unexpectedly."
        )

    if any(
        record["blocking_reason_codes"]
        for record in records
    ):
        raise EligibilityError(
            "Current 37/37 governed Watershed cohort must have "
            "no blocking eligibility reasons."
        )

    return {
        "analytical_project_count": len(records),
        "evidence_feasible_count": (
            evidence_feasible_count
        ),
        "model_eligible_count": eligible_count,
        "model_ineligible_count": ineligible_count,
        "eligible_with_request_version_conflict_count": (
            eligible_with_request_conflict_count
        ),
        "eligible_without_january_recommendation_count": (
            eligible_without_recommendation_count
        ),
    }


def render_artifact(
    records: tuple[dict[str, object], ...],
    summary: dict[str, int],
) -> bytes:
    artifact = {
        "artifact_version": ARTIFACT_VERSION,
        "governance_checkpoint": "M3.7B",
        "historical_decision_snapshot_date": "2026-01-21",
        "model_scope": MODEL_SCOPE,
        "runtime_integration_authorized": False,
        "source_artifacts": {
            "structural_universe": (
                "data/governed/cross_category/"
                "source_rows/watershed.json"
            ),
            "prb_reconciliation": (
                "data/governed/cross_category/"
                "reconciliation/"
                "watershed-prb-reconciliation.json"
            ),
        },
        "eligibility_policy": {
            "evidence_requirements": [
                "RECONCILED_CANONICAL_IDENTITY",
                "COMPLETE_PRB_COMPONENT_VECTOR",
                "VALID_PRB_GRAND_TOTAL",
            ],
            "model_requirements": [
                "ANALYTICAL_PROJECT",
                "EVIDENCE_FEASIBLE",
                "USABLE_CANONICAL_REQUEST",
            ],
            "contextual_evidence_not_required": [
                "RNA_GEOMETRY",
                "FEMA_FLOODPLAIN_CONTEXT",
                "EAZ_2021_CONTEXT",
                "WATERSHED_PROBLEM_SCORE_CONTEXT",
            ],
            "benchmark_outcome_not_used": [
                "JANUARY_INITIAL_RECOMMENDATION",
            ],
        },
        "summary": summary,
        "records": list(records),
    }

    return (
        json.dumps(
            artifact,
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    ).encode("utf-8")


def write_artifact(
    output_path: Path,
    content: bytes,
) -> str:
    if output_path.exists():
        existing = output_path.read_bytes()

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite differing governed eligibility "
            f"artifact: {output_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_bytes(content)

    return "created"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--watershed-path",
        type=Path,
        default=DEFAULT_WATERSHED_PATH,
    )

    parser.add_argument(
        "--reconciliation-path",
        type=Path,
        default=DEFAULT_RECONCILIATION_PATH,
    )

    parser.add_argument(
        "--output-path",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
    )

    parser.add_argument(
        "--verify-only",
        action="store_true",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    projects = load_analytical_projects(
        args.watershed_path
    )

    reconciliation = load_reconciliation(
        args.reconciliation_path
    )

    records = build_records(
        projects,
        reconciliation,
    )

    summary = validate_records(
        records
    )

    print("M3.7B Watershed PRB-model eligibility")
    print(
        "Analytical projects: "
        f"{summary['analytical_project_count']}"
    )
    print(
        "Evidence feasible: "
        f"{summary['evidence_feasible_count']}/37"
    )
    print(
        "PRB-model eligible: "
        f"{summary['model_eligible_count']}/37"
    )
    print(
        "PRB-model ineligible: "
        f"{summary['model_ineligible_count']}"
    )
    print(
        "Eligible despite request-version conflict: "
        f"{summary['eligible_with_request_version_conflict_count']}"
    )
    print(
        "Eligible without January recommendation: "
        f"{summary['eligible_without_january_recommendation_count']}"
    )
    print(
        "Runtime integration authorized: false"
    )

    if args.verify_only:
        print(
            "Verify-only mode: "
            "no governed eligibility artifact written."
        )
        return 0

    content = render_artifact(
        records,
        summary,
    )

    result = write_artifact(
        args.output_path,
        content,
    )

    print(
        "Governed eligibility artifact: "
        f"{result}: {args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
