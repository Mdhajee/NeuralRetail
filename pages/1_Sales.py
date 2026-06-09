import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Sales", layout="wide")
st.title("📊 Sales Dashboard")

DATA_SAMPLE = Path(__file__).parent.parent / "data_sample"

@st.cache_data
def load():
    events   = pd.read_parquet(DATA_SAMPLE / "events_clean.parquet")
    item_pop = pd.read_parquet(DATA_SAMPLE / "item_popularity.parquet")
    return events, item_pop

events, item_pop = load()

views     = events[events['event']=='view']
carts     = events[events['event']=='addtocart']
purchases = events[events['event']=='transaction']

c1,c2,c3,c4 = st.columns(4)
c1.metric("Total Views",    f"{len(views):,}")
c2.metric("Cart Additions", f"{len(carts):,}")
c3.metric("Purchases",      f"{len(purchases):,}")
c4.metric("Conversion",     f"{len(purchases)/max(len(views),1)*100:.2f}%")

st.divider()
st.subheader("Daily Event Volume")
daily = events.groupby(['date','event']).size().reset_index(name='count')
daily['date'] = pd.to_datetime(daily['date'])
fig = px.line(daily, x='date', y='count', color='event',
              color_discrete_map={'view':'#185FA5',
                                  'addtocart':'#F7941D',
                                  'transaction':'#0F6E56'})
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    st.subheader("Conversion Funnel")
    funnel = pd.DataFrame({'Stage':['Views','Carts','Purchases'],
                           'Count':[len(views),len(carts),len(purchases)]})
    st.plotly_chart(px.funnel(funnel,x='Count',y='Stage'),
                   use_container_width=True)
with col2:
    st.subheader("Top 10 Items")
    top10 = item_pop.nlargest(10,'total_events')
    fig2  = px.bar(top10,x='total_events',
                   y=top10['itemid'].astype(str),orientation='h')
    fig2.update_layout(yaxis=dict(autorange='reversed'))
    st.plotly_chart(fig2, use_container_width=True)
