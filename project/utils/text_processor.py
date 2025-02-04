import re
import uuid
from typing import Dict, List
from datetime import datetime
from project.models.chunk import TextChunk
from project.utils.text_preprocessor import TextPreprocessor
from project.config.settings import MIN_CHUNK_SIZE, MAX_CHUNK_SIZE

class TextProcessor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()

    def extract_basic_info(self, text: str) -> Dict[str, str]:
        """Trích xuất thông tin cơ bản từ văn bản."""
        info = {}
        
        # Cải thiện regex để bắt chính xác mã thủ tục
        ma_thu_tuc_match = re.search(r'Mã thủ tục:\s*([\d.]+H\d+)', text)
        if ma_thu_tuc_match:
            info['ma_thu_tuc'] = ma_thu_tuc_match.group(1).strip()
        
        # Cải thiện regex để bắt chính xác tên thủ tục
        ten_thu_tuc_match = re.search(r'Tên thủ tục:\s*([^\n]+?)(?=\s*Cấp thực hiện|$)', text)
        if ten_thu_tuc_match:
            info['ten_thu_tuc'] = ten_thu_tuc_match.group(1).strip()
        
        return info

    def split_into_sections(self, text: str) -> Dict[str, str]:
        """Tách văn bản thành các phần chính."""
        sections = {}
        
        # Thêm pattern để tách phần Lưu ý riêng
        section_keywords = [
            "Lưu ý:",
            "Trình tự thực hiện",
            "Thành phần hồ sơ",
            "Thời hạn giải quyết",
            "Đối tượng thực hiện",
            "Cơ quan thực hiện",
            "Kết quả thực hiện",
            "Lệ phí",
            "Căn cứ pháp lý"
        ]
        
        pattern = "|".join(map(re.escape, section_keywords))
        matches = list(re.finditer(pattern, text))
        
        for i in range(len(matches)):
            section_start = matches[i].start()
            section_name = matches[i].group()
            
            if i < len(matches) - 1:
                section_end = matches[i + 1].start()
            else:
                section_end = len(text)
                
            section_content = text[section_start:section_end].strip()
            # Loại bỏ khoảng trắng thừa và chuẩn hóa text
            section_content = ' '.join(section_content.split())
            sections[section_name] = section_content
        
        return sections

    def create_chunks_from_section(self, section_content: str, file_name: str, ma_thu_tuc: str, ten_thu_tuc: str, section_name: str) -> List[TextChunk]:
        """Tạo chunks từ nội dung section."""
        chunks = []
        position = 0
        
        # Giảm kích thước chunk tối đa
        MAX_CHUNK_SIZE = 500  # Điều chỉnh giảm từ giá trị cũ
        
        # Tách đoạn văn và xử lý từng đoạn
        paragraphs = re.split(r'\n\s*\n', section_content)
        
        current_chunk = ""
        for para in paragraphs:
            para = ' '.join(para.split())  # Chuẩn hóa khoảng trắng
            
            if len(para) > MAX_CHUNK_SIZE:
                # Tách câu và xử lý từng câu
                sentences = re.split(r'(?<=[.!?])\s+', para)
                for sentence in sentences:
                    if len(current_chunk) + len(sentence) > MAX_CHUNK_SIZE:
                        if current_chunk:
                            chunk = TextChunk(
                                chunk_id=str(uuid.uuid4()),
                                file_name=file_name,
                                ma_thu_tuc=ma_thu_tuc,
                                ten_thu_tuc=ten_thu_tuc,
                                section=section_name,
                                content=current_chunk.strip(),
                                position=position
                            )
                            chunks.append(chunk)
                            position += 1
                        current_chunk = sentence
                    else:
                        current_chunk = f"{current_chunk} {sentence}".strip()
            else:
                if len(current_chunk) + len(para) > MAX_CHUNK_SIZE:
                    chunk = TextChunk(
                        chunk_id=str(uuid.uuid4()),
                        file_name=file_name,
                        ma_thu_tuc=ma_thu_tuc,
                        ten_thu_tuc=ten_thu_tuc,
                        section=section_name,
                        content=current_chunk.strip(),
                        position=position
                    )
                    chunks.append(chunk)
                    position += 1
                    current_chunk = para
                else:
                    current_chunk = f"{current_chunk} {para}".strip()
        
        # Xử lý chunk cuối cùng
        if current_chunk:
            chunk = TextChunk(
                chunk_id=str(uuid.uuid4()),
                file_name=file_name,
                ma_thu_tuc=ma_thu_tuc,
                ten_thu_tuc=ten_thu_tuc,
                section=section_name,
                content=current_chunk.strip(),
                position=position
            )
            chunks.append(chunk)
        
        return chunks

