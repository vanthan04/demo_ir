from elasticsearch import Elasticsearch

# Initialize Elasticsearch client
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# Create an index with the appropriate mapping
mapping = {
    "mappings": {
        "properties": {
            "id": {"type": "text"},
            "title": {"type": "text"},
            "text": {"type": "text"},
            "title_embedding": {"type": "dense_vector", "dims": 384},
            "text_embedding": {"type": "dense_vector", "dims": 384}
        }
    }
}

es.indices.create(index="tvtt", body=mapping, ignore=400)