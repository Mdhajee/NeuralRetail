import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Forecast", layout="wide")
st.title("📈 Forecast Dashboard")

HERE      = Path(__file__).parent.parent.parent
DATA_PROC = HERE / 'data' / 'processed'

@st.cache_data
def load():
    forecast     = pd.read_parquet(DATA_PROC / 'forecast_output.parquet')
    daily_demand = pd.read_parquet(DATA_PROC / 'daily_demand.parquet')
    lb           = pd.read_csv(HERE / 'outputs' / 'forecast_leaderboard.csv')
    return forecast, daily_demand, lb

forecast, daily_demand, lb = load()

forecast['ds']          = pd.to_datetime(forecast['ds'])
daily_demand['date']   = pd.to_datetime(daily_demand['date'])

# Show leaderboard
st.subheader("📋 Forecast MAPE Leaderboard")
st.dataframe(lb, width='stretch')

st.divider()
st.subheader("Demand Forecast Chart")

# Get best product column name
prod_col = 'StockCode' if 'StockCode' in forecast.columns else 'itemid'
best_prod = forecast[prod_col].iloc[0]
st.caption(f"Showing forecast for product: {best_prod}")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=forecast['ds'], y=forecast['yhat'],
    name='Forecast', line=dict(color='#E84E1B', width=2)))
fig.add_trace(go.Scatter(
    x=pd.concat([forecast['ds'], forecast['ds'][::-1]]),
    y=pd.concat([forecast['yhat_upper'], forecast['yhat_lower'][::-1]]),
    fill='toself', fillcolor='rgba(232,78,27,0.15)',
    line=dict(color='rgba(255,255,255,0)'), name='90% CI'))
fig.update_layout(title=f'Prophet Forecast — {best_prod}',
                  xaxis_title='Date', yaxis_title='Demand')
st.plotly_chart(fig, width='stretch')