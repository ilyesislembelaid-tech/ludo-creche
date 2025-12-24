import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"

st.set_page_config(page_title="Ludo Management Pro", layout="wide", page_icon="🚀")

# --- DESIGN PREMIUM (CSS) ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .main-title {
        font-size: 50px;
        font-weight: bold;
        text-align: center;
        background: -webkit-linear-gradient(#fff, #cbd5e0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px 10px 0px 0px;
        color: white;
        padding: 10px 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p class="main-title">🎨 LUDO PRO</p>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; opacity: 0.8;'>Solution de Gestion Intelligente pour Crèches</p>", unsafe_allow_html=True)

# --- CORPS DE L'APPLI ---
tab1, tab2, tab3 = st.tabs(["💎 Dashboard", "👶 Familles", "💰 Finances"])

with tab1:
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Inscriptions", "42 Enfants", "+4 ce mois")
    with col2:
        st.metric("Alertes Paiement", "12 Relances", "Action requise")
    
    st.write("### Prochaines Échéances")
    st.info("📌 Rappel : Réunion pédagogique ce jeudi à 17h.")

with tab2:
    st.subheader("Base de données interactive")
    data = pd.DataFrame({
        "Enfant": ["Yanis", "Lina", "Adam"],
        "Parent": ["Mme Amraoui", "Mr Belkaid", "Mme Saidi"],
        "Contact": ["213550123456", "213660123456", "213770123456"],
        "Statut": ["Payé", "Retard", "Payé"]
    })
    st.data_editor(data, use_container_width=True)
    if st.button("📤 Envoyer les rappels groupés"):
        st.success("Système prêt pour l'envoi WhatsApp !")

with tab3:
    st.subheader("Bilan Mensuel (DZD)")
    st.write("Visualisation des flux financiers")
    st.progress(70, text="Objectif Revenus (70%)")
    st.metric("Total Net", "340,000 DZD", "Stable")
