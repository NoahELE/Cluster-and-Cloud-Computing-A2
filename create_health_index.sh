curl -XPUT -k 'https://127.0.0.1:9200/asthma_copd' \
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
            "sa2_code_2021": {
                "type": "text"
            },
            "cob_aus_lc_copd_emph": {
                "type": "integer"
            },
            "cob_aus_asth": {
                "type": "integer"
            }
        }
    }
}' | jq '.'
