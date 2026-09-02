"""Focused regressions for the final independent M1 re-audit."""

from __future__ import annotations

import copy
import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path

from pydantic import ValidationError

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.api import (  # noqa: E402
    BenchmarkSuccessEnvelope,
    BootstrapSuccessEnvelope,
)
from climatecapital.contracts.plans import (  # noqa: E402
    EvaluatedPlan,
    PlanEvaluationResponseData,
)
from climatecapital.contracts.session import BrowserSessionState  # noqa: E402
from climatecapital.contracts.versions import (  # noqa: E402
    ACTIVE_FAMILY_PROJECT_IDS,
    ACTIVE_FAMILY_REQUEST_DOLLARS,
    API_NAMESPACE,
    BENCHMARK_CONTRACT_VERSION,
    BROWSER_SESSION_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    GOVERNED_PROJECT_IDS,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)
from tests.release.bundle_factory import build_bundle, load_json  # noqa: E402


class FinalM1AuditRegressionTests(unittest.TestCase):
    data_version = "m1-contract-test-1"

    def evaluated_plan(
        self,
        project_ids: list[str],
        *,
        budget: int = 125_000_000,
        plan_fingerprint: str = "a" * 64,
        expected_fingerprint: str | None = None,
        matches: bool | None = None,
    ) -> dict:
        included = sorted(project_ids)
        requests = [
            {
                "project_id": project_id,
                "governed_request_dollars": ACTIVE_FAMILY_REQUEST_DOLLARS[project_id],
            }
            for project_id in included
        ]
        total = sum(item["governed_request_dollars"] for item in requests)
        return {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": self.data_version,
            "included_project_ids": included,
            "not_included_active_family_project_ids": sorted(
                set(ACTIVE_FAMILY_PROJECT_IDS) - set(included)
            ),
            "included_count": len(included),
            "included_governed_requests": requests,
            "included_total_dollars": total,
            "available_budget_dollars": budget,
            "remainder_dollars": budget - total,
            "overage_dollars": None,
            "confirmation_status": "VALID",
            "warnings": [],
            "plan_fingerprint": plan_fingerprint,
            "fingerprint_verification": {
                "expected_fingerprint": expected_fingerprint,
                "matches": matches,
            },
        }

    def deployment_identity(self, release_tier: str) -> dict:
        return {
            "code_git_sha": "a" * 40,
            "manifest_sha256": "b" * 64,
            "container_image_digest": f"sha256:{'c' * 64}",
            "release_tier": release_tier,
        }

    def response_identity(self, data_version: str, contract_version: str | None) -> dict:
        return {
            "request_id": "123e4567-e89b-42d3-a456-426614174000",
            "api_namespace": API_NAMESPACE,
            "contract_version": contract_version,
            "data_version": data_version,
            "release_id": "m1-final-audit",
        }

    def test_published_schemas_express_representable_m1_invariants(self) -> None:
        schema_dir = REPOSITORY_ROOT / "contracts" / "schemas"
        governed_csv = (
            REPOSITORY_ROOT
            / "data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv"
        )
        with governed_csv.open(newline="", encoding="utf-8") as handle:
            self.assertEqual(
                [row["subproject_id"] for row in csv.DictReader(handle)],
                list(GOVERNED_PROJECT_IDS),
            )
        plan_input = json.loads(
            (schema_dir / "funding-plan-input-1.0.0.schema.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertIs(plan_input["properties"]["project_ids"]["uniqueItems"], True)

        evaluated = json.loads(
            (schema_dir / "funding-plan-evaluated-result-1.0.0.schema.json").read_text(
                encoding="utf-8"
            )
        )
        for property_name in (
            "included_project_ids",
            "not_included_active_family_project_ids",
            "included_governed_requests",
        ):
            self.assertIs(evaluated["properties"][property_name]["uniqueItems"], True)

        catalog = json.loads(
            (schema_dir / "catalog-1.0.0.schema.json").read_text(encoding="utf-8")
        )
        evidence = catalog["$defs"]["EvidenceItem"]
        evidence_types = {
            branch["if"]["properties"]["evidence_type"]["const"]: branch["then"]
            for branch in evidence["allOf"]
            if "evidence_type" in branch.get("if", {}).get("properties", {})
        }
        expected_benefit = evidence_types["EXPECTED_FLOOD_REDUCTION_BENEFIT"]
        self.assertEqual(
            expected_benefit["properties"]["evidence_role"]["const"],
            "UNAVAILABLE_UNSUPPORTED",
        )
        self.assertEqual(
            expected_benefit["properties"]["availability"]["enum"],
            ["UNSUPPORTED"],
        )
        self.assertEqual(
            catalog["$defs"]["ProjectRecord"]["properties"]["project_id"]["enum"],
            list(GOVERNED_PROJECT_IDS),
        )
        self.assertEqual(len(catalog["properties"]["projects"]["allOf"]), 37)
        active_family = catalog["$defs"]["ActiveFamilySummary"]["properties"][
            "project_ids"
        ]
        self.assertEqual(
            [item["const"] for item in active_family["prefixItems"]],
            list(ACTIVE_FAMILY_PROJECT_IDS),
        )

        manifest = json.loads(
            (schema_dir / "release-manifest-1.0.0.schema.json").read_text(
                encoding="utf-8"
            )
        )
        governed_family = manifest["$defs"]["GovernedReconciliations"][
            "properties"
        ]["active_family_project_ids"]
        for keyword in ("items", "maxItems", "minItems", "prefixItems", "uniqueItems"):
            self.assertEqual(governed_family[keyword], active_family[keyword])
        self.assertEqual(
            len(manifest["properties"]["evidence_coverage_missingness"]["allOf"]),
            20,
        )

    def test_fingerprint_truth_rejects_false_match_and_stale_confirmation(self) -> None:
        mismatch = self.evaluated_plan(
            [],
            plan_fingerprint="a" * 64,
            expected_fingerprint="b" * 64,
            matches=True,
        )
        with self.assertRaises(ValidationError):
            EvaluatedPlan.model_validate(mismatch, strict=True)

        false_negative = self.evaluated_plan(
            [],
            plan_fingerprint="a" * 64,
            expected_fingerprint="a" * 64,
            matches=False,
        )
        with self.assertRaises(ValidationError):
            EvaluatedPlan.model_validate(false_negative, strict=True)

        identity = {
            "data_version": self.data_version,
            "manifest_sha256": "d" * 64,
            "release_id": "m1-final-audit",
            "release_manifest_contract_version": RELEASE_MANIFEST_CONTRACT_VERSION,
        }
        state = {
            "contract_version": BROWSER_SESSION_CONTRACT_VERSION,
            "validated_identity": identity,
            "presentation": {
                "route": "FUNDING_PLAN",
                "search_text": "",
                "filter_ids": [],
                "sort": "SOURCE_ORDER",
                "visible_layers": ["rna_current_project_display"],
                "list_position": 0,
            },
            "working_plan": {
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": self.data_version,
                "available_budget_dollars": 125_000_000,
                "project_ids": [],
                "expected_fingerprint": "b" * 64,
            },
            "session_reference_plan": {
                "validated_identity": identity,
                "input": {
                    "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                    "data_version": self.data_version,
                    "available_budget_dollars": 125_000_000,
                    "project_ids": [],
                    "expected_fingerprint": "b" * 64,
                },
                "last_server_result": mismatch,
                "fingerprint": "a" * 64,
            },
            "current_confirmed_plan": "REFERENCE",
            "reviewed_draft": {
                "plan": "REFERENCE",
                "fingerprint": "a" * 64,
                "validated_identity": identity,
                "current_session_only": True,
                "non_official": True,
            },
            "local_request_states": [],
        }
        with self.assertRaises(ValidationError):
            BrowserSessionState.model_validate(state, strict=True)

        valid = self.evaluated_plan(
            [],
            plan_fingerprint="a" * 64,
            expected_fingerprint="a" * 64,
            matches=True,
        )
        self.assertIs(
            EvaluatedPlan.model_validate(valid, strict=True).fingerprint_verification.matches,
            True,
        )

    def test_plan_comparison_must_be_exactly_derived_from_both_plans(self) -> None:
        unchanged_id = "5789.107"
        entering_id = "5789.075"
        leaving_id = "5282.043"
        current = self.evaluated_plan([entering_id, unchanged_id])
        reference = self.evaluated_plan([leaving_id, unchanged_id])
        valid = {
            "current": {
                "status": "VALID",
                "evaluated_plan": current,
                "semantic_errors": [],
            },
            "reference": {
                "status": "VALID",
                "evaluated_plan": reference,
                "semantic_errors": [],
            },
            "comparison": {
                "budget_difference_dollars": 0,
                "included_total_difference_dollars": 26_500_000,
                "remainder_difference_dollars": -26_500_000,
                "included_count_difference": 0,
                "entering": {
                    "project_ids": [entering_id],
                    "governed_request_total_dollars": 35_000_000,
                },
                "leaving": {
                    "project_ids": [leaving_id],
                    "governed_request_total_dollars": 8_500_000,
                },
                "unchanged_project_ids": [unchanged_id],
            },
        }
        PlanEvaluationResponseData.model_validate(valid, strict=True)
        mutations = (
            ("invented scalar delta", lambda item: item["comparison"].update(
                included_total_difference_dollars=26_500_001
            )),
            ("invented entering IDs", lambda item: item["comparison"]["entering"].update(
                project_ids=[], governed_request_total_dollars=0
            )),
            ("invented leaving IDs", lambda item: item["comparison"]["leaving"].update(
                project_ids=[], governed_request_total_dollars=0
            )),
            ("duplicate unchanged IDs", lambda item: item["comparison"].update(
                unchanged_project_ids=[unchanged_id, unchanged_id]
            )),
        )
        for label, mutate in mutations:
            candidate = copy.deepcopy(valid)
            mutate(candidate)
            with self.subTest(label=label), self.assertRaises(ValidationError):
                PlanEvaluationResponseData.model_validate(candidate, strict=True)

    def test_api_deployment_tier_must_match_bootstrap_and_benchmark_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            build_bundle(directory)
            catalog = load_json(directory / "catalog.json")
            map_context = load_json(directory / "map-context.geojson")
            benchmark = load_json(directory / "benchmark.json")
        data_version = catalog["data_version"]
        fixture_deployment = self.deployment_identity("FIXTURE")
        reviewed_deployment = self.deployment_identity("REVIEWED_RELEASE")
        bootstrap = {
            "endpoint": "/api/v1/bootstrap",
            "status": "SUCCESS",
            "identity": self.response_identity(data_version, None),
            "data": {
                "catalog": catalog,
                "map_context": map_context,
                "map_defaults": {
                    "rna_current_project_display": True,
                    "fema_current_hazard_context": False,
                    "eaz_2021_context": False,
                },
                "public_configuration": {
                    "environment_label": "M1 fixture",
                    "osm_tile_url": "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
                    "osm_attribution": "OpenStreetMap contributors",
                    "fixture_mode": True,
                },
                "deployment_identity": fixture_deployment,
            },
        }
        BootstrapSuccessEnvelope.model_validate_json(json.dumps(bootstrap), strict=True)
        invalid_bootstrap = copy.deepcopy(bootstrap)
        invalid_bootstrap["data"]["deployment_identity"] = reviewed_deployment
        with self.assertRaises(ValidationError):
            BootstrapSuccessEnvelope.model_validate_json(
                json.dumps(invalid_bootstrap), strict=True
            )

        benchmark_envelope = {
            "endpoint": "/api/v1/benchmark",
            "status": "SUCCESS",
            "identity": self.response_identity(
                data_version, BENCHMARK_CONTRACT_VERSION
            ),
            "data": {
                "benchmark": benchmark,
                "deployment_identity": fixture_deployment,
            },
        }
        BenchmarkSuccessEnvelope.model_validate_json(
            json.dumps(benchmark_envelope), strict=True
        )
        invalid_benchmark = copy.deepcopy(benchmark_envelope)
        invalid_benchmark["data"]["deployment_identity"] = reviewed_deployment
        with self.assertRaises(ValidationError):
            BenchmarkSuccessEnvelope.model_validate_json(
                json.dumps(invalid_benchmark), strict=True
            )


if __name__ == "__main__":
    unittest.main()
