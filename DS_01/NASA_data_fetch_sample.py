# It's a simple script to fetch data from NASA's API and save it to a local file.

import pandas as pd
import requests

locations = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Kerala": {"lat": 10.8505, "lon": 76.2711},
}

url = "https://power.larc.nasa.gov/api/temporal/monthly/point"
params_base = {
    "parameters": "TS,PRECTOTCORR,GWETTOP",
    "community": "AG",
    "start": "2004",
    "end": "2024",
    "format": "CSV",
}

combined_dfs = []

for loc_name, coords in locations.items():
    print(f"\nFetching & Processing 20-Year Data for {loc_name}...")
    params = params_base.copy()
    params["latitude"] = coords["lat"]
    params["longitude"] = coords["lon"]

    response = requests.get(url, params=params)
    file_path = f"nasa_monthly_{loc_name.lower()}_raw.csv"

    if response.status_code == 200:
        with open(file_path, "w") as f:
            f.write(response.text)

        header_line = 0
        with open(file_path, "r") as f:
            for i, line in enumerate(f):
                if line.startswith("PARAMETER") or "PARAMETER,YEAR" in line:
                    header_line = i
                    break

        df = pd.read_csv(file_path, skiprows=header_line, na_values=[-999, -999.0])
        
        # Melt wide format (JAN-DEC) to long time-series format
        month_cols = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        df_long = df.melt(id_vars=['PARAMETER', 'YEAR'], value_vars=month_cols, var_name='MONTH', value_name='VALUE')
        
        # Pivot parameters into separate columns
        df_pivoted = df_long.pivot(index=['YEAR', 'MONTH'], columns='PARAMETER', values='VALUE').reset_index()
        
        # Create proper Datetime column
        df_pivoted['DATE'] = pd.to_datetime(df_pivoted['YEAR'].astype(str) + '-' + df_pivoted['MONTH'], format='%Y-%b')
        df_pivoted = df_pivoted.sort_values('DATE').reset_index(drop=True)
        df_pivoted['LOCATION'] = loc_name
        
        # Reorder columns
        df_clean = df_pivoted[['LOCATION', 'DATE', 'YEAR', 'MONTH', 'TS', 'PRECTOTCORR', 'GWETTOP']]
        df_clean.to_csv(f"nasa_monthly_{loc_name.lower()}_processed.csv", index=False)
        combined_dfs.append(df_clean)

        print(f"Cleaned Time-Series Data saved for {loc_name}: {df_clean.shape[0]} monthly entries.")
        print(df_clean.head(3))

# Combine all locations
final_df = pd.concat(combined_dfs, ignore_index=True)
final_df.to_csv("nasa_multi_region_processed.csv", index=False)
print("\n--- Final Merged Dataset Info ---")
print("Total Rows:", final_df.shape[0])