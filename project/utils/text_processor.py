import re
from typing import Dict, List
from ..models.chunk import TextChunk

def extract_basic_info(text: str) -> Dict[str, str]:
    """Trích xuất thông tin cơ bản từ văn bản."""
    info = {}
    
    ma_thu_tuc_match = re.search(r'Mã thủ tục: ([\d.]+H\d+)', text)
    if ma_thu_tuc_match:
        info['ma_thu_tuc'] = ma_thu_tuc_match.group(1)
    
    ten_thu_tuc_match = re.search(r'Tên thủ tục: ([^\n]+)', text)
    if ten_thu_tuc_match:
        info['ten_thu_tuc'] = ten_thu_tuc_match.group(1).strip()
    
    return info

def split_into_sections(text: str) -> Dict[str, str]:
    """Tách văn bản thành các phần chính."""
    sections = {}
    
    section_keywords = [
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
        sections[section_name] = section_content
    
    return sections

def create_chunks_from_section(section_content: str, max_chunk_size: int = 1000) -> List[str]:
    """Chia nội dung của một section thành các chunk nhỏ hơn."""
    chunks = []
    
    paragraphs = re.split(r'\n\s*\n', section_content)
    
    current_chunk = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        if len(para) > max_chunk_size:
            sentences = re.split(r'(?<=[.!?])\s+', para)
            for sentence in sentences:
                if len(current_chunk) + len(sentence) > max_chunk_size:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    current_chunk = sentence
                else:
                    current_chunk = (current_chunk + " " + sentence).strip()
        else:
            if len(current_chunk) + len(para) > max_chunk_size:
                chunks.append(current_chunk.strip())
                current_chunk = para
            else:
                current_chunk = (current_chunk + " " + para).strip()
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks
