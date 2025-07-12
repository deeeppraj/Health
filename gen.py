import pandas as pd
import numpy as np
import random
import datetime
import os

os.makedirs("data", exist_ok=True)

names = ["Ananya", "Rohit", "Kiran", "Sanya", "Aditya", "Priya", "Nikhil", "Meera", "Arjun", "Kavya"]
genders = ["Male", "Female", "Other"]
medications = ["Paracetamol", "Amoxicillin", "Atorvastatin", "Ibuprofen", "Metformin", "Omeprazole"]
frequencies = ["Once daily", "Twice daily", "Thrice daily", "As needed"]

records = []
for i in range(500):
    abha_id = f"ABHA-{i:04d}"
    name = random.choice(names) + " " + random.choice(["Sharma", "Verma", "Nair", "Khan", "Das"])
    age = np.random.randint(1, 80)
    gender = random.choice(genders)
    medication = random.choice(medications)
    dosage = f"{random.randint(100, 1000)} mg"
    frequency = random.choice(frequencies)
    start_date = datetime.date.today() - datetime.timedelta(days=random.randint(1, 60))
    duration_days = random.choice([5, 7, 10, 15])
    end_date = start_date + datetime.timedelta(days=duration_days)

    records.append({
        "ABHA_ID": abha_id,
        "Name": name,
        "Age": age,
        "Gender": gender,
        "Medication": medication,
        "Dosage": dosage,
        "Frequency": frequency,
        "Start Date": start_date.strftime('%Y-%m-%d'),
        "End Date": end_date.strftime('%Y-%m-%d')
    })

df = pd.DataFrame(records)
df.to_csv("data/medication_data.csv", index=False)
print("✅ Medication records saved to data/medication_data.csv")
