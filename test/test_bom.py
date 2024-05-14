import requests


def test_bom_avg_day_temp():
    resp = requests.get("http://127.0.0.1:9090/bom-real-time/avg-day-temp/2024-05-13")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["avg_temp"], float)
