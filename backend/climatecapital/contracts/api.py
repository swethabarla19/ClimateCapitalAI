"""Closed, endpoint-typed same-origin HTTP response envelope contracts."""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import ConfigDict, Field, RootModel, StringConstraints, model_validator

from .artifacts import (
    BenchmarkArtifact,
    CatalogArtifact,
    ContractVersionSet,
    MapContextArtifact,
)
from .common import DataVersion, NonEmptyString, ReleaseTier, Sha256, StrictModel
from .gemini import GeminiExplainResponse
from .plans import BenchmarkComparisonResponseData, PlanEvaluationResponseData
from .versions import (
    API_NAMESPACE,
    BENCHMARK_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
    GEMINI_EXPLAIN_CONTRACT_VERSION,
)

RequestId = Annotated[
    str,
    StringConstraints(
        pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    ),
]
GitSha = Annotated[str, StringConstraints(pattern=r"^[0-9a-f]{40}$")]
ContainerDigest = Annotated[
    str, StringConstraints(pattern=r"^sha256:[0-9a-f]{64}$")
]


class ResponseIdentity(StrictModel):
    request_id: RequestId
    api_namespace: Literal[API_NAMESPACE]
    contract_version: str | None = None
    data_version: DataVersion
    release_id: Annotated[str, StringConstraints(min_length=1, max_length=200)]


class DeploymentIdentityData(StrictModel):
    code_git_sha: GitSha
    manifest_sha256: Sha256
    container_image_digest: ContainerDigest
    release_tier: ReleaseTier


class HealthResponseData(StrictModel):
    status: Literal["READY"]
    deployment_identity: DeploymentIdentityData
    contract_versions: ContractVersionSet
    gemini_enabled: bool = Field(strict=True)


class BootstrapMapDefaults(StrictModel):
    rna_current_project_display: Literal[True]
    fema_current_hazard_context: Literal[False]
    eaz_2021_context: Literal[False]


class PublicConfiguration(StrictModel):
    environment_label: Annotated[str, StringConstraints(min_length=1, max_length=100)]
    osm_tile_url: Annotated[str, StringConstraints(pattern=r"^https://[^\s]+$")]
    osm_attribution: NonEmptyString
    fixture_mode: bool = Field(strict=True)


class BootstrapResponseData(StrictModel):
    catalog: CatalogArtifact
    map_context: MapContextArtifact
    map_defaults: BootstrapMapDefaults
    public_configuration: PublicConfiguration
    deployment_identity: DeploymentIdentityData

    @model_validator(mode="after")
    def bootstrap_identity_agrees(self) -> BootstrapResponseData:
        if self.catalog.data_version != self.map_context.data_version:
            raise ValueError("bootstrap catalog and map data versions must agree")
        if self.catalog.release_tier != self.map_context.release_tier:
            raise ValueError("bootstrap catalog and map release tiers must agree")
        if self.deployment_identity.release_tier != self.catalog.release_tier:
            raise ValueError("bootstrap deployment and artifact release tiers must agree")
        if self.public_configuration.fixture_mode != (
            self.catalog.release_tier == ReleaseTier.FIXTURE
        ):
            raise ValueError("fixture-mode configuration must match artifact tier")
        return self


class BenchmarkResponseData(StrictModel):
    benchmark: BenchmarkArtifact
    deployment_identity: DeploymentIdentityData

    @model_validator(mode="after")
    def benchmark_tier_agrees(self) -> BenchmarkResponseData:
        if self.deployment_identity.release_tier != self.benchmark.release_tier:
            raise ValueError("benchmark deployment and artifact release tiers must agree")
        return self


class HealthSuccessEnvelope(StrictModel):
    endpoint: Literal["/healthz"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: HealthResponseData


class BootstrapSuccessEnvelope(StrictModel):
    endpoint: Literal["/api/v1/bootstrap"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: BootstrapResponseData

    @model_validator(mode="after")
    def identity_agrees(self) -> BootstrapSuccessEnvelope:
        if self.identity.data_version != self.data.catalog.data_version:
            raise ValueError("bootstrap envelope identity must match catalog data")
        return self


class BenchmarkSuccessEnvelope(StrictModel):
    endpoint: Literal["/api/v1/benchmark"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: BenchmarkResponseData

    @model_validator(mode="after")
    def identity_agrees(self) -> BenchmarkSuccessEnvelope:
        if self.identity.contract_version != BENCHMARK_CONTRACT_VERSION:
            raise ValueError("benchmark response contract identity is inconsistent")
        if self.identity.data_version != self.data.benchmark.data_version:
            raise ValueError("benchmark envelope identity must match benchmark data")
        return self


class PlanEvaluationSuccessEnvelope(StrictModel):
    endpoint: Literal["/api/v1/plans/evaluate"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: PlanEvaluationResponseData

    @model_validator(mode="after")
    def identity_agrees(self) -> PlanEvaluationSuccessEnvelope:
        if self.identity.contract_version != FUNDING_PLAN_CONTRACT_VERSION:
            raise ValueError("plan response contract identity is inconsistent")
        for side in (self.data.current, self.data.reference):
            if (
                side is not None
                and side.evaluated_plan is not None
                and side.evaluated_plan.data_version != self.identity.data_version
            ):
                raise ValueError("plan envelope data identity is inconsistent")
        return self


class BenchmarkComparisonSuccessEnvelope(StrictModel):
    endpoint: Literal["/api/v1/benchmark/compare"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: BenchmarkComparisonResponseData

    @model_validator(mode="after")
    def identity_agrees(self) -> BenchmarkComparisonSuccessEnvelope:
        if self.identity.contract_version != BENCHMARK_CONTRACT_VERSION:
            raise ValueError("benchmark-comparison contract identity is inconsistent")
        if self.identity.data_version != self.data.benchmark_data_version:
            raise ValueError("benchmark-comparison data identity is inconsistent")
        return self


class GeminiExplainSuccessEnvelope(StrictModel):
    endpoint: Literal["/api/v1/gemini/explain"]
    status: Literal["SUCCESS"]
    identity: ResponseIdentity
    data: GeminiExplainResponse

    @model_validator(mode="after")
    def identity_agrees(self) -> GeminiExplainSuccessEnvelope:
        if self.identity.contract_version != GEMINI_EXPLAIN_CONTRACT_VERSION:
            raise ValueError("Gemini response contract identity is inconsistent")
        if self.identity.data_version != self.data.data_version:
            raise ValueError("Gemini envelope data identity is inconsistent")
        return self


SuccessEnvelope = Annotated[
    HealthSuccessEnvelope
    | BootstrapSuccessEnvelope
    | BenchmarkSuccessEnvelope
    | PlanEvaluationSuccessEnvelope
    | BenchmarkComparisonSuccessEnvelope
    | GeminiExplainSuccessEnvelope,
    Field(discriminator="endpoint"),
]


class ApiSuccessEnvelope(RootModel[SuccessEnvelope]):
    """Closed union of every permitted successful P0 endpoint payload."""

    model_config = ConfigDict(strict=True)


class ApiErrorDetail(StrictModel):
    error_code: Literal[
        "CONTRACT_VERSION_CONFLICT",
        "DATA_VERSION_CONFLICT",
        "MALFORMED_REQUEST",
        "UNKNOWN_FIELD",
        "INVALID_PRIMITIVE",
        "BODY_TOO_LARGE",
        "RATE_LIMITED",
        "OPTIONAL_DEPENDENCY_DISABLED",
        "OPTIONAL_DEPENDENCY_UNAVAILABLE",
        "UNEXPECTED_FAILURE",
    ]
    message: NonEmptyString
    field_path: list[str | int]
    retryable: bool = Field(strict=True)


class ApiErrorEnvelope(StrictModel):
    status: Literal["ERROR"]
    identity: ResponseIdentity
    error: ApiErrorDetail
