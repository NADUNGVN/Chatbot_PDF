import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Thư mục chứa PDF
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf")

# Thư mục output
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# Cấu hình chunk
MIN_CHUNK_SIZE = 200
MAX_CHUNK_SIZE = 1000

# Cấu hình xử lý text
REMOVE_SPECIAL_CHARS = True
NORMALIZE_WHITESPACE = True
NORMALIZE_PUNCTUATION = True
