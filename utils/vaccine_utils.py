import pandas as pd
from datetime import datetime

def get_status(due_date):
    today = pd.to_datetime(datetime.today().date())
    if pd.isna(due_date):
        return "Unknown"
    elif due_date > today:
        return "Pending"
    elif due_date == today:
        return "Due Today"
    else:
        return "Overdue"

def load_vaccine_data(path=r"data/vaccine_records.csv"):
    df = pd.read_csv(path, parse_dates=["Due Date"])
    df.columns = df.columns.str.strip()
    df["Status"] = df["Due Date"].apply(get_status)
    return df

def get_patient_vaccine_status(abha_id, df):
    abha_id = abha_id.strip().upper()
    return df[df["ABHA_ID"].str.upper() == abha_id]
