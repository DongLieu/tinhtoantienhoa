import numpy as np
import os

# Bộ dữ liệu:
name_file = "cogent_center_0"

# Lấy đường dẫn tuyệt đối đến thư mục hiện tại
current_dir = os.path.abspath(os.getcwd())

# Kết hợp đường dẫn tương đối để tạo đường dẫn đầy đủ đến file input.txt
file_path = os.path.join(current_dir, "dataset", name_file, "input.txt")

# Đọc nội dung của file và chia theo dòng
with open(file_path, "r") as f:
    data = f.readlines()

# Hiển thị danh sách các dòng
for line in data:
    print(line)