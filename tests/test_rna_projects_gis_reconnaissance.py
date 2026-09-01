from __future__ import annotations

import csv
import json
import tempfile
import unittest
from collections import defaultdict
from pathlib import Path

from scripts.data import fetch_rna_projects_gis as fetch_gis
from scripts.data import match_watershed_projects_rna as match_gis


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":")).encode("utf-8")


def _service_bytes() -> bytes:
    return _json_bytes(
        {"layers": [{"id": 8, "name": "RNA Projects", "type": "Feature Layer"}]}
    )


def _layer_bytes() -> bytes:
    return _json_bytes(
        {
            "id": 8,
            "name": "RNA Projects",
            "geometryType": "esriGeometryPolygon",
            "capabilities": "Map,Query,Data",
            "maxRecordCount": 1000,
            "sourceSpatialReference": {"wkid": 102739, "latestWkid": 2277},
            "fields": [
                {"name": name, "type": field_type}
                for name, field_type in fetch_gis.EXPECTED_FIELDS
            ],
        }
    )


def _object_ids_bytes(*object_ids: int) -> bytes:
    return _json_bytes(
        {"objectIdFieldName": "OBJECTID", "objectIds": list(object_ids)}
    )


def _feature_response_bytes(
    records: list[tuple[int, int, str, str, object]],
    *,
    exceeded_transfer_limit: bool = False,
) -> bytes:
    fields = [
        {"name": name, "type": field_type}
        for name, field_type in fetch_gis.EXPECTED_FIELDS
        if name != "SHAPE"
    ]
    features: list[str] = []
    for object_id, lrcsp_id, id_token, name, geometry in records:
        attributes = {
            "OBJECTID": object_id,
            "LRCSP_ROLLING_NEEDS_ID": lrcsp_id,
            "SUB_PROJECT_ID": "__RAW_NUMERIC_TOKEN__",
            "SUB_PROJECT_NAME": name,
            "SUB_PROJECT_STATUS": "ACTIVE",
            "SUB_PROJECT_PHASE": "DESIGN",
            "SUB_PROJECT_TYPE_CATEGORY": "Stormwater",
            "DESCRIPTION": "source description",
            "CONTACT": "source contact",
            "DEPARTMENT": "Watershed Protection",
        }
        attributes_json = json.dumps(attributes, separators=(",", ":")).replace(
            '"__RAW_NUMERIC_TOKEN__"', id_token
        )
        features.append(
            '{"attributes":'
            + attributes_json
            + ',"geometry":'
            + json.dumps(geometry, separators=(",", ":"))
            + "}"
        )
    return (
        '{"spatialReference":{"wkid":102739,"latestWkid":2277},'
        + '"fields":'
        + json.dumps(fields, separators=(",", ":"))
        + ',"exceededTransferLimit":'
        + str(exceeded_transfer_limit).lower()
        + ',"features":['
        + ",".join(features)
        + "]}"
    ).encode("utf-8")


class PublicContractTests(unittest.TestCase):
    def test_layer_8_is_the_only_canonical_feature_source(self) -> None:
        self.assertEqual(fetch_gis.LAYER_ID, 8)
        self.assertEqual(fetch_gis.LAYER_NAME, "RNA Projects")
        self.assertEqual(
            fetch_gis.LAYER_URL,
            "https://maps.austintexas.gov/arcgis/rest/services/LongRangeCIP/"
            "RNAProjects/MapServer/8",
        )
        self.assertEqual(match_gis.GIS_SOURCE_LAYER_ID, 8)

    def test_official_id_regex_uses_a_literal_decimal_point(self) -> None:
        self.assertIsNotNone(match_gis.OFFICIAL_ID_PATTERN.fullmatch("5789.150"))
        self.assertIsNone(match_gis.OFFICIAL_ID_PATTERN.fullmatch("5789x150"))


class NumericIdentifierTests(unittest.TestCase):
    def test_native_numeric_token_is_preserved_without_binary_float(self) -> None:
        parsed = fetch_gis.parse_arcgis_json(
            b'{"SUB_PROJECT_ID":5282.043}', "test response"
        )
        value = parsed["SUB_PROJECT_ID"]

        self.assertIsInstance(value, fetch_gis.JsonNumber)
        self.assertEqual(str(value), "5282.043")
        self.assertEqual(
            fetch_gis.canonicalize_gis_id(value),
            ("5282.043", "5282.043"),
        )

    def test_zero_padding_is_exact_and_does_not_change_numeric_value(self) -> None:
        self.assertEqual(
            fetch_gis.canonicalize_gis_id(fetch_gis.JsonNumber("5848.07")),
            ("5848.07", "5848.070"),
        )

    def test_unexpected_meaningful_digits_are_never_rounded(self) -> None:
        with self.assertRaisesRegex(
            fetch_gis.UnsafeGisIdentifierError,
            "require rounding",
        ):
            fetch_gis.canonicalize_gis_id(
                fetch_gis.JsonNumber("5282.0430000000006")
            )


class SnapshotValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = fetch_gis.validate_layer_metadata(
            fetch_gis.parse_arcgis_json(_layer_bytes(), "test layer")
        )
        self.geometry = {"rings": [[[1, 2], [3, 4], [1, 2]]]}

    def test_layer_contract_preserves_schema_and_native_crs(self) -> None:
        self.assertEqual(self.contract.fields, fetch_gis.EXPECTED_FIELDS)
        self.assertEqual(self.contract.geometry_type, "esriGeometryPolygon")
        self.assertEqual((self.contract.wkid, self.contract.latest_wkid), (102739, 2277))

    def test_feature_snapshot_requires_every_frozen_object_id_exactly_once(self) -> None:
        content = _feature_response_bytes(
            [
                (1, 101, "5282.043", "One", self.geometry),
                (2, 102, "5848.07", "Two", self.geometry),
            ]
        )
        snapshot = fetch_gis.validate_feature_response(content, (1, 2), self.contract)

        self.assertEqual(snapshot.object_ids, (1, 2))
        self.assertEqual(snapshot.audit.feature_count, 2)
        self.assertEqual(snapshot.audit.safe_numeric_id_count, 2)
        self.assertEqual(snapshot.audit.geometry_present_count, 2)
        self.assertEqual(snapshot.audit.true_curve_count, 0)
        self.assertRegex(snapshot.audit.semantic_checksum, r"^sha256:[0-9a-f]{64}$")

    def test_missing_or_unexpected_object_ids_fail_as_source_mutation(self) -> None:
        content = _feature_response_bytes(
            [(1, 101, "5282.043", "One", self.geometry)]
        )
        with self.assertRaisesRegex(fetch_gis.SourceMutationError, "frozen OBJECTID"):
            fetch_gis.validate_feature_response(content, (1, 2), self.contract)

    def test_exceeded_transfer_limit_is_never_accepted(self) -> None:
        content = _feature_response_bytes(
            [(1, 101, "5282.043", "One", self.geometry)],
            exceeded_transfer_limit=True,
        )
        with self.assertRaisesRegex(fetch_gis.GisAcquisitionError, "exceededTransferLimit"):
            fetch_gis.validate_feature_response(content, (1,), self.contract)

    def test_geometry_missingness_and_true_curves_are_preserved(self) -> None:
        content = _feature_response_bytes(
            [
                (1, 101, "5282.043", "One", None),
                (
                    2,
                    102,
                    "5848.070",
                    "Two",
                    {"rings": [[[1, 2], [3, 4], [1, 2]]], "curveRings": [[1, 2, 3]]},
                ),
            ]
        )
        snapshot = fetch_gis.validate_feature_response(content, (1, 2), self.contract)

        self.assertEqual(snapshot.audit.geometry_present_count, 1)
        self.assertEqual(snapshot.audit.geometry_missing_count, 1)
        self.assertEqual(snapshot.audit.true_curve_count, 1)

    def test_pre_and_post_object_id_mismatch_fails_without_writing(self) -> None:
        responses = iter(
            [
                fetch_gis.HttpResponse(_service_bytes(), 200, fetch_gis.MAPSERVER_URL, "application/json"),
                fetch_gis.HttpResponse(_layer_bytes(), 200, fetch_gis.LAYER_URL, "application/json"),
                fetch_gis.HttpResponse(_object_ids_bytes(1), 200, fetch_gis.QUERY_URL, "application/json"),
                fetch_gis.HttpResponse(
                    _feature_response_bytes([(1, 101, "5282.043", "One", self.geometry)]),
                    200,
                    fetch_gis.QUERY_URL,
                    "application/json",
                ),
                fetch_gis.HttpResponse(_object_ids_bytes(1, 2), 200, fetch_gis.QUERY_URL, "application/json"),
            ]
        )

        def transport(
            _method: str,
            _url: str,
            _parameters: object,
            _timeout: float,
        ) -> fetch_gis.HttpResponse:
            return next(responses)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = root / "source_registry.csv"
            registry.write_bytes(fetch_gis.DEFAULT_REGISTRY_PATH.read_bytes())
            with self.assertRaisesRegex(fetch_gis.GisAcquisitionError, "changed during"):
                fetch_gis.acquire_snapshot(
                    registry_path=registry,
                    staging_root=root / "staging",
                    manifest_root=root / "manifests",
                    max_attempts=1,
                    transport=transport,
                    clock=lambda: "2026-09-01T12:34:56Z",
                )
            self.assertFalse((root / "staging").exists())
            self.assertFalse((root / "manifests").exists())

    def test_consistent_acquisition_writes_exact_raw_bytes_and_manifest(self) -> None:
        feature_bytes = _feature_response_bytes(
            [(1, 101, "5282.043", "One", self.geometry)]
        )
        responses = iter(
            [
                fetch_gis.HttpResponse(_service_bytes(), 200, fetch_gis.MAPSERVER_URL, "application/json"),
                fetch_gis.HttpResponse(_layer_bytes(), 200, fetch_gis.LAYER_URL, "application/json"),
                fetch_gis.HttpResponse(_object_ids_bytes(1), 200, fetch_gis.QUERY_URL, "application/json"),
                fetch_gis.HttpResponse(feature_bytes, 200, fetch_gis.QUERY_URL, "application/json"),
                fetch_gis.HttpResponse(_object_ids_bytes(1), 200, fetch_gis.QUERY_URL, "application/json"),
            ]
        )

        def transport(
            _method: str,
            _url: str,
            _parameters: object,
            _timeout: float,
        ) -> fetch_gis.HttpResponse:
            return next(responses)

        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            registry = root / "source_registry.csv"
            registry.write_bytes(fetch_gis.DEFAULT_REGISTRY_PATH.read_bytes())
            result = fetch_gis.acquire_snapshot(
                registry_path=registry,
                staging_root=root / "staging",
                manifest_root=root / "manifests",
                max_attempts=1,
                transport=transport,
                clock=lambda: "2026-09-01T12:34:56Z",
            )

            self.assertEqual(result.snapshot_id, "20260901T123456Z")
            self.assertEqual(
                (result.raw_directory / "features.arcgis.json").read_bytes(),
                feature_bytes,
            )
            manifest = json.loads(result.manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["canonical_source"]["layer_id"], 8)
            self.assertEqual(manifest["canonical_source"]["historical_fit"], "uncertain")
            self.assertEqual(manifest["canonical_source"]["analytical_role"], "research-only")
            self.assertTrue(manifest["object_id_reconciliation"]["sets_equal"])
            self.assertFalse(manifest["review_required"])


class MatchingTests(unittest.TestCase):
    def test_zero_and_multiple_matches_are_explicit_and_funding_reconciles(self) -> None:
        geometry = {"rings": [[[1, 2], [3, 4], [1, 2]]]}
        response = fetch_gis.parse_arcgis_json(
            _feature_response_bytes(
                [
                    (1, 101, "1000.001", "Exact", geometry),
                    (2, 102, "1000.001", "Different", geometry),
                ]
            ),
            "test features",
        )
        features = response["features"]
        self.assertIsInstance(features, list)
        projects = (
            match_gis.OfficialProject(1, "1000.001", "Exact", 10),
            match_gis.OfficialProject(2, "2000.002", "Missing", 20),
        )
        rows, reconciliation = match_gis._render_match_rows(
            projects, features, "20260901T123456Z"  # type: ignore[arg-type]
        )

        self.assertEqual(len(rows), 3)
        self.assertEqual([row["match_status"] for row in rows], ["multiple_matches", "multiple_matches", "zero_match"])
        zero_row = rows[-1]
        self.assertEqual(zero_row["official_subproject_id"], "2000.002")
        self.assertEqual(zero_row["match_count"], 0)
        self.assertEqual(zero_row["gis_object_id"], "")
        self.assertEqual(reconciliation.matched_project_count, 1)
        self.assertEqual(reconciliation.matched_funding_total, 10)
        self.assertEqual(reconciliation.unmatched_project_count, 1)
        self.assertEqual(reconciliation.unmatched_funding_total, 20)
        self.assertEqual(reconciliation.multiple_match_project_count, 1)
        self.assertEqual(reconciliation.governed_funding_total, 30)


class CloudSafetyTests(unittest.TestCase):
    def test_gcloud_copy_command_is_create_only(self) -> None:
        command = fetch_gis.build_gcloud_copy_command(
            Path("snapshot.json"), "gs://example-bucket/snapshot.json"
        )
        self.assertIn("--if-generation-match=0", command)
        self.assertNotIn("--overwrite", command)

    def test_cloud_byte_verification_uses_real_sha256_and_size(self) -> None:
        checksum = fetch_gis.verify_cloud_bytes(b"exact bytes", b"exact bytes", "gs://object#1")
        self.assertEqual(checksum, fetch_gis.sha256_bytes(b"exact bytes"))

        with self.assertRaises(fetch_gis.CloudPreservationError):
            fetch_gis.verify_cloud_bytes(b"exact bytes", b"changed", "gs://object#1")


class TrackedSnapshotContractTests(unittest.TestCase):
    def test_latest_snapshot_and_match_artifact_reconcile_without_fixed_match_counts(self) -> None:
        manifests = sorted(fetch_gis.DEFAULT_MANIFEST_ROOT.glob("*/manifest.json"))
        self.assertTrue(manifests, "Expected one acquired layer-8 snapshot manifest.")
        manifest_path = manifests[-1]
        snapshot_id = manifest_path.parent.name
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["snapshot_id"], snapshot_id)
        self.assertEqual(manifest["canonical_source"]["layer_id"], 8)
        self.assertEqual(manifest["canonical_source"]["historical_fit"], "uncertain")
        self.assertEqual(manifest["canonical_source"]["analytical_role"], "research-only")
        self.assertEqual(manifest["numeric_id_audit"]["safe_count"], manifest["numeric_id_audit"]["feature_count"])
        self.assertEqual(manifest["numeric_id_audit"]["unsafe_values"], [])
        self.assertEqual(manifest["geometry"]["source_wkid"], 102739)
        self.assertEqual(manifest["geometry"]["latest_wkid"], 2277)
        self.assertEqual(manifest["geometry"]["true_curve_count"], 0)
        self.assertTrue(manifest["object_id_reconciliation"]["sets_equal"])

        raw_features = (
            fetch_gis.DEFAULT_STAGING_ROOT
            / "raw"
            / "city_austin"
            / "rna_projects"
            / "layer_8"
            / snapshot_id
            / "features.arcgis.json"
        ).read_bytes()
        feature_inventory = next(
            item
            for item in manifest["response_inventory"]
            if item["filename"] == "features.arcgis.json"
        )
        self.assertEqual(fetch_gis.sha256_bytes(raw_features), feature_inventory["sha256"])

        with match_gis.DEFAULT_PROJECTS_PATH.open(encoding="utf-8", newline="") as source_file:
            source_rows = list(csv.DictReader(source_file))
        match_path = (
            match_gis.DEFAULT_OUTPUT_ROOT
            / snapshot_id
            / "project_id_geometry_matches.csv"
        )
        with match_path.open(encoding="utf-8", newline="") as match_file:
            reader = csv.DictReader(match_file)
            self.assertEqual(tuple(reader.fieldnames or ()), match_gis.MATCH_COLUMNS)
            match_rows = list(reader)

        grouped: defaultdict[str, list[dict[str, str]]] = defaultdict(list)
        for row in match_rows:
            grouped[row["official_subproject_id"]].append(row)
            self.assertEqual(row["gis_snapshot_id"], snapshot_id)
            self.assertEqual(row["gis_source_layer_id"], "8")
            self.assertEqual(row["match_method"], match_gis.MATCH_METHOD)
        source_by_id = {row["subproject_id"]: row for row in source_rows}
        self.assertEqual(set(grouped), set(source_by_id))
        self.assertEqual(len(grouped), 37)

        matched_ids: set[str] = set()
        unmatched_ids: set[str] = set()
        multiple_ids: set[str] = set()
        for project_id, rows in grouped.items():
            expected_count = int(rows[0]["match_count"])
            self.assertTrue(all(int(row["match_count"]) == expected_count for row in rows))
            self.assertTrue(
                all(
                    row["official_project_name"] == source_by_id[project_id]["project_name"]
                    for row in rows
                )
            )
            if expected_count == 0:
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows[0]["match_status"], "zero_match")
                self.assertEqual(rows[0]["gis_object_id"], "")
                unmatched_ids.add(project_id)
            else:
                self.assertEqual(len(rows), expected_count)
                self.assertEqual(
                    [int(row["match_ordinal"]) for row in rows],
                    list(range(1, expected_count + 1)),
                )
                for row in rows:
                    raw_token = fetch_gis.JsonNumber(row["gis_subproject_id_raw_token"])
                    _, canonical = fetch_gis.canonicalize_gis_id(raw_token)
                    self.assertEqual(canonical, project_id)
                    self.assertEqual(row["geometry_crs_wkid"], "102739")
                    self.assertEqual(row["geometry_crs_latest_wkid"], "2277")
                matched_ids.add(project_id)
                if expected_count > 1:
                    multiple_ids.add(project_id)

        funding = {
            project_id: int(row["current_funding_request_estimate_dollars"])
            for project_id, row in source_by_id.items()
        }
        self.assertEqual(len(matched_ids) + len(unmatched_ids), 37)
        self.assertEqual(
            sum(funding[project_id] for project_id in matched_ids)
            + sum(funding[project_id] for project_id in unmatched_ids),
            327_970_000,
        )
        self.assertEqual(
            len(multiple_ids),
            sum(1 for rows in grouped.values() if int(rows[0]["match_count"]) > 1),
        )

        receipt_path = manifest_path.parent / "gcs_receipt.json"
        self.assertTrue(receipt_path.exists(), "Expected a durable GCS verification receipt.")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual(receipt["snapshot_id"], snapshot_id)
        self.assertEqual(receipt["receipt_upload"], "not uploaded; Git-tracked receipt avoids provenance circularity")
        self.assertEqual(
            {item["filename"] for item in receipt["objects"]},
            {
                "service.json",
                "layer.json",
                "object_ids_pre.json",
                "features.arcgis.json",
                "object_ids_post.json",
                "manifest.json",
            },
        )
        for item in receipt["objects"]:
            self.assertEqual(item["local_byte_size"], item["cloud_byte_size"])
            self.assertEqual(item["local_sha256"], item["cloud_stream_sha256"])
            self.assertRegex(str(item["generation"]), r"^\d+$")
        manifest_receipt = next(
            item for item in receipt["objects"] if item["filename"] == "manifest.json"
        )
        self.assertEqual(
            manifest_receipt["local_sha256"],
            fetch_gis.sha256_bytes(manifest_path.read_bytes()),
        )


if __name__ == "__main__":
    unittest.main()
