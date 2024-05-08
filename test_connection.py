from elasticsearch import Elasticsearch
from flask import current_app, jsonify


def main():
    # host = f"{config('ES_URL')}"
    host = "https://elasticsearch-master.elastic.svc.cluster.local:9200"
    # basic_auth = (config("ES_USERNAME"), config("ES_PASSWORD"))
    basic_auth = ("elastic", "elastic")
    client = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)
    current_app.logger.info("Checking connection to Elasticsearch")
    return jsonify(client.info())
