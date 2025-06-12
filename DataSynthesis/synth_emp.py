from faker import Faker
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Country and locale setup
countries = {
    'USA': 0.60,
    'India': 0.20,
    'China': 0.05,
    'Mexico': 0.03,
    'Canada': 0.03,
    'Philippines': 0.03,
    'Taiwan': 0.03,
    'South Korea': 0.03
}

country_locale_map = {
    'USA': 'en_US',
    'India': 'en_IN',
    'China': 'zh_CN',
    'Mexico': 'es_MX',
    'Canada': 'en_CA',
    'Philippines': 'en_PH',
    'Taiwan': 'zh_TW',
    'South Korea': 'ko_KR'
}

departments = {
    'Engineering': ['Software Engineer', 'DevOps Engineer'],
    'HR': ['Recruiter', 'HR Manager'],
    'Finance': ['Accountant', 'Financial Analyst'],
    'Sales': ['Sales Executive', 'Account Manager']
}

salary_ranges = {
    'Software Engineer': (80000, 140000),
    'DevOps Engineer': (85000, 130000),
    'Recruiter': (50000, 80000),
    'HR Manager': (70000, 100000),
    'Accountant': (60000, 85000),
    'Financial Analyst': (65000, 95000),
    'Sales Executive': (50000, 90000),
    'Account Manager': (60000, 95000)
}

def sample_countries(n):
    country_list = []
    for country, prob in countries.items():
        count = int(n * prob)
        country_list.extend([country] * count)
    while len(country_list) < n:
        country_list.append('USA')
    random.shuffle(country_list)
    return country_list

def generate_employee_data(n=10000):
    country_list = sample_countries(n)
    data = []
    used_emails = set()
    genders = ['female'] * 49 + ['male'] * 49 + ['nonbinary'] * 2

    for i in range(n):
        emp_id = random.randint(100000000, 999999999)
        country = country_list[i]
        locale = country_locale_map[country]
        fake = Faker(locale)
        us_fake = Faker('en_US')

        # Personal Info
        name = fake.name()
        gender = random.choice(genders)
        age = random.randint(20, 65)
        birthdate = datetime.today() - timedelta(days=age*365 + random.randint(0, 364))

        # Hiredate: after age 20, not before 2010
        min_hire_age = 20
        # hire_year = random.randint(max(2010, birthdate.year + min_hire_age), 2023)
        min_hire_year = max(2010, birthdate.year + min_hire_age)
        max_hire_year = min(2023, min_hire_year + 45)  # Prevent from going beyond range
        if min_hire_year > 2023:
            hire_year = 2023  # fallback to the latest allowed
        else:
            hire_year = random.randint(min_hire_year, 2023)

        hiredate = datetime(hire_year, random.randint(1,12), random.randint(1,28))

        # Email and phone
        email_base = fake.user_name()
        email = f"{email_base}_{i}@example.com"
        while email in used_emails:
            email = f"{email_base}_{i}_{random.randint(1,999)}@example.com"
        used_emails.add(email)

        phone = us_fake.phone_number()
        ssid = us_fake.ssn()

        # Department, Role, Salary
        dept = random.choice(list(departments.keys()))
        role = random.choice(departments[dept])
        salary = random.randint(*salary_ranges[role])

        data.append({
            'employeeID': emp_id,
            'CountryOfBirth': country,
            'name': name,
            'phone': phone,
            'email': email,
            'gender': gender,
            'birthdate': birthdate.date(),
            'hiredate': hiredate.date(),
            'department': dept,
            'role': role,
            'salary': salary,
            'SSID': ssid
        })

    return pd.DataFrame(data)

if __name__ == "__main__":
    emp_df = generate_employee_data(10000)
    emp_df.to_csv("synthetic_employees.csv", index=False)
    print("synthetic_employees.csv created with 10,000 records.")

