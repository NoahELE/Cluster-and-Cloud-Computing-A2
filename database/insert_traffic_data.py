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


def split_file(data, instert_size):
    return (data[pos : pos + instert_size] for pos in range(0, len(data), instert_size))


def insert_traffic(file_path, index_name, insert_size=1500):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=(os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"]),
        verify_certs=False,
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    outputs = []
    for i in split_file(data, insert_size):
        insert_data = [
            {
                "_index": index_name,
                "_id": doc["ACCIDENT_NO"],  # Assuming each document has an 'id' field
                "_source": doc,
            }
            for doc in i
        ]
        output = helpers.bulk(es, insert_data)
        outputs.append(output)
    return outputs


file_path = "data/traffic/traffic_accidents.json"
index_name = "traffic"
insert_traffic(file_path, index_name)
