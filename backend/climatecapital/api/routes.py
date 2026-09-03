"""M3 health/bootstrap/plan/benchmark route surface."""

from __future__ import annotations

from fastapi import APIRouter, Request

from climatecapital.api.http import error_response, response_identity
from climatecapital.benchmark.comparator import compare_plan_to_benchmark
from climatecapital.contracts.api import (
    BenchmarkResponseData,
    BenchmarkSuccessEnvelope,
    BootstrapResponseData,
    BootstrapSuccessEnvelope,
    HealthResponseData,
    HealthSuccessEnvelope,
    PlanEvaluationSuccessEnvelope,
)
from climatecapital.contracts.plans import (
    BenchmarkComparisonRequest,
    PlanEvaluationRequest,
)
from climatecapital.contracts.api import BenchmarkComparisonSuccessEnvelope
from climatecapital.contracts.versions import (
    BENCHMARK_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
)
from climatecapital.plans.evaluator import evaluate_plan, evaluate_plan_request

router = APIRouter()


@router.get("/healthz", response_model=HealthSuccessEnvelope)
def health(request: Request) -> HealthSuccessEnvelope:
    runtime = request.app.state.runtime
    return HealthSuccessEnvelope(
        endpoint="/healthz",
        status="SUCCESS",
        identity=response_identity(request),
        data=HealthResponseData(
            status="READY",
            deployment_identity=runtime.deployment_identity,
            contract_versions=runtime.manifest.contract_versions,
            gemini_enabled=runtime.gemini_enabled,
        ),
    )


@router.get("/api/v1/bootstrap", response_model=BootstrapSuccessEnvelope)
def bootstrap(request: Request) -> BootstrapSuccessEnvelope:
    runtime = request.app.state.runtime
    return BootstrapSuccessEnvelope(
        endpoint="/api/v1/bootstrap",
        status="SUCCESS",
        identity=response_identity(request),
        data=BootstrapResponseData(
            catalog=runtime.catalog,
            map_context=runtime.map_context,
            map_defaults=runtime.map_defaults,
            public_configuration=runtime.public_configuration,
            deployment_identity=runtime.deployment_identity,
        ),
    )


@router.post(
    "/api/v1/plans/evaluate",
    response_model=PlanEvaluationSuccessEnvelope,
)
def evaluate(
    request: Request,
    payload: PlanEvaluationRequest,
):
    runtime = request.app.state.runtime
    expected = runtime.manifest.data_version
    if payload.current.data_version != expected:
        return error_response(
            request,
            status_code=409,
            error_code="DATA_VERSION_CONFLICT",
            message="Plan data version does not match the loaded release.",
            field_path=["current", "data_version"],
        )
    if payload.reference is not None and payload.reference.data_version != expected:
        return error_response(
            request,
            status_code=409,
            error_code="DATA_VERSION_CONFLICT",
            message="Reference data version does not match the loaded release.",
            field_path=["reference", "data_version"],
        )

    result = evaluate_plan_request(runtime.catalog, payload)
    return PlanEvaluationSuccessEnvelope(
        endpoint="/api/v1/plans/evaluate",
        status="SUCCESS",
        identity=response_identity(
            request,
            contract_version=FUNDING_PLAN_CONTRACT_VERSION,
        ),
        data=result,
    )


@router.get(
    "/api/v1/benchmark",
    response_model=BenchmarkSuccessEnvelope,
)
def benchmark(request: Request):
    runtime = request.app.state.runtime
    if runtime.benchmark is None:
        return error_response(
            request,
            status_code=503,
            error_code="OPTIONAL_DEPENDENCY_UNAVAILABLE",
            message="Historical benchmark data is unavailable.",
            retryable=False,
        )
    return BenchmarkSuccessEnvelope(
        endpoint="/api/v1/benchmark",
        status="SUCCESS",
        identity=response_identity(
            request,
            contract_version=BENCHMARK_CONTRACT_VERSION,
        ),
        data=BenchmarkResponseData(
            benchmark=runtime.benchmark,
            deployment_identity=runtime.deployment_identity,
        ),
    )


@router.post(
    "/api/v1/benchmark/compare",
    response_model=BenchmarkComparisonSuccessEnvelope,
)
def benchmark_compare(
    request: Request,
    payload: BenchmarkComparisonRequest,
):
    runtime = request.app.state.runtime
    benchmark = runtime.benchmark
    if benchmark is None:
        return error_response(
            request,
            status_code=503,
            error_code="OPTIONAL_DEPENDENCY_UNAVAILABLE",
            message="Historical benchmark data is unavailable.",
            retryable=False,
        )

    if payload.plan.data_version != runtime.manifest.data_version:
        return error_response(
            request,
            status_code=409,
            error_code="DATA_VERSION_CONFLICT",
            message="Plan data version does not match the loaded release.",
            field_path=["plan", "data_version"],
        )
    if (
        payload.expected_benchmark_data_version
        != benchmark.data_version
    ):
        return error_response(
            request,
            status_code=409,
            error_code="DATA_VERSION_CONFLICT",
            message="Benchmark data version does not match the loaded release.",
            field_path=["expected_benchmark_data_version"],
        )

    evaluated = evaluate_plan(runtime.catalog, payload.plan)
    if evaluated.status != "VALID" or evaluated.evaluated_plan is None:
        first = evaluated.semantic_errors[0] if evaluated.semantic_errors else None
        return error_response(
            request,
            status_code=422,
            error_code="MALFORMED_REQUEST",
            message=(
                first.message
                if first is not None
                else "Benchmark comparison requires a valid within-budget plan."
            ),
            field_path=(first.field_path if first is not None else ["plan"]),
        )

    comparison = compare_plan_to_benchmark(
        benchmark,
        evaluated.evaluated_plan,
    )
    return BenchmarkComparisonSuccessEnvelope(
        endpoint="/api/v1/benchmark/compare",
        status="SUCCESS",
        identity=response_identity(
            request,
            contract_version=BENCHMARK_CONTRACT_VERSION,
        ),
        data=comparison,
    )
