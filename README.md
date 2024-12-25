1. Clone git repository

2. Mở terminal

3. Chạy lần lượt các câu lệnh, nhớ để docker trạng thái đang chạy

python -m venv venv

.\venv\Scripts\activate

pip install --no-cache-dir -r requirements.txt

cd flask_app

docker-compose up --build -d


* Thực hiện chèn dữ liệu vào elasticsearch
    - Chèn dữ liệu
        + cd ..
        
        + cd data-import
        
        + python create_index.py
        
        + python insert_data.py
    - Kiểm tra dữ liệu
        + python check_data.py

4. Chạy http://localhost:5000/
