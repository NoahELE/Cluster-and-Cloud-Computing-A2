import logging, json
from flask import current_app, request
from elasticsearch import Elasticsearch, helpers
from datetime import datetime, timedelta


def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)

def main():
    """
    Get rainfall everyday.
    """

    try:
        date_str = request.headers["X-Fission-Params-Date"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_str = dt.strftime("%Y-%m-%d")

        weather_index_name = 'bom_melbourne_weather_past'
        query = {
                "query": {
                    "term": {
                    "Date": date_str
                    }
                },
                "_source": ["Date", "Rainfall (mm)"]
                }
        
        response = es.search(index=weather_index_name, body=query, size=500)  # set large size for getting more data

        for hit in response['hits']['hits']:
            source = hit['_source']
            rainfall_date = source['Date']
            rainfall_amount = source['Rainfall (mm)']

        return {"ok": True, "rainfall_date": rainfall_date, "rainfall_amount": rainfall_amount}
    except ValueError as e:
        return {"ok": False, "error": f"date str format is wrong: {str(e)}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

    

