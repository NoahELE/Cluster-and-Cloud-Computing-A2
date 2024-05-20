# BOM Weather Real Time Data

The code is in `backend/bom_real_time` folder.

## Code

### `bom_real_time_harvester.py`

This script is used to harvest real time weather data from BOM website. It uses the `requests` library to get the data from the BOM website. It fetch the data from BOM website every 30 minutes and store the latest data into `ElasticSearch` index `bom_melbourne_weather`.

### `bom_real_time_avg_day_temp.py`

This script is used to provide an API for users to fetch the average temperature of a given day. The endpoint is `/bom-real-time/avg-day-temp/{date}`, where `date` is in the format `YYYY-MM-DD`. It fetches the data from `ElasticSearch` index `bom_melbourne_weather` and calculates the average temperature of the given day. The successful response will be in the format:

```json
{
  "ok": true,
  "avg_temp": 15.0
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
fission pkg create --name bom-real-time --sourcearchive backend/bom_real_time/bom_real_time.zip --env python --buildcmd './build.sh' --spec
fission fn create --name bom-real-time-avg-day-temp-spec --env python-spec --pkg bom-real-time-spec --entrypoint "bom_real_time_avg_day_temp.main" --secret secrets --spec
fission fn create --name bom-real-time-harvester --env python --pkg bom-real-time --entrypoint "bom_real_time_harvester.main" --secret secrets --spec
fission httptrigger create --name bom-real-time-avg-day-temp --method GET --url "/bom-real-time/avg-day-temp/{date}" --function bom-real-time-avg-day-temp --spec
fission timer create --name bom-real-time-harvester --function bom-real-time-harvester --cron "@every 30m" --spec
```
