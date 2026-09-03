from __future__ import annotations

import itertools
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


def plan_input(
    catalog: CatalogArtifact,
    project_ids: list[str],
    *,
    budget: int = 1_000_000_000,
    expected_fingerprint: str | None = None,
) -> PlanInput:
    return PlanInput(
        contract_version=FUNDING_PLAN_CONTRACT_VERSION,
        data_version=catalog.data_version,
        available_budget_dollars=budget,
        project_ids=project_ids,
        expected_fingerprint=expected_fingerprint,
    )


class PlanEvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = fixture_catalog()
        cls.family_ids = list(ACTIVE_FAMILY_PROJECT_IDS)
        cls.requests = {
            project.project_id: project.governed_request_dollars
            for project in cls.catalog.projects
        }

    def test_zero_project_plan_is_valid(self) -> None:
        result = evaluate_plan(
            self.catalog,
            plan_input(self.catalog, [], budget=0),
        )

        self.assertEqual(result.status, "VALID")
        self.assertIsNotNone(result.evaluated_plan)

        evaluated = result.evaluated_plan
        assert evaluated is not None

        self.assertEqual(evaluated.included_project_ids, [])
        self.assertEqual(evaluated.included_count, 0)
        self.assertEqual(evaluated.included_total_dollars, 0)
        self.assertEqual(evaluated.remainder_dollars, 0)
        self.assertIsNone(evaluated.overage_dollars)

    def test_all_4096_active_family_subsets(self) -> None:
        tested = 0

        for subset_size in range(len(self.family_ids) + 1):
            for subset_tuple in itertools.combinations(
                self.family_ids,
                subset_size,
            ):
                subset = list(subset_tuple)
                expected_total = sum(
                    self.requests[project_id]
                    for project_id in subset
                )

                result = evaluate_plan(
                    self.catalog,
                    plan_input(self.catalog, subset),
                )

                self.assertEqual(result.status, "VALID")
                self.assertIsNotNone(result.evaluated_plan)

                evaluated = result.evaluated_plan
                assert evaluated is not None

                self.assertEqual(
                    evaluated.included_project_ids,
                    sorted(subset),
                )
                self.assertEqual(
                    evaluated.included_count,
                    len(subset),
                )
                self.assertEqual(
                    evaluated.included_total_dollars,
                    expected_total,
                )
                self.assertEqual(
                    evaluated.available_budget_dollars,
                    1_000_000_000,
                )
                self.assertEqual(
                    evaluated.remainder_dollars,
                    1_000_000_000 - expected_total,
                )
                self.assertIsNone(evaluated.overage_dollars)

                request_map = {
                    item.project_id: item.governed_request_dollars
                    for item in evaluated.included_governed_requests
                }
                self.assertEqual(
                    request_map,
                    {
                        project_id: self.requests[project_id]
                        for project_id in sorted(subset)
                    },
                )

                tested += 1

        self.assertEqual(len(self.family_ids), 12)
        self.assertEqual(tested, 4096)

    def test_full_family_exact_total(self) -> None:
        result = evaluate_plan(
            self.catalog,
            plan_input(
                self.catalog,
                self.family_ids,
                budget=143_005_000,
            ),
        )

        self.assertEqual(result.status, "VALID")
        evaluated = result.evaluated_plan
        assert evaluated is not None

        self.assertEqual(evaluated.included_count, 12)
        self.assertEqual(
            evaluated.included_total_dollars,
            143_005_000,
        )
        self.assertEqual(evaluated.remainder_dollars, 0)

    def test_over_budget_plan_returns_exact_overage(self) -> None:
        result = evaluate_plan(
            self.catalog,
            plan_input(
                self.catalog,
                self.family_ids,
                budget=143_004_999,
            ),
        )

        self.assertEqual(result.status, "OVER_BUDGET")
        evaluated = result.evaluated_plan
        assert evaluated is not None

        self.assertEqual(
            evaluated.included_total_dollars,
            143_005_000,
        )
        self.assertEqual(evaluated.overage_dollars, 1)
        self.assertIsNone(evaluated.remainder_dollars)

    def test_unknown_project_id_is_invalid(self) -> None:
        result = evaluate_plan(
            self.catalog,
            plan_input(self.catalog, ["9999.999"]),
        )

        self.assertEqual(result.status, "INVALID")
        self.assertIsNone(result.evaluated_plan)
        self.assertEqual(
            [error.error_code for error in result.semantic_errors],
            ["UNKNOWN_PROJECT_ID"],
        )

    def test_out_of_family_project_is_invalid(self) -> None:
        out_of_family = next(
            project.project_id
            for project in self.catalog.projects
            if not project.p0_family.member
        )

        result = evaluate_plan(
            self.catalog,
            plan_input(self.catalog, [out_of_family]),
        )

        self.assertEqual(result.status, "INVALID")
        self.assertEqual(
            [error.error_code for error in result.semantic_errors],
            ["OUT_OF_FAMILY_PROJECT_ID"],
        )

    def test_duplicate_project_id_is_rejected(self) -> None:
        project_id = self.family_ids[0]

        with self.assertRaises(ValidationError):
            plan_input(
                self.catalog,
                [project_id, project_id],
            )

    def test_fingerprint_is_order_independent(self) -> None:
        ids = self.family_ids[:3]

        first = evaluate_plan(
            self.catalog,
            plan_input(self.catalog, ids),
        )
        second = evaluate_plan(
            self.catalog,
            plan_input(self.catalog, list(reversed(ids))),
        )

        assert first.evaluated_plan is not None
        assert second.evaluated_plan is not None

        self.assertEqual(
            first.evaluated_plan.plan_fingerprint,
            second.evaluated_plan.plan_fingerprint,
        )
        self.assertEqual(
            first.evaluated_plan.included_project_ids,
            sorted(ids),
        )
        self.assertEqual(
            second.evaluated_plan.included_project_ids,
            sorted(ids),
        )

    def test_expected_fingerprint_mismatch_is_visible(self) -> None:
        project_id = self.family_ids[0]

        result = evaluate_plan(
            self.catalog,
            plan_input(
                self.catalog,
                [project_id],
                expected_fingerprint="0" * 64,
            ),
        )

        self.assertEqual(result.status, "VALID")
        evaluated = result.evaluated_plan
        assert evaluated is not None

        self.assertEqual(
            evaluated.fingerprint_verification.expected_fingerprint,
            "0" * 64,
        )
        self.assertFalse(
            evaluated.fingerprint_verification.matches,
        )

    def test_current_reference_comparison(self) -> None:
        first_id, second_id = self.family_ids[:2]

        request = PlanEvaluationRequest(
            current=plan_input(
                self.catalog,
                [first_id, second_id],
                budget=125_000_000,
            ),
            reference=plan_input(
                self.catalog,
                [first_id],
                budget=125_000_000,
            ),
        )

        result = evaluate_plan_request(
            self.catalog,
            request,
        )

        self.assertEqual(result.current.status, "VALID")
        self.assertIsNotNone(result.reference)

        assert result.reference is not None
        self.assertEqual(result.reference.status, "VALID")

        comparison = result.comparison
        self.assertIsNotNone(comparison)
        assert comparison is not None

        self.assertEqual(
            comparison.entering.project_ids,
            [second_id],
        )
        self.assertEqual(
            comparison.entering.governed_request_total_dollars,
            self.requests[second_id],
        )
        self.assertEqual(
            comparison.leaving.project_ids,
            [],
        )
        self.assertEqual(
            comparison.unchanged_project_ids,
            [first_id],
        )
        self.assertEqual(
            comparison.included_count_difference,
            1,
        )
        self.assertEqual(
            comparison.included_total_difference_dollars,
            self.requests[second_id],
        )

    def test_invalid_reference_preserves_valid_current(self) -> None:
        current_id = self.family_ids[0]

        request = PlanEvaluationRequest(
            current=plan_input(
                self.catalog,
                [current_id],
            ),
            reference=plan_input(
                self.catalog,
                ["9999.999"],
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

        self.assertEqual(result.reference.status, "INVALID")
        self.assertEqual(
            [error.error_code for error in result.reference.semantic_errors],
            ["UNKNOWN_PROJECT_ID"],
        )
        self.assertIsNone(result.comparison)


if __name__ == "__main__":
    unittest.main()
