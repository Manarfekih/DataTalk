from __future__ import annotations

import json
import logging
import os
import time
from typing import Optional, Type, TypeVar

import httpx
from langchain_ollama import ChatOllama
from pydantic import BaseModel

from datatalk.config import settings

from .base import BaseLLMProvider
from .response import LLMResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class QwenProvider(BaseLLMProvider):

    PROVIDER_NAME = "ollama"

    AVAILABLE_MODELS = [
        "qwen3:8b",
    ]

    def __init__(
        self,
        model: str = "qwen3:8b",
        num_gpu: int | None = None,
    ) -> None:

        self.model_name = os.getenv("QWEN_MODEL", model)
        self.num_gpu = self._resolve_num_gpu(num_gpu)
        self.base_url = getattr(
            settings,
            "ollama_base_url",
            os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        ).rstrip("/")

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
    ) -> LLMResponse:

        start = time.perf_counter()
        last_error: Exception | None = None

        for base_url in self._candidate_base_urls():
            llm = ChatOllama(
                model=self.model_name,
                base_url=base_url,
                temperature=0,
                num_gpu=self.num_gpu,
            )

            try:
                response = llm.invoke(prompt)
                self.base_url = base_url
                latency = (time.perf_counter() - start) * 1000

                return LLMResponse(
                    content=response.content,
                    provider=self.PROVIDER_NAME,
                    model=self.model_name,
                    latency_ms=latency,
                )

            except httpx.HTTPError as exc:
                last_error = exc
                logger.warning(
                    "Failed to reach Ollama at %s; trying next fallback if available.",
                    base_url,
                )

        attempted = ", ".join(self._candidate_base_urls())
        raise RuntimeError(
            f"Cannot reach Ollama at any configured endpoint ({attempted}). "
            "Start the container and ensure port 11434 is published, or set OLLAMA_BASE_URL to the correct host."
        ) from last_error

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

Schema:

{schema}
"""

        response = self.generate(
            full_prompt,
            temperature,
        )

        text = response.content.strip()

        if text.startswith("```json"):
            text = text[7:]

        if text.endswith("```"):
            text = text[:-3]

        data = json.loads(text)

        return response_model.model_validate(data)

    def get_provider_name(self) -> str:
        return self.PROVIDER_NAME

    def get_model_name(self) -> str:
        return self.model_name

    def get_available_models(self) -> list[str]:
        return self.AVAILABLE_MODELS.copy()

    def _candidate_base_urls(self) -> list[str]:
        urls: list[str] = []
        primary = self.base_url.rstrip("/")
        urls.append(primary)

        alternate = self._alternate_base_url(primary)
        if alternate and alternate not in urls:
            urls.append(alternate)

        return urls

    @staticmethod
    def _alternate_base_url(base_url: str) -> str | None:
        if "host.docker.internal" in base_url:
            return base_url.replace("host.docker.internal", "localhost")

        if "localhost" in base_url:
            return base_url.replace("localhost", "host.docker.internal")

        return None

    @staticmethod
    def _resolve_num_gpu(explicit_value: int | None) -> int | None:
        if explicit_value is not None:
            return explicit_value

        raw_value = os.getenv("QWEN_NUM_GPU")
        if raw_value is None or not raw_value.strip():
            return None

        try:
            return int(raw_value)
        except ValueError as exc:
            raise ValueError(
                "QWEN_NUM_GPU must be an integer, for example 1 to prefer a single GPU."
            ) from exc
