import re
from typing import Dict, List
from datetime import datetime

class TextChunk:
    def __init__(self, content: str, metadata: Dict):
        self.content = content
        self.metadata = metadata

class TextProcessor:
    def __init__(self):
        self.min_chunk_size = 200
        self.max_chunk_size = 1000
        self.overlap_size = 100
        
    def extract_procedure_info(self, text: str) -> Dict:
        """Trích xuất thông tin thủ tục từ văn bản"""
        info = {
            'ma_thu_tuc': '',
            'ten_thu_tuc': '',
            'cap_thuc_hien': '',
            'linh_vuc': ''
        }
        
        # Tìm mã thủ tục
        ma_thu_tuc_match = re.search(r'Mã thủ tục:\s*([^\n]+)', text)
        if ma_thu_tuc_match:
            info['ma_thu_tuc'] = ma_thu_tuc_match.group(1).strip()
            
        # Tìm tên thủ tục
        ten_thu_tuc_match = re.search(r'Tên thủ tục:\s*([^\n]+)', text)
        if ten_thu_tuc_match:
            info['ten_thu_tuc'] = ten_thu_tuc_match.group(1).strip()
            
        # Tìm cấp thực hiện
        cap_match = re.search(r'Cấp thực hiện:\s*([^\n]+)', text)
        if cap_match:
            info['cap_thuc_hien'] = cap_match.group(1).strip()
            
        # Tìm lĩnh vực
        linh_vuc_match = re.search(r'Lĩnh vực:\s*([^\n]+)', text)
        if linh_vuc_match:
            info['linh_vuc'] = linh_vuc_match.group(1).strip()
            
        return info

    def split_into_sections(self, text: str) -> Dict[str, str]:
        """Tách văn bản thành các section dựa trên các tiêu đề"""
        sections = {}
        current_section = "Thông tin chung"
        current_content = []
        
        # Danh sách các tiêu đề section cần nhận diện
        section_headers = [
            "Trình tự thực hiện",
            "Cách thức thực hiện",
            "Thành phần hồ sơ",
            "Thời hạn giải quyết",
            "Phí, lệ phí",
            "Căn cứ pháp lý",
            "Yêu cầu, điều kiện thực hiện"
        ]
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Kiểm tra xem line có phải là tiêu đề section không
            is_header = False
            for header in section_headers:
                if line.lower().startswith(header.lower()):
                    # Lưu section hiện tại
                    if current_content:
                        sections[current_section] = '\n'.join(current_content)
                    # Bắt đầu section mới
                    current_section = header
                    current_content = []
                    is_header = True
                    break
            
            if not is_header:
                current_content.append(line)
        
        # Lưu section cuối cùng
        if current_content:
            sections[current_section] = '\n'.join(current_content)
        
        return sections

    def split_into_paragraphs(self, text: str) -> List[str]:
        """Tách văn bản thành các đoạn có ý nghĩa"""
        # Tách theo dấu xuống dòng kép hoặc nhiều hơn
        paragraphs = re.split(r'\n\s*\n', text)
        # Loại bỏ khoảng trắng thừa và các đoạn trống
        return [p.strip() for p in paragraphs if p.strip()]

    def split_long_paragraph(self, paragraph: str) -> List[str]:
        """Chia đoạn dài thành các chunk nhỏ hơn"""
        chunks = []
        words = paragraph.split()
        current_chunk = []
        current_length = 0
        
        for word in words:
            word_len = len(word) + 1  # +1 cho khoảng trắng
            if current_length + word_len > self.max_chunk_size:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))
                    # Thêm overlap
                    overlap_words = current_chunk[-self.overlap_size:] if self.overlap_size < len(current_chunk) else current_chunk
                    current_chunk = overlap_words + [word]
                    current_length = sum(len(w) + 1 for w in current_chunk)
                else:
                    chunks.append(word)
                    current_chunk = []
                    current_length = 0
            else:
                current_chunk.append(word)
                current_length += word_len
        
        if current_chunk:
            chunks.append(' '.join(current_chunk))
        
        return chunks

    def create_chunk(self, content: str, metadata: Dict) -> Dict:
        """Tạo chunk mới với metadata"""
        return {
            "content": content.strip(),
            "metadata": metadata
        }

    def process_text(self, text: str, metadata: Dict) -> List[Dict]:
        # Trích xuất thông tin thủ tục
        procedure_info = self.extract_procedure_info(text)
        
        # Cập nhật metadata với thông tin thủ tục
        metadata.update(procedure_info)
        
        # Tách văn bản thành các section
        sections = self.split_into_sections(text)
        chunks = []
        
        for section_name, section_content in sections.items():
            # Tách section thành các đoạn có ý nghĩa
            paragraphs = self.split_into_paragraphs(section_content)
            
            current_chunk = []
            current_length = 0
            
            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                    
                # Nếu đoạn quá dài, chia nhỏ
                if len(para) > self.max_chunk_size:
                    # Xử lý chunk hiện tại nếu có
                    if current_chunk:
                        chunk_content = "\n".join(current_chunk)
                        chunk_metadata = {
                            **metadata,
                            "section_name": section_name
                        }
                        chunks.append(self.create_chunk(chunk_content, chunk_metadata))
                        current_chunk = []
                        current_length = 0
                    
                    # Chia đoạn dài
                    para_chunks = self.split_long_paragraph(para)
                    for p_chunk in para_chunks:
                        chunk_metadata = {
                            **metadata,
                            "section_name": section_name
                        }
                        chunks.append(self.create_chunk(p_chunk, chunk_metadata))
                else:
                    # Thêm đoạn vào chunk hiện tại hoặc tạo chunk mới
                    if current_length + len(para) > self.max_chunk_size:
                        chunk_content = "\n".join(current_chunk)
                        chunk_metadata = {
                            **metadata,
                            "section_name": section_name
                        }
                        chunks.append(self.create_chunk(chunk_content, chunk_metadata))
                        current_chunk = [para]
                        current_length = len(para)
                    else:
                        current_chunk.append(para)
                        current_length += len(para)
            
            # Xử lý chunk cuối cùng của section
            if current_chunk:
                chunk_content = "\n".join(current_chunk)
                chunk_metadata = {
                    **metadata,
                    "section_name": section_name
                }
                chunks.append(self.create_chunk(chunk_content, chunk_metadata))
        
        return chunks