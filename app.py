import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Ludo Gold Interne", layout="wide")

st.markdown("""
    <style>
    .stApp { background: #0e1117; color: white; }
    [data-testid="stMetricValue"] { color: #00f2fe !important; }
    .stButton>button { background: #00f2fe; color: black; border-radius: 10px; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNEXION GOOGLE SHEETS ---
url = st.secrets["gsheets_url"]
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("👑 LUDO GOLD : GESTION INTERNE")

t1, t2, t3 = st.tabs(["👶 ENFANTS & PAIEMENTS", "🔌 CHARGES (GAZ/EAU/EDF)", "📊 BILAN"])

# --- ONGLET 1 : ENFANTS ---
with t1:
    st.subheader("Registre des Enfants")
    try:
        df_p = conn.read(spreadsheet=url, worksheet="Parents")
        # Colonnes : Nom, Prénom, Age, Papa, Maman, Tel, Date_Paiement, Montant
        edit_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key="p_edit")
        
        if st.button("💾 Enregistrer la liste des enfants"):
            conn.update(spreadsheet=url, worksheet="Parents", data=edit_p)
            st.success("Données sauvegardées ! ✅")

        # LOGIQUE RAPPEL AUTO
        st.divider()
        st.subheader("🔔 Rappels WhatsApp Automatiques")
        today = datetime.now().strftime("%Y-%m-%d")
        for index, row in edit_p.iterrows():
            if str(row['Date_Paiement']) == today:
                msg = f"Bonjour, c'est La Ludo Crèche. Un petit rappel pour le paiement de {row['Prénom']} aujourd'hui. Merci !"
                tel = str(row['Tel']).replace("+", "")
                link = f"https://wa.me/{tel}?text={msg.replace(' ', '%20')}"
                st.warning(f"⚠️ PAIEMENT DÛ AUJOURD'HUI : {row['Prénom']} {row['Nom']}")
                st.markdown(f"[📲 CLIQUER ICI POUR ENVOYER LE MESSAGE À {row['Prénom']}]({link})")
    except:
        st.info("Ajoutez les colonnes: Nom, Prénom, Age, Papa, Maman, Tel, Date_Paiement, Montant dans votre Sheets 'Parents'")

# --- ONGLET 2 : CHARGES ---
with t2:
    st.subheader("Gestion des Dépenses")
    try:
        df_d = conn.read(spreadsheet=url, worksheet="Dépenses")
        # Colonnes : Catégorie (Gaz, Eau, Elec, Nutrition), Montant, Date
        edit_d = st.data_editor(df_d, num_rows="dynamic", use_container_width=True, key="d_edit")
        
        if st.button("💾 Enregistrer les dépenses"):
            conn.update(spreadsheet=url, worksheet="Dépenses", data=edit_d)
            st.success("Dépenses mises à jour ! ✅")
    except:
        st.info("Ajoutez les colonnes: Catégorie, Montant, Date dans votre Sheets 'Dépenses'")

# --- ONGLET 3 : BILAN ---
with t3:
    st.subheader("Bilan Financier")
    try:
        total_recettes = pd.to_numeric(edit_p["Montant"]).sum()
        total_depenses = pd.to_numeric(edit_d["Montant"]).sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("TOTAL REÇU", f"{total_recettes} DA")
        c2.metric("TOTAL CHARGES", f"{total_depenses} DA")
        c3.metric("RÉEL (NET)", f"{total_recettes - total_depenses} DA")
    except:
        st.write("Calcul impossible. Vérifiez les chiffres dans les tableaux.")
