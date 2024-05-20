# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
from elasticsearch import Elasticsearch


def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)


def main():
    """
    Get all data from health_geo index in elastic search.
    """

    try:
        # Define the Elasticsearch query
        index_name = "health_geo"
        query = {
            "size": 1000,  # Adjust this value based on your needs
            "query": {"match_all": {}},
        }

        # Execute the search query
        response = es.search(index=index_name, body=query)
        hits = response["hits"]["hits"]

        # Extract data and convert to a list of dictionaries
        data = [
            {
                "sa2_code_0": hit["_source"]["sa2_code_0"],
                "asthma_count": hit["_source"]["asthma_count"],
                "copd_count": hit["_source"]["copd_count"],
                "Name_of_Geographic_feature": hit["_source"][
                    "Name_of_Geographic_feature"
                ],
                "geometry": hit["_source"]["geometry"],
            }
            for hit in hits
        ]
        return {"ok": True, "json_data": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}
