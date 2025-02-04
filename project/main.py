import os
import json
from datetime import datetime
from typing import List
from .utils.pdf_reader import read_pdf_files
from .utils.text_processor import (
    extract_basic_info,
    split_into_sections,
    create_chunks_from_section
)
from .models.chunk import TextChunk
from .config.settings import PDF_DIR, OUTPUT_DIR, MAX_CHUNK_SIZE

def process_pdf_content(file_name: str, content: str) -> List[TextChunk]:
    """Xử lý nội dung PDF và tạo ra các chunk."""
    chunks = []
    
    basic_info = extract_basic_info(content)
    sections = split_into_sections(content)
    
    for section_name, section_content in sections.items():
        content_chunks = create_chunks_from_section(section_content, MAX_CHUNK_SIZE)
        
        for chunk_content in content_chunks:
            chunk = TextChunk(
                file_name=file_name,
                ma_thu_tuc=basic_info.get('ma_thu_tuc', ''),
                ten_thu_tuc=basic_info.get('ten_thu_tuc', ''),
                section=section_name,
                content=chunk_content
            )
            chunks.append(chunk)
    
    return chunks

def main():
    # Tạo thư mục output nếu chưa tồn tại
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Đọc tất cả các file PDF
    pdf_contents = read_pdf_files(PDF_DIR)
    
    # Xử lý từng file
    all_chunks = []
    for file_name, content in pdf_contents.items():
        chunks = process_pdf_content(file_name, content)
        all_chunks.extend(chunks)
    
    # Lưu kết quả
    output_file = os.path.join(
        OUTPUT_DIR,
        f"chunks_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump([chunk.to_dict() for chunk in all_chunks], f, ensure_ascii=False, indent=2)
    
    print(f"\nThống kê:")
    print(f"Tổng số file PDF: {len(pdf_contents)}")
    print(f"Tổng số chunks: {len(all_chunks)}")
    print(f"Đã lưu kết quả vào: {output_file}")

if __name__ == "__main__":
    main()
