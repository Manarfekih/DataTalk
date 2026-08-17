from __future__ import annotations

import logging
from functools import lru_cache

from datatalk.config import settings

from .base import BaseLLMProvider
from .fallback import FallbackLLMProvider
from .gemini import GeminiProvider
from .qwen import QwenProvider


def _is_placeholder_api_key(api_key: str | None) -> bool:
    if not api_key:
        return True

    normalized = api_key.strip().upper()
    return normalized.startswith("YOUR_") or normalized in {"CHANGE_ME", "REPLACE_ME", "TODO", "TBD"}

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_llm() -> BaseLLMProvider:

    provider = settings.llm_provider.lower().strip()

    logger.info(
        "Initializing LLM provider: %s",
        provider,
    )

    gemini_key_invalid = _is_placeholder_api_key(settings.gemini_api_key)

    if provider == "gemini":
        return GeminiProvider()

    if provider == "qwen":
        return QwenProvider()

    if provider == "fallback":
        if gemini_key_invalid:
            logger.warning(
                "GEMINI_API_KEY is missing or placeholder-like; using Qwen directly."
            )
            return QwenProvider()

        return FallbackLLMProvider(
            primary=GeminiProvider(),
            fallback=QwenProvider(),
        )

    raise ValueError(
        f"Unknown LLM provider: {provider}"
    )