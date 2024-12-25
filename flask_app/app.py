from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import json

from query_embedding import get_embedding


app = Flask(__name__)

with open("./config.json") as json_data_file:
    config = json.load(json_data_file)

es = Elasticsearch([{'host': config["es_host"], 'port': config["es_port"], 'scheme': 'http'}])

@app.route("/")
def home():
    data = ""
    error_message = ""
    order_list = []

    try:
        # Kiểm tra xem index "tvtt" có tồn tại không
        if es.indices.exists(index="tvtt"):
            # Nếu tồn tại, thực hiện tìm kiếm
            data = es.search(index="tvtt", body={"query": {"match_all": {}}})
        else:
            error_message = "Index 'tvtt' not found in Elasticsearch."
    except ConnectionError as e:
        error_message = f"Failed to connect to Elasticsearch. Please check your connection and configuration.{es, e}"
        print(f"Connection error: {e}")
    except Exception as e:
        error_message = "An unexpected error occurred with Elasticsearch."
        print(f"Unexpected error: {e}")

    # Nếu có dữ liệu, chuyển kết quả vào order_list
    if data and 'hits' in data:
        for i in data['hits']['hits']:
            order_list.append(i['_source'])

    return render_template("index.html", data=order_list, error_message=error_message)

@app.route("/search", methods=["GET", "POST"])
def search():
    error_message = ""  # Biến để lưu thông báo lỗi

    if request.method == "POST":
        query = request.form.get("query")  # Lấy truy vấn từ form

        if query:
            print(f"Received query: {query}")

            # Tính toán embedding cho truy vấn
            query_embedding = get_embedding(query)[0].tolist()

            index_name = 'tvtt'

            # Cấu trúc truy vấn Elasticsearch
            search_query = {
                "query": {
                    "script_score": {
                        "query": {"match_all": {}},  # Tìm kiếm tất cả các tài liệu
                        "script": {
                            "source": "cosineSimilarity(params.query_vector, 'title_embedding') + 1.0",  # Tính cosine similarity
                            "params": {"query_vector": query_embedding}  # Đưa embedding của truy vấn vào
                        }
                    }
                },
                "size": 5  # Chỉ lấy 5 kết quả hàng đầu
            }

            try:
                response = es.search(index=index_name, body=search_query)
                hits = response['hits']['hits']  # Lấy các kết quả trả về từ Elasticsearch
            except Exception as e:
                error_message = f"Error while querying Elasticsearch: {e}"  # Lưu thông báo lỗi vào biến
                print(f"Error while querying Elasticsearch: {e}")
                hits = []

            results = []
            for hit in hits:
                passage = hit['_source']
                score = hit['_score']  # Lấy điểm cosine similarity từ Elasticsearch

                result = {
                    'context': passage.get('text', ''),  # Lấy nội dung của tài liệu
                    'cosine_similarity': score  # Điểm cosine similarity
                }

                results.append(result)

            # Render lại giao diện với kết quả trả về từ Elasticsearch
            return render_template("index.html", query=query, results=results, error_message=error_message)

    # Nếu không có truy vấn POST, render giao diện mặc định
    return render_template("index.html", query=None, results=None, error_message=error_message)


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0', port=5000)