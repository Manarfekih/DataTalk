from __future__ import annotations


import logging

from sentence_transformers import SentenceTransformer


logger = logging.getLogger(__name__)



class EmbeddingService:
    


    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
    ) -> None:


        self._model_name = model_name

        self._model: SentenceTransformer | None = None



    @property
    def model(self) -> SentenceTransformer:
        

        if self._model is None:

            logger.info(
                "Loading embedding model: %s",
                self._model_name,
            )

            self._model = SentenceTransformer(
                self._model_name
            )


        return self._model



    def embed(
        self,
        text: str,
    ) -> list[float]:
        


        if not text.strip():

            raise ValueError(
                "Cannot embed empty text."
            )


        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )


        return embedding.tolist()



    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        


        if not texts:

            return []


        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )


        return [
            vector.tolist()
            for vector in embeddings
        ]