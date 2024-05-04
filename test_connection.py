import logging

from elasticsearch import Elasticsearch

from k8s_utils import config

host = f"{config('ES_URL')}/{config('ES_DATABASE')}"
basic_auth = (config("ES_USERNAME"), config("ES_PASSWORD"))
client = Elasticsearch(host, basic_auth=basic_auth)


def main():
    logging.info("Checking connection to Elasticsearch")
    ping = client.ping()
    logging.info(f"Ping to Elasticsearch successful, {ping}")
    return client.info()
