# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
from datetime import datetime, timedelta

from elasticsearch import Elasticsearch
from flask import request
from haversine import Unit, haversine


def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)


def main():
    """
    Count accidents of a day from Elasticsearch index.
    """

    # latitude and longitude of melbourne centre
    melbourne_center = (-37.8136, 144.9631)
    radius_km = 15  # 15km range

    try:
        date_str = request.headers["X-Fission-Params-Date"]
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        date_str = dt.strftime("%Y-%m-%d")
        dt1 = dt + timedelta(days=1)
        date_str1 = dt1.strftime("%Y-%m-%d")
        resp = es.search(
            index="traffic",
            query={"range": {"ACCIDENT_DATE": {"gte": date_str, "lt": date_str1}}},
            size=10000,
        )

        hits = resp["hits"]["hits"]
        accident_count = len(hits)
        center_accidents = 0

        for hit in hits:
            source = hit["_source"]
            accident_location = (source["LATITUDE"], source["LONGITUDE"])

            # calculate the distance between accident location and melbourne central
            distance = haversine(
                melbourne_center, accident_location, unit=Unit.KILOMETERS
            )

            if distance <= radius_km:
                center_accidents += 1

        return {
            "ok": True,
            "accident_count": accident_count,
            "center_accidents": center_accidents,
        }
    except ValueError as e:
        return {"ok": False, "error": f"date str format is wrong: {str(e)}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}
