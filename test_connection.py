from elasticsearch import Elasticsearch
from flask import current_app, jsonify

from k8s_utils import config

host = f"{config('ES_URL')}"
basic_auth = (config("ES_USERNAME"), config("ES_PASSWORD"))
client = Elasticsearch(host, basic_auth=basic_auth)


def main():
    current_app.logger.info("Checking connection to Elasticsearch")
    return jsonify(client.info())
