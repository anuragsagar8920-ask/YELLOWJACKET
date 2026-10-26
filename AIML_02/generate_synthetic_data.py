# 

import pandas as pd
import numpy as np
import os
from datetime import datetime

# Reproducibility ke liye seed set kar rahe hain
np.random.seed(42)

# 1. Date Range Setup: Monthly dates from Jan 2010 to Dec 2024
date_range = pd.date_range(start='2010-01-01', end='2024-12-31', freq='MS')

# 2. Simulated Coordinates (e.g., Coastal / Ocean Region grid)
lats = np.linspace(10.0, 25.0, 10)
lons = np.linspace(70.0, 85.0, 10)

grid_lats, grid_lons = np.meshgrid(lats, lons)
flat_lats = grid_lats.flatten()
flat_lons = grid_lons.flatten()

data_rows = []

# 3. Generating synthetic features
for date in date_range:
    month_val = date.month
    seasonal_temp = 2.0 * np.sin(2 * np.pi * month_val / 12)
    
    for lat, lon in zip(flat_lats, flat_lons):
        temp_base = 26.0 + seasonal_temp + (lat * 0.1) - (lon * 0.05)
        ocean_temp = round(temp_base + np.random.normal(0, 0.8), 2)
        
        veg_base = 0.8 - 0.02 * ((ocean_temp - 26) ** 2)
        coastal_veg = round(float(np.clip(veg_base + np.random.normal(0, 0.05), 0.1, 0.9)), 3)
        
        data_rows.append({
            'date': date.strftime('%Y-%m-%d'),
            'latitude': round(lat, 4),
            'longitude': round(lon, 4),
            'ocean_temperature': ocean_temp,
            'vegetation_index': coastal_veg
        })

df = pd.DataFrame(data_rows)

# Save in current directory (AIML_02)
output_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(output_dir, 'synthetic_nasa_data.csv')
json_path = os.path.join(output_dir, 'synthetic_nasa_data.json')

df.to_csv(csv_path, index=False)
df.to_json(json_path, orient='records', date_format='iso')

print(f"Dataset generated successfully! Total records: {len(df)}")