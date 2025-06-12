import pandas as pd
import numpy as np

# Load original dataset
emp_df = pd.read_csv("synthetic_employees.csv")

# Choose standard deviation for noise: 10% of salary std dev
salary_std = emp_df['salary'].std()
sigma = 0.1 * salary_std

# Generate noise and perturb salary
noise = np.random.normal(loc=0, scale=sigma, size=len(emp_df))
perturbed_salaries = emp_df['salary'] + noise

# Optional: Clip to keep salaries in reasonable range (e.g., ≥ 0)
perturbed_salaries = perturbed_salaries.clip(lower=0).round(2)

# Create new DataFrame
prtrb_df = emp_df.copy()
prtrb_df['salary'] = perturbed_salaries

# Show output
print("prtrb_df.describe(include='all'):")
print(prtrb_df.describe(include='all'))

print("\nprtrb_df.head(10):")
print(prtrb_df.head(10))

