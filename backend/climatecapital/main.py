"""ClimateCapital AI FastAPI entry point for the M3 local API surface."""

from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from climatecapital.api.http import (
    MAX_REQUEST_BYTES,
    error_response,
    request_id,
    request_validation_handler,
    unexpected_error_handler,
)
from climatecapital.api.routes import router
from climatecapital.api.runtime import load_runtime_state


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.runtime = load_runtime_state()
    yield


app = FastAPI(
    title="ClimateCapital AI",
    version="1.0.0",
    lifespan=lifespan,
)


@app.middleware("http")
async def request_boundary(request: Request, call_next):
    request_id(request)
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            declared = int(content_length)
        except ValueError:
            return error_response(
                request,
                status_code=422,
                error_code="MALFORMED_REQUEST",
                message="Invalid Content-Length header.",
            )
        if declared > MAX_REQUEST_BYTES:
            return error_response(
                request,
                status_code=413,
                error_code="BODY_TOO_LARGE",
                message="Request body exceeds the endpoint limit.",
            )
    if request.method in {"POST", "PUT", "PATCH"}:
        body = await request.body()
        if len(body) > MAX_REQUEST_BYTES:
            return error_response(
                request,
                status_code=413,
                error_code="BODY_TOO_LARGE",
                message="Request body exceeds the endpoint limit.",
            )

    return await call_next(request)


app.add_exception_handler(
    RequestValidationError,
    request_validation_handler,
)
app.add_exception_handler(
    Exception,
    unexpected_error_handler,
)
app.include_router(router)
