#!/usr/bin/env python3
"""Audit official pre-snapshot portfolio-constraint feasibility for M3.7D-B0."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from pypdf import PdfReader

if __package__:
    from . import extract_non_watershed_prb_scores as non_watershed
    from . import extract_watershed_prb_scores as watershed
else:
    import extract_non_watershed_prb_scores as non_watershed
    import extract_watershed_prb_scores as watershed


ROOT = Path(__file__).resolve().parents[2]

SOURCE_PATH = non_watershed.DEFAULT_SOURCE_PATH
REGISTRY_PATH = non_watershed.DEFAULT_REGISTRY_PATH

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

EXPECTED_PROJECT_COUNT = 106
EXPECTED_REQUEST_TOTAL = 1_973_520_000


def normalize_om(value: str) -> str:
    value = value.strip().lower()

    if value not in {"yes", "no", "n/a"}:
        raise RuntimeError(
            f"Unexpected O&M value: {value!r}"
        )

    return value


def normalize_district(raw: str) -> str:
    value = raw.strip()

    if not value:
        return "UNSPECIFIED"

    cleaned = (
        value.replace(",", " ")
        .replace("/", " ")
        .strip()
    )

    cleaned = " ".join(
        cleaned.split()
    )

    if cleaned.lower() == "citywide":
        return "CITYWIDE"

    tokens = cleaned.split()

    if not all(
        token.isdigit()
        for token in tokens
    ):
        raise RuntimeError(
            "Could not interpret Council "
            f"District value: {raw!r}"
        )

    districts = [
        int(token)
        for token in tokens
    ]

    if any(
        district < 1 or district > 10
        for district in districts
    ):
        raise RuntimeError(
            "Council District outside "
            f"1-10: {raw!r}"
        )

    return ",".join(
        str(district)
        for district in districts
    )


def district_type(value: str) -> str:
    if value == "CITYWIDE":
        return "CITYWIDE"

    if value == "UNSPECIFIED":
        return "UNSPECIFIED"

    if "," in value:
        return "MULTI_DISTRICT"

    return "SINGLE_DISTRICT"


def district_list(value: str) -> tuple[int, ...]:
    if value in {
        "CITYWIDE",
        "UNSPECIFIED",
    }:
        return ()

    return tuple(
        int(token)
        for token in value.split(",")
    )



def extract_council_district(
    remainder: str,
    january_request_dollars: int,
    decision_unit_id: str,
) -> str:
    """Separate Council District from the following request amount.

    PDF extraction does not preserve the dollar sign consistently.
    Therefore the governed January request value, rather than '$',
    is used to identify the field boundary.
    """

    normalized_remainder = (
        non_watershed.normalize(
            remainder
        )
    )

    request_marker = (
        non_watershed.normalize(
            f"{january_request_dollars:,}"
        )
    )

    position = (
        normalized_remainder.find(
            request_marker
        )
    )

    if position < 0:
        raise RuntimeError(
            f"{decision_unit_id}: "
            "could not locate governed January "
            "request amount in PRB row remainder. "
            f"Expected request "
            f"{january_request_dollars:,}; "
            f"remainder={normalized_remainder!r}"
        )

    district_raw = (
        normalized_remainder[
            :position
        ]
        .replace("$", " ")
        .strip()
    )

    # A blank Council District is a valid source state.
    # Preserve it as UNSPECIFIED rather than inventing geography
    # or treating missing district evidence as an extraction failure.
    return normalize_district(
        district_raw
    )

def extract_non_watershed(
    reader: PdfReader,
    january_requests: dict[str, int],
) -> list[dict[str, object]]:
    governed = (
        non_watershed
        .load_governed_projects()
    )

    page_text: dict[
        int,
        str,
    ] = {}

    for physical_page in (
        non_watershed
        .PHYSICAL_PDF_PAGES
    ):
        raw = (
            reader.pages[
                physical_page - 1
            ].extract_text()
            or ""
        )

        page_text[
            physical_page
        ] = non_watershed.normalize(
            raw
        )

    records = []

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
                "expected exactly one "
                "January PRB occurrence; "
                f"found {occurrences}"
            )

        (
            physical_page,
            start,
            count,
        ) = occurrences[0]

        if count != 1:
            raise RuntimeError(
                f"{decision_unit_id}: "
                f"name appears {count} times"
            )

        text = page_text[
            physical_page
        ]

        suffix = text[
            start
            + len(
                normalized_name
            ):
        ]

        match = (
            non_watershed
            .ROW_SUFFIX_PATTERN
            .match(suffix)
        )

        if match is None:
            raise RuntimeError(
                f"{decision_unit_id}: "
                "could not parse PRB row"
            )

        raw = match.groupdict()

        om_impact = normalize_om(
            raw["om_impact"]
        )

        remainder = suffix[
            match.end():
        ].lstrip()

        council_district = (
            extract_council_district(
                remainder,
                january_requests[
                    decision_unit_id
                ],
                decision_unit_id,
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
                "om_impact": (
                    om_impact
                ),
                "council_district": (
                    council_district
                ),
            }
        )

    if len(records) != 69:
        raise RuntimeError(
            "Expected 69 non-Watershed "
            f"projects; found {len(records)}"
        )

    return records


def extract_watershed(
    reader: PdfReader,
    january_requests: dict[str, int],
) -> list[dict[str, object]]:
    overlay = (
        watershed
        .load_governed_january_overlay(
            watershed
            .DEFAULT_WATERSHED_PATH
        )
    )

    records = []

    for physical_page in (
        watershed
        .PHYSICAL_PDF_PAGES
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

            january_name = raw[
                "name"
            ]

            if january_name not in overlay:
                raise RuntimeError(
                    "Unexpected Watershed "
                    "PRB project: "
                    f"{january_name!r}"
                )

            canonical_id = str(
                overlay[
                    january_name
                ][
                    "canonical_project_id"
                ]
            )

            decision_unit_id = (
                "watershed/"
                f"{canonical_id}"
            )

            remainder = normalized[
                match.end():
            ].lstrip()

            council_district = (
                extract_council_district(
                    remainder,
                    january_requests[
                        decision_unit_id
                    ],
                    decision_unit_id,
                )
            )

            # The governed Watershed pattern
            # explicitly matches "No" after
            # Grand Total as the O&M Impact
            # source field.
            records.append(
                {
                    "decision_unit_id": (
                        decision_unit_id
                    ),
                    "presentation_category": (
                        "Watershed"
                    ),
                    "physical_page": (
                        physical_page
                    ),
                    "om_impact": "no",
                    "council_district": (
                        council_district
                    ),
                }
            )

    if len(records) != 37:
        raise RuntimeError(
            "Expected 37 Watershed "
            f"projects; found {len(records)}"
        )

    return records


def print_constraint(
    name: str,
    evidence: str,
    machine_feasibility: str,
    governed_role: str,
    reason: str,
) -> None:
    print()
    print(name)
    print("-" * 88)
    print(
        "Evidence:",
        evidence,
    )
    print(
        "Machine feasibility:",
        machine_feasibility,
    )
    print(
        "Governed role:",
        governed_role,
    )
    print(
        "Reason:",
        reason,
    )


def main() -> int:
    checksum = (
        non_watershed
        .validate_source_checksum(
            SOURCE_PATH,
            REGISTRY_PATH,
        )
    )

    priority = json.loads(
        PRIORITY_PATH.read_text(
            encoding="utf-8"
        )
    )

    reconciliation = json.loads(
        RECONCILIATION_PATH.read_text(
            encoding="utf-8"
        )
    )

    if (
        priority[
            "cross_category_ranking_authorized"
        ]
        is not True
    ):
        raise RuntimeError(
            "M3.7F ranking must remain "
            "authorized."
        )

    if (
        priority[
            "portfolio_selection_authorized"
        ]
        is not False
    ):
        raise RuntimeError(
            "Portfolio selection must remain "
            "unauthorized during B0."
        )

    if (
        priority[
            "runtime_integration_authorized"
        ]
        is not False
    ):
        raise RuntimeError(
            "Runtime integration must remain "
            "unauthorized during B0."
        )

    reconciliation_records = (
        reconciliation[
            "records"
        ]
    )

    if (
        len(
            reconciliation_records
        )
        != EXPECTED_PROJECT_COUNT
    ):
        raise RuntimeError(
            "Expected 106 reconciliation "
            "records."
        )

    request_total = sum(
        int(
            record[
                "model_request_dollars"
            ]
        )
        for record
        in reconciliation_records
    )

    if (
        request_total
        != EXPECTED_REQUEST_TOTAL
    ):
        raise RuntimeError(
            "Governed request total changed."
        )

    january_requests = {}

    for record in reconciliation_records:
        decision_unit_id = str(
            record["decision_unit_id"]
        )

        january_request = record.get(
            "january_request_dollars"
        )

        if january_request is None:
            january_request = record[
                "model_request_dollars"
            ]

        january_requests[
            decision_unit_id
        ] = int(
            january_request
        )

    if len(january_requests) != EXPECTED_PROJECT_COUNT:
        raise RuntimeError(
            "Expected January request lookup "
            "for all 106 analytical projects."
        )

    reader = PdfReader(
        SOURCE_PATH
    )

    records = [
        *extract_non_watershed(
            reader,
            january_requests,
        ),
        *extract_watershed(
            reader,
            january_requests,
        ),
    ]

    if len(records) != EXPECTED_PROJECT_COUNT:
        raise RuntimeError(
            "Expected 106 project-level "
            "constraint records."
        )

    ids = [
        record[
            "decision_unit_id"
        ]
        for record in records
    ]

    if len(ids) != len(set(ids)):
        raise RuntimeError(
            "Duplicate project identities "
            "in B0 audit."
        )

    governed_ids = {
        record[
            "decision_unit_id"
        ]
        for record
        in reconciliation_records
    }

    if set(ids) != governed_ids:
        missing = sorted(
            governed_ids
            - set(ids)
        )

        extra = sorted(
            set(ids)
            - governed_ids
        )

        raise RuntimeError(
            "B0 project identity mismatch. "
            f"Missing={missing}; "
            f"Extra={extra}"
        )

    om_counts = Counter(
        record["om_impact"]
        for record in records
    )

    district_type_counts = Counter(
        district_type(
            str(
                record[
                    "council_district"
                ]
            )
        )
        for record in records
    )

    category_district_types = {}

    categories = (
        "Transportation",
        "Parks & Open Space",
        "Watershed",
        "Community Facilities",
    )

    for category in categories:
        category_records = [
            record
            for record in records
            if (
                record[
                    "presentation_category"
                ]
                == category
            )
        ]

        category_district_types[
            category
        ] = Counter(
            district_type(
                str(
                    record[
                        "council_district"
                    ]
                )
            )
            for record
            in category_records
        )

    district_counts = Counter()

    for record in records:
        for district in district_list(
            str(
                record[
                    "council_district"
                ]
            )
        ):
            district_counts[
                district
            ] += 1

    print(
        "M3.7D-B0 OFFICIAL PORTFOLIO-"
        "CONSTRAINT FEASIBILITY AUDIT"
    )
    print("=" * 88)

    print()
    print(
        "January source checksum:",
        checksum,
    )

    print(
        "Analytical projects:",
        len(records),
    )

    print(
        "Governed request total:",
        f"${request_total:,.0f}",
    )

    print()
    print("STRUCTURED SOURCE-FIELD COVERAGE")
    print("=" * 88)

    print()
    print("O&M Impact")
    print("-" * 88)
    print(dict(sorted(om_counts.items())))

    print()
    print("Council District assignment type")
    print("-" * 88)
    print(
        dict(
            sorted(
                district_type_counts.items()
            )
        )
    )

    print()
    print("Council District assignment type by category")
    print("-" * 88)

    for category in categories:
        print(
            category,
            dict(
                sorted(
                    category_district_types[
                        category
                    ].items()
                )
            ),
        )

    print()
    print(
        "Specific project associations "
        "by Council District"
    )
    print("-" * 88)

    for district in range(1, 11):
        print(
            f"District {district}:",
            district_counts[
                district
            ],
        )

    print()
    print("PRE-SNAPSHOT PORTFOLIO-CONSIDERATION CLASSIFICATION")
    print("=" * 88)

    print_constraint(
        "1. PRB Funding Priority",
        (
            "Complete official PRB Grand "
            "Total for 106/106 projects"
        ),
        "YES",
        "HARD_ORDINAL_PRIORITY_RULE",
        (
            "M3.7F already authorizes "
            "cross-category ordinal ranking."
        ),
    )

    print_constraint(
        "2. Governed project request",
        (
            "Positive governed model request "
            "for 106/106 projects"
        ),
        "YES",
        "HARD_BUDGET_FEASIBILITY_INPUT",
        (
            "Exact project cost can be "
            "tested against Available Budget."
        ),
    )

    print_constraint(
        "3. Council District distribution",
        (
            "January PRB table contains "
            "Council District source field"
        ),
        "NO_AS_NUMERIC_HARD_CONSTRAINT",
        "ANALYST_REVIEW_AND_REPORTING",
        (
            "January 14 committee framework "
            "material identifies equitable "
            "Council-district distribution "
            "as a proposed portfolio consideration. "
            "It was not yet adopted as a hard "
            "selection rule at the January 21 "
            "historical snapshot, and no reproducible "
            "quota or project-selection formula "
            "was provided."
        ),
    )

    print_constraint(
        "4. O&M impact",
        (
            "January PRB table contains "
            "structured Yes/No/N/A O&M field"
        ),
        "NO_AS_PORTFOLIO_CAP",
        "CONTEXT_AND_ANALYST_WARNING",
        (
            "Boolean impact does not quantify "
            "five-year operating-budget cost. "
            "Net O&M is also already considered "
            "inside the PRB Efficiency rubric, "
            "so an added preference would risk "
            "double counting."
        ),
    )

    print_constraint(
        "5. Six-year deliverability",
        (
            "January 14 committee framework "
            "material identifies six-year "
            "deliverability as a proposed "
            "portfolio consideration"
        ),
        "NO",
        "ANALYST_REVIEW_ONLY",
        (
            "No governed 106-project schedule, "
            "delivery-capacity consumption, or "
            "resource model supports a machine "
            "portfolio constraint."
        ),
    )

    print_constraint(
        "6. Matching funds / private investment",
        (
            "January 14 committee framework "
            "material identifies leveraged "
            "projects as a proposed priority"
        ),
        "NO_ADDITIONAL_RULE",
        "ALREADY_PARTLY_ENCODED_IN_PRB",
        (
            "Outside funding/private investment "
            "is explicitly scored within the "
            "official PRB Efficiency rubric. "
            "Adding another preference would "
            "double count it."
        ),
    )

    print_constraint(
        "7. Preventative maintenance",
        (
            "January 14 committee framework "
            "material identifies preventative "
            "maintenance and avoided future "
            "reconstruction cost as a proposed "
            "portfolio consideration"
        ),
        "NO",
        "ANALYST_REVIEW_ONLY",
        (
            "No complete governed project-level "
            "preventative-maintenance flag or "
            "avoided-cost measure exists for "
            "the 106-project cohort."
        ),
    )

    print_constraint(
        "8. Strategic alignment",
        (
            "Official PRB Strategic Alignment "
            "component exists for 106/106"
        ),
        "NO_ADDITIONAL_RULE",
        "ALREADY_ENCODED_IN_PRB",
        (
            "Using it again during portfolio "
            "selection would reopen PRB weights "
            "and double count the official score."
        ),
    )

    print_constraint(
        "9. Historical category allocations",
        (
            "January Initial Recommendation "
            "contains category allocations"
        ),
        "NO",
        "BENCHMARK_OUTCOME_ONLY",
        (
            "The allocations are recommendation "
            "outcomes, not independently proven "
            "pre-snapshot hard project-cohort "
            "caps."
        ),
    )

    print_constraint(
        "10. Historical project membership",
        (
            "20/106 analytical projects have "
            "January project-level recommendation"
        ),
        "NO",
        "BENCHMARK_OUTCOME_ONLY",
        (
            "Using membership to select projects "
            "would leak the historical outcome."
        ),
    )

    print_constraint(
        "11. $750M financial-capacity figure",
        (
            "Austin Financial Services modeled "
            "$750M as the Jan. 14 maximum "
            "citywide 2026 bond option"
        ),
        "NO_AS_106_PROJECT_BUDGET",
        "CITYWIDE_CAPACITY_REFERENCE",
        (
            "It applies to the complete bond "
            "program, not only the 106 analytical "
            "project cohort."
        ),
    )

    print_constraint(
        "12. $332M matched-cohort envelope",
        (
            "Historical recommendation dollars "
            "attached to the same 106-project "
            "analytical cohort"
        ),
        "YES_AS_COMPARISON_SCENARIO",
        "HISTORICAL_MATCHED_COHORT_BENCHMARK",
        (
            "It supports an apples-to-apples "
            "historical comparison but is not "
            "a permanent City-mandated model "
            "budget."
        ),
    )

    print()
    print("B0 PRELIMINARY RESULT")
    print("=" * 88)

    print(
        "Machine-operational portfolio inputs:"
    )
    print(
        "- model eligibility"
    )
    print(
        "- ordinal PRB Funding Priority"
    )
    print(
        "- governed project request"
    )
    print(
        "- analyst-supplied Available Project Budget"
    )

    print()
    print(
        "Official portfolio considerations "
        "requiring analyst review/context:"
    )
    print(
        "- equitable Council-district distribution"
    )
    print(
        "- O&M implications"
    )
    print(
        "- six-year deliverability"
    )
    print(
        "- preventative-maintenance policy"
    )

    print()
    print(
        "Do not double count:"
    )
    print(
        "- matching/outside funding"
    )
    print(
        "- strategic alignment"
    )
    print(
        "- O&M through a new score preference"
    )

    print()
    print(
        "Do not use as selection inputs:"
    )
    print(
        "- historical category allocations"
    )
    print(
        "- historical project recommendation membership"
    )

    print()
    print(
        "Portfolio selection remains unauthorized "
        "until M3.7D-B methodology is explicitly locked."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
