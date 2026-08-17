from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path
from typing import Optional, Type, TypeVar

from pydantic import BaseModel

from .base import BaseLLMProvider
from .response import LLMResponse


logger = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)


class CachedLLMProvider(BaseLLMProvider):
    """File-backed cache for LLM outputs.

    Intended for evaluation runs so repeated benchmark executions can reuse
    previous model outputs instead of spending additional quota.
    """

    CACHE_VERSION = 2

    def __init__(
        self,
        inner: BaseLLMProvider | None,
        cache_dir: str | Path,
        *,
        cache_only: bool = False,
    ) -> None:
        self._inner = inner
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._cache_only = cache_only

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
    ) -> LLMResponse:
        cache_key = self._build_cache_key(
            kind="generate",
            prompt=prompt,
            temperature=temperature,
        )
        cache_file = self._cache_path(cache_key)

        cached = self._read_json(cache_file)
        if cached is not None:
            logger.info("LLM cache hit: generate %s", cache_file.name)
            return LLMResponse.model_validate(cached)

        if self._cache_only:
            raise RuntimeError(
                f"LLM cache miss in cache-only mode for {cache_file.name}. "
                "Run a warmup pass first."
            )

        if self._inner is None:
            raise RuntimeError("CachedLLMProvider requires an inner provider unless cache_only is set.")

        response = self._inner.generate(prompt=prompt, temperature=temperature)
        self._write_json(cache_file, response.model_dump())
        logger.info("LLM cache stored: generate %s", cache_file.name)
        return response

    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T],
        temperature: Optional[float] = None,
    ) -> T:
        cache_key = self._build_cache_key(
            kind="structured",
            prompt=prompt,
            temperature=temperature,
            response_model=f"{response_model.__module__}.{response_model.__qualname__}",
        )
        cache_file = self._cache_path(cache_key)

        cached = self._read_json(cache_file)
        if cached is not None:
            logger.info("LLM cache hit: structured %s", cache_file.name)
            return response_model.model_validate(cached)

        if self._cache_only:
            raise RuntimeError(
                f"LLM cache miss in cache-only mode for {cache_file.name}. "
                "Run a warmup pass first."
            )

        if self._inner is None:
            raise RuntimeError("CachedLLMProvider requires an inner provider unless cache_only is set.")

        response = self._inner.generate_structured(
            prompt=prompt,
            response_model=response_model,
            temperature=temperature,
        )
        self._write_json(cache_file, response.model_dump())
        logger.info("LLM cache stored: structured %s", cache_file.name)
        return response

    def get_model_name(self) -> str:
        if self._inner is not None:
            return self._inner.get_model_name()
        return "cache-only"

    def get_provider_name(self) -> str:
        if self._inner is not None:
            return self._inner.get_provider_name()
        return "cache-only"

    def get_available_models(self) -> list[str]:
        if self._inner is not None:
            return self._inner.get_available_models()
        return ["cache-only"]

    def _cache_path(self, cache_key: str) -> Path:
        return self._cache_dir / f"{cache_key}.json"

    def _build_cache_key(self, **payload: object) -> str:
        data = {
            "version": self.CACHE_VERSION,
            "provider": self.get_provider_name(),
            "model": self.get_model_name(),
            **payload,
        }
        blob = json.dumps(data, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()

    @staticmethod
    def _read_json(path: Path) -> dict | None:
        if not path.exists():
            return None

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    @staticmethod
    def _write_json(path: Path, data: dict) -> None:
        tmp_path = path.with_suffix(".tmp")
        with open(tmp_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False, default=str)
        tmp_path.replace(path)
