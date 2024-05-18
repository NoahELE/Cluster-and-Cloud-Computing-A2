import os
import json
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers

load_dotenv()

INDEX_NAME = 'mastodon_melbourne_past'  
FILE_PATH = 'data/mastodon_past/mastodon_melbourne_past_data.json' 


API_KEY = os.getenv('API_KEY_ELASTIC')


User = Elasticsearch(
    "https://localhost:9200",
    api_key = API_KEY,
    verify_certs=False,
)



def create_index():
    index_content = {
        "settings": {
            "index": {
                "number_of_shards": 3,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "properties": {
                "id": {"type": "keyword"},
                "creat_time": {"type": "date"},
                "content": {"type": "keyword"},
                "language": {"type": "keyword"},
                "sentiment": {"type": "float"},
                "tag": {"type": "keyword"},
            }
        }
    }
    output =  User.indices.create(index = INDEX_NAME, body = index_content)
    return output


def split_file(data, instert_size):
    return (data[pos:pos + instert_size] for pos in range(0, len(data), instert_size))

def insert_data(FILE_PATH, INDEX_NAME, insert_size = 1500):
    with open(FILE_PATH, 'r', encoding='utf-8') as file:
        data = [json.loads(line) for line in file]
    
    outputs=[]
    for i in split_file(data, insert_size):
        insert_data = [
            {
                '_index': INDEX_NAME,
                '_id': doc['id'],  # Assuming each document has an 'id' field
                '_source': doc
            }
            for doc in i
        ]
        output = helpers.bulk(User, insert_data)
        outputs.append(output)
    return outputs



print(create_index())
print(insert_data(FILE_PATH, INDEX_NAME))

