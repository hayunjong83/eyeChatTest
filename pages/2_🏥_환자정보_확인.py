import streamlit as st
from supabase import create_client, Client
import pandas as pd

from datetime import datetime

st.set_page_config(
    page_title="환자정보확인",
    page_icon=":hospital:",
    layout="wide"
)

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase

supabase = init_connection()

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_resource(ttl=600)
def run_query():
    return supabase.table("patient").select("*").execute()

rows = run_query()

df = pd.DataFrame(rows.data)
df.set_index("id", inplace=True)
df['patientNo'] = df['patientNo'].astype("str")

df['operation_time'] = pd.to_datetime(df['operation_time']).dt.strftime('%y%m%d %H:%M')
df['birth'] = pd.to_datetime(df['birth'])
df['age'] = df['birth'].apply(lambda x: datetime.now().year - x.year - ((datetime.now().month, datetime.now().day) < (x.month, x.day)))
df['gender'] = df['gender'].apply(lambda x: 'M' if x else 'W')
df['eye'] = df['eye'].map({0: '우안', 1: '좌안', 2: '양안'})

st.markdown(
    """
    ## 환자 정보 확인
"""
)
st.dataframe(df)