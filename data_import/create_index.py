from elasticsearch import Elasticsearch
from elasticsearch.exceptions import RequestError

# Initialize Elasticsearch client
client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Kiểm tra kết nối
if client.ping():
    print("Kết nối Elasticsearch thành công!")
else:
    print("Không thể kết nối Elasticsearch.")
    exit(1)

# Define mapping with dense_vector for embeddings
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "text"},
            "title": {"type": "text"},
            "text": {"type": "text"},
            "title_embedding": {
                "type": "dense_vector",
                "dims": 384
            },
            "text_embedding": {
                "type": "dense_vector",
                "dims": 384
            }
        }
    }
}

index_name = "tvtt"

# Xóa chỉ mục cũ nếu có
if client.indices.exists(index=index_name):
    try:
        client.indices.delete(index=index_name)
        print(f"Chỉ mục '{index_name}' đã được xóa.")
    except RequestError as e:
        print(f"Đã xảy ra lỗi khi xóa chỉ mục: {e}")
        exit(1)

# Tạo chỉ mục mới với mapping
try:
    client.indices.create(index=index_name, body=mapping)
    print(f"Chỉ mục '{index_name}' đã được tạo.")
except RequestError as e:
    print(f"Đã xảy ra lỗi khi tạo chỉ mục: {e}")
    exit(1)
