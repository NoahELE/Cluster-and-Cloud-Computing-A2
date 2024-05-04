from elasticsearch import Elasticsearch

from k8s_utils import config

client = Elasticsearch(
    f"{config("ES_HOST")}/{config("ES_DATABASE")}",
    basic_auth=(config("ES_USERNAME"), config("ES_PASSWORD")),
)


def main():
    return client.info()
