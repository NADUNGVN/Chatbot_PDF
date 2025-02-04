import logging
from typing import List, Dict
import json
from ..config.settings import CHUNKS_PATH, VECTOR_DB_PATH
from ..utils.chunk_loader import load_chunks
from ..utils.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vector_database():
    """Tạo vector database từ chunks"""
    try:
        logger.info(f"Loading chunks from {CHUNKS_PATH}")
        chunks = load_chunks(CHUNKS_PATH)
        logger.info(f"Loaded {len(chunks)} chunks")
        
        vector_store = VectorStore(VECTOR_DB_PATH)
        
        logger.info("Adding chunks to vector store...")
        vector_store.add_chunks(chunks)
        
        logger.info("Saving vector store...")
        vector_store.save()
        
        logger.info("Vector database created successfully!")
        
    except Exception as e:
        logger.error(f"Error creating vector database: {str(e)}")
        raise

if __name__ == "__main__":
    create_vector_database()
