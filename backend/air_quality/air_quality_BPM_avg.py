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
    """Get average BPM2.5 of a day from Elasticsearch index"""
    try:
        date_str = request.headers["X-Fission-Params-Date"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_str = dt.strftime("%Y-%m-%d")
        dt1 = dt + timedelta(days=1)
        date_str1 = dt1.strftime("%Y-%m-%d")
        resp = es.search(
            index="air_quality",
            query={"range": {"date": {"gte": date_str, "lt": date_str1}}},
        )
        bpm25_values = [hit["_source"]["BPM2.5"] for hit in resp["hits"]["hits"]]
        return {"ok": True, "avg_BPM2.5": sum(bpm25_values) / len(bpm25_values)}
    except ValueError as e:
        return {"ok": False, "error": f"date str format is wrong: {str(e)}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
