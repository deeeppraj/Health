import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

abha_ids = [f"ABHA-{i:04d}" for i in range(1, 301)]
dates = pd.date_range(end=datetime.today(), periods=10).tolist()
records = []

for abha in abha_ids:
    for _ in range(random.randint(2, 5)):
        date = random.choice(dates)
        prediction = random.choice(['Benign', 'Malignant'])
        confidence = round(np.random.uniform(0.85, 0.99), 2)
        records.append([abha, date.strftime('%Y-%m-%d'), prediction, confidence])

df = pd.DataFrame(records, columns=["ABHA_ID", "Date", "Prediction", "Confidence"])
df.to_csv("data/breast_cancer_history.csv", index=False)
print("✅ breast_cancer_history.csv generated")
