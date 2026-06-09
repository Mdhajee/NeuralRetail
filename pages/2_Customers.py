import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Customers", layout="wide")
st.title("👥 Customer Dashboard")

DATA_SAMPLE = Path(__file__).parent.parent / "data_sample"

@st.cache_data
def load():
    segments = pd.read_parquet(DATA_SAMPLE / "segments.parquet")
    churn    = pd.read_parquet(DATA_SAMPLE / "churn_scores.parquet")
    return segments, churn

segments, churn = load()

seg_counts = segments['segment'].value_counts() if 'segment' in segments.columns else pd.Series()

c1,c2,c3 = st.columns(3)
c1.metric("Total Visitors", f"{len(segments):,}")
c2.metric("Segments",        f"{seg_counts.nunique()}")
c3.metric("High Risk",
          f"{(churn['churn_risk_tier']=='High risk').sum():,}"
          if 'churn_risk_tier' in churn.columns else 'N/A')

st.divider()
col1, col2 = st.columns(2)

with col1:
    st.subheader("Segment Distribution")
    if len(seg_counts) > 0:
        fig = px.pie(values=seg_counts.values, names=seg_counts.index,
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No segment column found in data")

with col2:
    st.subheader("Churn Risk Tiers")
    if 'churn_risk_tier' in churn.columns:
        risk = churn['churn_risk_tier'].value_counts().reset_index()
        risk.columns = ['tier','count']
        fig2 = px.bar(risk, x='tier', y='count', color='tier',
                      color_discrete_map={'High risk':'#E84E1B',
                                          'Medium risk':'#F7941D',
                                          'Low risk':'#0F6E56'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.warning("No churn_risk_tier column found")

st.divider()
st.subheader("Visitor Data")
st.dataframe(segments.head(50), use_container_width=True)
