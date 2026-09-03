#!/usr/bin/env python3
"""Pin the approved documentary Problem Score inputs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]

SOURCES = {
    "edims_261630.pdf":
        "https://services.austintexas.gov/edims/document.cfm?id=261630",
    "edims_404946.pdf":
        "https://services.austintexas.gov/edims/document.cfm?id=404946",
    "fy26_budget_response_2050cddcca.pdf":
        "https://services.austintexas.gov/budget/cbq/index.cfm?"
        "FILE_ID=2050CDDCCA&action=pushFile&popup=true",
}

SOURCE_ID = "austin_wpd_problem_score_documentary_context"

RAW_ROOT = (
    ROOT / "data/staging/raw/city_austin/problem_score"
)

MANIFEST_ROOT = (
    ROOT / "data/metadata/source_snapshots" / SOURCE_ID
)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")


def sid(ts: str) -> str:
    return ts.replace("-", "").replace(":", "")


def sha(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def main() -> None:
    started = now()
    snapshot = sid(started)

    raw_dir = RAW_ROOT / snapshot
    manifest_dir = MANIFEST_ROOT / snapshot

    records = []

    for filename, url in SOURCES.items():
        request = Request(
            url,
            headers={"User-Agent": "ClimateCapitalAI/1.0"},
        )

        with urlopen(request, timeout=90) as response:
            body = response.read()
            status = response.status
            final_url = response.url
            content_type = response.headers.get("Content-Type", "")

        if status != 200:
            raise RuntimeError(f"{filename}: HTTP {status}")

        if not body.startswith(b"%PDF"):
            raise RuntimeError(f"{filename}: response is not a PDF")

        path = raw_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("xb") as f:
            f.write(body)

        records.append({
            "filename": filename,
            "source_url": url,
            "final_url": final_url,
            "http_status": status,
            "content_type": content_type,
            "byte_size": len(body),
            "sha256": sha(body),
        })

    manifest = {
        "manifest_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": snapshot,
        "analytical_role": "contextual",
        "evidence_role": "CONTEXTUAL_EVIDENCE",
        "historical_fit": "valid_as_documentary_context_only",
        "historical_limitation": (
            "The preserved documents do not support a reproducible January 2026 "
            "Local Flood numeric severity across the active family."
        ),
        "license_reuse_status": "UNVERIFIED",
        "license_reuse_basis": (
            "Public document availability and general City website terms do not "
            "establish redistribution permission for these exact PDFs."
        ),
        "problem_score_treatment": (
            "Documented project/problem associations and provenance "
            "context only; association strength is not severity."
        ),
        "must_not_establish": [
            "numeric Local Flood severity",
            "Funding Priority",
            "eligibility",
            "expected flood-reduction benefit",
            "beneficiaries",
        ],
        "problem_score_viewer_reference": {
            "arcgis_item_id": "d45481abb0804c95a8e6b033188982b9",
            "role": "provenance reference only",
            "numeric_reproduction_supported": False,
        },
        "documents": records,
        "retrieval_started_at": started,
        "retrieval_completed_at": now(),
    }

    manifest_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    print("PROBLEM SCORE SNAPSHOT: PASS")
    print("snapshot_id:", snapshot)

    for record in records:
        print(
            record["filename"],
            record["byte_size"],
            record["sha256"],
        )

    print("manifest:", manifest_path)


if __name__ == "__main__":
    main()
