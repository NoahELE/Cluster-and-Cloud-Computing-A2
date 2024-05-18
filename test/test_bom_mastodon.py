import requests


def test_bom_avg_day_temp():
    resp = requests.get("http://127.0.0.1:9090/bom-mastodon/2023-05-18")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["bom_dict"], dict)


def test_bom_avg_day_temp_malformed_date():
    resp = requests.get("http://127.0.0.1:9090/bom-mastodon/aaa")
    resp_json = resp.json()
    assert not resp_json["ok"]
    assert isinstance(resp_json["error"], str)
