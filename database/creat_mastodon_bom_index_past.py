from elasticsearch import Elasticsearch, helpers
import json
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv('API_KEY_ELASTIC')



User = Elasticsearch(
    "https://localhost:9200",
    api_key = API_KEY,
    verify_certs=False,
)


#mastodon合并数据
mastodon_tempo_result = User.search(index='mastodon_melbourne_past', body={
    "size": 0,
    "aggs": {
        "by_date": {
            "date_histogram": {
                "field": "creat_time",
                "calendar_interval": "day"
            },
            "aggs": {
                "average_sentiment": {
                    "avg": {
                        "field": "sentiment"
                    }
                },
                "max_sentiment": {
                    "max": {
                        "field": "sentiment"
                    }
                },
                "min_sentiment": {
                    "min": {
                        "field": "sentiment"
                    }
                },
                "contents": {
                    "terms": {
                        "field": "content",
                        "size": 100
                    }
                },
                "tags": {
                    "significant_terms": {
                        "field": "tag",
                        "size": 50
                    }
                }
            }
        }
    }
})

mastodon_data = {}
for bucket in mastodon_tempo_result["aggregations"]["by_date"]["buckets"]:
    date = datetime.strptime(bucket["key_as_string"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
    doc_count = bucket["doc_count"]
    mastodon_data[date] = {
        "average_sentiment": bucket['average_sentiment']['value'],
        "max_sentiment": bucket['max_sentiment']['value'],
        "min_sentiment": bucket['min_sentiment']['value'],
        "toots_count": bucket['tags']["doc_count"],
        "tags": [tag['key'] for tag in bucket['tags']['buckets']],
        "content": [content['key'] for content in bucket['contents']['buckets']]
    }
    

#bom合并数据
bom_tempo_result =  User.search(index='bom_melbourne_weather_past', body={
    "size":450,
    "_source":["Date", "Minimum temperature (C)", "Maximum temperature (C)", 
               "Rainfall (mm)", "Speed of maximum wind gust (km/h)"],
    "query":{
        "match_all":{}
    }
})

def get_tem(min_tem, max_tem):
    if min_tem == None:
        average =  max_tem
        return average, max_tem, max_tem
    elif max_tem == None:
        average =  min_tem
        return average, min_tem, min_tem
    else:
         average = (min_tem + max_tem)/2
    return average, min_tem, max_tem

bom_data = {}
for data in bom_tempo_result["hits"]["hits"]:
    source = data["_source"]
    date = source["Date"]
    aver_temp, min_temp, max_temp = get_tem(source["Minimum temperature (C)"], source["Maximum temperature (C)"])
    bom_data[date] = {
        "min_temp": min_temp,
        "max_temp": max_temp,
        "average_temp": aver_temp,
        "rainfall": source["Rainfall (mm)"],
        "wind_gust_speed": source["Speed of maximum wind gust (km/h)"]
    }


merge_data = []
for date in mastodon_data:
    if date in bom_data:
        combind_entry = {
            "Date": date,
            "min_temp": bom_data[date]["min_temp"],
            "max_temp": bom_data[date]["max_temp"],
            "average_temp": bom_data[date]["average_temp"],
            "rainfall": bom_data[date]["rainfall"],
            "wind_gust_speed": bom_data[date]["wind_gust_speed"],

            "toots_count": mastodon_data[date]["toots_count"],
            "average_sentiment": mastodon_data[date]["average_sentiment"],
            "max_sentiment": mastodon_data[date]["max_sentiment"],
            "min_sentiment": mastodon_data[date]["min_sentiment"],
            "toots_count": mastodon_data[date]["toots_count"],
            "tags": mastodon_data[date]["tags"],
            "content": mastodon_data[date]["content"]
        }
        merge_data.append(combind_entry)

#----------------------------------------
INDEX_NAME = 'mastodon_bom_past'  #need to changed
#Upload data to elastic
def create_index():
    index_content = {
        "settings": {
            "index": {
                "number_of_shards": 1,
                "number_of_replicas": 1
            }
        },
        "mappings": {
            "properties": {
                "Date": {"type": "date"},
                "min_temp": {"type": "float"},
                "max_temp": {"type": "float"},
                "average_temp": {"type": "float"},
                "rainfall": {"type": "float"},
                "wind_gust_speed": {"type": "float"},

                "average_sentiment": {"type": "float"},
                "max_sentiment": {"type": "float"},
                "min_sentiment": {"type": "float"},
                "toots_count": {"type": "integer"},
                "tags": {"type": "keyword"},
                "content": {"type": "keyword"}
            }
        }
    }
    output = User.indices.create(index=INDEX_NAME, body=index_content)
    return output


def insert_data(index_name, data):
    actions = [
        {
            '_index': index_name,
            '_id': doc["Date"],
            '_source': doc
        }
        for doc in data
    ]
    output = helpers.bulk(User, actions)
    return output



print(create_index())
print(insert_data(INDEX_NAME, merge_data))

