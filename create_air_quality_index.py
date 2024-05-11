from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "gHcmDFVcTaCkB4QPVHSYkEe7bTbYd!x"),
    verify_certs=False,
    request_timeout=10,
)

es.indices.create(
    index="Melbourne CBD air quality",
    mappings={
        "properties": {
            "datetime_AEST": {"type": "date"},
            "datetime_local": {"type": "date"},
            "location_id": {"type": "text"},
            "location_name": {"type": "text"},
            "BPM2.5": {"type": "float"},
        },
    },
)