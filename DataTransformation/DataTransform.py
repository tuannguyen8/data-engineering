import pandas as pd
from datetime import datetime, timedelta

# Read the CSV into a DataFrame
#df = pd.read_csv("bc_trip259172515_230215.csv")
df = pd.read_csv("bc_veh4223_230215.csv")

# Print the first 5 rows 
print(df.head())


# Load only 
# Read only the useful columns (exclude the ones we want to drop)
df = pd.read_csv("bc_trip259172515_230215.csv", usecols=[
    "EVENT_NO_TRIP", "OPD_DATE", "VEHICLE_ID", "METERS", "ACT_TIME",
    "GPS_LONGITUDE", "GPS_LATITUDE"
])

# Clean column names just in case
df.columns = df.columns.str.strip()

# Define a function to compute timestamp from a row
def compute_timestamp(row):
    date_str = row["OPD_DATE"].split(":")[0]  # Get "15FEB2023"
    base_date = datetime.strptime(date_str, "%d%b%Y")  # Convert to datetime
    return base_date + timedelta(seconds=row["ACT_TIME"])  # Add ACT_TIME as timedelta

# Apply function to every row to create a new TIMESTAMP column
df["TIMESTAMP"] = df.apply(compute_timestamp, axis=1)

# Drop OPD_DATE and ACT_TIME
df = df.drop(columns=["OPD_DATE", "ACT_TIME"])

# Compute deltas
# df["dMETERS"] = df["METERS"].diff()
# df["dSECONDS"] = df["TIMESTAMP"].diff().dt.total_seconds()

df["dMETERS"] = df.groupby("EVENT_NO_TRIP")["METERS"].diff()
df["dSECONDS"] = df.groupby("EVENT_NO_TRIP")["TIMESTAMP"].diff().dt.total_seconds()

# Compute speed (meters per second), avoid division by zero
df["SPEED"] = df.apply(lambda row: row["dMETERS"] / row["dSECONDS"] if row["dSECONDS"] > 0 else 0, axis=1)

# Drop intermediate columns
df = df.drop(columns=["dMETERS", "dSECONDS"])

# Print min, max, and average speed
# print("Minimum speed (m/s):", df["SPEED"].min())
# print("Maximum speed (m/s):", df["SPEED"].max())
# print("Average speed (m/s):", df["SPEED"].mean())

# Summary statistics
max_speed = df["SPEED"].max()
median_speed = df["SPEED"].median()
max_speed_row = df[df["SPEED"] == max_speed].iloc[0]

# Print results
print("Maximum speed (m/s):", max_speed)
print("Location: (Lat:", max_speed_row["GPS_LATITUDE"], ", Long:", max_speed_row["GPS_LONGITUDE"], ")")
print("Time:", max_speed_row["TIMESTAMP"])
print("Median speed (m/s):", median_speed)

# print a few rows
print(df[["METERS", "TIMESTAMP", "SPEED"]].head(10))

# Show final columns
# print("Remaining columns in DataFrame:")
# print(df.columns.tolist())

# Parse OPD_DATE into a pandas datetime 
# df["OPD_DATE_CLEAN"] = df["OPD_DATE"].str.extract(r"(^\d{1,2}[A-Z]{3}\d{4})")

# Convert to datetime
# df["OPD_DATE_CLEAN"] = pd.to_datetime(df["OPD_DATE_CLEAN"], format="%d%b%Y")

# Add ACT_TIME seconds to OPD_DATE_CLEAN
# df["TIMESTAMP"] = df["OPD_DATE_CLEAN"] + pd.to_timedelta(df["ACT_TIME"], unit="s")

# drop the cleaned OPD_DATE column if no longer needed
# df = df.drop(columns=["OPD_DATE_CLEAN"])

# Show result
# print(df[["OPD_DATE", "ACT_TIME", "TIMESTAMP"]].head())

# print(df.head())