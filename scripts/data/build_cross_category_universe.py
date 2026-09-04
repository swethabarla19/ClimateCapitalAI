"""Assemble and validate the governed M3.5 cross-category universe."""

from __future__ import annotations

import json
from pathlib import Path

from climatecapital.contracts.cross_category import (
    CrossCategoryUniverseArtifact,
)


ROOT = Path("data/governed/cross_category")

SLICE_PATHS = (
    ROOT / "source_rows/transportation.json",
    ROOT / "source_rows/parks.json",
    ROOT / "source_rows/watershed.json",
    ROOT / "source_rows/community_facilities.json",
    ROOT / "source_rows/affordable_housing.json",
)

OUT_PATH = ROOT / "cross-category-universe.json"


decision_units = []

for path in SLICE_PATHS:
    rows = json.loads(path.read_text())
    if not isinstance(rows, list):
        raise RuntimeError(f"{path} must contain a JSON array")

    decision_units.extend(rows)


artifact_data = {
    "contract_version": "p0-cross-category-universe/1.0.0",
    "data_version": "m3-6-cross-category-2026-09-04",
    "governance_checkpoint": "M3.5",
    "governance_status": "APPROVED",
    "historical_decision_snapshot_date": "2026-01-21",
    "summary": {
        "source_row_count": 136,
        "analytical_project_count": 106,
        "program_bucket_count": 23,
        "program_allocation_count": 4,
        "not_scored_count": 3,
        "source_rows_by_presentation_category": {
            "transportation": 18,
            "parks_open_space": 34,
            "watershed": 42,
            "community_facilities": 41,
            "affordable_housing": 1,
        },
        "analytical_projects_by_presentation_category": {
            "transportation": 9,
            "parks_open_space": 22,
            "watershed": 37,
            "community_facilities": 38,
        },
    },
    "decision_units": decision_units,
}


# This is the governing validation gate.
artifact = CrossCategoryUniverseArtifact.model_validate(artifact_data)

serialized = artifact.model_dump(
    mode="json",
    by_alias=True,
)

OUT_PATH.write_text(
    json.dumps(serialized, indent=2) + "\n"
)

print(f"wrote governed artifact: {OUT_PATH}")
print(f"source rows = {len(artifact.decision_units)}")
print(
    "classifications = "
    f"{artifact.summary.analytical_project_count} analytical projects / "
    f"{artifact.summary.program_bucket_count} program buckets / "
    f"{artifact.summary.program_allocation_count} program allocations / "
    f"{artifact.summary.not_scored_count} not scored"
)