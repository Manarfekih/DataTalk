from pathlib import Path

from datatalk.memory.chroma_store import ChromaStore, default_chroma_path


def test_default_chroma_path_is_project_root_relative(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    expected = Path(__file__).resolve().parents[2] / "memory" / "chroma"

    assert default_chroma_path() == expected


def test_chroma_collection():
    store = ChromaStore()

    assert store.collection is not None
