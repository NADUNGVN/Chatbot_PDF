# main.py
import os
import json
import logging
from datetime import datetime
from typing import List
from pathlib import Path

# Import từ các module trong project
from project_create_chunks.utils.pdf_reader import read_pdf_files
from project_create_chunks.utils.text_processor import TextProcessor
from project_create_chunks.config.settings import PDF_DIR, OUTPUT_DIR
from project_create_chunks.models.chunk import TextChunk  # Thêm import TextChunk

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def save_chunks_to_json(chunks: List[TextChunk], output_dir: str):
    """Lưu chunks vào file JSON"""
    try:
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(output_dir, exist_ok=True)
        
        # Chuẩn bị dữ liệu để lưu
        output_data = []
        for chunk in chunks:
            chunk_dict = {
                'content': chunk.content,
                'metadata': chunk.metadata
            }
            output_data.append(chunk_dict)
        
        # Tạo tên file với timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(output_dir, f"chunks_{timestamp}.json")
        
        # Lưu file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Đã lưu {len(chunks)} chunks vào file: {output_file}")
        return output_file
    
    except Exception as e:
        logger.error(f"Lỗi khi lưu chunks: {str(e)}")
        raise  # Ném lỗi để main() có thể xử lý

def main():
    try:
        # Đọc PDF files
        pdf_contents = read_pdf_files(PDF_DIR)
        if not pdf_contents:
            logger.error("Không tìm thấy file PDF nào để xử lý")
            return
        
        # Xử lý text
        processor = TextProcessor()
        all_chunks = []
        
        for file_name, content in pdf_contents.items():
            logger.info(f"Đang xử lý file: {file_name}")
            
            # Tạo metadata cơ bản
            base_metadata = {
                'file_name': file_name,
                'processed_date': datetime.now().isoformat()
            }
            
            # Xử lý text thành chunks
            file_chunks = processor.process_text(content, base_metadata)
            
            # Chuyển đổi Dict thành TextChunk objects
            chunk_objects = [
                TextChunk(
                    content=chunk['content'],
                    metadata=chunk['metadata']
                ) for chunk in file_chunks
            ]
            
            all_chunks.extend(chunk_objects)
            logger.info(f"Đã tạo {len(chunk_objects)} chunks từ file {file_name}")
        
        # Lưu kết quả
        if all_chunks:
            try:
                output_file = save_chunks_to_json(all_chunks, OUTPUT_DIR)
                logger.info("Xử lý hoàn tất")
            except Exception as e:
                logger.error(f"Lỗi khi lưu kết quả: {str(e)}")
        else:
            logger.warning("Không có chunks nào được tạo")
    
    except Exception as e:
        logger.error(f"Lỗi trong quá trình xử lý: {str(e)}")

if __name__ == "__main__":
    main()