import logging

from elasticsearch import Elasticsearch

from k8s_utils import config

try:
    client = Elasticsearch(
        f"{config("ES_HOST")}/{config("ES_DATABASE")}",
        basic_auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
    )
    logging.info("Connection to Elasticsearch successful")
except Exception:
    logging.error("Connection to Elasticsearch failed")


def main():
    logging.info("Checking connection to Elasticsearch")
    return client.info()
