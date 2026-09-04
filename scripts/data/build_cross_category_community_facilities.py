"""Build the governed M3.5 Community Facilities source-row slice."""

from __future__ import annotations

import json
from pathlib import Path


JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
JUL_SOURCE_ID = (
    "austin_2026_bond_initial_project_request_list_2025_07_31"
)

OUT_PATH = Path(
    "data/governed/cross_category/source_rows/community_facilities.json"
)

# (
#   id,
#   department,
#   domain,
#   name,
#   type,
#   score,
#   request,
#   recommendation,
# )
rows = [
    # Cultural / ACME — 7 analytical projects
    (
        "community-facilities/acme/dougherty-arts-center",
        "ACME",
        "Cultural / ACME",
        "Dougherty Arts Center",
        "ANALYTICAL_PROJECT",
        77,
        45_000_000,
        None,
    ),
    (
        "community-facilities/acme/george-washington-carver-museum",
        "ACME",
        "Cultural / ACME",
        "George Washington Carver Museum Phase 1a and 1b",
        "ANALYTICAL_PROJECT",
        70,
        12_000_000,
        None,
    ),
    (
        "community-facilities/acme/elizabet-ney-museum",
        "ACME",
        "Cultural / ACME",
        "Elizabet Ney Museum ADA Restroom and Storage Facility",
        "ANALYTICAL_PROJECT",
        66,
        1_000_000,
        None,
    ),
    (
        "community-facilities/acme/mexican-american-cultural-center",
        "ACME",
        "Cultural / ACME",
        "Mexican American Cultural Center",
        "ANALYTICAL_PROJECT",
        64,
        12_000_000,
        None,
    ),
    (
        "community-facilities/acme/zilker-hillside-theatre",
        "ACME",
        "Cultural / ACME",
        "Zilker Hillside Theatre",
        "ANALYTICAL_PROJECT",
        59,
        5_000_000,
        None,
    ),
    (
        "community-facilities/acme/asian-american-resource-center",
        "ACME",
        "Cultural / ACME",
        "Asian American Resource Center",
        "ANALYTICAL_PROJECT",
        60,
        58_000_000,
        None,
    ),
    (
        "community-facilities/acme/old-bakery-and-emporium",
        "ACME",
        "Cultural / ACME",
        "Old Bakery and Emporium",
        "ANALYTICAL_PROJECT",
        45,
        10_000_000,
        None,
    ),

    # Libraries — 3 analytical projects + 2 program buckets
    (
        "community-facilities/library/colony-park-branch-library",
        "Austin Public Library",
        "Libraries",
        "Colony Park Branch Library",
        "ANALYTICAL_PROJECT",
        69,
        58_000_000,
        None,
    ),
    (
        "community-facilities/library/regional-library-land-acquisition",
        "Austin Public Library",
        "Libraries",
        "Regional Library Land Acquisition",
        "PROGRAM_BUCKET",
        68,
        20_000_000,
        None,
    ),
    (
        "community-facilities/library/hampton-oak-hill",
        "Austin Public Library",
        "Libraries",
        "Hampton at Oak Hill Branch Renovation and Expansion",
        "ANALYTICAL_PROJECT",
        65,
        19_000_000,
        20_000_000,
    ),
    (
        "community-facilities/library/milwood-branch",
        "Austin Public Library",
        "Libraries",
        "Milwood Branch Library Renovation and Expansion",
        "ANALYTICAL_PROJECT",
        65,
        24_000_000,
        None,
    ),
    (
        "community-facilities/library/safe-secure-libraries",
        "Austin Public Library",
        "Libraries",
        "Safe & Secure Libraries Project",
        "PROGRAM_BUCKET",
        54,
        10_800_000,
        None,
    ),

    # Public Health — 2 analytical projects
    (
        "community-facilities/public-health/colony-park",
        "Austin Public Health",
        "Public Health",
        "Colony Park Public Health Center",
        "ANALYTICAL_PROJECT",
        74,
        42_000_000,
        None,
    ),
    (
        "community-facilities/public-health/northeast",
        "Austin Public Health",
        "Public Health",
        "Northeast Public Health Center",
        "ANALYTICAL_PROJECT",
        72,
        51_000_000,
        None,
    ),

    # EMS — 7 analytical projects
    (
        "community-facilities/ems/demand-station-1",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Demand Station #1 (401 E 5th St)",
        "ANALYTICAL_PROJECT",
        56,
        21_000_000,
        None,
    ),
    (
        "community-facilities/ems/station-03",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Station #03 (1305 Red River St)",
        "ANALYTICAL_PROJECT",
        54.5,
        18_000_000,
        None,
    ),
    (
        "community-facilities/ems/station-14",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Station #14 (7200 Berkman Dr)",
        "ANALYTICAL_PROJECT",
        53.5,
        20_000_000,
        None,
    ),
    (
        "community-facilities/ems/demand-station-9",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Demand Station #9",
        "ANALYTICAL_PROJECT",
        51,
        28_000_000,
        None,
    ),
    (
        "community-facilities/ems/demand-station-2",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Demand Station #2",
        "ANALYTICAL_PROJECT",
        46,
        18_000_000,
        None,
    ),
    (
        "community-facilities/ems/demand-station-4",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Demand Station #4",
        "ANALYTICAL_PROJECT",
        46,
        18_000_000,
        None,
    ),
    (
        "community-facilities/ems/demand-station-3",
        "EMS",
        "Emergency Medical Services",
        "ATCEMS Demand Station #3 (1705 S Congress Ave)",
        "ANALYTICAL_PROJECT",
        46,
        20_000_000,
        None,
    ),

    # Fire — 5 analytical projects
    (
        "community-facilities/fire/station-26",
        "Fire",
        "Fire",
        "Fire Station 26 Expansion",
        "ANALYTICAL_PROJECT",
        50,
        29_000_000,
        29_000_000,
    ),
    (
        "community-facilities/fire/station-15",
        "Fire",
        "Fire",
        "Fire Station 15 Renovation",
        "ANALYTICAL_PROJECT",
        49,
        35_000_000,
        None,
    ),
    (
        "community-facilities/fire/station-14",
        "Fire",
        "Fire",
        "Fire Station 14 Renovation",
        "ANALYTICAL_PROJECT",
        47,
        26_000_000,
        None,
    ),
    (
        "community-facilities/fire/station-20",
        "Fire",
        "Fire",
        "Fire Station 20 Renovation",
        "ANALYTICAL_PROJECT",
        46,
        26_000_000,
        None,
    ),
    (
        "community-facilities/fire/education-building-b",
        "Fire",
        "Fire",
        "Education Building B",
        "ANALYTICAL_PROJECT",
        40,
        71_000_000,
        None,
    ),

    # Fleet — 4 analytical projects
    (
        "community-facilities/fleet/consolidated-service-center",
        "Fleet Services",
        "Fleet Services",
        "Consolidated Fleet Service Center (South/Southeast)",
        "ANALYTICAL_PROJECT",
        50.5,
        245_000_000,
        10_000_000,
    ),
    (
        "community-facilities/fleet/fuel-station-southeast",
        "Fleet Services",
        "Fleet Services",
        "Fuel Station Southeast",
        "ANALYTICAL_PROJECT",
        50,
        10_200_000,
        None,
    ),
    (
        "community-facilities/fleet/fuel-station-central",
        "Fleet Services",
        "Fleet Services",
        "Fuel Station Central",
        "ANALYTICAL_PROJECT",
        50,
        10_500_000,
        None,
    ),
    (
        "community-facilities/fleet/fuel-station-northwest",
        "Fleet Services",
        "Fleet Services",
        "Fuel Station Northwest",
        "ANALYTICAL_PROJECT",
        50,
        10_200_000,
        None,
    ),

    # Homeless Strategy — 1 program bucket + 1 analytical project
    (
        "community-facilities/hso/austin-shelters",
        "HSO",
        "Homeless Strategy",
        "Austin Shelters",
        "PROGRAM_BUCKET",
        52,
        50_000_000,
        25_000_000,
    ),
    (
        "community-facilities/hso/north-austin-homeless-resource-center",
        "HSO",
        "Homeless Strategy",
        "North Austin Homeless Resource Center",
        "ANALYTICAL_PROJECT",
        51,
        15_000_000,
        None,
    ),

    # Police — 7 analytical projects
    (
        "community-facilities/police/canyon-creek-northwest",
        "Police",
        "Police",
        "Canyon Creek Northwest Substation",
        "ANALYTICAL_PROJECT",
        67,
        60_500_000,
        62_000_000,
    ),
    (
        "community-facilities/police/scenario-based-training",
        "Police",
        "Police",
        "Scenario Based Training Facility",
        "ANALYTICAL_PROJECT",
        51,
        100_000_000,
        None,
    ),
    (
        "community-facilities/police/air-operations",
        "Police",
        "Police",
        "Police Air Operations Facility",
        "ANALYTICAL_PROJECT",
        49,
        10_000_000,
        None,
    ),
    (
        "community-facilities/police/downtown-substation",
        "Police",
        "Police",
        "Downtown Police Substation",
        "ANALYTICAL_PROJECT",
        47,
        40_000_000,
        None,
    ),
    (
        "community-facilities/police/northeast-substation",
        "Police",
        "Police",
        "Northeast Police Substation",
        "ANALYTICAL_PROJECT",
        44,
        10_000_000,
        None,
    ),
    (
        "community-facilities/police/southwest-substation",
        "Police",
        "Police",
        "Southwest Police Substation",
        "ANALYTICAL_PROJECT",
        44,
        10_000_000,
        None,
    ),
    (
        "community-facilities/police/central-west-substation",
        "Police",
        "Police",
        "Central West Police Substation",
        "ANALYTICAL_PROJECT",
        43,
        10_000_000,
        None,
    ),

    # Animal Services — 1 analytical project
    (
        "community-facilities/animal-services/campus-improvements",
        "Animal Services",
        "Animal Services",
        "Animal Service Center Campus Improvements",
        "ANALYTICAL_PROJECT",
        61,
        40_000_000,
        3_000_000,
    ),

    # Municipal Court — 1 analytical project
    (
        "community-facilities/municipal-court/customer-service-center",
        "Municipal Court",
        "Municipal Court",
        "Municipal Court Customer Service Center",
        "ANALYTICAL_PROJECT",
        44,
        10_000_000,
        None,
    ),
]


# Earlier July source versions that materially differ from January.
july_versions = {
    "community-facilities/acme/george-washington-carver-museum": {
        "source_name": "George Washington Carver Museum Phase 1a and 1b",
        "department_request_dollars": 6_000_000,
        "notes": "July request was $6M; January PRB request is $12M.",
    },
    "community-facilities/library/colony-park-branch-library": {
        "source_name": "Colony Park Branch Library",
        "department_request_dollars": 58_800_000,
        "notes": "July request was $58.8M; January PRB request is $58M.",
    },
    "community-facilities/library/safe-secure-libraries": {
        "source_name": "Safe & Ready Libraries Project",
        "department_request_dollars": 10_800_000,
        "notes": (
            "July source used Safe & Ready Libraries Project; "
            "January PRB uses Safe & Secure Libraries Project."
        ),
    },
}


result = []

for (
    unit_id,
    department,
    domain,
    name,
    unit_type,
    score,
    request,
    recommendation,
) in rows:
    source_ids = [JAN_SOURCE_ID]
    source_versions = []

    if unit_id in july_versions:
        july = july_versions[unit_id]
        source_ids.insert(0, JUL_SOURCE_ID)
        source_versions.append(
            {
                "source_id": JUL_SOURCE_ID,
                "source_date": "2025-07-31",
                "source_name": july["source_name"],
                "department_request_dollars": (
                    july["department_request_dollars"]
                ),
                "historical_recommendation_amount_dollars": None,
                "prb_score": None,
                "notes": july["notes"],
            }
        )

    source_versions.append(
        {
            "source_id": JAN_SOURCE_ID,
            "source_date": "2026-01-21",
            "source_name": name,
            "department_request_dollars": request,
            "historical_recommendation_amount_dollars": recommendation,
            "prb_score": score,
            "notes": "January 21 PRB scoring snapshot.",
        }
    )

    result.append(
        {
            "decision_unit_id": unit_id,
            "canonical_project_id": None,
            "source_name": name,
            "source_department": department,
            "source_domain": domain,
            "presentation_category": "Community Facilities",
            "analytical_unit_type": unit_type,
            "analytical_unit": unit_type == "ANALYTICAL_PROJECT",
            "prb_scored": True,
            "prb_score": score,
            "department_request_dollars": request,
            "historical_recommendation_amount_dollars": recommendation,
            "evidence_feasibility_status": "NOT_EVALUATED",
            "model_eligible": False,
            "exclusion_reason": (
                None
                if unit_type == "ANALYTICAL_PROJECT"
                else "PROGRAM_BUCKET"
            ),
            "source_ids": source_ids,
            "source_versions": source_versions,
            "source_conflict_flag": unit_id in july_versions,
        }
    )


assert len(result) == 41

analytical = [
    row
    for row in result
    if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
]
programs = [
    row
    for row in result
    if row["analytical_unit_type"] == "PROGRAM_BUCKET"
]

assert len(analytical) == 38
assert len(programs) == 3

analytical_request_total = sum(
    row["department_request_dollars"] or 0
    for row in analytical
)

analytical_recommendation_total = sum(
    row["historical_recommendation_amount_dollars"] or 0
    for row in analytical
)

all_recommendation_total = sum(
    row["historical_recommendation_amount_dollars"] or 0
    for row in result
)

assert analytical_request_total == 1_248_400_000
assert analytical_recommendation_total == 124_000_000
assert all_recommendation_total == 149_000_000

conflicts = [
    row["decision_unit_id"]
    for row in result
    if row["source_conflict_flag"]
]

assert conflicts == [
    "community-facilities/acme/george-washington-carver-museum",
    "community-facilities/library/colony-park-branch-library",
    "community-facilities/library/safe-secure-libraries",
]

OUT_PATH.write_text(json.dumps(result, indent=2) + "\n")

print(f"wrote {len(result)} Community Facilities rows to {OUT_PATH}")
print(f"analytical projects = {len(analytical)}")
print(f"program buckets = {len(programs)}")
print(f"analytical request total = ${analytical_request_total:,}")
print(
    "analytical historical recommendation = "
    f"${analytical_recommendation_total:,}"
)
print(f"all historical recommendations = ${all_recommendation_total:,}")
print(f"source-version conflicts = {len(conflicts)}")