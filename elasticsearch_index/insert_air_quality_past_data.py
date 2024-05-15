import json
import os
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

def format_date_time(date_str, time_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date, time_str

def insert_air_quality(file_path, index_name):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        'https://127.0.0.1:9200',
        basic_auth=('elastic', 'gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x'),
        verify_certs=False
    )
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    insert_data = []
    for record in data:
        formatted_date, formatted_time = format_date_time(record['date'], record['time'])
        record['date'] = formatted_date
        record['time'] = formatted_time
        # Combine date and time to create a unique ID for each record
        record_id = f"{formatted_date}_{formatted_time}"
        insert_data.append(
            {'_index': index_name, '_id': record_id, '_source': record}
        )

    try:
        response = helpers.bulk(es, insert_data)
        print("Uploaded data successfully with result:", response)
    except helpers.BulkIndexError as e:
        print("Error uploading data:", e.errors)
    except Exception as e:
        print("Error uploading data:", str(e)) 


file_path = 'data/air_quality/2021_Melbourne_CBD_air_quality.json'
index_name = 'air_quality'
insert_air_quality(file_path, index_name)
