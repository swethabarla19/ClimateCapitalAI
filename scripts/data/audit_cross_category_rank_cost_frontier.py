#!/usr/bin/env python3
"""Audit PRB rank-tier cost frontiers for M3.7D portfolio methodology."""

from __future__ import annotations

import json
from collections import defaultdict
from decimal import Decimal
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]

PRIORITY_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "funding_priority"
    / "cross-category-prb-funding-priority.json"
)

RECONCILIATION_PATH = (
    ROOT
    / "data"
    / "governed"
    / "cross_category"
    / "reconciliation"
    / "cross-category-prb-reconciliation.json"
)

BUDGETS = {
    "HISTORICAL_MATCHED_PROJECT_COHORT": 332_000_000,
    "HISTORICAL_FULL_PACKAGE": 700_000_000,
    "HISTORICAL_CITYWIDE_CAPACITY_CEILING": 750_000_000,
}

EXPECTED_COUNT = 106
EXPECTED_REQUEST_TOTAL = 1_973_520_000


def money(value: int) -> str:
    return f"${value:,.0f}"


def score_text(value: Decimal) -> str:
    if value == value.to_integral():
        return str(int(value))
    return format(value, "f")


def main() -> int:
    priority = json.loads(
        PRIORITY_PATH.read_text(encoding="utf-8")
    )

    reconciliation = json.loads(
        RECONCILIATION_PATH.read_text(encoding="utf-8")
    )

    priority_records = priority["records"]
    reconciliation_records = reconciliation["records"]

    if len(priority_records) != EXPECTED_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_COUNT} priority records; "
            f"found {len(priority_records)}."
        )

    if len(reconciliation_records) != EXPECTED_COUNT:
        raise RuntimeError(
            f"Expected {EXPECTED_COUNT} reconciliation records; "
            f"found {len(reconciliation_records)}."
        )

    requests = {
        row["decision_unit_id"]: int(row["model_request_dollars"])
        for row in reconciliation_records
    }

    missing = [
        row["decision_unit_id"]
        for row in priority_records
        if row["decision_unit_id"] not in requests
    ]

    if missing:
        raise RuntimeError(
            "Priority records missing governed request values: "
            + ", ".join(missing)
        )

    request_total = sum(requests.values())

    if request_total != EXPECTED_REQUEST_TOTAL:
        raise RuntimeError(
            "Governed request total changed: "
            f"{money(request_total)}"
        )

    groups = defaultdict(
        lambda: {
            "rank": None,
            "projects": [],
            "group_cost": 0,
        }
    )

    for row in priority_records:
        score = Decimal(str(row["funding_priority_score"]))
        group = groups[score]

        group["rank"] = row["funding_priority_rank"]
        group["projects"].append(
            (
                row["decision_unit_id"],
                row["presentation_category"],
                requests[row["decision_unit_id"]],
            )
        )
        group["group_cost"] += requests[
            row["decision_unit_id"]
        ]

    ordered_scores = sorted(
        groups,
        reverse=True,
    )

    print("M3.7D-B PRB RANK-TIER COST FRONTIER")
    print("=" * 100)
    print()
    print(
        "This audit does NOT select a portfolio. "
        "It shows where budget boundaries intersect substantive PRB ties."
    )
    print()

    header = (
        f"{'Rank':>6}"
        f"{'Score':>8}"
        f"{'Projects':>10}"
        f"{'Tier Cost':>18}"
        f"{'Cumulative Cost':>20}"
    )

    print(header)
    print("-" * len(header))

    cumulative = 0

    for score in ordered_scores:
        group = groups[score]
        cumulative += group["group_cost"]

        print(
            f"{group['rank']:>6}"
            f"{score_text(score):>8}"
            f"{len(group['projects']):>10}"
            f"{money(group['group_cost']):>18}"
            f"{money(cumulative):>20}"
        )

    print()
    print("BUDGET BOUNDARY ANALYSIS")
    print("=" * 100)

    for label, budget in BUDGETS.items():
        cumulative = 0
        funded_projects = 0
        funded_tiers = 0
        boundary = None

        for score in ordered_scores:
            group = groups[score]
            next_total = cumulative + group["group_cost"]

            if next_total <= budget:
                cumulative = next_total
                funded_projects += len(group["projects"])
                funded_tiers += 1
                continue

            boundary = (
                score,
                group,
                budget - cumulative,
            )
            break

        print()
        print(label)
        print("-" * 100)
        print("Budget:", money(budget))
        print(
            "Fully fundable complete PRB tiers:",
            funded_tiers,
        )
        print(
            "Projects in complete higher-priority tiers:",
            funded_projects,
        )
        print(
            "Cost of complete higher-priority tiers:",
            money(cumulative),
        )
        print(
            "Remaining before boundary tier:",
            money(budget - cumulative),
        )

        if boundary is None:
            print("Boundary tier: NONE")
            continue

        score, group, remaining = boundary

        print(
            "Boundary rank:",
            group["rank"],
        )
        print(
            "Boundary score:",
            score_text(score),
        )
        print(
            "Projects tied at boundary:",
            len(group["projects"]),
        )
        print(
            "Full boundary-tier cost:",
            money(group["group_cost"]),
        )
        print(
            "Budget available for boundary tier:",
            money(remaining),
        )

        individually_fitting = [
            project
            for project in group["projects"]
            if project[2] <= remaining
        ]

        print(
            "Boundary projects individually fitting:",
            len(individually_fitting),
        )

        for decision_unit_id, category, cost in group["projects"]:
            status = (
                "FITS_INDIVIDUALLY"
                if cost <= remaining
                else "DOES_NOT_FIT_INDIVIDUALLY"
            )

            print(
                "  ",
                decision_unit_id,
                "|",
                category,
                "|",
                money(cost),
                "|",
                status,
            )

    print()
    print("METHODOLOGY QUESTION")
    print("=" * 100)
    print(
        "If a budget intersects a substantive tie group, "
        "M3.7D must define a defensible rule without pretending "
        "that deterministic display order is analytical priority."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
