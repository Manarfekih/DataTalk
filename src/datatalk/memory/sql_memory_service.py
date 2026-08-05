from __future__ import annotations


import logging


from datatalk.models import SQLExperience


from .embedding import EmbeddingService
from .chroma_store import ChromaStore



logger = logging.getLogger(__name__)




class SQLMemoryService:
    """
    Vector memory for successful SQL corrections.

    Stores SQL repair experiences in ChromaDB
    and retrieves similar past fixes.
    """



    def __init__(
        self,
        store: ChromaStore | None = None,
        embedding: EmbeddingService | None = None,
    ) -> None:


        self._store = (
            store
            or ChromaStore()
        )


        self._embedding = (
            embedding
            or EmbeddingService()
        )





    def add(
        self,
        experience: SQLExperience,
    ) -> None:


        document = self._build_document(
            experience
        )


        vector = self._embedding.embed(
            document
        )


        metadata = self._serialize_metadata(
            experience
        )


        self._store.collection.upsert(

            ids=[
                experience.id
            ],

            embeddings=[
                vector
            ],

            documents=[
                document
            ],

            metadatas=[
                metadata
            ],
        )


        logger.info(
            "Stored SQL experience %s",
            experience.id,
        )



  

    def retrieve(
        self,
        *,
        question: str,
        sql: str,
        error: str,
        top_k: int = 3,
    ) -> list[SQLExperience]:


        query_text = f"""
Question:
{question}

Failed SQL:
{sql}

Database Error:
{error}
"""


        vector = self._embedding.embed(
            query_text
        )


        result = (
            self._store.collection.query(
                query_embeddings=[
                    vector
                ],
                n_results=top_k,
            )
        )


        experiences: list[SQLExperience] = []


        metadatas = result.get(
            "metadatas",
            []
        )


        if not metadatas:

            return experiences



        for metadata in metadatas[0]:

            experiences.append(
                self._deserialize_metadata(
                    metadata
                )
            )



        logger.info(
            "Retrieved %d SQL experiences",
            len(experiences),
        )


        return experiences



   

    @staticmethod
    def _build_document(
        experience: SQLExperience,
    ) -> str:


        return f"""
Question:
{experience.question}

Failed SQL:
{experience.original_sql}

Database Error:
{experience.error}

Corrected SQL:
{experience.corrected_sql}

Reasoning:
{experience.reasoning}

Detected Error:
{experience.detected_error}

Changes:
{", ".join(experience.changes_made)}
"""



    @staticmethod
    def _serialize_metadata(
        experience: SQLExperience,
    ) -> dict:


        return {

            "id":
                experience.id,


            "created_at":
                experience.created_at.isoformat(),


            "question":
                experience.question,


            "original_sql":
                experience.original_sql,


            "corrected_sql":
                experience.corrected_sql,


            "error":
                experience.error,


            "reasoning":
                experience.reasoning,


            "confidence":
                experience.confidence,


            "detected_error":
                experience.detected_error,


            "changes_made":
                "|||".join(
                    experience.changes_made
                ),


            "execution_success":
                experience.execution_success,
        }



  
    @staticmethod
    def _deserialize_metadata(
        metadata: dict,
    ) -> SQLExperience:


        raw_execution_success = metadata["execution_success"]

        if isinstance(raw_execution_success, bool):
            execution_success = raw_execution_success
        elif isinstance(raw_execution_success, str):
            execution_success = raw_execution_success.lower() in {
                "true",
                "1",
                "yes",
                "y",
                "on",
            }
        else:
            execution_success = bool(raw_execution_success)

        return SQLExperience(

            id=metadata["id"],

            created_at=metadata["created_at"],

            question=metadata["question"],

            original_sql=metadata["original_sql"],

            corrected_sql=metadata["corrected_sql"],

            error=metadata["error"],

            reasoning=metadata["reasoning"],

            confidence=float(
                metadata["confidence"]
            ),

            detected_error=metadata["detected_error"],

            changes_made=(
                metadata["changes_made"].split("|||")
                if metadata["changes_made"]
                else []
            ),

            execution_success=execution_success,
        )

