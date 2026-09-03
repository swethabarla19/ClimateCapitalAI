#!/usr/bin/env python3
"""Acquire an immutable local snapshot of Austin Equity Analysis Zones 2021."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[2]

SOURCE_ID = "austin_equity_analysis_zones_2021"
ITEM_ID = "0a095a37ea8a4eb8b835a888f00ef53f"
ITEM_URL = (
    "https://www.arcgis.com/sharing/rest/content/items/"
    f"{ITEM_ID}"
)

STAGING_ROOT = (
    REPO_ROOT
    / "data/staging/raw/city_austin/equity_analysis_zones/2021"
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
    return timestamp.replace("-", "").replace(":", "")


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
        raise RuntimeError(
            f"ArcGIS error from {url}: {payload['error']}"
        )

    return raw, payload


def write_exact(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.exists():
        raise RuntimeError(
            f"Refusing to overwrite snapshot file: {path}"
        )

    with path.open("xb") as handle:
        handle.write(content)


def inventory_record(
    filename: str,
    raw: bytes,
    retrieved_at: str,
) -> dict:
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

    inventory: list[dict] = []

    # Preserve exact ArcGIS item metadata.
    retrieved = utc_now()
    item_raw, item = request_json(
        ITEM_URL,
        {"f": "pjson"},
    )

    if item.get("id") != ITEM_ID:
        raise RuntimeError("Unexpected ArcGIS item identity")

    service_url = item.get("url")

    if not isinstance(service_url, str) or not service_url.startswith(
        "https://"
    ):
        raise RuntimeError(
            f"Unexpected EAZ service URL: {service_url!r}"
        )

    write_exact(staging_dir / "item.json", item_raw)
    inventory.append(
        inventory_record("item.json", item_raw, retrieved)
    )

    # Preserve FeatureServer metadata.
    retrieved = utc_now()
    service_raw, service = request_json(
        service_url,
        {"f": "pjson"},
    )

    write_exact(staging_dir / "service.json", service_raw)
    inventory.append(
        inventory_record("service.json", service_raw, retrieved)
    )

    layer_url = f"{service_url}/0"

    # Preserve and validate layer metadata.
    retrieved = utc_now()
    layer_raw, layer = request_json(
        layer_url,
        {"f": "pjson"},
    )

    if layer.get("name") != "Equity Analysis Zones Version 1_2021":
        raise RuntimeError(
            f"Unexpected EAZ layer name: {layer.get('name')!r}"
        )

    if layer.get("geometryType") != "esriGeometryPolygon":
        raise RuntimeError(
            f"Unexpected geometry type: {layer.get('geometryType')!r}"
        )

    if layer.get("objectIdField") != "FID":
        raise RuntimeError(
            f"Unexpected object ID field: {layer.get('objectIdField')!r}"
        )

    field_names = {
        f.get("name")
        for f in layer.get("fields", [])
        if isinstance(f, dict)
    }

    required_fields = {
        "FID",
        "GEOID",
        "NAME",
        "indxd_v",
        "EAZ_Type",
    }

    missing = required_fields - field_names

    if missing:
        raise RuntimeError(
            f"Required EAZ fields missing: {sorted(missing)}"
        )

    write_exact(staging_dir / "layer.json", layer_raw)
    inventory.append(
        inventory_record("layer.json", layer_raw, retrieved)
    )

    query_url = f"{layer_url}/query"

    # Pre-acquisition ID inventory.
    retrieved = utc_now()
    pre_raw, pre_payload = request_json(
        query_url,
        {
            "where": "1=1",
            "returnIdsOnly": "true",
            "f": "json",
        },
        method="POST",
    )

    ids_pre = sorted(
        int(v)
        for v in pre_payload.get("objectIds", [])
    )

    if not ids_pre:
        raise RuntimeError("EAZ source returned no object IDs")

    if len(ids_pre) != len(set(ids_pre)):
        raise RuntimeError("Duplicate EAZ object IDs")

    write_exact(staging_dir / "object_ids_pre.json", pre_raw)
    inventory.append(
        inventory_record(
            "object_ids_pre.json",
            pre_raw,
            retrieved,
        )
    )

    returned_ids: list[int] = []

    # Acquire exact feature response bytes.
    for batch_number, start in enumerate(
        range(0, len(ids_pre), BATCH_SIZE),
        start=1,
    ):
        batch_ids = ids_pre[start:start + BATCH_SIZE]

        retrieved = utc_now()
        raw, payload = request_json(
            query_url,
            {
                "objectIds": ",".join(map(str, batch_ids)),
                "outFields": "*",
                "returnGeometry": "true",
                "orderByFields": "FID ASC",
                "f": "json",
            },
            method="POST",
        )

        features = payload.get("features")

        if not isinstance(features, list):
            raise RuntimeError(
                f"EAZ batch {batch_number} missing features"
            )

        for feature in features:
            attributes = feature.get("attributes", {})
            oid = attributes.get("FID")

            if not isinstance(oid, int):
                raise RuntimeError(
                    f"Invalid EAZ FID: {oid!r}"
                )

            returned_ids.append(oid)

        filename = f"features_{batch_number:04d}.arcgis.json"

        write_exact(staging_dir / filename, raw)
        inventory.append(
            inventory_record(filename, raw, retrieved)
        )

    if sorted(returned_ids) != ids_pre:
        raise RuntimeError(
            "EAZ feature/object-ID reconciliation failed"
        )

    if len(returned_ids) != len(set(returned_ids)):
        raise RuntimeError(
            "Duplicate EAZ features returned"
        )

    # Post-acquisition mutation check.
    retrieved = utc_now()
    post_raw, post_payload = request_json(
        query_url,
        {
            "where": "1=1",
            "returnIdsOnly": "true",
            "f": "json",
        },
        method="POST",
    )

    ids_post = sorted(
        int(v)
        for v in post_payload.get("objectIds", [])
    )

    write_exact(staging_dir / "object_ids_post.json", post_raw)
    inventory.append(
        inventory_record(
            "object_ids_post.json",
            post_raw,
            retrieved,
        )
    )

    if ids_pre != ids_post:
        raise RuntimeError(
            "EAZ source mutated during acquisition"
        )

    manifest = {
        "manifest_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": sid,
        "snapshot_identity": (
            "Controlled retrieval of the locked EAZ 2021 ArcGIS item; "
            "retrieval time is not the data vintage."
        ),
        "canonical_source": {
            "publisher": "City of Austin",
            "arcgis_item_id": ITEM_ID,
            "item_url": ITEM_URL,
            "service_url": service_url,
            "layer_url": layer_url,
            "layer_id": 0,
            "layer_name": layer.get("name"),
            "source_vintage": "2021",
            "analytical_role": "contextual",
            "historical_fit": "valid_as_dated_2021_snapshot",
            "license_info": item.get("licenseInfo"),
            "license_reuse_status": "UNVERIFIED",
            "license_reuse_basis": (
                "Preserved item licenseInfo/accessInformation and layer "
                "copyrightText fields are empty."
            ),
        },
        "object_id_reconciliation": {
            "pre_count": len(ids_pre),
            "post_count": len(ids_post),
            "returned_feature_count": len(returned_ids),
            "sets_equal": ids_pre == ids_post,
            "every_requested_object_id_returned_exactly_once": (
                sorted(returned_ids) == ids_pre
                and len(returned_ids) == len(set(returned_ids))
            ),
        },
        "fields_required_for_p0": [
            "FID",
            "GEOID",
            "NAME",
            "indxd_v",
            "EAZ_Type",
        ],
        "evidence_semantics": {
            "role": "CONTEXTUAL_EVIDENCE",
            "may_support": [
                "dated EAZ 2021 location context where defensible project geography exists"
            ],
            "must_not_establish": [
                "Watershed-specific equity methodology",
                "beneficiaries",
                "eligibility",
                "Funding Plan membership",
                "project priority",
            ],
        },
        "limitations": [
            "EAZ 2021 is a dated Austin Transportation vulnerability framework.",
            "It uses historical ACS-based inputs and is not evergreen.",
            "Project-level EAZ context requires defensible project geography.",
            "Missing project geography must remain explicit and must not be imputed.",
        ],
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
        ) + "\n",
        encoding="utf-8",
    )

    print("EAZ SNAPSHOT: PASS")
    print("snapshot_id:", sid)
    print("object_ids:", len(ids_pre))
    print("features:", len(returned_ids))
    print("service_url:", service_url)
    print("raw_path:", staging_dir)
    print("manifest:", manifest_path)


if __name__ == "__main__":
    main()
