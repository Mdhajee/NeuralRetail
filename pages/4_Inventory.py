import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Inventory", layout="wide")
st.title("📦 Inventory Dashboard")

DATA_SAMPLE = Path(__file__).parent.parent / "data_sample"

@st.cache_data
def load():
    inv = pd.read_parquet(DATA_SAMPLE / "inventory_optimised.parquet")
    return inv

inv = load()

c1,c2,c3 = st.columns(3)
c1.metric("Total Items",   f"{len(inv):,}")
c2.metric("Class A Items",
          f"{(inv['abc_class']=='A').sum():,}"
          if 'abc_class' in inv.columns else 'N/A')
c3.metric("Avg EOQ",
          f"{inv['eoq'].mean():.0f}"
          if 'eoq' in inv.columns else 'N/A')

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("ABC Classification")
    if 'abc_class' in inv.columns:
        abc = inv['abc_class'].value_counts().reset_index()
        abc.columns = ['class','count']
        st.plotly_chart(
            px.pie(abc,names='class',values='count',
                   color_discrete_sequence=['#185FA5','#F7941D','#E84E1B']),
            use_container_width=True)

with col2:
    st.subheader("EOQ vs Daily Demand")
    if 'eoq' in inv.columns and 'avg_daily_demand' in inv.columns:
        sample = inv.sample(min(200,len(inv)))
        st.plotly_chart(
            px.scatter(sample, x='avg_daily_demand', y='eoq',
                       labels={'avg_daily_demand':'Avg Daily Demand',
                                'eoq':'EOQ'}),
            use_container_width=True)

st.divider()
st.subheader("Inventory Data")
cols = [c for c in ['itemid','avg_daily_demand','eoq',
                     'safety_stock','reorder_point','abc_class']
        if c in inv.columns]
st.dataframe(inv[cols].head(20), use_container_width=True)
