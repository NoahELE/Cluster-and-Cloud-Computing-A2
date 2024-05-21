# Bom Mastodon Route

The code is in `backend/bom_mastodon` folder.

### `get_num_toots_by_date.py`

This script is used to provide an API for users to fetch weather and sentiment information of a given day. The endpoint is `/bom-mastodo/{date}`, where `date` is in the format `YYYY-MM-DD`. It fetches the data from `ElasticSearch` index `bom_mastodon`. The successful response will be in the format:

```json
{
  "ok": true,
  "resp_dict": {
        "sentiment_dict": {
            "min_sentiment": 0.11,
            "max_sentiment": 0.72,
            "average_sentiment": 0.35
        },
    
        "num_of_toots": 10,
    
        "bom_dict": {
          "min_temp": 11.3,
          "max_temp": 16.4,
          "average_temp":15.0,
          "rainfall": 4.6,
          "wind_gust_speed": 33
        }
    }
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
##### create get-bom-mastodon-by-date package:  
fission package create --spec \
--sourcearchive ./backend/bom_mastodon/get_bom_mastodon_by_date.zip  \
--env python  \
--name get-bom-mastodon-by-date  \
--buildcmd './build.sh'

##### create get-bom-mastodon-by-date function:
fission fn create --spec \
--name get-bom-mastodon-by-date\
--pkg get-bom-mastodon-by-date\
--env python\
--entrypoint "get_bom_mastodon_by_date.main"\
--secret secrets
  
##### create get-bom-mastodon-by-date trigger:
fission route create --spec \
--url /bom-mastodon/{date} \
--function get-bom-mastodon-by-date \
--name get-bom-mastodon-by-date \
--createingress
```