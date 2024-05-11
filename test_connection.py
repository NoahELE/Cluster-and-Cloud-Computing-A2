import os

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

host = "https://localhost:9200"
basic_auth = (os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"])
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False, request_timeout=10)
print(es.info())
