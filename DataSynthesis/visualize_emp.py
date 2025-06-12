import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
df = pd.read_csv("synthetic_employees.csv")

# Convert date columns
df['birthdate'] = pd.to_datetime(df['birthdate'], errors='coerce')
df['hiredate'] = pd.to_datetime(df['hiredate'], errors='coerce')

# Visualization 1: Bar chart of CountryOfBirth counts (ordered)
plt.figure(figsize=(10, 6))
country_counts = df['CountryOfBirth'].value_counts()
sns.barplot(x=country_counts.index, y=country_counts.values)
plt.title("Employee Count by Country of Birth")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("01_country_of_birth.png")
plt.clf()

# Visualization 2: Department counts (ordered)
plt.figure(figsize=(10, 6))
dept_counts = df['department'].value_counts()
sns.barplot(x=dept_counts.index, y=dept_counts.values)
plt.title("Employee Count by Department")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("02_department_counts.png")
plt.clf()

# Visualization 3: Hires by day of week
df['hire_dayofweek'] = df['hiredate'].dt.day_name()
hireday_counts = df['hire_dayofweek'].value_counts().reindex([
    'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
])
sns.barplot(x=hireday_counts.index, y=hireday_counts.values)
plt.title("Employees Hired by Day of the Week")
plt.ylabel("Number of Employees")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("03_hire_dayofweek.png")
plt.clf()

# Visualization 4: KDE plot of salaries
sns.kdeplot(df['salary'], shade=True)
plt.title("KDE Plot of Salaries")
plt.xlabel("Salary (USD)")
plt.tight_layout()
plt.savefig("04_kde_salary.png")
plt.clf()

# Visualization 5: Line plot of birth year distribution
df['birth_year'] = df['birthdate'].dt.year
birth_year_counts = df['birth_year'].value_counts().sort_index()
birth_year_counts.plot(kind='line', marker='o')
plt.title("Employees Born Each Year")
plt.xlabel("Year")
plt.ylabel("Number of Employees")
plt.tight_layout()
plt.savefig("05_birth_year_line.png")
plt.clf()

# Visualization 6: KDE plots of salaries by department
plt.figure(figsize=(10, 6))
for dept in df['department'].unique():
    sns.kdeplot(df[df['department'] == dept]['salary'], label=dept, shade=True)
plt.title("KDE of Salaries by Department")
plt.xlabel("Salary (USD)")
plt.legend()
plt.tight_layout()
plt.savefig("06_kde_salary_by_dept.png")
plt.clf()

print("All plots generated and saved as PNG files.")

