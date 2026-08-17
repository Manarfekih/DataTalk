from __future__ import annotations

from pathlib import Path

from datatalk.evaluation import BenchmarkDataset



def test_load_benchmark() -> None:
    benchmark_file = (
        Path(__file__).resolve().parents[2]
        / "benchmarks"
        / "cases"
        / "northwind_basic.json"
    )

    dataset = BenchmarkDataset.from_json(benchmark_file)

    assert len(dataset) == 5

    first = dataset.cases[0]
    assert first.question == "How many customers are there?"
