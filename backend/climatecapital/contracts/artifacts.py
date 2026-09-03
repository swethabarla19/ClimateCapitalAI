"""Strict models for the four versioned release-data artifacts."""

from __future__ import annotations

import hashlib
from typing import Annotated, Literal

from pydantic import Field, StringConstraints, field_validator, model_validator

from .common import (
    Availability,
    ByteSize,
    Confidence,
    Count,
    DataVersion,
    EVIDENCE_TYPE_ROLES,
    EvidenceItem,
    EvidenceRole,
    EvidenceType,
    FactKind,
    HistoricalFit,
    IsoDate,
    NonEmptyString,
    PositiveWholeDollars,
    ProjectId,
    ReleaseTier,
    Sha256,
    ShortText,
    SourceReference,
    StableIdentifier,
    StrictModel,
    WholeDollars,
)
from .versions import (
    ACTIVE_FAMILY_PROJECT_COUNT,
    ACTIVE_FAMILY_PROJECT_IDS,
    ACTIVE_FAMILY_REQUEST_TOTAL_DOLLARS,
    APPROVED_MAP_LAYER_DEFAULTS,
    BENCHMARK_CONTRACT_VERSION,
    BROWSER_SESSION_CONTRACT_VERSION,
    CATALOG_CONTRACT_VERSION,
    CITYWIDE_PROJECT_ID,
    FUNDING_PLAN_CONTRACT_VERSION,
    GEMINI_EXPLAIN_CONTRACT_VERSION,
    GOVERNED_PROJECT_COUNT,
    GOVERNED_REQUEST_TOTAL_DOLLARS,
    GOVERNED_SOURCE_SEMANTIC_SHA256,
    HISTORICAL_BENCHMARK_SOURCE_ID,
    HISTORICAL_ENVELOPE_DOLLARS,
    HISTORICAL_WATERSHED_ALLOCATION_DOLLARS,
    MAP_CONTEXT_CONTRACT_VERSION,
    METHODOLOGY_VERSION,
    RELEASE_MANIFEST_CONTRACT_VERSION,
)


class ContractVersionSet(StrictModel):
    catalog: Literal[CATALOG_CONTRACT_VERSION]
    map_context: Literal[MAP_CONTEXT_CONTRACT_VERSION]
    benchmark: Literal[BENCHMARK_CONTRACT_VERSION]
    funding_plan: Literal[FUNDING_PLAN_CONTRACT_VERSION]
    browser_session: Literal[BROWSER_SESSION_CONTRACT_VERSION]
    gemini_explain: Literal[GEMINI_EXPLAIN_CONTRACT_VERSION]


class TransformationVersions(StrictModel):
    extractor: StableIdentifier
    join: StableIdentifier
    geometry: StableIdentifier
    classification: StableIdentifier
    serializer: StableIdentifier


class ArtifactIdentity(StrictModel):
    sha256: Sha256
    byte_size: ByteSize


class ArtifactIdentities(StrictModel):
    catalog_json: ArtifactIdentity = Field(alias="catalog.json")
    map_context_geojson: ArtifactIdentity = Field(alias="map-context.geojson")
    benchmark_json: ArtifactIdentity = Field(alias="benchmark.json")


class GovernedReconciliations(StrictModel):
    governed_project_count: Literal[GOVERNED_PROJECT_COUNT]
    governed_unique_project_id_count: Literal[GOVERNED_PROJECT_COUNT]
    governed_request_total_dollars: Literal[GOVERNED_REQUEST_TOTAL_DOLLARS]
    governed_source_semantic_sha256: Literal[GOVERNED_SOURCE_SEMANTIC_SHA256]
    active_family_project_ids: list[ProjectId] = Field(
        min_length=ACTIVE_FAMILY_PROJECT_COUNT,
        max_length=ACTIVE_FAMILY_PROJECT_COUNT,
    )
    active_family_project_count: Literal[ACTIVE_FAMILY_PROJECT_COUNT]
    active_family_request_total_dollars: Literal[ACTIVE_FAMILY_REQUEST_TOTAL_DOLLARS]
    whole_dollar_requests: Literal[True]
    active_family_ids_in_governed_universe: Literal[True]
    citywide_non_project_geography_without_feature: Literal[True]
    catalog_map_project_id_coverage_agrees: Literal[True]
    catalog_and_map_contain_no_benchmark_fields: Literal[True]

    @field_validator("active_family_project_ids")
    @classmethod
    def exact_active_family(cls, value: list[str]) -> list[str]:
        if value != list(ACTIVE_FAMILY_PROJECT_IDS):
            raise ValueError("active_family_project_ids must be the exact canonical family")
        return value


class EvidenceCoverageMissingness(StrictModel):
    evidence_type: EvidenceType
    evidence_role: EvidenceRole
    scope: Literal["GOVERNED_UNIVERSE", "ACTIVE_FAMILY"]
    denominator: Count
    available_count: Count
    missing_count: Count
    unsupported_count: Count
    not_applicable_count: Count
    fixture_state_count: Count

    @model_validator(mode="after")
    def counts_reconcile(self) -> EvidenceCoverageMissingness:
        if self.evidence_role != EVIDENCE_TYPE_ROLES[self.evidence_type]:
            raise ValueError(
                "manifest evidence role must match locked evidence-type semantics"
            )
        expected = (
            GOVERNED_PROJECT_COUNT
            if self.scope == "GOVERNED_UNIVERSE"
            else ACTIVE_FAMILY_PROJECT_COUNT
        )
        if self.denominator != expected:
            raise ValueError(f"{self.scope} denominator must equal {expected}")
        observed = (
            self.available_count
            + self.missing_count
            + self.unsupported_count
            + self.not_applicable_count
            + self.fixture_state_count
        )
        if observed != self.denominator:
            raise ValueError("availability counts must sum to the declared denominator")
        return self


class ManifestBenchmarkIdentity(StrictModel):
    source_id: Literal[HISTORICAL_BENCHMARK_SOURCE_ID]
    published_title: ShortText
    published_date: IsoDate
    extraction_version: StableIdentifier
    benchmark_contract_version: Literal[BENCHMARK_CONTRACT_VERSION]
    artifact_sha256: Sha256


class ReleaseManifest(StrictModel):
    contract_version: Literal[RELEASE_MANIFEST_CONTRACT_VERSION]
    data_version: DataVersion
    release_tier: ReleaseTier
    contract_versions: ContractVersionSet
    approved_source_ids: list[StableIdentifier] = Field(min_length=1)
    sources: list[SourceReference] = Field(min_length=1)
    transformation_versions: TransformationVersions
    artifacts: ArtifactIdentities
    governed_reconciliations: GovernedReconciliations
    evidence_coverage_missingness: list[EvidenceCoverageMissingness] = Field(
        min_length=len(EvidenceType) * 2,
        max_length=len(EvidenceType) * 2,
    )
    benchmark_identity: ManifestBenchmarkIdentity

    @model_validator(mode="after")
    def source_and_coverage_identity(self) -> ReleaseManifest:
        if self.approved_source_ids != sorted(set(self.approved_source_ids)):
            raise ValueError("approved_source_ids must be sorted and unique")
        source_ids = [source.source_id for source in self.sources]
        if source_ids != self.approved_source_ids:
            raise ValueError("sources must appear once in approved_source_ids order")
        coverage_keys = [
            (entry.evidence_type, entry.evidence_role, entry.scope)
            for entry in self.evidence_coverage_missingness
        ]
        if len(coverage_keys) != len(set(coverage_keys)):
            raise ValueError("evidence coverage entries must be unique by type/role/scope")
        types_and_scopes = {(entry.evidence_type, entry.scope) for entry in self.evidence_coverage_missingness}
        required = {
            (evidence_type.value, scope)
            for evidence_type in EvidenceType
            for scope in ("GOVERNED_UNIVERSE", "ACTIVE_FAMILY")
        }
        if types_and_scopes != required:
            raise ValueError("coverage requires both governed and family scopes for every evidence type")
        if self.benchmark_identity.source_id not in self.approved_source_ids:
            raise ValueError("benchmark source must be approved")
        if self.benchmark_identity.artifact_sha256 != self.artifacts.benchmark_json.sha256:
            raise ValueError("benchmark identity must match benchmark artifact checksum")
        return self


class DecisionContext(StrictModel):
    historical_decision_snapshot_date: Literal["2026-01-21"]
    historical_decision_snapshot_label: Literal["Historical Decision Snapshot"]
    historical_envelope_dollars: Literal[HISTORICAL_ENVELOPE_DOLLARS]
    historical_envelope_label: Literal["Historical Envelope"]
    historical_watershed_allocation_dollars: Literal[
        HISTORICAL_WATERSHED_ALLOCATION_DOLLARS
    ]
    historical_simulation: Literal[True]
    not_official_funding_decision: Literal[True]


class GovernedUniverseSummary(StrictModel):
    project_count: Literal[GOVERNED_PROJECT_COUNT]
    governed_request_total_dollars: Literal[GOVERNED_REQUEST_TOTAL_DOLLARS]


class ActiveFamilySummary(StrictModel):
    project_ids: list[ProjectId] = Field(
        min_length=ACTIVE_FAMILY_PROJECT_COUNT,
        max_length=ACTIVE_FAMILY_PROJECT_COUNT,
    )
    project_count: Literal[ACTIVE_FAMILY_PROJECT_COUNT]
    governed_request_total_dollars: Literal[ACTIVE_FAMILY_REQUEST_TOTAL_DOLLARS]
    provisional_climatecapital_derivation: Literal[True]
    not_city_taxonomy_or_eligibility: Literal[True]

    @field_validator("project_ids")
    @classmethod
    def exact_active_family(cls, value: list[str]) -> list[str]:
        if value != list(ACTIVE_FAMILY_PROJECT_IDS):
            raise ValueError("project_ids must be the exact canonical active family")
        return value


class SourceRow(StrictModel):
    source_id: StableIdentifier
    source_pdf_page: Annotated[int, Field(strict=True, gt=0)]
    source_table_row_order: Annotated[int, Field(strict=True, gt=0)]
    map_label: ShortText
    council_districts_source: ShortText


class PurposeFact(StrictModel):
    label: ShortText
    evidence_role: Literal[EvidenceRole.FACT]
    fact_kind: Literal[FactKind.CLIMATE_CAPITAL_DERIVED]
    confidence: Confidence
    confidence_meaning: Literal["Purpose classification strength only"]
    evidence_summary: NonEmptyString
    ambiguity_or_conflict: NonEmptyString
    transformation_version: StableIdentifier


class P0FamilyFact(StrictModel):
    member: bool = Field(strict=True)
    rationale: NonEmptyString
    evidence_role: Literal[EvidenceRole.FACT]
    fact_kind: Literal[FactKind.CLIMATE_CAPITAL_DERIVED]
    not_city_taxonomy_or_eligibility: Literal[True]
    geometry_is_not_membership_authority: Literal[True]


class ProjectRecord(StrictModel):
    project_id: ProjectId
    governed_name: ShortText
    governed_request_dollars: PositiveWholeDollars
    governed_request_source_text: Annotated[
        str, StringConstraints(pattern=r"^\$[0-9]{1,3}(?:,[0-9]{3})*$")
    ]
    source_row: SourceRow
    purpose: PurposeFact
    p0_family: P0FamilyFact
    geography_status: Literal[
        "DISPLAY_GEOMETRY_AVAILABLE",
        "DISPLAY_GEOMETRY_MISSING",
        "NON_PROJECT_GEOGRAPHY",
    ]
    program_scope: Literal["DISCRETE_PROJECT", "CITYWIDE_PROGRAM"]
    evidence: list[EvidenceItem] = Field(
        min_length=len(EvidenceType), max_length=len(EvidenceType)
    )
    provenance_refs: list[StableIdentifier] = Field(min_length=1)

    @model_validator(mode="after")
    def evidence_and_geography_contract(self) -> ProjectRecord:
        evidence_types = [item.evidence_type for item in self.evidence]
        if len(evidence_types) != len(set(evidence_types)) or set(evidence_types) != {
            item.value for item in EvidenceType
        }:
            raise ValueError("each project requires exactly one item for every P0 evidence type")
        rna = next(
            item
            for item in self.evidence
            if item.evidence_type == EvidenceType.RNA_DISPLAY_GEOMETRY_AVAILABILITY
        )
        permitted_availability = {
            "DISPLAY_GEOMETRY_AVAILABLE": {Availability.AVAILABLE},
            "DISPLAY_GEOMETRY_MISSING": {
                Availability.MISSING,
                Availability.NOT_EVALUATED_FIXTURE,
            },
            "NON_PROJECT_GEOGRAPHY": {Availability.NOT_APPLICABLE},
        }[self.geography_status]
        if rna.availability not in permitted_availability:
            raise ValueError("RNA geometry evidence availability must match geography_status")
        evidence_by_type = {item.evidence_type: item for item in self.evidence}
        if evidence_by_type[EvidenceType.GOVERNED_PROJECT_IDENTITY].value != self.project_id:
            raise ValueError("governed identity evidence must equal project_id")
        if evidence_by_type[EvidenceType.GOVERNED_REQUEST].value != self.governed_request_dollars:
            raise ValueError("governed request evidence must equal governed_request_dollars")
        if evidence_by_type[EvidenceType.DERIVED_PURPOSE].value != self.purpose.label:
            raise ValueError("derived purpose evidence must equal the purpose label")
        if evidence_by_type[EvidenceType.P0_FAMILY].value is not self.p0_family.member:
            raise ValueError("family evidence must equal the locked membership fact")
        if self.project_id == CITYWIDE_PROJECT_ID:
            if self.program_scope != "CITYWIDE_PROGRAM" or self.geography_status != "NON_PROJECT_GEOGRAPHY":
                raise ValueError("5789.150 must be a citywide program with non-project geography")
        elif self.program_scope != "DISCRETE_PROJECT":
            raise ValueError("only 5789.150 may be CITYWIDE_PROGRAM in P0")
        return self


class UnsupportedMetricDefinition(StrictModel):
    metric_id: Literal[
        "EXPECTED_FLOOD_REDUCTION_BENEFIT",
        "PEOPLE_POTENTIALLY_BENEFITING",
        "STRUCTURES_BENEFITED",
    ]
    evidence_role: Literal[EvidenceRole.UNAVAILABLE_UNSUPPORTED]
    availability: Literal[Availability.UNSUPPORTED]
    reason_code: StableIdentifier
    public_explanation: NonEmptyString


class CatalogArtifact(StrictModel):
    contract_version: Literal[CATALOG_CONTRACT_VERSION]
    data_version: DataVersion
    release_tier: ReleaseTier
    decision_context: DecisionContext
    governed_universe_summary: GovernedUniverseSummary
    active_family_summary: ActiveFamilySummary
    source_references: dict[StableIdentifier, SourceReference]
    unsupported_metric_definitions: list[UnsupportedMetricDefinition] = Field(
        min_length=3, max_length=3
    )
    projects: list[ProjectRecord] = Field(
        min_length=GOVERNED_PROJECT_COUNT, max_length=GOVERNED_PROJECT_COUNT
    )
    methodology_version: Literal[METHODOLOGY_VERSION]

    @model_validator(mode="after")
    def catalog_reconciles(self) -> CatalogArtifact:
        project_ids = [project.project_id for project in self.projects]
        if len(project_ids) != len(set(project_ids)):
            raise ValueError("catalog project IDs must be unique")
        if sum(project.governed_request_dollars for project in self.projects) != GOVERNED_REQUEST_TOTAL_DOLLARS:
            raise ValueError("catalog governed requests must reconcile to $327,970,000")
        ordered = sorted(
            self.projects, key=lambda item: item.source_row.source_table_row_order
        )
        semantic_rows = [
            "\x1f".join(
                (
                    project.source_row.source_id,
                    str(project.source_row.source_pdf_page),
                    str(project.source_row.source_table_row_order),
                    project.source_row.map_label,
                    project.project_id,
                    project.governed_name,
                    project.governed_request_source_text,
                    str(project.governed_request_dollars),
                    project.source_row.council_districts_source,
                )
            )
            for project in ordered
        ]
        semantic_sha256 = hashlib.sha256(
            "\x1e".join(semantic_rows).encode("utf-8")
        ).hexdigest()
        if semantic_sha256 != GOVERNED_SOURCE_SEMANTIC_SHA256:
            raise ValueError(
                "catalog governed identities/facts do not match the authoritative source fingerprint"
            )
        family_ids = sorted(project.project_id for project in self.projects if project.p0_family.member)
        if family_ids != list(ACTIVE_FAMILY_PROJECT_IDS):
            raise ValueError("catalog family flags must equal the exact 12-project family")
        family_total = sum(
            project.governed_request_dollars for project in self.projects if project.p0_family.member
        )
        if family_total != ACTIVE_FAMILY_REQUEST_TOTAL_DOLLARS:
            raise ValueError("catalog family requests must reconcile to $143,005,000")
        if self.active_family_summary.project_ids != family_ids:
            raise ValueError("active family summary and project flags disagree")
        source_ids = set(self.source_references)
        if any(key != value.source_id for key, value in self.source_references.items()):
            raise ValueError("source_references keys must equal embedded source IDs")
        for project in self.projects:
            referenced = set(project.provenance_refs)
            referenced.add(project.source_row.source_id)
            referenced.update(
                source_id for item in project.evidence for source_id in item.source_ids
            )
            if not referenced <= source_ids:
                raise ValueError(f"project {project.project_id} references an unknown source")
        metric_ids = [item.metric_id for item in self.unsupported_metric_definitions]
        if set(metric_ids) != {
            "EXPECTED_FLOOD_REDUCTION_BENEFIT",
            "PEOPLE_POTENTIALLY_BENEFITING",
            "STRUCTURES_BENEFITED",
        }:
            raise ValueError("all required unsupported metric definitions must be explicit")
        return self


Position = list[float]


def _validate_position(position: list[float]) -> None:
    if len(position) != 2:
        raise ValueError("RFC 7946 positions must contain longitude and latitude")
    longitude, latitude = position
    if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
        raise ValueError("GeoJSON coordinates must be WGS84 longitude/latitude")


def _validate_ring(ring: list[list[float]]) -> None:
    if len(ring) < 4:
        raise ValueError("polygon rings require at least four positions")
    for position in ring:
        _validate_position(position)
    if ring[0] != ring[-1]:
        raise ValueError("polygon rings must be closed")


class PointGeometry(StrictModel):
    type: Literal["Point"]
    coordinates: Position

    @field_validator("coordinates")
    @classmethod
    def valid_position(cls, value: Position) -> Position:
        _validate_position(value)
        return value


class MultiPointGeometry(StrictModel):
    type: Literal["MultiPoint"]
    coordinates: list[Position] = Field(min_length=1)

    @field_validator("coordinates")
    @classmethod
    def valid_positions(cls, value: list[Position]) -> list[Position]:
        for position in value:
            _validate_position(position)
        return value


class LineStringGeometry(StrictModel):
    type: Literal["LineString"]
    coordinates: list[Position] = Field(min_length=2)

    @field_validator("coordinates")
    @classmethod
    def valid_positions(cls, value: list[Position]) -> list[Position]:
        for position in value:
            _validate_position(position)
        return value


class MultiLineStringGeometry(StrictModel):
    type: Literal["MultiLineString"]
    coordinates: list[list[Position]] = Field(min_length=1)

    @field_validator("coordinates")
    @classmethod
    def valid_lines(cls, value: list[list[Position]]) -> list[list[Position]]:
        for line in value:
            if len(line) < 2:
                raise ValueError("line strings require at least two positions")
            for position in line:
                _validate_position(position)
        return value


class PolygonGeometry(StrictModel):
    type: Literal["Polygon"]
    coordinates: list[list[Position]] = Field(min_length=1)

    @field_validator("coordinates")
    @classmethod
    def valid_rings(cls, value: list[list[Position]]) -> list[list[Position]]:
        for ring in value:
            _validate_ring(ring)
        return value


class MultiPolygonGeometry(StrictModel):
    type: Literal["MultiPolygon"]
    coordinates: list[list[list[Position]]] = Field(min_length=1)

    @field_validator("coordinates")
    @classmethod
    def valid_polygons(
        cls, value: list[list[list[Position]]]
    ) -> list[list[list[Position]]]:
        for polygon in value:
            if not polygon:
                raise ValueError("polygons require at least one ring")
            for ring in polygon:
                _validate_ring(ring)
        return value


Geometry = Annotated[
    PointGeometry
    | MultiPointGeometry
    | LineStringGeometry
    | MultiLineStringGeometry
    | PolygonGeometry
    | MultiPolygonGeometry,
    Field(discriminator="type"),
]


class CrsContract(StrictModel):
    standard: Literal["RFC_7946"]
    coordinate_reference_system: Literal["EPSG:4326"]
    axis_order: Literal["longitude_latitude"]


class SourceCrsTransformation(StrictModel):
    layer_id: Literal[
        "rna_current_project_display",
        "fema_current_hazard_context",
        "eaz_2021_context",
    ]
    source_crs: ShortText
    transformation_tool: ShortText
    transformation_version: StableIdentifier
    validation: NonEmptyString
    limitations: list[ShortText] = Field(min_length=1)


class LayerDefinition(StrictModel):
    layer_id: Literal[
        "rna_current_project_display",
        "fema_current_hazard_context",
        "eaz_2021_context",
    ]
    evidence_role: EvidenceRole
    default_visible: bool = Field(strict=True)
    public_label: ShortText
    caveat: NonEmptyString


class MapFeatureProperties(StrictModel):
    feature_id: StableIdentifier
    source_feature_id: StableIdentifier
    layer_id: Literal[
        "rna_current_project_display",
        "fema_current_hazard_context",
        "eaz_2021_context",
    ]
    evidence_role: EvidenceRole
    availability: Literal[Availability.AVAILABLE]
    source_id: StableIdentifier
    source_vintage: ShortText
    historical_fit: HistoricalFit
    transformation_version: StableIdentifier
    limitations: list[ShortText] = Field(min_length=1)
    project_id: ProjectId | None = None


class MapFeature(StrictModel):
    type: Literal["Feature"]
    id: StableIdentifier
    properties: MapFeatureProperties
    geometry: Geometry

    @model_validator(mode="after")
    def feature_contract(self) -> MapFeature:
        if self.id != self.properties.feature_id:
            raise ValueError("GeoJSON feature id must equal properties.feature_id")
        if self.properties.layer_id == "rna_current_project_display":
            if self.properties.project_id is None:
                raise ValueError("RNA display features require one governed project_id")
            if self.properties.evidence_role != EvidenceRole.RESEARCH_ONLY_EVIDENCE:
                raise ValueError("RNA display geometry is research-only evidence")
        elif self.properties.evidence_role != EvidenceRole.CONTEXTUAL_EVIDENCE:
            raise ValueError("FEMA and EAZ map context must be contextual evidence")
        if self.properties.project_id == CITYWIDE_PROJECT_ID:
            raise ValueError("5789.150 cannot have a map feature")
        return self


class MapContextArtifact(StrictModel):
    type: Literal["FeatureCollection"]
    contract_version: Literal[MAP_CONTEXT_CONTRACT_VERSION]
    data_version: DataVersion
    release_tier: ReleaseTier
    crs_contract: CrsContract
    source_crs_and_transformations: list[SourceCrsTransformation] = Field(min_length=1)
    layer_definitions: list[LayerDefinition] = Field(min_length=3, max_length=3)
    features: list[MapFeature]

    @model_validator(mode="after")
    def locked_layers(self) -> MapContextArtifact:
        definitions = {definition.layer_id: definition for definition in self.layer_definitions}
        if set(definitions) != set(APPROVED_MAP_LAYER_DEFAULTS):
            raise ValueError("map must define exactly the three approved P0 layers")
        transformation_layers = [
            transformation.layer_id
            for transformation in self.source_crs_and_transformations
        ]
        if (
            len(transformation_layers) != len(set(transformation_layers))
            or set(transformation_layers) != set(APPROVED_MAP_LAYER_DEFAULTS)
        ):
            raise ValueError(
                "map requires exactly one source CRS/transformation record per approved layer"
            )
        for layer_id, expected_default in APPROVED_MAP_LAYER_DEFAULTS.items():
            definition = definitions[layer_id]
            if definition.default_visible is not expected_default:
                raise ValueError(f"invalid default visibility for {layer_id}")
            expected_role = (
                EvidenceRole.RESEARCH_ONLY_EVIDENCE
                if layer_id == "rna_current_project_display"
                else EvidenceRole.CONTEXTUAL_EVIDENCE
            )
            if definition.evidence_role != expected_role:
                raise ValueError(f"invalid evidence role for {layer_id}")
        feature_ids = [feature.id for feature in self.features]
        if len(feature_ids) != len(set(feature_ids)):
            raise ValueError("map feature IDs must be unique")
        rna_project_ids = [
            feature.properties.project_id
            for feature in self.features
            if feature.properties.layer_id == "rna_current_project_display"
        ]
        if len(rna_project_ids) != len(set(rna_project_ids)):
            raise ValueError("each project may have at most one RNA display feature")
        return self


class BenchmarkPublishedIdentity(StrictModel):
    source_id: Literal[HISTORICAL_BENCHMARK_SOURCE_ID]
    published_title: ShortText
    published_date: IsoDate
    source_snapshot_sha256: Sha256
    extraction_version: StableIdentifier


class PublishedMoneyValue(StrictModel):
    availability: Availability
    value_dollars: WholeDollars | None = None
    source_text: ShortText | None = None
    unit: Literal["USD"]
    reason_code: StableIdentifier | None = None
    explanation: NonEmptyString

    @model_validator(mode="after")
    def availability_controls_value(self) -> PublishedMoneyValue:
        if self.availability == Availability.AVAILABLE:
            if self.value_dollars is None or self.source_text is None:
                raise ValueError("available published money requires value and source text")
            if self.reason_code is not None:
                raise ValueError("available published money cannot have a reason_code")
        elif (
            self.value_dollars is not None
            or self.source_text is not None
            or self.reason_code is None
        ):
            raise ValueError("unavailable published money requires only a reason_code")
        return self


class PublishedCountValue(StrictModel):
    availability: Availability
    value: Count | None = None
    reason_code: StableIdentifier | None = None
    explanation: NonEmptyString

    @model_validator(mode="after")
    def availability_controls_value(self) -> PublishedCountValue:
        if self.availability == Availability.AVAILABLE:
            if self.value is None or self.reason_code is not None:
                raise ValueError(
                    "available published count requires a value and no reason_code"
                )
        elif self.value is not None or self.reason_code is None:
            raise ValueError("unavailable published count requires only a reason_code")
        return self


class PublishedTreatmentValue(StrictModel):
    availability: Availability
    value: Literal[
        "HISTORICALLY_RECOMMENDED",
        "NOT_HISTORICALLY_RECOMMENDED",
        "CITY_INCLUDED",
        "NOT_CITY_INCLUDED",
        "OTHER_PUBLISHED_TREATMENT",
    ] | None = None
    reason_code: StableIdentifier | None = None
    explanation: NonEmptyString

    @model_validator(mode="after")
    def availability_controls_value(self) -> PublishedTreatmentValue:
        if self.availability == Availability.AVAILABLE:
            if self.value is None or self.reason_code is not None:
                raise ValueError(
                    "available City treatment requires a value and no reason_code"
                )
        elif self.value is not None or self.reason_code is None:
            raise ValueError("unavailable City treatment requires only a reason_code")
        return self


class PublishedPortfolioSummary(StrictModel):
    published_allocation: PublishedMoneyValue
    city_included_count: PublishedCountValue
    explanation: NonEmptyString


class PublishedProjectTreatment(StrictModel):
    entry_id: StableIdentifier
    governed_project_id: ProjectId | None = None
    published_project_name: ShortText
    city_treatment: PublishedTreatmentValue
    published_amount: PublishedMoneyValue
    source_ids: list[StableIdentifier] = Field(min_length=1)
    limitations: list[ShortText] = Field(min_length=1)

class BenchmarkReconciliation(StrictModel):
    entry_count: Count
    available_amount_total_dollars: WholeDollars
    publication_reconciliation_passed: Literal[True]
    explanation: NonEmptyString


class BenchmarkArtifact(StrictModel):
    contract_version: Literal[BENCHMARK_CONTRACT_VERSION]
    data_version: DataVersion
    release_tier: ReleaseTier
    benchmark_identity: BenchmarkPublishedIdentity
    source_references: dict[StableIdentifier, SourceReference]
    published_portfolio_summary: PublishedPortfolioSummary
    published_project_treatments: list[PublishedProjectTreatment]
    transformation_version: StableIdentifier
    limitations: list[ShortText] = Field(min_length=1)
    reconciliation: BenchmarkReconciliation

    @model_validator(mode="after")
    def benchmark_reconciles(self) -> BenchmarkArtifact:
        if any(key != value.source_id for key, value in self.source_references.items()):
            raise ValueError("benchmark source keys must equal embedded source IDs")
        if self.benchmark_identity.source_id not in self.source_references:
            raise ValueError("benchmark identity source must be present")
        if set(self.source_references) != {self.benchmark_identity.source_id}:
            raise ValueError("benchmark artifact may contain only its isolated benchmark source")
        source_ids = set(self.source_references)
        entry_ids = [entry.entry_id for entry in self.published_project_treatments]
        if len(entry_ids) != len(set(entry_ids)):
            raise ValueError("benchmark entry IDs must be unique")
        if any(not set(entry.source_ids) <= source_ids for entry in self.published_project_treatments):
            raise ValueError("benchmark treatment references an unknown benchmark source")
        if self.reconciliation.entry_count != len(self.published_project_treatments):
            raise ValueError("benchmark entry count does not reconcile")
        total = sum(
            entry.published_amount.value_dollars or 0
            for entry in self.published_project_treatments
            if entry.published_amount.availability == Availability.AVAILABLE
        )
        if self.reconciliation.available_amount_total_dollars != total:
            raise ValueError("benchmark available amount total does not reconcile")
        return self
