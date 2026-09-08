"""Cross-category governed-runtime FastAPI route surface."""

from __future__ import annotations

import hashlib

from fastapi import (
    APIRouter,
    Request,
)

from climatecapital.api.http import (
    error_response,
    request_id,
    response_identity,
)
from climatecapital.contracts.api import (
    GeminiExplainSuccessEnvelope,
    HealthResponseData,
    HealthSuccessEnvelope,
)
from climatecapital.contracts.gemini import (
    GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION,
    GeminiExplanationRequest,
)
from climatecapital.gemini.provider import (
    GeminiProviderInvalidResponse,
    GeminiProviderRateLimited,
    GeminiProviderUnavailable,
)
from climatecapital.gemini.service import (
    GeminiContextInvalidError,
    GeminiContextMismatchError,
    GeminiApplicationRateLimitedError,
    GeminiDisabledError,
    GeminiTimeoutError,
)
from climatecapital.contracts.cross_category_api import (
    CrossCategoryBenchmarkResponseData,
    CrossCategoryBenchmarkSuccessEnvelope,
    CrossCategoryPlanSuccessEnvelope,
    CrossCategoryRuntimeBootstrapData,
    CrossCategoryRuntimeBootstrapEnvelope,
)
from climatecapital.contracts.cross_category_release import (
    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION,
)
from climatecapital.contracts.cross_category_runtime import (
    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION,
    CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION,
    CrossCategoryPlanInput,
)
from climatecapital.plans.cross_category_evaluator import (
    CrossCategoryPortfolioEvaluationError,
    evaluate_cross_category_plan,
)


router = APIRouter()


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------


@router.get(
    "/healthz",
    response_model=HealthSuccessEnvelope,
)
def health(
    request: Request,
) -> HealthSuccessEnvelope:
    runtime = request.app.state.runtime

    return HealthSuccessEnvelope(
        endpoint="/healthz",
        status="SUCCESS",
        identity=response_identity(
            request
        ),
        data=HealthResponseData(
            status="READY",
            deployment_identity=(
                runtime.deployment_identity
            ),
            contract_versions=(
                runtime.manifest
                .contract_versions
            ),
            gemini_enabled=(
                request.app.state.gemini_settings.enabled
            ),
        ),
    )


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------


def _bootstrap_response(
    request: Request,
    *,
    endpoint: str,
) -> CrossCategoryRuntimeBootstrapEnvelope:
    runtime = (
        request.app.state
        .cross_category_runtime
    )

    return (
        CrossCategoryRuntimeBootstrapEnvelope(
            endpoint=endpoint,
            status="SUCCESS",
            identity=response_identity(
                request,
                contract_version=(
                    CROSS_CATEGORY_CATALOG_CONTRACT_VERSION
                ),
                data_version=(
                    runtime.catalog.data_version
                ),
                release_id=(
                    runtime.release_id
                ),
            ),
            data=(
                CrossCategoryRuntimeBootstrapData(
                    catalog=runtime.catalog,
                    map_context=(
                        runtime.map_context
                    ),
                    public_configuration=(
                        runtime
                        .public_configuration
                    ),
                )
            ),
        )
    )


@router.get(
    "/api/v1/bootstrap",
    response_model=CrossCategoryRuntimeBootstrapEnvelope,
)
def bootstrap(
    request: Request,
) -> CrossCategoryRuntimeBootstrapEnvelope:
    return _bootstrap_response(
        request,
        endpoint="/api/v1/bootstrap",
    )


@router.get(
    "/api/v1/cross-category/bootstrap",
    response_model=CrossCategoryRuntimeBootstrapEnvelope,
)
def cross_category_bootstrap(
    request: Request,
) -> CrossCategoryRuntimeBootstrapEnvelope:
    return _bootstrap_response(
        request,
        endpoint=(
            "/api/v1/cross-category/bootstrap"
        ),
    )


# ---------------------------------------------------------------------------
# Funding Plan
# ---------------------------------------------------------------------------


def _evaluate_response(
    request: Request,
    payload: CrossCategoryPlanInput,
    *,
    endpoint: str,
):
    runtime = (
        request.app.state
        .cross_category_runtime
    )

    if (
        payload.data_version
        != runtime.catalog.data_version
    ):
        return error_response(
            request,
            status_code=409,
            error_code=(
                "DATA_VERSION_CONFLICT"
            ),
            message=(
                "Plan data version does not "
                "match the active "
                "cross-category release."
            ),
            field_path=[
                "data_version"
            ],
        )

    try:
        result = (
            evaluate_cross_category_plan(
                runtime.catalog,
                payload,
            )
        )

    except (
        CrossCategoryPortfolioEvaluationError
    ) as error:
        status_code = (
            409
            if error.code
            in {
                "DATA_VERSION_CONFLICT",
                "PLAN_FINGERPRINT_CONFLICT",
                "STALE_BOUNDARY_RESOLUTION",
            }
            else 422
        )

        return error_response(
            request,
            status_code=status_code,
            error_code=(
                "DATA_VERSION_CONFLICT"
                if error.code
                == "DATA_VERSION_CONFLICT"
                else "MALFORMED_REQUEST"
            ),
            message=error.message,
            field_path=[],
        )

    return CrossCategoryPlanSuccessEnvelope(
        endpoint=endpoint,
        status="SUCCESS",
        identity=response_identity(
            request,
            contract_version=(
                CROSS_CATEGORY_FUNDING_PLAN_CONTRACT_VERSION
            ),
            data_version=(
                runtime.catalog.data_version
            ),
            release_id=(
                runtime.release_id
            ),
        ),
        data=result,
    )


@router.post(
    "/api/v1/plans/evaluate",
    response_model=CrossCategoryPlanSuccessEnvelope,
)
def evaluate(
    request: Request,
    payload: CrossCategoryPlanInput,
):
    return _evaluate_response(
        request,
        payload,
        endpoint=(
            "/api/v1/plans/evaluate"
        ),
    )


@router.post(
    "/api/v1/cross-category/plans/evaluate",
    response_model=CrossCategoryPlanSuccessEnvelope,
)
def cross_category_evaluate(
    request: Request,
    payload: CrossCategoryPlanInput,
):
    return _evaluate_response(
        request,
        payload,
        endpoint=(
            "/api/v1/cross-category/"
            "plans/evaluate"
        ),
    )


# ---------------------------------------------------------------------------
# Historical benchmark
# ---------------------------------------------------------------------------


@router.get(
    "/api/v1/benchmark",
    response_model=CrossCategoryBenchmarkSuccessEnvelope,
)
def benchmark(
    request: Request,
) -> CrossCategoryBenchmarkSuccessEnvelope:
    runtime = (
        request.app.state
        .cross_category_runtime
    )

    return (
        CrossCategoryBenchmarkSuccessEnvelope(
            endpoint="/api/v1/benchmark",
            status="SUCCESS",
            identity=response_identity(
                request,
                contract_version=(
                    CROSS_CATEGORY_BENCHMARK_CONTRACT_VERSION
                ),
                data_version=(
                    runtime.benchmark
                    .data_version
                ),
                release_id=(
                    runtime.release_id
                ),
            ),
            data=(
                CrossCategoryBenchmarkResponseData(
                    benchmark=(
                        runtime.benchmark
                    ),
                )
            ),
        )
    )


@router.post(
    "/api/v1/benchmark/compare",
)
def benchmark_compare(
    request: Request,
):
    return error_response(
        request,
        status_code=503,
        error_code=(
            "OPTIONAL_DEPENDENCY_UNAVAILABLE"
        ),
        message=(
            "Cross-category historical "
            "benchmark comparison is not "
            "activated in this runtime "
            "checkpoint."
        ),
        retryable=False,
    )


# ---------------------------------------------------------------------------
# Gemini explanation
# ---------------------------------------------------------------------------


@router.post(
    "/api/v1/gemini/explain",
    response_model=GeminiExplainSuccessEnvelope,
)
async def gemini_explain(
    request: Request,
    payload: GeminiExplanationRequest,
):
    service = request.app.state.gemini_service
    active_request_id = request_id(request)
    try:
        client_host = request.client.host if request.client is not None else "unknown"
        client_key = hashlib.sha256(client_host.encode("utf-8")).hexdigest()
        result = await service.explain(
            payload,
            request_id=active_request_id,
            client_key=client_key,
        )
    except GeminiContextMismatchError:
        return error_response(
            request,
            status_code=409,
            error_code="GEMINI_CONTEXT_MISMATCH",
            message=(
                "Gemini context identity does not match the active governed runtime."
            ),
            field_path=["data_version", "release_id"],
        )
    except GeminiContextInvalidError as error:
        return error_response(
            request,
            status_code=422,
            error_code="GEMINI_CONTEXT_INVALID",
            message=str(error) or "Gemini context is invalid.",
        )
    except GeminiDisabledError:
        return error_response(
            request,
            status_code=503,
            error_code="GEMINI_DISABLED",
            message=(
                "Gemini explanations are disabled. Deterministic application "
                "features remain available."
            ),
        )
    except (GeminiProviderRateLimited, GeminiApplicationRateLimitedError):
        return error_response(
            request,
            status_code=429,
            error_code="GEMINI_RATE_LIMITED",
            message="Gemini is rate limited. Try the question again shortly.",
            retryable=True,
        )
    except GeminiProviderInvalidResponse:
        return error_response(
            request,
            status_code=502,
            error_code="GEMINI_INVALID_RESPONSE",
            message="Gemini returned an invalid structured response.",
        )
    except GeminiProviderUnavailable:
        return error_response(
            request,
            status_code=503,
            error_code="GEMINI_UNAVAILABLE",
            message=(
                "Gemini is temporarily unavailable. Project evidence and Funding "
                "Plan calculations remain available."
            ),
            retryable=True,
        )
    except GeminiTimeoutError:
        return error_response(
            request,
            status_code=504,
            error_code="GEMINI_TIMEOUT",
            message="Gemini did not respond before the configured timeout.",
            retryable=True,
        )

    return GeminiExplainSuccessEnvelope(
        endpoint="/api/v1/gemini/explain",
        status="SUCCESS",
        identity=response_identity(
            request,
            contract_version=GEMINI_EXPLANATION_RESULT_CONTRACT_VERSION,
            data_version=result.data_version,
            release_id=result.release_id,
        ),
        data=result,
    )
