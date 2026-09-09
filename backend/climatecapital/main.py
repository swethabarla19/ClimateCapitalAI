"""ClimateCapital AI FastAPI entry point for local and Cloud Run execution."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager, contextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from climatecapital.api.http import (
    MAX_REQUEST_BYTES,
    error_response,
    request_id,
    request_validation_handler,
    unexpected_error_handler,
)
from climatecapital.api.cross_category_runtime import (
    is_production_environment,
    load_cross_category_runtime_state,
)
from climatecapital.api.routes import router
from climatecapital.gemini import GeminiExplanationService, GeminiSettings


CONTENT_SECURITY_POLICY = "; ".join(
    (
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https://tile.openstreetmap.org",
        "font-src 'self' data:",
        "connect-src 'self'",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
        "manifest-src 'self'",
    )
)

APPLICATION_LOGGER_NAME = "climatecapital"
APPLICATION_LOG_FORMAT = "%(levelname)s:%(name)s:%(message)s"


@contextmanager
def _production_application_logging(enabled: bool):
    """Emit bounded application INFO events without changing Uvicorn logging."""

    if not enabled:
        yield
        return

    application_logger = logging.getLogger(APPLICATION_LOGGER_NAME)
    previous_level = application_logger.level
    previous_propagate = application_logger.propagate
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter(APPLICATION_LOG_FORMAT))
    application_logger.addHandler(handler)
    application_logger.setLevel(logging.INFO)
    application_logger.propagate = False
    try:
        yield
    finally:
        application_logger.removeHandler(handler)
        handler.close()
        application_logger.setLevel(previous_level)
        application_logger.propagate = previous_propagate


def default_frontend_dist_directory() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "frontend"
        / "dist"
    )


def _has_compiled_frontend(directory: Path) -> bool:
    return (
        directory.is_dir()
        and not directory.is_symlink()
        and (directory / "index.html").is_file()
    )


def _frontend_file(directory: Path, filename: str) -> FileResponse:
    path = directory / filename
    if path.is_symlink() or not path.is_file():
        raise HTTPException(status_code=404)
    return FileResponse(path)


@asynccontextmanager
async def lifespan(app: FastAPI):
    with _production_application_logging(app.state.production):
        if (
            app.state.production
            and not _has_compiled_frontend(
                app.state.frontend_dist_directory
            )
        ):
            raise RuntimeError(
                "production requires a compiled frontend/dist bundle"
            )
        app.state.cross_category_runtime = (
            load_cross_category_runtime_state()
        )
        app.state.gemini_settings = GeminiSettings.from_environment()
        app.state.gemini_service = GeminiExplanationService(
            runtime=app.state.cross_category_runtime,
            settings=app.state.gemini_settings,
        )
        yield


async def _request_boundary(request: Request, call_next):
    request_id(request)
    content_length = request.headers.get("content-length")
    if content_length:
        try:
            declared = int(content_length)
        except ValueError:
            return _with_security_headers(
                request,
                error_response(
                    request,
                    status_code=422,
                    error_code="MALFORMED_REQUEST",
                    message="Invalid Content-Length header.",
                ),
            )
        if declared > MAX_REQUEST_BYTES:
            return _with_security_headers(
                request,
                error_response(
                    request,
                    status_code=413,
                    error_code="BODY_TOO_LARGE",
                    message="Request body exceeds the endpoint limit.",
                ),
            )
    if request.method in {"POST", "PUT", "PATCH"}:
        body = await request.body()
        if len(body) > MAX_REQUEST_BYTES:
            return _with_security_headers(
                request,
                error_response(
                    request,
                    status_code=413,
                    error_code="BODY_TOO_LARGE",
                    message="Request body exceeds the endpoint limit.",
                ),
            )

    response = await call_next(request)
    return _with_security_headers(
        request,
        response,
    )


def _with_security_headers(request: Request, response):
    if request.app.state.production:
        response.headers["Content-Security-Policy"] = (
            CONTENT_SECURITY_POLICY
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = (
            "strict-origin-when-cross-origin"
        )
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000"
        )
        response.headers["X-Robots-Tag"] = (
            "noindex, nofollow, noarchive"
        )
    return response


def create_app(
    *,
    static_directory: Path | None = None,
) -> FastAPI:
    """Create the API and expose only the compiled frontend's known surfaces."""

    production = is_production_environment()
    frontend_directory = (
        static_directory
        if static_directory is not None
        else default_frontend_dist_directory()
    )
    application = FastAPI(
        title="ClimateCapital AI",
        version="1.0.0",
        lifespan=lifespan,
        docs_url=None if production else "/docs",
        redoc_url=None if production else "/redoc",
        openapi_url=None if production else "/openapi.json",
    )
    application.state.production = production
    application.state.frontend_dist_directory = frontend_directory
    application.middleware("http")(_request_boundary)
    application.add_exception_handler(
        RequestValidationError,
        request_validation_handler,
    )
    application.add_exception_handler(
        Exception,
        unexpected_error_handler,
    )
    application.include_router(router)

    if _has_compiled_frontend(frontend_directory):
        @application.get(
            "/",
            include_in_schema=False,
        )
        def frontend_index() -> FileResponse:
            return _frontend_file(
                frontend_directory,
                "index.html",
            )

        @application.get(
            "/favicon.svg",
            include_in_schema=False,
        )
        def frontend_favicon() -> FileResponse:
            return _frontend_file(
                frontend_directory,
                "favicon.svg",
            )

        @application.get(
            "/icons.svg",
            include_in_schema=False,
        )
        def frontend_icons() -> FileResponse:
            return _frontend_file(
                frontend_directory,
                "icons.svg",
            )

        @application.get(
            "/robots.txt",
            include_in_schema=False,
        )
        def frontend_robots() -> FileResponse:
            return _frontend_file(
                frontend_directory,
                "robots.txt",
            )

        assets_directory = frontend_directory / "assets"
        application.mount(
            "/assets",
            StaticFiles(
                directory=assets_directory,
            ),
            name="frontend-assets",
        )
    else:
        @application.get(
            "/",
            include_in_schema=False,
        )
        def frontend_not_built() -> JSONResponse:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "UNAVAILABLE",
                    "message": (
                        "Compiled frontend is not available; "
                        "use the Vite development server or build frontend/dist."
                    ),
                },
            )

    return application


app = create_app()
