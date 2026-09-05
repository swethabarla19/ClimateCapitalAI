#!/usr/bin/env python3
"""Audit six-component PRB parsing for the remaining 69 analytical projects."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[2]

PDF_PATH = (
    ROOT
    / "data"
    / "staging"
    / "raw"
    / "city_austin"
    / "initial_draft_recommendation"
    / "2026-01-21"
    / "source.pdf"
)

CATEGORY_FILES = {
    "Transportation": (
        ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "transportation.json"
    ),
    "Parks & Open Space": (
        ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "parks.json"
    ),
    "Community Facilities": (
        ROOT
        / "data"
        / "governed"
        / "cross_category"
        / "source_rows"
        / "community_facilities.json"
    ),
}

PHYSICAL_PAGES = (5, 6, 7)

NUMBER = r"\d+(?:\.\d+)?"

ROW_SUFFIX_PATTERN = re.compile(
    rf"^\s+"
    rf"(?P<requirement>yes|no|n/a)\s+"
    rf"(?P<city_owned>yes|no|n/a)\s+"
    rf"(?P<strategic_alignment>{NUMBER})\s+"
    rf"(?P<critical_asset>{NUMBER})\s+"
    rf"(?P<community_consideration>{NUMBER})\s+"
    rf"(?P<efficiency>{NUMBER})\s+"
    rf"(?P<timeliness_readiness>{NUMBER})\s+"
    rf"(?P<climate_resilience>{NUMBER})\s+"
    rf"(?P<grand_total>{NUMBER})\s+"
    rf"(?P<om_impact>yes|no|n/a)\b"
)

COMPONENT_FIELDS = (
    "strategic_alignment",
    "critical_asset",
    "community_consideration",
    "efficiency",
    "timeliness_readiness",
    "climate_resilience",
)


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.replace("&", " and ")
    value = value.replace("–", "-")
    value = value.replace("—", "-")
    value = value.lower()

    value = re.sub(
        r"[^a-z0-9.$]+",
        " ",
        value,
    )

    return " ".join(value.split())


def decimal_from_governed(value: int | float) -> Decimal:
    return Decimal(str(value))


reader = PdfReader(PDF_PATH)

page_text = {}

for page_number in PHYSICAL_PAGES:
    raw = reader.pages[page_number - 1].extract_text() or ""
    page_text[page_number] = normalize(raw)


all_results = []
failures = []

for category, path in CATEGORY_FILES.items():
    rows = json.loads(
        path.read_text(encoding="utf-8")
    )

    projects = [
        row
        for row in rows
        if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
    ]

    category_results = []

    for row in projects:
        normalized_name = normalize(row["source_name"])

        occurrences = []

        for page_number, text in page_text.items():
            start = text.find(normalized_name)

            if start != -1:
                count = text.count(normalized_name)

                occurrences.append(
                    {
                        "page": page_number,
                        "start": start,
                        "count": count,
                    }
                )

        if len(occurrences) != 1:
            failures.append(
                {
                    "decision_unit_id": row["decision_unit_id"],
                    "source_name": row["source_name"],
                    "reason": (
                        "NAME_OCCURRENCE_NOT_UNIQUE_ACROSS_PAGES"
                    ),
                    "occurrences": occurrences,
                }
            )
            continue

        occurrence = occurrences[0]

        if occurrence["count"] != 1:
            failures.append(
                {
                    "decision_unit_id": row["decision_unit_id"],
                    "source_name": row["source_name"],
                    "reason": (
                        "NAME_OCCURRENCE_NOT_UNIQUE_WITHIN_PAGE"
                    ),
                    "occurrences": occurrences,
                }
            )
            continue

        page_number = occurrence["page"]
        text = page_text[page_number]

        suffix_start = (
            occurrence["start"]
            + len(normalized_name)
        )

        suffix = text[suffix_start:]

        match = ROW_SUFFIX_PATTERN.match(suffix)

        if match is None:
            failures.append(
                {
                    "decision_unit_id": row["decision_unit_id"],
                    "source_name": row["source_name"],
                    "reason": "ROW_SUFFIX_PARSE_FAILED",
                    "page": page_number,
                    "suffix_preview": suffix[:250],
                }
            )
            continue

        raw_scores = match.groupdict()

        scores = {
            field: Decimal(raw_scores[field])
            for field in COMPONENT_FIELDS
        }

        grand_total = Decimal(
            raw_scores["grand_total"]
        )

        component_sum = sum(
            scores.values(),
            Decimal("0"),
        )

        governed_total = decimal_from_governed(
            row["prb_score"]
        )

        component_sum_matches = (
            component_sum == grand_total
        )

        governed_total_matches = (
            grand_total == governed_total
        )

        result = {
            "category": category,
            "decision_unit_id": row["decision_unit_id"],
            "source_name": row["source_name"],
            "page": page_number,
            "strategic_alignment": scores[
                "strategic_alignment"
            ],
            "critical_asset": scores[
                "critical_asset"
            ],
            "community_consideration": scores[
                "community_consideration"
            ],
            "efficiency": scores[
                "efficiency"
            ],
            "timeliness_readiness": scores[
                "timeliness_readiness"
            ],
            "climate_resilience": scores[
                "climate_resilience"
            ],
            "grand_total": grand_total,
            "governed_total": governed_total,
            "component_sum_matches": (
                component_sum_matches
            ),
            "governed_total_matches": (
                governed_total_matches
            ),
        }

        category_results.append(result)
        all_results.append(result)

        if (
            not component_sum_matches
            or not governed_total_matches
        ):
            failures.append(
                {
                    **result,
                    "reason": (
                        "PRB_SCORE_RECONCILIATION_FAILED"
                    ),
                }
            )

    print("=" * 80)
    print(category)
    print("=" * 80)

    print("Expected analytical projects:", len(projects))
    print("Parsed rows:", len(category_results))

    print(
        "Component sums valid:",
        sum(
            result["component_sum_matches"]
            for result in category_results
        ),
    )

    print(
        "Governed Grand Totals matched:",
        sum(
            result["governed_total_matches"]
            for result in category_results
        ),
    )

    print(
        "Page distribution:",
        Counter(
            result["page"]
            for result in category_results
        ),
    )

    print()


print("=" * 80)
print("ALL REMAINING CROSS-CATEGORY PROJECTS")
print("=" * 80)

print("Expected projects: 69")
print("Parsed projects:", len(all_results))

print(
    "Component sums valid:",
    sum(
        result["component_sum_matches"]
        for result in all_results
    ),
)

print(
    "Governed Grand Totals matched:",
    sum(
        result["governed_total_matches"]
        for result in all_results
    ),
)

print("Failures:", len(failures))

half_point_projects = [
    result
    for result in all_results
    if any(
        value % 1 != 0
        for value in (
            result["strategic_alignment"],
            result["critical_asset"],
            result["community_consideration"],
            result["efficiency"],
            result["timeliness_readiness"],
            result["climate_resilience"],
            result["grand_total"],
        )
    )
]

print(
    "Projects containing half-point values:",
    len(half_point_projects),
)

for result in half_point_projects:
    print(
        "HALF-POINT",
        result["category"],
        "|",
        result["decision_unit_id"],
        "| total=",
        result["grand_total"],
    )


if failures:
    print()
    print("=" * 80)
    print("FAILURES")
    print("=" * 80)

    for failure in failures:
        print(json.dumps(
            failure,
            indent=2,
            default=str,
        ))


print()
print("=" * 80)
print("PARSED ROWS BY PAGE")
print("=" * 80)

by_page = defaultdict(list)

for result in all_results:
    by_page[result["page"]].append(
        result["decision_unit_id"]
    )

for page_number in sorted(by_page):
    print(
        f"Page {page_number}: "
        f"{len(by_page[page_number])}"
    )