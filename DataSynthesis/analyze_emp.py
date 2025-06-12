import pandas as pd

# Load the CSV file
emp_df = pd.read_csv("synthetic_employees.csv")

# Show summary of all columns
print("emp_df.describe(include='all'):")
print(emp_df.describe(include='all'))

# Show first 10 rows
print("\nemp_df.head(10):")
print(emp_df.head(10))

# Total payroll
total_payroll = emp_df['salary'].sum()
print(f"\nTotal Yearly Payroll: ${total_payroll:,}")

