import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import requests
import plotly.express as px

# --- CONFIGURATION ---
GOOGLE_AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"
GREEN_API_ID = "41e4cb90444f42a8"
GREEN_API_TOKEN = "b2ef21886432f2286ad973eefb1e45f3a8"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PaX2JKScxAwnEVXUiKrB5fxvRdaxjjJFWa-kJ-i_e7g/edit"

# Init IA
genai.configure(api_key=GOOGLE_AI_KEY)
model_ia = genai.GenerativeModel('gemini-pro')

# --- FONCTION CONNEXION GSHEET ---
def load_data():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sh = client.open_by_url(SHEET_URL)
    return sh.get_worksheet(0) # Prend la première feuille

# --- UI DESIGN ---
st.set_page_config(page_title="Lumina Nursery", layout="wide")
st.markdown("<style>div.block-container{padding-top:2rem;} .stApp{background-color:#0E1117; color:white;}</style>", unsafe_allow_html=True)

st.title("🏛️ LUMINA EXECUTIVE MANAGER")

try:
    worksheet = load_data()
    records = worksheet.get_all_records()
    df = pd.DataFrame(records)

    menu = st.sidebar.selectbox("Menu", ["Dashboard", "Familles", "Finance IA"])

    if menu == "Dashboard":
        st.subheader("Vue d'ensemble")
        col1, col2 = st.columns(2)
        col1.metric("CA Mensuel", f"{df['Montant'].sum()} €")
        col2.metric("Effectif", len(df))
        
        fig = px.bar(df, x="Nom de l'enfant", y="Montant", color="Statut", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Familles":
        st.subheader("Base de données interactive")
        # Éditeur direct
        new_df = st.data_editor(df, num_rows="dynamic")
        if st.button("💾 Synchroniser avec Google Sheets"):
            worksheet.update([new_df.columns.values.tolist()] + new_df.values.tolist())
            st.success("Données enregistrées !")
            
        st.divider()
        if st.button("📲 Envoyer les rappels WhatsApp (J-3)"):
            st.info("Traitement Green API en cours...")
            # Ici la boucle requests.post vers Green API pour chaque ligne

    elif menu == "Finance IA":
        st.subheader("💎 IA Financial Auditor")
        exp = st.text_area("Listez vos dépenses du mois (ex: Elec 200, Food 500...)")
        if st.button("Analyser avec Gemini"):
            response = model_ia.generate_content(f"Analyze these nursery expenses and give 3 tips in English: {exp}")
            st.write(response.text)

except Exception as e:
    st.error(f"Erreur : {e}")
    st.warning("Assurez-vous d'avoir partagé le Sheet avec l'email du robot et configuré les secrets.")
