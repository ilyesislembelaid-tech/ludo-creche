import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from datetime import datetime
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Ludo Gold - Gestion Totale", layout="wide")

# Connexion
url = st.secrets["gsheets_url"]
conn = st.connection("gsheets", type=GSheetsConnection)

# --- CSS POUR UN LOOK PRO ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .stButton>button { border-radius: 8px; height: 3em; font-weight: bold; }
    .main-title { color: #1E3A8A; text-align: center; font-weight: bold; font-size: 40px; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">🏰 LUDO GOLD : GESTION INTERNE</p>', unsafe_allow_html=True)

# --- CHARGEMENT DES DONNÉES ---
df_p = conn.read(spreadsheet=url, worksheet="Parents", ttl=0)
df_d = conn.read(spreadsheet=url, worksheet="Dépenses", ttl=0)

menu = st.sidebar.radio("MENU", ["📊 Tableau de Bord", "👶 Gestion Enfants", "💸 Gestion Dépenses"])

# --- 1. TABLEAU DE BORD ---
if menu == "📊 Tableau de Bord":
    st.header("État de la Crèche")
    recettes = pd.to_numeric(df_p["Montant"]).sum()
    depenses = pd.to_numeric(df_d["Montant"]).sum()
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Recettes", f"{recettes} DA")
    col2.metric("Total Charges", f"{depenses} DA")
    col3.metric("Bénéfice Net", f"{recettes - depenses} DA")

    st.divider()
    st.subheader("🔔 Rappels WhatsApp du jour")
    today_day = datetime.now().day
    for _, row in df_p.iterrows():
        if str(row['Date_Paiement']) == str(today_day):
            msg = f"Bonjour {row['Maman']}, rappel pour le paiement de {row['Prénom']}. Merci !"
            link = f"https://wa.me/{str(row['Tel']).replace(' ', '')}?text={urllib.parse.quote(msg)}"
            st.info(f"Paiement dû pour **{row['Prénom']}**")
            st.markdown(f"[📲 Envoyer le message WhatsApp]({link})")

# --- 2. GESTION ENFANTS (MODIFICATION TOTALE) ---
elif menu == "👶 Gestion Enfants":
    st.header("Registre des Enfants")
    
    # Mode Edition via le tableau
    st.subheader("📝 Modifier ou Supprimer (Directement dans le tableau)")
    edited_df = st.data_editor(df_p, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Enregistrer toutes les modifications"):
        conn.update(spreadsheet=url, worksheet="Parents", data=edited_df)
        st.success("C'est enregistré dans la base de données ! ✅")

    st.divider()
    
    # Formulaire d'ajout rapide
    with st.expander("➕ Ajouter un nouvel enfant"):
        with st.form("add_child"):
            c1, c2, c3 = st.columns(3)
            nom = c1.text_input("Nom")
            prenom = c2.text_input("Prénom")
            age = c3.number_input("Âge", min_value=0, max_value=6)
            
            c4, c5, c6 = st.columns(3)
            papa = c4.text_input("Nom du Papa")
            maman = c5.text_input("Nom de la Maman")
            tel = c6.text_input("Téléphone WhatsApp (ex: 213...)")
            
            c7, c8 = st.columns(2)
            date_p = c7.slider("Jour de paiement (1 au 31)", 1, 31, 5)
            montant = c8.number_input("Montant Mensuel (DA)", value=15000)
            
            if st.form_submit_button("Ajouter l'enfant"):
                new_data = pd.DataFrame([[nom, prenom, age, papa, maman, tel, date_p, montant]], columns=df_p.columns)
                updated_df = pd.concat([df_p, new_data], ignore_index=True)
                conn.update(spreadsheet=url, worksheet="Parents", data=updated_df)
                st.success("Enfant ajouté ! Actualisez la page.")

# --- 3. GESTION DÉPENSES ---
elif menu == "💸 Gestion Dépenses":
    st.header("Suivi des Charges")
    
    st.subheader("📝 Liste des frais (Gaz, Eau, Nourriture...)")
    edited_d = st.data_editor(df_d, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Enregistrer les dépenses"):
        conn.update(spreadsheet=url, worksheet="Dépenses", data=edited_d)
        st.success("Dépenses mises à jour ! ✅")

    with st.expander("➕ Ajouter une dépense"):
        with st.form("add_dep"):
            cat = st.selectbox("Catégorie", ["Nutrition", "Gaz", "Électricité", "Eau", "Loyer", "Autre"])
            mnt = st.number_input("Montant (DA)")
            date_d = st.date_input("Date")
            if st.form_submit_button("Ajouter la charge"):
                new_dep = pd.DataFrame([[cat, mnt, date_d.strftime("%Y-%m-%d")]], columns=df_d.columns)
                updated_dep = pd.concat([df_d, new_dep], ignore_index=True)
                conn.update(spreadsheet=url, worksheet="Dépenses", data=updated_dep)
                st.success("Dépense enregistrée !")
