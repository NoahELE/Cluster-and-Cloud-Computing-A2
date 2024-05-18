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