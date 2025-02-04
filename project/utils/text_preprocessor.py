import re
from typing import List

class TextPreprocessor:
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Chuẩn hóa khoảng trắng."""
        # Thay thế nhiều khoảng trắng bằng một khoảng trắng
        text = re.sub(r'\s+', ' ', text)
        # Xóa khoảng trắng đầu và cuối
        return text.strip()

    @staticmethod
    def normalize_punctuation(text: str) -> str:
        """Chuẩn hóa dấu câu."""
        # Chuẩn hóa dấu chấm
        text = re.sub(r'\.+', '.', text)
        # Đảm bảo khoảng trắng sau dấu câu
        text = re.sub(r'([.,!?])(\w)', r'\1 \2', text)
        return text

    @staticmethod
    def remove_special_chars(text: str) -> str:
        """Loại bỏ ký tự đặc biệt không cần thiết."""
        # Giữ lại chữ, số, dấu câu cơ bản và khoảng trắng
        text = re.sub(r'[^\w\s.,!?;:()[\]{}"\'%-]', ' ', text)
        return text

    @staticmethod
    def clean_text(text: str) -> str:
        """Thực hiện tất cả các bước tiền xử lý."""
        text = TextPreprocessor.remove_special_chars(text)
        text = TextPreprocessor.normalize_punctuation(text)
        text = TextPreprocessor.normalize_whitespace(text)
        return text

    @staticmethod
    def validate_chunk_size(chunk: str, min_size: int, max_size: int) -> bool:
        """Kiểm tra kích thước chunk có hợp lệ."""
        chunk_length = len(chunk)
        return min_size <= chunk_length <= max_size
