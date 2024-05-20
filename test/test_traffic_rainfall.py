import requests


def test_traffic_count():
    resp = requests.get(
        "http://localhost:9090/traffic-accident/accident-count/2023-04-01"
    )
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["accident_count"], int)
    assert isinstance(resp_json["center_accidents"], int)


def test_rainfall():
    resp = requests.get("http://localhost:9090/bom-past-rainfall/rainfall/2023-04-01")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["rainfall_amount"], float)
    assert isinstance(resp_json["rainfall_date"], str)
