import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import requests
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
GOOGLE_AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"
GREEN_API_ID = "41e4cb90444f42a8"
GREEN_API_TOKEN = "b2ef21886432f2286ad973eefb1e45f3a8"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PaX2JKScxAwnEVXUiKrB5fxvRdaxjjJFWa-kJ-i_e7g/edit"

# Configuration IA
genai.configure(api_key=GOOGLE_AI_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

# --- CONNEXION GOOGLE SHEETS ---
def get_worksheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # Utilise les secrets configurés dans .streamlit/secrets.toml
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sh = client.open_by_url(SHEET_URL)
    return sh.get_worksheet(0)

# --- UI DESIGN ---
st.set_page_config(page_title="Lumina Nursery Manager", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1A1C23; border-right: 1px solid #D4AF37; }
    .stMetric { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; background: #1A1C23; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stButton>button { border: 1px solid #D4AF37; background: transparent; color: #D4AF37; transition: 0.3s; width: 100%; }
    .stButton>button:hover { background: #D4AF37; color: black; box-shadow: 0 0 10px #D4AF37; }
    </style>
""", unsafe_allow_html=True)

try:
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Familles", "IA Finance"])

    if menu == "Dashboard":
        st.title("✨ Executive Dashboard")
        col1, col2, col3 = st.columns(3)
        
        ca = df['Montant à payer'].sum() if 'Montant à payer' in df.columns else 0
        retards = len(df[df['Statut de paiement'] == 'En retard']) if 'Statut de paiement' in df.columns else 0
        
        col1.metric("REVENUS PRÉVUS", f"{ca} €")
        col2.metric("EFFECTIF", len(df))
        col3.metric("RETARDS", retards)

        fig = px.pie(df, names='Statut de paiement', values='Montant à payer', hole=0.5,
                     color_discrete_sequence=['#D4AF37', '#E5E4E2', '#FF4B4B'])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig, use_container_width=True)

    elif menu == "Familles":
        st.title("👨‍👩‍👧 Gestion des Familles")
        edited_df = st.data_editor(df, num_rows="dynamic")
        
        if st.button("💾 Enregistrer les modifications"):
            clean_df = edited_df.fillna("")
            worksheet.update([clean_df.columns.values.tolist()] + clean_df.values.tolist())
            st.success("Synchronisation Sheets réussie !")

        st.divider()
        if st.button("🚀 Lancer les rappels WhatsApp (J-3)"):
            today = datetime.now().date()
            count = 0
            for _, row in edited_df.iterrows():
                try:
                    echeance = pd.to_datetime(row['Date de paiement mensuelle']).date()
                    if 0 <= (echeance - today).days <= 3 and row['Statut de paiement'] != "Payé":
                        phone = str(row['Numéro WhatsApp']).replace("+", "").strip()
                        parent = row['Nom du père'] if row['Nom du père'] else row['Nom de la mère']
                        msg = f"Bonjour Mr/Mme {parent}, rappel de paiement pour {row['Prénom de l’enfant']} prévu le {echeance}. Montant: {row['Montant à payer']}€."
                        
                        url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
                        requests.post(url, json={"chatId": f"{phone}@c.us", "message": msg})
                        count += 1
                except: continue
            st.success(f"{count} messages envoyés !")

    elif menu == "IA Finance":
        st.title("💎 Analyse IA des Dépenses")
        e = st.number_input("Électricité", 0)
        f = st.number_input("Nourriture", 0)
        s = st.number_input("Salaires", 0)
        
        if st.button("Analyser"):
            res = ai_model.generate_content(f"Analyze these expenses and give 3 tips in English: Elec {e}, Food {f}, Staff {s}")
            st.info(res.text)

except Exception as e:
    st.error(f"Erreur : {e}")
