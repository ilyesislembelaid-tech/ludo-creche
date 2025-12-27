import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime, timedelta
import urllib.parse

# --- CONFIGURATION ET THEME ---
st.set_page_config(page_title="Ludo Gold Management", layout="wide", page_icon="👶")

# CSS pour un look "Premium Crèche" (Doux mais moderne)
st.markdown("""
    <style>
    .stApp { background-color: #FDFCF0; color: #2C3E50; }
    .main-header { font-size: 38px; font-weight: 800; color: #4facfe; text-align: center; margin-bottom: 20px; }
    .metric-card { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; }
    div[data-testid="stMetricValue"] { color: #4facfe; font-size: 28px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f0f2f6; border-radius: 10px; padding: 10px 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNEXION BASE DE DONNÉES ---
try:
    url = st.secrets["gsheets_url"]
    conn = st.connection("gsheets", type=GSheetsConnection)
except:
    st.error("⚠️ Erreur de connexion au Google Sheets. Vérifiez les Secrets.")
    st.stop()

# Fonctions de lecture
def get_data(sheet):
    return conn.read(spreadsheet=url, worksheet=sheet, ttl=0)

# --- LOGIQUE WHATSAPP ---
def send_wa(phone, message):
    phone = str(phone).replace("+", "").replace(" ", "")
    if not phone.startswith("213"): phone = "213" + phone # Défaut Algérie
    encoded_msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_msg}"

# --- NAVIGATION ---
st.markdown('<p class="main-header">🌸 LUDO GOLD MANAGEMENT 🌸</p>', unsafe_allow_html=True)
tabs = st.tabs(["🏠 DASHBOARD", "👶 ENFANTS & FAMILLES", "💰 PAIEMENTS", "📉 BUDGET & CHARGES", "⚙️ ADMIN"])

# 1. DASHBOARD
with tabs[0]:
    df_p = get_data("Parents")
    df_d = get_data("Dépenses")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Effectif", len(df_p))
    with col2: 
        total_rev = pd.to_numeric(df_p["Montant"], errors='coerce').sum()
        st.metric("Revenus Théoriques", f"{total_rev:,.0f} DA")
    with col3:
        total_exp = pd.to_numeric(df_d["Montant"], errors='coerce').sum()
        st.metric("Total Dépenses", f"{total_exp:,.0f} DA")
    with col4:
        st.metric("Bénéfice Net", f"{(total_rev - total_exp):,.0f} DA")

    st.divider()
    c_left, c_right = st.columns(2)
    with c_left:
        fig_exp = px.pie(df_d, values='Montant', names='Catégorie', title="Répartition des Dépenses", hole=.4)
        st.plotly_chart(fig_exp, use_container_width=True)
    with c_right:
        st.subheader("🔔 Alertes du jour")
        today = datetime.now().date()
        # Simulation d'alertes basées sur la colonne Date_Paiement
        df_p['Date_DT'] = pd.to_datetime(df_p['Date_Paiement'], errors='coerce')
        retards = df_p[df_p['Date_DT'].dt.day == today.day]
        if not retards.empty:
            for _, r in retards.iterrows():
                st.warning(f"Paiement attendu aujourd'hui : {r['Prénom']} ({r['Montant']} DA)")

# 2. GESTION DES ENFANTS
with tabs[1]:
    st.subheader("🗂️ Registre Complet")
    df_p = get_data("Parents")
    edited_p = st.data_editor(df_p, num_rows="dynamic", use_container_width=True, key="p_editor")
    if st.button("💾 Sauvegarder les modifications (Enfants)"):
        conn.update(spreadsheet=url, worksheet="Parents", data=edited_p)
        st.success("Base de données mise à jour !")

# 3. PAIEMENTS & WHATSAPP
with tabs[2]:
    st.subheader("💵 Suivi des mensualités")
    df_pay = edited_p.copy()
    
    for index, row in df_pay.iterrows():
        col_n, col_s, col_w = st.columns([2, 1, 2])
        col_n.write(f"**{row['Prénom']} {row['Nom']}** ({row['Montant']} DA)")
        status = col_s.selectbox("Statut", ["Payé", "En attente", "Retard"], key=f"status_{index}")
        
        msg = f"Bonjour {row['Maman']}, rappel pour le paiement de {row['Prénom']} ({row['Montant']} DA). Merci de votre confiance ✨"
        wa_url = send_wa(row['Tel'], msg)
        col_w.markdown(f"[📩 Envoyer Rappel WhatsApp]({wa_url})")

# 4. BUDGET & CHARGES
with tabs[3]:
    st.subheader("📉 Gestion des Frais")
    df_d = get_data("Dépenses")
    edited_d = st.data_editor(df_d, num_rows="dynamic", use_container_width=True, key="d_editor")
    if st.button("💾 Enregistrer les dépenses"):
        conn.update(spreadsheet=url, worksheet="Dépenses", data=edited_d)
        st.success("Charges enregistrées !")

# 5. ADMIN & MESSAGES PRESET
with tabs[4]:
    st.subheader("⚙️ Configuration des messages")
    st.text_input("Message de bienvenue", "Bienvenue chez Ludo Gold ! Nous sommes ravis d'accueillir...")
    st.text_area("Menu de la semaine", "Lundi : Purée de légumes...")
    st.button("Mettre à jour les modèles de messages")
