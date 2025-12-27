import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import urllib.parse

# --- CONFIGURATION SÉCURISÉE ---
st.set_page_config(page_title="Ludo Gold Interne", layout="wide", page_icon="👶")

# Connexion au Google Sheets (utilise le lien mis dans tes Secrets Streamlit)
url = st.secrets["gsheets_url"]
conn = st.connection("gsheets", type=GSheetsConnection)

# --- STYLE PREMIUM ---
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; color: #1a1a1a; }
    .main-header { font-size: 32px; font-weight: bold; color: #2E86C1; text-align: center; }
    .stButton>button { background: #28B463; color: white; border-radius: 10px; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">🏠 LUDO GOLD : LOGICIEL INTERNE v1.0</p>', unsafe_allow_html=True)

# --- NAVIGATION ---
tabs = st.tabs(["📊 BILAN", "👶 ENFANTS & FAMILLES", "💸 DÉPENSES"])

# --- MODULE 1 : BILAN & DASHBOARD ---
with tabs[0]:
    try:
        df_p = conn.read(spreadsheet=url, worksheet="Parents")
        df_d = conn.read(spreadsheet=url, worksheet="Dépenses")
        
        # Calculs
        recettes = pd.to_numeric(df_p["Montant"], errors='coerce').sum()
        depenses = pd.to_numeric(df_d["Montant"], errors='coerce').sum()
        solde = recettes - depenses
        
        c1, c2, c3 = st.columns(3)
        c1.metric("REVENUS", f"{recettes:,.0f} DA")
        c2.metric("DÉPENSES", f"{depenses:,.0f} DA")
        c3.metric("BÉNÉFICE NET", f"{solde:,.0f} DA", delta=f"{solde:,.0f}")
        
        # Graphique
        fig = px.pie(df_d, values='Montant', names='Catégorie', title="Répartition des Charges", hole=0.5)
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.info("Veuillez remplir les données dans les autres onglets.")

# --- MODULE 2 : GESTION DES ENFANTS & WHATSAPP ---
with tabs[1]:
    st.subheader("👨‍👩‍👧‍👦 Registre des Familles")
    try:
        df_p = conn.read(spreadsheet=url, worksheet="Parents")
        # Colonnes attendues : Nom, Prénom, Age, Papa, Maman, Tel, Date_Paiement, Montant
        edited_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key="parent_editor")
        
        if st.button("💾 SAUVEGARDER LES ENFANTS"):
            conn.update(spreadsheet=url, worksheet="Parents", data=edited_p)
            st.success("Synchronisation Google Sheets réussie ! ✅")
        
        st.divider()
        st.subheader("📲 Rappels WhatsApp")
        today_day = datetime.now().day
        
        for i, row in edited_p.iterrows():
            # On vérifie si le jour de paiement correspond à aujourd'hui
            try:
                pay_day = int(row['Date_Paiement'])
                if pay_day == today_day:
                    msg = f"Bonjour {row['Maman']}, rappel pour le paiement de {row['Prénom']} ({row['Montant']} DA). Merci ! 🌸"
                    phone = str(row['Tel']).replace(" ", "")
                    # Ajout de l'indicatif Algérie si manquant
                    if not phone.startswith('213'): phone = "213" + phone
                    
                    wa_url = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                    st.warning(f"⏰ ÉCHÉANCE AUJOURD'HUI : {row['Prénom']}")
                    st.markdown(f"[CLIQUEZ ICI POUR ENVOYER LE RAPPEL À {row['Maman']}]( {wa_url} )")
            except:
                continue
    except Exception as e:
        st.error(f"Erreur de structure : {e}")

# --- MODULE 3 : DÉPENSES ---
with tabs[2]:
    st.subheader("🧾 Gaz, Eau, Électricité & Nutrition")
    try:
        df_d = conn.read(spreadsheet=url, worksheet="Dépenses")
        # Colonnes attendues : Catégorie, Montant, Date
        edited_d = st.data_editor(df_d, num_rows="dynamic", use_container_width=True, key="dep_editor")
        
        if st.button("💾 SAUVEGARDER LES DÉPENSES"):
            conn.update(spreadsheet=url, worksheet="Dépenses", data=edited_d)
            st.success("Dépenses enregistrées ! ✅")
    except Exception as e:
        st.error(f"Erreur de structure : {e}")
