import pandas as pd
import time
import numpy as np
from elasticsearch import Elasticsearch, helpers
from elasticsearch.helpers import BulkIndexError
from httpx import TransportError

client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]).options(request_timeout=120)


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


import time
from elasticsearch import helpers, TransportError, ConnectionError
from elasticsearch.helpers import BulkIndexError

def bulk_insert(client, docs_batch, index_name=index_name):
    try:
        success, failed = helpers.bulk(client, docs_batch, index=index_name)
        print(f"Chèn thành công {success} tài liệu, Thất bại {len(failed)} tài liệu.")
    except (ConnectionError, TransportError) as e:
        # Xử lý lỗi kết nối hoặc lỗi truyền thông
        print(f"Error occurred: {e}.")
    except BulkIndexError as bulk_error:
        # Xử lý lỗi BulkIndexError để ghi lại thông tin chi tiết
        print(f"Bulk index error: {len(bulk_error.errors)} document(s) failed.")
        for error in bulk_error.errors:
            print(f"Document failed: {error}")



file_path = "ir_data.pkl"

if client is not None:
    # Đặt kích thước lô dữ liệu
    batch_size = 500

    # Load và xử lý từng lô dữ liệu
    for batch_num, data_df in enumerate(load_data_in_batches(file_path, batch_size)):
        print(f"Đã load batch {batch_num + 1} dòng {batch_num * batch_size}")

        # Chuyển đổi dữ liệu sang định dạng cho Elasticsearch
        docs = process_df(data_df)

        # Chèn dữ liệu batch vào Elasticsearch
        bulk_insert(client, docs)

        print()
        time.sleep(1)

    print("Hoàn thành xử lý tất cả các batch")
else:
    print("Không thể kết nối tới Elasticsearch")