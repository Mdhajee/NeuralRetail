import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customers", layout="wide")
st.title("👥 Customer Dashboard")

HERE      = Path(__file__).parent.parent.parent
DATA_PROC = HERE / 'data' / 'processed'

@st.cache_data
def load():
    segments = pd.read_parquet(DATA_PROC / 'segments.parquet')
    churn    = pd.read_parquet(DATA_PROC / 'churn_scores.parquet')
    return segments, churn

segments, churn = load()

# ── Segment KPIs ─────────────────────────────────────
seg_counts = segments['segment'].value_counts()
c1,c2,c3 = st.columns(3)
c1.metric("Total Segmented",  f"{len(segments):,}")
c2.metric("Segments",          f"{segments['segment'].nunique()}")
c3.metric("Champions",
          f"{seg_counts.get('Champions', 0):,}")

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Segment Distribution")
    fig = px.pie(values=seg_counts.values,
                 names=seg_counts.index,
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Avg RFM Score by Segment")
    rfm_avg = (segments.groupby('segment')['RFM_score']
               .mean().sort_values(ascending=False).reset_index())
    fig2 = px.bar(rfm_avg, x='RFM_score', y='segment',
                  orientation='h', color='RFM_score',
                  color_continuous_scale='Blues')
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Churn Risk Distribution")
risk_counts = churn['churn_risk_tier'].value_counts().reset_index()
risk_counts.columns = ['tier','count']
fig3 = px.bar(risk_counts, x='tier', y='count',
              color='tier',
              color_discrete_map={'High risk':'#E84E1B',
                                  'Medium risk':'#F7941D',
                                  'Low risk':'#0F6E56'})
st.plotly_chart(fig3, use_container_width=True)

# Segment filter
st.subheader("Browse Visitors by Segment")
seg_filter = st.selectbox("Select segment", options=sorted(segments['segment'].unique()))
st.dataframe(segments[segments['segment']==seg_filter]
             [['visitorid','recency','view_count',
               'cart_count','RFM_score','segment']]
             .head(50), use_container_width=True)