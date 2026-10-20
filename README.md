# Kenya Health Data Lake and ETL Pipeline

An end-to-end ETL pipeline that extracts, validates, transforms, and loads Kenya county-level health data, with an interactive Streamlit dashboard for epidemiological analysis.

## Features

- Extract: Simulated Kenya county health data (DHIS2-style), ready for live API integration
- Validate: Schema, null, range, and record count checks on raw data
- Transform: Computes malaria rates, cholera rates, maternal mortality ratio, under-5 mortality, ANC coverage, and a composite disease burden score
- Load: CSV output with PostgreSQL support via SQLAlchemy
- Orchestrate: Apache Airflow DAG with four sequential tasks (extract, validate, transform, load)
- Dashboard: Streamlit app with KPI metrics, county risk classification, and CSV download

## Tech Stack

- Python 3.10
- Apache Airflow
- pandas
- Great Expectations
- SQLAlchemy
- psycopg2
- Streamlit

## Setup

```bash
conda create -n health-datalake python=3.10 --copy -y
conda activate health-datalake
pip install -r requirements.txt
```

Create a `.env` file in the root:


## Run the Dashboard

```bash
streamlit run app.py
```

## Project Structure

    kenya-health-datalake/
    ├── app.py
    ├── requirements.txt
    ├── dags/
    │   └── health_etl_dag.py
    └── src/
        ├── extract.py
        ├── transform.py
        ├── load.py
        └── validate.py

## Author

ZENIK.AI | Amos Mwaura  
mwauramos.n@gmailcom
