from pathlib import Path
from typing import List, Dict, Any
from ..models.vector_db import VectorDB
from .embedding_utils import EmbeddingGenerator
from .chunk_loader import prepare_chunk_for_embedding
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, db_path: Path):
        self.vector_db = VectorDB(db_path)
        self.embedding_generator = EmbeddingGenerator()
        
    def add_chunks(self, chunks: List[Dict]):
        """Thêm chunks vào vector store"""
        for chunk in chunks:
            text = prepare_chunk_for_embedding(chunk)
            
            try:
                vector = self.embedding_generator.create_embedding(text)
                self.vector_db.add_vector(vector, chunk)
                
            except Exception as e:
                logger.error(f"Error processing chunk: {str(e)}")
                continue
                
    def save(self):
        """Lưu vector store"""
        self.vector_db.save()
        
    def load(self):
        """Load vector store"""
        self.vector_db.load()
        
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Tìm kiếm chunks tương tự query"""
        query_vector = self.embedding_generator.create_embedding(query)
        results = self.vector_db.search(query_vector, top_k)
        return results
