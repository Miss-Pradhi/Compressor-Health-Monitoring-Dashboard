import pandas as pd
import random
from datetime import datetime, timedelta

data = []

start_time = datetime(2026, 1, 1, 8, 0)

compressors = ["C1", "C2", "C3"]

for hour in range(200):
    current_time = start_time + timedelta(hours=hour)

    for comp in compressors:
        pressure = round(random.uniform(10, 15), 1)
        temperature = round(random.uniform(65, 85), 1)
        vibration = round(random.uniform(2, 5), 1)
        running_hours = 1000 + hour

        data.append([
            current_time,
            comp,
            pressure,
            temperature,
            vibration,
            running_hours
        ])

df = pd.DataFrame(data, columns=[
    "Timestamp",
    "Compressor_ID",
    "Pressure_bar",
    "Temperature_C",
    "Vibration_mm_s",
    "Running_Hours"
])

df.to_csv("compressor_data.csv", index=False)

print("Dataset created successfully!")
print("\nFirst 5 rows:")
print(df.head())

print("\nTotal records:", len(df))