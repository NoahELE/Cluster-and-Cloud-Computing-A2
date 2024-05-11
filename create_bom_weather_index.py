from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "elastic"),
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
