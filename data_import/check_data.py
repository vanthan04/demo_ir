from elasticsearch import Elasticsearch

def check_elasticsearch_data(client, index_name):
    try:
        # Kiểm tra xem index có tồn tại không
        if not client.indices.exists(index=index_name):
            print(f"Index '{index_name}' không tồn tại.")
            return

        # Lấy thông tin cơ bản của index
        index_info = client.indices.get(index=index_name)
        print(f"Thông tin cơ bản của index '{index_name}':")
        print(index_info)

        # Kiểm tra số lượng tài liệu trong index
        doc_count = client.count(index=index_name)['count']
        print(f"Số lượng tài liệu trong index '{index_name}': {doc_count}")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

if __name__ == "__main__":
    # Kết nối tới Elasticsearch
    client = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}]).options(request_timeout=60)

    # Tên của index bạn muốn kiểm tra
    index_name = "tvtt"

    # Gọi hàm kiểm tra dữ liệu
    check_elasticsearch_data(client, index_name)
