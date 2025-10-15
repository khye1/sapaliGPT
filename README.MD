# RAG Chatbot (LangChain + ChromaDB + OpenAI gpt-5-nano)

Cách chạy nhanh:

1. Copy `.env.example` sang `.env` và thêm `OPENAI_API_KEY`.
2. `pip install -r requirements.txt`
3. Thả tài liệu (.txt hoặc .md) vào thư mục `data/`
4. Chạy nhập dữ liệu: `python scripts/ingest.py`
5. Khởi chạy API: `python app/main.py` hoặc `uvicorn app.main:app --reload --port 8000`

Endpoint chính:
POST /query { "query": "..." }  
→ Trả về: { "answer": "...", "sources": [...] }

Lưu ý: Chỉ là bản mẫu, **không dùng dữ liệu nhạy cảm** trên Colab.

rag-chatbot/
├── README.md
├── requirements.txt
├── .env.example
├── data/ # Thư mục chứa tài liệu nguồn (txt/md/pdf)
├── chroma_data/ # Thư mục lưu trữ CSDL vector (bỏ qua khi push git)
├── scripts/
│ ├── ingest.py # Tiền xử lý + nhúng dữ liệu
│ ├── chunking.py # Cắt đoạn văn bản
│ ├── embeddings.py # Sinh vector embedding
│ └── eval.py # Đánh giá kết quả
├── app/
│ ├── main.py # API FastAPI chính
│ ├── retriever.py # Module truy xuất dữ liệu từ ChromaDB
│ ├── prompt_templates.py # Mẫu prompt cho LLM
│ └── utils.py # Các hàm tiện ích
├── tests/
│ ├── test_ingest.py
│ └── test_retrieval.py
└── docker/
├── Dockerfile
└── docker-compose.yml
