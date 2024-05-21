# COMP90024 Cluster and Cloud Computing - Assignment 2

The repository contains the code and data for the COMP90024 Cluster and Cloud Computing Assignment 2. The project is a FaaS (Function as a Service) application that harvests data from various sources and performs analysis.

## Team Members

| Name        | Student ID | Email                           |
| ----------- | ---------- | ------------------------------- |
| Xinhao Chen | 1166113    | xinhaoc1@student.unimelb.edu.au |
| Yueyang Li  | 1213643    | yueyangl4@student.unimelb.edu.au|
| Xin Su      | 1557128    | xsu6@student.unimelb.edu.au     |
| Zheqi Shen  | 1254834    | zheqis@student.unimelb.edu.au   |
| Kejing Li   | 1240956    | kejingl1@student.unimelb.edu.au

## Installation

- Clone the repository
- Deploy `Kubernetes` cluster on `OpenStack` machines
- Deploy `Fission`, `Elasticsearch`, and `Kibana` on `Kubernetes` cluster
- Store credentials like `ES_URL`, `ES_USERNAME` and `ES_PASSWORD` to `Kubernetes` secrets
- Create the functions with `fission spec apply --wait`
- Open the `Jupyter` notebook in `frontend` and run the cells to perform analysis

## Data Sources

### BOM Real-Time Data

Data Source: [Bureau of Meteorology](https://reg.bom.gov.au/)

Code in `backend/bom_real_time` directory

- Harvest real-time weather data from BOM API and store in `Elasticsearch` every 30 minutes
- Expose `/bom-real-time/avg-day-temp/{date}` to get the average temperature of a day\

### Mastodon Past Data

Data Source: [Mastodon Aus.social instance](https://aus.social)

Code in `data/mastodon_past` directory

- Get toots ID, create time, content, language, sentiment and tag for each toot

### EPA Past Data

Data Source: [Environment Protection Authority](https://www.epa.vic.gov.au/)

Code in `data/air_quality_json` directory

- Get location id, location name, BPM2.5, date and time for stations that monitor BPM2.5 in Melbourne. 

### DataVic Past Data

Data Source: [DataVic](https://www.data.vic.gov.au/)

Code in `data/traffic` directory

- Get accident NO, accident date, accident time, latitude and longitude for each accident within 15 km of Melbourne Central.

### SUDO Past Data

Data Source: [Spatial Urban Data Observatory](https://sudo.eresearch.unimelb.edu.au)

Code in `data/health_geo` directory

- Get sa2 code, asthma count, copd count, code of geographic feature and name of geographic feature in Greater Melbourne.

## Fission Spec

create get-bom-mastodon-by-date package:  
fission package create --spec --sourcearchive ./backend/bom_mastodon/get_bom_mastodon_by_date.zip  --env python  --name get-bom-mastodon-by-date  --buildcmd './build.sh'

create get-bom-mastodon-by-date function:
fission fn create --spec --name get-bom-mastodon-by-date\
  --pkg get-bom-mastodon-by-date\
  --env python\
  --entrypoint "get_bom_mastodon_by_date.main"\
  --secret secrets
  
create get-bom-mastodon-by-date trigger:
fission route create --spec --url /bom-mastodon/{date} --function get-bom-mastodon-by-date --name get-bom-mastodon-by-date --createingress

create mastodon-real-time package:
fission package create --spec --sourcearchive ./backend/mastodon_real_time/mastodon_real_time.zip  --env python  --name mastodon-real-time  --buildcmd './build.sh'

create mastodon-real-time-harvester function:
fission fn create --spec --name mastodon-real-time-harvester\
  --pkg mastodon-real-time\
  --env python\
  --entrypoint "mastodon_real_time_harvester.main"\
  --secret secrets
  
create mastodon-real-time-harvester timer trigger:
fission timer create --spec --name mastodon-real-time-harvester-every-30minutes --function mastodon-real-time-harvester --cron "@every 30m"

create get-num-toots-by-date function:
fission fn create --spec --name get-num-toots-by-date\
  --pkg mastodon-real-time\
  --env python\
  --entrypoint "get_num_toots_by_date.main"\
  --secret secrets
  
create get-num-toots-by-date trigger:
fission route create --spec --url /get-num-toots-by-date/{date} --function get-num-toots-by-date --name get-num-toots-by-date --createingress

