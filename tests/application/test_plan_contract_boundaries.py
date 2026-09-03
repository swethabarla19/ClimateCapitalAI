from __future__ import annotations

import unittest

from pydantic import ValidationError

from climatecapital.contracts.artifacts import CatalogArtifact
from climatecapital.contracts.plans import PlanEvaluationRequest, PlanInput
from climatecapital.contracts.versions import (
    ACTIVE_FAMILY_PROJECT_IDS,
    FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.plans.evaluator import evaluate_plan, evaluate_plan_request
from tests.release.bundle_factory import build_catalog, canonical_bytes


def fixture_catalog() -> CatalogArtifact:
    return CatalogArtifact.model_validate_json(
        canonical_bytes(build_catalog()),
        strict=True,
    )


def make_plan(
    catalog: CatalogArtifact,
    project_ids: list[str],
    *,
    budget: int = 125_000_000,
    data_version: str | None = None,
    expected_fingerprint: str | None = None,
) -> PlanInput:
    return PlanInput(
        contract_version=FUNDING_PLAN_CONTRACT_VERSION,
        data_version=data_version or catalog.data_version,
        available_budget_dollars=budget,
        project_ids=project_ids,
        expected_fingerprint=expected_fingerprint,
    )


class PlanContractBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = fixture_catalog()
        cls.family_ids = list(ACTIVE_FAMILY_PROJECT_IDS)

    def test_float_budget_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            PlanInput(
                contract_version=FUNDING_PLAN_CONTRACT_VERSION,
                data_version=self.catalog.data_version,
                available_budget_dollars=125_000_000.0,
                project_ids=[],
                expected_fingerprint=None,
            )

    def test_negative_budget_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            make_plan(
                self.catalog,
                [],
                budget=-1,
            )

    def test_budget_above_one_billion_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            make_plan(
                self.catalog,
                [],
                budget=1_000_000_001,
            )

    def test_numeric_project_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            PlanInput(
                contract_version=FUNDING_PLAN_CONTRACT_VERSION,
                data_version=self.catalog.data_version,
                available_budget_dollars=125_000_000,
                project_ids=[5789.075],
                expected_fingerprint=None,
            )

    def test_malformed_project_id_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            make_plan(
                self.catalog,
                ["5789.75"],
            )

    def test_more_than_twelve_project_ids_is_rejected(self) -> None:
        too_many_ids = [
            f"9999.{index:03d}"
            for index in range(13)
        ]

        with self.assertRaises(ValidationError):
            make_plan(
                self.catalog,
                too_many_ids,
            )

    def test_unknown_input_field_is_rejected(self) -> None:
        payload = {
            "contract_version": FUNDING_PLAN_CONTRACT_VERSION,
            "data_version": self.catalog.data_version,
            "available_budget_dollars": 125_000_000,
            "project_ids": [],
            "expected_fingerprint": None,
            "client_computed_total": 123,
        }

        with self.assertRaises(ValidationError):
            PlanInput.model_validate(
                payload,
                strict=True,
            )

    def test_wrong_contract_version_is_rejected(self) -> None:
        with self.assertRaises(ValidationError):
            PlanInput(
                contract_version="p0-funding-plan/999.0.0",
                data_version=self.catalog.data_version,
                available_budget_dollars=125_000_000,
                project_ids=[],
                expected_fingerprint=None,
            )

    def test_stale_data_version_returns_typed_invalid_result(self) -> None:
        stale_version = self.catalog.data_version + "-stale"

        result = evaluate_plan(
            self.catalog,
            make_plan(
                self.catalog,
                [self.family_ids[0]],
                data_version=stale_version,
            ),
        )

        self.assertEqual(result.status, "INVALID")
        self.assertIsNone(result.evaluated_plan)
        self.assertEqual(
            [error.error_code for error in result.semantic_errors],
            ["DATA_VERSION_CONFLICT"],
        )

    def test_matching_expected_fingerprint_is_visible(self) -> None:
        project_ids = self.family_ids[:2]

        first = evaluate_plan(
            self.catalog,
            make_plan(
                self.catalog,
                project_ids,
            ),
        )

        self.assertEqual(first.status, "VALID")
        assert first.evaluated_plan is not None

        fingerprint = first.evaluated_plan.plan_fingerprint

        second = evaluate_plan(
            self.catalog,
            make_plan(
                self.catalog,
                project_ids,
                expected_fingerprint=fingerprint,
            ),
        )

        self.assertEqual(second.status, "VALID")
        assert second.evaluated_plan is not None

        self.assertEqual(
            second.evaluated_plan.fingerprint_verification.expected_fingerprint,
            fingerprint,
        )
        self.assertTrue(
            second.evaluated_plan.fingerprint_verification.matches,
        )

    def test_mismatched_current_reference_data_versions_are_rejected(self) -> None:
        stale_version = self.catalog.data_version + "-stale"

        with self.assertRaises(ValidationError):
            PlanEvaluationRequest(
                current=make_plan(
                    self.catalog,
                    [self.family_ids[0]],
                ),
                reference=make_plan(
                    self.catalog,
                    [self.family_ids[0]],
                    data_version=stale_version,
                ),
            )

    def test_over_budget_reference_preserves_valid_current(self) -> None:
        request = PlanEvaluationRequest(
            current=make_plan(
                self.catalog,
                [],
                budget=125_000_000,
            ),
            reference=make_plan(
                self.catalog,
                self.family_ids,
                budget=143_004_999,
            ),
        )

        result = evaluate_plan_request(
            self.catalog,
            request,
        )

        self.assertEqual(result.current.status, "VALID")
        self.assertIsNotNone(result.current.evaluated_plan)

        self.assertIsNotNone(result.reference)
        assert result.reference is not None

        self.assertEqual(
            result.reference.status,
            "OVER_BUDGET",
        )
        self.assertIsNotNone(
            result.reference.evaluated_plan,
        )
        self.assertIsNone(result.comparison)


if __name__ == "__main__":
    unittest.main()
