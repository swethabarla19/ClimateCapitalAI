"""Governance contract for cross-category project map evidence."""

from __future__ import annotations

from collections import Counter
from typing import Annotated, Literal

from pydantic import Field, model_validator

from .common import (
    DataVersion,
    NonEmptyString,
    Sha256,
    ShortText,
    StableIdentifier,
    StrictModel,
)


CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION = (
    "p0-cross-category-geometry-governance/1.0.0"
)
CROSS_CATEGORY_GEOMETRY_GOVERNANCE_DECISION_ID = "D-116"
CROSS_CATEGORY_GOVERNED_MAPPED_PROJECT_COUNT = 74
CROSS_CATEGORY_GOVERNED_UNMAPPED_PROJECT_COUNT = 32


PresentationCategory = Literal[
    "Transportation",
    "Parks & Open Space",
    "Watershed",
    "Community Facilities",
]

GeometryType = Literal[
    "point",
    "line",
    "polygon",
    "address-only",
    "no geometry",
]

MapGeometryType = Literal[
    "point",
    "line",
    "polygon",
]

ProjectMapDisplayRole = Literal[
    "PROJECT_DISPLAY_POINT",
    "PROJECT_SITE",
    "PROJECT_PARCEL",
    "PARK_SITE_CONTEXT",
    "FACILITY_SITE_CONTEXT",
    "PROJECT_CORRIDOR",
]

HistoricalFitClass = Literal[
    "EXACT_SNAPSHOT_DATE",
    "PRE_SNAPSHOT_SOURCE",
    "POST_SNAPSHOT_STABLE_LOCATION_ONLY",
    "UNRESOLVED_OR_NOT_APPLICABLE",
]

GovernanceStatus = Literal[
    "PROMOTED",
    "HELD_FOR_MORE_EVIDENCE",
    "REJECTED_LOW_CONFIDENCE",
    "REJECTED_NO_MATCH",
]


class GeometryResearchArtifactReference(StrictModel):
    path: ShortText
    sha256: Sha256


class CrossCategoryGeometryGovernanceDecision(StrictModel):
    decision_unit_id: StableIdentifier
    governed_name: ShortText
    presentation_category: PresentationCategory

    governance_status: GovernanceStatus
    reviewed_individually: Literal[True]
    governance_rationale: NonEmptyString
    unmapped_reason_code: StableIdentifier | None = None

    candidate_source_title: ShortText
    source_url: NonEmptyString
    arcgis_item_id: ShortText | None = None
    arcgis_service_id: ShortText | None = None
    source_layer_id: ShortText | None = None
    source_feature_id: ShortText | None = None
    source_agency: ShortText

    candidate_geometry_type: GeometryType
    candidate_geometry_origin: Literal[
        "source-native",
        "none",
    ]
    candidate_confidence: Literal[
        "HIGH",
        "MEDIUM",
        "LOW",
        "NO_MATCH",
    ]
    candidate_governance_eligibility: ShortText
    candidate_ambiguity: bool = Field(strict=True)
    candidate_multiple_possible_features: bool = Field(strict=True)

    source_date: ShortText | None = None
    source_last_updated_date: ShortText | None = None
    historical_fit_class: HistoricalFitClass
    historical_fit_judgment: NonEmptyString
    match_identifiers: NonEmptyString
    match_method: NonEmptyString

    display_role: ProjectMapDisplayRole | None = None
    caveats: list[ShortText] = Field(min_length=1)

    @model_validator(mode="after")
    def promotion_requirements(self) -> CrossCategoryGeometryGovernanceDecision:
        if self.governance_status == "PROMOTED":
            if self.candidate_confidence != "HIGH":
                raise ValueError("promoted geometry requires HIGH confidence")
            if self.candidate_geometry_origin != "source-native":
                raise ValueError("promoted geometry must be source-native")
            if self.candidate_geometry_type not in {"point", "line", "polygon"}:
                raise ValueError("promoted geometry must contain source geometry")
            if self.source_feature_id is None:
                raise ValueError("promoted geometry requires a source feature ID")
            if self.display_role is None:
                raise ValueError("promoted geometry requires a display role")
            if self.unmapped_reason_code is not None:
                raise ValueError("promoted geometry cannot have an unmapped reason")
            if self.candidate_ambiguity:
                raise ValueError("ambiguous candidate geometry cannot be promoted")
            if self.historical_fit_class == "UNRESOLVED_OR_NOT_APPLICABLE":
                raise ValueError("promoted geometry requires a resolved historical fit")
        else:
            if self.display_role is not None:
                raise ValueError("unmapped decisions cannot have a display role")
            if self.unmapped_reason_code is None:
                raise ValueError("unmapped decisions require a reason code")

        return self


class CrossCategoryGeometryGovernanceArtifact(StrictModel):
    contract_version: Literal[
        CROSS_CATEGORY_GEOMETRY_GOVERNANCE_CONTRACT_VERSION
    ]
    data_version: DataVersion
    historical_decision_snapshot_date: Literal["2026-01-21"]
    governance_decision_id: Literal[
        CROSS_CATEGORY_GEOMETRY_GOVERNANCE_DECISION_ID
    ]
    governance_review_date: Literal["2026-09-08"]
    project_identity_key: Literal["decision_unit_id"]

    analytical_project_count: Literal[106]
    candidates_reviewed_count: Literal[106]
    promotion_candidates_reviewed_individually: Literal[74]
    promoted_project_count: Literal[
        CROSS_CATEGORY_GOVERNED_MAPPED_PROJECT_COUNT
    ]
    unmapped_project_count: Literal[
        CROSS_CATEGORY_GOVERNED_UNMAPPED_PROJECT_COUNT
    ]

    fabricated_geometry: Literal[False]
    geocoded_geometry: Literal[False]
    inferred_or_centroid_geometry: Literal[False]
    geometry_changes_analytical_eligibility: Literal[False]
    geometry_changes_funding_priority: Literal[False]
    geometry_changes_funding_plan: Literal[False]
    geometry_changes_historical_benchmark: Literal[False]

    candidate_reconciliation: GeometryResearchArtifactReference
    candidate_geometry_snapshot: GeometryResearchArtifactReference
    candidate_investigation_report: GeometryResearchArtifactReference

    decisions: list[CrossCategoryGeometryGovernanceDecision] = Field(
        min_length=106,
        max_length=106,
    )

    @model_validator(mode="after")
    def governance_reconciles(self) -> CrossCategoryGeometryGovernanceArtifact:
        ids = [decision.decision_unit_id for decision in self.decisions]
        if ids != sorted(ids) or len(ids) != len(set(ids)):
            raise ValueError("geometry governance identities must be sorted and unique")

        promoted = [
            decision
            for decision in self.decisions
            if decision.governance_status == "PROMOTED"
        ]
        if len(promoted) != self.promoted_project_count:
            raise ValueError("promoted decision count does not reconcile")
        if len(self.decisions) - len(promoted) != self.unmapped_project_count:
            raise ValueError("unmapped decision count does not reconcile")

        expected_promoted_by_category = {
            "Transportation": 1,
            "Parks & Open Space": 21,
            "Watershed": 35,
            "Community Facilities": 17,
        }
        observed = Counter(
            decision.presentation_category
            for decision in promoted
        )
        if observed != expected_promoted_by_category:
            raise ValueError("promoted category coverage changed")

        if Counter(decision.candidate_geometry_type for decision in promoted) != {
            "point": 64,
            "polygon": 10,
        }:
            raise ValueError("promoted geometry-type coverage changed")

        if Counter(decision.display_role for decision in promoted) != {
            "PROJECT_DISPLAY_POINT": 42,
            "FACILITY_SITE_CONTEXT": 22,
            "PARK_SITE_CONTEXT": 8,
            "PROJECT_SITE": 1,
            "PROJECT_PARCEL": 1,
        }:
            raise ValueError("promoted display-role coverage changed")

        if Counter(decision.historical_fit_class for decision in promoted) != {
            "EXACT_SNAPSHOT_DATE": 35,
            "PRE_SNAPSHOT_SOURCE": 18,
            "POST_SNAPSHOT_STABLE_LOCATION_ONLY": 21,
        }:
            raise ValueError("promoted historical-fit coverage changed")

        if Counter(decision.governance_status for decision in self.decisions) != {
            "PROMOTED": 74,
            "HELD_FOR_MORE_EVIDENCE": 15,
            "REJECTED_LOW_CONFIDENCE": 2,
            "REJECTED_NO_MATCH": 15,
        }:
            raise ValueError("geometry governance disposition counts changed")

        citywide = "watershed/5789.150"
        if any(
            decision.decision_unit_id == citywide
            and decision.governance_status == "PROMOTED"
            for decision in self.decisions
        ):
            raise ValueError("citywide 5789.150 cannot receive project geometry")

        return self
