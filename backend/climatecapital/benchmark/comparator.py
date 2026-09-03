"""One-way comparison from a freshly evaluated plan to the City benchmark."""

from __future__ import annotations

from climatecapital.contracts.artifacts import (
    BenchmarkArtifact,
    PublishedMoneyValue,
)
from climatecapital.contracts.common import Availability
from climatecapital.contracts.plans import (
    BenchmarkComparisonResponseData,
    BenchmarkOverlap,
    EvaluatedPlan,
)

_CITY_INCLUDED = {"HISTORICALLY_RECOMMENDED", "CITY_INCLUDED"}


def compare_plan_to_benchmark(
    benchmark: BenchmarkArtifact,
    plan: EvaluatedPlan,
) -> BenchmarkComparisonResponseData:
    """Compare without allowing benchmark data to affect plan evaluation.

    Overlap is emitted only when the benchmark has explicit City-included
    treatment for governed project IDs and every overlapping published amount
    is available. Otherwise overlap is omitted rather than inferred.
    """

    included = set(plan.included_project_ids)
    city_entries = []
    for entry in benchmark.published_project_treatments:
        project_id = entry.governed_project_id
        treatment = entry.city_treatment
        if (
            project_id is not None
            and project_id in included
            and treatment.availability == Availability.AVAILABLE
            and treatment.value in _CITY_INCLUDED
        ):
            city_entries.append(entry)

    overlap = None
    if city_entries and all(
        entry.published_amount.availability == Availability.AVAILABLE
        and entry.published_amount.value_dollars is not None
        for entry in city_entries
    ):
        overlap_ids = sorted(
            entry.governed_project_id
            for entry in city_entries
            if entry.governed_project_id is not None
        )
        total = sum(
            entry.published_amount.value_dollars or 0
            for entry in city_entries
        )
        overlap = BenchmarkOverlap(
            project_ids=overlap_ids,
            project_count=len(overlap_ids),
            published_amount=PublishedMoneyValue(
                availability=Availability.AVAILABLE,
                value_dollars=total,
                source_text=f"${total:,}",
                unit="USD",
                reason_code=None,
                explanation=(
                    "Sum of explicitly published City amounts for governed "
                    "projects that are both City-included and present in the "
                    "freshly evaluated analyst plan."
                ),
            ),
        )

    divergences = list(benchmark.limitations)
    if overlap is None:
        divergences.append(
            "Project-level overlap dollars are omitted unless explicit City "
            "treatment and published amount semantics support the calculation."
        )

    return BenchmarkComparisonResponseData(
        benchmark_contract_version=benchmark.contract_version,
        benchmark_data_version=benchmark.data_version,
        benchmark_source_id=benchmark.benchmark_identity.source_id,
        evaluated_plan=plan,
        published_allocation=(
            benchmark.published_portfolio_summary.published_allocation
        ),
        city_included_count=(
            benchmark.published_portfolio_summary.city_included_count
        ),
        overlap=overlap,
        documented_divergences=divergences,
    )
