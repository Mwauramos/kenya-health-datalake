import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()


def load_to_csv(df: pd.DataFrame, output_dir: str = "data/processed") -> str:
    """
    Loads transformed data to CSV as the primary storage layer.
    In production, swap or extend with load_to_postgres().
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(output_dir, f"kenya_health_{timestamp}.csv")
    df.to_csv(filepath, index=False)
    print(f"Loaded {len(df)} records to {filepath}")
    return filepath


def load_to_postgres(df: pd.DataFrame, table_name: str = "kenya_health_metrics") -> None:
    """
    Loads transformed data to PostgreSQL.
    Requires DATABASE_URL in .env:
    DATABASE_URL=postgresql://user:password@localhost:5432/health_db
    """
    from sqlalchemy import create_engine

    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL not set in .env")

    engine = create_engine(db_url)
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists="replace",
        index=False,
        method="multi"
    )
    print(f"Loaded {len(df)} records to PostgreSQL table '{table_name}'")


def load_data(df: pd.DataFrame, target: str = "csv") -> str:
    """
    Router: sends data to CSV (default) or PostgreSQL.
    Set target='postgres' to use PostgreSQL.
    """
    if target == "postgres":
        load_to_postgres(df)
        return "postgres"
    else:
        return load_to_csv(df)


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.extract import extract_kenya_health_data
    from src.transform import transform_health_data

    raw = extract_kenya_health_data()
    transformed = transform_health_data(raw)
    path = load_data(transformed)
    print(f"Output: {path}")