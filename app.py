import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"
AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"

st.set_page_config(page_title="La Ludo Crèche", layout="wide")

st.title("🎨 La Ludo Crèche : Gestion")

# Fonction d'envoi WhatsApp
def send_wa(number, message):
    url = f"https://api.green-api.com/waInstance{ID_INSTANCE}/sendMessage/{API_TOKEN}"
    payload = {"chatId": f"{number}@c.us", "message": message}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False

# Onglets
tab1, tab2, tab3 = st.tabs(["👶 Parents", "👥 Employés", "💰 Bilan"])

with tab1:
    st.subheader("Paiements Parents")
    df_p = pd.DataFrame([
        {"Enfant": "Exemple", "Tel": "213550000000", "Prix": 25000}
    ])
    edit_p = st.data_editor(df_p, num_rows="dynamic", key="parents")
    if st.button("🚀 Envoyer rappels WhatsApp"):
        st.info("Envoi en cours...")

with tab2:
    st.subheader("Salaires Employés")
    df_e = pd.DataFrame([
        {"Nom": "Exemple", "Tel": "213550000000", "Salaire": 35000}
    ])
    edit_e = st.data_editor(df_e, num_rows="dynamic", key="staff")

with tab3:
    gains = edit_p["Prix"].sum()
    depenses = edit_e["Salaire"].sum()
    st.metric("Bénéfice Net", f"{gains - depenses} DZD")
