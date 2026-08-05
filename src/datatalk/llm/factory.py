import logging
from functools import lru_cache

from .base import BaseLLMProvider
from ..config import settings


logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def get_llm() -> BaseLLMProvider:
    
    provider = settings.llm_provider.lower().strip()

    logger.info(
        "🔧 Initializing LLM provider: %s",
        provider
    )


    # Gemini Provider

    if provider == "gemini":

        from .gemini import GeminiProvider

        return GeminiProvider()


    

    #elif provider == "ollama":

        #from .ollama import OllamaProvider

        #return OllamaProvider()


    


    else:

        raise ValueError(
            f"""
Unsupported LLM provider: '{provider}'.

Available providers:
- gemini
- ollama
- openai
"""
        )


