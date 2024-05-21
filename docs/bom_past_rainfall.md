# BOM Weather Past Data

The code is in `backend/bom_past_rainfall` folder.

## Code

### `rainfall.py`

This script is used to provide an API for users to fetch the rainfall amount of a given day. The endpoint is `/bom-past-rainfall/rainfall/{date}`, where `date` is in the format `YYYY-MM-DD`.
It fetches the data from `ElasticSearch` index `bom_melbourne_weather_past`. The successful response will be in the format:

```json
{
  "ok": true,
  "rainfall_date": "2023-04-01",
  "rainfall_amount": 4.3
}
```

If an error occurs, for example the date format is incorrect, the response will be in the format:

```json
{
  "ok": false,
  "error": "Error message"
}
```

## Fission Spec

```bash
fission pkg create --name bom-past-rainfall --sourcearchive backend/bom_past_rainfall/bom-past-rainfall.zip --env python --buildcmd './build.sh' --spec
fission fn create --name rainfall --env python-spec --pkg bom-past-rainfall --entrypoint "rainfall.main" --secret secrets --spec
fission httptrigger create --name get-rainfall --method GET --url "/bom-past-rainfall/rainfall/{date}" --function rainfall --spec
```
