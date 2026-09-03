from __future__ import annotations

import csv
import hashlib
import subprocess
import sys
import unittest
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.artifacts import CatalogArtifact
from climatecapital.contracts.common import ReleaseTier
from climatecapital.contracts.plans import PlanInput
from climatecapital.contracts.versions import (
    ACTIVE_FAMILY_PROJECT_IDS,
    FUNDING_PLAN_CONTRACT_VERSION,
    RELEASE_ARTIFACT_FILENAMES,
)
from climatecapital.plans.evaluator import evaluate_plan
from climatecapital.release.validator import BundleValidationError, validate_bundle


FIXTURE_DIRECTORY = REPOSITORY_ROOT / "release-data/fixture"
METHODOLOGY_PATH = REPOSITORY_ROOT / "docs/methodology/p0-evidence-methodology.md"
RNA_MATCH_PATH = REPOSITORY_ROOT / (
    "data/reconnaissance/city_austin/rna_projects/layer_8/"
    "20260901T183323Z/project_id_geometry_matches.csv"
)


def manifest_sha256() -> str:
    return hashlib.sha256((FIXTURE_DIRECTORY / "manifest.json").read_bytes()).hexdigest()


def authoritative_purpose_audit() -> dict[str, tuple[str, str]]:
    text = METHODOLOGY_PATH.read_text(encoding="utf-8")
    table = text.split("## All-37 Derived Purpose Classification", 1)[1].split(
        "## Evidence Findings and Final P0 Treatment", 1
    )[0]
    expected: dict[str, tuple[str, str]] = {}
    for line in table.splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 6 and cells[0][:1].isdigit():
            expected[cells[0]] = (cells[2], cells[4].upper())
    return expected


class PersistentFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.digest = manifest_sha256()
        cls.bundle = validate_bundle(
            FIXTURE_DIRECTORY,
            manifest_sha256=cls.digest,
            expected_release_tier=ReleaseTier.FIXTURE,
        )

    def test_purpose_and_confidence_match_the_locked_all_37_audit(self) -> None:
        expected = authoritative_purpose_audit()
        actual = {
            project.project_id: (project.purpose.label, project.purpose.confidence)
            for project in self.bundle.catalog.projects
        }
        self.assertEqual(len(expected), 37)
        self.assertEqual(actual, expected)

    def test_fixture_rna_state_does_not_relabel_incomplete_curation_missing(self) -> None:
        rna_items = {
            project.project_id: next(
                item
                for item in project.evidence
                if item.evidence_type == "RNA_DISPLAY_GEOMETRY_AVAILABILITY"
            )
            for project in self.bundle.catalog.projects
        }
        self.assertEqual(rna_items["5789.150"].availability, "NOT_APPLICABLE")
        self.assertTrue(
            all(
                item.availability == "NOT_EVALUATED_FIXTURE"
                and item.reason_code is not None
                and item.reason_code.startswith("fixture:")
                for project_id, item in rna_items.items()
                if project_id != "5789.150"
            )
        )

        coverage = {
            entry.scope: entry
            for entry in self.bundle.manifest.evidence_coverage_missingness
            if entry.evidence_type == "RNA_DISPLAY_GEOMETRY_AVAILABILITY"
        }
        self.assertEqual(
            (
                coverage["GOVERNED_UNIVERSE"].available_count,
                coverage["GOVERNED_UNIVERSE"].missing_count,
                coverage["GOVERNED_UNIVERSE"].not_applicable_count,
                coverage["GOVERNED_UNIVERSE"].fixture_state_count,
            ),
            (0, 0, 1, 36),
        )
        self.assertEqual(
            (
                coverage["ACTIVE_FAMILY"].available_count,
                coverage["ACTIVE_FAMILY"].missing_count,
                coverage["ACTIVE_FAMILY"].not_applicable_count,
                coverage["ACTIVE_FAMILY"].fixture_state_count,
            ),
            (0, 0, 1, 11),
        )

        with RNA_MATCH_PATH.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        matched_ids = {
            row["official_subproject_id"]
            for row in rows
            if row["match_status"] == "single_match"
        }
        self.assertEqual(len(matched_ids), 15)
        self.assertEqual(len(matched_ids & set(ACTIVE_FAMILY_PROJECT_IDS)), 5)

    def test_citywide_program_has_no_fabricated_feature(self) -> None:
        project = next(
            project
            for project in self.bundle.catalog.projects
            if project.project_id == "5789.150"
        )
        self.assertEqual(project.geography_status, "NON_PROJECT_GEOGRAPHY")
        self.assertEqual(project.program_scope, "CITYWIDE_PROGRAM")
        self.assertNotIn(
            "5789.150",
            {
                feature.properties.project_id
                for feature in self.bundle.map_context.features
            },
        )

    def test_all_four_fixture_files_are_git_visible_and_usable(self) -> None:
        visible = subprocess.run(
            [
                "git",
                "ls-files",
                "--cached",
                "--others",
                "--exclude-standard",
                "--",
                "release-data/fixture",
            ],
            cwd=REPOSITORY_ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            set(visible.stdout.splitlines()),
            {f"release-data/fixture/{name}" for name in RELEASE_ARTIFACT_FILENAMES},
        )
        self.assertIsInstance(self.bundle.catalog, CatalogArtifact)

    def test_contextual_fixture_evidence_uses_correct_source_provenance(self) -> None:
        expected = {
            "PROBLEM_SCORE_ASSOCIATION": (
                "austin_wpd_problem_score_documentary_context",
                "HISTORICALLY_VALID",
            ),
            "FEMA_CURRENT_HAZARD_CONTEXT": (
                "austin_floodpro_fema_layer_8_live",
                "HISTORICAL_FIT_UNCERTAIN",
            ),
            "EAZ_2021_CONTEXT": (
                "austin_equity_analysis_zones_2021",
                "HISTORICALLY_VALID",
            ),
        }

        source_references = self.bundle.catalog.source_references

        for evidence_type, (source_id, historical_fit) in expected.items():
            self.assertIn(source_id, source_references)

            source = source_references[source_id]
            self.assertEqual(source.historical_fit, historical_fit)
            self.assertEqual(source.license_reuse_status, "UNVERIFIED")

            for project in self.bundle.catalog.projects:
                item = next(
                    evidence
                    for evidence in project.evidence
                    if evidence.evidence_type == evidence_type
                )

                self.assertEqual(item.availability, "NOT_EVALUATED_FIXTURE")
                self.assertEqual(item.source_ids, [source_id])
                self.assertEqual(item.source_vintage, source.source_vintage)
                self.assertEqual(item.historical_fit, historical_fit)
                self.assertIsNone(item.value)

    def test_reviewed_release_validation_rejects_the_fixture(self) -> None:
        with self.assertRaises(BundleValidationError) as caught:
            validate_bundle(FIXTURE_DIRECTORY, manifest_sha256=self.digest)
        self.assertIn(
            "RELEASE_TIER_REJECTED",
            {violation.code for violation in caught.exception.violations},
        )

    def test_evaluator_loads_and_uses_the_persistent_fixture(self) -> None:
        result = evaluate_plan(
            self.bundle.catalog,
            PlanInput(
                contract_version=FUNDING_PLAN_CONTRACT_VERSION,
                data_version=self.bundle.catalog.data_version,
                available_budget_dollars=143_005_000,
                project_ids=list(ACTIVE_FAMILY_PROJECT_IDS),
                expected_fingerprint=None,
            ),
        )
        self.assertEqual(result.status, "VALID")
        self.assertIsNotNone(result.evaluated_plan)
        assert result.evaluated_plan is not None
        self.assertEqual(result.evaluated_plan.included_total_dollars, 143_005_000)
        self.assertEqual(result.evaluated_plan.remainder_dollars, 0)


if __name__ == "__main__":
    unittest.main()
