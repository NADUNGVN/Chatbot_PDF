import os
from pathlib import Path

# Đường dẫn cơ sở
BASE_DIR = Path("C:/Users/nguye/OneDrive/Máy tính/CHATBOT")

# Đường dẫn data
DATA_DIR = BASE_DIR / "data"
CHUNKS_PATH = DATA_DIR / "output" / "chunks_20250204_115343.json"

# Together AI settings
TOGETHER_MODEL = "togethercomputer/m2-bert-80M-32k-retrieval"
EMBEDDING_DIMENSION = 768

# Vector DB settings
VECTOR_DB_PATH = DATA_DIR / "vector_db"
VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)

# Chunk settings
MAX_CHUNK_SIZE = 1000
