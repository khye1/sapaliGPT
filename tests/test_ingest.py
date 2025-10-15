from scripts.chunking import naive_chunk_text

def test_chunking_basic():
    text = "xin chào " * 1000
    chunks = naive_chunk_text(text, max_words=200, overlap=40)
    assert len(chunks) > 0
