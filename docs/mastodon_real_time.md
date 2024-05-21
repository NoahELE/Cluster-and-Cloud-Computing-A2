# Mastodon Real Time Data

The code is in `backend/mastodon_real_time` folder.

## Code

### `mastodon_real_time_harvesterr.py`

This script is used to harvest real time weather data from Mastodon with tag "Melbourne".
It uses the `requests` library to get the data from Mastodon. It fetch the data from Mastodon every 30 minutes and store the latest data into `ElasticSearch` index `mastodon_melbourne`.


### `get_num_toots_by_date.py`

This script is used to provide an API for users to fetch the number of toots of a given day. The endpoint is `/get-num-toots-by-date/{date}`, where `date` is in the format `YYYY-MM-DD`. It fetches the data from `ElasticSearch` index `mastodon_melbourne`. The successful response will be in the format:

```json
{
  "ok": true,
  "num_of_toots": 10
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

### Mastodon Harvester
```bash
fission package create --spec\
--sourcearchive ./backend/mastodon_real_time/mastodon_real_time.zip
--env python\
--name mastodon-real-time\
--buildcmd './build.sh'

fission fn create --spec\
--name mastodon-real-time-harvester\
--pkg mastodon-real-time\
--env python\
--entrypoint "mastodon_real_time_harvester.main"\
--secret secrets
  
fission timer create --spec\
--name mastodon-real-time-harvester-every-30minutes\
--function mastodon-real-time-harvester --cron "@every 30m"
```

### Get Number of Toots by Date Route
```bash
fission fn create --spec \
--name get-num-toots-by-date\
--pkg mastodon-real-time\
--env python\
--entrypoint "get_num_toots_by_date.main"\
--secret secrets
  
fission route create --spec \
--url /get-num-toots-by-date/{date} \
--function get-num-toots-by-date \
--name get-num-toots-by-date \
--createingress
```

