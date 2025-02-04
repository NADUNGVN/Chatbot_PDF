import os
from pathlib import Path

# Thư mục gốc của dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Thư mục chứa PDF
PDF_DIR = os.path.join(BASE_DIR, "data", "pdf")

# Thư mục output
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "output")

# Kích thước tối đa của mỗi chunk
MAX_CHUNK_SIZE = 1000
