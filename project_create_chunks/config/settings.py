import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Thư mục chứa PDF và output
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "chunks")

# Cấu hình chunk
MIN_CHUNK_SIZE = 200
MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
MIN_SECTION_LENGTH = 50

# Các section cần gộp
MERGEABLE_SECTIONS = [
    "Lệ phí",
    "Phí",
    "Thời hạn giải quyết"
]