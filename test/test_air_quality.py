import requests


def test_air_quality():
    resp = requests.get(
        "http://localhost:9090/air-quality/air-quality-avg/Box/2021-01-01/365"
    )
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["avg_BPM25"], float)
