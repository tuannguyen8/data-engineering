import pandas as pd

# Load the cleaned stop events DataFrame
stops_df = pd.read_csv("stops_df.csv")

print("\n--- Location 6913 Analysis ---")
# Filter by location 6913
location_df = stops_df[stops_df['location_id'] == 6913]

# Number of stops made at this location
num_stops_location = len(location_df)
print("Number of stops at location 6913:", num_stops_location)

# Number of different buses stopped 
unique_buses = location_df['vehicle_number'].nunique()
print("Number of unique vehicles at location 6913:", unique_buses)

# percentage had at least one boarding
boarding_events = len(location_df[location_df['ons'] >= 1])
boarding_percentage = (boarding_events / num_stops_location) * 100 if num_stops_location > 0 else 0
print(f"Percentage of stops with boarding at location 6913: {boarding_percentage:.2f}%")

print("\n--- Vehicle 4062 Analysis ---")
# Filter by vehicle 4062
vehicle_df = stops_df[stops_df['vehicle_number'] == 4062]

# Number of stops made by this vehicle
num_stops_vehicle = len(vehicle_df)
print("Number of stops made by vehicle 4062:", num_stops_vehicle)

# Number of total passengers boarded
total_boarded = vehicle_df['ons'].sum()
print("Total passengers boarded on vehicle 4062:", total_boarded)

# Number of passengers deboarded
total_deboarded = vehicle_df['offs'].sum()
print("Total passengers deboarded from vehicle 4062:", total_deboarded)

# Percentage of stops with at least one boarding
boarding_stops = len(vehicle_df[vehicle_df['ons'] >= 1])
boarding_vehicle_percentage = (boarding_stops / num_stops_vehicle) * 100 if num_stops_vehicle > 0 else 0
print(f"Percentage of stops with boarding on vehicle 4062: {boarding_vehicle_percentage:.2f}%")

