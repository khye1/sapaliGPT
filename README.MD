# RAG Chatbot (LangChain + ChromaDB + OpenAI gpt-5-nano)

Cách chạy nhanh:

1. Copy `.env.example` sang `.env` và thêm `OPENAI_API_KEY`.
2. `pip install -r requirements.txt`
3. Thả tài liệu (.txt hoặc .md) vào thư mục `data/`
4. Chạy nhập dữ liệu: `python3 scripts/ingest.py`
5. Khởi chạy API: `python3 app/main.py

Endpoint chính:
POST /query { "query": "..." }  
→ Trả về: { "answer": "...", "sources": [...] }

Lưu ý: Chỉ là bản mẫu, **không dùng dữ liệu nhạy cảm** trên Colab.
