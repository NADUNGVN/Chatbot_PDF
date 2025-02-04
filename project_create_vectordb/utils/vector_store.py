from pathlib import Path
from typing import List, Dict, Any
from ..models.vector_db import VectorDB
from .embedding_utils import EmbeddingGenerator
from .chunk_loader import prepare_chunk_for_embedding
from tqdm import tqdm
import logging

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, db_path: Path):
        self.vector_db = VectorDB(db_path)
        self.embedding_generator = EmbeddingGenerator()
        
    def add_chunks(self, chunks: List[Dict]):
        """Thêm chunks vào vector store với thanh tiến trình"""
        # Chuẩn bị texts trước
        texts = []
        for chunk in chunks:
            text = prepare_chunk_for_embedding(chunk)
            texts.append(text)
            
        # Tạo embeddings với thanh tiến trình
        try:
            vectors = self.embedding_generator.create_batch_embeddings(texts)
            
            # Thêm vectors vào database với thanh tiến trình
            print("\nLưu vectors vào database...")
            for vector, chunk in tqdm(zip(vectors, chunks), total=len(chunks), desc="Lưu vectors"):
                self.vector_db.add_vector(vector, chunk)
                
        except Exception as e:
            logger.error(f"Error processing chunks: {str(e)}")
            raise
            
    def save(self):
        """Lưu vector store"""
        self.vector_db.save()
        
    def load(self):
        """Load vector store từ file"""
        try:
            logger.info("Loading vector database...")
            self.vector_db.load()
            logger.info("Vector database loaded successfully!")
        except Exception as e:
            logger.error(f"Error loading vector database: {str(e)}")
            raise
            
    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        """Tìm kiếm chunks tương tự query"""
        try:
            query_vector = self.embedding_generator.create_embedding(query)
            results = self.vector_db.search(query_vector, top_k)
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            raise
