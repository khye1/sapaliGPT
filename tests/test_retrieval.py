# tests/test_retrieval.py
# This is a smoke test; requires that you have ingested some data into chroma_data
import pytest
from app.retriever import RAGRetriever

def test_retrieve_smoke():
    r = RAGRetriever()
    results = r.retrieve("test", top_k=1)
    # result is a list (may be empty)
    assert isinstance(results, list)
