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

## Repository Contents
- Frontend: Jupyter notebooks source code of the client part of the application,
contains code for retrieve data through `REST` API, perform data analysis and visualisation.
- Backend: The application back-end source code, contains code for data harvester, store harvested data to `ElasticSearch`,
`Fission` trigger to retrieve data from `ElasticSearch`, and all necessary component to create `Fission` packages.
- Test: The application back-end automated tests for `Fission` routes.
- Database: Contain code to create `ElasticSearch` index and insert data into `ElasticSearch`.
- Data: Data that are inserted into `ElasticSearch`.
- Documentation: Documentation on backend API.


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
- Expose `/bom-real-time/avg-day-temp/{date}` to get the average temperature of a day

### BOM Past Data

Data Source: [Bureau of Meteorology](https://reg.bom.gov.au/)

Code in `database/get_bom_weather_past.py` and `data/weather_json` directory

- Get min and max temperature, rainfall (mm) and max wind speed for each day from April 2023 to May 2024

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

- Get SA2 code, asthma count, copd count, code of geographic feature and name of geographic feature in Greater Melbourne.

## Fission Spec

All details in folder `docs`

## Front-end

Jupyter notebooks in `frontend` directory, click `Run All` to execuate all cells to retrieve data through RESTful API and visualise data

`air_and_health.ipynb`: Focus on scenario - relationship between weather & air quality, air quality & health

`mastodon.ipynb`: Focus on scenario - relationship between weather & mastodon sentiment score

`traffic_and_toots.ipynb`: Focus on scenario - relationship between weather & traffic accidents, weather & number of mastodon toots

`frontend_merged.ipynb`: A typesetted collection of the former three files
