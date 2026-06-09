import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

st.set_page_config(page_title="Forecast", layout="wide")
st.title("📈 Forecast Dashboard")

DATA_SAMPLE = Path(__file__).parent.parent / "data_sample"

@st.cache_data
def load():
    fc = pd.read_parquet(DATA_SAMPLE / "forecast_output.parquet")
    fc['ds'] = pd.to_datetime(fc['ds'])
    return fc

fc = load()
prod_col  = 'StockCode' if 'StockCode' in fc.columns else 'itemid'
best_prod = fc[prod_col].iloc[0] if prod_col in fc.columns else 'Unknown'

c1,c2 = st.columns(2)
c1.metric("Forecast Days", f"{len(fc):,}")
c2.metric("Product",       f"{best_prod}")

st.divider()
st.subheader(f"Prophet Forecast — {best_prod}")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=fc['ds'], y=np.maximum(fc['yhat'].values,0),
    name='Forecast', line=dict(color='#E84E1B',width=2)))
fig.add_trace(go.Scatter(
    x=pd.concat([fc['ds'], fc['ds'][::-1]]),
    y=pd.concat([np.maximum(fc['yhat_upper'],0),
                 np.maximum(fc['yhat_lower'][::-1],0)]),
    fill='toself', fillcolor='rgba(232,78,27,0.15)',
    line=dict(color='rgba(0,0,0,0)'), name='90% CI'))
fig.update_layout(xaxis_title='Date', yaxis_title='Demand')
st.plotly_chart(fig, use_container_width=True)
st.dataframe(fc.tail(10), use_container_width=True)
