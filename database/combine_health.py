import json
import os

# Define a function to extract the required properties
def extract_properties(data):
    if "features" in data:
        features = data["features"]
        properties_list = []
        for feature in features:
            if "properties" in feature:
                properties = feature["properties"]
                properties_list.append(properties)
        return properties_list
    else:
        return []

output_file = "data/asthma_copd/asthma_copd_merged.json"

all_properties = []

# Iterate through the directory and read each JSON file
directory_path = "data/asthma_copd"
for filename in os.listdir(directory_path):
    file_path = os.path.join(directory_path, filename)
    if os.path.isfile(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            properties_list = extract_properties(data)
            all_properties.extend(properties_list)

# Write all properties to the JSON output file
with open(output_file, "w") as f:
    json.dump(all_properties, f)