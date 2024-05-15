from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("elastic", "comp90024-elastic"),
    verify_certs=False,
    request_timeout=10,
)

es.indices.create(
    index="asthma_copd",
    mappings={
        "properties": {
            "sa2_code_2021": {"type": "text"},
            "cob_aus_lc_copd_emph":{"type":"integer"},
            "cob_aus_asth":{"type":"integer"}
        },
    },
)