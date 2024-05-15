import json
import os
from elasticsearch import Elasticsearch, helpers

def insert_health_data(file_path, index_name):
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
        insert_data.append(
            {
                '_index': index_name,
                '_id': record['sa2_code_2021'], 
                '_source': record
            }
        )

    try:
        response = helpers.bulk(es, insert_data)
        print("Uploaded data successfully with result:", response)
    except helpers.BulkIndexError as e:
        print("Error uploading data:", e.errors)
    except Exception as e:
        print("Error uploading data:", str(e))

# Define file path and index name
file_path = 'data/asthma_copd/asthma_copd_merged.json'
index_name = 'asthma_copd'
insert_health_data(file_path, index_name)
