# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x"),
    verify_certs=False,
    request_timeout=10,
)

es.indices.create(
    index="mastodon_melbourne",
    mappings={
        "properties": {
            "id": {"type": "keyword"},
            "creat_time": {"type": "date"},
            "content": {"type": "text"},
            "language": {"type": "keyword"},
            "sentiment": {"type": "float"},
            "tag": {"type": "text"},
        },
    },
)
