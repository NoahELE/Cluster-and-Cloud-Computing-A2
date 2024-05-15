curl -XPUT -k 'https://127.0.0.1:9200/traffic' \
   --user 'elastic:gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x' \
   --header 'Content-Type: application/json' \
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "ACCIDENT_NO": {
                "type": "text"
            },
            "ACCIDENT_DATE": {
                "type": "date"
            },
            "ACCIDENT_TIME": {
                "type": "text"
            },
            "LATITUDE": {
                "type": "float"
            },
            "LONGITUDE": {
                "type": "float"
            }
        }
    }
}' | jq '.'
