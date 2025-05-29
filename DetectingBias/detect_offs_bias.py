import pandas as pd
from scipy.stats import chi2_contingency

# Load stops data
stops_df = pd.read_csv("stops_df.csv")

# System-wide totals
total_ons = stops_df['ons'].sum()
total_offs = stops_df['offs'].sum()

print(f"System-wide ons: {total_ons}")
print(f"System-wide offs: {total_offs}")

# Per-vehicle analysis
results = []

for vehicle_id, group in stops_df.groupby('vehicle_number'):
    vehicle_ons = group['ons'].sum()
    vehicle_offs = group['offs'].sum()

    if vehicle_ons + vehicle_offs < 10:
        continue  # skip small-sample vehicles to avoid noise

    # Construct contingency table
    contingency = [
        [vehicle_ons, vehicle_offs],
        [total_ons - vehicle_ons, total_offs - vehicle_offs]
    ]

    # Run chi-squared test
    chi2, p_value, dof, expected = chi2_contingency(contingency)

    if p_value < 0.05:
        results.append((vehicle_id, vehicle_ons, vehicle_offs, p_value))

# Output
print("\nVehicles with biased offs/ons ratios (p < 0.05):")
print("vehicle_id\tons\toffs\tp_value")
for r in results:
    print(f"{r[0]}\t\t{r[1]}\t{r[2]}\t{r[3]:.4f}")

