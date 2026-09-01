#!/usr/bin/env python3
"""Acquire and preserve one immutable Austin RNA Projects layer-8 snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Callable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.data.fetch_sources import update_registry, write_snapshot


SOURCE_ID = "austin_rna_projects_layer_8_live"
MAPSERVER_URL = (
    "https://maps.austintexas.gov/arcgis/rest/services/LongRangeCIP/"
    "RNAProjects/MapServer"
)
LAYER_ID = 8
LAYER_NAME = "RNA Projects"
LAYER_URL = f"{MAPSERVER_URL}/{LAYER_ID}"
QUERY_URL = f"{LAYER_URL}/query"
SOURCE_WKID = 102739
LATEST_WKID = 2277

DEFAULT_REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
DEFAULT_STAGING_ROOT = REPOSITORY_ROOT / "data" / "staging"
DEFAULT_MANIFEST_ROOT = (
    REPOSITORY_ROOT / "data" / "metadata" / "source_snapshots" / SOURCE_ID
)

SNAPSHOT_ID_PATTERN = re.compile(r"^\d{8}T\d{6}Z$")
SHA256_PATTERN = re.compile(r"^sha256:[0-9a-f]{64}$")
GCS_BUCKET_PATTERN = re.compile(r"^gs://[a-z0-9._-]+/?$")

EXPECTED_FIELDS = (
    ("OBJECTID", "esriFieldTypeOID"),
    ("LRCSP_ROLLING_NEEDS_ID", "esriFieldTypeInteger"),
    ("SUB_PROJECT_ID", "esriFieldTypeDouble"),
    ("SUB_PROJECT_NAME", "esriFieldTypeString"),
    ("SUB_PROJECT_STATUS", "esriFieldTypeString"),
    ("SUB_PROJECT_PHASE", "esriFieldTypeString"),
    ("SUB_PROJECT_TYPE_CATEGORY", "esriFieldTypeString"),
    ("DESCRIPTION", "esriFieldTypeString"),
    ("CONTACT", "esriFieldTypeString"),
    ("DEPARTMENT", "esriFieldTypeString"),
    ("SHAPE", "esriFieldTypeGeometry"),
)
EXPECTED_ATTRIBUTE_FIELDS = tuple(name for name, _ in EXPECTED_FIELDS if name != "SHAPE")


class GisAcquisitionError(RuntimeError):
    """Raised when a source-faithful GIS snapshot cannot be established."""


class SourceMutationError(GisAcquisitionError):
    """Raised for observable live-service mutation during an acquisition attempt."""


class UnsafeGisIdentifierError(GisAcquisitionError):
    """Raised when a numeric GIS ID cannot enter the governed three-decimal domain."""


class CloudPreservationError(GisAcquisitionError):
    """Raised when create-only GCS preservation or byte verification fails."""


class JsonNumber(str):
    """Exact JSON numeric token retained without binary-float conversion."""


@dataclass(frozen=True)
class HttpResponse:
    body: bytes
    status: int
    final_url: str
    media_type: str


@dataclass(frozen=True)
class LayerContract:
    fields: tuple[tuple[str, str], ...]
    geometry_type: str
    wkid: int
    latest_wkid: int
    max_record_count: int


@dataclass(frozen=True)
class FeatureAudit:
    feature_count: int
    geometry_present_count: int
    geometry_missing_count: int
    rings_count: int
    true_curve_count: int
    safe_numeric_id_count: int
    unsafe_numeric_ids: tuple[dict[str, object], ...]
    unique_canonical_id_count: int
    duplicate_canonical_ids: dict[str, int]
    fractional_digit_widths: dict[str, int]
    semantic_checksum: str


@dataclass(frozen=True)
class AcquisitionResult:
    snapshot_id: str
    retrieval_started_at: str
    raw_directory: Path
    manifest_path: Path
    features_checksum: str
    feature_audit: FeatureAudit
    review_required: bool


@dataclass(frozen=True)
class MatchableFeatureSnapshot:
    parsed_response: dict[str, object]
    object_ids: tuple[int, ...]
    audit: FeatureAudit


Transport = Callable[[str, str, Sequence[tuple[str, str]], float], HttpResponse]
Clock = Callable[[], str]
CommandRunner = Callable[[Sequence[str]], subprocess.CompletedProcess[bytes]]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def snapshot_id_from_timestamp(timestamp: str) -> str:
    try:
        parsed = datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise GisAcquisitionError(f"Invalid UTC acquisition timestamp {timestamp!r}.") from error
    if not timestamp.endswith("Z") or parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise GisAcquisitionError(f"Acquisition timestamp must be UTC and end in Z: {timestamp!r}.")
    return parsed.strftime("%Y%m%dT%H%M%SZ")


def sha256_bytes(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def _normalize_decimal_token(token: str) -> str:
    value = Decimal(token)
    if not value.is_finite():
        raise InvalidOperation
    rendered = format(value, "f")
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return "0" if rendered in {"-0", ""} else rendered


def parse_arcgis_json(content: bytes, context: str) -> dict[str, object]:
    """Parse UTF-8 ArcGIS JSON while retaining every numeric token exactly."""

    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError as error:
        raise GisAcquisitionError(f"{context} is not valid UTF-8 JSON.") from error
    try:
        parsed = json.loads(decoded, parse_float=JsonNumber, parse_int=JsonNumber)
    except json.JSONDecodeError as error:
        raise GisAcquisitionError(f"{context} is not valid JSON: {error}.") from error
    if not isinstance(parsed, dict):
        raise GisAcquisitionError(f"{context} must be a JSON object.")
    if "error" in parsed:
        raise GisAcquisitionError(f"{context} contains an ArcGIS error: {parsed['error']!r}.")
    return parsed


def _exact_int(value: object, context: str) -> int:
    if not isinstance(value, (JsonNumber, int)) or isinstance(value, bool):
        raise GisAcquisitionError(f"{context} must be an integer JSON number; got {value!r}.")
    try:
        decimal_value = Decimal(str(value))
    except InvalidOperation as error:
        raise GisAcquisitionError(f"{context} is not a valid integer: {value!r}.") from error
    if not decimal_value.is_finite() or decimal_value != decimal_value.to_integral_value():
        raise GisAcquisitionError(f"{context} must be an exact integer; got {value!r}.")
    return int(decimal_value)


def canonicalize_gis_id(value: object) -> tuple[str, str]:
    """Return the exact raw token and zero-padded three-decimal representation."""

    if not isinstance(value, (JsonNumber, int)) or isinstance(value, bool):
        raise UnsafeGisIdentifierError(f"GIS SUB_PROJECT_ID is not numeric: {value!r}.")
    raw_token = str(value)
    try:
        decimal_value = Decimal(raw_token)
    except InvalidOperation as error:
        raise UnsafeGisIdentifierError(
            f"GIS SUB_PROJECT_ID token is invalid: {raw_token!r}."
        ) from error
    if not decimal_value.is_finite() or decimal_value < 0:
        raise UnsafeGisIdentifierError(
            f"GIS SUB_PROJECT_ID must be finite and nonnegative: {raw_token!r}."
        )
    scaled = decimal_value * Decimal(1000)
    if scaled != scaled.to_integral_value():
        raise UnsafeGisIdentifierError(
            "GIS SUB_PROJECT_ID has meaningful precision beyond three decimals and "
            f"would require rounding: {raw_token!r}."
        )
    scaled_integer = int(scaled)
    canonical = f"{scaled_integer // 1000}.{scaled_integer % 1000:03d}"
    if Decimal(canonical) != decimal_value:
        raise UnsafeGisIdentifierError(
            f"GIS SUB_PROJECT_ID cannot be represented losslessly: {raw_token!r}."
        )
    return raw_token, canonical


def _json_number_width(token: str) -> str:
    if "e" in token.lower():
        return "scientific"
    return str(len(token.partition(".")[2]))


def request_https_json(
    method: str,
    url: str,
    parameters: Sequence[tuple[str, str]],
    timeout: float,
) -> HttpResponse:
    if urlsplit(url).scheme.lower() != "https":
        raise GisAcquisitionError(f"Refusing non-HTTPS GIS URL: {url!r}.")
    encoded = urlencode(parameters).encode("ascii")
    request_url = url
    body: bytes | None = None
    headers = {"User-Agent": "ClimateCapitalAI-data-reconnaissance/1.0"}
    if method == "GET":
        request_url = f"{url}?{encoded.decode('ascii')}"
    elif method == "POST":
        body = encoded
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    else:
        raise GisAcquisitionError(f"Unsupported HTTP method {method!r}.")
    try:
        with urlopen(Request(request_url, data=body, headers=headers, method=method), timeout=timeout) as response:
            status = response.getcode()
            final_url = response.geturl()
            content = response.read()
            media_type = response.headers.get_content_type()
    except HTTPError as error:
        raise GisAcquisitionError(
            f"ArcGIS request failed: HTTP {error.code} {error.reason} for {url}."
        ) from error
    except (URLError, TimeoutError, OSError) as error:
        raise GisAcquisitionError(f"ArcGIS request failed for {url}: {error}.") from error
    if status is None or not 200 <= status < 300:
        raise GisAcquisitionError(f"ArcGIS request returned unexpected status {status} for {url}.")
    if urlsplit(final_url).scheme.lower() != "https":
        raise GisAcquisitionError(f"ArcGIS request downgraded from HTTPS: {final_url!r}.")
    if not content:
        raise GisAcquisitionError(f"ArcGIS request returned no bytes for {url}.")
    return HttpResponse(content, status, final_url, media_type)


def validate_service_metadata(service: Mapping[str, object]) -> None:
    layers = service.get("layers")
    if not isinstance(layers, list):
        raise GisAcquisitionError("Service metadata contains no layer inventory.")
    candidates = [
        layer
        for layer in layers
        if isinstance(layer, dict)
        and _exact_int(layer.get("id"), "service layer id") == LAYER_ID
    ]
    if len(candidates) != 1 or candidates[0].get("name") != LAYER_NAME:
        raise GisAcquisitionError(
            f"Service metadata does not identify exactly one layer {LAYER_ID} named {LAYER_NAME!r}."
        )


def validate_layer_metadata(layer: Mapping[str, object]) -> LayerContract:
    if _exact_int(layer.get("id"), "layer id") != LAYER_ID or layer.get("name") != LAYER_NAME:
        raise GisAcquisitionError("Layer metadata identity differs from canonical layer 8.")
    if layer.get("geometryType") != "esriGeometryPolygon":
        raise GisAcquisitionError(
            f"Layer geometry type changed: {layer.get('geometryType')!r}."
        )
    fields = layer.get("fields")
    if not isinstance(fields, list):
        raise GisAcquisitionError("Layer metadata contains no fields.")
    field_contract = tuple(
        (str(field.get("name")), str(field.get("type")))
        for field in fields
        if isinstance(field, dict)
    )
    if field_contract != EXPECTED_FIELDS:
        raise GisAcquisitionError(
            f"Layer schema changed: expected {EXPECTED_FIELDS!r}; found {field_contract!r}."
        )
    spatial_reference = layer.get("sourceSpatialReference")
    if not isinstance(spatial_reference, dict):
        raise GisAcquisitionError("Layer metadata lacks sourceSpatialReference.")
    wkid = _exact_int(spatial_reference.get("wkid"), "source WKID")
    latest_wkid = _exact_int(spatial_reference.get("latestWkid"), "latest WKID")
    if (wkid, latest_wkid) != (SOURCE_WKID, LATEST_WKID):
        raise GisAcquisitionError(
            f"Layer CRS changed: expected {(SOURCE_WKID, LATEST_WKID)}; found {(wkid, latest_wkid)}."
        )
    capabilities = set(str(layer.get("capabilities", "")).split(","))
    if not {"Query", "Data"}.issubset(capabilities):
        raise GisAcquisitionError(f"Layer lacks required Query/Data capabilities: {capabilities!r}.")
    max_record_count = _exact_int(layer.get("maxRecordCount"), "maxRecordCount")
    return LayerContract(
        fields=field_contract,
        geometry_type="esriGeometryPolygon",
        wkid=wkid,
        latest_wkid=latest_wkid,
        max_record_count=max_record_count,
    )


def parse_object_ids(payload: Mapping[str, object], context: str) -> tuple[int, ...]:
    if payload.get("objectIdFieldName") != "OBJECTID":
        raise GisAcquisitionError(
            f"{context} did not identify OBJECTID as the object-ID field."
        )
    values = payload.get("objectIds")
    if not isinstance(values, list) or not values:
        raise GisAcquisitionError(f"{context} returned no object-ID set.")
    object_ids = tuple(sorted(_exact_int(value, f"{context} OBJECTID") for value in values))
    if len(object_ids) != len(set(object_ids)):
        raise GisAcquisitionError(f"{context} returned duplicate OBJECTIDs.")
    return object_ids


def object_id_set_checksum(object_ids: Sequence[int]) -> str:
    return sha256_bytes((",".join(str(value) for value in object_ids) + "\n").encode("ascii"))


def _semantic_number(value: JsonNumber) -> dict[str, str]:
    try:
        normalized = _normalize_decimal_token(str(value))
    except InvalidOperation as error:
        raise GisAcquisitionError(f"Invalid JSON numeric token {value!r}.") from error
    return {"$number": normalized}


def _semantic_value(value: object) -> object:
    if isinstance(value, JsonNumber):
        return _semantic_number(value)
    if isinstance(value, dict):
        return {str(key): _semantic_value(item) for key, item in sorted(value.items())}
    if isinstance(value, list):
        return [_semantic_value(item) for item in value]
    return value


def semantic_feature_checksum(features: Sequence[Mapping[str, object]]) -> str:
    ordered = sorted(
        features,
        key=lambda feature: _exact_int(
            feature.get("attributes", {}).get("OBJECTID")
            if isinstance(feature.get("attributes"), dict)
            else None,
            "feature OBJECTID",
        ),
    )
    semantic = [
        {
            "attributes": _semantic_value(feature.get("attributes")),
            "geometry": _semantic_value(feature.get("geometry")),
        }
        for feature in ordered
    ]
    encoded = json.dumps(
        semantic,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(encoded)


def validate_feature_response(
    content: bytes,
    frozen_object_ids: Sequence[int],
    contract: LayerContract,
) -> MatchableFeatureSnapshot:
    payload = parse_arcgis_json(content, "Layer-8 feature response")
    if payload.get("exceededTransferLimit") is True:
        raise GisAcquisitionError(
            "Layer-8 feature response indicates exceededTransferLimit; snapshot is incomplete."
        )
    spatial_reference = payload.get("spatialReference")
    if not isinstance(spatial_reference, dict):
        raise GisAcquisitionError("Feature response lacks spatialReference.")
    response_crs = (
        _exact_int(spatial_reference.get("wkid"), "feature-response WKID"),
        _exact_int(spatial_reference.get("latestWkid"), "feature-response latest WKID"),
    )
    if response_crs != (contract.wkid, contract.latest_wkid):
        raise GisAcquisitionError(
            f"Feature-response CRS differs from layer metadata: {response_crs!r}."
        )
    fields = payload.get("fields")
    if not isinstance(fields, list):
        raise GisAcquisitionError("Feature response contains no field schema.")
    response_fields = tuple(
        str(field.get("name")) for field in fields if isinstance(field, dict)
    )
    if response_fields != EXPECTED_ATTRIBUTE_FIELDS:
        raise GisAcquisitionError(
            "Feature-response field order differs from the expected attribute schema: "
            f"{response_fields!r}."
        )
    features = payload.get("features")
    if not isinstance(features, list):
        raise GisAcquisitionError("Feature response contains no feature list.")

    returned_ids: list[int] = []
    canonical_ids: list[str] = []
    unsafe: list[dict[str, object]] = []
    fractional_widths: Counter[str] = Counter()
    geometry_present = 0
    rings_count = 0
    curve_count = 0

    for feature in features:
        if not isinstance(feature, dict) or not isinstance(feature.get("attributes"), dict):
            raise GisAcquisitionError("Feature response contains a malformed feature.")
        attributes = feature["attributes"]
        missing_attributes = [name for name in EXPECTED_ATTRIBUTE_FIELDS if name not in attributes]
        if missing_attributes:
            raise GisAcquisitionError(
                "Feature response is missing required attributes: " + ", ".join(missing_attributes)
            )
        object_id = _exact_int(attributes["OBJECTID"], "feature OBJECTID")
        returned_ids.append(object_id)
        try:
            raw_token, canonical = canonicalize_gis_id(attributes["SUB_PROJECT_ID"])
        except UnsafeGisIdentifierError as error:
            unsafe.append(
                {
                    "object_id": object_id,
                    "raw_token": str(attributes["SUB_PROJECT_ID"]),
                    "reason": str(error),
                }
            )
        else:
            canonical_ids.append(canonical)
            fractional_widths[_json_number_width(raw_token)] += 1

        geometry = feature.get("geometry")
        if isinstance(geometry, dict):
            rings = geometry.get("rings")
            curve_rings = geometry.get("curveRings")
            has_rings = isinstance(rings, list) and bool(rings)
            has_curve_rings = isinstance(curve_rings, list) and bool(curve_rings)
            if has_rings or has_curve_rings:
                geometry_present += 1
            if has_rings:
                rings_count += 1
            if has_curve_rings:
                curve_count += 1

    frozen = tuple(sorted(frozen_object_ids))
    returned = tuple(sorted(returned_ids))
    if len(returned_ids) != len(set(returned_ids)):
        raise SourceMutationError("Feature response returned one or more OBJECTIDs multiple times.")
    if returned != frozen:
        missing = sorted(set(frozen) - set(returned))
        unexpected = sorted(set(returned) - set(frozen))
        raise SourceMutationError(
            "Feature response does not match the frozen OBJECTID set: "
            f"missing={missing!r}; unexpected={unexpected!r}."
        )

    duplicate_ids = {
        key: count for key, count in sorted(Counter(canonical_ids).items()) if count > 1
    }
    audit = FeatureAudit(
        feature_count=len(features),
        geometry_present_count=geometry_present,
        geometry_missing_count=len(features) - geometry_present,
        rings_count=rings_count,
        true_curve_count=curve_count,
        safe_numeric_id_count=len(canonical_ids),
        unsafe_numeric_ids=tuple(unsafe),
        unique_canonical_id_count=len(set(canonical_ids)),
        duplicate_canonical_ids=duplicate_ids,
        fractional_digit_widths=dict(sorted(fractional_widths.items())),
        semantic_checksum=semantic_feature_checksum(features),
    )
    return MatchableFeatureSnapshot(payload, returned, audit)


def _response_record(
    filename: str,
    method: str,
    url: str,
    parameters: Sequence[tuple[str, str]],
    response: HttpResponse,
    retrieved_at: str,
) -> dict[str, object]:
    return {
        "filename": filename,
        "request": {
            "method": method,
            "url": url,
            "parameters": [{"name": name, "value": value} for name, value in parameters],
        },
        "retrieved_at": retrieved_at,
        "http_status": response.status,
        "final_url": response.final_url,
        "media_type": response.media_type,
        "byte_size": len(response.body),
        "sha256": sha256_bytes(response.body),
    }


def _write_json_immutable(path: Path, value: Mapping[str, object]) -> str:
    content = (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")
    return write_snapshot(path, content)


def acquire_snapshot(
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    staging_root: Path = DEFAULT_STAGING_ROOT,
    manifest_root: Path = DEFAULT_MANIFEST_ROOT,
    timeout: float = 60.0,
    max_attempts: int = 3,
    transport: Transport = request_https_json,
    clock: Clock = utc_timestamp,
) -> AcquisitionResult:
    """Acquire one consistent layer-8 snapshot and update its registry checksum."""

    if max_attempts < 1 or max_attempts > 5:
        raise GisAcquisitionError("max_attempts must be between 1 and 5.")
    last_mutation: SourceMutationError | None = None

    for attempt in range(1, max_attempts + 1):
        started_at = clock()
        snapshot_id = snapshot_id_from_timestamp(started_at)
        records: list[dict[str, object]] = []

        def retrieve(
            filename: str,
            method: str,
            url: str,
            parameters: Sequence[tuple[str, str]],
        ) -> HttpResponse:
            response = transport(method, url, parameters, timeout)
            records.append(
                _response_record(filename, method, url, parameters, response, clock())
            )
            return response

        try:
            service_parameters = (("f", "json"),)
            service_response = retrieve("service.json", "GET", MAPSERVER_URL, service_parameters)
            service = parse_arcgis_json(service_response.body, "Service metadata")
            validate_service_metadata(service)

            layer_parameters = (("f", "json"),)
            layer_response = retrieve("layer.json", "GET", LAYER_URL, layer_parameters)
            layer = parse_arcgis_json(layer_response.body, "Layer-8 metadata")
            contract = validate_layer_metadata(layer)

            object_id_parameters = (
                ("where", "1=1"),
                ("returnIdsOnly", "true"),
                ("f", "json"),
            )
            pre_response = retrieve(
                "object_ids_pre.json", "POST", QUERY_URL, object_id_parameters
            )
            pre_ids = parse_object_ids(
                parse_arcgis_json(pre_response.body, "Pre-acquisition OBJECTID response"),
                "Pre-acquisition OBJECTID response",
            )
            if len(pre_ids) > contract.max_record_count:
                raise GisAcquisitionError(
                    f"Frozen feature count {len(pre_ids)} exceeds maxRecordCount "
                    f"{contract.max_record_count}; deterministic batching is not implemented."
                )

            feature_parameters = (
                ("where", "1=1"),
                ("objectIds", ",".join(str(value) for value in pre_ids)),
                ("outFields", "*"),
                ("returnGeometry", "true"),
                ("orderByFields", "OBJECTID ASC"),
                ("outSR", str(SOURCE_WKID)),
                ("returnZ", "true"),
                ("returnM", "true"),
                ("returnTrueCurves", "true"),
                ("f", "json"),
            )
            feature_response = retrieve(
                "features.arcgis.json", "POST", QUERY_URL, feature_parameters
            )
            feature_snapshot = validate_feature_response(
                feature_response.body, pre_ids, contract
            )

            post_response = retrieve(
                "object_ids_post.json", "POST", QUERY_URL, object_id_parameters
            )
            post_ids = parse_object_ids(
                parse_arcgis_json(post_response.body, "Post-acquisition OBJECTID response"),
                "Post-acquisition OBJECTID response",
            )
            if pre_ids != post_ids:
                raise SourceMutationError(
                    "Pre- and post-acquisition OBJECTID sets differ; retrying the complete snapshot."
                )
        except SourceMutationError as error:
            last_mutation = error
            if attempt < max_attempts:
                continue
            raise GisAcquisitionError(
                f"Live layer changed during {max_attempts} acquisition attempts: {error}"
            ) from error

        raw_directory = (
            staging_root / "raw" / "city_austin" / "rna_projects" / "layer_8" / snapshot_id
        )
        response_by_name = {
            "service.json": service_response.body,
            "layer.json": layer_response.body,
            "object_ids_pre.json": pre_response.body,
            "features.arcgis.json": feature_response.body,
            "object_ids_post.json": post_response.body,
        }
        for filename, content in response_by_name.items():
            write_snapshot(raw_directory / filename, content)

        audit = feature_snapshot.audit
        review_reasons: list[str] = []
        if audit.unsafe_numeric_ids:
            review_reasons.append("one or more SUB_PROJECT_ID values are not losslessly canonicalizable")
        if audit.true_curve_count:
            review_reasons.append("one or more true-curve geometries require review before derivation")

        manifest: dict[str, object] = {
            "manifest_version": 1,
            "source_id": SOURCE_ID,
            "snapshot_id": snapshot_id,
            "snapshot_identity": "UTC retrieval timestamp only; not a source vintage",
            "retrieval_started_at": started_at,
            "retrieval_completed_at": clock(),
            "canonical_source": {
                "service_url": MAPSERVER_URL,
                "layer_url": LAYER_URL,
                "layer_id": LAYER_ID,
                "layer_name": LAYER_NAME,
                "selection_basis": (
                    "Layer 8 is the live RNA master superset and avoids duplicate "
                    "category-layer representations; category layers were not acquired."
                ),
                "historical_fit": "uncertain",
                "analytical_role": "research-only",
                "historical_limitation": (
                    "This live/current City GIS snapshot does not establish January 2026 geometry."
                ),
            },
            "response_inventory": records,
            "snapshot_inventory": sorted(response_by_name),
            "object_id_reconciliation": {
                "pre_count": len(pre_ids),
                "post_count": len(post_ids),
                "returned_feature_count": audit.feature_count,
                "pre_sha256": object_id_set_checksum(pre_ids),
                "post_sha256": object_id_set_checksum(post_ids),
                "sets_equal": pre_ids == post_ids == feature_snapshot.object_ids,
                "every_requested_object_id_returned_exactly_once": True,
                "unexpected_object_ids": [],
                "exceeded_transfer_limit": False,
                "attempt": attempt,
                "max_attempts": max_attempts,
                "second_complete_feature_retrieval_performed": False,
            },
            "schema": [
                {"name": name, "arcgis_type": field_type}
                for name, field_type in contract.fields
            ],
            "geometry": {
                "geometry_type": contract.geometry_type,
                "source_wkid": contract.wkid,
                "latest_wkid": contract.latest_wkid,
                "request": {
                    "returnGeometry": True,
                    "outSR": SOURCE_WKID,
                    "returnZ": True,
                    "returnM": True,
                    "returnTrueCurves": True,
                    "geometryPrecision": "not specified",
                    "maxAllowableOffset": "not specified",
                    "quantization": "not requested",
                },
                "present_count": audit.geometry_present_count,
                "missing_count": audit.geometry_missing_count,
                "rings_count": audit.rings_count,
                "true_curve_count": audit.true_curve_count,
            },
            "numeric_id_audit": {
                "parser": "exact JSON numeric tokens; no binary-float conversion",
                "canonicalization": "exact three-decimal representation by zero-padding only",
                "feature_count": audit.feature_count,
                "safe_count": audit.safe_numeric_id_count,
                "unsafe_values": list(audit.unsafe_numeric_ids),
                "unique_canonical_id_count": audit.unique_canonical_id_count,
                "duplicate_canonical_ids": audit.duplicate_canonical_ids,
                "fractional_digit_widths": audit.fractional_digit_widths,
            },
            "semantic_fingerprint": {
                "algorithm": "sha256",
                "scope": "all feature attributes and native geometry, sorted by OBJECTID",
                "value": audit.semantic_checksum,
            },
            "review_required": bool(review_reasons),
            "review_reasons": review_reasons,
        }
        manifest_path = manifest_root / snapshot_id / "manifest.json"
        _write_json_immutable(manifest_path, manifest)

        if not review_reasons:
            update_registry(
                registry_path,
                SOURCE_ID,
                started_at,
                sha256_bytes(feature_response.body),
            )

        return AcquisitionResult(
            snapshot_id=snapshot_id,
            retrieval_started_at=started_at,
            raw_directory=raw_directory,
            manifest_path=manifest_path,
            features_checksum=sha256_bytes(feature_response.body),
            feature_audit=audit,
            review_required=bool(review_reasons),
        )

    raise GisAcquisitionError(f"Snapshot acquisition failed: {last_mutation}")


def _run_command(arguments: Sequence[str]) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


def build_gcloud_copy_command(local_path: Path, destination: str) -> list[str]:
    return [
        "gcloud",
        "storage",
        "cp",
        "--if-generation-match=0",
        "--content-type=application/json",
        str(local_path),
        destination,
    ]


def verify_cloud_bytes(local_content: bytes, cloud_content: bytes, object_uri: str) -> str:
    local_checksum = sha256_bytes(local_content)
    cloud_checksum = sha256_bytes(cloud_content)
    if len(local_content) != len(cloud_content) or local_checksum != cloud_checksum:
        raise CloudPreservationError(
            f"Cloud bytes differ for {object_uri}: local {len(local_content)} bytes "
            f"{local_checksum}; cloud {len(cloud_content)} bytes {cloud_checksum}."
        )
    return cloud_checksum


def _command_error(result: subprocess.CompletedProcess[bytes]) -> str:
    return result.stderr.decode("utf-8", errors="replace").strip()


def _describe_object(
    object_uri: str, runner: CommandRunner
) -> tuple[dict[str, object] | None, str]:
    result = runner(
        ["gcloud", "storage", "objects", "describe", object_uri, "--format=json"]
    )
    if result.returncode == 0:
        try:
            metadata = json.loads(result.stdout.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CloudPreservationError(
                f"Could not parse GCS metadata for {object_uri}."
            ) from error
        if not isinstance(metadata, dict):
            raise CloudPreservationError(f"Unexpected GCS metadata for {object_uri}.")
        return metadata, "exists"
    error_text = _command_error(result)
    if "not found" in error_text.lower() or "404" in error_text or "no urls matched" in error_text.lower():
        return None, "absent"
    raise CloudPreservationError(
        f"Could not determine whether {object_uri} exists: {error_text or 'unknown gcloud error'}."
    )


def _metadata_integer(metadata: Mapping[str, object], field: str, object_uri: str) -> int:
    value = metadata.get(field)
    try:
        return int(str(value))
    except (TypeError, ValueError) as error:
        raise CloudPreservationError(
            f"GCS metadata for {object_uri} lacks a valid {field}: {value!r}."
        ) from error


def upload_snapshot(
    snapshot_id: str,
    bucket: str,
    staging_root: Path = DEFAULT_STAGING_ROOT,
    manifest_root: Path = DEFAULT_MANIFEST_ROOT,
    runner: CommandRunner = _run_command,
    clock: Clock = utc_timestamp,
) -> Path:
    """Create or verify the exact snapshot objects, then write a Git receipt."""

    if not SNAPSHOT_ID_PATTERN.fullmatch(snapshot_id):
        raise CloudPreservationError(f"Invalid snapshot ID {snapshot_id!r}.")
    if not GCS_BUCKET_PATTERN.fullmatch(bucket):
        raise CloudPreservationError(
            "Bucket must be a gs:// bucket root without an object prefix."
        )
    manifest_path = manifest_root / snapshot_id / "manifest.json"
    try:
        manifest_content = manifest_path.read_bytes()
    except OSError as error:
        raise CloudPreservationError(f"Unable to read manifest {manifest_path}: {error}.") from error
    manifest = parse_arcgis_json(manifest_content, "Snapshot manifest")
    if manifest.get("snapshot_id") != snapshot_id or manifest.get("source_id") != SOURCE_ID:
        raise CloudPreservationError("Snapshot manifest identity does not match upload request.")
    if manifest.get("review_required") is not False:
        raise CloudPreservationError("Snapshot requires review and cannot be cloud-preserved yet.")

    raw_directory = (
        staging_root / "raw" / "city_austin" / "rna_projects" / "layer_8" / snapshot_id
    )
    inventory = manifest.get("response_inventory")
    if not isinstance(inventory, list):
        raise CloudPreservationError("Snapshot manifest has no response inventory.")
    local_objects: list[tuple[str, Path, str]] = []
    for item in inventory:
        if not isinstance(item, dict):
            raise CloudPreservationError("Snapshot response inventory is malformed.")
        filename = str(item.get("filename"))
        expected_checksum = str(item.get("sha256"))
        if not SHA256_PATTERN.fullmatch(expected_checksum):
            raise CloudPreservationError(f"Invalid manifest checksum for {filename}.")
        local_path = raw_directory / filename
        try:
            content = local_path.read_bytes()
        except OSError as error:
            raise CloudPreservationError(f"Unable to read raw snapshot {local_path}: {error}.") from error
        if sha256_bytes(content) != expected_checksum:
            raise CloudPreservationError(f"Local raw snapshot checksum differs for {local_path}.")
        local_objects.append((filename, local_path, expected_checksum))
    local_objects.append(("manifest.json", manifest_path, sha256_bytes(manifest_content)))

    prefix = f"{bucket.rstrip('/')}/raw/city_austin/rna_projects/layer_8/{snapshot_id}"
    receipt_objects: list[dict[str, object]] = []
    for filename, local_path, expected_checksum in local_objects:
        object_uri = f"{prefix}/{filename}"
        metadata, state = _describe_object(object_uri, runner)
        upload_status = "existing-identical"
        if state == "absent":
            result = runner(build_gcloud_copy_command(local_path, object_uri))
            if result.returncode != 0:
                raise CloudPreservationError(
                    f"Create-only upload failed for {object_uri}: {_command_error(result)}."
                )
            metadata, state = _describe_object(object_uri, runner)
            if metadata is None:
                raise CloudPreservationError(f"Uploaded object is not visible: {object_uri}.")
            upload_status = "created"
        assert metadata is not None
        generation = _metadata_integer(metadata, "generation", object_uri)
        cloud_size = _metadata_integer(metadata, "size", object_uri)
        generation_uri = f"{object_uri}#{generation}"
        cloud_result = runner(["gcloud", "storage", "cat", generation_uri])
        if cloud_result.returncode != 0:
            raise CloudPreservationError(
                f"Could not stream generation-specific object {generation_uri}: "
                f"{_command_error(cloud_result)}."
            )
        local_content = local_path.read_bytes()
        cloud_checksum = verify_cloud_bytes(local_content, cloud_result.stdout, generation_uri)
        if cloud_size != len(local_content) or cloud_checksum != expected_checksum:
            raise CloudPreservationError(
                f"GCS metadata/stream verification disagrees for {generation_uri}."
            )
        receipt_objects.append(
            {
                "filename": filename,
                "gcs_uri": object_uri,
                "generation": generation,
                "generation_uri": generation_uri,
                "upload_status": upload_status,
                "local_byte_size": len(local_content),
                "cloud_byte_size": cloud_size,
                "local_sha256": expected_checksum,
                "cloud_stream_sha256": cloud_checksum,
            }
        )

    receipt: dict[str, object] = {
        "receipt_version": 1,
        "source_id": SOURCE_ID,
        "snapshot_id": snapshot_id,
        "bucket": bucket.rstrip("/"),
        "verified_at": clock(),
        "verification_method": (
            "generation-specific gcloud storage cat byte stream independently SHA-256 hashed"
        ),
        "objects": receipt_objects,
        "receipt_upload": "not uploaded; Git-tracked receipt avoids provenance circularity",
    }
    receipt_path = manifest_root / snapshot_id / "gcs_receipt.json"
    if receipt_path.exists():
        try:
            existing_receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
            raise CloudPreservationError(
                f"Existing GCS receipt cannot be validated: {receipt_path}."
            ) from error

        def stable_receipt(value: Mapping[str, object]) -> dict[str, object]:
            stable_objects = []
            objects = value.get("objects")
            if not isinstance(objects, list):
                raise CloudPreservationError("Existing GCS receipt has no object inventory.")
            for item in objects:
                if not isinstance(item, dict):
                    raise CloudPreservationError("Existing GCS receipt is malformed.")
                stable_objects.append(
                    {key: item.get(key) for key in item if key != "upload_status"}
                )
            return {
                key: value.get(key)
                for key in (
                    "receipt_version",
                    "source_id",
                    "snapshot_id",
                    "bucket",
                    "verification_method",
                    "receipt_upload",
                )
            } | {"objects": stable_objects}

        if stable_receipt(existing_receipt) != stable_receipt(receipt):
            raise CloudPreservationError(
                f"Existing GCS receipt differs from current verified object state: {receipt_path}."
            )
        return receipt_path
    _write_json_immutable(receipt_path, receipt)
    return receipt_path


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    acquire = subparsers.add_parser("acquire", help="Acquire and validate a new layer-8 snapshot.")
    acquire.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    acquire.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    acquire.add_argument("--manifest-root", type=Path, default=DEFAULT_MANIFEST_ROOT)
    acquire.add_argument("--timeout", type=float, default=60.0)
    acquire.add_argument("--max-attempts", type=int, default=3)
    upload = subparsers.add_parser("upload", help="Create-only upload and verify a validated snapshot.")
    upload.add_argument("--snapshot-id", required=True)
    upload.add_argument("--bucket", required=True)
    upload.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    upload.add_argument("--manifest-root", type=Path, default=DEFAULT_MANIFEST_ROOT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        if args.command == "acquire":
            result = acquire_snapshot(
                registry_path=args.registry,
                staging_root=args.staging_root,
                manifest_root=args.manifest_root,
                timeout=args.timeout,
                max_attempts=args.max_attempts,
            )
            print("SUCCESS: Austin RNA Projects layer-8 snapshot acquired")
            print(f"  Snapshot ID: {result.snapshot_id}")
            print(f"  Acquisition time: {result.retrieval_started_at}")
            print(f"  Raw directory: {_display_path(result.raw_directory)}")
            print(f"  Manifest: {_display_path(result.manifest_path)}")
            print(f"  Features: {result.feature_audit.feature_count}")
            print(f"  Feature response checksum: {result.features_checksum}")
            print(f"  Semantic checksum: {result.feature_audit.semantic_checksum}")
            print(f"  Geometry present: {result.feature_audit.geometry_present_count}")
            print(f"  True curves: {result.feature_audit.true_curve_count}")
            if result.review_required:
                print("REVIEW REQUIRED: matching and cloud preservation stopped.", file=sys.stderr)
                return 2
            return 0
        receipt_path = upload_snapshot(
            snapshot_id=args.snapshot_id,
            bucket=args.bucket,
            staging_root=args.staging_root,
            manifest_root=args.manifest_root,
        )
        print("SUCCESS: layer-8 snapshot preserved and independently verified in GCS")
        print(f"  Snapshot ID: {args.snapshot_id}")
        print(f"  Receipt: {_display_path(receipt_path)}")
        return 0
    except GisAcquisitionError as error:
        print("FAILURE: Austin RNA Projects layer-8 reconnaissance", file=sys.stderr)
        print(f"  {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
