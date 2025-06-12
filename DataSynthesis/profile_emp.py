import pandas as pd
from ydata_profiling import ProfileReport

# Load your dataset
emp_df = pd.read_csv("synthetic_employees.csv")

# Generate the profile
profile = ProfileReport(emp_df, title="Employee Data Profile", explorative=True)

# Save as HTML file (recommended for GCP)
profile.to_file("employee_profile_report.html")

print("Profile report saved to employee_profile_report.html")

