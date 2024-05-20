# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=(os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"]),
    verify_certs=False,
)


index_config = {
    "settings": {"index": {"number_of_shards": 3, "number_of_replicas": 1}},
    "mappings": {
        "properties": {
            "date": {"type": "date", "format": "yyyy-MM-dd"},
            "time": {"type": "text"},
            "location_id": {"type": "integer"},
            "location_name": {"type": "text"},
            "BPM25": {"type": "float"},
        }
    },
}

try:
    response = es.indices.create(index="air_quality_all", body=index_config)
    print("Index created:", response)
except Exception as e:
    print("Error creating index:", e)
