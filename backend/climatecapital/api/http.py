"""Request identity and stable typed HTTP error helpers."""

from __future__ import annotations

import uuid
from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from climatecapital.contracts.api import (
    ApiErrorDetail,
    ApiErrorEnvelope,
    ResponseIdentity,
)
from climatecapital.contracts.versions import (
    API_NAMESPACE,
    BENCHMARK_CONTRACT_VERSION,
    FUNDING_PLAN_CONTRACT_VERSION,
)

MAX_REQUEST_BYTES = 64 * 1024


def request_id(request: Request) -> str:
    existing = getattr(request.state, "request_id", None)
    if existing:
        return existing
    value = str(uuid.uuid4())
    request.state.request_id = value
    return value


def contract_version_for_path(path: str) -> str | None:
    if path == "/api/v1/plans/evaluate":
        return FUNDING_PLAN_CONTRACT_VERSION
    if path.startswith("/api/v1/benchmark"):
        return BENCHMARK_CONTRACT_VERSION
    return None


def response_identity(
    request: Request,
    *,
    contract_version: str | None = None,
) -> ResponseIdentity:
    runtime = request.app.state.runtime
    return ResponseIdentity(
        request_id=request_id(request),
        api_namespace=API_NAMESPACE,
        contract_version=contract_version,
        data_version=runtime.manifest.data_version,
        release_id=runtime.release_id,
    )


def error_response(
    request: Request,
    *,
    status_code: int,
    error_code: str,
    message: str,
    field_path: list[str | int] | None = None,
    retryable: bool = False,
) -> JSONResponse:
    envelope = ApiErrorEnvelope(
        status="ERROR",
        identity=response_identity(
            request,
            contract_version=contract_version_for_path(request.url.path),
        ),
        error=ApiErrorDetail(
            error_code=error_code,
            message=message,
            field_path=field_path or [],
            retryable=retryable,
        ),
    )
    return JSONResponse(
        status_code=status_code,
        content=envelope.model_dump(mode="json"),
    )


async def request_validation_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = exc.errors()
    first = errors[0] if errors else {}
    location = [
        part
        for part in first.get("loc", ())
        if part not in {"body", "query", "path"}
    ]

    error_type = first.get("type", "")
    input_value = first.get("input")
    if (
        location
        and location[-1] in {
            "contract_version",
            "expected_benchmark_contract_version",
        }
        and "literal" in error_type
    ):
        return error_response(
            request,
            status_code=409,
            error_code="CONTRACT_VERSION_CONFLICT",
            message="Request contract version does not match this API.",
            field_path=location,
        )

    if error_type == "extra_forbidden":
        code = "UNKNOWN_FIELD"
        message = "Request contains a field that is not permitted."
    elif error_type in {
        "int_type",
        "string_type",
        "bool_type",
        "list_type",
        "dict_type",
        "literal_error",
    }:
        code = "INVALID_PRIMITIVE"
        message = "Request contains a value with an invalid type or value."
    else:
        code = "MALFORMED_REQUEST"
        message = "Request body does not satisfy the endpoint contract."

    return error_response(
        request,
        status_code=422,
        error_code=code,
        message=message,
        field_path=location,
    )


async def unexpected_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    return error_response(
        request,
        status_code=500,
        error_code="UNEXPECTED_FAILURE",
        message="The request could not be completed.",
        retryable=False,
    )
