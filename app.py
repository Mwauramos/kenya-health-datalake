import streamlit as st
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.extract import extract_kenya_health_data
from src.transform import transform_health_data
from src.validate import run_all_validations

st.set_page_config(
    page_title="ZENIK.AI | Kenya Health Data Lake",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Kenya Health Data Lake and ETL Pipeline")
st.markdown("---")

st.sidebar.header("Pipeline Controls")
run_pipeline = st.sidebar.button("▶ Run ETL Pipeline", type="primary")
show_raw = st.sidebar.checkbox("Show Raw Data", value=False)
show_validation = st.sidebar.checkbox("Show Validation Report", value=True)

if run_pipeline or "df_transformed" not in st.session_state:
    with st.spinner("Running ETL pipeline..."):
        raw_df = extract_kenya_health_data()
        transformed_df = transform_health_data(raw_df)

        os.makedirs("data/processed", exist_ok=True)
        timestamp = pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"data/processed/kenya_health_{timestamp}.csv"
        transformed_df.to_csv(output_path, index=False)

        st.session_state["df_raw"] = raw_df
        st.session_state["df_transformed"] = transformed_df
        st.session_state["output_path"] = output_path

    st.success(f"Pipeline complete. {len(transformed_df)} county records processed.")

df = st.session_state["df_transformed"]
raw = st.session_state["df_raw"]

# KPI row
col1, col2, col3, col4 = st.columns(4)
col1.metric("Counties", len(df))
col2.metric("Total Malaria Cases", f"{df['malaria_cases'].sum():,}")
col3.metric("Avg Disease Burden Score", f"{df['disease_burden_score'].mean():.1f}")
col4.metric("High Risk Counties", len(df[df["risk_category"] == "High"]))

st.markdown("---")

# Risk breakdown
st.subheader("County Risk Classification")
risk_cols = st.columns(3)
for i, risk in enumerate(["High", "Medium", "Low"]):
    subset = df[df["risk_category"] == risk][["county", "disease_burden_score", "malaria_rate_per_100k"]]
    risk_cols[i].markdown(f"**{risk} Risk**")
    risk_cols[i].dataframe(subset.reset_index(drop=True), use_container_width=True)

st.markdown("---")

# Full transformed table
st.subheader("Transformed Health Metrics")
display_cols = [
    "county", "malaria_rate_per_100k", "cholera_rate_per_100k",
    "maternal_mortality_ratio", "under5_mortality_rate",
    "anc_coverage_pct", "facilities_per_100k",
    "disease_burden_score", "risk_category"
]
st.dataframe(df[display_cols].reset_index(drop=True), use_container_width=True)

if show_raw:
    st.subheader("Raw Extracted Data")
    st.dataframe(raw, use_container_width=True)

if show_validation:
    st.subheader("Validation Report")
    results = run_all_validations(df)
    for r in results:
        status = "✅" if r["passed"] else "❌"
        st.write(f"{status} **{r['check']}**")
        if not r["passed"]:
            st.json({k: v for k, v in r.items() if k not in ("check", "passed")})

st.markdown("---")
st.caption("ZENIK.AI | Kenya Health Data Lake | Built with Apache Airflow, Great Expectations, pandas, SQLAlchemy")

# Download button
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download Processed Data (CSV)",
    data=csv_data,
    file_name="kenya_health_metrics.csv",
    mime="text/csv"
)