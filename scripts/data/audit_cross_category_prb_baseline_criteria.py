#!/usr/bin/env python3
"""Audit PRB baseline criteria for all 106 governed analytical projects."""

from __future__ import annotations

from collections import Counter, defaultdict

from pypdf import PdfReader

if __package__:
    from . import extract_non_watershed_prb_scores as non_watershed
    from . import extract_watershed_prb_scores as watershed
else:
    import extract_non_watershed_prb_scores as non_watershed
    import extract_watershed_prb_scores as watershed


SOURCE_PATH = non_watershed.DEFAULT_SOURCE_PATH
REGISTRY_PATH = non_watershed.DEFAULT_REGISTRY_PATH

EXPECTED_TOTAL = 106

EXPECTED_CATEGORY_COUNTS = {
    "Transportation": 9,
    "Parks & Open Space": 22,
    "Watershed": 37,
    "Community Facilities": 38,
}


def normalize_answer(value: str) -> str:
    return value.strip().lower()


def baseline_satisfied(
    requirement: str,
    city_owned: str,
) -> bool:
    return (
        normalize_answer(requirement) == "yes"
        or normalize_answer(city_owned) == "yes"
    )


def audit_non_watershed(
    reader: PdfReader,
) -> list[dict[str, object]]:
    governed = (
        non_watershed.load_governed_projects()
    )

    page_text: dict[int, str] = {}

    for physical_page in (
        non_watershed.PHYSICAL_PDF_PAGES
    ):
        raw = (
            reader.pages[
                physical_page - 1
            ].extract_text()
            or ""
        )

        page_text[physical_page] = (
            non_watershed.normalize(raw)
        )

    records: list[
        dict[str, object]
    ] = []

    for governed_record in (
        governed.values()
    ):
        decision_unit_id = str(
            governed_record[
                "decision_unit_id"
            ]
        )

        category = str(
            governed_record[
                "presentation_category"
            ]
        )

        january_name = str(
            governed_record[
                "january_source_name"
            ]
        )

        normalized_name = (
            non_watershed.normalize(
                january_name
            )
        )

        occurrences = []

        for (
            physical_page,
            text,
        ) in page_text.items():
            count = text.count(
                normalized_name
            )

            if count:
                occurrences.append(
                    (
                        physical_page,
                        text.find(
                            normalized_name
                        ),
                        count,
                    )
                )

        if len(occurrences) != 1:
            raise RuntimeError(
                f"{decision_unit_id}: "
                "expected exactly one page "
                f"occurrence; found "
                f"{occurrences}"
            )

        (
            physical_page,
            start,
            count,
        ) = occurrences[0]

        if count != 1:
            raise RuntimeError(
                f"{decision_unit_id}: "
                f"name occurs {count} times "
                f"on page {physical_page}"
            )

        text = page_text[
            physical_page
        ]

        suffix = text[
            start
            + len(normalized_name):
        ]

        match = (
            non_watershed
            .ROW_SUFFIX_PATTERN
            .match(suffix)
        )

        if match is None:
            raise RuntimeError(
                f"{decision_unit_id}: "
                "could not parse PRB row "
                f"on page {physical_page}"
            )

        raw = match.groupdict()

        requirement = (
            normalize_answer(
                raw["requirement"]
            )
        )

        city_owned = (
            normalize_answer(
                raw["city_owned"]
            )
        )

        records.append(
            {
                "decision_unit_id": (
                    decision_unit_id
                ),
                "presentation_category": (
                    category
                ),
                "physical_page": (
                    physical_page
                ),
                "requirement": (
                    requirement
                ),
                "city_owned": (
                    city_owned
                ),
                "baseline_satisfied": (
                    baseline_satisfied(
                        requirement,
                        city_owned,
                    )
                ),
            }
        )

    return records


def audit_watershed(
    reader: PdfReader,
) -> list[dict[str, object]]:
    overlay = (
        watershed
        .load_governed_january_overlay(
            watershed.DEFAULT_WATERSHED_PATH
        )
    )

    records: list[
        dict[str, object]
    ] = []

    for physical_page in (
        watershed.PHYSICAL_PDF_PAGES
    ):
        raw_text = (
            reader.pages[
                physical_page - 1
            ].extract_text()
            or ""
        )

        normalized = (
            watershed
            .normalize_whitespace(
                raw_text
            )
        )

        for match in (
            watershed
            .PROJECT_PATTERN
            .finditer(normalized)
        ):
            raw = match.groupdict()

            january_name = raw["name"]

            if january_name not in overlay:
                raise RuntimeError(
                    "Unexpected Watershed "
                    "project in PRB source: "
                    f"{january_name!r}"
                )

            canonical_id = str(
                overlay[
                    january_name
                ][
                    "canonical_project_id"
                ]
            )

            requirement = (
                normalize_answer(
                    raw["requirement"]
                )
            )

            city_owned = (
                normalize_answer(
                    raw["city_owned"]
                )
            )

            records.append(
                {
                    "decision_unit_id": (
                        "watershed/"
                        f"{canonical_id}"
                    ),
                    "presentation_category": (
                        "Watershed"
                    ),
                    "physical_page": (
                        physical_page
                    ),
                    "requirement": (
                        requirement
                    ),
                    "city_owned": (
                        city_owned
                    ),
                    "baseline_satisfied": (
                        baseline_satisfied(
                            requirement,
                            city_owned,
                        )
                    ),
                }
            )

    if len(records) != 37:
        raise RuntimeError(
            "Expected 37 Watershed "
            "analytical projects; "
            f"found {len(records)}"
        )

    return records


def main() -> int:
    checksum = (
        non_watershed
        .validate_source_checksum(
            SOURCE_PATH,
            REGISTRY_PATH,
        )
    )

    reader = PdfReader(
        SOURCE_PATH
    )

    records = (
        audit_non_watershed(
            reader
        )
        + audit_watershed(
            reader
        )
    )

    if len(records) != EXPECTED_TOTAL:
        raise RuntimeError(
            f"Expected {EXPECTED_TOTAL} "
            "analytical projects; "
            f"found {len(records)}"
        )

    ids = [
        str(
            record[
                "decision_unit_id"
            ]
        )
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            "Baseline audit contains "
            "duplicate decision_unit_ids."
        )

    category_counts = Counter(
        str(
            record[
                "presentation_category"
            ]
        )
        for record in records
    )

    if dict(
        category_counts
    ) != EXPECTED_CATEGORY_COUNTS:
        raise RuntimeError(
            "Category counts changed: "
            f"{dict(category_counts)}"
        )

    failures = [
        record
        for record in records
        if not record[
            "baseline_satisfied"
        ]
    ]

    combinations = Counter(
        (
            str(
                record[
                    "requirement"
                ]
            ),
            str(
                record[
                    "city_owned"
                ]
            ),
        )
        for record in records
    )

    by_category = defaultdict(
        lambda: Counter()
    )

    for record in records:
        by_category[
            str(
                record[
                    "presentation_category"
                ]
            )
        ][
            (
                str(
                    record[
                        "requirement"
                    ]
                ),
                str(
                    record[
                        "city_owned"
                    ]
                ),
            )
        ] += 1

    print(
        "M3.7F PRB BASELINE "
        "CRITERIA AUDIT"
    )

    print("=" * 72)

    print(
        "Verified source checksum:",
        checksum,
    )

    print()

    print(
        "Analytical projects:",
        len(records),
    )

    print(
        "Baseline satisfied:",
        sum(
            bool(
                record[
                    "baseline_satisfied"
                ]
            )
            for record in records
        ),
    )

    print(
        "Baseline failures:",
        len(failures),
    )

    print()

    print(
        "Requirement = Yes:",
        sum(
            record[
                "requirement"
            ]
            == "yes"
            for record in records
        ),
    )

    print(
        "City Owned = Yes:",
        sum(
            record[
                "city_owned"
            ]
            == "yes"
            for record in records
        ),
    )

    print()

    print(
        "BASELINE COMBINATIONS"
    )

    for combination in sorted(
        combinations
    ):
        print(
            combination,
            combinations[
                combination
            ],
        )

    print()

    print(
        "BY CATEGORY"
    )

    for category in (
        "Transportation",
        "Parks & Open Space",
        "Watershed",
        "Community Facilities",
    ):
        print()
        print(category)

        for combination in sorted(
            by_category[category]
        ):
            print(
                " ",
                combination,
                by_category[
                    category
                ][
                    combination
                ],
            )

    if failures:
        print()
        print(
            "BASELINE FAILURES"
        )

        for record in failures:
            print(
                record[
                    "decision_unit_id"
                ],
                "|",
                record[
                    "presentation_category"
                ],
                "| requirement=",
                record[
                    "requirement"
                ],
                "| city_owned=",
                record[
                    "city_owned"
                ],
                "| page=",
                record[
                    "physical_page"
                ],
            )

        raise RuntimeError(
            "One or more analytical "
            "projects fail the PRB "
            "baseline prerequisite."
        )

    print()

    print(
        "RESULT: 106/106 satisfy "
        "at least one PRB baseline "
        "criterion."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())