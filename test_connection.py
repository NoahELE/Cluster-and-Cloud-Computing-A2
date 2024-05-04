import logging

from elasticsearch import Elasticsearch

from k8s_utils import config

try:
    host = f"{config('ES_URL')}/{config('ES_DATABASE')}"
    basic_auth = (config("ES_USERNAME"), config("ES_PASSWORD"))
    logging.info(f"Connecting to Elasticsearch, {host} {basic_auth}")
    client = Elasticsearch(host, basic_auth=basic_auth)
    logging.info("Connection to Elasticsearch successful")
except Exception as e:
    logging.error(f"Connection to Elasticsearch failed, {e}")


def main():
    logging.info("Checking connection to Elasticsearch")
    ping = client.ping()
    logging.info(f"Ping to Elasticsearch successful, {ping}")
    return client.info()
