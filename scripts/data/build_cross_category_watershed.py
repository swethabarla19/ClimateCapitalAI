import csv
import json
from pathlib import Path

NOV_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"

CSV_PATH = Path(
    "data/reconnaissance/city_austin/"
    "watershed_bond_projects/2025-11-21/projects.csv"
)

OUT_PATH = Path(
    "data/governed/cross_category/source_rows/watershed.json"
)

# January 21 PRB overlay keyed to the canonical Nov. 21 subproject ID.
# Values:
#   prb_name, prb_score, prb_request_dollars, historical_recommendation_dollars
overlay = {
    "4015.001": (
        "Country Club Creek Metcalf & Oltorf Wastewater Improvements",
        66, 5_470_000, 5_470_000,
    ),
    "5282.043": (
        "Tannehill Creek - Morris Williams Stormwater Improvements",
        73, 8_500_000, 8_500_000,
    ),
    "5282.133": (
        "Boggy Creek Kealing Park Green Infrastructure Retrofits",
        73, 1_300_000, 1_300_000,
    ),
    "5282.134": (
        "Walnut Creek - Tannehill Creek Bartholomew Park Stormwater Retrofit",
        74, 1_400_000, 1_400_000,
    ),
    "5282.150": (
        "Lady Bird Lake - W. Austin Park Water Quality Retrofits",
        69, 2_625_000, None,
    ),
    "5282.162": (
        "CapEx",
        68, 21_650_000, 21_650_000,
    ),
    "5754.089": (
        "Walnut Creek - McNeal Dr Low Water Crossing Improvement",
        71, 1_500_000, 1_500_000,
    ),
    "5754.139": (
        "Onion Creek - Paces Mill Creek Flood Risk Reduction",
        65, 8_100_000, None,
    ),
    "5754.145": (
        "Dry Creek North - Highland Hills Low Water Crossing",
        66, 1_075_000, 1_075_000,
    ),
    "5754.147": (
        "Boggy Creek - Corps Flood Control Ecosystem Restoration",
        62, 3_750_000, None,
    ),
    "5754.149": (
        "Country Club West - Riverside Farms Low Water Crossing Improvements",
        63, 2_625_000, None,
    ),
    "5789.075": (
        "Waller Creek - Guadalupe St. Flood Risk Reduction Phase I - III",
        67, 35_000_000, 35_000_000,
    ),
    "5789.107": (
        "Barton Creek - Oak Park Local Flood Risk Reduction",
        64, 16_750_000, None,
    ),
    "5789.121": (
        "Taylor Slough S. - Warren St. Flood Risk Reduction",
        58, 6_255_000, None,
    ),
    "5789.126": (
        "Walnut Creek - North Acres Storm Drain Improvements",
        73, 21_250_000, 21_250_000,
    ),
    "5789.127": (
        "West Boldin Creek - Hether St. Storm drain Improvements",
        60, 11_000_000, None,
    ),
    "5789.136": (
        "Slaughter Creek - Vassal Dr. Flood Risk Reduction Phase I",
        65, 7_700_000, 6_355_000,
    ),
    "5789.139": (
        "Walnut Creek - West Cow Path Flood Risk Reduction",
        56, 11_250_000, None,
    ),
    "5789.141": (
        "Boggy Creek - Oakwood Cemetery Storm drain Reroute",
        61, 7_350_000, None,
    ),
    "5789.150": (
        "City Storm Drain Renewal Downtown",
        60, 3_000_000, None,
    ),
    "5789.145": (
        "Williamson Creek - Brassiewood Dr. Phase III Stormwater Improvements",
        68, 20_000_000, 20_000_000,
    ),
    "5789.146": (
        "E. Bouldin - Annie St. Flood Risk Reduction Phase II",
        66, 4_450_000, None,
    ),
    "5848.053": (
        "Boggy Creek - Clarkson Tributary Rehabilitation",
        62, 5_195_000, None,
    ),
    "5848.070": (
        "Shoal Creek - Grover Channel Stabilization",
        52, 22_000_000, None,
    ),
    "5848.071": (
        "Walnut Creek - Wells Branch Willow Bend Stream Restoration",
        62, 5_000_000, None,
    ),
    "5848.087": (
        "Sunken Garden Erosion Protection",
        56, 7_125_000, None,
    ),
    "5848.091": (
        "Walnut Creek - Eubank Tributary Stream Stabilization",
        64, 5_200_000, None,
    ),
    "5848.092": (
        "Little Walnut Creek Loyola Ln. and Dottie Jordan Park Stream Stabilization",
        67, 4_000_000, None,
    ),
    "6039.109": (
        "Shoal Creek - Brentwood Drainage Improvement",
        61, 33_500_000, None,
    ),
    "7492.011": (
        "Walnut Creek Duval Dam Modernization",
        59, 4_200_000, None,
    ),
    "7492.032": (
        "Shoal Creek - NW Park Dam Modernization",
        59, 10_500_000, None,
    ),
    "7492.045": (
        "Bull Creek - Bintliff Dam Modernization",
        56, 2_750_000, None,
    ),
    "8598.014": (
        "Boggy Creek - MLK TOD Stormwater Conveyance Improvements Phase III",
        67, 1_500_000, 1_500_000,
    ),
    "9999.235": (
        "Walnut Creek - Oak Creek Low Water Crossing",
        59, 5_000_000, None,
    ),
    "9999.236": (
        "Johnson Creek Low Water Crossing",
        62, 8_750_000, None,
    ),
    "10878.010": (
        "Waller Creek Tunnel Outlet Improvement",
        65, 8_750_000, None,
    ),
    "11889.004": (
        "William Cannon Dr. Corridor",
        63, 2_625_000, None,
    ),
}

with CSV_PATH.open(newline="") as f:
    canonical_rows = list(csv.DictReader(f))

assert len(canonical_rows) == 37
assert set(overlay) == {row["subproject_id"] for row in canonical_rows}

result = []

for row in canonical_rows:
    project_id = row["subproject_id"]
    canonical_name = row["project_name"]
    canonical_request = int(
        row["current_funding_request_estimate_dollars"]
    )

    (
        prb_name,
        prb_score,
        prb_request,
        recommendation,
    ) = overlay[project_id]

    source_conflict = canonical_request != prb_request

    result.append(
        {
            "decision_unit_id": f"watershed/{project_id}",
            "canonical_project_id": project_id,

            # Canonical identity remains Nov. 21.
            "source_name": canonical_name,
            "source_department": "Watershed Protection",
            "source_domain": "Watershed Protection",
            "presentation_category": "Watershed",

            "analytical_unit_type": "ANALYTICAL_PROJECT",
            "analytical_unit": True,

            # January PRB scoring overlay.
            "prb_scored": True,
            "prb_score": prb_score,

            # Top-level request remains the governed Nov. 21 project request.
            "department_request_dollars": canonical_request,

            # Historical recommendation is a separate January attribute.
            "historical_recommendation_amount_dollars": recommendation,

            # M3.5 does not automatically make projects model-eligible.
            "evidence_feasibility_status": "NOT_EVALUATED",
            "model_eligible": False,
            "exclusion_reason": None,

            "source_ids": [
                NOV_SOURCE_ID,
                JAN_SOURCE_ID,
            ],
            "source_versions": [
                {
                    "source_id": NOV_SOURCE_ID,
                    "source_date": "2025-11-21",
                    "source_name": canonical_name,
                    "department_request_dollars": canonical_request,
                    "historical_recommendation_amount_dollars": None,
                    "prb_score": None,
                    "notes": "Canonical Watershed source-universe record.",
                },
                {
                    "source_id": JAN_SOURCE_ID,
                    "source_date": "2026-01-21",
                    "source_name": prb_name,
                    "department_request_dollars": prb_request,
                    "historical_recommendation_amount_dollars": recommendation,
                    "prb_score": prb_score,
                    "notes": "January PRB scoring and historical recommendation overlay.",
                },
            ],
            "source_conflict_flag": source_conflict,
        }
    )

program_rows = [
    (
        "watershed/small-scale-asset-management",
        "Small Scale Stormwater & Drainage Asset Management Opportunities",
        "PROGRAM_BUCKET",
        69,
        36_000_000,
        7_000_000,
    ),
    (
        "watershed/partnership-opportunities",
        "Stormwater & Drainage Partnership Opportunities",
        "PROGRAM_BUCKET",
        68,
        140_000_000,
        15_000_000,
    ),
    (
        "watershed/stormwater-resilience-program",
        "Stormwater Resilience Program",
        "PROGRAM_BUCKET",
        66,
        50_000_000,
        3_000_000,
    ),
    (
        "watershed/facility-for-operations",
        "Watershed Protection - Facility for Operations",
        "PROGRAM_BUCKET",
        51,
        16_000_000,
        None,
    ),
    (
        "watershed/open-space-acquisition",
        "Open Space Acquisition",
        "NOT_SCORED",
        None,
        300_000_000,
        10_000_000,
    ),
]

for unit_id, name, unit_type, score, request, recommendation in program_rows:
    scored = unit_type == "PROGRAM_BUCKET"

    result.append(
        {
            "decision_unit_id": unit_id,
            "canonical_project_id": None,
            "source_name": name,
            "source_department": (
                "Office of Climate Action and Resilience, Austin Water, "
                "Watershed Protection Department"
                if unit_type == "NOT_SCORED"
                else "Watershed Protection"
            ),
            "source_domain": "Watershed Protection",
            "presentation_category": "Watershed",
            "analytical_unit_type": unit_type,
            "analytical_unit": False,
            "prb_scored": scored,
            "prb_score": score,
            "department_request_dollars": request,
            "historical_recommendation_amount_dollars": recommendation,
            "evidence_feasibility_status": "NOT_EVALUATED",
            "model_eligible": False,
            "exclusion_reason": (
                "PROGRAM_BUCKET"
                if unit_type == "PROGRAM_BUCKET"
                else "PRB_NOT_SCORED"
            ),
            "source_ids": [JAN_SOURCE_ID],
            "source_versions": [
                {
                    "source_id": JAN_SOURCE_ID,
                    "source_date": "2026-01-21",
                    "source_name": name,
                    "department_request_dollars": request,
                    "historical_recommendation_amount_dollars": recommendation,
                    "prb_score": score,
                    "notes": None,
                }
            ],
            "source_conflict_flag": False,
        }
    )

assert len(result) == 42

canonical_total = sum(
    unit["department_request_dollars"]
    for unit in result
    if unit["analytical_unit_type"] == "ANALYTICAL_PROJECT"
)

jan_prb_total = sum(
    next(
        version["department_request_dollars"]
        for version in unit["source_versions"]
        if version["source_id"] == JAN_SOURCE_ID
    )
    for unit in result
    if unit["analytical_unit_type"] == "ANALYTICAL_PROJECT"
)

recommendation_total = sum(
    unit["historical_recommendation_amount_dollars"] or 0
    for unit in result
    if unit["analytical_unit_type"] == "ANALYTICAL_PROJECT"
)

assert canonical_total == 327_970_000
assert jan_prb_total == 328_095_000
assert recommendation_total == 125_000_000

conflicts = [
    unit["canonical_project_id"]
    for unit in result
    if unit["source_conflict_flag"]
]

assert conflicts == ["5754.149"]

OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")

print(f"wrote {len(result)} Watershed rows to {OUT_PATH}")
print(f"canonical project total = ${canonical_total:,}")
print(f"January PRB project total = ${jan_prb_total:,}")
print(f"historical project recommendation = ${recommendation_total:,}")
print(f"source conflicts = {conflicts}")