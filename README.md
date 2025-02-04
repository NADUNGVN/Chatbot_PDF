# PDF Chunk Processor cho TTHC

Dự án này là một công cụ xử lý và phân tích văn bản từ các file PDF chứa Thủ tục Hành chính (TTHC). Công cụ này tự động đọc, phân tích và tách nội dung thành các chunk có ý nghĩa, đồng thời trích xuất metadata quan trọng từ mỗi thủ tục.

## Tính năng chính

- 📄 Đọc và xử lý file PDF tự động
- 🔍 Trích xuất thông tin thủ tục (mã, tên, cấp thực hiện, lĩnh vực)
- ✂️ Tách văn bản thành các section có ý nghĩa
- 📊 Tạo chunks với kích thước tối ưu (200-1000 ký tự)
- 🔄 Hỗ trợ overlap giữa các chunks để đảm bảo tính liên tục
- 💾 Xuất dữ liệu sang định dạng JSON

## Cấu trúc dự án

```
CHATBOT/
├── project/
│   ├── main.py              # Entry point của ứng dụng
│   ├── utils/               # Các công cụ tiện ích
│   │   ├── pdf_reader.py    # Xử lý đọc PDF
│   │   └── text_processor.py # Xử lý và phân tích văn bản
│   ├── models/             # Các model dữ liệu
│   │   └── chunk.py        # Model cho text chunks
│   └── config/             # Cấu hình
│       └── settings.py     # Các thiết lập của ứng dụng
├── data/
│   ├── pdf/               # Thư mục input PDF
│   └── output/            # Thư mục output JSON
└── tests/                 # Unit tests
```

## Cài đặt

1. Clone repository:
```bash
git clone https://github.com/NADUNGVN/Chatbot_PDF.git
cd Chatbot_PDF
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

## Cách sử dụng

1. Đặt các file PDF TTHC vào thư mục `data/pdf/`

2. Chạy chương trình:
```bash
python -m project.main
```

3. Kết quả sẽ được lưu trong thư mục `data/output/` dưới dạng file JSON

## Cấu hình

Các thông số cấu hình chính trong `settings.py`:
- `MIN_CHUNK_SIZE`: 200 ký tự
- `MAX_CHUNK_SIZE`: 1000 ký tự
- `CHUNK_OVERLAP`: 100 ký tự
- `MIN_SECTION_LENGTH`: 50 ký tự

## Cấu trúc output

File JSON output bao gồm danh sách các chunks với format:
```json
{
  "content": "Nội dung văn bản",
  "metadata": {
    "file_name": "tên_file.pdf",
    "ma_thu_tuc": "Mã TTHC",
    "ten_thu_tuc": "Tên thủ tục",
    "cap_thuc_hien": "Cấp thực hiện",
    "linh_vuc": "Lĩnh vực",
    "section_name": "Tên section",
    "processed_date": "Ngày xử lý"
  }
}
```

## Dependencies chính

- PyMuPDF (fitz): Đọc file PDF
- Python 3.8+
- Standard library: json, os, logging, datetime

## Tác giả

- NADUNGVN - [GitHub](https://github.com/NADUNGVN)

## License

MIT License