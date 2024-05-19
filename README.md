# COMP90024 Cluster and Cloud Computing - Assignment 2

The repository contains the code and data for the COMP90024 Cluster and Cloud Computing Assignment 2. The project is a FaaS (Function as a Service) application that harvest data from various sources and perform analysis.

## Team Members

| Name        | Student ID | Email                           |
| ----------- | ---------- | ------------------------------- |
| Xinhao Chen | 1166113    | xinhaoc1@student.unimelb.edu.au |
| Yueyang Li  | 1213643    | yueyangl4@student.unimelb.edu.au|

## Installation

- Clone the repository
- Deploy `Kubernetes` cluster on `OpenStack` machines
- Deploy `Fission`, `Elasticsearch`, `Kibana` on `Kubernetes` cluster
- Store credentials like `ES_URL`, `ES_USERNAME` and `ES_PASSWORD` to `Kubernetes` secrets
- Create the functions with `fission spec apply --wait`
- Open the `Jupyter` notebook in `frontend` and run the cells to perform analysis

## Data Sources

### BOM Real Time Data

Data Source: [Bureau of Meteorology](https://reg.bom.gov.au/)

Code in `backend/bom_real_time` directory

- Harvest real time weather data from BOM API and store in `Elasticsearch` every 30 minutes
- Expose `/bom-real-time/avg-day-temp/{date}` to get the average temperature of a day\

### Mastodon Past Data

Data Source: [Mastodon Aus.social instance](https://aus.social)

Code in `data/mastodon_past` directory

- Get toots ID, create time, content, language, sentiment and tag for each toot



