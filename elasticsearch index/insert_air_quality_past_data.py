import json
import os
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

def format_datetime(datetime_str):
    date_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    formatted_datetime = date_obj.strftime('%Y-%m-%dT%H:%M:%S')
    return formatted_datetime

def insert_air_quality(file_path, index_name):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        'https://127.0.0.1:9200',
        basic_auth=('elastic', 'gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x'),
        verify_certs=False,
        timeout=60
    )
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    insert_data = []
    for record in data:
        formatted_datetime = format_datetime(record['datetime_AEST'])
        record['datetime_AEST'] = formatted_datetime 
        insert_data.append(
            {'_index': index_name, '_id': formatted_datetime, '_source': record}
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
