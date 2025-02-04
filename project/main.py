import os
import json
from datetime import datetime
from typing import List
# Sửa lại imports để không dùng relative imports
from project.utils.pdf_reader import read_pdf_files
from project.utils.text_processor import TextProcessor
from project.utils.text_preprocessor import TextPreprocessor
from project.models.chunk import TextChunk
from project.config.settings import PDF_DIR, OUTPUT_DIR, MIN_CHUNK_SIZE, MAX_CHUNK_SIZE

def process_pdf_content(file_name: str, content: str) -> List[TextChunk]:
    """Xử lý nội dung PDF và tạo ra các chunk."""
    chunks = []
    
    # Khởi tạo các processors
    text_processor = TextProcessor()
    preprocessor = TextPreprocessor()
    
    # Tiền xử lý content
    content = preprocessor.clean_text(content)
    
    # Xử lý thông tin
    basic_info = text_processor.extract_basic_info(content)
    sections = text_processor.split_into_sections(content)
    
    for section_name, section_content in sections.items():
        section_chunks = text_processor.create_chunks_from_section(
            section_content,
            file_name,
            basic_info.get('ma_thu_tuc', ''),
            basic_info.get('ten_thu_tuc', ''),
            section_name
        )
        chunks.extend(section_chunks)
    
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
    
    # Thống kê về chunks
    if all_chunks:
        chunk_stats = {
            "total_chunks": len(all_chunks),
            "avg_chunk_length": sum(chunk.length for chunk in all_chunks) / len(all_chunks),
            "min_chunk_length": min(chunk.length for chunk in all_chunks),
            "max_chunk_length": max(chunk.length for chunk in all_chunks)
        }
    else:
        chunk_stats = {
            "total_chunks": 0,
            "avg_chunk_length": 0,
            "min_chunk_length": 0,
            "max_chunk_length": 0
        }
    
    # Lưu kết quả
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Lưu chunks
    chunks_file = os.path.join(OUTPUT_DIR, f"chunks_{timestamp}.json")
    with open(chunks_file, 'w', encoding='utf-8') as f:
        json.dump([chunk.to_dict() for chunk in all_chunks], f, ensure_ascii=False, indent=2)
    
    # Lưu thống kê
    stats_file = os.path.join(OUTPUT_DIR, f"stats_{timestamp}.json")
    with open(stats_file, 'w', encoding='utf-8') as f:
        json.dump(chunk_stats, f, ensure_ascii=False, indent=2)
    
    print(f"\nThống kê:")
    print(f"Tổng số file PDF: {len(pdf_contents)}")
    print(f"Tổng số chunks: {chunk_stats['total_chunks']}")
    print(f"Độ dài trung bình: {chunk_stats['avg_chunk_length']:.2f}")
    print(f"Độ dài min: {chunk_stats['min_chunk_length']}")
    print(f"Độ dài max: {chunk_stats['max_chunk_length']}")
    print(f"Đã lưu chunks vào: {chunks_file}")
    print(f"Đã lưu thống kê vào: {stats_file}")

if __name__ == "__main__":
    main()
