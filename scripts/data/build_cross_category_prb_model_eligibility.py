#!/usr/bin/env python3
"""Build the governed M3.7E-B cross-category PRB model-eligibility overlay."""

from __future__ import annotations

import argparse
import json
from decimal import Decimal
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

MODEL_SCOPE = "CROSS_CATEGORY_PRB_PROJECT_MODEL"
ARTIFACT_VERSION = "m3.7e-b-cross-category-prb-model-eligibility/1.0.0"

EXPECTED_PROJECT_COUNT = 106
EXPECTED_ELIGIBLE_COUNT = 106
EXPECTED_CONFLICT_ELIGIBLE_COUNT = 3
EXPECTED_WITHOUT_RECOMMENDATION_COUNT = 86
EXPECTED_HALF_POINT_COUNT = 3
EXPECTED_MODEL_REQUEST_TOTAL = 1_973_520_000

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}

ALLOWED_RECONCILIATION_STATUSES = {
    "EXACT_GOVERNED_JANUARY_NAME_MATCH",
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

SOURCE_ROW_PATHS = {
    "Transportation": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "transportation.json"
    ),
    "Parks & Open Space": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "parks.json"
    ),
    "Watershed": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "watershed.json"
    ),
    "Community Facilities": (
        REPOSITORY_ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "community_facilities.json"
    ),
}

DEFAULT_RECONCILIATION_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "cross-category-prb-model-eligibility.json"
)


class EligibilityError(RuntimeError):
    """Raised when model eligibility cannot be evaluated without guessing."""


class DerivedArtifactConflictError(EligibilityError):
    """Raised when a differing governed eligibility artifact exists."""


def load_json(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def decimal_value(value: object) -> Decimal:
    return Decimal(str(value))


def is_half_point(value: object) -> bool:
    number = decimal_value(value)
    doubled = number * Decimal("2")

    return (
        doubled == doubled.to_integral_value()
        and number != number.to_integral_value()
    )


def load_analytical_projects() -> dict[str, dict[str, object]]:
    projects: dict[str, dict[str, object]] = {}

    for category, path in SOURCE_ROW_PATHS.items():
        rows = load_json(path)

        if not isinstance(rows, list):
            raise EligibilityError(
                f"{path} must contain a JSON list."
            )

        category_projects = [
            row
            for row in rows
            if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
        ]

        expected = EXPECTED_CATEGORY_COUNTS[category]

        if len(category_projects) != expected:
            raise EligibilityError(
                f"{category}: expected {expected} analytical projects; "
                f"found {len(category_projects)}."
            )

        for project in category_projects:
            decision_unit_id = str(
                project["decision_unit_id"]
            )

            if decision_unit_id in projects:
                raise EligibilityError(
                    f"Duplicate decision_unit_id: {decision_unit_id}"
                )

            projects[decision_unit_id] = project

    if len(projects) != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_PROJECT_COUNT} analytical projects; "
            f"found {len(projects)}."
        )

    return projects


def load_reconciliation(
    path: Path,
) -> dict[str, dict[str, object]]:
    artifact = load_json(path)

    if not isinstance(artifact, dict):
        raise EligibilityError(
            "M3.7E-A reconciliation must contain a JSON object."
        )

    if artifact.get("governance_checkpoint") != "M3.7E-A":
        raise EligibilityError(
            "Eligibility requires governed M3.7E-A reconciliation."
        )

    if (
        artifact.get("artifact_scope")
        != "CROSS_CATEGORY_PRB_RECONCILIATION"
    ):
        raise EligibilityError(
            "Unexpected M3.7E-A artifact scope."
        )

    for flag in (
        "cross_category_ranking_authorized",
        "portfolio_selection_authorized",
        "runtime_integration_authorized",
    ):
        if artifact.get(flag) is not False:
            raise EligibilityError(
                f"M3.7E-A unexpectedly authorizes {flag}."
            )

    records = artifact.get("records")

    if not isinstance(records, list):
        raise EligibilityError(
            "M3.7E-A reconciliation has no records list."
        )

    by_id: dict[str, dict[str, object]] = {}

    for record in records:
        decision_unit_id = str(
            record["decision_unit_id"]
        )

        if decision_unit_id in by_id:
            raise EligibilityError(
                f"Duplicate reconciliation ID: {decision_unit_id}"
            )

        by_id[decision_unit_id] = record

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
    decision_unit_id = str(
        project["decision_unit_id"]
    )

    evidence_reason_codes: list[str] = []
    model_reason_codes: list[str] = []
    blocking_reason_codes: list[str] = []

    identity_reconciled = (
        reconciliation is not None
        and reconciliation.get("reconciliation_status")
        in ALLOWED_RECONCILIATION_STATUSES
        and reconciliation.get("decision_unit_id")
        == decision_unit_id
    )

    if identity_reconciled:
        evidence_reason_codes.append(
            "RECONCILED_GOVERNED_IDENTITY"
        )
    else:
        blocking_reason_codes.append(
            "UNRECONCILED_GOVERNED_IDENTITY"
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
            (
                decimal_value(
                    reconciliation[field]
                )
                for field in COMPONENT_FIELDS
            ),
            Decimal("0"),
        )

        reconciled_total = reconciliation.get(
            "prb_grand_total"
        )

        governed_total = project.get(
            "prb_score"
        )

        valid_grand_total = (
            reconciled_total is not None
            and governed_total is not None
            and component_sum
            == decimal_value(reconciled_total)
            and decimal_value(reconciled_total)
            == decimal_value(governed_total)
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

    model_request = (
        reconciliation.get("model_request_dollars")
        if reconciliation is not None
        else None
    )

    usable_model_request = (
        model_request is not None
        and int(model_request) > 0
    )

    if usable_model_request:
        model_reason_codes.append(
            "USABLE_GOVERNED_MODEL_REQUEST"
        )
    else:
        blocking_reason_codes.append(
            "MISSING_USABLE_GOVERNED_MODEL_REQUEST"
        )

    model_eligible = (
        analytical_project
        and evidence_feasible
        and usable_model_request
    )

    january_recommendation_present = (
        reconciliation is not None
        and reconciliation.get(
            "january_recommendation_dollars"
        )
        is not None
    )

    source_conflict = bool(
        reconciliation.get("source_conflict_flag")
        if reconciliation is not None
        else False
    )

    request_conflict = bool(
        reconciliation.get("request_version_conflict")
        if reconciliation is not None
        else False
    )

    return {
        "decision_unit_id": decision_unit_id,
        "canonical_project_id": (
            reconciliation.get("canonical_project_id")
            if reconciliation is not None
            else None
        ),
        "presentation_category": str(
            project["presentation_category"]
        ),
        "model_scope": MODEL_SCOPE,
        "evidence_feasibility_status": (
            evidence_feasibility_status
        ),
        "model_eligible": model_eligible,
        "evidence_reason_codes": evidence_reason_codes,
        "model_eligibility_reason_codes": (
            model_reason_codes
        ),
        "blocking_reason_codes": sorted(
            set(blocking_reason_codes)
        ),
        "model_request_dollars": (
            int(model_request)
            if model_request is not None
            else None
        ),
        "model_request_authority": (
            reconciliation.get("model_request_authority")
            if reconciliation is not None
            else None
        ),
        "prb_grand_total": (
            reconciliation.get("prb_grand_total")
            if reconciliation is not None
            else None
        ),
        "source_conflict_flag": source_conflict,
        "request_version_conflict": request_conflict,
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
            "Analytical-project IDs do not exactly match "
            "M3.7E-A reconciliation IDs. "
            f"Missing={sorted(project_ids - reconciliation_ids)}; "
            f"unexpected={sorted(reconciliation_ids - project_ids)}"
        )

    return tuple(
        evaluate_project(
            projects[decision_unit_id],
            reconciliation[decision_unit_id],
        )
        for decision_unit_id in sorted(projects)
    )


def validate_records(
    records: tuple[dict[str, object], ...],
) -> dict[str, object]:
    if len(records) != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_PROJECT_COUNT} eligibility records; "
            f"found {len(records)}."
        )

    ids = [
        str(record["decision_unit_id"])
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise EligibilityError(
            "Eligibility decision_unit_ids are not unique."
        )

    category_counts = {
        category: sum(
            record["presentation_category"] == category
            for record in records
        )
        for category in EXPECTED_CATEGORY_COUNTS
    }

    if category_counts != EXPECTED_CATEGORY_COUNTS:
        raise EligibilityError(
            f"Category counts changed: {category_counts}"
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

    eligible_with_conflict_count = sum(
        record["model_eligible"] is True
        and record["source_conflict_flag"] is True
        for record in records
    )

    eligible_without_recommendation_count = sum(
        record["model_eligible"] is True
        and record["january_recommendation_present"] is False
        for record in records
    )

    model_request_total = sum(
        int(record["model_request_dollars"])
        for record in records
        if record["model_request_dollars"] is not None
    )

    half_point_count = sum(
        is_half_point(
            record["prb_grand_total"]
        )
        for record in records
    )

    if evidence_feasible_count != EXPECTED_PROJECT_COUNT:
        raise EligibilityError(
            "Current evidence does not produce 106/106 FEASIBLE projects."
        )

    if eligible_count != EXPECTED_ELIGIBLE_COUNT:
        raise EligibilityError(
            f"Expected {EXPECTED_ELIGIBLE_COUNT} model-eligible projects; "
            f"found {eligible_count}."
        )

    if (
        eligible_with_conflict_count
        != EXPECTED_CONFLICT_ELIGIBLE_COUNT
    ):
        raise EligibilityError(
            "Eligible source-conflict count changed unexpectedly."
        )

    if (
        eligible_without_recommendation_count
        != EXPECTED_WITHOUT_RECOMMENDATION_COUNT
    ):
        raise EligibilityError(
            "Recommendation-independent eligibility count "
            "changed unexpectedly."
        )

    if half_point_count != EXPECTED_HALF_POINT_COUNT:
        raise EligibilityError(
            "Half-point eligibility count changed unexpectedly."
        )

    if model_request_total != EXPECTED_MODEL_REQUEST_TOTAL:
        raise EligibilityError(
            f"Model request total changed: ${model_request_total:,}"
        )

    if any(
        record["blocking_reason_codes"]
        for record in records
    ):
        raise EligibilityError(
            "The governed 106-project cohort must have "
            "no blocking eligibility reasons."
        )

    return {
        "analytical_project_count": len(records),
        "category_counts": category_counts,
        "evidence_feasible_count": evidence_feasible_count,
        "model_eligible_count": eligible_count,
        "model_ineligible_count": (
            len(records) - eligible_count
        ),
        "eligible_with_source_version_conflict_count": (
            eligible_with_conflict_count
        ),
        "eligible_without_january_recommendation_count": (
            eligible_without_recommendation_count
        ),
        "half_point_project_count": half_point_count,
        "model_request_total_dollars": model_request_total,
    }


def render_artifact(
    records: tuple[dict[str, object], ...],
    summary: dict[str, object],
) -> bytes:
    artifact = {
        "artifact_version": ARTIFACT_VERSION,
        "governance_checkpoint": "M3.7E-B",
        "historical_decision_snapshot_date": "2026-01-21",
        "model_scope": MODEL_SCOPE,
        "cross_category_ranking_authorized": False,
        "portfolio_selection_authorized": False,
        "runtime_integration_authorized": False,
        "source_artifacts": {
            "structural_universe": (
                "data/governed/cross_category/source_rows/"
            ),
            "prb_reconciliation": (
                "data/governed/cross_category/reconciliation/"
                "cross-category-prb-reconciliation.json"
            ),
        },
        "eligibility_policy": {
            "evidence_requirements": [
                "RECONCILED_GOVERNED_IDENTITY",
                "COMPLETE_PRB_COMPONENT_VECTOR",
                "VALID_PRB_GRAND_TOTAL",
            ],
            "model_requirements": [
                "ANALYTICAL_PROJECT",
                "EVIDENCE_FEASIBLE",
                "USABLE_GOVERNED_MODEL_REQUEST",
            ],
            "non_blocking_provenance_conditions": [
                "SOURCE_VERSION_CONFLICT",
                "REQUEST_VERSION_CONFLICT",
                "NO_JANUARY_RECOMMENDATION",
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
            "Refusing to overwrite differing governed "
            f"cross-category eligibility artifact: {output_path}"
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

    projects = load_analytical_projects()

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

    print(
        "M3.7E-B Cross-Category PRB Model Eligibility"
    )

    print(
        "Analytical projects: "
        f"{summary['analytical_project_count']}"
    )

    print(
        "Evidence FEASIBLE: "
        f"{summary['evidence_feasible_count']}/106"
    )

    print(
        "Model eligible: "
        f"{summary['model_eligible_count']}/106"
    )

    print(
        "Model ineligible: "
        f"{summary['model_ineligible_count']}"
    )

    print(
        "Eligible with source-version conflict: "
        f"{summary['eligible_with_source_version_conflict_count']}"
    )

    print(
        "Eligible without January recommendation: "
        f"{summary['eligible_without_january_recommendation_count']}"
    )

    print(
        "Half-point projects: "
        f"{summary['half_point_project_count']}"
    )

    print(
        "Model request total: "
        f"${summary['model_request_total_dollars']:,}"
    )

    print(
        "Cross-category ranking authorized: false"
    )

    print(
        "Portfolio selection authorized: false"
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