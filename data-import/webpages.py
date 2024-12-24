import json
import pandas as pd
import os
import time
import numpy as np
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
from httpx import TransportError

# Initialize Elasticsearch client
client = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200}],  # Định nghĩa host và port
    timeout=60,  # Tăng thời gian chờ (timeout) lên 60 giây
    max_retries=10,  # Tăng số lần thử lại
    retry_on_timeout=True  # Bật retry nếu timeout
)

index_name = "tvtt"

def load_data_in_batches(file_path, batch_size):
    # Đọc file .pkl theo từng batch
    data_df = pd.read_pickle(file_path)

    for i in range(0, len(data_df), batch_size):
        yield data_df[i:i + batch_size]


def process_df(df):
    # Chuẩn bị tài liệu cho Elasticsearch bulk API
    docs = [
        {
            "title_embedding": np.array(df['title_embedding'].iloc[i]).flatten().tolist() if 'title_embedding' in df.columns else None,
            "text_embedding": np.array(df['text_embedding'].iloc[i]).flatten().tolist() if 'text_embedding' in df.columns else None,
            "text": df['text'].iloc[i] if 'text' in df.columns else '',
            "id": df['id'].iloc[i] if 'id' in df.columns else '',
            "title": df['title'].iloc[i] if 'title' in df.columns else ''
        }
        for i in range(len(df))  # Duyệt qua từng hàng trong DataFrame
    ]

    return docs


def bulk_insert_with_retry(client, docs_batch, index_name=index_name, max_retries=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            success, failed = helpers.bulk(client, docs_batch, index=index_name, request_timeout=60)
            print(f"Successfully inserted {success} documents, Failed {failed} documents.")
            break  # Dừng lại nếu thành công
        except (ConnectionError, TransportError) as e:
            retry_count += 1
            print(f"Error occurred: {e}. Retrying {retry_count}/{max_retries}...")
            time.sleep(2)  # Chờ 2 giây trước khi retry
        except BulkIndexError as bulk_error:
            # Xử lý lỗi BulkIndexError để ghi lại thông tin chi tiết
            print(f"Bulk index error: {len(bulk_error.errors)} document(s) failed.")
            break  # Ngừng retry khi gặp lỗi này, vì đó là lỗi từ tài liệu

    if retry_count == max_retries:
        print("Max retries reached. Bulk insert failed for this batch.")

file_path = "ir_data.pkl"

if client is not None:
    # Đặt kích thước lô dữ liệu
    batch_size = 500

    # Load và xử lý từng lô dữ liệu
    for batch_num, data_df in enumerate(load_data_in_batches(file_path, batch_size)):
        print(f"Đã load batch {batch_num + 1} dòng {batch_num * batch_size}")

        # Chuyển đổi dữ liệu sang định dạng cho Elasticsearch
        docs = process_df(data_df)
        print(f"Đã chuyển batch {batch_num + 1} dòng {batch_num * batch_size} sang định dạng Elasticsearch")

        # Chèn dữ liệu batch vào Elasticsearch
        bulk_insert_with_retry(client, docs)

    print("Hoàn thành xử lý tất cả các batch")
else:
    print("Không thể kết nối tới Elasticsearch")