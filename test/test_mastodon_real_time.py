import requests


def test_bom_avg_day_temp():
    resp = requests.get("http://127.0.0.1:9090/get-num-toots-by-date/2024-05-18")
    resp_json = resp.json()
    assert resp_json["ok"]
    assert isinstance(resp_json["num_of_toots"], int)


def test_bom_avg_day_temp_malformed_date():
    resp = requests.get("http://127.0.0.1:9090/get-num-toots-by-date/aaa")
    resp_json = resp.json()
    assert not resp_json["ok"]
    assert isinstance(resp_json["error"], str)
