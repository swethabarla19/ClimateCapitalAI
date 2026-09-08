"""Environment configuration boundary for Gemini on Vertex AI."""

from __future__ import annotations

import os
from dataclasses import dataclass


DEFAULT_GOOGLE_CLOUD_PROJECT = "climatecapital-ai"
DEFAULT_GOOGLE_CLOUD_LOCATION = "global"
DEFAULT_GEMINI_MODEL = "gemini-3.5-flash"
DEFAULT_GEMINI_TIMEOUT_SECONDS = 20.0


class GeminiConfigurationError(ValueError):
    """Reject unsafe or malformed Gemini environment configuration."""


def _enabled(value: str) -> bool:
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise GeminiConfigurationError("GEMINI_ENABLED must be true or false")


@dataclass(frozen=True, slots=True)
class GeminiSettings:
    enabled: bool
    project: str
    location: str
    model: str
    timeout_seconds: float

    @classmethod
    def from_environment(cls) -> GeminiSettings:
        project = os.getenv(
            "GOOGLE_CLOUD_PROJECT", DEFAULT_GOOGLE_CLOUD_PROJECT
        ).strip()
        location = os.getenv(
            "GOOGLE_CLOUD_LOCATION", DEFAULT_GOOGLE_CLOUD_LOCATION
        ).strip()
        model = os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL).strip()
        try:
            timeout = float(
                os.getenv(
                    "GEMINI_TIMEOUT_SECONDS",
                    str(DEFAULT_GEMINI_TIMEOUT_SECONDS),
                )
            )
        except ValueError as error:
            raise GeminiConfigurationError(
                "GEMINI_TIMEOUT_SECONDS must be numeric"
            ) from error

        if not project or not location or not model:
            raise GeminiConfigurationError(
                "Gemini project, location, and model must be non-empty"
            )
        if not 1 <= timeout <= 120:
            raise GeminiConfigurationError(
                "GEMINI_TIMEOUT_SECONDS must be between 1 and 120"
            )

        return cls(
            enabled=_enabled(os.getenv("GEMINI_ENABLED", "false")),
            project=project,
            location=location,
            model=model,
            timeout_seconds=timeout,
        )
