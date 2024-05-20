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

# Define the configuration for the index
index_config = {
    "settings": {"index": {"number_of_shards": 3, "number_of_replicas": 1}},
    "mappings": {
        "properties": {
            "geometry": {"type": "geo_shape"},
            "sa2_code_0": {"type": "long"},
            "asthma_count": {"type": "integer"},
            "copd_count": {"type": "integer"},
            "Code_of_Geographic_feature": {"type": "long"},
            "Name_of_Geographic_feature": {"type": "text"},
        }
    },
}

# Create the index with the specified configuration
try:
    response = es.indices.create(index="health_geo", body=index_config)
    print("Index created:", response)
except Exception as e:
    print("Error creating index:", e)
