#!/usr/bin/env python3
"""Build the governed M3.7E-A cross-category PRB reconciliation artifact."""

from __future__ import annotations

import argparse
import csv
import json
from decimal import Decimal
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]

JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
NOV_WATERSHED_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"

ARTIFACT_VERSION = "m3.7e-a-cross-category-prb-reconciliation/1.0.0"

EXPECTED_PROJECT_COUNT = 106

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}

EXPECTED_NON_WATERSHED_COUNT = 69
EXPECTED_WATERSHED_COUNT = 37

EXPECTED_MODEL_REQUEST_TOTAL = 1_973_520_000
EXPECTED_JANUARY_REQUEST_TOTAL = 1_973_645_000
EXPECTED_RECOMMENDATION_TOTAL = 332_000_000
EXPECTED_RECOMMENDATION_PRESENT_COUNT = 20

EXPECTED_SOURCE_CONFLICT_IDS = {
    "watershed/5754.149",
    "community-facilities/acme/george-washington-carver-museum",
    "community-facilities/library/colony-park-branch-library",
}

EXPECTED_HALF_POINT_IDS = {
    "community-facilities/ems/station-03",
    "community-facilities/ems/station-14",
    "community-facilities/fleet/consolidated-service-center",
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

DEFAULT_WATERSHED_RECONCILIATION_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "watershed-prb-reconciliation.json"
)

DEFAULT_NON_WATERSHED_SCORE_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "non_watershed_prb_scores.csv"
)

DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)


class ReconciliationError(RuntimeError):
    """Raised when cross-category reconciliation cannot proceed safely."""


class DerivedArtifactConflictError(ReconciliationError):
    """Raised when a differing governed artifact would be overwritten."""


def load_json(path: Path) -> object:
    return json.loads(
        path.read_text(encoding="utf-8")
    )


def numeric_value(value: str | int | float | Decimal) -> int | float:
    decimal_value = Decimal(str(value))

    if decimal_value == decimal_value.to_integral_value():
        return int(decimal_value)

    return float(decimal_value)


def decimal_value(value: object) -> Decimal:
    return Decimal(str(value))


def load_analytical_projects() -> dict[str, dict[str, object]]:
    projects: dict[str, dict[str, object]] = {}

    for category, path in SOURCE_ROW_PATHS.items():
        rows = load_json(path)

        if not isinstance(rows, list):
            raise ReconciliationError(
                f"{path} must contain a JSON list."
            )

        category_projects = [
            row
            for row in rows
            if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
        ]

        expected_count = EXPECTED_CATEGORY_COUNTS[category]

        if len(category_projects) != expected_count:
            raise ReconciliationError(
                f"{category}: expected {expected_count} analytical "
                f"projects; found {len(category_projects)}."
            )

        for project in category_projects:
            decision_unit_id = str(project["decision_unit_id"])

            if decision_unit_id in projects:
                raise ReconciliationError(
                    f"Duplicate decision_unit_id: {decision_unit_id}"
                )

            if project["analytical_unit"] is not True:
                raise ReconciliationError(
                    f"{decision_unit_id} must remain an analytical unit."
                )

            if project["prb_scored"] is not True:
                raise ReconciliationError(
                    f"{decision_unit_id} must remain PRB-scored."
                )

            if project["prb_score"] is None:
                raise ReconciliationError(
                    f"{decision_unit_id} has no governed PRB Grand Total."
                )

            request = project.get("department_request_dollars")

            if request is None or int(request) <= 0:
                raise ReconciliationError(
                    f"{decision_unit_id} has no usable request amount."
                )

            if project["presentation_category"] != category:
                raise ReconciliationError(
                    f"{decision_unit_id} presentation category changed."
                )

            projects[decision_unit_id] = project

    if len(projects) != EXPECTED_PROJECT_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_PROJECT_COUNT} analytical projects; "
            f"found {len(projects)}."
        )

    return projects


def load_watershed_reconciliation(
    path: Path,
) -> dict[str, dict[str, object]]:
    artifact = load_json(path)

    if not isinstance(artifact, dict):
        raise ReconciliationError(
            "Watershed reconciliation artifact must be a JSON object."
        )

    if artifact.get("governance_checkpoint") != "M3.7A":
        raise ReconciliationError(
            "Expected governed M3.7A Watershed reconciliation."
        )

    records = artifact.get("records")

    if not isinstance(records, list):
        raise ReconciliationError(
            "Watershed reconciliation has no records list."
        )

    by_canonical_id: dict[str, dict[str, object]] = {}

    for record in records:
        canonical_id = str(record["canonical_project_id"])

        if canonical_id in by_canonical_id:
            raise ReconciliationError(
                f"Duplicate Watershed canonical ID: {canonical_id}"
            )

        by_canonical_id[canonical_id] = record

    if len(by_canonical_id) != EXPECTED_WATERSHED_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_WATERSHED_COUNT} Watershed "
            f"reconciliation records; found {len(by_canonical_id)}."
        )

    return by_canonical_id


def load_non_watershed_scores(
    path: Path,
) -> dict[str, dict[str, str]]:
    with path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as input_file:
        rows = list(csv.DictReader(input_file))

    if len(rows) != EXPECTED_NON_WATERSHED_COUNT:
        raise ReconciliationError(
            f"Expected {EXPECTED_NON_WATERSHED_COUNT} non-Watershed "
            f"PRB score rows; found {len(rows)}."
        )

    by_id: dict[str, dict[str, str]] = {}

    for row in rows:
        decision_unit_id = row["decision_unit_id"]

        if decision_unit_id in by_id:
            raise ReconciliationError(
                f"Duplicate non-Watershed score ID: {decision_unit_id}"
            )

        by_id[decision_unit_id] = row

    return by_id


def january_source_version(
    project: dict[str, object],
) -> dict[str, object]:
    versions = [
        version
        for version in project["source_versions"]
        if version["source_id"] == JAN_SOURCE_ID
    ]

    if len(versions) != 1:
        raise ReconciliationError(
            f"{project['decision_unit_id']} must contain exactly one "
            "January source version."
        )

    return versions[0]


def is_half_point(value: int | float) -> bool:
    decimal_number = Decimal(str(value))

    return (
        decimal_number * Decimal("2")
        == (
            decimal_number * Decimal("2")
        ).to_integral_value()
        and decimal_number
        != decimal_number.to_integral_value()
    )
def request_version_conflict(
    project: dict[str, object],
) -> bool:
    request_values = {
        int(version["department_request_dollars"])
        for version in project["source_versions"]
        if version.get("department_request_dollars") is not None
    }

    return len(request_values) > 1


def validate_score_increment(
    value: Decimal,
    decision_unit_id: str,
    field: str,
) -> None:
    doubled = value * Decimal("2")

    if doubled != doubled.to_integral_value():
        raise ReconciliationError(
            f"{decision_unit_id} {field} does not use a "
            "whole- or half-point increment."
        )


def build_non_watershed_record(
    project: dict[str, object],
    score: dict[str, str],
) -> dict[str, object]:
    decision_unit_id = str(
        project["decision_unit_id"]
    )

    january = january_source_version(
        project
    )

    january_name = str(
        january["source_name"]
    )

    if score["decision_unit_id"] != decision_unit_id:
        raise ReconciliationError(
            f"Score identity mismatch for {decision_unit_id}."
        )

    if score["january_source_name"] != january_name:
        raise ReconciliationError(
            f"January source-name mismatch for {decision_unit_id}: "
            f"score={score['january_source_name']!r}; "
            f"governed={january_name!r}"
        )

    if (
        score["presentation_category"]
        != project["presentation_category"]
    ):
        raise ReconciliationError(
            f"Presentation-category mismatch for {decision_unit_id}."
        )

    if score["source_id"] != JAN_SOURCE_ID:
        raise ReconciliationError(
            f"Unexpected PRB source for {decision_unit_id}."
        )

    values = {
        field: decimal_value(
            score[field]
        )
        for field in (
            *COMPONENT_FIELDS,
            "grand_total",
        )
    }

    for field, value in values.items():
        validate_score_increment(
            value,
            decision_unit_id,
            field,
        )

    component_sum = sum(
        (
            values[field]
            for field in COMPONENT_FIELDS
        ),
        Decimal("0"),
    )

    if (
        component_sum
        != values["grand_total"]
    ):
        raise ReconciliationError(
            f"PRB component sum mismatch for {decision_unit_id}: "
            f"{component_sum} != {values['grand_total']}"
        )

    governed_total = decimal_value(
        project["prb_score"]
    )

    january_total = decimal_value(
        january["prb_score"]
    )

    if (
        values["grand_total"]
        != governed_total
        or values["grand_total"]
        != january_total
    ):
        raise ReconciliationError(
            f"PRB Grand Total mismatch for {decision_unit_id}: "
            f"PDF={values['grand_total']}; "
            f"governed={governed_total}; "
            f"January={january_total}"
        )

    model_request = project.get(
        "department_request_dollars"
    )

    january_request = january.get(
        "department_request_dollars"
    )

    if (
        model_request is None
        or january_request is None
    ):
        raise ReconciliationError(
            f"{decision_unit_id} is missing its governed "
            "January request amount."
        )

    if int(model_request) != int(
        january_request
    ):
        raise ReconciliationError(
            f"{decision_unit_id} non-Watershed model request "
            "must match the governed January request."
        )

    project_recommendation = project.get(
        "historical_recommendation_amount_dollars"
    )

    january_recommendation = january.get(
        "historical_recommendation_amount_dollars"
    )

    if (
        project_recommendation
        != january_recommendation
    ):
        raise ReconciliationError(
            f"Historical recommendation mismatch for "
            f"{decision_unit_id}."
        )

    conflict = bool(
        project["source_conflict_flag"]
    )

    return {
        "decision_unit_id": decision_unit_id,
        "canonical_project_id": None,
        "presentation_category": str(
            project["presentation_category"]
        ),
        "source_department": str(
            project["source_department"]
        ),
        "source_domain": str(
            project["source_domain"]
        ),
        "governed_source_name": str(
            project["source_name"]
        ),
        "january_source_name": january_name,
        "reconciliation_status": (
            "EXACT_GOVERNED_JANUARY_NAME_MATCH"
        ),
        "identity_authority": (
            "M3.6_GOVERNED_DECISION_UNIT_ID"
        ),
        "model_request_dollars": int(
            model_request
        ),
        "model_request_authority": (
            "M3.6_GOVERNED_JANUARY_REQUEST"
        ),
        "model_request_authority_source_id": (
            JAN_SOURCE_ID
        ),
        "january_request_dollars": int(
            january_request
        ),
        "january_recommendation_dollars": (
            int(january_recommendation)
            if january_recommendation is not None
            else None
        ),
        "source_conflict_flag": conflict,
        "request_version_conflict": (
            request_version_conflict(
                project
            )
        ),
        "strategic_alignment": numeric_value(
            values["strategic_alignment"]
        ),
        "critical_asset": numeric_value(
            values["critical_asset"]
        ),
        "community_consideration": numeric_value(
            values["community_consideration"]
        ),
        "efficiency": numeric_value(
            values["efficiency"]
        ),
        "timeliness_readiness": numeric_value(
            values["timeliness_readiness"]
        ),
        "climate_resilience": numeric_value(
            values["climate_resilience"]
        ),
        "prb_grand_total": numeric_value(
            values["grand_total"]
        ),
        "prb_scoring_source_id": (
            JAN_SOURCE_ID
        ),
        "prb_source_pdf_page": int(
            score["source_pdf_page"]
        ),
        "prb_source_table_row_order": int(
            score["source_table_row_order"]
        ),
    }


def build_watershed_record(
    project: dict[str, object],
    watershed_record: dict[str, object],
) -> dict[str, object]:
    decision_unit_id = str(
        project["decision_unit_id"]
    )

    canonical_id = project.get(
        "canonical_project_id"
    )

    if canonical_id is None:
        raise ReconciliationError(
            f"{decision_unit_id} is missing "
            "canonical_project_id."
        )

    canonical_id = str(
        canonical_id
    )

    if (
        str(
            watershed_record[
                "canonical_project_id"
            ]
        )
        != canonical_id
    ):
        raise ReconciliationError(
            f"Watershed canonical identity mismatch for "
            f"{decision_unit_id}."
        )

    values = {
        field: decimal_value(
            watershed_record[field]
        )
        for field in (
            *COMPONENT_FIELDS,
            "prb_grand_total",
        )
    }

    for field, value in values.items():
        validate_score_increment(
            value,
            decision_unit_id,
            field,
        )

    component_sum = sum(
        (
            values[field]
            for field in COMPONENT_FIELDS
        ),
        Decimal("0"),
    )

    if (
        component_sum
        != values["prb_grand_total"]
    ):
        raise ReconciliationError(
            f"Watershed PRB component sum mismatch for "
            f"{decision_unit_id}."
        )

    if (
        values["prb_grand_total"]
        != decimal_value(
            project["prb_score"]
        )
    ):
        raise ReconciliationError(
            f"Watershed governed PRB Grand Total mismatch for "
            f"{decision_unit_id}."
        )

    november_request = watershed_record.get(
        "november_request_dollars"
    )

    january_request = watershed_record.get(
        "january_request_dollars"
    )

    if (
        november_request is None
        or january_request is None
    ):
        raise ReconciliationError(
            f"{decision_unit_id} is missing Watershed "
            "request authority evidence."
        )

    project_request = project.get(
        "department_request_dollars"
    )

    if (
        project_request is None
        or int(project_request)
        != int(november_request)
    ):
        raise ReconciliationError(
            f"{decision_unit_id} M3.6 governed request no longer "
            "matches canonical November authority."
        )

    existing_conflict = bool(
        watershed_record[
            "request_version_conflict"
        ]
    )

    if (
        existing_conflict
        != request_version_conflict(
            project
        )
    ):
        raise ReconciliationError(
            f"Watershed request-conflict provenance mismatch "
            f"for {decision_unit_id}."
        )

    return {
        "decision_unit_id": decision_unit_id,
        "canonical_project_id": canonical_id,
        "presentation_category": "Watershed",
        "source_department": str(
            project["source_department"]
        ),
        "source_domain": str(
            project["source_domain"]
        ),
        "governed_source_name": str(
            project["source_name"]
        ),
        "january_source_name": str(
            watershed_record[
                "january_source_name"
            ]
        ),
        "reconciliation_status": str(
            watershed_record[
                "reconciliation_status"
            ]
        ),
        "identity_authority": (
            "M3.7A_WATERSHED_CANONICAL_PROJECT_ID"
        ),
        "model_request_dollars": int(
            november_request
        ),
        "model_request_authority": (
            "CANONICAL_NOVEMBER_2025_WATERSHED_REQUEST"
        ),
        "model_request_authority_source_id": (
            NOV_WATERSHED_SOURCE_ID
        ),
        "january_request_dollars": int(
            january_request
        ),
        "january_recommendation_dollars": (
            int(
                watershed_record[
                    "january_recommendation_dollars"
                ]
            )
            if watershed_record[
                "january_recommendation_dollars"
            ]
            is not None
            else None
        ),
        "source_conflict_flag": bool(
            project["source_conflict_flag"]
        ),
        "request_version_conflict": (
            existing_conflict
        ),
        "strategic_alignment": numeric_value(
            values["strategic_alignment"]
        ),
        "critical_asset": numeric_value(
            values["critical_asset"]
        ),
        "community_consideration": numeric_value(
            values["community_consideration"]
        ),
        "efficiency": numeric_value(
            values["efficiency"]
        ),
        "timeliness_readiness": numeric_value(
            values["timeliness_readiness"]
        ),
        "climate_resilience": numeric_value(
            values["climate_resilience"]
        ),
        "prb_grand_total": numeric_value(
            values["prb_grand_total"]
        ),
        "prb_scoring_source_id": (
            JAN_SOURCE_ID
        ),
        "prb_source_pdf_page": int(
            watershed_record[
                "prb_source_pdf_page"
            ]
        ),
        "prb_source_table_row_order": int(
            watershed_record[
                "prb_source_table_row_order"
            ]
        ),
    }


def build_records(
    projects: dict[str, dict[str, object]],
    watershed_reconciliation: dict[
        str,
        dict[str, object],
    ],
    non_watershed_scores: dict[
        str,
        dict[str, str],
    ],
) -> tuple[dict[str, object], ...]:
    records: list[
        dict[str, object]
    ] = []

    observed_non_watershed_ids = {
        decision_unit_id
        for decision_unit_id, project
        in projects.items()
        if (
            project[
                "presentation_category"
            ]
            != "Watershed"
        )
    }

    if (
        observed_non_watershed_ids
        != set(non_watershed_scores)
    ):
        raise ReconciliationError(
            "Non-Watershed analytical-project IDs do not "
            "exactly match extracted PRB score IDs. "
            f"Missing={sorted(observed_non_watershed_ids - set(non_watershed_scores))}; "
            f"unexpected={sorted(set(non_watershed_scores) - observed_non_watershed_ids)}"
        )

    observed_watershed_ids = {
        str(
            project["canonical_project_id"]
        )
        for project in projects.values()
        if (
            project[
                "presentation_category"
            ]
            == "Watershed"
        )
    }

    if (
        observed_watershed_ids
        != set(
            watershed_reconciliation
        )
    ):
        raise ReconciliationError(
            "Watershed canonical IDs do not exactly match "
            "the governed M3.7A reconciliation."
        )

    category_order = {
        "Transportation": 0,
        "Parks & Open Space": 1,
        "Watershed": 2,
        "Community Facilities": 3,
    }

    ordered_projects = sorted(
        projects.values(),
        key=lambda project: (
            category_order[
                str(
                    project[
                        "presentation_category"
                    ]
                )
            ],
            str(
                project[
                    "decision_unit_id"
                ]
            ),
        ),
    )

    for project in ordered_projects:
        decision_unit_id = str(
            project[
                "decision_unit_id"
            ]
        )

        category = str(
            project[
                "presentation_category"
            ]
        )

        if category == "Watershed":
            canonical_id = str(
                project[
                    "canonical_project_id"
                ]
            )

            record = build_watershed_record(
                project,
                watershed_reconciliation[
                    canonical_id
                ],
            )

        else:
            record = build_non_watershed_record(
                project,
                non_watershed_scores[
                    decision_unit_id
                ],
            )

        records.append(
            record
        )

    return tuple(records)


def validate_records(
    records: tuple[
        dict[str, object],
        ...,
    ],
) -> dict[str, object]:
    if (
        len(records)
        != EXPECTED_PROJECT_COUNT
    ):
        raise ReconciliationError(
            f"Expected {EXPECTED_PROJECT_COUNT} reconciliation "
            f"records; found {len(records)}."
        )

    ids = [
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise ReconciliationError(
            "Cross-category decision_unit_ids are not unique."
        )

    category_counts = {
        category: sum(
            record[
                "presentation_category"
            ]
            == category
            for record in records
        )
        for category in (
            EXPECTED_CATEGORY_COUNTS
        )
    }

    if (
        category_counts
        != EXPECTED_CATEGORY_COUNTS
    ):
        raise ReconciliationError(
            "Cross-category project counts changed: "
            f"{category_counts}"
        )

    model_request_total = sum(
        int(
            record[
                "model_request_dollars"
            ]
        )
        for record in records
    )

    january_request_total = sum(
        int(
            record[
                "january_request_dollars"
            ]
        )
        for record in records
    )

    recommendation_total = sum(
        int(
            record[
                "january_recommendation_dollars"
            ]
            or 0
        )
        for record in records
    )

    recommendation_present_count = sum(
        record[
            "january_recommendation_dollars"
        ]
        is not None
        for record in records
    )

    if (
        model_request_total
        != EXPECTED_MODEL_REQUEST_TOTAL
    ):
        raise ReconciliationError(
            "Model request total changed: "
            f"${model_request_total:,}"
        )

    if (
        january_request_total
        != EXPECTED_JANUARY_REQUEST_TOTAL
    ):
        raise ReconciliationError(
            "January request overlay total changed: "
            f"${january_request_total:,}"
        )

    if (
        recommendation_total
        != EXPECTED_RECOMMENDATION_TOTAL
    ):
        raise ReconciliationError(
            "Project-level January recommendation total changed: "
            f"${recommendation_total:,}"
        )

    if (
        recommendation_present_count
        != EXPECTED_RECOMMENDATION_PRESENT_COUNT
    ):
        raise ReconciliationError(
            "January recommendation-present count changed: "
            f"{recommendation_present_count}"
        )

    source_conflict_ids = {
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
        if (
            record[
                "source_conflict_flag"
            ]
            is True
        )
    }

    if (
        source_conflict_ids
        != EXPECTED_SOURCE_CONFLICT_IDS
    ):
        raise ReconciliationError(
            "Source-conflict set changed: "
            f"{sorted(source_conflict_ids)}"
        )

    request_conflict_ids = {
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
        if (
            record[
                "request_version_conflict"
            ]
            is True
        )
    }

    if (
        request_conflict_ids
        != EXPECTED_SOURCE_CONFLICT_IDS
    ):
        raise ReconciliationError(
            "Request-version conflict set changed: "
            f"{sorted(request_conflict_ids)}"
        )

    half_point_ids = {
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
        if any(
            is_half_point(
                value
            )
            for value in (
                record[
                    "strategic_alignment"
                ],
                record[
                    "critical_asset"
                ],
                record[
                    "community_consideration"
                ],
                record[
                    "efficiency"
                ],
                record[
                    "timeliness_readiness"
                ],
                record[
                    "climate_resilience"
                ],
                record[
                    "prb_grand_total"
                ],
            )
        )
    }

    if (
        half_point_ids
        != EXPECTED_HALF_POINT_IDS
    ):
        raise ReconciliationError(
            "Half-point project set changed: "
            f"{sorted(half_point_ids)}"
        )

    watershed_records = [
        record
        for record in records
        if (
            record[
                "presentation_category"
            ]
            == "Watershed"
        )
    ]

    non_watershed_records = [
        record
        for record in records
        if (
            record[
                "presentation_category"
            ]
            != "Watershed"
        )
    ]

    if len(watershed_records) != 37:
        raise ReconciliationError(
            "Expected 37 Watershed records."
        )

    if len(non_watershed_records) != 69:
        raise ReconciliationError(
            "Expected 69 non-Watershed records."
        )

    if any(
        record[
            "canonical_project_id"
        ]
        is None
        for record in watershed_records
    ):
        raise ReconciliationError(
            "Watershed records must preserve canonical IDs."
        )

    if any(
        record[
            "canonical_project_id"
        ]
        is not None
        for record in non_watershed_records
    ):
        raise ReconciliationError(
            "Non-Watershed records must use decision_unit_id "
            "rather than fabricated canonical project IDs."
        )

    non_watershed_exact_count = sum(
        record[
            "reconciliation_status"
        ]
        == "EXACT_GOVERNED_JANUARY_NAME_MATCH"
        for record in non_watershed_records
    )

    if non_watershed_exact_count != 69:
        raise ReconciliationError(
            "All 69 non-Watershed identities must reconcile "
            "by exact governed January name."
        )

    watershed_exact_count = sum(
        record[
            "reconciliation_status"
        ]
        == "EXACT_NAME_MATCH"
        for record in watershed_records
    )

    watershed_version_match_count = sum(
        record[
            "reconciliation_status"
        ]
        == "GOVERNED_SOURCE_VERSION_MATCH"
        for record in watershed_records
    )

    if (
        watershed_exact_count != 7
        or watershed_version_match_count != 30
    ):
        raise ReconciliationError(
            "Watershed reconciliation-status distribution changed."
        )

    return {
        "analytical_project_count": (
            len(records)
        ),
        "category_counts": (
            category_counts
        ),
        "complete_prb_component_vector_count": (
            len(records)
        ),
        "valid_prb_grand_total_count": (
            len(records)
        ),
        "non_watershed_exact_identity_match_count": (
            non_watershed_exact_count
        ),
        "watershed_exact_name_match_count": (
            watershed_exact_count
        ),
        "watershed_governed_source_version_match_count": (
            watershed_version_match_count
        ),
        "source_conflict_count": (
            len(source_conflict_ids)
        ),
        "request_version_conflict_count": (
            len(request_conflict_ids)
        ),
        "half_point_project_count": (
            len(half_point_ids)
        ),
        "model_request_total_dollars": (
            model_request_total
        ),
        "january_request_overlay_total_dollars": (
            january_request_total
        ),
        "january_project_recommendation_total_dollars": (
            recommendation_total
        ),
        "january_recommendation_present_count": (
            recommendation_present_count
        ),
    }


def render_artifact(
    records: tuple[
        dict[str, object],
        ...,
    ],
    summary: dict[str, object],
) -> bytes:
    artifact = {
        "artifact_version": (
            ARTIFACT_VERSION
        ),
        "governance_checkpoint": (
            "M3.7E-A"
        ),
        "historical_decision_snapshot_date": (
            "2026-01-21"
        ),
        "artifact_scope": (
            "CROSS_CATEGORY_PRB_RECONCILIATION"
        ),
        "cross_category_ranking_authorized": False,
        "portfolio_selection_authorized": False,
        "runtime_integration_authorized": False,
        "authority_policy": {
            "watershed_identity": (
                "M3.7A_CANONICAL_PROJECT_ID"
            ),
            "non_watershed_identity": (
                "M3.6_GOVERNED_DECISION_UNIT_ID"
            ),
            "watershed_model_request": (
                "CANONICAL_NOVEMBER_2025_REQUEST"
            ),
            "non_watershed_model_request": (
                "M3.6_GOVERNED_JANUARY_REQUEST"
            ),
            "prb_scoring": (
                "JANUARY_21_2026_PRB_SCORE_COMPONENTS"
            ),
            "january_initial_recommendation": (
                "BENCHMARK_OUTCOME_ONLY"
            ),
            "source_version_conflict_policy": (
                "PRESERVE_PROVENANCE_DO_NOT_AUTO_EXCLUDE"
            ),
        },
        "source_artifacts": {
            "cross_category_structural_universe": (
                "data/governed/cross_category/"
                "cross-category-universe.json"
            ),
            "watershed_reconciliation": (
                "data/governed/cross_category/reconciliation/"
                "watershed-prb-reconciliation.json"
            ),
            "non_watershed_prb_scores": (
                "data/reconnaissance/city_austin/"
                "initial_draft_recommendation/2026-01-21/"
                "non_watershed_prb_scores.csv"
            ),
        },
        "summary": summary,
        "records": list(
            records
        ),
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
        existing = (
            output_path.read_bytes()
        )

        if existing == content:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Refusing to overwrite differing governed "
            f"cross-category reconciliation artifact: "
            f"{output_path}"
        )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output_path.write_bytes(
        content
    )

    return "created"


def parse_args() -> argparse.Namespace:
    parser = (
        argparse.ArgumentParser()
    )

    parser.add_argument(
        "--watershed-reconciliation-path",
        type=Path,
        default=(
            DEFAULT_WATERSHED_RECONCILIATION_PATH
        ),
    )

    parser.add_argument(
        "--non-watershed-score-path",
        type=Path,
        default=(
            DEFAULT_NON_WATERSHED_SCORE_PATH
        ),
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

    projects = (
        load_analytical_projects()
    )

    watershed_reconciliation = (
        load_watershed_reconciliation(
            args.watershed_reconciliation_path
        )
    )

    non_watershed_scores = (
        load_non_watershed_scores(
            args.non_watershed_score_path
        )
    )

    records = build_records(
        projects,
        watershed_reconciliation,
        non_watershed_scores,
    )

    summary = validate_records(
        records
    )

    print(
        "M3.7E-A Cross-Category PRB Reconciliation"
    )

    print(
        "Analytical projects reconciled: "
        f"{summary['analytical_project_count']}/106"
    )

    print(
        "Complete PRB component vectors: "
        f"{summary['complete_prb_component_vector_count']}/106"
    )

    print(
        "Valid PRB Grand Totals: "
        f"{summary['valid_prb_grand_total_count']}/106"
    )

    print(
        "Transportation: "
        f"{summary['category_counts']['Transportation']}"
    )

    print(
        "Parks & Open Space: "
        f"{summary['category_counts']['Parks & Open Space']}"
    )

    print(
        "Watershed: "
        f"{summary['category_counts']['Watershed']}"
    )

    print(
        "Community Facilities: "
        f"{summary['category_counts']['Community Facilities']}"
    )

    print(
        "Source-version conflicts preserved: "
        f"{summary['source_conflict_count']}"
    )

    print(
        "Half-point projects: "
        f"{summary['half_point_project_count']}"
    )

    print(
        "Model request authority total: "
        f"${summary['model_request_total_dollars']:,}"
    )

    print(
        "January request overlay total: "
        f"${summary['january_request_overlay_total_dollars']:,}"
    )

    print(
        "January project-level recommendation total: "
        f"${summary['january_project_recommendation_total_dollars']:,}"
    )

    print(
        "Projects with January recommendation: "
        f"{summary['january_recommendation_present_count']}"
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
            "no governed artifact written."
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
        "Governed reconciliation artifact: "
        f"{result}: {args.output_path}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())