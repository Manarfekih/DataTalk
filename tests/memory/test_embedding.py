from datatalk.memory.embedding import EmbeddingService


def test_embedding():

    embedding = EmbeddingService()

    vector = embedding.embed(
        "SELECT * FROM customers"
    )

    assert isinstance(vector, list)

    assert len(vector) > 100

    assert isinstance(vector[0], float)