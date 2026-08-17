from __future__ import annotations

from pydantic import BaseModel

from datatalk.llm import CachedLLMProvider, LLMResponse
from datatalk.llm.base import BaseLLMProvider


class SampleOutput(BaseModel):
    answer: str


class DummyLLM(BaseLLMProvider):
    def __init__(self) -> None:
        self.generate_calls = 0
        self.structured_calls = 0

    def generate(self, prompt: str, temperature=None) -> LLMResponse:
        self.generate_calls += 1
        return LLMResponse(
            content=f"response:{prompt}",
            provider="dummy",
            model="dummy-model",
        )

    def generate_structured(self, prompt: str, response_model, temperature=None):
        self.structured_calls += 1
        return response_model(answer=f"structured:{prompt}")

    def get_model_name(self) -> str:
        return "dummy-model"

    def get_provider_name(self) -> str:
        return "dummy"

    def get_available_models(self) -> list[str]:
        return ["dummy-model"]


def test_cached_generate_reuses_file(tmp_path) -> None:
    inner = DummyLLM()
    cached = CachedLLMProvider(inner=inner, cache_dir=tmp_path)

    first = cached.generate("hello", temperature=0.1)
    second = cached.generate("hello", temperature=0.1)

    assert first.content == second.content
    assert inner.generate_calls == 1


def test_cached_generate_structured_reuses_file(tmp_path) -> None:
    inner = DummyLLM()
    cached = CachedLLMProvider(inner=inner, cache_dir=tmp_path)

    first = cached.generate_structured(
        "hello",
        response_model=SampleOutput,
        temperature=0.1,
    )
    second = cached.generate_structured(
        "hello",
        response_model=SampleOutput,
        temperature=0.1,
    )

    assert first.answer == second.answer
    assert inner.structured_calls == 1
