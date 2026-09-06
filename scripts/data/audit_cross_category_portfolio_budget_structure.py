#!/usr/bin/env python3
"""Audit budget scope for M3.7D cross-category portfolio methodology."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

HISTORICAL_FULL_PACKAGE_CATEGORY_DOLLARS = {
    "Transportation": 251_000_000,
    "Parks & Open Space": 140_000_000,
    "Watershed": 160_000_000,
    "Community Facilities": 149_000_000,
}

EXPECTED_ANALYTICAL_PROJECT_COUNT = 106
EXPECTED_MODEL_REQUEST_TOTAL = 1_973_520_000
EXPECTED_PROJECT_LEVEL_RECOMMENDATION_TOTAL = 332_000_000
EXPECTED_FULL_PACKAGE_TOTAL = 700_000_000


def money(value: int) -> str:
    return f"${value:,.0f}"


def main() -> int:
    artifact = json.loads(
        RECONCILIATION_PATH.read_text(
            encoding="utf-8"
        )
    )

    records = artifact["records"]

    if len(records) != EXPECTED_ANALYTICAL_PROJECT_COUNT:
        raise RuntimeError(
            "Expected "
            f"{EXPECTED_ANALYTICAL_PROJECT_COUNT} "
            "analytical projects; "
            f"found {len(records)}."
        )

    category = defaultdict(
        lambda: {
            "project_count": 0,
            "request_total": 0,
            "recommendation_count": 0,
            "recommendation_total": 0,
        }
    )

    for record in records:
        presentation_category = (
            record["presentation_category"]
        )

        stats = category[
            presentation_category
        ]

        stats["project_count"] += 1

        stats["request_total"] += int(
            record["model_request_dollars"]
        )

        recommendation = record.get(
            "january_recommendation_dollars"
        )

        if recommendation is not None:
            stats[
                "recommendation_count"
            ] += 1

            stats[
                "recommendation_total"
            ] += int(recommendation)

    model_request_total = sum(
        int(record["model_request_dollars"])
        for record in records
    )

    project_recommendation_total = sum(
        int(record["january_recommendation_dollars"])
        for record in records
        if record.get("january_recommendation_dollars")
        is not None
    )

    full_package_total = sum(
        HISTORICAL_FULL_PACKAGE_CATEGORY_DOLLARS.values()
    )

    if model_request_total != EXPECTED_MODEL_REQUEST_TOTAL:
        raise RuntimeError(
            "Governed model-request total changed: "
            f"{money(model_request_total)}"
        )

    if (
        project_recommendation_total
        != EXPECTED_PROJECT_LEVEL_RECOMMENDATION_TOTAL
    ):
        raise RuntimeError(
            "Project-level recommendation total changed: "
            f"{money(project_recommendation_total)}"
        )

    if full_package_total != EXPECTED_FULL_PACKAGE_TOTAL:
        raise RuntimeError(
            "Historical full-package total changed: "
            f"{money(full_package_total)}"
        )

    outside_project_cohort_total = (
        full_package_total
        - project_recommendation_total
    )

    print(
        "M3.7D-A CROSS-CATEGORY "
        "PORTFOLIO BUDGET-SCOPE AUDIT"
    )
    print("=" * 88)

    print()
    print("GOVERNED ANALYTICAL COHORT")
    print("-" * 88)

    print(
        "Analytical projects:",
        len(records),
    )

    print(
        "Total governed project requests:",
        money(model_request_total),
    )

    print()
    print(
        "HISTORICAL JANUARY 21 "
        "INITIAL RECOMMENDATION"
    )
    print("-" * 88)

    print(
        "Full historical package:",
        money(full_package_total),
    )

    print(
        "Recommendation attached to "
        "106 analytical projects:",
        money(project_recommendation_total),
    )

    print(
        "Historical recommendation outside "
        "the 106-project analytical cohort:",
        money(outside_project_cohort_total),
    )

    print()
    print("CATEGORY RECONCILIATION")
    print("-" * 88)

    header = (
        f"{'Category':24}"
        f"{'Projects':>10}"
        f"{'Requests':>18}"
        f"{'Hist. Projects':>16}"
        f"{'Project Rec.':>18}"
        f"{'Full Package':>18}"
        f"{'Outside Cohort':>18}"
    )

    print(header)
    print("-" * len(header))

    categories = (
        "Transportation",
        "Parks & Open Space",
        "Watershed",
        "Community Facilities",
    )

    outside_by_category = {}

    for name in categories:
        stats = category[name]

        full_package = (
            HISTORICAL_FULL_PACKAGE_CATEGORY_DOLLARS[name]
        )

        outside_cohort = (
            full_package
            - stats["recommendation_total"]
        )

        outside_by_category[name] = outside_cohort

        print(
            f"{name:24}"
            f"{stats['project_count']:>10}"
            f"{money(stats['request_total']):>18}"
            f"{stats['recommendation_count']:>16}"
            f"{money(stats['recommendation_total']):>18}"
            f"{money(full_package):>18}"
            f"{money(outside_cohort):>18}"
        )

    if (
        sum(outside_by_category.values())
        != outside_project_cohort_total
    ):
        raise RuntimeError(
            "Category reconciliation does not "
            "reproduce outside-cohort total."
        )

    print()
    print("BUDGET-AUTHORITY QUESTIONS FOR M3.7D")
    print("-" * 88)

    print(
        "1. $700M is the full historical "
        "Initial Draft Recommendation package."
    )

    print(
        "2. $332M is the historical recommendation "
        "attached to the 106 analytical projects."
    )

    print(
        "3. $368M of the historical package lies "
        "outside the 106-project analytical cohort."
    )

    print(
        "4. Historical category allocations are "
        "NOT automatically model constraints."
    )

    print(
        "5. Historical project recommendation "
        "membership remains benchmark/outcome-only."
    )

    print(
        "6. M3.7D must separately authorize the "
        "model budget and any category constraints."
    )

    print()
    print(
        "RESULT: budget scope reconciled; "
        "no portfolio constraint authorized by this audit."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
