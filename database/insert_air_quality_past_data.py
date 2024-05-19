import json
import os
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def format_date_time(date_str, time_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%Y-%m-%d")
    return formatted_date, time_str


def insert_air_quality(file_path, index_name):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        "https://localhost:9200",
        basic_auth=(os.environ["ES_USERNAME"], os.environ["ES_PASSWORD"]),
        verify_certs=False,
    )

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    insert_data = []
    for record in data:
        formatted_date, formatted_time = format_date_time(
            record["date"], record["time"]
        )
        record["date"] = formatted_date
        record["time"] = formatted_time
        # Combine date and time to create a unique ID for each record
        record_id = f"{formatted_date}_{formatted_time}_{record['location_id']}"
        insert_data.append({"_index": index_name, "_id": record_id, "_source": record})

    try:
        response = helpers.bulk(es, insert_data)
        print("Uploaded data successfully with result:", response)
    except helpers.BulkIndexError as e:
        print("Error uploading data:", e.errors)
    except Exception as e:
        print("Error uploading data:", str(e))


folder_path = "data/air_quality_json"
index_name = "air_quality_all"

for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        print(file_path)
        insert_air_quality(file_path, index_name)
