import matplotlib.pyplot as plt
import csv

file_path = "employees.csv"
salaries = []

# Read the salaries from the file
with open(file_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            salary = float(row["salary"])
            salaries.append(salary)
        except ValueError:
            continue  # skip rows with invalid/missing salary

# Show histogram of salary distribution
plt.figure(figsize=(10, 6))
plt.hist(salaries, bins=30, edgecolor='black')
plt.title("Salary Distribution Histogram")
plt.xlabel("Salary")
plt.ylabel("Number of Employees")
plt.grid(True)
plt.tight_layout()

# Save the histogram 
plt.savefig("salary_histogram.png")
print("Histogram saved as salary_histogram.png")

# New assertion: average salary should be between 80,000 and 150,000
average_salary = sum(salaries) / len(salaries)
if 80000 <= average_salary <= 150000:
    print(f"Average salary is ${average_salary:.2f} — valid")
else:
    print(f"Average salary is ${average_salary:.2f} — NOT valid")