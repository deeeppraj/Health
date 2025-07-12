def get_mock_ehr(abha_id: str):
    return {
        "clinical_visits": [
            {
                "date": "2025-07-10",
                "doctor": "Dr. Neha Sharma",
                "department": "General Medicine",
                "diagnosis": "Seasonal Flu"
            },
            {
                "date": "2025-06-18",
                "doctor": "Dr. Rajiv Patel",
                "department": "Cardiology",
                "diagnosis": "Mild Hypertension"
            },
            {
                "date": "2025-05-02",
                "doctor": "Dr. Sweta Mehta",
                "department": "ENT",
                "diagnosis": "Sinusitis"
            }
        ],
        "medications": [
            {
                "name": "Paracetamol",
                "dose": "500mg",
                "frequency": "Twice a day",
                "start_date": "2025-07-10",
                "end_date": "2025-07-15"
            },
            {
                "name": "Amlodipine",
                "dose": "5mg",
                "frequency": "Once daily",
                "start_date": "2025-06-18"
            }
        ],
        "lab_tests": [
            {
                "date": "2025-07-10",
                "test": "CBC (Complete Blood Count)",
                "result": "Normal"
            },
            {
                "date": "2025-06-18",
                "test": "Lipid Profile",
                "result": "Borderline High Cholesterol"
            },
            {
                "date": "2025-05-02",
                "test": "Sinus CT Scan",
                "result": "Mucosal thickening in maxillary sinus"
            }
        ],
        "vitals_history": [
            {
                "date": "2025-07-10",
                "bp": "118/78",
                "pulse": 72,
                "temp": 37.1,
                "spo2": 98
            },
            {
                "date": "2025-06-18",
                "bp": "135/88",
                "pulse": 80,
                "temp": 36.9,
                "spo2": 97
            },
            {
                "date": "2025-05-02",
                "bp": "122/80",
                "pulse": 75,
                "temp": 37.0,
                "spo2": 99
            }
        ]
    }
