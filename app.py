import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# --- CONFIGURATION ---
st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- DESIGN "MOZART" (CSS PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 15px; border: 1px solid #00f2fe; }
    .main-header { font-size: 40px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-top: -30px; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { color: #88c0d0; font-size: 16px; font-weight: 600; }
    .stButton>button { width: 100%; border-radius: 50px; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: black; font-weight: bold; border: none; height: 45px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 20px #00f2fe; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO & TITRE ---
# Utilisation du lien direct qui fonctionne
logo_url = "https://i.ibb.co/svzNSJTR/468888427-1244682499919526-1850707048973692228-n.jpg"

col1, col2, col3 = st.columns([1, 1.5, 1])
with col2:
    st.image(logo_url, use_container_width=True)
    st.markdown('<p class="main-header">LUDO GOLD SYSTEM</p>', unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([
        {"Enfant": "Exemple", "Tel": "213", "Montant": 25000, "Abonnement": "Mensuel", "Echeance": "2024-01-01"}
    ])
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = pd.DataFrame([
        {"Nom": "Khadidja", "Poste": "Directrice", "Salaire": 55000, "Tel": "213"}
    ])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([
        {"Catégorie": "Nutrition", "Montant": 15000},
        {"Catégorie": "Électricité", "Montant": 8000},
        {"Catégorie": "Gaz", "Montant": 4000},
        {"Catégorie": "Eau", "Montant": 2500},
        {"Catégorie": "Activités", "Montant": 6000}
    ])

# --- NAVIGATION ---
tabs = st.tabs(["📊 DASHBOARD", "👶 PARENTS", "👥 ÉQUIPE", "📉 CHARGES DÉTAILLÉES"])

# --- DASHBOARD ---
with tabs[0]:
    rev = st.session_state.parents_db['Montant'].sum()
    salaires = st.session_state.staff_db['Salaire'].sum()
    charges = st.session_state.expenses_db['Montant'].sum()
    benefice = rev - (salaires + charges)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("REVENUS BRUTS", f"{rev:,} DA")
    c2.metric("PAIES STAFF", f"-{salaires:,} DA")
    c3.metric("FRAIS GÉNÉRAUX", f"-{charges:,} DA")
