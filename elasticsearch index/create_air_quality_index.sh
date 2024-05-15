curl -XPUT -k 'https://127.0.0.1:9200/air_quality' \
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
            "datetime_AEST": {
                "type": "date"
            },
            "location_id": {
                "type": "integer"
            },
            "location_name": {
                "type": "text"
            },
            "BPM2.5": {
                "type": "float"
            }
        }
    }
}' | jq '.'
