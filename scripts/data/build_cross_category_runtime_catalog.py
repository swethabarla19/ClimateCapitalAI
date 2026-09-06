"""Build the deterministic 106-project cross-category runtime-v2 catalog."""

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(BACKEND_ROOT),
    )


from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_PORTFOLIO_METHODOLOGY,
    CROSS_CATEGORY_PROJECTS_IN_TIES,
    CROSS_CATEGORY_RUNTIME_MODEL_SCOPE,
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
    CROSS_CATEGORY_TIED_SCORE_GROUP_COUNT,
    CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT,
    CrossCategoryRuntimeCatalog,
)

if __package__:
    from . import (
        audit_cross_category_official_portfolio_constraints
        as official_constraints,
    )
else:
    import audit_cross_category_official_portfolio_constraints as official_constraints


RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

ELIGIBILITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "model_eligibility"
    / "cross-category-prb-model-eligibility.json"
)

PRIORITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "cross-category-prb-funding-priority.json"
)

METHODOLOGY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "portfolio_methodology"
    / "cross-category-portfolio-methodology.json"
)

OUTPUT_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v2"
    / "catalog.json"
)

DATA_VERSION = (
    "climatecapital-austin-2026-01-21-cross-category-v2"
)

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}

EXPECTED_HALF_POINT_SCORES = {
    54.5,
    53.5,
    50.5,
}


class RuntimeCatalogBuildError(RuntimeError):
    """Raised when governed runtime-catalog prerequisites do not reconcile."""


class DerivedArtifactConflictError(RuntimeCatalogBuildError):
    """Raised when an existing deterministic catalog differs."""


def load_json(
    path: Path,
) -> dict[str, object]:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def index_records(
    artifact: dict[str, object],
    *,
    label: str,
) -> dict[str, dict[str, object]]:
    records = artifact.get(
        "records"
    )

    if not isinstance(
        records,
        list,
    ):
        raise RuntimeCatalogBuildError(
            f"{label} records must be a list"
        )

    result = {}

    for record in records:
        if not isinstance(
            record,
            dict,
        ):
            raise RuntimeCatalogBuildError(
                f"{label} record must be an object"
            )

        decision_unit_id = record.get(
            "decision_unit_id"
        )

        if not isinstance(
            decision_unit_id,
            str,
        ):
            raise RuntimeCatalogBuildError(
                f"{label} record missing decision_unit_id"
            )

        if decision_unit_id in result:
            raise RuntimeCatalogBuildError(
                f"{label} duplicate decision_unit_id: "
                f"{decision_unit_id}"
            )

        result[
            decision_unit_id
        ] = record

    return result


def validate_authority_chain(
    reconciliation: dict[str, object],
    eligibility: dict[str, object],
    priority: dict[str, object],
    methodology: dict[str, object],
) -> None:
    if (
        reconciliation.get(
            "historical_decision_snapshot_date"
        )
        != "2026-01-21"
    ):
        raise RuntimeCatalogBuildError(
            "Reconciliation snapshot changed."
        )

    if (
        eligibility.get(
            "historical_decision_snapshot_date"
        )
        != "2026-01-21"
    ):
        raise RuntimeCatalogBuildError(
            "Eligibility snapshot changed."
        )

    if (
        priority.get(
            "historical_decision_snapshot_date"
        )
        != "2026-01-21"
    ):
        raise RuntimeCatalogBuildError(
            "Funding Priority snapshot changed."
        )

    if (
        methodology.get(
            "historical_decision_snapshot_date"
        )
        != "2026-01-21"
    ):
        raise RuntimeCatalogBuildError(
            "Portfolio methodology snapshot changed."
        )

    if (
        eligibility.get(
            "model_scope"
        )
        != CROSS_CATEGORY_RUNTIME_MODEL_SCOPE
    ):
        raise RuntimeCatalogBuildError(
            "Eligibility model scope changed."
        )

    if (
        priority.get(
            "model_scope"
        )
        != CROSS_CATEGORY_RUNTIME_MODEL_SCOPE
    ):
        raise RuntimeCatalogBuildError(
            "Funding Priority model scope changed."
        )

    if (
        methodology.get(
            "model_scope"
        )
        != CROSS_CATEGORY_RUNTIME_MODEL_SCOPE
    ):
        raise RuntimeCatalogBuildError(
            "Portfolio methodology model scope changed."
        )

    if (
        priority.get(
            "cross_category_ranking_authorized"
        )
        is not True
    ):
        raise RuntimeCatalogBuildError(
            "Cross-category ranking must be authorized."
        )

    if (
        methodology.get(
            "cross_category_ranking_authorized"
        )
        is not True
    ):
        raise RuntimeCatalogBuildError(
            "Portfolio methodology must preserve "
            "ranking authorization."
        )

    if (
        methodology.get(
            "portfolio_selection_authorized"
        )
        is not True
    ):
        raise RuntimeCatalogBuildError(
            "Portfolio methodology must be authorized."
        )

    if (
        methodology.get(
            "runtime_integration_authorized"
        )
        is not False
    ):
        raise RuntimeCatalogBuildError(
            "Runtime integration must remain "
            "unauthorized while building v2 catalog."
        )

    if (
        methodology.get(
            "methodology_name"
        )
        != CROSS_CATEGORY_PORTFOLIO_METHODOLOGY
    ):
        raise RuntimeCatalogBuildError(
            "Unexpected portfolio methodology."
        )


def build_january_context(
    reconciliation_records: dict[
        str,
        dict[str, object],
    ],
) -> dict[str, dict[str, object]]:
    january_requests = {}

    for (
        decision_unit_id,
        record,
    ) in reconciliation_records.items():
        request = record.get(
            "january_request_dollars"
        )

        if request is None:
            request = record.get(
                "model_request_dollars"
            )

        if not isinstance(
            request,
            int,
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: invalid January request"
            )

        january_requests[
            decision_unit_id
        ] = request

    reader = PdfReader(
        official_constraints.SOURCE_PATH
    )

    records = [
        *official_constraints.extract_non_watershed(
            reader,
            january_requests,
        ),
        *official_constraints.extract_watershed(
            reader,
            january_requests,
        ),
    ]

    if (
        len(records)
        != CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ):
        raise RuntimeCatalogBuildError(
            "Expected 106 January context rows."
        )

    result = {}

    for record in records:
        decision_unit_id = str(
            record[
                "decision_unit_id"
            ]
        )

        if decision_unit_id in result:
            raise RuntimeCatalogBuildError(
                "Duplicate January context identity: "
                f"{decision_unit_id}"
            )

        result[
            decision_unit_id
        ] = record

    return result


def council_district_payload(
    normalized_value: str,
) -> dict[str, object]:
    assignment_type = (
        official_constraints.district_type(
            normalized_value
        )
    )

    if (
        normalized_value
        in {
            "CITYWIDE",
            "UNSPECIFIED",
        }
    ):
        districts = []
    else:
        districts = [
            int(value)
            for value
            in normalized_value.split(",")
        ]

    return {
        "assignment_type":
            assignment_type,
        "districts":
            districts,
        "source_value":
            (
                None
                if normalized_value
                == "UNSPECIFIED"
                else normalized_value
            ),
        "analyst_review_only":
            True,
        "hard_portfolio_constraint":
            False,
    }


def om_payload(
    value: str,
) -> dict[str, object]:
    normalized = (
        value
        .strip()
        .upper()
    )

    if normalized not in {
        "YES",
        "NO",
    }:
        raise RuntimeCatalogBuildError(
            f"Unexpected O&M value: {value!r}"
        )

    return {
        "value":
            normalized,
        "analyst_review_only":
            True,
        "hard_portfolio_constraint":
            False,
        "additional_score_preference_authorized":
            False,
    }


def sorted_unique(
    values: list[str],
) -> list[str]:
    return sorted(
        set(values)
    )


def build_catalog_payload() -> dict[str, object]:
    reconciliation = load_json(
        RECONCILIATION_PATH
    )

    eligibility = load_json(
        ELIGIBILITY_PATH
    )

    priority = load_json(
        PRIORITY_PATH
    )

    methodology = load_json(
        METHODOLOGY_PATH
    )

    validate_authority_chain(
        reconciliation,
        eligibility,
        priority,
        methodology,
    )

    reconciliation_records = (
        index_records(
            reconciliation,
            label="reconciliation",
        )
    )

    eligibility_records = (
        index_records(
            eligibility,
            label="eligibility",
        )
    )

    priority_records = (
        index_records(
            priority,
            label="priority",
        )
    )

    identity_sets = {
        "reconciliation":
            set(
                reconciliation_records
            ),
        "eligibility":
            set(
                eligibility_records
            ),
        "priority":
            set(
                priority_records
            ),
    }

    expected_ids = (
        identity_sets[
            "reconciliation"
        ]
    )

    if (
        len(expected_ids)
        != CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ):
        raise RuntimeCatalogBuildError(
            "Expected exactly 106 reconciliation IDs."
        )

    for (
        label,
        identities,
    ) in identity_sets.items():
        if identities != expected_ids:
            raise RuntimeCatalogBuildError(
                f"{label} identity set does not match "
                "the governed 106-project cohort."
            )

    january_context = (
        build_january_context(
            reconciliation_records
        )
    )

    if (
        set(january_context)
        != expected_ids
    ):
        raise RuntimeCatalogBuildError(
            "January context identities do not match "
            "the governed 106-project cohort."
        )

    projects = []

    for decision_unit_id in sorted(
        expected_ids
    ):
        recon = (
            reconciliation_records[
                decision_unit_id
            ]
        )

        eligible = (
            eligibility_records[
                decision_unit_id
            ]
        )

        ranked = (
            priority_records[
                decision_unit_id
            ]
        )

        context = (
            january_context[
                decision_unit_id
            ]
        )

        if (
            eligible.get(
                "model_eligible"
            )
            is not True
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: project is not model eligible"
            )

        if (
            eligible.get(
                "evidence_feasibility_status"
            )
            != "FEASIBLE"
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: evidence is not FEASIBLE"
            )

        if (
            eligible.get(
                "blocking_reason_codes"
            )
            != []
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: unexpected blocking reasons"
            )

        recon_request = recon.get(
            "model_request_dollars"
        )

        eligibility_request = (
            eligible.get(
                "model_request_dollars"
            )
        )

        if (
            recon_request
            != eligibility_request
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: governed request mismatch"
            )

        recon_total = recon.get(
            "prb_grand_total"
        )

        eligibility_total = (
            eligible.get(
                "prb_grand_total"
            )
        )

        priority_total = (
            ranked.get(
                "funding_priority_score"
            )
        )

        if not (
            recon_total
            == eligibility_total
            == priority_total
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: PRB total mismatch"
            )

        if (
            recon.get(
                "presentation_category"
            )
            != ranked.get(
                "presentation_category"
            )
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: category mismatch"
            )

        if (
            recon.get(
                "canonical_project_id"
            )
            != ranked.get(
                "canonical_project_id"
            )
        ):
            raise RuntimeCatalogBuildError(
                f"{decision_unit_id}: canonical ID mismatch"
            )

        provenance_refs = (
            sorted_unique(
                [
                    str(
                        recon[
                            "model_request_authority_source_id"
                        ]
                    ),
                    str(
                        recon[
                            "prb_scoring_source_id"
                        ]
                    ),
                ]
            )
        )

        project = {
            "decision_unit_id":
                decision_unit_id,
            "canonical_project_id":
                recon.get(
                    "canonical_project_id"
                ),
            "governed_name":
                str(
                    recon[
                        "governed_source_name"
                    ]
                ),
            "presentation_category":
                str(
                    recon[
                        "presentation_category"
                    ]
                ),
            "source_department":
                str(
                    recon[
                        "source_department"
                    ]
                ),
            "source_domain":
                str(
                    recon[
                        "source_domain"
                    ]
                ),
            "model_request_dollars":
                int(
                    recon[
                        "model_request_dollars"
                    ]
                ),
            "model_request_authority":
                str(
                    recon[
                        "model_request_authority"
                    ]
                ),
            "model_request_authority_source_id":
                str(
                    recon[
                        "model_request_authority_source_id"
                    ]
                ),
            "request_version_conflict":
                bool(
                    recon[
                        "request_version_conflict"
                    ]
                ),
            "funding_priority_score":
                ranked[
                    "funding_priority_score"
                ],
            "funding_priority_rank":
                int(
                    ranked[
                        "funding_priority_rank"
                    ]
                ),
            "is_tied":
                bool(
                    ranked[
                        "is_tied"
                    ]
                ),
            "tie_group_size":
                int(
                    ranked[
                        "tie_group_size"
                    ]
                ),
            "display_order_within_tie":
                int(
                    ranked[
                        "display_order_within_tie"
                    ]
                ),
            "display_tiebreak_has_analytical_meaning":
                False,
            "prb_components": {
                "strategic_alignment":
                    recon[
                        "strategic_alignment"
                    ],
                "critical_asset":
                    recon[
                        "critical_asset"
                    ],
                "community_consideration":
                    recon[
                        "community_consideration"
                    ],
                "efficiency":
                    recon[
                        "efficiency"
                    ],
                "timeliness_readiness":
                    recon[
                        "timeliness_readiness"
                    ],
                "climate_resilience":
                    recon[
                        "climate_resilience"
                    ],
            },
            "council_district":
                council_district_payload(
                    str(
                        context[
                            "council_district"
                        ]
                    )
                ),
            "om_impact":
                om_payload(
                    str(
                        context[
                            "om_impact"
                        ]
                    )
                ),
            "provenance_refs":
                provenance_refs,
        }

        projects.append(
            project
        )

    payload = {
        "contract_version":
            CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
        "data_version":
            DATA_VERSION,
        "historical_decision_snapshot_date":
            "2026-01-21",
        "model_scope":
            CROSS_CATEGORY_RUNTIME_MODEL_SCOPE,
        "methodology_name":
            CROSS_CATEGORY_PORTFOLIO_METHODOLOGY,
        "cross_category_ranking_authorized":
            True,
        "portfolio_selection_authorized":
            True,
        "runtime_integration_authorized":
            False,
        "project_count":
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
        "governed_request_total_dollars":
            CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
        "category_counts": {
            "transportation":
                9,
            "parks_open_space":
                22,
            "watershed":
                37,
            "community_facilities":
                38,
        },
        "unique_funding_priority_score_count":
            CROSS_CATEGORY_UNIQUE_PRIORITY_SCORE_COUNT,
        "tied_score_group_count":
            CROSS_CATEGORY_TIED_SCORE_GROUP_COUNT,
        "projects_in_tied_score_groups":
            CROSS_CATEGORY_PROJECTS_IN_TIES,
        "projects":
            projects,
    }

    # Full Pydantic validation is part of the build.
    validated = (
        CrossCategoryRuntimeCatalog
        .model_validate(
            payload
        )
    )

    return validated.model_dump(
        mode="json"
    )


def validate_catalog_semantics(
    payload: dict[str, object],
) -> None:
    projects = payload[
        "projects"
    ]

    if not isinstance(
        projects,
        list,
    ):
        raise RuntimeCatalogBuildError(
            "Runtime projects must be a list."
        )

    if (
        len(projects)
        != CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ):
        raise RuntimeCatalogBuildError(
            "Runtime catalog must contain 106 projects."
        )

    category_counts = Counter(
        project[
            "presentation_category"
        ]
        for project in projects
    )

    if dict(
        category_counts
    ) != EXPECTED_CATEGORY_COUNTS:
        raise RuntimeCatalogBuildError(
            "Runtime category counts changed."
        )

    request_total = sum(
        int(
            project[
                "model_request_dollars"
            ]
        )
        for project in projects
    )

    if (
        request_total
        != CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
    ):
        raise RuntimeCatalogBuildError(
            "Runtime request total changed."
        )

    half_points = {
        float(
            project[
                "funding_priority_score"
            ]
        )
        for project in projects
        if (
            float(
                project[
                    "funding_priority_score"
                ]
            )
            % 1
            != 0
        )
    }

    if (
        half_points
        != EXPECTED_HALF_POINT_SCORES
    ):
        raise RuntimeCatalogBuildError(
            "Half-point Funding Priority scores changed."
        )

    forbidden_catalog_keys = {
        "january_recommendation_dollars",
        "january_recommendation_present",
        "historical_recommendation_amount_dollars",
        "historical_category_allocation",
    }

    for project in projects:
        overlap = (
            forbidden_catalog_keys
            & set(project)
        )

        if overlap:
            raise RuntimeCatalogBuildError(
                "Benchmark fields leaked into catalog: "
                f"{sorted(overlap)}"
            )


def serialized_catalog() -> str:
    payload = build_catalog_payload()

    validate_catalog_semantics(
        payload
    )

    return (
        json.dumps(
            payload,
            indent=2,
            ensure_ascii=False,
            sort_keys=True,
        )
        + "\n"
    )


def write_catalog() -> str:
    rendered = (
        serialized_catalog()
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if OUTPUT_PATH.exists():
        existing = (
            OUTPUT_PATH.read_text(
                encoding="utf-8"
            )
        )

        if existing == rendered:
            return "unchanged"

        raise DerivedArtifactConflictError(
            "Runtime-v2 catalog already exists "
            "with different deterministic content."
        )

    OUTPUT_PATH.write_text(
        rendered,
        encoding="utf-8",
    )

    return "created"


def main() -> int:
    result = write_catalog()

    payload = build_catalog_payload()

    print(
        "M3.8B runtime-v2 catalog:",
        result,
    )

    print(
        "Data version:",
        payload[
            "data_version"
        ],
    )

    print(
        "Projects:",
        payload[
            "project_count"
        ],
    )

    print(
        "Governed request total:",
        f"${payload['governed_request_total_dollars']:,.0f}",
    )

    print(
        "Runtime integration authorized:",
        payload[
            "runtime_integration_authorized"
        ],
    )

    print(
        "Benchmark fields in catalog:",
        "NO",
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())