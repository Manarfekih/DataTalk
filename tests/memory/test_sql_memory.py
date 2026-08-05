from datatalk.memory import ChromaStore, SQLMemoryService
from datatalk.models import SQLExperience


class FakeEmbedding:
    def embed(self, text: str):
        return [0.1, 0.2, 0.3]


def test_chroma_memory_creation(tmp_path):
    store = ChromaStore(
        path=str(tmp_path / "chroma"),
        collection_name="sql_experiences_test",
    )

    memory = SQLMemoryService(store=store, embedding=FakeEmbedding())

    experience = SQLExperience(
        question="How many customers?",
        original_sql="SELECT COUNT(*) FROM customer;",
        corrected_sql="SELECT COUNT(*) FROM customers;",
        error="relation customer does not exist",
        reasoning="Table name was incorrect.",
        confidence=0.95,
        detected_error="wrong table name",
        changes_made=["Changed customer to customers"],
        execution_success=False,
    )

    memory.add(experience)

    results = memory.retrieve(
        question="How many customers?",
        sql="SELECT COUNT(*) FROM customer;",
        error="relation customer does not exist",
        top_k=3,
    )

    assert len(results) == 1

    recovered = results[0]

    assert recovered.id == experience.id
    assert recovered.question == experience.question
    assert recovered.original_sql == experience.original_sql
    assert recovered.corrected_sql == experience.corrected_sql
    assert recovered.error == experience.error
    assert recovered.reasoning == experience.reasoning
    assert recovered.detected_error == experience.detected_error
    assert recovered.changes_made == experience.changes_made
    assert recovered.execution_success is False

