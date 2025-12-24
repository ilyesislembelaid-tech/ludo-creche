import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"

st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- DESIGN ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    .main-header { font-size: 38px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITRE (SECTION CORRIGÉE) ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # Ce lien est testé et fonctionne en direct
    st.image("https://i.ibb.co/v4S6Yf7/468888427-1244682499919526-1850707048973692228-n.jpg", use_container_width=True)
    st.markdown('<p class="main-header">LUDO GOLD SYSTEM</p>', unsafe_allow_html=True)

# --- LE RESTE DU CODE (DASHBOARD) ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([{"Enfant": "Exemple", "Tel": "213", "Montant": 25000}])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([{"Catégorie": "Nutrition", "Montant": 15000}, {"Catégorie": "Gaz/EAU", "Montant": 5000}])

t1, t2, t3 = st.tabs(["📊 DASHBOARD", "👶 PARENTS", "📉 DÉPENSES"])

with t1:
    rev = st.session_state.parents_db['Montant'].sum()
    exp = st.session_state.expenses_db['Montant'].sum()
    st.columns(3)[0].metric("REVENUS", f"{rev:,} DA")
    st.columns(3)[1].metric("CHARGES", f"{exp:,} DA")
    st.columns(3)[2].metric("NET", f"{rev-exp:,} DA")
    fig = px.pie(st.session_state.expenses_db, values='Montant', names='Catégorie', hole=0.4)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.session_state.parents_db = st.data_editor(st.session_state.parents_db, num_rows="dynamic", use_container_width=True)

with t3:
    st.session_state.expenses_db = st.data_editor(st.session_state.expenses_db, num_rows="dynamic", use_container_width=True)
