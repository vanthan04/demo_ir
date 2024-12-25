# 1. Clone git repository

```
git init
git clone https://github.com/vanthan04/demo_ir.git
```

# 2. Tải Dữ Liệu Đã Xử Lý

Tải dữ liệu đã xử lý tại [đây](https://www.kaggle.com/datasets/tranvanthan/dataa-embedding-wiki).

# 3. Mở terminal

# 4. Thực hiện lần lượt các câu lệnh, lưu ý docker đang chạy
### Tạo Môi Trường Ảo Python
```
python -m venv venv
```

### Kích Hoạt Môi Trường Ảo
```
.\venv\Scripts\activate
```

### Cài Đặt Các Phụ Thuộc
```
pip install --no-cache-dir -r requirements.txt
```

### Di Chuyển Đến Thư Mục `flask_app`

```
cd flask_app
```

### Khởi Động Docker Compose
```
docker-compose up --build -d  
```

# 5. Thực hiện chèn dữ liệu vào elasticsearch

### Di chuyển đến folder data_import
```
cd ..
cd data-import
```
### Tạo index và chèn dữ liệu
```
python create_index.py
python insert_data.py
```

### Kiểm tra dữ liệu
```
python check_data.py
```
# 6. Chạy http://localhost:5000/