from elasticsearch import Elasticsearch

from flask import Flask, render_template, request
from query_embedding import *

app = Flask(__name__)




# # Define a retry strategy for the Elasticsearch client
# retry_strategy = Retry(
#     total=3,
#     status_forcelist=[429, 500, 502, 503, 504],
#     allowed_methods=["HEAD", "GET", "PUT", "DELETE", "OPTIONS", "POST"],
#     backoff_factor=1
# )

# adapter = HTTPAdapter(max_retries=retry_strategy)

# # Initialize the Elasticsearch client with the retry strategy
# es = Elasticsearch(
#     [{'host': 'elasticsearch', 'port': 9200}],
#     connection_class=RequestsHttpConnection,
#     max_retries=3
# )
# es.transport.connection_pool.adapter = adapter

# Initialize Elasticsearch client
client = Elasticsearch(
    hosts=[{'host': 'localhost', 'port': 9200}],  # Định nghĩa host và port
    timeout=60,  # Tăng thời gian chờ (timeout) lên 60 giây
    max_retries=10,  # Tăng số lần thử lại
    retry_on_timeout=True  # Bật retry nếu timeout
)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query = request.form["query"]

        # Compute the query embedding
        query_embedding = get_embedding(query)[0].tolist()

        index_name = 'tvtt'

        query = {
            "query": {
                "script_score": {
                    "query": {"match_all": {}},
                    "script": {
                        "source": "cosineSimilarity(params.query_vector, 'title_embedding') + 1.0",
                        "params": {"title_embedding": query_embedding}
                    }
                }
            },
            "size": 5
        }
        response = client.search(index=index_name, body=query)
        hits = response['hits']['hits']

        results = []
        for hit in hits:
            passage = hit['_source']
            score = hit['_score']  # Lấy điểm cosine similarity từ Elasticsearch

            result = {
                'query': query,
                'context': passage['text'],
                'cosine_similarity': score  # Thêm độ tương đồng cosin vào kết quả
            }

            results.append(result)

        return render_template("index.html", query=query, results=results)
    else:
        return render_template("index.html", query=None, results=None)


if __name__ == "__main__":
    app.run(debug=True)
