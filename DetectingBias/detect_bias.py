import pandas as pd
from scipy.stats import binomtest

# Load the stop events DataFrame
stops_df = pd.read_csv("stops_df.csv")

# Calculate overall boarding rate
total_stops = len(stops_df)
total_boarding_stops = len(stops_df[stops_df['ons'] >= 1])
p_overall = total_boarding_stops / total_stops
print(f"Overall system-wide boarding rate: {p_overall:.4f}")

# Check each vehicle
results = []
for vehicle_id, group in stops_df.groupby('vehicle_number'):
    n = len(group)  # total stops for this vehicle
    x = len(group[group['ons'] >= 1])  # stops with boarding
    result = binomtest(x, n, p_overall, alternative='two-sided')
    p_value = result.pvalue
    if p_value < 0.05:
        results.append((vehicle_id, x, n, x/n, p_value))

# Display results with bias
print("\nVehicles with statistically biased boarding behavior (p < 0.05):")
print("vehicle_id\tx\tn\tboarding_rate\tp_value")
for r in results:
    print(f"{r[0]}\t\t{r[1]}\t{r[2]}\t{r[3]:.2f}\t\t{r[4]:.4f}")

