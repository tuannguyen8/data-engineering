from datetime import datetime
from collections import defaultdict
import csv

file_path = "employees.csv"

# Existence assertion counters
missing_name_count = 0
missing_address_count = 0

# Limit assertion counters
early_hire_count = 0
low_salary_count = 0

# Intra-record assertion counters
invalid_birth_vs_hire_count = 0
underage_hire_count = 0

# Inter-record assertion counters
invalid_manager_count = 0
duplicate_phone_count = 0

# Summary assertion storage
city_counts = defaultdict(int)
manager_counts = defaultdict(int)

# Store data for inter- and summary-record checks
all_rows = []
employee_ids = set()
phone_numbers = set()
duplicate_phones_seen = set()
salaries = []

# First pass: read data and apply per-record assertions
with open(file_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        all_rows.append(row)
        employee_ids.add(row["eid"])

        # Existence assertions
        if not row["name"].strip():
            missing_name_count += 1
        if not row["address"].strip():
            missing_address_count += 1

        # Limit assertions
        hire_year = int(row["hire_date"].split("-")[0])
        if hire_year < 2015:
            early_hire_count += 1

        salary = float(row["salary"])
        salaries.append(salary)
        if salary < 70000:
            low_salary_count += 1

        # Intra-record assertions
        birth_date = datetime.strptime(row["birth_date"], "%Y-%m-%d")
        hire_date = datetime.strptime(row["hire_date"], "%Y-%m-%d")

        if birth_date >= hire_date:
            invalid_birth_vs_hire_count += 1

        age_at_hire = (hire_date - birth_date).days // 365
        if age_at_hire < 18:
            underage_hire_count += 1
        # Inter-record prep: collect phones
        phone = row["phone"].strip()
        if phone in phone_numbers:
            duplicate_phones_seen.add(phone)
        else:
            phone_numbers.add(phone)

        # Summary assertions prep
        city = row["city"].strip()
        city_counts[city] += 1

        manager_id = row["reports_to"].strip()
        if manager_id:
            manager_counts[manager_id] += 1

# Second pass: inter-record validation
for row in all_rows:
    manager_id = row["reports_to"].strip()
    if manager_id and manager_id not in employee_ids:
        invalid_manager_count += 1

duplicate_phone_count = len(duplicate_phones_seen)
cities_with_only_one_employee = [city for city, count in city_counts.items() if count == 1]
managers_with_less_than_two = [mid for mid, count in manager_counts.items() if count < 2]

# Final output
print(f"Missing 'name' field: {missing_name_count} records")
print(f"Missing 'address' field: {missing_address_count} records")
print(f"Hired before 2015: {early_hire_count} records")
print(f"Salary less than $70,000: {low_salary_count} records")
print(f"Birth after or on hire date: {invalid_birth_vs_hire_count} records")
print(f"Hired under age 18: {underage_hire_count} records")
print(f"'reports_to' not a valid employee ID: {invalid_manager_count} records")
print(f"Duplicate phone numbers: {duplicate_phone_count} unique duplicates found")