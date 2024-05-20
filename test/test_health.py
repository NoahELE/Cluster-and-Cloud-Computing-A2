import requests


def test_health():
    resp = requests.get("http://localhost:9090/health/get-health")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["json_data"], list)
