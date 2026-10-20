import pandas as pd
from typing import Dict, List


def validate_schema(df: pd.DataFrame) -> Dict:
    """Checks all required columns are present."""
    required_columns = [
        "county", "year", "quarter", "malaria_cases", "cholera_cases",
        "maternal_deaths", "under5_mortality", "antenatal_visits",
        "health_facilities", "population"
    ]
    missing = [col for col in required_columns if col not in df.columns]
    return {
        "check": "schema",
        "passed": len(missing) == 0,
        "missing_columns": missing
    }


def validate_no_nulls(df: pd.DataFrame) -> Dict:
    """Checks for null values in critical columns."""
    critical_cols = ["county", "population", "malaria_cases", "cholera_cases"]
    null_counts = {col: int(df[col].isnull().sum()) for col in critical_cols if col in df.columns}
    total_nulls = sum(null_counts.values())
    return {
        "check": "no_nulls",
        "passed": total_nulls == 0,
        "null_counts": null_counts
    }


def validate_positive_values(df: pd.DataFrame) -> Dict:
    """Checks numeric health metrics are non-negative."""
    numeric_cols = ["malaria_cases", "cholera_cases", "maternal_deaths",
                    "under5_mortality", "antenatal_visits", "health_facilities", "population"]
    violations = {}
    for col in numeric_cols:
        if col in df.columns:
            neg_count = int((df[col] < 0).sum())
            if neg_count > 0:
                violations[col] = neg_count
    return {
        "check": "positive_values",
        "passed": len(violations) == 0,
        "violations": violations
    }


def validate_population_range(df: pd.DataFrame) -> Dict:
    """Checks county populations are within realistic Kenya bounds."""
    if "population" not in df.columns:
        return {"check": "population_range", "passed": False, "error": "population column missing"}
    min_pop = 200000
    max_pop = 6000000
    out_of_range = df[(df["population"] < min_pop) | (df["population"] > max_pop)]["county"].tolist()
    return {
        "check": "population_range",
        "passed": len(out_of_range) == 0,
        "out_of_range_counties": out_of_range
    }


def validate_county_count(df: pd.DataFrame, expected: int = 15) -> Dict:
    """Checks expected number of county records are present."""
    actual = len(df)
    return {
        "check": "county_count",
        "passed": actual >= expected,
        "expected": expected,
        "actual": actual
    }


def run_all_validations(df: pd.DataFrame) -> List[Dict]:
    """Runs all validation checks and prints a summary report."""
    checks = [
        validate_schema(df),
        validate_no_nulls(df),
        validate_positive_values(df),
        validate_population_range(df),
        validate_county_count(df)
    ]

    print("\n=== DATA VALIDATION REPORT ===")
    all_passed = True
    for check in checks:
        status = "PASS" if check["passed"] else "FAIL"
        if not check["passed"]:
            all_passed = False
        print(f"[{status}] {check['check']}")
        if not check["passed"]:
            for k, v in check.items():
                if k not in ("check", "passed"):
                    print(f"       {k}: {v}")

    print(f"\nOverall: {'ALL CHECKS PASSED' if all_passed else 'VALIDATION FAILED'}")
    print("==============================\n")
    return checks


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.extract import extract_kenya_health_data
    from src.transform import transform_health_data

    raw = extract_kenya_health_data()
    transformed = transform_health_data(raw)
    run_all_validations(transformed)