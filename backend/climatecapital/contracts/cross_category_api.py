"""HTTP envelopes for the governed cross-category runtime-v2 API."""

from __future__ import annotations

from typing import Literal

from pydantic import model_validator

from .api import (
    PublicConfiguration,
    ResponseIdentity,
)
from .common import StrictModel
from .cross_category_release import (
    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
    CrossCategoryBenchmarkArtifact,
    CrossCategoryMapContextArtifact,
)
from .cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CrossCategoryPlanResult,
    CrossCategoryRuntimeCatalog,
)


class CrossCategoryRuntimeBootstrapData(
    StrictModel
):
    catalog: CrossCategoryRuntimeCatalog
    map_context: CrossCategoryMapContextArtifact
    public_configuration: PublicConfiguration


class CrossCategoryRuntimeBootstrapEnvelope(
    StrictModel
):
    endpoint: Literal[
        "/api/v1/bootstrap",
        "/api/v1/cross-category/bootstrap",
    ]

    status: Literal["SUCCESS"]

    identity: ResponseIdentity

    data: CrossCategoryRuntimeBootstrapData

    @model_validator(mode="after")
    def identity_agrees(
        self,
    ) -> (
        CrossCategoryRuntimeBootstrapEnvelope
    ):
        if (
            self.identity.contract_version
            != CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
        ):
            raise ValueError(
                "cross-category bootstrap "
                "contract identity is inconsistent"
            )

        if (
            self.identity.data_version
            != self.data.catalog.data_version
        ):
            raise ValueError(
                "cross-category bootstrap "
                "data identity is inconsistent"
            )

        if (
            self.data.catalog.data_version
            != self.data.map_context.data_version
        ):
            raise ValueError(
                "cross-category bootstrap catalog "
                "and map data identities differ"
            )

        return self


class CrossCategoryPlanSuccessEnvelope(
    StrictModel
):
    endpoint: Literal[
        "/api/v1/plans/evaluate",
        "/api/v1/cross-category/plans/evaluate",
    ]

    status: Literal["SUCCESS"]

    identity: ResponseIdentity

    data: CrossCategoryPlanResult

    @model_validator(mode="after")
    def identity_agrees(
        self,
    ) -> (
        CrossCategoryPlanSuccessEnvelope
    ):
        if (
            self.identity.contract_version
            != CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
        ):
            raise ValueError(
                "cross-category plan response "
                "contract identity is inconsistent"
            )

        if (
            self.identity.data_version
            != self.data.data_version
        ):
            raise ValueError(
                "cross-category plan response "
                "data identity is inconsistent"
            )

        return self


class CrossCategoryBenchmarkResponseData(
    StrictModel
):
    benchmark: CrossCategoryBenchmarkArtifact


class CrossCategoryBenchmarkSuccessEnvelope(
    StrictModel
):
    endpoint: Literal[
        "/api/v1/benchmark"
    ]

    status: Literal["SUCCESS"]

    identity: ResponseIdentity

    data: CrossCategoryBenchmarkResponseData

    @model_validator(mode="after")
    def identity_agrees(
        self,
    ) -> (
        CrossCategoryBenchmarkSuccessEnvelope
    ):
        if (
            self.identity.contract_version
            != CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION
        ):
            raise ValueError(
                "cross-category benchmark "
                "contract identity is inconsistent"
            )

        if (
            self.identity.data_version
            != self.data.benchmark.data_version
        ):
            raise ValueError(
                "cross-category benchmark "
                "data identity is inconsistent"
            )

        return self
