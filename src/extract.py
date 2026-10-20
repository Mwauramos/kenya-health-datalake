import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def extract_kenya_health_data() -> pd.DataFrame:
    """
    Simulates extraction of Kenya health data from DHIS2-style API.
    In production, replace with actual Kenya DHIS2 or KHIS API endpoint.
    """
    data = {
        "county": [
            "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret",
            "Thika", "Malindi", "Kitale", "Garissa", "Kakamega",
            "Machakos", "Meru", "Nyeri", "Kilifi", "Bungoma"
        ],
        "year": [2023] * 15,
        "quarter": ["Q3"] * 15,
        "malaria_cases": [1200, 3400, 2100, 890, 670, 540, 4200, 320, 5600, 1800,
                          760, 430, 290, 3800, 950],
        "cholera_cases": [45, 120, 67, 23, 12, 8, 180, 5, 340, 56,
                          19, 7, 4, 145, 28],
        "maternal_deaths": [12, 28, 19, 8, 5, 4, 35, 3, 67, 22,
                            7, 4, 2, 31, 11],
        "under5_mortality": [340, 890, 560, 210, 145, 98, 1200, 78, 1800, 450,
                             178, 112, 67, 980, 245],
        "antenatal_visits": [8900, 12000, 9500, 6700, 5200, 4100, 7800, 3200, 2100, 8400,
                             5600, 4800, 3900, 6200, 5100],
        "health_facilities": [234, 156, 189, 145, 112, 89, 134, 67, 45, 178,
                              123, 98, 87, 112, 134],
        "population": [4500000, 1200000, 1100000, 2100000, 800000, 600000, 900000,
                       400000, 500000, 1700000, 1200000, 1500000, 800000, 1200000, 1600000]
    }

    df = pd.DataFrame(data)
    df["extraction_timestamp"] = pd.Timestamp.now()
    print(f"Extracted {len(df)} county health records")
    return df


if __name__ == "__main__":
    df = extract_kenya_health_data()
    print(df.head())
    print(f"Shape: {df.shape}")