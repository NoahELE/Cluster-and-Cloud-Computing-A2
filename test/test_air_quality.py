import requests


def test_health():
    resp = requests.get("http://localhost:9090/air-quality/air-quality-avg/Box")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["avg_BPM25"], float)
