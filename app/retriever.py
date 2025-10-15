# app/retriever.py
import os
from dotenv import load_dotenv
import chromadb
from openai import OpenAI
from app.utils import CHROMA_PERSIST_DIR, COLLECTION_NAME, TOP_K, format_sources
from app.prompt_templates import SYSTEM_PROMPT, USER_TEMPLATE

# Load biến môi trường
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano")

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY not set")

client = OpenAI(api_key=OPENAI_API_KEY)

class RAGRetriever:
    """
    RAGRetriever: dùng để truy xuất và sinh câu trả lời dựa trên dữ liệu trong ChromaDB.
    """

    def __init__(self, persist_dir: str = CHROMA_PERSIST_DIR, collection_name: str = COLLECTION_NAME):
        # Updated ChromaDB client initialization
        self.chroma_client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.chroma_client.get_collection(name=collection_name)

    def retrieve(self, query: str, top_k: int = TOP_K):
        """
        Truy xuất tài liệu liên quan trong ChromaDB theo truy vấn người dùng.
        """
        # Tạo embedding cho truy vấn
        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=[query]
        )
        q_emb = response.data[0].embedding

        # Truy vấn ChromaDB
        results = self.collection.query(
            query_embeddings=[q_emb],
            n_results=min(top_k, 3)
        )

        docs = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        ids = results.get("ids", [[]])[0]

        return [
            {"id": ids[i], "text": docs[i], "metadata": metadatas[i]}
            for i in range(len(docs))
        ]

    def answer(self, query: str, top_k: int = TOP_K, temperature: float = 0.0):
        """
        Trả lời người dùng dựa trên context tìm được trong ChromaDB.
        """
        retrieved = self.retrieve(query, top_k=top_k)
        if not retrieved:
            return {
                "answer": "Xin lỗi, tôi không tìm thấy thông tin liên quan trong cơ sở dữ liệu.",
                "sources": [],
                "raw": None
            }

        # Kết hợp context từ các tài liệu
        context = "\n\n".join([f"[{r['id']}] {r['text']}" for r in retrieved])
        prompt = USER_TEMPLATE.format(context=context, question=query)

        # Gửi prompt đến mô hình GPT
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=512
        )

        answer_text = response.choices[0].message.content.strip()
        sources = format_sources([r["metadata"] for r in retrieved])

        return {
            "answer": answer_text,
            "sources": sources,
            "raw": response
        }