import json
import os
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date

def insert_past_weather(file_path, index_name):
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
        formatted_date = format_date(record['Date'])
        record['Date'] = formatted_date 
        insert_data.append(
            {'_index': index_name, '_id': formatted_date, '_source': record}
        )

    try:
        response = helpers.bulk(es, insert_data)
        print("Uploaded data successfully with result:", response)
    except helpers.BulkIndexError as e:
        print("Error uploading data:", e.errors)
    except Exception as e:
        print("Error uploading data:", str(e)) 


file_path = 'data/weather_json/gathered_bom_weather_past.json'
index_name = 'bom_melbourne_weather_past'
insert_past_weather(file_path, index_name)
