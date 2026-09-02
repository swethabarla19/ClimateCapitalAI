"""Strict shared primitives for artifacts, requests, and state contracts."""

from __future__ import annotations

import math
from enum import StrEnum
from types import MappingProxyType
from typing import Annotated, Any

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

from .versions import MAX_SCENARIO_BUDGET_DOLLARS


class StrictModel(BaseModel):
    """Base contract: no coercion and no undeclared fields."""

    model_config = ConfigDict(
        extra="forbid",
        strict=True,
        validate_assignment=True,
        use_enum_values=True,
    )


ProjectId = Annotated[str, StringConstraints(pattern=r"^[0-9]+\.[0-9]{3}$")]
Sha256 = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{64}$")]
DataVersion = Annotated[
    str,
    StringConstraints(pattern=r"^[a-z0-9][a-z0-9._-]{0,127}$"),
]
StableIdentifier = Annotated[
    str,
    StringConstraints(pattern=r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$"),
]
NonEmptyString = Annotated[str, StringConstraints(min_length=1, max_length=4_000)]
ShortText = Annotated[str, StringConstraints(min_length=1, max_length=500)]
IsoDate = Annotated[
    str,
    StringConstraints(pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$"),
]
IsoTimestamp = Annotated[
    str,
    StringConstraints(
        pattern=r"^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$"
    ),
]
WholeDollars = Annotated[int, Field(strict=True, ge=0)]
PositiveWholeDollars = Annotated[
    int,
    Field(strict=True, gt=0),
]
ScenarioBudgetDollars = Annotated[
    int,
    Field(strict=True, ge=0, le=MAX_SCENARIO_BUDGET_DOLLARS),
]
ByteSize = Annotated[int, Field(strict=True, gt=0)]
Count = Annotated[int, Field(strict=True, ge=0)]


class ReleaseTier(StrEnum):
    FIXTURE = "FIXTURE"
    REVIEWED_RELEASE = "REVIEWED_RELEASE"


class EvidenceRole(StrEnum):
    FACT = "FACT"
    CONTEXTUAL_EVIDENCE = "CONTEXTUAL_EVIDENCE"
    RESEARCH_ONLY_EVIDENCE = "RESEARCH_ONLY_EVIDENCE"
    UNAVAILABLE_UNSUPPORTED = "UNAVAILABLE_UNSUPPORTED"


class FactKind(StrEnum):
    SOURCE_GOVERNED = "SOURCE_GOVERNED"
    CLIMATE_CAPITAL_DERIVED = "CLIMATE_CAPITAL_DERIVED"


class Availability(StrEnum):
    AVAILABLE = "AVAILABLE"
    MISSING = "MISSING"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"
    NOT_EVALUATED_FIXTURE = "NOT_EVALUATED_FIXTURE"


class HistoricalFit(StrEnum):
    HISTORICALLY_VALID = "HISTORICALLY_VALID"
    CURRENT_CONTEXT_ONLY = "CURRENT_CONTEXT_ONLY"
    HISTORICAL_FIT_UNCERTAIN = "HISTORICAL_FIT_UNCERTAIN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class LicenseReuseStatus(StrEnum):
    VERIFIED = "VERIFIED"
    UNVERIFIED = "UNVERIFIED"
    RESTRICTED = "RESTRICTED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class Confidence(StrEnum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class EvidenceType(StrEnum):
    GOVERNED_PROJECT_IDENTITY = "GOVERNED_PROJECT_IDENTITY"
    GOVERNED_REQUEST = "GOVERNED_REQUEST"
    DERIVED_PURPOSE = "DERIVED_PURPOSE"
    P0_FAMILY = "P0_FAMILY"
    PROBLEM_SCORE_ASSOCIATION = "PROBLEM_SCORE_ASSOCIATION"
    RNA_DISPLAY_GEOMETRY_AVAILABILITY = "RNA_DISPLAY_GEOMETRY_AVAILABILITY"
    FEMA_CURRENT_HAZARD_CONTEXT = "FEMA_CURRENT_HAZARD_CONTEXT"
    EAZ_2021_CONTEXT = "EAZ_2021_CONTEXT"
    EXPECTED_FLOOD_REDUCTION_BENEFIT = "EXPECTED_FLOOD_REDUCTION_BENEFIT"
    BENEFICIARY_ESTIMATES = "BENEFICIARY_ESTIMATES"


EVIDENCE_TYPE_ROLES = MappingProxyType(
    {
        EvidenceType.GOVERNED_PROJECT_IDENTITY: EvidenceRole.FACT,
        EvidenceType.GOVERNED_REQUEST: EvidenceRole.FACT,
        EvidenceType.DERIVED_PURPOSE: EvidenceRole.FACT,
        EvidenceType.P0_FAMILY: EvidenceRole.FACT,
        EvidenceType.PROBLEM_SCORE_ASSOCIATION: EvidenceRole.CONTEXTUAL_EVIDENCE,
        EvidenceType.RNA_DISPLAY_GEOMETRY_AVAILABILITY: EvidenceRole.RESEARCH_ONLY_EVIDENCE,
        EvidenceType.FEMA_CURRENT_HAZARD_CONTEXT: EvidenceRole.CONTEXTUAL_EVIDENCE,
        EvidenceType.EAZ_2021_CONTEXT: EvidenceRole.CONTEXTUAL_EVIDENCE,
        EvidenceType.EXPECTED_FLOOD_REDUCTION_BENEFIT: EvidenceRole.UNAVAILABLE_UNSUPPORTED,
        EvidenceType.BENEFICIARY_ESTIMATES: EvidenceRole.UNAVAILABLE_UNSUPPORTED,
    }
)

EVIDENCE_TYPE_FACT_KINDS = MappingProxyType(
    {
        EvidenceType.GOVERNED_PROJECT_IDENTITY: FactKind.SOURCE_GOVERNED,
        EvidenceType.GOVERNED_REQUEST: FactKind.SOURCE_GOVERNED,
        EvidenceType.DERIVED_PURPOSE: FactKind.CLIMATE_CAPITAL_DERIVED,
        EvidenceType.P0_FAMILY: FactKind.CLIMATE_CAPITAL_DERIVED,
    }
)

_CURATABLE_AVAILABILITY = frozenset(
    {
        Availability.AVAILABLE,
        Availability.MISSING,
        Availability.NOT_APPLICABLE,
        Availability.NOT_EVALUATED_FIXTURE,
    }
)
EVIDENCE_TYPE_AVAILABILITY = MappingProxyType(
    {
        EvidenceType.GOVERNED_PROJECT_IDENTITY: frozenset({Availability.AVAILABLE}),
        EvidenceType.GOVERNED_REQUEST: frozenset({Availability.AVAILABLE}),
        EvidenceType.DERIVED_PURPOSE: frozenset({Availability.AVAILABLE}),
        EvidenceType.P0_FAMILY: frozenset({Availability.AVAILABLE}),
        EvidenceType.PROBLEM_SCORE_ASSOCIATION: _CURATABLE_AVAILABILITY,
        EvidenceType.RNA_DISPLAY_GEOMETRY_AVAILABILITY: _CURATABLE_AVAILABILITY,
        EvidenceType.FEMA_CURRENT_HAZARD_CONTEXT: _CURATABLE_AVAILABILITY,
        EvidenceType.EAZ_2021_CONTEXT: _CURATABLE_AVAILABILITY,
        EvidenceType.EXPECTED_FLOOD_REDUCTION_BENEFIT: frozenset(
            {Availability.UNSUPPORTED}
        ),
        EvidenceType.BENEFICIARY_ESTIMATES: frozenset({Availability.UNSUPPORTED}),
    }
)


class GcsObject(StrictModel):
    uri: Annotated[str, StringConstraints(pattern=r"^gs://[^/]+/.+$")]
    generation: Annotated[str, StringConstraints(pattern=r"^[1-9][0-9]*$")]
    sha256: Sha256
    byte_size: ByteSize

    @field_validator("uri")
    @classmethod
    def reject_mutable_latest_uri(cls, value: str) -> str:
        if any(part.lower() == "latest" for part in value.split("/")):
            raise ValueError("mutable 'latest' GCS pointers are forbidden")
        return value


class SourceReference(StrictModel):
    source_id: StableIdentifier
    publisher: ShortText
    title: ShortText
    source_url: Annotated[str, StringConstraints(pattern=r"^https://[^\s]+$")]
    source_vintage: ShortText
    published_date: IsoDate | None = None
    retrieval_timestamp: IsoTimestamp | None = None
    sha256: Sha256
    byte_size: ByteSize
    gcs_object: GcsObject | None
    historical_fit: HistoricalFit
    license_reuse_status: LicenseReuseStatus
    attribution_text: NonEmptyString
    known_limitations: list[ShortText] = Field(min_length=1)

    @model_validator(mode="after")
    def source_and_gcs_bytes_agree(self) -> SourceReference:
        if self.gcs_object is not None and (
            self.gcs_object.sha256 != self.sha256
            or self.gcs_object.byte_size != self.byte_size
        ):
            raise ValueError("GCS identity must match the exact governed source bytes")
        if (
            self.historical_fit == HistoricalFit.HISTORICAL_FIT_UNCERTAIN
            and self.retrieval_timestamp is None
        ):
            raise ValueError("mutable/current evidence requires a retrieval timestamp")
        return self


EvidenceScalar = int | float | str | bool


class EvidenceItem(StrictModel):
    evidence_id: StableIdentifier
    evidence_type: EvidenceType
    evidence_role: EvidenceRole
    fact_kind: FactKind | None = None
    availability: Availability
    reason_code: StableIdentifier | None = None
    explanation: NonEmptyString
    value: EvidenceScalar | None = None
    unit: ShortText | None = None
    category: ShortText | None = None
    source_ids: list[StableIdentifier] = Field(min_length=1)
    source_vintage: ShortText
    historical_fit: HistoricalFit
    association_method: ShortText | None = None
    transformation_version: StableIdentifier | None = None
    coverage_scope: ShortText
    limitations: list[ShortText] = Field(min_length=1)
    confidence: Confidence | None = None
    confidence_meaning: ShortText | None = None
    public_label: ShortText
    public_disclaimer: NonEmptyString

    @model_validator(mode="after")
    def enforce_role_and_availability(self) -> EvidenceItem:
        expected_role = EVIDENCE_TYPE_ROLES[self.evidence_type]
        if self.evidence_role != expected_role:
            raise ValueError(
                f"{self.evidence_type} requires evidence_role={expected_role}"
            )
        expected_fact_kind = EVIDENCE_TYPE_FACT_KINDS.get(self.evidence_type)
        if self.fact_kind != expected_fact_kind:
            if expected_fact_kind is None:
                raise ValueError("fact_kind is valid only for locked FACT evidence types")
            raise ValueError(
                f"{self.evidence_type} requires fact_kind={expected_fact_kind}"
            )
        if self.availability not in EVIDENCE_TYPE_AVAILABILITY[self.evidence_type]:
            raise ValueError(
                f"{self.evidence_type} does not permit availability={self.availability}"
            )

        if self.evidence_role == EvidenceRole.UNAVAILABLE_UNSUPPORTED and self.availability not in {
            Availability.MISSING,
            Availability.UNSUPPORTED,
            Availability.NOT_APPLICABLE,
            Availability.NOT_EVALUATED_FIXTURE,
        }:
            raise ValueError("unavailable/unsupported evidence cannot be AVAILABLE")
        if (
            self.availability == Availability.UNSUPPORTED
            and self.evidence_role != EvidenceRole.UNAVAILABLE_UNSUPPORTED
        ):
            raise ValueError("UNSUPPORTED availability requires UNAVAILABLE_UNSUPPORTED role")

        if self.availability == Availability.AVAILABLE:
            if self.value is None:
                raise ValueError("AVAILABLE evidence requires a value")
            if self.reason_code is not None:
                raise ValueError("AVAILABLE evidence cannot have a missingness reason")
        else:
            if self.reason_code is None:
                raise ValueError("non-AVAILABLE evidence requires a stable reason_code")
            if self.value is not None or self.unit is not None or self.category is not None:
                raise ValueError("non-AVAILABLE evidence cannot carry a value, unit, or category")

        if isinstance(self.value, float) and not math.isfinite(self.value):
            raise ValueError("evidence numbers must be finite")

        if (self.confidence is None) != (self.confidence_meaning is None):
            raise ValueError("confidence and confidence_meaning must appear together")
        if self.confidence_meaning and any(
            term in self.confidence_meaning.lower()
            for term in ("need", "severity", "benefit", "priority", "decision correctness")
        ):
            raise ValueError("confidence cannot describe need, severity, benefit, or priority")
        return self


def model_to_plain_data(model: BaseModel) -> dict[str, Any]:
    """Return strict JSON-compatible data using public aliases."""

    return model.model_dump(mode="json", by_alias=True, exclude_none=False)
