import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "Virgin Islands, U.S.": "VI",
}
   
# Read the CSV files
cases_df = pd.read_csv("covid_confirmed_usafacts.csv")
deaths_df = pd.read_csv("covid_deaths_usafacts.csv")
census_df = pd.read_csv("acs2017_county_data.csv")

# Trim columns
# Keep 'County Name', 'State', and '2023-07-23' (last COVID date)
cases_df = cases_df[['County Name', 'State', '2023-07-23']]
deaths_df = deaths_df[['County Name', 'State', '2023-07-23']]

# Rename the date column for clarity
cases_df.rename(columns={'2023-07-23': 'Cases'}, inplace=True)
deaths_df.rename(columns={'2023-07-23': 'Deaths'}, inplace=True)

# For census data, keep relevant columns
census_df = census_df[['County', 'State', 'TotalPop', 'IncomePerCap', 'Poverty', 'Unemployment']]

# Show column headers to verify
print("Cases DataFrame columns:", cases_df.columns.tolist())
print("Deaths DataFrame columns:", deaths_df.columns.tolist())
print("Census DataFrame columns:", census_df.columns.tolist())

# Remove trailing spaces from 'County Name' columns
cases_df['County Name'] = cases_df['County Name'].str.strip()
deaths_df['County Name'] = deaths_df['County Name'].str.strip()

# Test for "Washington County"
cases_count = cases_df[cases_df['County Name'] == "Washington County"].shape[0]
deaths_count = deaths_df[deaths_df['County Name'] == "Washington County"].shape[0]

print(f"'Washington County' in cases_df: {cases_count}")
print(f"'Washington County' in deaths_df: {deaths_count}")

# Remove rows where 'County Name' is "Statewide Unallocated"
cases_df = cases_df[cases_df['County Name'] != "Statewide Unallocated"]
deaths_df = deaths_df[deaths_df['County Name'] != "Statewide Unallocated"]

# Count remaining rows
print("Rows remaining in cases_df:", len(cases_df))
print("Rows remaining in deaths_df:", len(deaths_df))

# Invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

# Convert state abbreviations to full names using your inverted dictionary
cases_df['State'] = cases_df['State'].map(abbrev_to_us_state)
deaths_df['State'] = deaths_df['State'].map(abbrev_to_us_state)

# Show the first few rows of cases_df to verify
print(cases_df.head())

# Create 'key' column in all three DataFrames
cases_df['key'] = cases_df['County Name'] + ", " + cases_df['State']
deaths_df['key'] = deaths_df['County Name'] + ", " + deaths_df['State']
census_df['key'] = census_df['County'] + ", " + census_df['State']

# Set 'key' as the index
cases_df.set_index('key', inplace=True)
deaths_df.set_index('key', inplace=True)
census_df.set_index('key', inplace=True)

# Show first few rows of census_df
print(census_df.head())

# Rename the 2023-07-23 column
cases_df.rename(columns={"2023-07-23": "Cases"}, inplace=True)
deaths_df.rename(columns={"2023-07-23": "Deaths"}, inplace=True)

# Show the column headers
print("cases_df columns:", cases_df.columns.values.tolist())
print("deaths_df columns:", deaths_df.columns.values.tolist())

# Join cases and deaths into census
join_df = census_df.join(cases_df[['Cases']])
join_df = join_df.join(deaths_df[['Deaths']])

# Calculate per capita rates
join_df['CasesPerCap'] = join_df['Cases'] / join_df['TotalPop']
join_df['DeathsPerCap'] = join_df['Deaths'] / join_df['TotalPop']

# Show number of rows
print("Number of rows in join_df:", join_df.shape[0])

# Construct the correlation matrix
correlation_matrix = join_df.corr(numeric_only=True)

# Display the matrix
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)

plt.title('Correlation Matrix Heatmap')
plt.tight_layout()

# Save the plot as an image file
plt.savefig("correlation_heatmap.png")
