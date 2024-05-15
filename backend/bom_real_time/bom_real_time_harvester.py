# Xinhao Chen 1166113
from datetime import datetime

import requests
from elasticsearch import Elasticsearch


def secret(key: str) -> str:
    """Read secret from k8s secret volume"""
    with open(f"/secrets/default/secrets/{key}", "r", encoding="utf-8") as f:
        return f.read()


melbourne_weather_url = "https://reg.bom.gov.au/fwo/IDV60901/IDV60901.95936.json"
host = secret("ES_URL")
basic_auth = (secret("ES_USERNAME"), secret("ES_PASSWORD"))
es = Elasticsearch(host, basic_auth=basic_auth, verify_certs=False)


def main():
    """Harvest latest weather data from BOM and index it in Elasticsearch"""
    try:
        latest_weather = get_latest_weather()
        es.index(
            index="bom_melbourne_weather",
            id=latest_weather["datetime"],
            document=latest_weather,
        )
        return "OK"
    except Exception as e:
        return str(e)


def get_latest_weather():
    """Get latest weather data from BOM API"""
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
