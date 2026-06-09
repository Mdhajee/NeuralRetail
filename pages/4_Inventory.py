import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Inventory", layout="wide")
st.title("📦 Inventory Dashboard")

HERE      = Path(__file__).parent.parent.parent
DATA_PROC = HERE / 'data' / 'processed'
OUTPUTS   = HERE / 'outputs'

@st.cache_data
def load():
    inv     = pd.read_parquet(DATA_PROC / 'inventory_optimised.parquet')
    reorder = pd.read_csv(OUTPUTS / 'reorder_alerts.csv')
    dead    = pd.read_csv(OUTPUTS / 'dead_stock_risk.csv')
    return inv, reorder, dead

inv, reorder, dead = load()

# KPIs
c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Items",       f"{len(inv):,}")
c2.metric("Class A Items",     f"{(inv['abc_class']=='A').sum():,}")
c3.metric("Reorder Alerts",    f"{len(reorder):,}")
c4.metric("Dead Stock Risk",   f"{len(dead):,}")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("ABC Classification")
    abc_c = inv['abc_class'].value_counts().reset_index()
    abc_c.columns = ['class','count']
    fig = px.pie(abc_c, names='class', values='count',
                 color_discrete_sequence=['#185FA5','#F7941D','#E84E1B'])
    st.plotly_chart(fig, width='stretch')

with col2:
    st.subheader("EOQ vs Daily Demand (Class A)")
    a = inv[inv['abc_class']=='A'].sample(min(500,len(inv[inv['abc_class']=='A'])))
    fig2 = px.scatter(a, x='avg_daily_demand', y='eoq',
                      color='safety_stock', color_continuous_scale='Blues',
                      labels={'avg_daily_demand':'Avg Daily Demand',
                               'eoq':'EOQ'})
    st.plotly_chart(fig2, width='stretch')

st.divider()
st.subheader("🚨 Top Reorder Alerts")
st.dataframe(reorder.head(20), width='stretch')

st.subheader("⚠️ Dead Stock Risk Items")
st.dataframe(dead.head(20), width='stretch')