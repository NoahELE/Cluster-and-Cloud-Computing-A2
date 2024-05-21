# Spatialised Aggregated Health (Asthma & COPD) Data
The code is in `backend/health_geo' folder

## Code

### `get_health.py`

This script is used to provide an API for users to fetch all health data with geometry info from `ElasticSearch` index `health_geo`. The endpoint is `/health/get-health`.

The successfull response will be in the format:

```json
{
    "ok": true,
    "json_data": [{
        'Name_of_Geographic_feature': 'Pascoe Vale South',
        'asthma_count': 694,
        'copd_count': 71,
        'geometry': {
            'coordinates': [
                [
                    [144.932641059999, -37.7422639999991],
                    [144.932505059999, -37.7422660199991]
                ]
            ]
        }
    }]
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
fission pkg create --name health --sourcearchive ./backend/health_geo/health.zip --env python --buildcmd './build.sh' --spec
fission fn create --name get-health --env python-spec --pkg health --entrypoint "get_health.main" --secret secrets --spec
fission httptrigger create --name get-health --method GET --url "/health/get-health" --function get-health --spec
```