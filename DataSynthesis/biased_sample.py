import pandas as pd
import numpy as np

# Load the employee dataset
emp_df = pd.read_csv("synthetic_employees.csv")
emp_df['birthdate'] = pd.to_datetime(emp_df['birthdate'], errors='coerce')

# Calculate age
today = pd.to_datetime("today")
emp_df['age'] = (today - emp_df['birthdate']).dt.days // 365

# Create bias weights: employees aged 40–49 get weight 3, others get 1
weights = np.where((emp_df['age'] >= 40) & (emp_df['age'] <= 49), 3, 1)

# Sample 500 with replacement=False
smpl_df = emp_df.sample(n=500, replace=False, weights=weights, random_state=42)

# Show stats and sample records
print("smpl_df.describe(include='all'):")
print(smpl_df.describe(include='all'))

print("\nsmpl_df.head(10):")
print(smpl_df.head(10))

