import pandas as pd
from scipy.stats import ttest_1samp

# Load relative position data
relpos_df = pd.read_csv("trimet_relpos_2022-12-07.csv")

# Rename and clean column headers if needed
relpos_df.columns = [col.strip().upper() for col in relpos_df.columns]

# Extract all RELPOS values (for null hypothesis)
all_relpos = relpos_df['RELPOS'].values

# Group by vehicle and perform t-test
results = []
for vehicle_id, group in relpos_df.groupby('VEHICLE_NUMBER'):
    vehicle_relpos = group['RELPOS'].values
    if len(vehicle_relpos) < 5:
        continue  # skip small samples to avoid unreliable t-tests
    t_stat, p_value = ttest_1samp(vehicle_relpos, popmean=all_relpos.mean())
    if p_value < 0.005:
        results.append((vehicle_id, len(vehicle_relpos), p_value))

# Show biased vehicles
print("Vehicles with GPS bias (p < 0.005):")
print("vehicle_id\tn_samples\tp_value")
for r in results:
    print(f"{r[0]}\t\t{r[1]}\t\t{r[2]:.6f}")

