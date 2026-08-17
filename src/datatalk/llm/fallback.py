from __future__ import annotations

import logging
from typing import Optional, Type, TypeVar

from pydantic import BaseModel

from .base import BaseLLMProvider
from .response import LLMResponse

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class FallbackLLMProvider(BaseLLMProvider):
    """
    LLM provider with automatic fallback.

    Strategy
    --------
    1. Try the primary provider (Gemini).
    2. If it fails once, permanently switch to the fallback provider
       (Qwen) for the remainder of the application lifetime.
    """

    def __init__(
        self,
        primary: BaseLLMProvider,
        fallback: BaseLLMProvider,
    ) -> None:

        self.primary = primary
        self.fallback = fallback

        self._use_fallback = False

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
    ) -> LLMResponse:

        if self._use_fallback:
            return self.fallback.generate(
                prompt=prompt,
                temperature=temperature,
            )

        try:
            return self.primary.generate(
                prompt=prompt,
                temperature=temperature,
            )

        except Exception as exc:

            logger.warning(
                "Primary provider (%s) failed: %s",
                self.primary.get_provider_name(),
                exc,
            )

            logger.info(
                "Switching permanently to fallback provider (%s).",
                self.fallback.get_provider_name(),
            )

            self._use_fallback = True

            return self.fallback.generate(
                prompt=prompt,
                temperature=temperature,
            )

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: Optional[float] = None,
    ) -> T:

        if self._use_fallback:
            return self.fallback.generate_structured(
                prompt=prompt,
                response_model=response_model,
                temperature=temperature,
            )

        try:
            return self.primary.generate_structured(
                prompt=prompt,
                response_model=response_model,
                temperature=temperature,
            )

        except Exception as exc:

            logger.warning(
                "Primary structured generation failed: %s",
                exc,
            )

            logger.info(
                "Switching permanently to fallback provider (%s).",
                self.fallback.get_provider_name(),
            )

            self._use_fallback = True

            return self.fallback.generate_structured(
                prompt=prompt,
                response_model=response_model,
                temperature=temperature,
            )

    def get_provider_name(self) -> str:
        return "fallback"

    def get_model_name(self) -> str:

        if self._use_fallback:
            return self.fallback.get_model_name()

        return self.primary.get_model_name()

    def get_available_models(self) -> list[str]:
        return (
            self.primary.get_available_models()
            + self.fallback.get_available_models()
        )

    @property
    def using_fallback(self) -> bool:
        
        return self._use_fallback