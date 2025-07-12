import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# --- Configuration ---
n_patients = 1000
n_days = 30
start_date = datetime(2025, 6, 1)
locations = ['Ward-A', 'Ward-B', 'Ward-C', 'Ward-D']
genders = ['Male', 'Female', 'Other']

# --- Data Storage ---
records = []

# --- Helper Functions ---
def generate_vitals():
    bp = np.random.normal(115, 15)
    pulse = np.random.normal(72, 12)
    temp = np.random.normal(98.6, 1.2)
    spo2 = np.random.normal(97, 2.5)
    return round(bp, 1), int(pulse), round(temp, 1), round(spo2, 1)

def generate_environment(location):
    base_aqi = {'Ward-A': 45, 'Ward-B': 70, 'Ward-C': 90, 'Ward-D': 60}
    base_density = {'Ward-A': 1800, 'Ward-B': 3200, 'Ward-C': 5000, 'Ward-D': 2500}
    return (
        base_aqi[location] + np.random.randint(-10, 10),
        base_density[location] + np.random.randint(-200, 200)
    )

# --- Dataset Generation ---
for patient_id in range(1, n_patients + 1):
    age = np.random.randint(10, 85)
    gender = random.choice(genders)
    location = random.choice(locations)

    for day in range(n_days):
        date = start_date + timedelta(days=day)
        bp, pulse, temp, spo2 = generate_vitals()

        fever = int(temp > 99.5)
        cough = int(np.random.rand() < 0.2)
        breath_short = int(spo2 < 94 or (pulse > 90 and temp > 99.5))

        air_quality, pop_density = generate_environment(location)

        # Simple anomaly logic
        is_anomaly = int(
            (bp > 140 or bp < 80 or temp > 100.5 or spo2 < 93 or pulse > 110)
            and air_quality > 90
        )

        records.append({
            "PatientID": patient_id,
            "Date": date.strftime('%Y-%m-%d'),
            "Age": age,
            "Gender": gender,
            "Location": location,
            "BP": round(bp, 1),
            "Pulse": pulse,
            "Temp": temp,
            "SpO2": spo2,
            "Fever": fever,
            "Cough": cough,
            "BreathShortness": breath_short,
            "AirQualityIndex": air_quality,
            "PopulationDensity": pop_density,
            "IsAnomaly": is_anomaly
        })

# --- Save as CSV ---
df = pd.DataFrame(records)
df.to_csv("community_health_full.csv", index=False)
print("✅ Dataset generated and saved as 'community_health_full.csv'")
