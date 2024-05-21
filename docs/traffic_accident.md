# Traffic Data

The code is in `backend/traffic_accident' folder

## Code

### `traffic_count.py`

This script is used to provide an API for users to fetch the number of traffic accidents and number of accidents happen within a 15 km radius of Melbourne of a given date. The endpoint is `/traffic-accident/accident-count/{date}`, `date` is in the format `YYYY-MM-DD`.

It fetches the data from `ElasticSearch` index `traffic`. The successfull response will be in the format:

```json
{
    "ok": true,
    "accident_count": 40,
    "center_accidents": 13,
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
fission pkg create --name traffic-accident --sourcearchive backend/traffic_accident/traffic-accident.zip --env python --buildcmd './build.sh' --spec
fission fn create --name count --env python-spec --pkg traffic-accident --entrypoint "accident_count.main" --secret secrets --spec
fission httptrigger create --name traffic-count --method GET --url "/traffic-accident/accident-count/{date}" --function count --spec
```