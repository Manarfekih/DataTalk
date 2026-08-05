from datatalk.memory.chroma_store import ChromaStore


def test_chroma_collection():

    store = ChromaStore()

    assert store.collection is not None