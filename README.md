# COMP90024 Cluster and Cloud Computing - Assignment 2

The repository contains the code and data for the COMP90024 Cluster and Cloud Computing Assignment 2. The project is a FaaS (Function as a Service) application that harvest data from various sources and perform analysis.

## Team Members

| Name        | Student ID | Email                           |
| ----------- | ---------- | ------------------------------- |
| Xinhao Chen | 1166113    | xinhaoc1@student.unimelb.edu.au |

## Installation

- Clone the repository
- Deploy `Kubernetes` cluster on `OpenStack` machines
- Deploy `Fission`, `Elasticsearch`, `Kibana` on `Kubernetes` cluster
- Store credentials like `ES_URL`, `ES_USERNAME` and `ES_PASSWORD` to `Kubernetes` secrets
- Create functions inside `backend` directory on `Fission` with the following commands
  - `fission pkg create --source <function_directory> --env python`
  - `fission fn create --name <function_name> --pkg <pkg_name> --entrypoint <entrypoint> --secret <secret_name>`
- Create triggers inside `backend` directory on `Fission` with the following commands
  - `fission timer create --name <timer_name> --function <function_name> --cron <cron_expression>`
  - `fission httptrigger create --name <http_route_name> --function <function_name> --url <url> --method <method>`
- Open the `Jupyter` notebook in `frontend` and run the cells to perform analysis

## Data Sources

### BOM Real Time Data

Data Source: [Bureau of Meteorology](https://reg.bom.gov.au/)

Code in `backend/bom_real_time` directory

- Harvest real time weather data from BOM API and store in `Elasticsearch` every 30 minutes
- Expose `/bom-real-time/avg-day-temp/{date}` to get the average temperature of a day
