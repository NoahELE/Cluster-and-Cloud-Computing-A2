# Air Quality (BPM2.5) Data

The code is in `backend/air_quality' folder

## Code

### `air_quality_avg_bpm.py`

This script is used to provide an API for users to fetch the average BPM2.5 value of a given time range of a given station name. The endpoint is `/air-quality/air-quality-avg/{location}/{date}/{days}`, where `location` is one of the station names from `Alphington, Box, Brighton, Campbellfield, Footscray, Melbourne, Melton`, `date` is in the format `YYYY-MM-DD` and `days` is the time range in `String` type. 

It fetches the data from `ElasticSearch` index `air_quality_all`. The successfull response will be in the format:

```json
{
    "ok": true,
    "avg_BPM25": 4.0171
}
```

If an error occurs, the response will be in the format:

```json
{
    "ok": false,
    "error": "error message"
}
```

## Fission Spec

```bash
fission pkg create --name air-quality --sourcearchive backend/air_quality/air-quality.zip --env python --buildcmd './build.sh' --spec
fission fn create --name air-quality-avg --env python-spec --pkg air-quality --entrypoint "air_quality_avg_bpm.main" --secret secrets --spec
fission httptrigger create --name air-quality-avg --method GET --url "/air-quality/air-quality-avg/{location}/{date}/{days}" --function air-quality-avg --spec
```