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
    request_timeout=10,
)

index_config = {
    "settings": {"index": {"number_of_shards": 3, "number_of_replicas": 1}},
    "mappings": {
        "properties": {
            "Date": {"type": "date"},
            "Minimum temperature (C)": {"type": "float"},
            "Maximum temperature (C)": {"type": "float"},
            "Rainfall (mm)": {"type": "float"},
            "Speed of maximum wind gust (km/h)": {"type": "float"},
        }
    },
}

try:
    response = es.indices.create(index="bom_melbourne_weather_past", body=index_config)
    print("Index created:", response)
except Exception as e:
    print("Error creating index:", e)
