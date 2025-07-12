import pandas as pd
import numpy as np
import random
import datetime
import os

os.makedirs("data", exist_ok=True)

names = ["Ananya", "Rohit", "Kiran", "Sanya", "Aditya", "Priya", "Nikhil", "Meera", "Arjun", "Kavya"]
genders = ["Male", "Female", "Other"]
vaccines = ["COVID-19", "Hepatitis B", "Tetanus", "MMR", "Influenza", "HPV"]
doses = ["1st Dose", "2nd Dose", "Booster", "Annual"]

records = []

for i in range(200):
    abha_id = f"ABHA-{i:04d}"
    name = random.choice(names) + " " + random.choice(["Sharma", "Verma", "Nair", "Khan", "Das"])
    age = np.random.randint(1, 80)
    gender = random.choice(genders)
    
    num_records = random.randint(2, 4)  # multiple vaccine records per person
    used_vaccines = set()

    for _ in range(num_records):
        vaccine = random.choice(vaccines)
        while vaccine in used_vaccines:
            vaccine = random.choice(vaccines)
        used_vaccines.add(vaccine)

        dose = random.choice(doses)

        # 40% past, 30% today, 30% future
        status_choice = random.choices(["past", "today", "future"], weights=[0.4, 0.3, 0.3])[0]
        if status_choice == "past":
            due_date = datetime.date.today() - datetime.timedelta(days=random.randint(10, 400))
        elif status_choice == "today":
            due_date = datetime.date.today()
        else:
            due_date = datetime.date.today() + datetime.timedelta(days=random.randint(1, 180))

        records.append({
            "ABHA_ID": abha_id,
            "Name": name,
            "Age": age,
            "Gender": gender,
            "Vaccine": vaccine,
            "Dose": dose,
            "Due Date": due_date
        })

df = pd.DataFrame(records)
df.to_csv("data/vaccine_records.csv", index=False)
print("✅ Generated", len(df), "records in data/vaccine_records.csv")
