# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
curl -XPUT -k 'https://127.0.0.1:9200/bom_melbourne_weather_past'\
   --user 'elastic:gHcmDFVtcTaCkB4QPVHSYkEe7bTbYd!x'\
   --header 'Content-Type: application/json'\
   --data '{
    "settings": {
        "index": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        }
    },
    "mappings": {
        "properties": {
            "Date": {
                "type": "date"
            },
            "Minimum temperature (C)": {
                "type": "float"
            },
            "Maximum temperature (C)": {
                "type": "float"
            },
            "Rainfall (mm)": {
                "type": "float"
            },
            "Speed of maximum wind gust (km/h)": {
                "type": "float"
            }
        }
    }
}'| jq '.'
