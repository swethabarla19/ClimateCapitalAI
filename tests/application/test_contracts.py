from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

from pydantic import ValidationError

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
BACKEND_ROOT = REPOSITORY_ROOT / "backend"
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from climatecapital.contracts.api import ApiErrorEnvelope  # noqa: E402
from climatecapital.contracts.artifacts import CatalogArtifact  # noqa: E402
from climatecapital.contracts.common import EvidenceItem  # noqa: E402
from climatecapital.contracts.gemini import GeminiExplainRequest  # noqa: E402
from climatecapital.contracts.plans import (  # noqa: E402
    EvaluatedPlan,
    PlanInput,
    PlanMembershipContractError,
    validate_plan_membership_contract,
)
from climatecapital.contracts.schema_export import SCHEMA_EXPORTS, render_schema  # noqa: E402
from climatecapital.contracts.session import BrowserSessionState  # noqa: E402
from climatecapital.contracts.versions import (  # noqa: E402
    ACTIVE_FAMILY_PROJECT_IDS,
    API_NAMESPACE,
    BENCHMARK_CONTRACT_VERSION,
    BROWSER_SESSION_CONTRACT_VERSION,
    CATALOG_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    GEMINI_EXPLAIN_CONTRACT_VERSION,
    MAP_CONTEXT_CONTRACT_VERSION,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)
from tests.release.bundle_factory import build_catalog, canonical_bytes  # noqa: E402


def validate_json(model: type, value: dict):
    return model.model_validate_json(canonical_bytes(value), strict=True)


class VersionAndSchemaContractTests(unittest.TestCase):
    def test_initial_versions_and_api_namespace_are_exact(self) -> None:
        self.assertEqual(RELEASE_MANIFEST_CONTRACT_VERSION, "p0-release-manifest/1.0.0")
        self.assertEqual(CATALOG_CONTRACT_VERSION, "p0-catalog/1.0.0")
        self.assertEqual(MAP_CONTEXT_CONTRACT_VERSION, "p0-map-context/1.0.0")
        self.assertEqual(BENCHMARK_CONTRACT_VERSION, "p0-benchmark/1.0.0")
        self.assertEqual(FUNDING_PLAN_CONTRACT_VERSION, "p0-funding-plan/1.0.0")
        self.assertEqual(BROWSER_SESSION_CONTRACT_VERSION, "p0-browser-session/1.0.0")
        self.assertEqual(GEMINI_EXPLAIN_CONTRACT_VERSION, "p0-gemini-explain/1.0.0")
        self.assertEqual(API_NAMESPACE, "/api/v1")

    def test_python_consumers_do_not_duplicate_version_literals(self) -> None:
        version_literals = (
            "p0-release-manifest/1.0.0",
            "p0-catalog/1.0.0",
            "p0-map-context/1.0.0",
            "p0-benchmark/1.0.0",
            "p0-funding-plan/1.0.0",
            "p0-browser-session/1.0.0",
            "p0-gemini-explain/1.0.0",
        )
        source_files = list((BACKEND_ROOT / "climatecapital").rglob("*.py"))
        for literal in version_literals:
            occurrences = sum(path.read_text(encoding="utf-8").count(literal) for path in source_files)
            self.assertEqual(occurrences, 1, literal)

    def test_tracked_json_schemas_are_exact_generated_outputs(self) -> None:
        schema_dir = REPOSITORY_ROOT / "contracts" / "schemas"
        self.assertEqual(
            {path.name for path in schema_dir.glob("*.schema.json")},
            {filename for filename, _ in SCHEMA_EXPORTS},
        )
        for filename, model in SCHEMA_EXPORTS:
            payload = (schema_dir / filename).read_bytes()
            self.assertEqual(payload, render_schema(filename, model))
            schema = json.loads(payload)
            self.assertEqual(
                schema["$schema"], "https://json-schema.org/draft/2020-12/schema"
            )
            if "additionalProperties" in schema:
                self.assertFalse(schema["additionalProperties"])
            else:
                self.assertFalse(schema["unevaluatedProperties"])


class StrictPrimitiveAndPlanContractTests(unittest.TestCase):
    def valid_plan_input(self) -> dict:
        return {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": "m1-contract-test-1",
            "available_budget_dollars": 125_000_000,
            "project_ids": ["5789.075"],
            "expected_fingerprint": None,
        }

    def test_plan_input_rejects_client_authoritative_fields_and_unknown_fields(self) -> None:
        for field, value in (
            ("included_total_dollars", 35_000_000),
            ("governed_request_dollars", 35_000_000),
            ("score", 1),
            ("geometry", {"type": "Point", "coordinates": [-97.7, 30.2]}),
        ):
            candidate = self.valid_plan_input()
            candidate[field] = value
            with self.subTest(field=field), self.assertRaises(ValidationError):
                validate_json(PlanInput, candidate)

    def test_money_and_project_id_primitives_are_strict(self) -> None:
        invalid_cases = (
            ("available_budget_dollars", 125_000_000.0),
            ("available_budget_dollars", True),
            ("available_budget_dollars", -1),
            ("available_budget_dollars", 1_000_000_001),
            ("project_ids", [5789.075]),
            ("project_ids", ["5789.75"]),
            ("project_ids", ["5789.075", "5789.075"]),
        )
        for field, value in invalid_cases:
            candidate = self.valid_plan_input()
            candidate[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValidationError):
                validate_json(PlanInput, candidate)

    def test_valid_zero_project_evaluated_result_is_not_an_error(self) -> None:
        result = {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": "m1-contract-test-1",
            "included_project_ids": [],
            "not_included_active_family_project_ids": list(ACTIVE_FAMILY_PROJECT_IDS),
            "included_count": 0,
            "included_governed_requests": [],
            "included_total_dollars": 0,
            "available_budget_dollars": 0,
            "remainder_dollars": 0,
            "overage_dollars": None,
            "confirmation_status": "VALID",
            "warnings": [],
            "plan_fingerprint": "0" * 64,
            "fingerprint_verification": {
                "expected_fingerprint": None,
                "matches": None,
            },
        }
        parsed = validate_json(EvaluatedPlan, result)
        self.assertEqual(parsed.confirmation_status, "VALID")
        self.assertEqual(parsed.included_count, 0)

    def test_membership_contract_uses_family_fact_not_geometry(self) -> None:
        catalog = validate_json(CatalogArtifact, build_catalog())
        missing_geometry_family_id = "5789.075"
        geometry_backed_out_of_family_id = "5754.089"
        self.assertEqual(
            validate_plan_membership_contract(catalog, [missing_geometry_family_id]),
            (missing_geometry_family_id,),
        )
        with self.assertRaises(PlanMembershipContractError) as caught:
            validate_plan_membership_contract(catalog, [geometry_backed_out_of_family_id])
        self.assertEqual(caught.exception.code, "OUT_OF_FAMILY_PROJECT_ID")


class EvidenceStateContractTests(unittest.TestCase):
    def available_zero_item(self) -> dict:
        return {
            "evidence_id": "test:zero",
            "evidence_type": "FEMA_CURRENT_HAZARD_CONTEXT",
            "evidence_role": "CONTEXTUAL_EVIDENCE",
            "fact_kind": None,
            "availability": "AVAILABLE",
            "reason_code": None,
            "explanation": "A governed source establishes numeric zero.",
            "value": 0,
            "unit": "count",
            "category": None,
            "source_ids": ["test-source"],
            "source_vintage": "2026 test",
            "historical_fit": "CURRENT_CONTEXT_ONLY",
            "association_method": "test association",
            "transformation_version": "test/1",
            "coverage_scope": "test",
            "limitations": ["test only"],
            "confidence": None,
            "confidence_meaning": None,
            "public_label": "Test zero",
            "public_disclaimer": "Context only.",
        }

    def test_numeric_zero_requires_available_and_is_not_missing(self) -> None:
        parsed = validate_json(EvidenceItem, self.available_zero_item())
        self.assertEqual(parsed.value, 0)
        missing = self.available_zero_item()
        missing.update(availability="MISSING", reason_code="missing:test")
        with self.assertRaises(ValidationError):
            validate_json(EvidenceItem, missing)

    def test_non_available_states_require_reason_and_forbid_values(self) -> None:
        for availability in (
            "MISSING",
            "UNSUPPORTED",
            "NOT_APPLICABLE",
            "NOT_EVALUATED_FIXTURE",
        ):
            candidate = self.available_zero_item()
            candidate.update(
                evidence_role="UNAVAILABLE_UNSUPPORTED",
                availability=availability,
                reason_code=None,
                value=None,
                unit=None,
            )
            with self.subTest(availability=availability), self.assertRaises(ValidationError):
                validate_json(EvidenceItem, candidate)


class SessionApiAndGeminiContractTests(unittest.TestCase):
    def test_browser_session_forbids_persistence_and_benchmark_state(self) -> None:
        plan = {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": "m1-contract-test-1",
            "available_budget_dollars": 125_000_000,
            "project_ids": [],
            "expected_fingerprint": None,
        }
        state = {
            "contract_version": BROWSER_SESSION_CONTRACT_VERSION,
            "validated_identity": {
                "data_version": "m1-contract-test-1",
                "manifest_sha256": "0" * 64,
                "release_id": "local-test",
                "release_manifest_contract_version": RELEASE_MANIFEST_CONTRACT_VERSION,
            },
            "presentation": {
                "route": "EXPLORE",
                "search_text": "",
                "filter_ids": [],
                "sort": "SOURCE_ORDER",
                "map_extent": None,
                "visible_layers": ["rna_current_project_display"],
                "selected_project_id": None,
                "list_position": 0,
            },
            "working_plan": plan,
            "session_reference_plan": None,
            "what_if": None,
            "current_confirmed_plan": None,
            "dirty_attempt": None,
            "pending_gemini_proposal": None,
            "reviewed_draft": None,
            "local_request_states": [],
            "visible_explanation": None,
        }
        validate_json(BrowserSessionState, state)
        for forbidden_field, value in (
            ("historical_city_recommendation", {"project_ids": []}),
            ("server_session_key", "server-state"),
            ("user_id", "analyst"),
            ("durable_scenario_id", "persisted"),
        ):
            candidate = dict(state)
            candidate[forbidden_field] = value
            with self.subTest(field=forbidden_field), self.assertRaises(ValidationError):
                validate_json(BrowserSessionState, candidate)

    def test_api_error_envelope_rejects_unknown_content(self) -> None:
        envelope = {
            "status": "ERROR",
            "identity": {
                "request_id": "123e4567-e89b-42d3-a456-426614174000",
                "api_namespace": "/api/v1",
                "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
                "data_version": "m1-contract-test-1",
                "release_id": "local-test",
            },
            "error": {
                "error_code": "MALFORMED_REQUEST",
                "message": "Request shape is invalid.",
                "field_path": ["current"],
                "retryable": False,
                "stack_trace": "forbidden",
            },
        }
        with self.assertRaises(ValidationError):
            validate_json(ApiErrorEnvelope, envelope)

    def test_gemini_request_accepts_references_not_client_grounding(self) -> None:
        request = {
            "contract_version": GEMINI_EXPLAIN_CONTRACT_VERSION,
            "data_version": "m1-contract-test-1",
            "context_type": "PROJECT",
            "project_ids": ["5789.075"],
            "current_plan": None,
            "reference_plan": None,
            "expected_fingerprints": None,
            "user_question": "What evidence is available?",
        }
        validate_json(GeminiExplainRequest, request)
        request["grounding_facts"] = {"priority": 99}
        with self.assertRaises(ValidationError):
            validate_json(GeminiExplainRequest, request)


if __name__ == "__main__":
    unittest.main()
