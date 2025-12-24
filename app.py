import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- 2. DESIGN ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    .main-header { font-size: 32px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-top: -20px; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGO ET TITRE ---
logo_url = "https://i.ibb.co/svzNSJTR/468888427-1244682499919526-1850707048973692228-n.jpg"

col_a, col_b, col_c = st.columns([2, 1, 2])
with col_b:
    st.image(logo_url, width=120) # Logo encore plus petit pour être sûr
    st.markdown('<p class="main-header">LUDO GOLD</p>', unsafe_allow_html=True)

# --- 4. BASES DE DONNÉES ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([{"Enfant": "Exemple", "Tel": "213", "Montant": 25000, "Statut": "Payé"}])
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = pd.DataFrame([{"Nom": "Employé 1", "Poste": "Educatrice", "Salaire": 45000}])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([{"Catégorie": "Nutrition", "Montant": 15000}, {"Catégorie": "Loyer", "Montant": 50000}])

# --- 5. ONGLETS ---
t1, t2, t3, t4 = st.tabs(["📊 DASHBOARD", "👶 PARENTS", "👥 ÉQUIPE", "💰 DÉPENSES"])

with t1:
    rev = st.session_state.parents_db['Montant'].sum()
    sal = st.session_state.staff_db['Salaire'].sum()
    exp = st.session_state.expenses_db['Montant'].sum()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("REVENUS", f"{rev:,} DA")
    c2.metric("CHARGES", f"{sal+exp:,} DA")
    c3.metric("BÉNÉFICE NET", f"{rev-sal-exp:,} DA")
    
    fig = px.pie(st.session_state.expenses_db, values='Montant', names='Catégorie', hole=0.5)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with t2:
    st.subheader("Fiches Parents")
    st.session_state.parents_db = st.data_editor(st.session_state.parents_db, num_rows="dynamic", key="p_edit")
    st.button("📲 Envoyer Rappels")

with t3:
    st.subheader("Fiches Personnel")
    st.session_state.staff_db = st.data_editor(st.session_state.staff_db, num_rows="dynamic", key="s_edit")

with t4:
    st.subheader("Registre des Dépenses")
    st.session_state.expenses_db = st.data_editor(st.session_state.expenses_db, num_rows="dynamic", key="e_edit")
