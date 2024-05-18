from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from flask import request

def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()

# host = "https://127.0.0.1:9200"
# basic_auth = ("elastic", "gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x")
host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)

def main():
    try:
        date_str = request.headers["X-Fission-Params-Date"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_str = dt.strftime("%Y-%m-%d")
        dt1 = dt + timedelta(days=1)
        date_str1 = dt1.strftime("%Y-%m-%d")
        resp = es.search(
            index="mastodon_bom_past",
            query={"range": {"Date": {"gte": date_str, "lt": date_str1}}},
        )
        # num_of_toots = resp["hits"]["total"]["value"]
        num_of_toots = resp["hits"]["hits"][0]["_source"]["toots_count"]
        sentiment_dict = {
            "min_sentiment": resp["hits"]["hits"][0]["_source"]["min_sentiment"],
            "max_sentiment": resp["hits"]["hits"][0]["_source"]["max_sentiment"],
            "average_sentiment": resp["hits"]["hits"][0]["_source"]["average_sentiment"]
        }
        bom_dict = {
            "min_temp": resp["hits"]["hits"][0]["_source"]["min_temp"],
            "max_temp": resp["hits"]["hits"][0]["_source"]["max_temp"],
            "average_temp": resp["hits"]["hits"][0]["_source"]["average_temp"],
            "rainfall": resp["hits"]["hits"][0]["_source"]["rainfall"],
            "wind_gust_speed": resp["hits"]["hits"][0]["_source"]["wind_gust_speed"]
        }

        resp_dict = {
            "sentiment_dict": sentiment_dict,
            "num_of_toots": num_of_toots,
            "bom_dict": bom_dict
        }
        return {"ok": True, "resp_dict": resp_dict}
    except ValueError as e:
        return {"ok": False, "error": f"date str format is wrong: {str(e)}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
