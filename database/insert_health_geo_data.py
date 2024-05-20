# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
import json
import os
from datetime import datetime

from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()


def format_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date


def insert_past_weather(file_path, index_name):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=(os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"]),
        verify_certs=False,
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    records = data["features"]

    insert_data = []
    for record in records:
        insert_data.append(
            {
                "_index": index_name,
                "_id": record["properties"]["sa2_code_0"],
                "_source": {**record["properties"], "geometry": record["geometry"]},
            }
        )

    response = helpers.bulk(es, insert_data)
    print("Uploaded data successfully with result:", response)


file_path = "data/health_geo/health_geo.json"
index_name = "health_geo"
insert_past_weather(file_path, index_name)
