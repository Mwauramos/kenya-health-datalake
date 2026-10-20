import pandas as pd
import numpy as np


def transform_health_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and transforms raw Kenya health data.
    Adds derived metrics used for epidemiological analysis.
    """
    df = df.copy()

    # Standardize county names
    df["county"] = df["county"].str.strip().str.title()

    # Calculate rates per 100,000 population
    df["malaria_rate_per_100k"] = (df["malaria_cases"] / df["population"] * 100000).round(2)
    df["cholera_rate_per_100k"] = (df["cholera_cases"] / df["population"] * 100000).round(2)
    df["maternal_mortality_ratio"] = (df["maternal_deaths"] / df["antenatal_visits"] * 100000).round(2)
    df["under5_mortality_rate"] = (df["under5_mortality"] / df["population"] * 1000).round(2)

    # Facility density
    df["facilities_per_100k"] = (df["health_facilities"] / df["population"] * 100000).round(2)

    # ANC coverage proxy (antenatal visits per expected births, ~3% birth rate)
    df["expected_births"] = (df["population"] * 0.03).astype(int)
    df["anc_coverage_pct"] = (df["antenatal_visits"] / df["expected_births"] * 100).round(1)
    df["anc_coverage_pct"] = df["anc_coverage_pct"].clip(upper=100)

    # Disease burden score (composite index 0-100)
    malaria_norm = df["malaria_rate_per_100k"] / df["malaria_rate_per_100k"].max()
    cholera_norm = df["cholera_rate_per_100k"] / df["cholera_rate_per_100k"].max()
    maternal_norm = df["maternal_mortality_ratio"] / df["maternal_mortality_ratio"].max()
    df["disease_burden_score"] = ((malaria_norm + cholera_norm + maternal_norm) / 3 * 100).round(1)

    # Risk classification
    def classify_risk(score):
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        else:
            return "Low"

    df["risk_category"] = df["disease_burden_score"].apply(classify_risk)

    # Add transformation timestamp
    df["transformed_at"] = pd.Timestamp.now()

    print(f"Transformed {len(df)} records. Risk breakdown:")
    print(df["risk_category"].value_counts().to_string())
    return df


if __name__ == "__main__":
    from extract import extract_kenya_health_data
    raw = extract_kenya_health_data()
    transformed = transform_health_data(raw)
    print(transformed[["county", "malaria_rate_per_100k", "disease_burden_score", "risk_category"]])