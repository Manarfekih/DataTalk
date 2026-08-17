from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from datatalk.evaluation.models import EvaluationCase


class BenchmarkDataset:
    """In-memory benchmark dataset loaded from a JSON file."""

    def __init__(self, cases: Iterable[EvaluationCase]) -> None:
        self.cases = list(cases)

    def __len__(self) -> int:
        return len(self.cases)

    def __iter__(self):
        return iter(self.cases)

    def __getitem__(self, index: int) -> EvaluationCase:
        return self.cases[index]

    @classmethod
    def from_json(cls, path: str | Path) -> "BenchmarkDataset":
        return cls(load_cases_from_json(path))


class BenchmarkLoader:
    """Load all benchmark JSON files from a directory."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def load(self) -> list[EvaluationCase]:
        """Load a single benchmark JSON file."""
        return load_cases_from_json(self.path)

    def load_all(self) -> list[EvaluationCase]:
        """Load every JSON benchmark file in a directory."""
        if not self.path.exists():
            raise FileNotFoundError(f"Benchmark directory not found: {self.path}")

        if self.path.is_file():
            return self.load()

        files = sorted(self.path.glob("*.json"))
        if not files:
            raise ValueError("No benchmark JSON files found.")

        cases: list[EvaluationCase] = []
        for file_path in files:
            cases.extend(load_cases_from_json(file_path))

        return cases


def load_cases_from_json(path: str | Path) -> list[EvaluationCase]:
    """Load a list of evaluation cases from a JSON file."""
    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"Benchmark file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{file_path.name} must contain a JSON list.")

    return [EvaluationCase(**item) for item in data]
