from pathlib import Path

from datatalk.benchmarks import BenchmarkLoader



def test_load_benchmarks() -> None:
    path = Path(__file__).resolve().parents[2] / "benchmarks" / "cases"

    loader = BenchmarkLoader(path)
    cases = loader.load_all()

    assert len(cases) == 45
    assert cases[0].question
