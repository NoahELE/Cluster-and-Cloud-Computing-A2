from elasticsearch import Elasticsearch
from flask import current_app, jsonify


def main():
    host = "https://elasticsearch-master.elastic.svc.cluster.local:9200"
    basic_auth = ("elastic", "gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x")
    client = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)
    current_app.logger.info("Checking connection to Elasticsearch")
    return jsonify(client.info().body)

