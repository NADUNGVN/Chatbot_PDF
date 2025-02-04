import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# # Lấy đường dẫn tuyệt đối đến thư mục gốc của project
# project_root = os.path.dirname(os.path.abspath(__file__))
# project_dir = os.path.join(project_root, "project")  # Thêm thư mục project

# # Tạo đường dẫn đến file CSV
# csv_path = os.path.join(project_dir, "data", "raw", "csv", "data_Q&A.csv")

# # In ra đường dẫn để kiểm tra
# print("Đường dẫn file:", csv_path)
# print("File tồn tại:", os.path.exists(csv_path))

# # Đọc file CSV
# try:
#     df = pd.read_csv(csv_path, encoding='utf-8')
#     print("\nSố dòng trong file:", len(df))
#     print("\nCác cột trong file:")
#     print(df.columns.tolist())
#     print("\n5 dòng đầu tiên:")
#     print(df.head())
# except FileNotFoundError:
#     print(f"Không tìm thấy file tại đường dẫn: {csv_path}")
# except Exception as e:
#     print(f"Lỗi khi đọc file: {str(e)}")

# Đọc file CSV
csv_path = "E:/WORK/Build-An-LLM-RAG-Chatbot-With-LangChain-Python/project/data/raw/csv/data_Q&A.csv"
df = pd.read_csv(csv_path, encoding='utf-8')

# Kiểm tra dữ liệu null
print("\nKiểm tra dữ liệu null:")
print(df.isnull().sum())

# Thống kê số lượng câu hỏi theo từ khóa
print("\nSố lượng câu hỏi theo từ khóa:")
print(df['Từ khóa'].value_counts())

# Thống kê độ dài trung bình của câu hỏi và câu trả lời
df['Độ dài câu hỏi'] = df['Câu hỏi'].str.len()
df['Độ dài câu trả lời'] = df['Trả lời'].str.len()

print("\nThống kê độ dài:")
print("Độ dài trung bình câu hỏi:", df['Độ dài câu hỏi'].mean())
print("Độ dài trung bình câu trả lời:", df['Độ dài câu trả lời'].mean())

# Lưu DataFrame đã xử lý
df.to_csv(csv_path.replace('.csv', '_processed.csv'), index=False, encoding='utf-8')


# Thêm cột độ dài
df['Độ dài câu hỏi'] = df['Câu hỏi'].str.len()
df['Độ dài câu trả lời'] = df['Trả lời'].str.len()

# 1. Thống kê chi tiết độ dài
print("\nThống kê chi tiết độ dài câu hỏi:")
print(df['Độ dài câu hỏi'].describe())
print("\nThống kê chi tiết độ dài câu trả lời:")
print(df['Độ dài câu trả lời'].describe())

# 2. Tìm câu hỏi dài nhất và ngắn nhất
print("\nCâu hỏi ngắn nhất:")
print(df.loc[df['Độ dài câu hỏi'].idxmin(), ['Từ khóa', 'Câu hỏi', 'Độ dài câu hỏi']])
print("\nCâu hỏi dài nhất:")
print(df.loc[df['Độ dài câu hỏi'].idxmax(), ['Từ khóa', 'Câu hỏi', 'Độ dài câu hỏi']])

# 3. Phân tích độ dài theo từ khóa
print("\nĐộ dài trung bình theo từ khóa:")
print(df.groupby('Từ khóa')[['Độ dài câu hỏi', 'Độ dài câu trả lời']].mean())

# 4. Vẽ biểu đồ phân phối độ dài
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(x='Từ khóa', y='Độ dài câu hỏi', data=df)
plt.xticks(rotation=45)
plt.title('Phân phối độ dài câu hỏi theo từ khóa')

plt.subplot(1, 2, 2)
sns.boxplot(x='Từ khóa', y='Độ dài câu trả lời', data=df)
plt.xticks(rotation=45)
plt.title('Phân phối độ dài câu trả lời theo từ khóa')

plt.tight_layout()
plt.show()

# Lưu kết quả phân tích
analysis_results = {
    'basic_stats': df[['Độ dài câu hỏi', 'Độ dài câu trả lời']].describe(),
    'by_keyword': df.groupby('Từ khóa')[['Độ dài câu hỏi', 'Độ dài câu trả lời']].mean()
}

# Lưu kết quả vào file Excel
with pd.ExcelWriter('analysis_results.xlsx') as writer:
    analysis_results['basic_stats'].to_excel(writer, sheet_name='Basic Stats')
    analysis_results['by_keyword'].to_excel(writer, sheet_name='By Keyword')