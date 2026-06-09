import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="NeuralRetail",
    page_icon="🛒",
    layout="wide"
)

# Works both locally and on Streamlit Cloud
DATA_SAMPLE = Path(__file__).parent / "data_sample"

@st.cache_data
def load_data():
    try:
        events    = pd.read_parquet(DATA_SAMPLE / "events_clean.parquet")
        segments  = pd.read_parquet(DATA_SAMPLE / "segments.parquet")
        churn     = pd.read_parquet(DATA_SAMPLE / "churn_scores.parquet")
        inventory = pd.read_parquet(DATA_SAMPLE / "inventory_optimised.parquet")
        forecast  = pd.read_parquet(DATA_SAMPLE / "forecast_output.parquet")
        item_pop  = pd.read_parquet(DATA_SAMPLE / "item_popularity.parquet")
        return events, segments, churn, inventory, forecast, item_pop
    except Exception as e:
        st.error(f"Data loading error: {e}")
        st.stop()

events, segments, churn, inventory, forecast, item_pop = load_data()

st.title("🛒 NeuralRetail — AI Sales Intelligence")
st.markdown("""
**An end-to-end AI-powered retail analytics platform built on RetailRocket clickstream data.**

Use the **sidebar** to navigate between pages:
- 📊 **Sales** — event volume, daily trends, top items
- 👥 **Customers** — RFM segments, churn risk
- 📈 **Forecast** — Prophet demand forecast
- 📦 **Inventory** — EOQ, safety stock, reorder alerts
""")

st.divider()
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Events",    f"{len(events):,}")
c2.metric("Visitors",         f"{events['visitorid'].nunique():,}")
c3.metric("Items",            f"{events['itemid'].nunique():,}")
c4.metric("Segments",         f"{segments['segment'].nunique() if 'segment' in segments.columns else 'N/A'}")

st.caption("⚠ Dashboard showing sample data (1000 rows). Full data runs locally.")