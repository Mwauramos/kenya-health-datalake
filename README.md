# Kenya Health Data Lake

An end-to-end health data pipeline and analytics dashboard built on Kenya county-level health data. Designed to demonstrate production-oriented data engineering practices applied to African public health contexts.

**Live Demo**: https://kenya-health-datalake-hk3ymlytfnf9nmsypsasww.streamlit.app

---

## What This Does

Kenya's health data is fragmented across county reports, MOH bulletins, and surveillance systems. This project builds a structured data lake on top of that data — extracting, validating, transforming, and loading county health indicators into a queryable format — and exposes the results through an interactive analytics dashboard.

The dashboard enables county-level comparison of disease burden, risk classification, and health system indicators across all 47 Kenya counties.

---

## Features

- Automated ETL pipeline orchestrated with Apache Airflow
- Data validation and quality checks at ingestion
- County risk classification based on composite health indicators
- Disease burden scoring across key conditions
- Interactive Streamlit dashboard with county-level filtering and comparison

---

## Tech Stack

- Python
- Apache Airflow (pipeline orchestration)
- pandas (data transformation)
- SQLAlchemy (database layer)
- Streamlit (dashboard)

---

## Project Structure

```
kenya-health-datalake/
├── dags/                  # Airflow DAG definitions
├── pipeline/              # ETL scripts (extract, transform, load)
├── data/                  # Raw and processed data
├── dashboard/             # Streamlit app
└── requirements.txt
```

---

## Running Locally

```bash
git clone https://github.com/Mwauramos/kenya-health-datalake
cd kenya-health-datalake
pip install -r requirements.txt
streamlit run dashboard/app.py
```

---

## Context

This project is part of the ZENIK.AI portfolio — a series of end-to-end healthcare AI and data engineering projects focused on African health systems.

**Author**: Amos Mwaura  
**Contact**: mwauramos.n@gmail.com  
**Portfolio**: https://mwauramos.github.io/zenik-ai
