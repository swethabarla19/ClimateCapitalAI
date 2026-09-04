"""Register the July 31, 2025 Initial Project Request List source."""

from __future__ import annotations

import csv
import hashlib
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


REGISTRY_PATH = Path("data/metadata/source_registry.csv")
RAW_PATH = Path(
    "data/staging/raw/city_austin/"
    "initial_project_request_list/2025-07-31/source.pdf"
)

JAN_SOURCE_ID = "austin_2026_bond_initial_draft_2026_01_21"
SOURCE_ID = "austin_2026_bond_initial_project_request_list_2025_07_31"


with REGISTRY_PATH.open(newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fieldnames = reader.fieldnames

if fieldnames is None:
    raise RuntimeError("source registry has no header")

existing_ids = {row["source_id"] for row in rows}

if SOURCE_ID in existing_ids:
    raise RuntimeError(f"{SOURCE_ID} is already registered")

jan_source = next(
    row
    for row in rows
    if row["source_id"] == JAN_SOURCE_ID
)

# Reuse the already-governed City EDIMS URL structure,
# changing only the official document identifier.
source_url = jan_source["source_url"].replace("466344", "456140")

if source_url == jan_source["source_url"]:
    raise RuntimeError("could not derive July 31 City source URL")

RAW_PATH.parent.mkdir(parents=True, exist_ok=True)

with urllib.request.urlopen(source_url, timeout=60) as response:
    pdf_bytes = response.read()

if not pdf_bytes.startswith(b"%PDF"):
    raise RuntimeError("downloaded source is not a PDF")

RAW_PATH.write_bytes(pdf_bytes)

checksum = hashlib.sha256(pdf_bytes).hexdigest()

retrieved_at = (
    datetime.now(timezone.utc)
    .replace(microsecond=0)
    .isoformat()
    .replace("+00:00", "Z")
)

new_row = {
    "source_id": SOURCE_ID,
    "dataset_name": (
        "Initial Project Request List - 2026 Bond Development Update"
    ),
    "publisher": "City of Austin - Capital Delivery Services",
    "source_url": source_url,
    "source_vintage": "2025-07-31 initial project request list",
    "published_date": "2025-07-31",
    "retrieved_at": retrieved_at,
    "format": "PDF",
    "crs": "N/A",
    "historical_fit": "valid",
    "analytical_role": "analytical",
    "license_notes": (
        "UNVERIFIED; public City document and general website terms do not "
        "establish reuse and redistribution permission for these exact bytes."
    ),
    "checksum": f"sha256:{checksum}",
    "known_caveats": (
        "Initial project request list predates January 21, 2026 PRB scoring; "
        "project names, scopes, and request values may change by the historical "
        "decision snapshot. Presence in this source does not establish "
        "ClimateCapital analytical or model eligibility."
    ),
    "notes": (
        "Historical source-version evidence for cross-category project and "
        "program names, scopes, and request amounts; January 21 PRB values "
        "remain separately preserved."
    ),
}

for index, row in enumerate(rows):
    if row["source_id"] == JAN_SOURCE_ID:
        rows.insert(index + 1, new_row)
        break
else:
    raise RuntimeError(f"{JAN_SOURCE_ID} is not registered")

with REGISTRY_PATH.open("w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
        lineterminator="\\n",
    )
    writer.writeheader()
    writer.writerows(rows)

print(f"registered source: {SOURCE_ID}")
print(f"saved raw source: {RAW_PATH}")
print(f"checksum: sha256:{checksum}")
print(f"retrieved_at: {retrieved_at}")