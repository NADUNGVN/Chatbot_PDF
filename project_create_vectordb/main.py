import logging
from pathlib import Path
import sys
import os
from dotenv import load_dotenv

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

from .config.settings import CHUNKS_PATH, VECTOR_DB_PATH
from .scripts.create_vectordb import create_vector_database
from .utils.vector_store import VectorStore

def initialize_system():
    """Khởi tạo hệ thống"""
    if not os.getenv("TOGETHER_API_KEY_1"):
        logger.error("TOGETHER_API_KEY_1 not found in .env file")
        sys.exit(1)
        
    if not CHUNKS_PATH.exists():
        logger.error(f"Chunks file not found at {CHUNKS_PATH}")
        sys.exit(1)
        
    VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

def main():
    """Hàm main của hệ thống"""
    try:
        initialize_system()
        
        vector_db_file = VECTOR_DB_PATH / "vectors.json"
        
        if not vector_db_file.exists():
            logger.info("Vector database not found. Creating new one...")
            create_vector_database()
        
        vector_store = VectorStore(VECTOR_DB_PATH)
        vector_store.load()
        
        while True:
            print("\n=== Vector Database Search System ===")
            print("1. Tìm kiếm")
            print("2. Tạo lại vector database")
            print("3. Thoát")
            
            choice = input("\nChọn chức năng (1-3): ")
            
            if choice == "1":
                query = input("Nhập câu query của bạn: ")
                results = vector_store.search(query)
                
                print("\nKết quả tìm kiếm:")
                for i, result in enumerate(results, 1):
                    print(f"\nKết quả #{i} (Score: {result['score']:.4f})")
                    print("Metadata:")
                    for key, value in result['metadata'].items():
                        print(f"  {key}: {value}")
                    print("-" * 30)
                    
            elif choice == "2":
                confirm = input("Bạn có chắc muốn tạo lại vector database? (y/n): ")
                if confirm.lower() == 'y':
                    create_vector_database()
                    vector_store.load()
                    
            elif choice == "3":
                print("Tạm biệt!")
                break
                
            else:
                print("Lựa chọn không hợp lệ!")
                
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
