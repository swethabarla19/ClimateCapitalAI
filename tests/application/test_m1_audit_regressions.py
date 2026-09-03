"""Public contract regressions for the independent M1 approval audit."""

from __future__ import annotations

import json
import csv
import hashlib
import sys
import unittest
from pathlib import Path

from pydantic import ValidationError

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.api import (  # noqa: E402
    ApiSuccessEnvelope,
    PlanEvaluationSuccessEnvelope,
)
from climatecapital.contracts.authority import REGISTERED_SOURCE_IDENTITIES  # noqa: E402
from climatecapital.contracts.artifacts import (  # noqa: E402
    PublishedMoneyValue,
    PublishedPortfolioSummary,
    PublishedProjectTreatment,
)
from climatecapital.contracts.common import EvidenceItem  # noqa: E402
from climatecapital.contracts.gemini import GeminiExplainRequest  # noqa: E402
from climatecapital.contracts.plans import (  # noqa: E402
    BenchmarkComparisonRequest,
    BenchmarkComparisonResponseData,
    EvaluatedPlan,
    PlanEvaluationRequest,
    PlanInput,
)
from climatecapital.contracts.schema_export import SCHEMA_EXPORTS  # noqa: E402
from climatecapital.contracts.session import BrowserSessionState  # noqa: E402
from climatecapital.contracts.versions import (  # noqa: E402
    ACTIVE_FAMILY_PROJECT_IDS,
    ACTIVE_FAMILY_REQUEST_DOLLARS,
    BENCHMARK_CONTRACT_VERSION,
    BROWSER_SESSION_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    GEMINI_EXPLAIN_CONTRACT_VERSION,
    GOVERNED_SOURCE_SEMANTIC_SHA256,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)


class AuditContractRegressionTests(unittest.TestCase):
    def plan_input(self, *, data_version: str = "m1-contract-test-1") -> dict:
        return {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": data_version,
            "available_budget_dollars": 125_000_000,
            "project_ids": [],
        }

    def evaluated_plan(self, *, data_version: str = "m1-contract-test-1") -> dict:
        return {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": data_version,
            "included_project_ids": [],
            "not_included_active_family_project_ids": list(ACTIVE_FAMILY_PROJECT_IDS),
            "included_count": 0,
            "included_governed_requests": [],
            "included_total_dollars": 0,
            "available_budget_dollars": 125_000_000,
            "remainder_dollars": 125_000_000,
            "overage_dollars": None,
            "confirmation_status": "VALID",
            "warnings": [],
            "plan_fingerprint": "a" * 64,
            "fingerprint_verification": {},
        }

    def test_expected_benefit_cannot_be_rewritten_as_available_fact(self) -> None:
        candidate = {
            "evidence_id": "audit:expected-benefit",
            "evidence_type": "EXPECTED_FLOOD_REDUCTION_BENEFIT",
            "evidence_role": "FACT",
            "fact_kind": "SOURCE_GOVERNED",
            "availability": "AVAILABLE",
            "explanation": "Invalid attempted rewrite.",
            "value": 1,
            "source_ids": ["austin_wpd_2026_bond_projects_2025_11_21"],
            "source_vintage": "2025-11-21 planning snapshot",
            "historical_fit": "HISTORICALLY_VALID",
            "coverage_scope": "ACTIVE_FAMILY",
            "limitations": ["Expected benefit is unsupported."],
            "public_label": "Expected flood-reduction benefit",
            "public_disclaimer": "Unsupported in P0.",
        }
        with self.assertRaises(ValidationError):
            EvidenceItem.model_validate(candidate, strict=True)

    def test_duplicate_evaluated_membership_cannot_inflate_arithmetic(self) -> None:
        candidate = self.evaluated_plan()
        candidate.update(
            included_project_ids=["5789.075", "5789.075"],
            not_included_active_family_project_ids=[
                project_id
                for project_id in ACTIVE_FAMILY_PROJECT_IDS
                if project_id != "5789.075"
            ],
            included_count=2,
            included_governed_requests=[
                {"project_id": "5789.075", "governed_request_dollars": 35_000_000},
                {"project_id": "5789.075", "governed_request_dollars": 35_000_000},
            ],
            included_total_dollars=70_000_000,
            remainder_dollars=55_000_000,
        )
        with self.assertRaises(ValidationError):
            EvaluatedPlan.model_validate(candidate, strict=True)

    def test_optional_expected_fingerprint_and_reference_are_omittable(self) -> None:
        plan = PlanInput.model_validate(self.plan_input(), strict=True)
        request = PlanEvaluationRequest.model_validate({"current": self.plan_input()}, strict=True)
        self.assertIsNone(plan.expected_fingerprint)
        self.assertIsNone(request.reference)

    def test_duplicate_identity_assertions_must_agree(self) -> None:
        reference = self.plan_input(data_version="different-data-version")
        with self.assertRaises(ValidationError):
            PlanEvaluationRequest.model_validate(
                {"current": self.plan_input(), "reference": reference}, strict=True
            )
        envelope = {
            "endpoint": "/api/v1/plans/evaluate",
            "status": "SUCCESS",
            "identity": {
                "request_id": "123e4567-e89b-42d3-a456-426614174000",
                "api_namespace": "/api/v1",
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": "different-data-version",
                "release_id": "local-test",
            },
            "data": {
                "current": {
                    "status": "VALID",
                    "evaluated_plan": self.evaluated_plan(),
                    "semantic_errors": [],
                }
            },
        }
        with self.assertRaises(ValidationError):
            PlanEvaluationSuccessEnvelope.model_validate(envelope, strict=True)

    def test_arbitrary_success_payload_cannot_bypass_endpoint_contracts(self) -> None:
        candidate = {
            "endpoint": "/api/v1/plans/evaluate",
            "status": "SUCCESS",
            "identity": {
                "request_id": "123e4567-e89b-42d3-a456-426614174000",
                "api_namespace": "/api/v1",
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": "m1-contract-test-1",
                "release_id": "local-test",
            },
            "data": {"priority_score": 99},
        }
        with self.assertRaises(ValidationError):
            ApiSuccessEnvelope.model_validate(candidate, strict=True)

    def test_stale_confirmed_browser_state_fails_under_new_identity(self) -> None:
        old_identity = {
            "data_version": "m1-contract-test-1",
            "manifest_sha256": "a" * 64,
            "release_id": "old-release",
            "release_manifest_contract_version": RELEASE_MANIFEST_CONTRACT_VERSION,
        }
        state = {
            "contract_version": BROWSER_SESSION_CONTRACT_VERSION,
            "validated_identity": {
                "data_version": "m1-contract-test-1",
                "manifest_sha256": "b" * 64,
                "release_id": "new-release",
                "release_manifest_contract_version": RELEASE_MANIFEST_CONTRACT_VERSION,
            },
            "presentation": {
                "route": "FUNDING_PLAN",
                "search_text": "",
                "filter_ids": [],
                "sort": "SOURCE_ORDER",
                "visible_layers": ["rna_current_project_display"],
                "list_position": 0,
            },
            "working_plan": self.plan_input(),
            "session_reference_plan": {
                "validated_identity": old_identity,
                "input": self.plan_input(),
                "last_server_result": self.evaluated_plan(),
                "fingerprint": "a" * 64,
            },
            "current_confirmed_plan": "REFERENCE",
            "reviewed_draft": {
                "plan": "REFERENCE",
                "fingerprint": "a" * 64,
                "validated_identity": old_identity,
                "current_session_only": True,
                "non_official": True,
            },
            "local_request_states": [],
        }
        with self.assertRaises(ValidationError):
            BrowserSessionState.model_validate(state, strict=True)

    def test_current_confirmed_and_reviewed_browser_state_passes(self) -> None:
        identity = {
            "data_version": "m1-contract-test-1",
            "manifest_sha256": "a" * 64,
            "release_id": "current-release",
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
            "working_plan": self.plan_input(),
            "session_reference_plan": {
                "validated_identity": identity,
                "input": self.plan_input(),
                "last_server_result": self.evaluated_plan(),
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
        parsed = BrowserSessionState.model_validate(state, strict=True)
        self.assertEqual(parsed.reviewed_draft.validated_identity, parsed.validated_identity)

    def test_contradictory_gemini_fingerprints_fail(self) -> None:
        plan = self.plan_input()
        plan["expected_fingerprint"] = "a" * 64
        candidate = {
            "contract_version": GEMINI_EXPLAIN_CONTRACT_VERSION,
            "data_version": "m1-contract-test-1",
            "context_type": "PLAN",
            "current_plan": plan,
            "expected_fingerprints": {"current": "b" * 64},
            "user_question": "Explain the governed plan.",
        }
        with self.assertRaises(ValidationError):
            GeminiExplainRequest.model_validate(candidate, strict=True)

    def test_benchmark_fields_have_independent_partial_availability(self) -> None:
        summary = PublishedPortfolioSummary.model_validate_json(
            json.dumps(
                {
                "published_allocation": {
                    "availability": "AVAILABLE",
                    "value_dollars": 125_000_000,
                    "source_text": "$125,000,000",
                    "unit": "USD",
                    "explanation": "Published allocation is available.",
                },
                "city_included_count": {
                    "availability": "MISSING",
                    "reason_code": "benchmark:count_not_published",
                    "explanation": "No supported count is available.",
                },
                    "explanation": "Fields retain independent availability.",
                }
            ),
            strict=True,
        )
        self.assertEqual(summary.published_allocation.value_dollars, 125_000_000)
        self.assertIsNone(summary.city_included_count.value)
        treatment = PublishedProjectTreatment.model_validate_json(
            json.dumps(
                {
                    "entry_id": "audit:partial-treatment",
                    "published_project_name": "Published project",
                    "city_treatment": {
                        "availability": "AVAILABLE",
                        "value": "CITY_INCLUDED",
                        "explanation": "Published treatment is available.",
                    },
                    "published_amount": {
                        "availability": "MISSING",
                        "unit": "USD",
                        "reason_code": "benchmark:amount_not_published",
                        "explanation": "No supported amount is available.",
                    },
                    "source_ids": ["austin_2026_bond_initial_draft_2026_01_21"],
                    "limitations": ["Descriptive benchmark only."],
                }
            ),
            strict=True,
        )
        self.assertEqual(treatment.city_treatment.value, "CITY_INCLUDED")
        self.assertIsNone(treatment.published_amount.value_dollars)

    def test_generic_artifact_money_is_not_limited_by_scenario_budget_ceiling(self) -> None:
        value = PublishedMoneyValue.model_validate_json(
            json.dumps(
                {
                "availability": "AVAILABLE",
                "value_dollars": 2_000_000_000,
                "source_text": "$2,000,000,000",
                "unit": "USD",
                    "explanation": "Generic whole-dollar artifact value.",
                }
            ),
            strict=True,
        )
        self.assertEqual(value.value_dollars, 2_000_000_000)
        plan = self.plan_input()
        plan["available_budget_dollars"] = 1_000_000_001
        with self.assertRaises(ValidationError):
            PlanInput.model_validate(plan, strict=True)

    def test_benchmark_comparison_request_and_response_schemas_are_exported(self) -> None:
        names = {name for name, _ in SCHEMA_EXPORTS}
        self.assertIn("benchmark-comparison-request-1.0.0.schema.json", names)
        self.assertIn("benchmark-comparison-response-1.0.0.schema.json", names)

    def test_benchmark_comparison_contracts_accept_permitted_partial_output(self) -> None:
        request = BenchmarkComparisonRequest.model_validate(
            {
                "plan": self.plan_input(),
                "expected_benchmark_contract_version": BENCHMARK_CONTRACT_VERSION,
                "expected_benchmark_data_version": "m1-contract-test-1",
            },
            strict=True,
        )
        response_data = {
            "benchmark_contract_version": BENCHMARK_CONTRACT_VERSION,
            "benchmark_data_version": "m1-contract-test-1",
            "benchmark_source_id": "austin_2026_bond_initial_draft_2026_01_21",
            "evaluated_plan": self.evaluated_plan(),
            "published_allocation": {
                "availability": "AVAILABLE",
                "value_dollars": 125_000_000,
                "source_text": "$125,000,000",
                "unit": "USD",
                "explanation": "Published allocation is available.",
            },
            "city_included_count": {
                "availability": "MISSING",
                "reason_code": "benchmark:count_not_published",
                "explanation": "No supported count is available.",
            },
            "documented_divergences": ["Descriptive comparison only."],
        }
        parsed = BenchmarkComparisonResponseData.model_validate_json(
            json.dumps(response_data), strict=True
        )
        self.assertIsNone(request.plan.expected_fingerprint)
        self.assertIsNone(parsed.overlap)
        envelope = {
            "endpoint": "/api/v1/plans/evaluate",
            "status": "SUCCESS",
            "identity": {
                "request_id": "123e4567-e89b-42d3-a456-426614174000",
                "api_namespace": "/api/v1",
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": "m1-contract-test-1",
                "release_id": "local-test",
            },
            "data": {
                "current": {
                    "status": "VALID",
                    "evaluated_plan": self.evaluated_plan(),
                    "semantic_errors": [],
                }
            },
        }
        self.assertEqual(
            PlanEvaluationSuccessEnvelope.model_validate(envelope, strict=True).status,
            "SUCCESS",
        )

    def test_patterned_dictionary_schemas_forbid_unmatched_keys(self) -> None:
        def patterned_objects(value: object):
            if isinstance(value, dict):
                if "patternProperties" in value:
                    yield value
                for child in value.values():
                    yield from patterned_objects(child)
            elif isinstance(value, list):
                for child in value:
                    yield from patterned_objects(child)

        found = 0
        for schema_path in sorted((REPOSITORY_ROOT / "contracts/schemas").glob("*.json")):
            schema = json.loads(schema_path.read_text(encoding="utf-8"))
            for constrained_dictionary in patterned_objects(schema):
                found += 1
                self.assertIs(
                    constrained_dictionary.get("additionalProperties"),
                    False,
                    schema_path.name,
                )
        self.assertGreater(found, 0)

    def test_machine_source_authority_matches_registry_and_pinned_handoff(self) -> None:
        registry_path = REPOSITORY_ROOT / "data/metadata/source_registry.csv"
        with registry_path.open(newline="", encoding="utf-8") as handle:
            registry = {row["source_id"]: row for row in csv.DictReader(handle)}
        self.assertLessEqual(set(REGISTERED_SOURCE_IDENTITIES), set(registry))
        historical_fit = {
            "valid": "HISTORICALLY_VALID",
            "uncertain": "HISTORICAL_FIT_UNCERTAIN",
            "valid_as_dated_2021_snapshot": "HISTORICALLY_VALID",
            "valid_as_documentary_context_only": "HISTORICALLY_VALID",
        }
        for source_id, expected in REGISTERED_SOURCE_IDENTITIES.items():
            row = registry[source_id]
            self.assertEqual(expected.publisher, row["publisher"])
            self.assertEqual(expected.title, row["dataset_name"])
            self.assertEqual(expected.source_url, row["source_url"])
            self.assertEqual(expected.source_vintage, row["source_vintage"])
            self.assertEqual(expected.published_date, row["published_date"] or None)
            self.assertEqual(expected.retrieval_timestamp, row["retrieved_at"] or None)
            self.assertEqual(expected.sha256, row["checksum"].removeprefix("sha256:"))
            self.assertEqual(expected.historical_fit, historical_fit[row["historical_fit"]])
            self.assertEqual(expected.analytical_role, row["analytical_role"])
            self.assertTrue(row["license_notes"].startswith(expected.license_reuse_status))
        progress = (REPOSITORY_ROOT / "PROJECT_PROGRESS.md").read_text(encoding="utf-8")
        for source_id, expected in REGISTERED_SOURCE_IDENTITIES.items():
            if (
                source_id != "austin_rna_projects_layer_8_live"
                and expected.gcs_uri is not None
                and expected.gcs_generation is not None
            ):
                self.assertIn(
                    f"{expected.gcs_uri}#{expected.gcs_generation}",
                    progress,
                )
        receipt = json.loads(
            (
                REPOSITORY_ROOT
                / "data/metadata/source_snapshots/austin_rna_projects_layer_8_live/20260901T183323Z/gcs_receipt.json"
            ).read_text(encoding="utf-8")
        )
        feature_pin = next(
            item for item in receipt["objects"] if item["filename"] == "features.arcgis.json"
        )
        rna = REGISTERED_SOURCE_IDENTITIES["austin_rna_projects_layer_8_live"]
        self.assertEqual(feature_pin["gcs_uri"], rna.gcs_uri)
        self.assertEqual(str(feature_pin["generation"]), rna.gcs_generation)
        self.assertEqual(feature_pin["cloud_stream_sha256"].removeprefix("sha256:"), rna.sha256)

    def test_governed_identity_and_family_requests_match_canonical_csv(self) -> None:
        csv_path = (
            REPOSITORY_ROOT
            / "data/reconnaissance/city_austin/watershed_bond_projects/2025-11-21/projects.csv"
        )
        with csv_path.open(newline="", encoding="utf-8") as handle:
            rows = list(csv.DictReader(handle))
        semantic_rows = [
            "\x1f".join(
                (
                    row["source_id"],
                    row["source_pdf_page"],
                    row["source_table_row_order"],
                    row["map_label"],
                    row["subproject_id"],
                    row["project_name"],
                    row["current_funding_request_estimate_source"],
                    row["current_funding_request_estimate_dollars"],
                    row["council_districts_source"],
                )
            )
            for row in sorted(rows, key=lambda item: int(item["source_table_row_order"]))
        ]
        self.assertEqual(
            hashlib.sha256("\x1e".join(semantic_rows).encode("utf-8")).hexdigest(),
            GOVERNED_SOURCE_SEMANTIC_SHA256,
        )
        requests = {
            row["subproject_id"]: int(row["current_funding_request_estimate_dollars"])
            for row in rows
            if row["subproject_id"] in ACTIVE_FAMILY_PROJECT_IDS
        }
        self.assertEqual(requests, dict(ACTIVE_FAMILY_REQUEST_DOLLARS))


if __name__ == "__main__":
    unittest.main()
