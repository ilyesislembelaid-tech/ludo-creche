import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION SÉCURISÉE ---
# Le code essaie de lire les secrets Streamlit, sinon il utilise tes clés par défaut
try:
    ID_INSTANCE = st.secrets["ID_INSTANCE"]
    API_TOKEN = st.secrets["API_TOKEN"]
except:
    ID_INSTANCE = "1101961689"
    API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"

st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- DESIGN PREMIUM ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    .main-header { font-size: 32px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-top: -20px; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; font-size: 24px; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 255, 255, 0.05); border-radius: 15px; }
    .stDataEditor { background-color: white; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER (LOGO PETIT) ---
logo_url = "https://i.ibb.co/svzNSJTR/468888427-1244682499919526-1850707048973692228-n.jpg"

col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    st.image(logo_url, width=150) # Ici le logo est mis en petit
    st.markdown('<p class="main-header">LUDO GOLD</p>', unsafe_allow_html=True)

# --- DONNÉES PAR DÉFAUT ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([{"Enfant": "Yanis", "Tel": "213550000000", "Montant": 25000, "Echeance": "2024-01-05"}])
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = pd.DataFrame([{"Nom": "Khadidja", "Poste": "Educatrice", "Salaire": 45000}])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([
        {"Catégorie": "Nutrition", "Montant": 15000},
        {"Catégorie": "Gaz/Electricité/Eau", "Montant": 12000},
        {"Catégorie": "Activités", "Montant": 5000}
    ])

# --- NAVIGATION ---
t1, t2, t3, t4 = st.tabs(["📊 DASHBOARD", "👶 PARENTS", "👥 ÉQUIPE", "💰 DÉPENSES"])

with t1:
    rev = st.session_state.parents_db['Montant'].sum()
    sal = st.session_state.staff_db['Salaire'].sum()
    exp = st.session_state.expenses_db['Montant'].sum()
    net = rev - sal - exp
    
    c1, c2, c3 = st.columns(3)
    c1.metric("REVENUS", f"{rev:,} DA")
    c2.metric("CHARGES TOTALES", f"{sal+exp:,} DA")
    c3.metric("BÉNÉFICE NET", f"{net:,} DA")
    
    fig = px.pie(st.session_state.expenses_db, values='Montant', names='Catégorie', hole=0.5, title="Répartition des Charges")
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.subheader("Paiements Parents")
    st.session_state.parents_db = st.data_editor(st.session_state
