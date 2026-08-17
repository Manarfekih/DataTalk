from __future__ import annotations

import logging
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from datatalk.evaluation import BenchmarkLoader, EvaluationReport, EvaluationRunner
from datatalk.core import container

from datatalk.llm import get_llm
from datatalk.llm.cached import CachedLLMProvider


logger = logging.getLogger(__name__)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
    )


def resolve_benchmark_dir() -> Path:
    return ROOT / "benchmarks" / "cases"


def resolve_llm_cache_dir() -> Path:
    return ROOT / ".cache" / "evaluation_llm"


def read_int_env(name: str, default: int | None = None) -> int | None:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return int(raw)


def read_bool_env(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def print_summary(summary: dict) -> None:
    print()
    print("========== Evaluation Summary ==========")
    print(f"Questions tested: {summary['total_questions']}")
    print(f"Text-to-SQL accuracy: {summary['text_to_sql_accuracy']:.2%}")
    print(f"Execution accuracy: {summary['execution_accuracy']:.2%}")
    print(f"Retry success rate: {summary['retry_success_rate']:.2%}")
    print("========================================")
    print()


def main() -> None:
    configure_logging()
    logger.info("Starting DataTalk evaluation...")

    cache_only = read_bool_env("EVAL_CACHE_ONLY", default=False)
    max_cases = read_int_env("EVAL_MAX_CASES")

    cached_llm = CachedLLMProvider(
        inner=None if cache_only else get_llm(),
        cache_dir=resolve_llm_cache_dir(),
        cache_only=cache_only,
    )

    container.initialize(llm_provider=cached_llm, force=True)
    graph = container.graph
    logger.info("DataTalk graph initialized.")
    logger.info("LLM cache directory: %s", resolve_llm_cache_dir())
    logger.info("Cache-only mode: %s", cache_only)

    benchmark_dir = resolve_benchmark_dir()
    loader = BenchmarkLoader(benchmark_dir)
    cases = loader.load_all()

    if max_cases is not None:
        cases = cases[:max_cases]
        logger.info("Limiting evaluation to first %d cases.", len(cases))

    logger.info("Loaded %d benchmark cases.", len(cases))

    runner = EvaluationRunner(graph)
    results = runner.run(cases)
    logger.info("Evaluation completed.")

    report = EvaluationReport(results)
    reports_dir = ROOT / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    json_path = reports_dir / "evaluation.json"
    markdown_path = reports_dir / "evaluation.md"

    report.save_json(json_path)
    report.save_markdown(markdown_path)

    logger.info("Reports generated:")
    logger.info("%s", json_path)
    logger.info("%s", markdown_path)

    print_summary(report.summary())


if __name__ == "__main__":
    main()

