# 🤖 Chatbot PDF

Một ứng dụng chatbot thông minh có khả năng đọc, phân tích và tương tác với nội dung từ các file PDF.

## 📋 Mục lục
- [Tổng quan](#tổng-quan)
- [Tính năng](#tính-năng)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Sử dụng](#sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Đóng góp](#đóng-góp)
- [Giấy phép](#giấy-phép)

## 🎯 Tổng quan
Chatbot PDF là một ứng dụng cho phép người dùng tải lên các file PDF và tương tác với nội dung thông qua giao diện chat. Ứng dụng sử dụng các công nghệ xử lý ngôn ngữ tự nhiên để hiểu và phản hồi các câu hỏi liên quan đến nội dung PDF.

## ✨ Tính năng
- Đọc và xử lý file PDF
- Tương tác thông qua chat
- Trích xuất thông tin từ PDF
- Giao diện người dùng thân thiện
- Hỗ trợ nhiều định dạng PDF khác nhau

## 🔧 Yêu cầu hệ thống
- Python 3.8 trở lên
- Các thư viện được liệt kê trong `requirements.txt`

## 📥 Cài đặt

1. Clone repository:
```bash
git clone https://github.com/NADUNGVN/Chatbot_PDF.git
cd Chatbot_PDF
```

2. Tạo môi trường ảo:
```bash
python -m venv .venv
```

3. Kích hoạt môi trường ảo:
```bash
# Windows
.venv\Scripts\activate

# Linux/MacOS
source .venv/bin/activate
```

4. Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

## 🚀 Sử dụng
1. Khởi động ứng dụng:
```bash
python main.py
```

2. Truy cập ứng dụng qua trình duyệt web tại địa chỉ được hiển thị trong terminal

## 📁 Cấu trúc dự án
```
Chatbot_PDF/
├── project/
│   ├── utils/
│   │   ├── pdf_reader.py
│   │   └── ...
│   ├── static/
│   ├── templates/
│   └── ...
├── .venv/
├── requirements.txt
└── README.md
```

## 🤝 Đóng góp
Mọi đóng góp đều được hoan nghênh! Vui lòng:
1. Fork dự án
2. Tạo nhánh tính năng (`git checkout -b feature/AmazingFeature`)
3. Commit thay đổi (`git commit -m 'Add some AmazingFeature'`)
4. Push lên nhánh (`git push origin feature/AmazingFeature`)
5. Tạo một Pull Request

## 📄 Giấy phép
Dự án được phân phối dưới giấy phép MIT. Xem `LICENSE` để biết thêm thông tin.

---
Developed with ❤️ by [NADUNGVN](https://github.com/NADUNGVN)