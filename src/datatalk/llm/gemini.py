from __future__ import annotations

import json
import logging
import time
from typing import Optional, TypeVar, Type

from pydantic import BaseModel, ValidationError

from google import genai
from google.genai.errors import ClientError
from google.genai.types import GenerateContentConfig

from ..config import settings
from .base import BaseLLMProvider
from .response import LLMResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


def _is_placeholder_api_key(api_key: str | None) -> bool:
    if not api_key:
        return True

    normalized = api_key.strip().upper()
    return normalized.startswith("YOUR_") or normalized in {"CHANGE_ME", "REPLACE_ME", "TODO", "TBD"}


class GeminiProvider(BaseLLMProvider):
    

    PROVIDER_NAME = "gemini"

    AVAILABLE_MODELS = [
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
        "gemini-2.0-flash-exp",
        "gemini-2.0-pro-exp",
    ]

    def __init__(self):
        api_key = settings.gemini_api_key

        if _is_placeholder_api_key(api_key):
            raise ValueError(
                "GEMINI_API_KEY is missing or still set to a placeholder. "
                "Set a real Gemini API key in .env or switch LLM_PROVIDER to qwen."
            )

        self.client = genai.Client(api_key=api_key)

        self.model_name = settings.gemini_model
        self.default_temperature = settings.gemini_temperature

        logger.info(
            "Initialized Gemini provider (model=%s)",
            self.model_name,
        )


    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        

        temperature = (
            self.default_temperature
            if temperature is None
            else temperature
        )

        start = time.perf_counter()

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=8192,
                ),
            )

        except ClientError as e:

            logger.exception("Gemini API error")

            if (
                getattr(e, "status_code", None) == 403
                or "PERMISSION_DENIED" in str(e)
            ):
                raise RuntimeError(
                    "Gemini returned PERMISSION_DENIED.\n"
                    "Check:\n"
                    "- API key\n"
                    "- AI Studio project\n"
                    "- Billing\n"
                    "- Country availability"
                ) from e

            raise

        latency_ms = (time.perf_counter() - start) * 1000

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        usage = getattr(response, "usage_metadata", None)

        return LLMResponse(
            content=text,
            provider=self.PROVIDER_NAME,
            model=self.model_name,
            prompt_tokens=getattr(usage, "prompt_token_count", None),
            completion_tokens=getattr(
                usage,
                "candidates_token_count",
                None,
            ),
            total_tokens=getattr(
                usage,
                "total_token_count",
                None,
            ),
            latency_ms=latency_ms,
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: Optional[float] = None,
    ) -> T:
       

        schema = json.dumps(
            response_model.model_json_schema(),
            indent=2,
        )

        full_prompt = f"""
{prompt}

Return ONLY valid JSON.

JSON Schema:

{schema}
"""

        response = self.generate(full_prompt, temperature)

        content = self._extract_json(response.content)

        try:
            data = json.loads(content)

        except json.JSONDecodeError as e:
            logger.error("Invalid JSON returned by Gemini")
            logger.debug(content)
            raise ValueError(
                "Gemini returned invalid JSON."
            ) from e

        try:
            return response_model.model_validate(data)

        except ValidationError as e:
            logger.error("Schema validation failed.")
            logger.debug(data)
            raise ValueError(
                "Gemini returned JSON that does not match "
                "the expected schema."
            ) from e

    def get_model_name(self) -> str:
        return self.model_name

    def get_provider_name(self) -> str:
        return self.PROVIDER_NAME

    def get_available_models(self) -> list[str]:
        return self.AVAILABLE_MODELS.copy()


    @staticmethod
    def _extract_json(text: str) -> str:
        

        text = text.strip()

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()


