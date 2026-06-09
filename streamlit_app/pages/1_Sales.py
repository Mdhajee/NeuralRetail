import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import os

# ── Page config ───────────────────────────────────────
st.set_page_config(
    page_title="NeuralRetail",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Find project root ─────────────────────────────────
HERE = Path(__file__).parent.parent   # streamlit_app/ → NeuralRetail/
DATA_PROC = HERE / 'data' / 'processed'
OUTPUTS   = HERE / 'outputs'

# ── Shared data loader (cached — loads once) ──────────
@st.cache_data
def load_all_data():
    events      = pd.read_parquet(DATA_PROC / 'events_clean.parquet')
    segments    = pd.read_parquet(DATA_PROC / 'segments.parquet')
    churn       = pd.read_parquet(DATA_PROC / 'churn_scores.parquet')
    inventory   = pd.read_parquet(DATA_PROC / 'inventory_optimised.parquet')
    forecast    = pd.read_parquet(DATA_PROC / 'forecast_output.parquet')
    item_pop    = pd.read_parquet(DATA_PROC / 'item_popularity.parquet')
    return events, segments, churn, inventory, forecast, item_pop

# ── Landing page ──────────────────────────────────────
st.title("🛒 NeuralRetail — AI Sales Intelligence")
st.markdown("""
**An end-to-end AI-powered retail analytics platform built on RetailRocket clickstream data.**

Navigate using the sidebar to explore:
- 📊 **Sales Dashboard** — event volume, daily trends, top items
- 👥 **Customer Dashboard** — RFM segments, churn risk scores
- 📈 **Forecast Dashboard** — Prophet demand forecasts
- 📦 **Inventory Dashboard** — EOQ, safety stock, reorder alerts
""")

st.divider()

# KPI summary on landing page
events, segments, churn, inventory, forecast, item_pop = load_all_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Events",      f"{len(events):,}")
col2.metric("Unique Visitors",   f"{events['visitorid'].nunique():,}")
col3.metric("Unique Items",      f"{events['itemid'].nunique():,}")
col4.metric("Segments",          f"{segments['segment'].nunique()}")

st.divider()
st.caption("NeuralRetail · Amdox Technologies · 2026")