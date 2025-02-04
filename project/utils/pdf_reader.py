import os
import logging
import fitz  # PyMuPDF
from typing import Dict

logger = logging.getLogger(__name__)

def read_pdf_files(pdf_dir: str) -> Dict[str, str]:
    """Đọc tất cả các file PDF trong thư mục"""
    pdf_contents = {}
    
    try:
        # Kiểm tra thư mục tồn tại
        if not os.path.exists(pdf_dir):
            logger.error(f"Thư mục không tồn tại: {pdf_dir}")
            return pdf_contents
        
        # Đọc từng file PDF
        for filename in os.listdir(pdf_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(pdf_dir, filename)
                try:
                    with fitz.open(file_path) as doc:
                        text = ""
                        for page in doc:
                            text += page.get_text()
                        pdf_contents[filename] = text
                        logger.info(f"Đã đọc thành công: {filename}")
                except Exception as e:
                    logger.error(f"Lỗi khi đọc file {filename}: {str(e)}")
                    continue
        
    except Exception as e:
        logger.error(f"Lỗi khi đọc thư mục PDF: {str(e)}")
    
    return pdf_contents
