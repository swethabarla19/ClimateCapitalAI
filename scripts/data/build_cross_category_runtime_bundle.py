"""Build M3.8D2 cross-category map, benchmark, and release manifest."""

from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(BACKEND_ROOT),
    )


from climatecapital.contracts.cross_category_release import (
    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
    CROSS_CATEGORY_HISTORICAL_FULL_PACKAGE_DOLLARS,
    CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS,
    CROSS_CATEGORY_HISTORICAL_OUTSIDE_COHORT_DOLLARS,
    CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT,
    CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION,
    CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION,
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifact,
    CrossCategoryReleaseManifest,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS,
    CrossCategoryRuntimeCatalog,
)

if __package__:
    from . import (
        extract_non_watershed_prb_scores
        as source_module,
    )
else:
    import extract_non_watershed_prb_scores as source_module


DATA_VERSION = (
    "climatecapital-austin-2026-01-21-cross-category-v2"
)

SOURCE_ID = (
    "austin_2026_bond_initial_draft_2026_01_21"
)

EXPECTED_SOURCE_SHA256 = (
    "da85a00273a32afb63f057e0e7f5065078f5e226d2e8c73a3efba69ee4bd0359"
)

RUNTIME_DIR = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "runtime_v2"
)

CATALOG_PATH = (
    RUNTIME_DIR
    / "catalog.json"
)

MAP_PATH = (
    RUNTIME_DIR
    / "map-context.geojson"
)

BENCHMARK_PATH = (
    RUNTIME_DIR
    / "benchmark.json"
)

MANIFEST_PATH = (
    RUNTIME_DIR
    / "manifest.json"
)

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

SOURCE_PATH = (
    source_module.DEFAULT_SOURCE_PATH
)


class RuntimeBundleBuildError(
    RuntimeError
):
    """Raised when governed D2 inputs fail reconciliation."""


class DerivedArtifactConflictError(
    RuntimeBundleBuildError
):
    """Raised when a deterministic artifact already differs."""


def load_json(
    path: Path,
) -> dict[str, object]:
    return json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )


def sha256_bytes(
    payload: bytes,
) -> str:
    return hashlib.sha256(
        payload
    ).hexdigest()


def artifact_identity(
    path: Path,
) -> dict[str, object]:
    payload = path.read_bytes()

    return {
        "sha256":
            sha256_bytes(
                payload
            ),
        "byte_size":
            len(payload),
    }


def source_sha256() -> str:
    if not SOURCE_PATH.is_file():
        raise RuntimeBundleBuildError(
            "January source PDF is missing."
        )

    digest = sha256_bytes(
        SOURCE_PATH.read_bytes()
    )

    if digest != EXPECTED_SOURCE_SHA256:
        raise RuntimeBundleBuildError(
            "January source checksum changed."
        )

    return digest


def load_catalog() -> (
    CrossCategoryRuntimeCatalog
):
    payload = (
        CATALOG_PATH.read_bytes()
    )

    catalog = (
        CrossCategoryRuntimeCatalog
        .model_validate_json(
            payload,
            strict=True,
        )
    )

    if (
        catalog.data_version
        != DATA_VERSION
    ):
        raise RuntimeBundleBuildError(
            "Runtime catalog data version changed."
        )

    if (
        len(catalog.projects)
        != CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ):
        raise RuntimeBundleBuildError(
            "Runtime catalog project count changed."
        )

    if (
        sum(
            project.model_request_dollars
            for project in catalog.projects
        )
        != CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS
    ):
        raise RuntimeBundleBuildError(
            "Runtime catalog request total changed."
        )

    return catalog


def reconciliation_records() -> (
    dict[str, dict[str, object]]
):
    artifact = load_json(
        RECONCILIATION_PATH
    )

    records = artifact.get(
        "records"
    )

    if not isinstance(
        records,
        list,
    ):
        raise RuntimeBundleBuildError(
            "Reconciliation records are missing."
        )

    result = {}

    for record in records:
        if not isinstance(
            record,
            dict,
        ):
            raise RuntimeBundleBuildError(
                "Reconciliation record must be an object."
            )

        decision_unit_id = (
            record.get(
                "decision_unit_id"
            )
        )

        if not isinstance(
            decision_unit_id,
            str,
        ):
            raise RuntimeBundleBuildError(
                "Reconciliation record missing decision_unit_id."
            )

        if decision_unit_id in result:
            raise RuntimeBundleBuildError(
                "Duplicate reconciliation identity: "
                f"{decision_unit_id}"
            )

        result[
            decision_unit_id
        ] = record

    if (
        len(result)
        != CROSS_CATEGORY_RUNTIME_PROJECT_COUNT
    ):
        raise RuntimeBundleBuildError(
            "Expected exactly 106 reconciliation records."
        )

    return result


def build_map_payload() -> dict[str, object]:
    catalog = load_catalog()

    payload = {
        "type":
            "FeatureCollection",
        "contract_version":
            CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION,
        "data_version":
            DATA_VERSION,
        "historical_decision_snapshot_date":
            "2026-01-21",
        "project_identity_key":
            "decision_unit_id",
        "geometry_authority":
            "GOVERNED_RUNTIME_GEOMETRY_ONLY",
        "mapping_status":
            "NO_GOVERNED_RUNTIME_GEOMETRY_AVAILABLE",
        "analytical_project_count":
            len(
                catalog.projects
            ),
        "mapped_project_count":
            0,
        "unmapped_project_count":
            len(
                catalog.projects
            ),
        "geometry_required_for_model_eligibility":
            False,
        "geometry_required_for_portfolio_selection":
            False,
        "fabricated_geometry":
            False,
        "crs_contract":
            "RFC_7946_EPSG_4326_IF_GEOMETRY_PRESENT",
        "limitations": [
            (
                "No governed cross-category runtime geometry "
                "is available at this checkpoint."
            ),
            (
                "Missing geometry does not remove an analytical "
                "project from Explore or Funding Plan."
            ),
            (
                "Council District assignments are contextual "
                "attributes and are not converted into project geometry."
            ),
        ],
        "features":
            [],
    }

    validated = (
        CrossCategoryMapContextArtifact
        .model_validate(
            payload
        )
    )

    return validated.model_dump(
        mode="json"
    )


def build_benchmark_payload() -> dict[str, object]:
    catalog = load_catalog()

    recon = (
        reconciliation_records()
    )

    catalog_ids = {
        project.decision_unit_id
        for project in catalog.projects
    }

    if set(recon) != catalog_ids:
        raise RuntimeBundleBuildError(
            "Benchmark/reconciliation identities do "
            "not equal runtime catalog identities."
        )

    project_outcomes = []

    category_project_counts = Counter()
    category_recommended_counts = Counter()
    category_recommendation_dollars = Counter()

    for project in sorted(
        catalog.projects,
        key=lambda item:
            item.decision_unit_id,
    ):
        record = recon[
            project.decision_unit_id
        ]

        recommendation = (
            record.get(
                "january_recommendation_dollars"
            )
        )

        if (
            recommendation is not None
            and (
                not isinstance(
                    recommendation,
                    int,
                )
                or recommendation <= 0
            )
        ):
            raise RuntimeBundleBuildError(
                f"{project.decision_unit_id}: "
                "invalid January recommendation amount"
            )

        historically_recommended = (
            recommendation is not None
        )

        category = str(
            project.presentation_category
        )

        category_project_counts[
            category
        ] += 1

        if historically_recommended:
            category_recommended_counts[
                category
            ] += 1

            category_recommendation_dollars[
                category
            ] += recommendation

        project_outcomes.append(
            {
                "decision_unit_id":
                    project.decision_unit_id,
                "canonical_project_id":
                    project.canonical_project_id,
                "governed_name":
                    project.governed_name,
                "presentation_category":
                    category,
                "historically_recommended":
                    historically_recommended,
                "january_recommendation_dollars":
                    recommendation,
                "source_conflict_flag":
                    bool(
                        record[
                            "source_conflict_flag"
                        ]
                    ),
                "request_version_conflict":
                    bool(
                        record[
                            "request_version_conflict"
                        ]
                    ),
                "outcome_role":
                    "BENCHMARK_OUTCOME_ONLY",
            }
        )

    recommended_count = sum(
        1
        for outcome
        in project_outcomes
        if outcome[
            "historically_recommended"
        ]
    )

    matched_total = sum(
        outcome[
            "january_recommendation_dollars"
        ]
        or 0
        for outcome
        in project_outcomes
    )

    if (
        recommended_count
        != CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT
    ):
        raise RuntimeBundleBuildError(
            "Expected exactly 20 historically "
            "recommended analytical projects."
        )

    if (
        matched_total
        != CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS
    ):
        raise RuntimeBundleBuildError(
            "Historical analytical-project "
            "recommendations must sum to $332M."
        )

    category_order = [
        "Transportation",
        "Parks & Open Space",
        "Watershed",
        "Community Facilities",
    ]

    category_summaries = [
        {
            "presentation_category":
                category,
            "analytical_project_count":
                category_project_counts[
                    category
                ],
            "historically_recommended_project_count":
                category_recommended_counts[
                    category
                ],
            "recommendation_total_dollars":
                category_recommendation_dollars[
                    category
                ],
        }
        for category
        in category_order
    ]

    payload = {
        "contract_version":
            CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
        "data_version":
            DATA_VERSION,
        "historical_decision_snapshot_date":
            "2026-01-21",
        "source_id":
            SOURCE_ID,
        "source_snapshot_sha256":
            source_sha256(),
        "outcome_role":
            "BENCHMARK_OUTCOME_ONLY",
        "analytical_project_count":
            CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
        "full_initial_recommendation_dollars":
            CROSS_CATEGORY_HISTORICAL_FULL_PACKAGE_DOLLARS,
        "matched_analytical_cohort_dollars":
            CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS,
        "outside_analytical_cohort_dollars":
            CROSS_CATEGORY_HISTORICAL_OUTSIDE_COHORT_DOLLARS,
        "historically_recommended_project_count":
            CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT,
        "ranking_input":
            False,
        "portfolio_selection_input":
            False,
        "category_summaries":
            category_summaries,
        "project_outcomes":
            project_outcomes,
        "limitations": [
            (
                "Historical Initial Draft Recommendation "
                "membership is an observed outcome only."
            ),
            (
                "Historical recommendation membership and "
                "amounts are not Funding Priority inputs."
            ),
            (
                "The $700M full package includes $368M "
                "outside the 106-project analytical cohort."
            ),
        ],
    }

    validated = (
        CrossCategoryBenchmarkArtifact
        .model_validate(
            payload
        )
    )

    return validated.model_dump(
        mode="json"
    )


def release_id(
    *,
    catalog_sha256: str,
    map_sha256: str,
    benchmark_sha256: str,
) -> str:
    semantic = (
        f"{DATA_VERSION}\n"
        f"{catalog_sha256}\n"
        f"{map_sha256}\n"
        f"{benchmark_sha256}\n"
    ).encode(
        "utf-8"
    )

    return sha256_bytes(
        semantic
    )


def build_manifest_payload() -> dict[str, object]:
    catalog = load_catalog()

    if (
        catalog.runtime_integration_authorized
        is not True
    ):
        raise RuntimeBundleBuildError(
            "Activated runtime-v2 release requires "
            "runtime_integration_authorized=true "
            "in the governed catalog."
        )

    if not MAP_PATH.is_file():
        raise RuntimeBundleBuildError(
            "map-context.geojson must exist before manifest."
        )

    if not BENCHMARK_PATH.is_file():
        raise RuntimeBundleBuildError(
            "benchmark.json must exist before manifest."
        )

    catalog_identity = (
        artifact_identity(
            CATALOG_PATH
        )
    )

    map_identity = (
        artifact_identity(
            MAP_PATH
        )
    )

    benchmark_identity = (
        artifact_identity(
            BENCHMARK_PATH
        )
    )

    payload = {
        "contract_version":
            CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION,
        "data_version":
            DATA_VERSION,
        "historical_decision_snapshot_date":
            "2026-01-21",
        "release_bundle_scope":
            "CROSS_CATEGORY_106_PROJECT_RUNTIME_V2",
        "release_id":
            release_id(
                catalog_sha256=(
                    catalog_identity[
                        "sha256"
                    ]
                ),
                map_sha256=(
                    map_identity[
                        "sha256"
                    ]
                ),
                benchmark_sha256=(
                    benchmark_identity[
                        "sha256"
                    ]
                ),
            ),
        "source_id":
            SOURCE_ID,
        "source_snapshot_sha256":
            source_sha256(),
        "contract_versions": {
            "catalog":
                CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
            "map_context":
                CROSS_CATEGORY_MAP_CONTEXT_CONTRACT_VERSION,
            "benchmark":
                CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
            "funding_plan":
                CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
            "manifest":
                CROSS_CATEGORY_RELEASE_MANIFEST_CONTRACT_VERSION,
        },
        "artifacts": {
            "catalog_json":
                catalog_identity,
            "map_context_geojson":
                map_identity,
            "benchmark_json":
                benchmark_identity,
        },
        "reconciliations": {
            "analytical_project_count":
                len(
                    catalog.projects
                ),
            "governed_request_total_dollars":
                sum(
                    project.model_request_dollars
                    for project
                    in catalog.projects
                ),
            "mapped_project_count":
                0,
            "unmapped_project_count":
                len(
                    catalog.projects
                ),
            "fabricated_geometry":
                False,
            "benchmark_matched_cohort_dollars":
                CROSS_CATEGORY_HISTORICAL_MATCHED_COHORT_DOLLARS,
            "benchmark_project_count":
                CROSS_CATEGORY_HISTORICALLY_RECOMMENDED_PROJECT_COUNT,
            "benchmark_isolated_from_catalog":
                True,
            "benchmark_isolated_from_portfolio_selection":
                True,
        },
        "runtime_integration_authorized":
            True,
    }

    validated = (
        CrossCategoryReleaseManifest
        .model_validate(
            payload
        )
    )

    return validated.model_dump(
        mode="json"
    )


def serialized_json(
    payload: dict[str, object],
) -> str:
    return (
        json.dumps(
            payload,
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n"
    )


def write_create_only(
    path: Path,
    rendered: str,
) -> str:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    if path.exists():
        existing = path.read_text(
            encoding="utf-8"
        )

        if existing == rendered:
            return "unchanged"

        raise DerivedArtifactConflictError(
            f"{path} already exists with "
            "different deterministic content."
        )

    path.write_text(
        rendered,
        encoding="utf-8",
    )

    return "created"


def write_bundle() -> dict[str, str]:
    map_result = (
        write_create_only(
            MAP_PATH,
            serialized_json(
                build_map_payload()
            ),
        )
    )

    benchmark_result = (
        write_create_only(
            BENCHMARK_PATH,
            serialized_json(
                build_benchmark_payload()
            ),
        )
    )

    manifest_result = (
        write_create_only(
            MANIFEST_PATH,
            serialized_json(
                build_manifest_payload()
            ),
        )
    )

    return {
        "map-context.geojson":
            map_result,
        "benchmark.json":
            benchmark_result,
        "manifest.json":
            manifest_result,
    }


def main() -> int:
    results = write_bundle()

    manifest = load_json(
        MANIFEST_PATH
    )

    benchmark = load_json(
        BENCHMARK_PATH
    )

    map_context = load_json(
        MAP_PATH
    )

    print(
        "M3.8D2 cross-category runtime bundle"
    )

    for (
        artifact,
        result,
    ) in results.items():
        print(
            f"{artifact}: {result}"
        )

    print(
        "Projects:",
        CROSS_CATEGORY_RUNTIME_PROJECT_COUNT,
    )

    print(
        "Governed request total:",
        f"${CROSS_CATEGORY_RUNTIME_REQUEST_TOTAL_DOLLARS:,.0f}",
    )

    print(
        "Mapped projects:",
        map_context[
            "mapped_project_count"
        ],
    )

    print(
        "Historical matched cohort:",
        f"${benchmark['matched_analytical_cohort_dollars']:,.0f}",
    )

    print(
        "Historical recommended projects:",
        benchmark[
            "historically_recommended_project_count"
        ],
    )

    print(
        "Runtime integration authorized:",
        manifest[
            "runtime_integration_authorized"
        ],
    )

    print(
        "Release ID:",
        manifest[
            "release_id"
        ],
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )