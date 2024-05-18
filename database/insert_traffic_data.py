import json
import os
from elasticsearch import Elasticsearch, helpers
from datetime import datetime

def format_date(date_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d')
    formatted_date = date_obj.strftime('%Y-%m-%d')
    return formatted_date

def split_file(data, instert_size):
    return (data[pos:pos + instert_size] for pos in range(0, len(data), instert_size))

def insert_traffic(file_path, index_name, insert_size = 1500):
    # Establish connection to Elasticsearch
    es = Elasticsearch(
        'https://127.0.0.1:9200',
        basic_auth=('elastic', 'gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x'),
        verify_certs=False
    )
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    outputs=[]
    for i in split_file(data, insert_size):
        insert_data = [
            {
                '_index': index_name,
                '_id': doc['ACCIDENT_NO'],  # Assuming each document has an 'id' field
                '_source': doc
            }
            for doc in i
        ]
        output = helpers.bulk(es, insert_data)
        outputs.append(output)
    return outputs

file_path = 'data/traffic/traffic_accidents.json'
index_name = 'traffic'
insert_traffic(file_path, index_name)