from datetime import datetime, timedelta
from elasticsearch import Elasticsearch
from flask import request


def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)


def main():
    """
    Get average BPM2.5 of a day from Elasticsearch index
    """

    try:
        location = request.headers["X-Fission-Params-Location"]
        date_str = request.headers["X-Fission-Params-Date"]
        days_str = request.headers["X-Fission-Params-Days"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_str = dt.strftime("%Y-%m-%d")
        days_int = int(days_str)
        dt1 = dt + timedelta(days=days_int)
        date_str1 = dt1.strftime("%Y-%m-%d")
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"location_name": location}},
                        {"range": {"date": {"gte": date_str, "lt": date_str1}}},
                    ]
                }
            },
            "aggs": {"avg_bpm25": {"avg": {"field": "BPM25"}}},
            "size": 0,
        }
        response = es.search(index="air_quality_all", body=query)
        avg_bpm25 = response["aggregations"]["avg_bpm25"]["value"]
        return {"ok": True, "avg_BPM25": avg_bpm25}
    except ValueError as e:
        return {"ok": False, "error": f"date str format is wrong: {str(e)}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
