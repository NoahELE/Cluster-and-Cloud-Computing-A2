# Team 64
# Kejing Li 1240956, Xin Su 1557128, Yueyang Li 1213643, Xinhao Chen 1166113, Zheqi Shen 1254834
import json
import os

import pandas as pd
import requests


def download_weather(location, code, year, month):
    # Format the month and URL
    month_str = f"{year}{month:02d}"  # Ensures the month is two digits
    url = f"https://reg.bom.gov.au/climate/dwo/{month_str}/text/IDCJDW{code}.{month_str}.csv"
    csv_filename = f"data/weather_csv/{location}_{month_str}.csv"
    json_filename = f"data/weather_json/{location}_{month_str}.json"

    # Fetch and save the CSV file
    response = requests.get(url)
    if response.status_code == 200:
        with open(csv_filename, "wb") as file:
            file.write(response.content)
        print(f"Successfully downloaded {csv_filename}")
    else:
        print(f"Failed to download data from {url}")

    if os.path.exists(csv_filename):
        # Read the CSV file
        # adjust skiprows as needed based on file structure
        weather = pd.read_csv(csv_filename, skiprows=5, encoding="iso-8859-1")
        weather = weather[
            [
                "Date",
                "Minimum temperature (°C)",
                "Maximum temperature (°C)",
                "Rainfall (mm)",
                "Speed of maximum wind gust (km/h)",
            ]
        ]
        # Rename the columns
        weather = weather.rename(
            columns={
                "Minimum temperature (°C)": "Minimum temperature (C)",
                "Maximum temperature (°C)": "Maximum temperature (C)",
            }
        )

        # # Convert DataFrame to JSON
        # weather_json = weather.to_dict(orient="records")
        # # Combine header and data
        # weather_json = {"header": location, "data": weather_json}
        # # Save JSON to file
        # with open(json_filename, "w") as f:
        #     json.dump(weather_json, f, indent=4)
        weather.to_json(json_filename, indent=2, orient="records")
        print(f"Successfully converted and saved {json_filename}")
    else:
        print(f"CSV file {csv_filename} does not exist")


# Iterate over each month from April 2023 to April 2024 for each station
station = {
    "Melbourne (Olympic Park)": "3033",
    # "Melbourne Airport": "3049",
    # "Avalon": "3003",
    # "Cerberus": "3014",
    # "Coldstream": "3016",
    # "Ferny Creek": "3102",
    # "Frankston (Ballam Park)": "3112",
    # "Geelong": "3030",
    # "Laverton": "3043",
    # "Moorabbin": "3052",
    # "Rhyll": "3070",
    # "Scoresby": "3072",
    # "Sheoaks": "3073",
}


if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists("data/weather_csv"):
    os.makedirs("data/weather_csv")

if not os.path.exists("data/weather_json"):
    os.makedirs("data/weather_json")

for location, code in station.items():
    for year in [2023, 2024]:
        for month in range(1, 13):
            if (year == 2023 and month >= 4) or (year == 2024 and month <= 5):
                download_weather(location, code, year, month)


def merge_json_files(directory_path, output_file_path):
    merged_data = []

    for file_name in os.listdir(directory_path):
        if file_name.endswith(".json"):
            file_path = os.path.join(directory_path, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                merged_data.extend(data)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(merged_data, output_file, indent=4)
        print("Successfully merged and saved data.")


directory_path = "data/weather_json"
output_file_path = "data/weather_json/gathered_bom_weather_past.json"
merge_json_files(directory_path, output_file_path)
