import streamlit as st
from supabase import create_client, Client
import pandas as pd

from datetime import datetime

st.set_page_config(
    page_title="환자정보등록",
    page_icon="👨‍⚕️",
    layout="wide"
)

@st.cache_resource
def init_connection():
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
    return supabase

supabase = init_connection()

@st.cache_resource(ttl=600)
def run_related_query():
    doctor = supabase.table("doctor").select("*").execute()
    category = supabase.table("diagnosis_1st").select("*").execute()
    diagnosis = supabase.table("diagnosis_2nd").select("*").execute()
    return doctor, category, diagnosis

docs, categories, diagnoses = run_related_query()
df_docs = pd.DataFrame(docs.data)
docs_lst = df_docs['name'].tolist()
docs_lst.insert(0, '<선택>')

df_cats = pd.DataFrame(categories.data)
df_cats_dict = df_cats.set_index('name')['id'].to_dict()

st.title(":blue[환자 정보 등록]")

if 'completed' not in st.session_state:
    st.session_state.completed = False

def calculate_age(birthday):
    today = datetime.today()
    age = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    return age

with st.form(key='personal_info_form'):
    
    c1_1, c1_2= st.columns(2)
    with c1_1:
        patient_name = st.text_input("환자 이름", disabled=st.session_state.completed)
    with c1_2:
        patient_no = st.text_input("환자 등록번호", disabled=st.session_state.completed)
    
    c2_1, c2_2 = st.columns(2)
    with c2_1:
        gender = st.radio("성별", ("남성", "여성"), disabled=st.session_state.completed, horizontal=True)

    with c2_2:
        birthday = st.date_input("생일",
                            value=datetime(2000, 1, 1),
                            min_value=datetime(1924, 1, 1),
                            max_value=datetime.today(), 
                            disabled=st.session_state.completed)
        calculated_age = calculate_age(birthday)

    c3_1, c3_2 = st.columns(2)
    with c3_1:
        doc = st.selectbox("주치의", docs_lst, disabled=st.session_state.completed)
    with c3_2:
        operation_time = st.date_input("수술 예정일",
                             value=datetime.today(), disabled=st.session_state.completed)

    submit_button = st.form_submit_button(label='제출', disabled=st.session_state.completed)
