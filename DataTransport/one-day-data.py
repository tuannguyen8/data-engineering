import csv
import requests
import json

vehicle_ids = []

# Read first column of every row
with open("data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row:
            try:
                vehicle_ids.append(int(row[0]))
            except ValueError:
                continue

# Remove duplicates
vehicle_ids = list(set(vehicle_ids))

print(f"Fetching data for {len(vehicle_ids)} unique vehicle IDs...")

all_data = []

for vid in vehicle_ids:
    url = f"https://busdata.cs.pdx.edu/api/getBreadCrumbs?vehicle_id={vid}"
    response = requests.get(url)
    if response.ok:
        data = response.json()
        all_data.extend(data)
        print(f"Vehicle {vid}: {len(data)} records")
    else:
        print(f"Failed to fetch data for VehicleID {vid}")

# Save all data
with open("vehicle_data.json", "w") as f:
    json.dump(all_data, f, indent=2)

print(f"Saved total of {len(all_data)} records to vehicle_data.json")