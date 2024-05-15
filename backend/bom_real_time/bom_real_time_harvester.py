from datetime import datetime

import requests
from elasticsearch import Elasticsearch

melbourne_weather_url = "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
host = "https://elasticsearch-master.elastic.svc.cluster.local:9200"
basic_auth = ("elastic", "comp90024-elastic")
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)


def main():
    latest_weather = get_latest_weather()
    es.index(
        index="bom_melbourne_weather",
        id=latest_weather["datetime"],
        document=latest_weather,
    )
    return "OK"


def get_latest_weather():
    r = requests.get(melbourne_weather_url)
    weather_json = r.json()
    latest_weather = weather_json["observations"]["data"][0]
    dt_str = datetime.strptime(
        latest_weather["local_date_time_full"], "%Y%m%d%H%M%S"
    ).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    temperature = latest_weather["air_temp"]
    pressure = latest_weather["press"]
    rainfall = float(latest_weather["rain_trace"])
    relative_humidity = latest_weather["rel_hum"]
    wind_speed = latest_weather["wind_spd_kmh"]
    wind_direction = latest_weather["wind_dir"]

    return {
        "datetime": dt_str,
            "temperature": temperature,
        "pressure": pressure,
        "rainfall": rainfall,
        "relative_humidity": relative_humidity,
        "wind_speed": wind_speed,
        "wind_direction": wind_direction,
    }
