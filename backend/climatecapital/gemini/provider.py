"""Small production/fake provider seam for structured Vertex generation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol

from google import genai
from google.genai import errors, types
from pydantic import ValidationError

from climatecapital.contracts.gemini import GeminiProviderResponse

from .config import GeminiSettings


class GeminiProviderError(RuntimeError):
    """Base class for deliberately mapped provider failures."""


class GeminiProviderRateLimited(GeminiProviderError):
    pass


class GeminiProviderUnavailable(GeminiProviderError):
    pass


class GeminiProviderSafetyBlocked(GeminiProviderError):
    pass


class GeminiProviderInvalidResponse(GeminiProviderError):
    pass


@dataclass(frozen=True, slots=True)
class GeminiGeneration:
    response: GeminiProviderResponse
    model: str
    token_usage: dict[str, int]


class GeminiProvider(Protocol):
    async def generate(
        self,
        *,
        system_instruction: str,
        contents: str,
    ) -> GeminiGeneration: ...


class VertexGeminiProvider:
    """Lazy Vertex AI client using ADC through the official Google SDK."""

    def __init__(self, settings: GeminiSettings) -> None:
        self._settings = settings
        self._client: genai.Client | None = None

    @property
    def initialized(self) -> bool:
        return self._client is not None

    def _get_client(self) -> genai.Client:
        if self._client is None:
            self._client = genai.Client(
                vertexai=True,
                project=self._settings.project,
                location=self._settings.location,
                http_options=types.HttpOptions(api_version="v1"),
            )
        return self._client

    async def generate(
        self,
        *,
        system_instruction: str,
        contents: str,
    ) -> GeminiGeneration:
        client = self._get_client()
        try:
            response = await client.aio.models.generate_content(
                model=self._settings.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    thinking_config=types.ThinkingConfig(
                        thinking_level=types.ThinkingLevel.LOW,
                    ),
                    candidate_count=1,
                    max_output_tokens=1_200,
                    response_mime_type="application/json",
                    response_schema=GeminiProviderResponse,
                    # Intentionally no tools, Search, Maps, URL context,
                    # function calling, browsing, or code execution.
                ),
            )
        except errors.APIError as error:
            if error.code == 429:
                raise GeminiProviderRateLimited from error
            if error.code in {408, 500, 502, 503, 504}:
                raise GeminiProviderUnavailable from error
            raise GeminiProviderUnavailable from error
        except (OSError, RuntimeError) as error:
            raise GeminiProviderUnavailable from error

        prompt_feedback = getattr(response, "prompt_feedback", None)
        if (
            prompt_feedback is not None
            and prompt_feedback.block_reason
            not in {None, types.BlockedReason.BLOCKED_REASON_UNSPECIFIED}
        ):
            raise GeminiProviderSafetyBlocked

        candidates = response.candidates or []
        if candidates:
            finish_reason = candidates[0].finish_reason
            if finish_reason in {
                types.FinishReason.SAFETY,
                types.FinishReason.BLOCKLIST,
                types.FinishReason.PROHIBITED_CONTENT,
                types.FinishReason.SPII,
            }:
                raise GeminiProviderSafetyBlocked

        parsed: Any = response.parsed
        try:
            if isinstance(parsed, GeminiProviderResponse):
                provider_response = parsed
            elif parsed is not None:
                provider_response = GeminiProviderResponse.model_validate(parsed)
            else:
                provider_response = GeminiProviderResponse.model_validate_json(
                    response.text
                )
        except (ValidationError, ValueError, TypeError) as error:
            raise GeminiProviderInvalidResponse from error

        usage = response.usage_metadata
        token_usage = {}
        if usage is not None:
            for public_name, sdk_name in (
                ("prompt_tokens", "prompt_token_count"),
                ("response_tokens", "candidates_token_count"),
                ("reasoning_tokens", "thoughts_token_count"),
                ("total_tokens", "total_token_count"),
            ):
                value = getattr(usage, sdk_name, None)
                if isinstance(value, int):
                    token_usage[public_name] = value

        return GeminiGeneration(
            response=provider_response,
            model=self._settings.model,
            token_usage=token_usage,
        )
