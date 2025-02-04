# scripts/search_vectors.py
import sys
from pathlib import Path
import logging

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(str(Path(__file__).parent.parent))

from config.settings import VECTOR_DB_PATH
from utils.vector_store import VectorStore

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_vectors(query: str, top_k: int = 5):
    """Tìm kiếm trong vector database"""
    try:
        # Khởi tạo và load vector store
        vector_store = VectorStore(VECTOR_DB_PATH)
        vector_store.load()
        
        # Thực hiện tìm kiếm
        results = vector_store.search(query, top_k)
        
        # Hiển thị kết quả
        print(f"\nKết quả tìm kiếm cho query: '{query}'")
        print("-" * 50)
        
        for i, result in enumerate(results, 1):
            print(f"\nKết quả #{i} (Score: {result['score']:.4f})")
            print("Metadata:")
            for key, value in result['metadata'].items():
                print(f"  {key}: {value}")
            print("-" * 30)
            
    except Exception as e:
        logger.error(f"Error searching vectors: {str(e)}")
        raise

if __name__ == "__main__":
    # Example usage
    query = input("Nhập câu query của bạn: ")
    search_vectors(query)
