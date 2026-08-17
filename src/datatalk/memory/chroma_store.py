from __future__ import annotations

import logging
from pathlib import Path

import chromadb
from chromadb.api.models.Collection import Collection

logger = logging.getLogger(__name__)


def default_chroma_path() -> Path:
    

    return Path(__file__).resolve().parents[3] / "memory" / "chroma"


class ChromaStore:
    def __init__(
        self,
        path: str | Path | None = None,
        collection_name: str = "sql_experiences",
    ) -> None:
        self._path = Path(path) if path is not None else default_chroma_path()
        self._collection_name = collection_name

        self.client = chromadb.PersistentClient(path=str(self._path))

        self.collection: Collection = self.client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        logger.info("ChromaDB initialized. Collection=%s", self._collection_name)

    def count(self) -> int:
        return self.collection.count()

    def clear(self) -> None:
        self.client.delete_collection(name=self._collection_name)
        self.collection = self.client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
        )

        logger.info("Chroma collection cleared.")
