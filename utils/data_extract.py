import json
import os

DATA_PATH = "data/records.json"

import random

def get_mock_profile(abha_id):
    mock_profiles = {
        "100000000001": {"name": "Ravi Kumar", "age": 45, "gender": "Male"},
        "100000000002": {"name": "Anita Sharma", "age": 31, "gender": "Female"},
        "100000000003": {"name": "Suresh Verma", "age": 52, "gender": "Male"},
        "100000000004": {"name": "Geeta Devi", "age": 60, "gender": "Female"},
        "100000000005": {"name": "Rajesh Mehta", "age": 28, "gender": "Male"},
        "100000000006": {"name": "Preeti Kaur", "age": 35, "gender": "Female"},
        "100000000007": {"name": "Amit Joshi", "age": 41, "gender": "Male"},
        "100000000008": {"name": "Nikita Roy", "age": 22, "gender": "Female"},
        "100000000009": {"name": "Devendra Yadav", "age": 50, "gender": "Male"},
        "100000000010": {"name": "Meena Kumari", "age": 37, "gender": "Female"},
        "100000000011": {"name": "Suraj Thakur", "age": 29, "gender": "Male"},
        "100000000012": {"name": "Sunita Bhatt", "age": 33, "gender": "Female"},
        "100000000013": {"name": "Manish Desai", "age": 40, "gender": "Male"},
        "100000000014": {"name": "Kavita Jain", "age": 48, "gender": "Female"},
        "100000000015": {"name": "Arjun Nair", "age": 36, "gender": "Male"},
        "100000000016": {"name": "Divya Reddy", "age": 27, "gender": "Female"},
        "100000000017": {"name": "Bhavesh Shah", "age": 55, "gender": "Male"},
        "100000000018": {"name": "Ishita Ghosh", "age": 24, "gender": "Female"},
        "100000000019": {"name": "Prakash Patil", "age": 61, "gender": "Male"},
        "100000000020": {"name": "Asha Menon", "age": 38, "gender": "Female"},
        "100000000021": {"name": "Naveen Gupta", "age": 30, "gender": "Male"},
        "100000000022": {"name": "Sneha Kapoor", "age": 26, "gender": "Female"},
        "100000000023": {"name": "Rohit Bansal", "age": 43, "gender": "Male"},
        "100000000024": {"name": "Pooja Shinde", "age": 34, "gender": "Female"},
        "100000000025": {"name": "Dinesh Raut", "age": 39, "gender": "Male"},
        "100000000026": {"name": "Neha Salunkhe", "age": 32, "gender": "Female"},
        "100000000027": {"name": "Harish Malhotra", "age": 58, "gender": "Male"},
        "100000000028": {"name": "Ritika Saxena", "age": 25, "gender": "Female"},
        "100000000029": {"name": "Sanjay Chawla", "age": 44, "gender": "Male"},
        "100000000030": {"name": "Nandita Pillai", "age": 29, "gender": "Female"},
        "100000000031": {"name": "Ashok Rao", "age": 62, "gender": "Male"},
        "100000000032": {"name": "Shreya Nambiar", "age": 23, "gender": "Female"},
        "100000000033": {"name": "Vikram Solanki", "age": 47, "gender": "Male"},
        "100000000034": {"name": "Rupal Sen", "age": 36, "gender": "Female"},
        "100000000035": {"name": "Anil Tiwari", "age": 50, "gender": "Male"},
        "100000000036": {"name": "Komal Bhatia", "age": 40, "gender": "Female"},
        "100000000037": {"name": "Yashwant Khedekar", "age": 53, "gender": "Male"},
        "100000000038": {"name": "Aarti Deshpande", "age": 45, "gender": "Female"},
        "100000000039": {"name": "Gopal Iyer", "age": 59, "gender": "Male"},
        "100000000040": {"name": "Nisha Mahajan", "age": 28, "gender": "Female"},
        "100000000041": {"name": "Karan Arora", "age": 33, "gender": "Male"},
        "100000000042": {"name": "Shruti Dalal", "age": 31, "gender": "Female"},
        "100000000043": {"name": "Rakesh Pandey", "age": 54, "gender": "Male"},
        "100000000044": {"name": "Smita Joshi", "age": 39, "gender": "Female"},
        "100000000045": {"name": "Tarun Goyal", "age": 42, "gender": "Male"},
        "100000000046": {"name": "Vidya Kulkarni", "age": 30, "gender": "Female"},
        "100000000047": {"name": "Naresh Dutt", "age": 37, "gender": "Male"},
        "100000000048": {"name": "Kritika Mishra", "age": 35, "gender": "Female"},
        "100000000049": {"name": "Ajay Rawat", "age": 49, "gender": "Male"},
        "100000000050": {"name": "Anjali Dubey", "age": 27, "gender": "Female"}
    }

    return mock_profiles.get(abha_id, {
        "name": f"Guest User",
        "age": random.randint(20, 70),
        "gender": random.choice(["Male", "Female"])
    })


def save_patient_data(abha_id, data):
    if not os.path.exists("data"):
        os.makedirs("data")

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            db = json.load(f)
    else:
        db = {}

    db[abha_id] = data

    with open(DATA_PATH, "w") as f:
        json.dump(db, f, indent=2)


def get_patient_data(abha_id):
    """
    Load patient data from local records.json using ABHA ID
    """
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            db = json.load(f)
        return db.get(abha_id, None)
    return None
