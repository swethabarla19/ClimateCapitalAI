#!/usr/bin/env python3
"""Audit governed cross-category analytical-project names against PRB PDF pages 5-7."""

from __future__ import annotations

import json
import re
import unicodedata
from collections import Counter
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


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKD", value)
    value = value.replace("&", " and ")
    value = value.replace("–", "-")
    value = value.replace("—", "-")
    value = value.lower()

    value = re.sub(
        r"[^a-z0-9]+",
        " ",
        value,
    )

    return " ".join(value.split())


reader = PdfReader(PDF_PATH)

page_text = {}

for physical_page in (5, 6, 7):
    raw = reader.pages[physical_page - 1].extract_text() or ""
    page_text[physical_page] = normalize(raw)


all_results = []

for category, path in CATEGORY_FILES.items():
    rows = json.loads(path.read_text(encoding="utf-8"))

    projects = [
        row
        for row in rows
        if row["analytical_unit_type"] == "ANALYTICAL_PROJECT"
    ]

    print("=" * 80)
    print(category)
    print("=" * 80)

    category_results = []

    for row in projects:
        normalized_name = normalize(row["source_name"])

        matched_pages = [
            page
            for page, text in page_text.items()
            if normalized_name in text
        ]

        result = {
            "category": category,
            "decision_unit_id": row["decision_unit_id"],
            "source_name": row["source_name"],
            "matched_pages": matched_pages,
        }

        category_results.append(result)
        all_results.append(result)

    exact_one = [
        row
        for row in category_results
        if len(row["matched_pages"]) == 1
    ]

    unmatched = [
        row
        for row in category_results
        if len(row["matched_pages"]) == 0
    ]

    ambiguous = [
        row
        for row in category_results
        if len(row["matched_pages"]) > 1
    ]

    print("Analytical projects:", len(projects))
    print("Matched exactly one page:", len(exact_one))
    print("Unmatched:", len(unmatched))
    print("Ambiguous:", len(ambiguous))

    print(
        "Page distribution:",
        Counter(
            row["matched_pages"][0]
            for row in exact_one
        ),
    )

    if unmatched:
        print("\nUNMATCHED")
        for row in unmatched:
            print(
                row["decision_unit_id"],
                "|",
                row["source_name"],
            )

    if ambiguous:
        print("\nAMBIGUOUS")
        for row in ambiguous:
            print(
                row["decision_unit_id"],
                "|",
                row["matched_pages"],
                "|",
                row["source_name"],
            )

    print()


print("=" * 80)
print("ALL REMAINING CROSS-CATEGORY PROJECTS")
print("=" * 80)

exact_one = [
    row
    for row in all_results
    if len(row["matched_pages"]) == 1
]

unmatched = [
    row
    for row in all_results
    if len(row["matched_pages"]) == 0
]

ambiguous = [
    row
    for row in all_results
    if len(row["matched_pages"]) > 1
]

print("Expected projects: 69")
print("Observed projects:", len(all_results))
print("Matched exactly one page:", len(exact_one))
print("Unmatched:", len(unmatched))
print("Ambiguous:", len(ambiguous))

print(
    "Overall page distribution:",
    Counter(
        row["matched_pages"][0]
        for row in exact_one
    ),
)