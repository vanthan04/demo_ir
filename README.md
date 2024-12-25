1. Clone git repository

2. Tải dữ liệu đã được xử lí: https://www.kaggle.com/datasets/tranvanthan/dataa-embedding-wiki
    Sau đó đưa file mới tải vào trong folder data_import

3. Mở terminal

4. ~~Chạy lần lượt các câu lệnh, nhớ để docker trạng thái đang chạy~~

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

5. Chạy http://localhost:5000/
