# utils/chunk_loader.py
import json
from typing import List, Dict
from pathlib import Path

def load_chunks(chunks_path: Path) -> List[Dict]:
    """Load chunks từ file JSON"""
    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    return chunks

def prepare_chunk_for_embedding(chunk: Dict) -> str:
    """Chuẩn bị nội dung chunk để tạo embedding"""
    # Kết hợp các trường thành một đoạn text
    text_parts = []
    
    if "title" in chunk:
        text_parts.append(f"Tiêu đề: {chunk['title']}")
        
    if "content" in chunk:
        text_parts.append(f"Nội dung: {chunk['content']}")
        
    if "metadata" in chunk:
        meta = chunk["metadata"]
        if isinstance(meta, dict):
            meta_str = ", ".join(f"{k}: {v}" for k, v in meta.items())
            text_parts.append(f"Metadata: {meta_str}")
            
    return " ".join(text_parts)
