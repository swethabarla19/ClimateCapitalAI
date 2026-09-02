from __future__ import annotations

import hashlib
import json
import subprocess
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
    build_bundle,
    canonical_bytes,
    load_json,
    rewrite_artifacts_and_manifest,
)


class BundleValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.bundle = Path(self.temporary_directory.name)
        _, self.manifest_sha256 = build_bundle(self.bundle)

    def assert_rejected(self, digest: str, expected_code: str, **kwargs) -> BundleValidationError:
        with self.assertRaises(BundleValidationError) as caught:
            validate_bundle(self.bundle, manifest_sha256=digest, **kwargs)
        codes = {violation.code for violation in caught.exception.violations}
        self.assertIn(expected_code, codes, caught.exception)
        return caught.exception

    def validate_fixture(self, digest: str | None = None):
        return validate_bundle(
            self.bundle,
            manifest_sha256=digest or self.manifest_sha256,
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_fixture_contract_object_is_valid_only_in_explicit_development_mode(self) -> None:
        bundle = self.validate_fixture()
        self.assertEqual(len(bundle.catalog.projects), 37)
        self.assertEqual(
            sum(project.governed_request_dollars for project in bundle.catalog.projects),
            327_970_000,
        )
        self.assert_rejected(self.manifest_sha256, "RELEASE_TIER_REJECTED")

    def test_cli_defaults_to_reviewed_release_and_requires_explicit_fixture_flag(self) -> None:
        command = [
            sys.executable,
            str(REPOSITORY_ROOT / "scripts/release/validate_bundle.py"),
            str(self.bundle),
            "--manifest-sha256",
            self.manifest_sha256,
        ]
        release_result = subprocess.run(command, capture_output=True, text=True, check=False)
        self.assertEqual(release_result.returncode, 1)
        self.assertIn("RELEASE_TIER_REJECTED", release_result.stderr)
        fixture_result = subprocess.run(
            [*command, "--development-fixture"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(fixture_result.returncode, 0, fixture_result.stderr)
        self.assertIn("tier=FIXTURE", fixture_result.stdout)

    def test_fixed_four_file_set_rejects_missing_and_extra_files(self) -> None:
        (self.bundle / "extra.json").write_text("{}\n", encoding="utf-8")
        self.assert_rejected(
            self.manifest_sha256,
            "INVALID_BUNDLE_FILE_SET",
            expected_release_tier=ReleaseTier.FIXTURE,
        )
        (self.bundle / "extra.json").unlink()
        (self.bundle / "benchmark.json").unlink()
        self.assert_rejected(
            self.manifest_sha256,
            "INVALID_BUNDLE_FILE_SET",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_external_manifest_checksum_is_required_and_exact(self) -> None:
        self.assert_rejected(
            "f" * 64,
            "MANIFEST_CHECKSUM_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )
        self.assert_rejected(
            "SHA256:not-a-checksum",
            "INVALID_EXTERNAL_MANIFEST_SHA256",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_artifact_checksum_and_size_mismatch_fail_closed(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        catalog["projects"][0]["purpose"]["evidence_summary"] += " "
        (self.bundle / "catalog.json").write_bytes(canonical_bytes(catalog))
        error = self.assert_rejected(
            self.manifest_sha256,
            "ARTIFACT_CHECKSUM_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )
        self.assertIn("ARTIFACT_SIZE_MISMATCH", {item.code for item in error.violations})

    def test_unknown_fields_numeric_project_ids_and_float_money_are_rejected(self) -> None:
        mutations = (
            ("unknown", lambda catalog: catalog["projects"][0].update(score=99)),
            (
                "numeric_id",
                lambda catalog: catalog["projects"][0].update(project_id=4015.001),
            ),
            (
                "float_money",
                lambda catalog: catalog["projects"][0].update(
                    governed_request_dollars=15_000_000.0
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    _, digest = build_bundle(directory)
                    catalog = load_json(directory / "catalog.json")
                    mutate(catalog)
                    (directory / "catalog.json").write_bytes(canonical_bytes(catalog))
                    with self.assertRaises(BundleValidationError) as caught:
                        validate_bundle(
                            directory,
                            manifest_sha256=digest,
                            expected_release_tier=ReleaseTier.FIXTURE,
                        )
                    self.assertIn(
                        "ARTIFACT_INVALID",
                        {violation.code for violation in caught.exception.violations},
                    )

    def test_noncanonical_json_duplicate_keys_and_nonfinite_numbers_are_rejected(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        pretty = json.dumps(catalog, ensure_ascii=False, indent=2) + "\n"
        (self.bundle / "catalog.json").write_text(pretty, encoding="utf-8")
        self.assert_rejected(
            self.manifest_sha256,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

        _, self.manifest_sha256 = build_bundle(self.bundle)
        manifest_payload = (self.bundle / "manifest.json").read_text(encoding="utf-8")
        duplicate = manifest_payload.replace(
            '{"approved_source_ids":',
            '{"approved_source_ids":[],"approved_source_ids":',
            1,
        )
        (self.bundle / "manifest.json").write_text(duplicate, encoding="utf-8")
        duplicate_digest = hashlib.sha256(duplicate.encode("utf-8")).hexdigest()
        self.assert_rejected(
            duplicate_digest,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_cross_file_data_contract_and_tier_identity_must_agree(self) -> None:
        for field, value in (
            ("data_version", "different-data-version"),
            ("contract_version", "p0-map-context/9.0.0"),
            ("release_tier", "REVIEWED_RELEASE"),
        ):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    _, _ = build_bundle(directory)
                    map_context = load_json(directory / "map-context.geojson")
                    map_context[field] = value
                    digest = rewrite_artifacts_and_manifest(
                        directory, map_context=map_context
                    )
                    with self.assertRaises(BundleValidationError) as caught:
                        validate_bundle(
                            directory,
                            manifest_sha256=digest,
                            expected_release_tier=ReleaseTier.FIXTURE,
                        )
                    codes = {violation.code for violation in caught.exception.violations}
                    if field == "contract_version":
                        self.assertIn("ARTIFACT_INVALID", codes)
                    else:
                        self.assertIn(
                            "DATA_VERSION_MISMATCH"
                            if field == "data_version"
                            else "RELEASE_TIER_MISMATCH",
                            codes,
                        )

    def test_governed_universe_and_exact_family_reconciliations_fail_closed(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        catalog["projects"][0]["governed_request_dollars"] += 1
        catalog["projects"][0]["governed_request_source_text"] = "$15,000,001"
        (self.bundle / "catalog.json").write_bytes(canonical_bytes(catalog))
        self.assert_rejected(
            self.manifest_sha256,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

        _, self.manifest_sha256 = build_bundle(self.bundle)
        catalog = load_json(self.bundle / "catalog.json")
        active = next(project for project in catalog["projects"] if project["project_id"] == "5789.075")
        outside = next(project for project in catalog["projects"] if project["project_id"] == "5754.089")
        active["p0_family"]["member"] = False
        outside["p0_family"]["member"] = True
        (self.bundle / "catalog.json").write_bytes(canonical_bytes(catalog))
        self.assert_rejected(
            self.manifest_sha256,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_family_membership_is_valid_without_geometry(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            _, digest = build_bundle(
                directory,
                available_geometry_ids={"5754.089"},
            )
            bundle = validate_bundle(
                directory,
                manifest_sha256=digest,
                expected_release_tier=ReleaseTier.FIXTURE,
            )
            family_projects = [project for project in bundle.catalog.projects if project.p0_family.member]
            self.assertEqual(len(family_projects), 12)
            self.assertTrue(
                all(project.geography_status == "DISPLAY_GEOMETRY_MISSING" for project in family_projects if project.project_id != "5789.150")
            )
            self.assertEqual(
                next(project for project in family_projects if project.project_id == "5789.150").geography_status,
                "NON_PROJECT_GEOGRAPHY",
            )

    def test_geometry_backed_out_of_family_record_cannot_change_family(self) -> None:
        bundle = self.validate_fixture()
        outside = next(
            project for project in bundle.catalog.projects if project.project_id == "5754.089"
        )
        self.assertEqual(outside.geography_status, "DISPLAY_GEOMETRY_AVAILABLE")
        self.assertFalse(outside.p0_family.member)
        self.assertEqual(
            sorted(project.project_id for project in bundle.catalog.projects if project.p0_family.member),
            list(bundle.catalog.active_family_summary.project_ids),
        )

    def test_catalog_map_coverage_agreement_rejects_missing_required_feature(self) -> None:
        map_context = load_json(self.bundle / "map-context.geojson")
        map_context["features"] = [
            feature
            for feature in map_context["features"]
            if feature["properties"]["project_id"] != "5282.043"
        ]
        digest = rewrite_artifacts_and_manifest(self.bundle, map_context=map_context)
        self.assert_rejected(
            digest,
            "CATALOG_MAP_COVERAGE_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_citywide_null_geometry_and_unapproved_layers_are_rejected(self) -> None:
        mutations = (
            (
                "citywide_feature",
                lambda map_context: map_context["features"][0]["properties"].update(
                    project_id="5789.150"
                ),
            ),
            (
                "null_geometry",
                lambda map_context: map_context["features"][0].update(geometry=None),
            ),
            (
                "wrong_default",
                lambda map_context: map_context["layer_definitions"][1].update(
                    default_visible=True
                ),
            ),
            (
                "fully_developed",
                lambda map_context: map_context["layer_definitions"].append(
                    {
                        "layer_id": "fully_developed_floodpro",
                        "evidence_role": "RESEARCH_ONLY_EVIDENCE",
                        "default_visible": False,
                        "public_label": "Forbidden",
                        "caveat": "Forbidden",
                    }
                ),
            ),
        )
        for label, mutate in mutations:
            with self.subTest(label=label):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    _, digest = build_bundle(directory)
                    map_context = load_json(directory / "map-context.geojson")
                    mutate(map_context)
                    (directory / "map-context.geojson").write_bytes(
                        canonical_bytes(map_context)
                    )
                    with self.assertRaises(BundleValidationError) as caught:
                        validate_bundle(
                            directory,
                            manifest_sha256=digest,
                            expected_release_tier=ReleaseTier.FIXTURE,
                        )
                    self.assertIn(
                        "ARTIFACT_INVALID",
                        {violation.code for violation in caught.exception.violations},
                    )

    def test_evidence_roles_availability_and_declared_coverage_are_enforced(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        target = next(
            item
            for item in catalog["projects"][0]["evidence"]
            if item["evidence_type"] == "EAZ_2021_CONTEXT"
        )
        target["evidence_role"] = "RESEARCH_ONLY_EVIDENCE"
        digest = rewrite_artifacts_and_manifest(self.bundle, catalog=catalog)
        self.assert_rejected(
            digest,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

        _, self.manifest_sha256 = build_bundle(self.bundle)
        manifest = load_json(self.bundle / "manifest.json")
        declaration = next(
            entry
            for entry in manifest["evidence_coverage_missingness"]
            if entry["evidence_type"] == "PROBLEM_SCORE_ASSOCIATION"
            and entry["scope"] == "ACTIVE_FAMILY"
        )
        declaration["available_count"] += 1
        declaration["fixture_state_count"] -= 1
        digest = rewrite_artifacts_and_manifest(self.bundle, manifest=manifest)
        self.assert_rejected(
            digest,
            "EVIDENCE_COVERAGE_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_reviewed_release_rejects_every_fixture_marker(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        map_context = load_json(self.bundle / "map-context.geojson")
        benchmark = load_json(self.bundle / "benchmark.json")
        manifest = load_json(self.bundle / "manifest.json")
        for artifact in (catalog, map_context, benchmark, manifest):
            artifact["release_tier"] = "REVIEWED_RELEASE"
        digest = rewrite_artifacts_and_manifest(
            self.bundle,
            catalog=catalog,
            map_context=map_context,
            benchmark=benchmark,
            manifest=manifest,
        )
        error = self.assert_rejected(digest, "FIXTURE_MARKER_FORBIDDEN")
        self.assertIn(
            "UNVERIFIED_SOURCE_REUSE",
            {violation.code for violation in error.violations},
        )

    def test_benchmark_fields_cannot_leak_into_catalog_or_map(self) -> None:
        for filename, mutator in (
            (
                "catalog.json",
                lambda value: value["projects"][0].update(
                    historical_city_recommendation={"city_treatment": "CITY_INCLUDED"}
                ),
            ),
            (
                "map-context.geojson",
                lambda value: value["features"][0]["properties"].update(
                    benchmark_treatment="CITY_INCLUDED"
                ),
            ),
        ):
            with self.subTest(filename=filename):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    _, digest = build_bundle(directory)
                    value = load_json(directory / filename)
                    mutator(value)
                    (directory / filename).write_bytes(canonical_bytes(value))
                    with self.assertRaises(BundleValidationError) as caught:
                        validate_bundle(
                            directory,
                            manifest_sha256=digest,
                            expected_release_tier=ReleaseTier.FIXTURE,
                        )
                    self.assertIn(
                        "ARTIFACT_INVALID",
                        {violation.code for violation in caught.exception.violations},
                    )

    def test_forbidden_analytical_aliases_are_rejected_even_in_dynamic_keys(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        manifest = load_json(self.bundle / "manifest.json")
        old_source_id = "austin_rna_projects_layer_8_live"
        forbidden_alias = "funding_priority"
        source = catalog["source_references"].pop(old_source_id)
        source["source_id"] = forbidden_alias
        catalog["source_references"][forbidden_alias] = source

        def replace_source_id(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    if child == old_source_id:
                        value[key] = forbidden_alias
                    else:
                        replace_source_id(child)
            elif isinstance(value, list):
                for index, child in enumerate(value):
                    if child == old_source_id:
                        value[index] = forbidden_alias
                    else:
                        replace_source_id(child)

        replace_source_id(catalog["projects"])
        for source_item in manifest["sources"]:
            if source_item["source_id"] == old_source_id:
                source_item["source_id"] = forbidden_alias
        manifest["approved_source_ids"] = sorted(
            forbidden_alias if source_id == old_source_id else source_id
            for source_id in manifest["approved_source_ids"]
        )
        manifest["sources"] = sorted(
            manifest["sources"], key=lambda item: item["source_id"]
        )
        digest = rewrite_artifacts_and_manifest(
            self.bundle, catalog=catalog, manifest=manifest
        )
        self.assert_rejected(
            digest,
            "FORBIDDEN_FIELD",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_benchmark_cannot_contain_core_family_evidence_or_plan_fields(self) -> None:
        benchmark = load_json(self.bundle / "benchmark.json")
        benchmark["p0_family"] = ["5789.075"]
        (self.bundle / "benchmark.json").write_bytes(canonical_bytes(benchmark))
        self.assert_rejected(
            self.manifest_sha256,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_benchmark_source_identity_cannot_enter_catalog_or_map_source_paths(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        manifest = load_json(self.bundle / "manifest.json")
        benchmark_source = next(
            source
            for source in manifest["sources"]
            if source["source_id"] == "austin_2026_bond_initial_draft_2026_01_21"
        )
        catalog["source_references"][benchmark_source["source_id"]] = benchmark_source
        digest = rewrite_artifacts_and_manifest(self.bundle, catalog=catalog)
        self.assert_rejected(
            digest,
            "BENCHMARK_LEAKAGE",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_source_reference_identity_and_approval_are_cross_checked(self) -> None:
        catalog = load_json(self.bundle / "catalog.json")
        catalog["source_references"]["austin_wpd_2026_bond_projects_2025_11_21"][
            "title"
        ] = "Different source identity"
        digest = rewrite_artifacts_and_manifest(self.bundle, catalog=catalog)
        self.assert_rejected(
            digest,
            "SOURCE_IDENTITY_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

        _, self.manifest_sha256 = build_bundle(self.bundle)
        map_context = load_json(self.bundle / "map-context.geojson")
        map_context["features"][0]["properties"]["source_id"] = "unapproved-source"
        digest = rewrite_artifacts_and_manifest(self.bundle, map_context=map_context)
        self.assert_rejected(
            digest,
            "UNAPPROVED_SOURCE_REFERENCE",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_benchmark_identity_must_match_manifest_and_source_snapshot(self) -> None:
        benchmark = load_json(self.bundle / "benchmark.json")
        benchmark["benchmark_identity"]["published_date"] = "2026-01-22"
        digest = rewrite_artifacts_and_manifest(self.bundle, benchmark=benchmark)
        self.assert_rejected(
            digest,
            "BENCHMARK_IDENTITY_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

        _, self.manifest_sha256 = build_bundle(self.bundle)
        benchmark = load_json(self.bundle / "benchmark.json")
        benchmark["benchmark_identity"]["source_snapshot_sha256"] = "a" * 64
        digest = rewrite_artifacts_and_manifest(self.bundle, benchmark=benchmark)
        self.assert_rejected(
            digest,
            "BENCHMARK_SOURCE_MISMATCH",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_manifest_rejects_circular_deployment_and_mutable_source_identity(self) -> None:
        for field, value in (
            ("manifest_sha256", "0" * 64),
            ("code_git_sha", "a" * 40),
            ("container_image_digest", "sha256:" + "b" * 64),
            ("release_id", "circular-release"),
        ):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as temporary:
                    directory = Path(temporary)
                    manifest, _ = build_bundle(directory)
                    manifest[field] = value
                    payload = canonical_bytes(manifest)
                    (directory / "manifest.json").write_bytes(payload)
                    digest = hashlib.sha256(payload).hexdigest()
                    with self.assertRaises(BundleValidationError) as caught:
                        validate_bundle(
                            directory,
                            manifest_sha256=digest,
                            expected_release_tier=ReleaseTier.FIXTURE,
                        )
                    self.assertIn(
                        "ARTIFACT_INVALID",
                        {violation.code for violation in caught.exception.violations},
                    )

        manifest, _ = build_bundle(self.bundle)
        manifest["sources"][0]["gcs_object"]["uri"] = (
            "gs://climatecapital-ai-raw-swetha/latest/source.pdf"
        )
        payload = canonical_bytes(manifest)
        (self.bundle / "manifest.json").write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        self.assert_rejected(
            digest,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_pinned_gcs_generation_cannot_be_missing_or_latest(self) -> None:
        manifest = load_json(self.bundle / "manifest.json")
        manifest["sources"][0]["gcs_object"]["generation"] = None
        payload = canonical_bytes(manifest)
        (self.bundle / "manifest.json").write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        self.assert_rejected(
            digest,
            "ARTIFACT_INVALID",
            expected_release_tier=ReleaseTier.FIXTURE,
        )


if __name__ == "__main__":
    unittest.main()
