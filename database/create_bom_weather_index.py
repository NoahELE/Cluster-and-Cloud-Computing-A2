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

es.indices.create(
    index="bom_melbourne_weather",
    mappings={
        "properties": {
            "datetime": {"type": "date"},
            "temperature": {"type": "float"},
            "pressure": {"type": "float"},
            "rainfall": {"type": "float"},
            "relative_humidity": {"type": "integer"},
            "wind_speed": {"type": "float"},
            "wind_direction": {"type": "keyword"},
        },
    },
)
