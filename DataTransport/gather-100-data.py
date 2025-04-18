import csv
import json
import requests

input_file = "data.csv"
output_file = "busses-100.json"

vehicle_ids = []

# Read first 100 valid vehicle IDs from Glitch column
with open(input_file, newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            vid = int(row["Glitch"])
            if 1000 <= vid <= 9999:  # ensure it's a 4-digit ID
                vehicle_ids.append(vid)
        except (ValueError, KeyError):
            continue
        if len(vehicle_ids) >= 100:
            break

print(f"Found {len(vehicle_ids)} valid 4-digit vehicle IDs.")

# Fetch data using the API
all_data = []
for vid in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    print(f"Fetching data for vehicle {vid}...")
    response = requests.get(url)
    if response.ok:
        data = response.json()
        all_data.extend(data)
        print(f"Received {len(data)} records.")
    else:
        print(f"Failed to fetch data for {vid} (status: {response.status_code})")

# Save to JSON
with open(output_file, "w") as f:
    json.dump(all_data, f, indent=2)

print(f"\nSaved {len(all_data)} records to {output_file}.")