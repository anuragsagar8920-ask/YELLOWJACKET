# It's a simple script to fetch data from NASA's API and save it to a local file.

import pandas as pd
import requests

# 1. API Endpoint & Parameters Configuration
url = "https://power.larc.nasa.gov/api/temporal/daily/point"

params = {
    "parameters": "TS",  # Earth Skin Temperature (Land Surface Temperature)
    "community": "AG",  # Agroclimatology
    "longitude": 78.9629,  # India Center Coordinates
    "latitude": 20.5937,
    "start": "20140101",  # 10 Years Range (2014-2024)
    "end": "20240101",
    "format": "CSV",
}

print("Fetching data from NASA POWER API...")
response = requests.get(url, params=params)

file_path = "nasa_lst_sample_raw.csv"

if response.status_code == 200:
    with open(file_path, "w") as f:
        f.write(response.text)
    print(f"Data successfully fetched and saved to {file_path}")
else:
    print(f"Failed to fetch data. Status Code: {response.status_code}")
    exit()

# 2. Dynamic Header Line Detection (Fixes ParserError)
header_line = 0
with open(file_path, "r") as f:
    for i, line in enumerate(f):
        if line.startswith("YEAR") or "YEAR,DOY" in line:
            header_line = i
            break

# 3. Read Clean Data Frame
df = pd.read_csv(file_path, skiprows=header_line, na_values=[-999, -999.0])

print("\n--- Data Integrity & Structure Check ---")
print("Data Shape (Rows, Columns):", df.shape)
print("\n--- Columns Info ---")
print(df.info())

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Missing Values Check ---")
print(df.isnull().sum())