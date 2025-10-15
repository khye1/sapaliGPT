# app/utils.py
import os
from dotenv import load_dotenv
from typing import List, Dict
load_dotenv()

OPENAI_CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL", "gpt-5-nano")
TOP_K = int(os.getenv("TOP_K", 5))
CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", "./chroma_data")
COLLECTION_NAME = "docs"

def format_sources(metadatas: List[Dict]) -> List[Dict]:
    out = []
    for md in metadatas:
        entry = {
            "source": md.get("source"),
            "chunk_id": md.get("chunk_id")
        }
        out.append(entry)
    return out
