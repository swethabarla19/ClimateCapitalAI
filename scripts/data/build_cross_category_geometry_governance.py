"""Build the reviewed cross-category project-geometry governance artifact."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.cross_category_geometry import (
    CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION,
    CROSS_CATEGORY_GEOMETRY_GOVERNANCE_DECISION_ID,
    CrossCategoryGeometryGovernanceArtifact,
)


DATA_VERSION = "climatecapital-austin-2026-01-21-cross-category-v2"
CATALOG_PATH = ROOT / "data/governed/cross_category/runtime_v2/catalog.json"
RESEARCH_DIR = ROOT / "data/reconnaissance/external_gis/2026-09-08"
CANDIDATE_CSV_PATH = (
    RESEARCH_DIR / "CANDIDATE_NOT_GOVERNED_project_geometry_reconciliation.csv"
)
CANDIDATE_GEOMETRY_PATH = (
    RESEARCH_DIR / "CANDIDATE_NOT_GOVERNED_source_geometries.geojson"
)
CANDIDATE_REPORT_PATH = (
    ROOT / "docs/reference/CANDIDATE-external-gis-evidence-investigation-2026-09-08.md"
)
OUTPUT_PATH = (
    ROOT
    / "data/governed/cross_category/reconciliation/project-geometry-governance.json"
)


# This explicit allowlist is the result of individual governance review. It is
# intentionally not derived from the candidate eligibility column.
PROMOTED_IDS = frozenset(
    {
        "community-facilities/acme/asian-american-resource-center",
        "community-facilities/acme/dougherty-arts-center",
        "community-facilities/acme/george-washington-carver-museum",
        "community-facilities/acme/mexican-american-cultural-center",
        "community-facilities/acme/old-bakery-and-emporium",
        "community-facilities/animal-services/campus-improvements",
        "community-facilities/ems/demand-station-3",
        "community-facilities/ems/demand-station-4",
        "community-facilities/ems/station-03",
        "community-facilities/ems/station-14",
        "community-facilities/fire/station-14",
        "community-facilities/fire/station-15",
        "community-facilities/fire/station-20",
        "community-facilities/fire/station-26",
        "community-facilities/library/hampton-oak-hill",
        "community-facilities/library/milwood-branch",
        "community-facilities/police/canyon-creek-northwest",
        "parks/alamo-rec-center",
        "parks/big-stacy-pool",
        "parks/bolm-district-park",
        "parks/buttermilk-nh-park",
        "parks/civitan-pool",
        "parks/doris-miller-auditorium",
        "parks/garrison-pool",
        "parks/givens-district-park-phase-ii",
        "parks/grand-meadow-phase-ii",
        "parks/gus-garcia-center",
        "parks/harris-branch-nh-park-development",
        "parks/jamestown-nh-park",
        "parks/kennemer-pool",
        "parks/lorraine-camancho-center",
        "parks/martin-pool",
        "parks/metz-community-center",
        "parks/north-grounds-maintenance-facility",
        "parks/walter-e-long-metro-park-phase-i",
        "parks/woodland-pocket-park",
        "parks/woolridge-square-plan",
        "parks/yates-pocket-park",
        "transportation/barton-springs-bridge",
        "watershed/10878.010",
        "watershed/11889.004",
        "watershed/4015.001",
        "watershed/5282.043",
        "watershed/5282.133",
        "watershed/5282.134",
        "watershed/5282.150",
        "watershed/5282.162",
        "watershed/5754.089",
        "watershed/5754.139",
        "watershed/5754.145",
        "watershed/5754.147",
        "watershed/5754.149",
        "watershed/5789.075",
        "watershed/5789.107",
        "watershed/5789.121",
        "watershed/5789.126",
        "watershed/5789.136",
        "watershed/5789.139",
        "watershed/5789.141",
        "watershed/5789.145",
        "watershed/5789.146",
        "watershed/5848.053",
        "watershed/5848.070",
        "watershed/5848.071",
        "watershed/5848.087",
        "watershed/5848.091",
        "watershed/5848.092",
        "watershed/6039.109",
        "watershed/7492.011",
        "watershed/7492.032",
        "watershed/7492.045",
        "watershed/8598.014",
        "watershed/9999.235",
        "watershed/9999.236",
    }
)

DISPLAY_ROLE_MAP = {
    "OFFICIAL_PROJECT_DISPLAY_POINT": "PROJECT_DISPLAY_POINT",
    "OFFICIAL_PROJECT_GEOMETRY": "PROJECT_SITE",
    "OFFICIAL_PROJECT_PARCEL": "PROJECT_PARCEL",
    "PARK_SITE_CONTEXT": "PARK_SITE_CONTEXT",
    "FACILITY_SITE_CONTEXT": "FACILITY_SITE_CONTEXT",
}

SPECIAL_UNMAPPED_REASONS = {
    "watershed/5789.127": "IDENTITY_SCOPE_CONFLICT",
    "watershed/5789.150": "CITYWIDE_SINGLE_POINT_MISLEADING",
    "community-facilities/ems/demand-station-1": "CONFLICTING_OFFICIAL_LOCATIONS",
    "community-facilities/ems/demand-station-2": "CONFLICTING_OFFICIAL_LOCATIONS",
    "parks/bolm-maintenance-center": "OVERBROAD_CONTEXT_GEOMETRY",
    "community-facilities/acme/elizabet-ney-museum": "MULTIPLE_POSSIBLE_PROJECT_FEATURES",
    "community-facilities/acme/zilker-hillside-theatre": "ADDRESS_ONLY_NO_SOURCE_GEOMETRY",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def optional(value: str) -> str | None:
    return value or None


def historical_fit_class(row: dict[str, str]) -> str:
    fit = row["historical_fit_judgment"]
    if fit.startswith("YES_EXACT_SNAPSHOT"):
        return "EXACT_SNAPSHOT_DATE"
    if fit.startswith("YES_PRE_SNAPSHOT"):
        return "PRE_SNAPSHOT_SOURCE"
    if fit.startswith("CONDITIONAL_STABLE_LOCATION"):
        return "POST_SNAPSHOT_STABLE_LOCATION_ONLY"
    return "UNRESOLVED_OR_NOT_APPLICABLE"


def promoted_caveats(row: dict[str, str], role: str) -> list[str]:
    role_caveat = {
        "PROJECT_DISPLAY_POINT": (
            "Official project display point; it is not an engineering or construction footprint."
        ),
        "PROJECT_SITE": (
            "Source-native project-site geometry; later non-geographic project attributes are excluded."
        ),
        "PROJECT_PARCEL": (
            "Official parcel linked to the project; it is not necessarily the construction footprint."
        ),
        "PARK_SITE_CONTEXT": (
            "Whole-park context only; it is not necessarily the capital-project construction footprint."
        ),
        "FACILITY_SITE_CONTEXT": (
            "Existing facility-site context only; it is not necessarily the capital-project construction footprint."
        ),
        "PROJECT_CORRIDOR": (
            "Official project corridor; it must not be rendered as an inferred midpoint pin."
        ),
    }[role]
    caveats = [role_caveat]
    if row["research_notes"] and row["research_notes"] not in caveats:
        caveats.append(row["research_notes"])
    if historical_fit_class(row) == "POST_SNAPSHOT_STABLE_LOCATION_ONLY":
        caveats.append(
            "Post-snapshot source refresh is accepted for stable location only; later project facts are not governed."
        )
    return caveats


def unmapped_reason(row: dict[str, str]) -> str:
    decision_unit_id = row["decision_unit_id"]
    if decision_unit_id in SPECIAL_UNMAPPED_REASONS:
        return SPECIAL_UNMAPPED_REASONS[decision_unit_id]
    if row["presentation_category"] == "Transportation":
        return "CORRIDOR_OR_ASSET_GEOMETRY_NOT_FOUND"
    if row["match_confidence"] == "LOW":
        return "INSUFFICIENT_PROJECT_LINKAGE"
    return "NO_DEFENSIBLE_PROJECT_GEOMETRY"


def governance_status(row: dict[str, str]) -> str:
    if row["decision_unit_id"] in PROMOTED_IDS:
        return "PROMOTED"
    if row["match_confidence"] == "LOW":
        return "REJECTED_LOW_CONFIDENCE"
    if row["match_confidence"] == "NO_MATCH":
        return "REJECTED_NO_MATCH"
    return "HELD_FOR_MORE_EVIDENCE"


def build_payload() -> dict[str, object]:
    catalog = load_json(CATALOG_PATH)
    catalog_by_id = {
        project["decision_unit_id"]: project
        for project in catalog["projects"]
    }
    rows = list(csv.DictReader(CANDIDATE_CSV_PATH.open(encoding="utf-8")))
    rows_by_id = {row["decision_unit_id"]: row for row in rows}
    candidate_geometry = load_json(CANDIDATE_GEOMETRY_PATH)
    candidate_geometry_ids = {
        feature["properties"]["decision_unit_id"]
        for feature in candidate_geometry["features"]
    }

    if len(rows) != 106 or len(rows_by_id) != 106:
        raise ValueError("candidate reconciliation must contain 106 unique projects")
    if set(rows_by_id) != set(catalog_by_id):
        raise ValueError("candidate identities must equal the governed catalog")
    if len(PROMOTED_IDS) != 74:
        raise ValueError("explicit promotion allowlist must contain 74 projects")
    if not PROMOTED_IDS <= candidate_geometry_ids:
        raise ValueError("every promoted project must have captured source geometry")

    decisions = []
    for decision_unit_id in sorted(catalog_by_id):
        project = catalog_by_id[decision_unit_id]
        row = rows_by_id[decision_unit_id]
        status = governance_status(row)
        promoted = status == "PROMOTED"

        if promoted:
            if row["governance_eligibility"] != "ELIGIBLE_FOR_GOVERNANCE_REVIEW":
                raise ValueError(f"{decision_unit_id}: ineligible candidate in allowlist")
            if row["match_confidence"] != "HIGH":
                raise ValueError(f"{decision_unit_id}: promoted confidence changed")
            if row["geometry_origin"] != "source-native":
                raise ValueError(f"{decision_unit_id}: geometry is not source-native")
            if row["ambiguity_flag"] != "false":
                raise ValueError(f"{decision_unit_id}: unresolved ambiguity")
            role = DISPLAY_ROLE_MAP[row["display_role"]]
            rationale = (
                f"Promoted after individual review: {row['match_method']}. "
                f"The governed display role is {role}."
            )
            caveats = promoted_caveats(row, role)
            reason_code = None
        else:
            role = None
            reason_code = unmapped_reason(row)
            rationale_detail = (
                row["ambiguity_notes"]
                or row["research_notes"]
                or row["match_method"]
            )
            rationale = f"Remain unmapped ({reason_code}): {rationale_detail}"
            caveats = [rationale_detail]

        decisions.append(
            {
                "decision_unit_id": decision_unit_id,
                "governed_name": project["governed_name"],
                "presentation_category": project["presentation_category"],
                "governance_status": status,
                "reviewed_individually": True,
                "governance_rationale": rationale,
                "unmapped_reason_code": reason_code,
                "candidate_source_title": row["candidate_source_title"],
                "source_url": row["source_url"],
                "arcgis_item_id": optional(row["arcgis_item_id"]),
                "arcgis_service_id": optional(row["arcgis_service_id"]),
                "source_layer_id": optional(row["layer_id"]),
                "source_feature_id": optional(row["feature_object_id"]),
                "source_agency": row["source_agency"],
                "candidate_geometry_type": row["geometry_type"],
                "candidate_geometry_origin": row["geometry_origin"],
                "candidate_confidence": row["match_confidence"],
                "candidate_governance_eligibility": row["governance_eligibility"],
                "candidate_ambiguity": row["ambiguity_flag"] == "true",
                "candidate_multiple_possible_features": (
                    row["multiple_possible_features"] == "true"
                ),
                "source_date": optional(row["source_date"]),
                "source_last_updated_date": optional(row["last_updated_date"]),
                "historical_fit_class": historical_fit_class(row),
                "historical_fit_judgment": row["historical_fit_judgment"],
                "match_identifiers": row["match_identifiers"],
                "match_method": row["match_method"],
                "display_role": role,
                "caveats": caveats,
            }
        )

    payload = {
        "contract_version": CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION,
        "data_version": DATA_VERSION,
        "historical_decision_snapshot_date": "2026-01-21",
        "governance_decision_id": CROSS_CATEGORY_GEOMETRY_GOVERNANCE_DECISION_ID,
        "governance_review_date": "2026-09-08",
        "project_identity_key": "decision_unit_id",
        "analytical_project_count": 106,
        "candidates_reviewed_count": 106,
        "promotion_candidates_reviewed_individually": 74,
        "promoted_project_count": 74,
        "unmapped_project_count": 32,
        "fabricated_geometry": False,
        "geocoded_geometry": False,
        "inferred_or_centroid_geometry": False,
        "geometry_changes_analytical_eligibility": False,
        "geometry_changes_funding_priority": False,
        "geometry_changes_funding_plan": False,
        "geometry_changes_historical_benchmark": False,
        "candidate_reconciliation": {
            "path": str(CANDIDATE_CSV_PATH.relative_to(ROOT)),
            "sha256": sha256(CANDIDATE_CSV_PATH),
        },
        "candidate_geometry_snapshot": {
            "path": str(CANDIDATE_GEOMETRY_PATH.relative_to(ROOT)),
            "sha256": sha256(CANDIDATE_GEOMETRY_PATH),
        },
        "candidate_investigation_report": {
            "path": str(CANDIDATE_REPORT_PATH.relative_to(ROOT)),
            "sha256": sha256(CANDIDATE_REPORT_PATH),
        },
        "decisions": decisions,
    }
    validated = CrossCategoryGeometryGovernanceArtifact.model_validate(payload)
    return validated.model_dump(mode="json")


def serialized_json(payload: dict[str, object]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def write_artifact() -> str:
    rendered = serialized_json(build_payload())
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_PATH.exists():
        if OUTPUT_PATH.read_text(encoding="utf-8") == rendered:
            return "unchanged"
        raise RuntimeError(f"{OUTPUT_PATH} exists with different governed content")
    OUTPUT_PATH.write_text(rendered, encoding="utf-8")
    return "created"


def main() -> int:
    result = write_artifact()
    payload = load_json(OUTPUT_PATH)
    print(f"project-geometry-governance.json: {result}")
    print(f"Promoted projects: {payload['promoted_project_count']}")
    print(f"Unmapped projects: {payload['unmapped_project_count']}")
    print(f"SHA-256: {sha256(OUTPUT_PATH)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
