from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.extract import extract_kenya_health_data
from src.transform import transform_health_data
from src.load import load_data
from src.validate import run_all_validations

default_args = {
    "owner": "zenik-ai",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def extract_task(**context):
    df = extract_kenya_health_data()
    filepath = "data/raw/kenya_health_raw.csv"
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(filepath, index=False)
    context["ti"].xcom_push(key="raw_filepath", value=filepath)
    print(f"Extract complete: {len(df)} records saved to {filepath}")


def validate_raw_task(**context):
    import pandas as pd
    filepath = context["ti"].xcom_pull(key="raw_filepath", task_ids="extract")
    df = pd.read_csv(filepath)
    results = run_all_validations(df)
    failed = [r for r in results if not r["passed"]]
    if failed:
        raise ValueError(f"Raw data validation failed: {failed}")
    print("Raw data validation passed.")


def transform_task(**context):
    import pandas as pd
    filepath = context["ti"].xcom_pull(key="raw_filepath", task_ids="extract")
    df = pd.read_csv(filepath)
    transformed = transform_health_data(df)
    transformed_path = "data/processed/kenya_health_transformed.csv"
    os.makedirs("data/processed", exist_ok=True)
    transformed.to_csv(transformed_path, index=False)
    context["ti"].xcom_push(key="transformed_filepath", value=transformed_path)
    print(f"Transform complete: {len(transformed)} records saved to {transformed_path}")


def load_task(**context):
    import pandas as pd
    filepath = context["ti"].xcom_pull(key="transformed_filepath", task_ids="transform")
    df = pd.read_csv(filepath)
    output = load_data(df, target="csv")
    print(f"Load complete: {output}")


with DAG(
    dag_id="kenya_health_etl",
    default_args=default_args,
    description="Kenya Health Data Lake ETL Pipeline",
    schedule_interval="@weekly",
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["kenya", "health", "etl", "zenik-ai"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_task,
    )

    validate_raw = PythonOperator(
        task_id="validate_raw",
        python_callable=validate_raw_task,
    )

    transform = PythonOperator(
        task_id="transform",
        python_callable=transform_task,
    )

    load = PythonOperator(
        task_id="load",
        python_callable=load_task,
    )

    extract >> validate_raw >> transform >> load