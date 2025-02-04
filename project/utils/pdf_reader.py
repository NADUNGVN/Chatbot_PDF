import os
from typing import Dict
from PyPDF2 import PdfReader

def read_pdf_files(pdf_directory: str) -> Dict[str, str]:
    """Đọc tất cả các file PDF trong thư mục."""
    pdf_contents = {}
    
    # Lấy danh sách tất cả các file PDF
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    
    for pdf_file in pdf_files:
        file_path = os.path.join(pdf_directory, pdf_file)
        try:
            # Đọc file PDF
            reader = PdfReader(file_path)
            
            # Trích xuất text từ tất cả các trang
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            # Lưu nội dung với tên file
            pdf_contents[pdf_file] = text
            
            print(f"Đã đọc thành công: {pdf_file}")
            
        except Exception as e:
            print(f"Lỗi khi đọc file {pdf_file}: {str(e)}")
    
    return pdf_contents
