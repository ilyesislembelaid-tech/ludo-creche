import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURATION ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"

st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- DESIGN LUXE ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; font-weight: bold; }
    .main-header { font-size: 35px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 20px; }
    .stButton>button { width: 100%; border-radius: 50px; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: black; font-weight: bold; border: none; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 15px #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITRE ---
col_l1, col_l2, col_l3 = st.columns([1, 1, 1])
with col_l2:
    # Utilisation d'un lien plus stable pour ton logo
    st.image("https://raw.githubusercontent.com/ilyesislembelaid-tech/ludo-creche/main/laludo.jpg", width=200)
    st.markdown('<p class="main-header">LUDO GOLD SYSTEM</p>', unsafe_allow_html=True)

# --- INITIALISATION ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([{"Enfant": "Yanis", "Tel": "213550000000", "Montant": 25000, "Statut": "Payé"}])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([
        {"Catégorie": "Nutrition", "Montant": 15000},
        {"Catégorie": "Électricité", "Montant": 8000},
        {"Catégorie": "Gaz", "Montant": 4000},
        {"Catégorie": "Eau", "Montant": 2500},
        {"Catégorie": "Activités", "Montant": 6000}
    ])

# --- ONGLETS ---
t1, t2, t3, t4 = st.tabs(["📊 DASHBOARD", "👶 FAMILLES", "👥 ÉQUIPE", "📉 DÉPENSES"])

with t1:
    rev = st.session_state.parents_db['Montant'].sum()
    exp = st.session_state.expenses_db['Montant'].sum()
    c1, c2, c3 = st.columns(3)
    c1.metric("REVENUS", f"{rev:,} DA")
    c2.metric("CHARGES", f"{exp:,} DA")
    c3.metric("BÉNÉFICE", f"{rev-exp:,} DA")

    fig = px.pie(st.session_state.expenses_db, values='Montant', names='Catégorie', hole=0.4, title="Analyse des Charges")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white", showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.session_state.parents_db = st.data_editor(st.session_state.parents_db, num_rows="dynamic", use_container_width=True)
    st.button("📲 Envoyer Rappels WhatsApp")

with t3:
    staff = pd.DataFrame([{"Nom": "Khadidja", "Poste": "Directrice", "Salaire": 55000}])
    st.data_editor(staff, num_rows="dynamic", use_container_width=True)
    st.button("💰 Confirmer les Salaires")

with t4:
    st.session_state.expenses_db = st.data_editor(st.session_state.expenses_db, num_rows="dynamic", use_container_width=True)
