#!/usr/bin/env python3
"""Acquire an immutable local snapshot of City of Austin FloodPro FEMA layer 8."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ID = "austin_floodpro_fema_layer_8_live"
SERVICE_URL = "https://maps.austintexas.gov/gis/rest/FloodPro/FloodPro/MapServer"
LAYER_ID = 8
LAYER_URL = f"{SERVICE_URL}/{LAYER_ID}"

STAGING_ROOT = (
    REPO_ROOT
    / "data/staging/raw/city_austin/floodpro/fema_layer_8"
)

MANIFEST_ROOT = (
    REPO_ROOT
    / "data/metadata/source_snapshots"
    / SOURCE_ID
)

BATCH_SIZE = 1000


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")


def snapshot_id(timestamp: str) -> str:
    return (
        timestamp
        .replace("-", "")
        .replace(":", "")
        .replace("+00:00", "Z")
    )


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def request_json(
    url: str,
    params: dict[str, str],
    *,
    method: str = "GET",
) -> tuple[bytes, dict]:
    encoded = urlencode(params).encode()

    if method == "POST":
        request = Request(
            url,
            data=encoded,
            headers={
                "User-Agent": "ClimateCapitalAI/1.0",
                "Content-Type": "application/x-www-form-urlencoded",
            },
        )
    else:
        request = Request(
            f"{url}?{urlencode(params)}",
            headers={"User-Agent": "ClimateCapitalAI/1.0"},
        )

    with urlopen(request, timeout=90) as response:
        raw = response.read()

    payload = json.loads(raw)

    if not isinstance(payload, dict):
        raise RuntimeError(f"Expected JSON object from {url}")

    if "error" in payload:
        raise RuntimeError(f"ArcGIS error from {url}: {payload['error']}")

    return raw, payload


def write_exact(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        raise RuntimeError(
            f"Refusing to overwrite existing snapshot file: {path}"
        )

    with path.open("xb") as handle:
        handle.write(content)


def response_record(filename: str, raw: bytes, retrieved_at: str) -> dict:
    return {
        "filename": filename,
        "byte_size": len(raw),
        "sha256": sha256_bytes(raw),
        "retrieved_at": retrieved_at,
    }


def main() -> None:
    started = utc_now()
    sid = snapshot_id(started)

    staging_dir = STAGING_ROOT / sid
    manifest_dir = MANIFEST_ROOT / sid

    if staging_dir.exists() or manifest_dir.exists():
        raise RuntimeError(f"Snapshot already exists: {sid}")

    inventory: list[dict] = []

    # Service metadata
    retrieved = utc_now()
    service_raw, service = request_json(
        SERVICE_URL,
        {"f": "json"},
    )
    write_exact(staging_dir / "service.json", service_raw)
    inventory.append(
        response_record("service.json", service_raw, retrieved)
    )

    # Layer metadata
    retrieved = utc_now()
    layer_raw, layer = request_json(
        LAYER_URL,
        {"f": "json"},
    )

    if layer.get("name") != "FEMA Floodplain":
        raise RuntimeError(
            f"Unexpected layer name: {layer.get('name')!r}"
        )

    if layer.get("geometryType") != "esriGeometryPolygon":
        raise RuntimeError(
            f"Unexpected geometry type: {layer.get('geometryType')!r}"
        )

    field_names = {
        field.get("name")
        for field in layer.get("fields", [])
        if isinstance(field, dict)
    }

    required_fields = {
        "OBJECTID",
        "FLOOD_ZONE",
        "FLOODWAY",
        "FIRM_PANEL",
        "EFFECTIVE_DATE",
        "COUNTY",
        "UNIQUE_GIS_ID",
        "SHAPE",
    }

    missing_fields = required_fields - field_names
    if missing_fields:
        raise RuntimeError(
            f"Required FEMA fields missing: {sorted(missing_fields)}"
        )

    write_exact(staging_dir / "layer.json", layer_raw)
    inventory.append(
        response_record("layer.json", layer_raw, retrieved)
    )

    # Pre-acquisition object IDs
    retrieved = utc_now()
    ids_pre_raw, ids_pre_payload = request_json(
        f"{LAYER_URL}/query",
        {
            "where": "1=1",
            "returnIdsOnly": "true",
            "f": "json",
        },
        method="POST",
    )

    ids_pre = ids_pre_payload.get("objectIds")
    if not isinstance(ids_pre, list):
        raise RuntimeError("ArcGIS response did not contain objectIds")

    ids_pre = sorted(int(value) for value in ids_pre)

    if len(ids_pre) != len(set(ids_pre)):
        raise RuntimeError("Duplicate FEMA OBJECTIDs returned")

    write_exact(
        staging_dir / "object_ids_pre.json",
        ids_pre_raw,
    )
    inventory.append(
        response_record(
            "object_ids_pre.json",
            ids_pre_raw,
            retrieved,
        )
    )

    # Acquire exact source responses in bounded batches.
    returned_ids: list[int] = []
    total_features = 0

    for batch_number, start in enumerate(
        range(0, len(ids_pre), BATCH_SIZE),
        start=1,
    ):
        batch_ids = ids_pre[start : start + BATCH_SIZE]

        retrieved = utc_now()
        raw, payload = request_json(
            f"{LAYER_URL}/query",
            {
                "objectIds": ",".join(map(str, batch_ids)),
                "outFields": "*",
                "returnGeometry": "true",
                "orderByFields": "OBJECTID ASC",
                "outSR": "102739",
                "f": "json",
            },
            method="POST",
        )

        features = payload.get("features")
        if not isinstance(features, list):
            raise RuntimeError(
                f"Batch {batch_number} missing features"
            )

        for feature in features:
            attributes = feature.get("attributes", {})
            oid = attributes.get("OBJECTID")

            if not isinstance(oid, int):
                raise RuntimeError(
                    f"Invalid OBJECTID in batch {batch_number}: {oid!r}"
                )

            returned_ids.append(oid)

        total_features += len(features)

        filename = f"features_{batch_number:04d}.arcgis.json"
        write_exact(staging_dir / filename, raw)
        inventory.append(
            response_record(filename, raw, retrieved)
        )

    if len(returned_ids) != len(set(returned_ids)):
        raise RuntimeError("Duplicate FEMA features returned")

    if sorted(returned_ids) != ids_pre:
        missing = sorted(set(ids_pre) - set(returned_ids))
        unexpected = sorted(set(returned_ids) - set(ids_pre))

        raise RuntimeError(
            "Feature/object-ID reconciliation failed. "
            f"missing={missing[:20]}, unexpected={unexpected[:20]}"
        )

    # Post-acquisition object IDs
    retrieved = utc_now()
    ids_post_raw, ids_post_payload = request_json(
        f"{LAYER_URL}/query",
        {
            "where": "1=1",
            "returnIdsOnly": "true",
            "f": "json",
        },
        method="POST",
    )

    ids_post = sorted(
        int(value)
        for value in ids_post_payload.get("objectIds", [])
    )

    write_exact(
        staging_dir / "object_ids_post.json",
        ids_post_raw,
    )
    inventory.append(
        response_record(
            "object_ids_post.json",
            ids_post_raw,
            retrieved,
        )
    )

    if ids_pre != ids_post:
        raise RuntimeError(
            "FEMA source mutated during acquisition: "
            "pre/post OBJECTID sets differ"
        )

    spatial_reference = layer.get("extent", {}).get(
        "spatialReference", {}
    )

    manifest = {
        "manifest_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": sid,
        "snapshot_identity": (
            "UTC retrieval timestamp only; "
            "not a historical FEMA effective-date assertion"
        ),
        "canonical_source": {
            "publisher": "City of Austin",
            "dataset_name": "FloodPro - FEMA Floodplain",
            "service_url": SERVICE_URL,
            "layer_url": LAYER_URL,
            "layer_id": 8,
            "layer_name": "FEMA Floodplain",
            "analytical_role": "contextual",
            "historical_fit": "uncertain",
            "license_reuse_status": "UNVERIFIED",
            "license_reuse_basis": (
                "Preserved layer metadata has an empty copyright field and no "
                "explicit reuse or redistribution grant."
            ),
            "historical_limitation": (
                "Live/current service state does not establish "
                "the exact January 2026 layer state."
            ),
        },
        "geometry": {
            "geometry_type": layer.get("geometryType"),
            "source_wkid": spatial_reference.get("wkid"),
            "latest_wkid": spatial_reference.get("latestWkid"),
        },
        "object_id_reconciliation": {
            "pre_count": len(ids_pre),
            "post_count": len(ids_post),
            "returned_feature_count": total_features,
            "sets_equal": ids_pre == ids_post,
            "every_requested_object_id_returned_exactly_once": (
                sorted(returned_ids) == ids_pre
                and len(returned_ids) == len(set(returned_ids))
            ),
        },
        "evidence_semantics": {
            "role": "CONTEXTUAL_EVIDENCE",
            "may_support": [
                "current FEMA hazard context where defensible project geometry exists"
            ],
            "must_not_establish": [
                "eligibility",
                "project priority",
                "expected flood-reduction benefit",
                "people benefiting",
                "structures benefiting",
            ],
        },
        "response_inventory": inventory,
        "retrieval_started_at": started,
        "retrieval_completed_at": utc_now(),
    }

    manifest_dir.mkdir(parents=True, exist_ok=False)

    manifest_path = manifest_dir / "manifest.json"
    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("FEMA SNAPSHOT: PASS")
    print("snapshot_id:", sid)
    print("object_ids:", len(ids_pre))
    print("features:", total_features)
    print("raw_path:", staging_dir)
    print("manifest:", manifest_path)


if __name__ == "__main__":
    main()
