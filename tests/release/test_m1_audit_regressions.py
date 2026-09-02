"""Bundle-validator regressions for the independent M1 approval audit."""

from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.common import ReleaseTier  # noqa: E402
from climatecapital.release.validator import (  # noqa: E402
    BundleValidationError,
    validate_bundle,
)
from tests.release.bundle_factory import (  # noqa: E402
    BENCHMARK_SOURCE_ID,
    MEMO_SOURCE_ID,
    build_bundle,
    canonical_bytes,
    load_json,
    rewrite_artifacts_and_manifest,
)


class AuditBundleRegressionTests(unittest.TestCase):
    def validate_fixture(self, directory: Path, digest: str):
        return validate_bundle(
            directory,
            manifest_sha256=digest,
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def assert_rejected(
        self, directory: Path, digest: str, expected_code: str
    ) -> BundleValidationError:
        with self.assertRaises(BundleValidationError) as caught:
            self.validate_fixture(directory, digest)
        self.assertIn(
            expected_code,
            {violation.code for violation in caught.exception.violations},
            caught.exception,
        )
        return caught.exception

    def test_invented_governed_id_fails_exact_authoritative_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            catalog = load_json(directory / "catalog.json")
            project = catalog["projects"][0]
            project["project_id"] = "7777.777"
            identity = next(
                item
                for item in project["evidence"]
                if item["evidence_type"] == "GOVERNED_PROJECT_IDENTITY"
            )
            identity["value"] = "7777.777"
            digest = rewrite_artifacts_and_manifest(directory, catalog=catalog)
            error = self.assert_rejected(directory, digest, "ARTIFACT_INVALID")
            self.assertIn("authoritative source fingerprint", str(error))

    def test_governed_fact_substitution_fails_exact_authoritative_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            catalog = load_json(directory / "catalog.json")
            first, second = catalog["projects"][:2]
            first["governed_name"], second["governed_name"] = (
                second["governed_name"],
                first["governed_name"],
            )
            digest = rewrite_artifacts_and_manifest(directory, catalog=catalog)
            error = self.assert_rejected(directory, digest, "ARTIFACT_INVALID")
            self.assertIn("authoritative source fingerprint", str(error))

    def test_removed_known_required_gcs_pin_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            manifest = load_json(directory / "manifest.json")
            catalog = load_json(directory / "catalog.json")
            next(
                source
                for source in manifest["sources"]
                if source["source_id"] == MEMO_SOURCE_ID
            )["gcs_object"] = None
            catalog["source_references"][MEMO_SOURCE_ID]["gcs_object"] = None
            digest = rewrite_artifacts_and_manifest(
                directory, manifest=manifest, catalog=catalog
            )
            self.assert_rejected(directory, digest, "REQUIRED_GCS_PIN_MISMATCH")

    def test_map_historical_fit_must_match_referenced_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            map_context = load_json(directory / "map-context.geojson")
            map_context["features"][0]["properties"]["historical_fit"] = (
                "CURRENT_CONTEXT_ONLY"
            )
            digest = rewrite_artifacts_and_manifest(
                directory, map_context=map_context
            )
            self.assert_rejected(directory, digest, "MAP_PROVENANCE_MISMATCH")

    def test_evidence_historical_fit_must_match_referenced_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            catalog = load_json(directory / "catalog.json")
            item = next(
                evidence
                for evidence in catalog["projects"][0]["evidence"]
                if evidence["evidence_type"] == "GOVERNED_PROJECT_IDENTITY"
            )
            item["historical_fit"] = "CURRENT_CONTEXT_ONLY"
            digest = rewrite_artifacts_and_manifest(directory, catalog=catalog)
            self.assert_rejected(directory, digest, "EVIDENCE_PROVENANCE_MISMATCH")

    def test_evidence_vintage_must_match_referenced_source(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            catalog = load_json(directory / "catalog.json")
            item = next(
                evidence
                for evidence in catalog["projects"][0]["evidence"]
                if evidence["evidence_type"] == "GOVERNED_PROJECT_IDENTITY"
            )
            item["source_vintage"] = "bundle-internal replacement vintage"
            digest = rewrite_artifacts_and_manifest(directory, catalog=catalog)
            self.assert_rejected(directory, digest, "EVIDENCE_PROVENANCE_MISMATCH")

    def test_map_transformation_must_match_layer_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            map_context = load_json(directory / "map-context.geojson")
            map_context["features"][0]["properties"]["transformation_version"] = (
                "bundle-internal-transform-1"
            )
            digest = rewrite_artifacts_and_manifest(
                directory, map_context=map_context
            )
            self.assert_rejected(directory, digest, "TRANSFORMATION_VERSION_MISMATCH")

    def test_invented_benchmark_governed_overlap_id_fails(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            benchmark = load_json(directory / "benchmark.json")
            benchmark["published_project_treatments"].append(
                {
                    "entry_id": "audit:invented-governed-overlap",
                    "governed_project_id": "7777.777",
                    "published_project_name": "Invented overlap",
                    "city_treatment": {
                        "availability": "NOT_EVALUATED_FIXTURE",
                        "reason_code": "benchmark:not_evaluated_fixture",
                        "explanation": "Technical state only.",
                    },
                    "published_amount": {
                        "availability": "NOT_EVALUATED_FIXTURE",
                        "unit": "USD",
                        "reason_code": "benchmark:not_evaluated_fixture",
                        "explanation": "Technical state only.",
                    },
                    "source_ids": [BENCHMARK_SOURCE_ID],
                    "limitations": ["No governed overlap exists."],
                }
            )
            benchmark["reconciliation"]["entry_count"] = 1
            digest = rewrite_artifacts_and_manifest(
                directory, benchmark=benchmark
            )
            self.assert_rejected(directory, digest, "BENCHMARK_GOVERNED_ID_UNKNOWN")

    def test_bom_newline_nonfinite_and_symlink_paths_are_explicit(self) -> None:
        byte_mutations = {
            "bom": lambda payload: b"\xef\xbb\xbf" + payload,
            "crlf": lambda payload: payload.replace(b"\n", b"\r\n"),
            "missing_final_newline": lambda payload: payload.rstrip(b"\n"),
            "nonfinite": lambda payload: payload.replace(
                b'"historical_envelope_dollars":125000000',
                b'"historical_envelope_dollars":NaN',
                1,
            ),
        }
        for label, mutate in byte_mutations.items():
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                directory = Path(temporary)
                _, digest = build_bundle(directory)
                path = directory / "catalog.json"
                path.write_bytes(mutate(path.read_bytes()))
                self.assert_rejected(directory, digest, "ARTIFACT_INVALID")

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, digest = build_bundle(directory)
            benchmark_path = directory / "benchmark.json"
            target = directory / "catalog.json"
            benchmark_path.unlink()
            os.symlink(target, benchmark_path)
            self.assert_rejected(directory, digest, "ARTIFACT_INVALID")

    def test_source_identity_cannot_be_changed_bundle_internally(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, _ = build_bundle(directory)
            manifest = load_json(directory / "manifest.json")
            catalog = load_json(directory / "catalog.json")
            changed_title = "Bundle-internal replacement source"
            next(
                source
                for source in manifest["sources"]
                if source["source_id"] == MEMO_SOURCE_ID
            )["title"] = changed_title
            catalog["source_references"][MEMO_SOURCE_ID]["title"] = changed_title
            digest = rewrite_artifacts_and_manifest(
                directory, manifest=manifest, catalog=catalog
            )
            self.assert_rejected(directory, digest, "SOURCE_REGISTRATION_MISMATCH")


if __name__ == "__main__":
    unittest.main()
