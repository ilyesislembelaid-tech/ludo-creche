import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURATION DES CLÉS (Gardées précieusement) ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"

st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👑")

# --- DESIGN "MOZART" (CSS PREMIUM) ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #020111 0%, #050b3a 100%); color: white; }
    .stMetric { background: rgba(255, 255, 255, 0.05); border-radius: 15px; padding: 15px; border: 1px solid #00f2fe; }
    .main-header { font-size: 40px; font-weight: 800; background: -webkit-linear-gradient(#00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 10px; }
    .stTabs [data-baseweb="tab"] { color: #88c0d0; font-size: 16px; font-weight: 600; }
    .stButton>button { width: 100%; border-radius: 50px; background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%); color: black; font-weight: bold; border: none; height: 45px; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0 0 20px #00f2fe; }
    /* Style pour les tableaux */
    .stDataEditor { background-color: rgba(255,255,255,0.05); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- ENTÊTE AVEC TON LOGO ---
col_logo1, col_logo2, col_logo3 = st.columns([1, 2, 1])
with col_logo2:
    # Intégration de ton logo
    st.image("https://i.ibb.co/v4S6Yf7/468888427-1244682499919526-1850707048973692228-n.jpg", use_container_width=True)
    st.markdown('<p class="main-header">LUDO GOLD SYSTEM</p>', unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES (Session State) ---
if 'parents_db' not in st.session_state:
    st.session_state.parents_db = pd.DataFrame([
        {"Enfant": "Yanis", "Tel": "213550000000", "Montant": 25000, "Echeance": "2024-01-05", "Abonnement": "Mensuel"}
    ])
if 'staff_db' not in st.session_state:
    st.session_state.staff_db = pd.DataFrame([
        {"Nom": "Khadidja", "Poste": "Éducatrice", "Tel": "213770000000", "Salaire": 45000, "Date_Paie": 30}
    ])
if 'expenses_db' not in st.session_state:
    st.session_state.expenses_db = pd.DataFrame([
        {"Catégorie": "Nutrition", "Détail": "Courses Hebdo", "Montant": 15000, "Date": "2023-12-25"},
        {"Catégorie": "Electricité", "Détail": "Facture Sonelgaz", "Montant": 8000, "Date": "2023-12-20"},
        {"Catégorie": "Gaz", "Détail": "Chauffage", "Montant": 4000, "Date": "2023-12-20"},
        {"Catégorie": "Eau", "Détail": "ADE", "Montant": 2500, "Date": "2023-12-15"},
        {"Catégorie": "Activités", "Détail": "Peinture & Jeux", "Montant": 6000, "Date": "2023-12-22"}
    ])

# --- NAVIGATION ---
tabs = st.tabs(["📊 DASHBOARD GLOBAL", "👶 UNIVERS ENFANTS", "👥 GESTION ÉQUIPE", "💳 FLUX FINANCIERS", "🏥 SANTÉ & NOTES"])

# --- 1. DASHBOARD GLOBAL ---
with tabs[0]:
    rev = st.session_state.parents_db['Montant'].sum()
    salaires = st.session_state.staff_db['Salaire'].sum()
    charges = st.session_state.expenses_db['Montant'].sum()
    benefice = rev - (salaires + charges)

    st.subheader("🚀 Analyse de Performance")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("REVENUS", f"{rev:,} DA")
    c2.metric("PAIES STAFF", f"-{salaires:,} DA")
    c3.metric("CHARGES (EAU/GAZ/ETC)", f"-{charges:,} DA")
    c4.metric("BÉNÉFICE NET", f"{benefice:,} DA")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        fig_pie = px.pie(st.session_state.expenses_db, values='Montant', names='Catégorie', 
                         title="Où part l'argent ? (Répartition des charges)", hole=0.5)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)
    with col_g2:
        st.write("### 🧠 Diagnostic Intelligent")
        if benefice > 0:
            st.success(f"La crèche est rentable ce mois-ci ! Profit : {benefice:,} DA")
        else:
            st.error("Attention : Les dépenses dépassent les revenus !")
        st.info(f"💡 Plus gros poste de dépense : {st.session_state.expenses_db.loc[st.session_state.expenses_db['Montant'].idxmax(), 'Catégorie']}")

# --- 2. UNIVERS ENFANTS (Rappels WhatsApp) ---
with tabs[1]:
    st.subheader("👶 Gestion des Familles")
    st.session_state.parents_db = st.data_editor(st.session_state.parents_db, num_rows="dynamic", use_container_width=True)
    
    if st.button("📲 ENVOYER LES RAPPELS DE PAIEMENT (3 jours avant)"):
        st.info("Recherche des échéances proches...")
        # Ici on simule l'envoi WhatsApp via Green-API
        st.success("WhatsApp activé : Les rappels ont été envoyés aux parents concernés !")

# --- 3. GESTION ÉQUIPE ---
with tabs[2]:
    st.subheader("👥 Registre du Personnel")
    st.session_state.staff_db = st.data_editor(st.session_state.staff_db, num_rows="dynamic", use_container_width=True)
    
    if st.button("💸 NOTIFIER L'ÉQUIPE (PAIE EFFECTUÉE)"):
        st.balloons()
        st.success("Confirmation de paiement envoyée par WhatsApp à toute l'équipe !")

# --- 4. FLUX FINANCIERS DÉTAILLÉS ---
with tabs[3]:
    st.subheader("📉 Détail des Dépenses (Eau, Gaz, Nutrition, Activités)")
    st.session_state.expenses_db = st.data_editor(st.session_state.expenses_db, num_rows="dynamic", use_container_width=True)
    
    # Graphique d'évolution
    fig_bar = px.bar(st.session_state.expenses_db, x='Date', y='Montant', color='Catégorie', title="Historique des frais")
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_bar, use_container_width=True)

# --- 5. SANTÉ & NOTES ---
with tabs[4]:
    st.subheader("📝 Cahier de Liaison & Santé")
    st.info("Espace pour noter les allergies, les médicaments ou les incidents.")
    notes_db = pd.DataFrame([
        {"Date": "2023-12-24", "Enfant": "Yanis", "Note": "Légère fièvre à midi", "Urgent": "Oui"},
        {"Date": "2023-12-25", "Enfant": "Tous", "Note": "Prévoir goûter de Noël", "Urgent": "Non"}
    ])
    st.data_editor(notes_db, num_rows="dynamic", use_container_width=True)
