#!/usr/bin/env python3
"""Match the governed 37-project universe to one immutable RNA layer-8 snapshot."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Mapping, Sequence

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from scripts.data import fetch_rna_projects_gis as fetch_gis
from scripts.data.fetch_sources import load_registry, write_snapshot


OFFICIAL_SOURCE_ID = "austin_wpd_2026_bond_projects_2025_11_21"
GIS_SOURCE_ID = fetch_gis.SOURCE_ID
GIS_SOURCE_LAYER_ID = fetch_gis.LAYER_ID
GIS_SOURCE_LAYER_NAME = fetch_gis.LAYER_NAME

DEFAULT_PROJECTS_PATH = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "watershed_bond_projects"
    / "2025-11-21"
    / "projects.csv"
)
DEFAULT_REGISTRY_PATH = REPOSITORY_ROOT / "data" / "metadata" / "source_registry.csv"
DEFAULT_STAGING_ROOT = REPOSITORY_ROOT / "data" / "staging"
DEFAULT_MANIFEST_ROOT = fetch_gis.DEFAULT_MANIFEST_ROOT
DEFAULT_OUTPUT_ROOT = (
    REPOSITORY_ROOT
    / "data"
    / "reconnaissance"
    / "city_austin"
    / "rna_projects"
    / "layer_8"
)

EXPECTED_GOVERNED_PROJECT_COUNT = 37
EXPECTED_GOVERNED_FUNDING_TOTAL = 327_970_000
OFFICIAL_ID_PATTERN = re.compile(r"^\d+\.\d{3}$")
MATCH_METHOD = "exact_decimal_three_place_canonicalization"

OFFICIAL_REQUIRED_COLUMNS = (
    "source_id",
    "source_table_row_order",
    "subproject_id",
    "project_name",
    "current_funding_request_estimate_dollars",
)

MATCH_COLUMNS = (
    "official_source_table_row_order",
    "official_subproject_id",
    "official_project_name",
    "gis_snapshot_id",
    "gis_source_layer_id",
    "gis_source_layer_name",
    "match_method",
    "match_status",
    "match_count",
    "match_ordinal",
    "gis_object_id",
    "gis_lrcsp_rolling_needs_id",
    "gis_subproject_id_raw_token",
    "gis_subproject_id_canonical_3dp",
    "gis_subproject_name",
    "project_name_exact_match",
    "gis_subproject_status",
    "gis_subproject_phase",
    "gis_subproject_type_category",
    "gis_department",
    "geometry_present",
    "geometry_type",
    "geometry_crs_wkid",
    "geometry_crs_latest_wkid",
)


class GisMatchingError(RuntimeError):
    """Raised when matching cannot remain complete, exact, and auditable."""


@dataclass(frozen=True)
class OfficialProject:
    source_table_row_order: int
    subproject_id: str
    project_name: str
    funding_dollars: int


@dataclass(frozen=True)
class FundingReconciliation:
    governed_project_count: int
    governed_funding_total: int
    matched_project_count: int
    matched_funding_total: int
    unmatched_project_count: int
    unmatched_funding_total: int
    multiple_match_project_count: int


@dataclass(frozen=True)
class MatchingResult:
    snapshot_id: str
    output_path: Path
    artifact_status: str
    output_row_count: int
    reconciliation: FundingReconciliation


def _exact_int(value: object, context: str) -> int:
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, ValueError) as error:
        raise GisMatchingError(f"{context} is not an exact integer: {value!r}.") from error
    if not decimal_value.is_finite() or decimal_value != decimal_value.to_integral_value():
        raise GisMatchingError(f"{context} is not an exact integer: {value!r}.")
    return int(decimal_value)


def load_official_projects(path: Path = DEFAULT_PROJECTS_PATH) -> tuple[OfficialProject, ...]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as error:
        raise GisMatchingError(f"Unable to read governed project artifact {path}: {error}.") from error
    try:
        reader = csv.DictReader(io.StringIO(content, newline=""))
        columns = tuple(reader.fieldnames or ())
        missing = [column for column in OFFICIAL_REQUIRED_COLUMNS if column not in columns]
        if missing:
            raise GisMatchingError(
                "Governed project artifact is missing columns: " + ", ".join(missing)
            )
        rows = list(reader)
    except csv.Error as error:
        raise GisMatchingError(f"Governed project artifact is invalid CSV: {error}.") from error
    if len(rows) != EXPECTED_GOVERNED_PROJECT_COUNT:
        raise GisMatchingError(
            f"Expected {EXPECTED_GOVERNED_PROJECT_COUNT} governed projects; found {len(rows)}."
        )

    projects: list[OfficialProject] = []
    for csv_row, row in enumerate(rows, start=2):
        if None in row or row.get("source_id") != OFFICIAL_SOURCE_ID:
            raise GisMatchingError(f"Governed project row {csv_row} has invalid source identity or shape.")
        official_id = row["subproject_id"]
        if not OFFICIAL_ID_PATTERN.fullmatch(official_id):
            raise GisMatchingError(
                f"Governed project row {csv_row} has invalid official ID {official_id!r}."
            )
        if not row["project_name"]:
            raise GisMatchingError(f"Governed project row {csv_row} has no project name.")
        projects.append(
            OfficialProject(
                source_table_row_order=_exact_int(
                    row["source_table_row_order"], "source_table_row_order"
                ),
                subproject_id=official_id,
                project_name=row["project_name"],
                funding_dollars=_exact_int(
                    row["current_funding_request_estimate_dollars"],
                    "current_funding_request_estimate_dollars",
                ),
            )
        )
    if [project.source_table_row_order for project in projects] != list(
        range(1, EXPECTED_GOVERNED_PROJECT_COUNT + 1)
    ):
        raise GisMatchingError("Governed source-table order must remain contiguous 1–37.")
    if len({project.subproject_id for project in projects}) != len(projects):
        raise GisMatchingError("Governed official project IDs must remain unique strings.")
    funding_total = sum(project.funding_dollars for project in projects)
    if funding_total != EXPECTED_GOVERNED_FUNDING_TOTAL:
        raise GisMatchingError(
            f"Governed funding total changed: expected ${EXPECTED_GOVERNED_FUNDING_TOTAL:,}; "
            f"found ${funding_total:,}."
        )
    return tuple(projects)


def _load_manifest(path: Path, snapshot_id: str) -> dict[str, object]:
    try:
        content = path.read_bytes()
    except OSError as error:
        raise GisMatchingError(f"Unable to read snapshot manifest {path}: {error}.") from error
    try:
        manifest = fetch_gis.parse_arcgis_json(content, "Snapshot manifest")
    except fetch_gis.GisAcquisitionError as error:
        raise GisMatchingError(str(error)) from error
    canonical_source = manifest.get("canonical_source")
    if (
        manifest.get("source_id") != GIS_SOURCE_ID
        or manifest.get("snapshot_id") != snapshot_id
        or not isinstance(canonical_source, dict)
        or _exact_int(canonical_source.get("layer_id"), "manifest layer id") != GIS_SOURCE_LAYER_ID
        or canonical_source.get("layer_name") != GIS_SOURCE_LAYER_NAME
    ):
        raise GisMatchingError("Snapshot manifest does not identify canonical RNA layer 8.")
    if manifest.get("review_required") is not False:
        raise GisMatchingError("Snapshot requires review; matching was not performed.")
    return manifest


def _inventory_checksum(manifest: Mapping[str, object], filename: str) -> str:
    inventory = manifest.get("response_inventory")
    if not isinstance(inventory, list):
        raise GisMatchingError("Snapshot manifest has no response inventory.")
    matches = [
        item
        for item in inventory
        if isinstance(item, dict) and item.get("filename") == filename
    ]
    if len(matches) != 1:
        raise GisMatchingError(f"Snapshot manifest must inventory {filename} exactly once.")
    checksum = str(matches[0].get("sha256"))
    if not fetch_gis.SHA256_PATTERN.fullmatch(checksum):
        raise GisMatchingError(f"Snapshot manifest checksum is invalid for {filename}.")
    return checksum


def _require_registry_snapshot(
    registry_path: Path, expected_checksum: str, snapshot_id: str
) -> None:
    rows = load_registry(registry_path)
    matches = [row for row in rows if row["source_id"] == GIS_SOURCE_ID]
    if len(matches) != 1:
        raise GisMatchingError(
            f"Source registry must contain exactly one {GIS_SOURCE_ID!r} row."
        )
    source = matches[0]
    if (
        source["historical_fit"] != "uncertain"
        or source["analytical_role"] != "research-only"
        or source["checksum"] != expected_checksum
    ):
        raise GisMatchingError("Registered GIS role, historical fit, or checksum is invalid.")
    retrieved_at = source["retrieved_at"]
    if fetch_gis.snapshot_id_from_timestamp(retrieved_at) != snapshot_id:
        raise GisMatchingError("Registry retrieval timestamp does not identify the snapshot.")


def _geometry_present(feature: Mapping[str, object]) -> bool:
    geometry = feature.get("geometry")
    if not isinstance(geometry, dict):
        return False
    rings = geometry.get("rings")
    curve_rings = geometry.get("curveRings")
    return bool((isinstance(rings, list) and rings) or (isinstance(curve_rings, list) and curve_rings))


def _render_match_rows(
    projects: Sequence[OfficialProject],
    features: Sequence[Mapping[str, object]],
    snapshot_id: str,
) -> tuple[list[dict[str, object]], FundingReconciliation]:
    feature_index: defaultdict[str, list[Mapping[str, object]]] = defaultdict(list)
    for feature in features:
        attributes = feature.get("attributes")
        if not isinstance(attributes, dict):
            raise GisMatchingError("Canonical feature snapshot contains malformed attributes.")
        try:
            _, canonical = fetch_gis.canonicalize_gis_id(attributes.get("SUB_PROJECT_ID"))
        except fetch_gis.UnsafeGisIdentifierError as error:
            raise GisMatchingError(str(error)) from error
        feature_index[canonical].append(feature)
    for candidates in feature_index.values():
        candidates.sort(
            key=lambda feature: _exact_int(
                feature.get("attributes", {}).get("OBJECTID")
                if isinstance(feature.get("attributes"), dict)
                else None,
                "GIS OBJECTID",
            )
        )

    output_rows: list[dict[str, object]] = []
    matched_projects: list[OfficialProject] = []
    unmatched_projects: list[OfficialProject] = []
    multiple_match_count = 0
    for project in projects:
        candidates = feature_index.get(project.subproject_id, [])
        match_count = len(candidates)
        if match_count:
            matched_projects.append(project)
        else:
            unmatched_projects.append(project)
        if match_count > 1:
            multiple_match_count += 1
        match_status = (
            "zero_match" if match_count == 0 else "single_match" if match_count == 1 else "multiple_matches"
        )
        base: dict[str, object] = {
            "official_source_table_row_order": project.source_table_row_order,
            "official_subproject_id": project.subproject_id,
            "official_project_name": project.project_name,
            "gis_snapshot_id": snapshot_id,
            "gis_source_layer_id": GIS_SOURCE_LAYER_ID,
            "gis_source_layer_name": GIS_SOURCE_LAYER_NAME,
            "match_method": MATCH_METHOD,
            "match_status": match_status,
            "match_count": match_count,
        }
        if not candidates:
            output_rows.append(
                {
                    **base,
                    "match_ordinal": "",
                    "gis_object_id": "",
                    "gis_lrcsp_rolling_needs_id": "",
                    "gis_subproject_id_raw_token": "",
                    "gis_subproject_id_canonical_3dp": "",
                    "gis_subproject_name": "",
                    "project_name_exact_match": "",
                    "gis_subproject_status": "",
                    "gis_subproject_phase": "",
                    "gis_subproject_type_category": "",
                    "gis_department": "",
                    "geometry_present": "",
                    "geometry_type": "",
                    "geometry_crs_wkid": "",
                    "geometry_crs_latest_wkid": "",
                }
            )
            continue
        for ordinal, feature in enumerate(candidates, start=1):
            attributes = feature["attributes"]
            assert isinstance(attributes, dict)
            raw_token, canonical = fetch_gis.canonicalize_gis_id(
                attributes["SUB_PROJECT_ID"]
            )
            gis_name = attributes.get("SUB_PROJECT_NAME")
            output_rows.append(
                {
                    **base,
                    "match_ordinal": ordinal,
                    "gis_object_id": _exact_int(attributes.get("OBJECTID"), "GIS OBJECTID"),
                    "gis_lrcsp_rolling_needs_id": _exact_int(
                        attributes.get("LRCSP_ROLLING_NEEDS_ID"),
                        "GIS LRCSP_ROLLING_NEEDS_ID",
                    ),
                    "gis_subproject_id_raw_token": raw_token,
                    "gis_subproject_id_canonical_3dp": canonical,
                    "gis_subproject_name": gis_name,
                    "project_name_exact_match": str(gis_name == project.project_name).lower(),
                    "gis_subproject_status": attributes.get("SUB_PROJECT_STATUS"),
                    "gis_subproject_phase": attributes.get("SUB_PROJECT_PHASE"),
                    "gis_subproject_type_category": attributes.get("SUB_PROJECT_TYPE_CATEGORY"),
                    "gis_department": attributes.get("DEPARTMENT"),
                    "geometry_present": str(_geometry_present(feature)).lower(),
                    "geometry_type": "esriGeometryPolygon",
                    "geometry_crs_wkid": fetch_gis.SOURCE_WKID,
                    "geometry_crs_latest_wkid": fetch_gis.LATEST_WKID,
                }
            )

    reconciliation = FundingReconciliation(
        governed_project_count=len(projects),
        governed_funding_total=sum(project.funding_dollars for project in projects),
        matched_project_count=len(matched_projects),
        matched_funding_total=sum(project.funding_dollars for project in matched_projects),
        unmatched_project_count=len(unmatched_projects),
        unmatched_funding_total=sum(project.funding_dollars for project in unmatched_projects),
        multiple_match_project_count=multiple_match_count,
    )
    if (
        reconciliation.matched_project_count + reconciliation.unmatched_project_count
        != reconciliation.governed_project_count
        or reconciliation.matched_funding_total + reconciliation.unmatched_funding_total
        != reconciliation.governed_funding_total
    ):
        raise GisMatchingError("Matched/unmatched funding reconciliation is incomplete.")
    return output_rows, reconciliation


def render_match_csv(rows: Sequence[Mapping[str, object]]) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=list(MATCH_COLUMNS), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


def match_snapshot(
    snapshot_id: str,
    projects_path: Path = DEFAULT_PROJECTS_PATH,
    registry_path: Path = DEFAULT_REGISTRY_PATH,
    staging_root: Path = DEFAULT_STAGING_ROOT,
    manifest_root: Path = DEFAULT_MANIFEST_ROOT,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
) -> MatchingResult:
    if not fetch_gis.SNAPSHOT_ID_PATTERN.fullmatch(snapshot_id):
        raise GisMatchingError(f"Invalid snapshot ID {snapshot_id!r}.")
    manifest_path = manifest_root / snapshot_id / "manifest.json"
    manifest = _load_manifest(manifest_path, snapshot_id)
    raw_directory = (
        staging_root / "raw" / "city_austin" / "rna_projects" / "layer_8" / snapshot_id
    )
    features_path = raw_directory / "features.arcgis.json"
    layer_path = raw_directory / "layer.json"
    pre_ids_path = raw_directory / "object_ids_pre.json"
    try:
        features_content = features_path.read_bytes()
        layer_content = layer_path.read_bytes()
        pre_ids_content = pre_ids_path.read_bytes()
    except OSError as error:
        raise GisMatchingError(f"Unable to read raw GIS snapshot: {error}.") from error
    expected_features_checksum = _inventory_checksum(manifest, "features.arcgis.json")
    if fetch_gis.sha256_bytes(features_content) != expected_features_checksum:
        raise GisMatchingError("Raw feature response checksum differs from the manifest.")
    _require_registry_snapshot(registry_path, expected_features_checksum, snapshot_id)

    try:
        layer = fetch_gis.parse_arcgis_json(layer_content, "Layer-8 metadata")
        contract = fetch_gis.validate_layer_metadata(layer)
        pre_ids = fetch_gis.parse_object_ids(
            fetch_gis.parse_arcgis_json(pre_ids_content, "Pre-acquisition OBJECTID response"),
            "Pre-acquisition OBJECTID response",
        )
        feature_snapshot = fetch_gis.validate_feature_response(
            features_content, pre_ids, contract
        )
    except fetch_gis.GisAcquisitionError as error:
        raise GisMatchingError(str(error)) from error
    if feature_snapshot.audit.unsafe_numeric_ids:
        raise GisMatchingError("Unsafe GIS numeric IDs prevent matching.")
    if feature_snapshot.audit.true_curve_count:
        raise GisMatchingError("True-curve geometry requires review before derivation.")
    semantic = manifest.get("semantic_fingerprint")
    if not isinstance(semantic, dict) or semantic.get("value") != feature_snapshot.audit.semantic_checksum:
        raise GisMatchingError("Feature semantic fingerprint differs from the manifest.")

    projects = load_official_projects(projects_path)
    features = feature_snapshot.parsed_response.get("features")
    if not isinstance(features, list):
        raise GisMatchingError("Validated feature response contains no features.")
    rows, reconciliation = _render_match_rows(projects, features, snapshot_id)
    output_path = output_root / snapshot_id / "project_id_geometry_matches.csv"
    artifact_status = write_snapshot(output_path, render_match_csv(rows))
    return MatchingResult(
        snapshot_id=snapshot_id,
        output_path=output_path,
        artifact_status=artifact_status,
        output_row_count=len(rows),
        reconciliation=reconciliation,
    )


def _display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(REPOSITORY_ROOT))
    except ValueError:
        return str(path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--snapshot-id", required=True)
    parser.add_argument("--projects", type=Path, default=DEFAULT_PROJECTS_PATH)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY_PATH)
    parser.add_argument("--staging-root", type=Path, default=DEFAULT_STAGING_ROOT)
    parser.add_argument("--manifest-root", type=Path, default=DEFAULT_MANIFEST_ROOT)
    parser.add_argument("--output-root", type=Path, default=DEFAULT_OUTPUT_ROOT)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        result = match_snapshot(
            snapshot_id=args.snapshot_id,
            projects_path=args.projects,
            registry_path=args.registry,
            staging_root=args.staging_root,
            manifest_root=args.manifest_root,
            output_root=args.output_root,
        )
    except (GisMatchingError, OSError, csv.Error, json.JSONDecodeError) as error:
        print("FAILURE: Watershed-to-RNA project matching", file=sys.stderr)
        print(f"  {error}", file=sys.stderr)
        return 1
    reconciliation = result.reconciliation
    print("SUCCESS: Watershed-to-RNA project matching")
    print(f"  Snapshot ID: {result.snapshot_id}")
    print(f"  Output: {_display_path(result.output_path)}")
    print(f"  Artifact status: {result.artifact_status}")
    print(f"  Output rows: {result.output_row_count}")
    print(f"  Matched projects: {reconciliation.matched_project_count}")
    print(f"  Matched funding: ${reconciliation.matched_funding_total:,}")
    print(f"  Zero-match projects: {reconciliation.unmatched_project_count}")
    print(f"  Zero-match funding: ${reconciliation.unmatched_funding_total:,}")
    print(f"  Multiple-match projects: {reconciliation.multiple_match_project_count}")
    print(
        f"  Governed reconciliation: {reconciliation.governed_project_count} projects / "
        f"${reconciliation.governed_funding_total:,}"
    )
    print("  GIS match status is evidence-feasibility information, not eligibility.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
