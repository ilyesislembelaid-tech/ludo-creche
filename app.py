import streamlit as st
import requests
import pandas as pd

# --- CONFIGURATION (Tes clés restent les mêmes) ---
ID_INSTANCE = "1101961689"
API_TOKEN = "41e4cb90444f42a8b2ef21886432f2286ad973eefb1e45f3a8"
AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"

st.set_page_config(page_title="Ludo Management Pro", layout="wide", page_icon="🎨")

# --- DESIGN FUTURISTE (CSS CUSTOM) ---
st.markdown("""
    <style>
    /* Fond dégradé doux */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Cartes futuristes */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.7);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        transition: transform 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }

    /* Titres colorés */
    h1 {
        color: #4A90E2;
        font-family: 'Comic Sans MS', cursive, sans-serif;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* Style des boutons */
    .stButton>button {
        width: 100%;
        border-radius: 50px;
        height: 3em;
        background-color: #FF4B4B;
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3);
    }
    .stButton>button:hover {
        background-color: #FF2B2B;
        box-shadow: 0 6px 20px rgba(255, 75, 75, 0.5);
        transform: scale(1.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO ET TITRE ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("https://i.ibb.co/v4S6Yf7/468888427-1244682499919526-1850707048973692228-n.jpg", width=150)
    st.title("Ludo Management Pro")
    st.markdown("<p style='text-align: center; color: #666;'>L'avenir de votre crèche, aujourd'hui.</p>", unsafe_allow_html=True)

# --- LOGIQUE ---
tab1, tab2, tab3 = st.tabs(["🚀 Dashboard", "👶 Enfants & Parents", "👥 Équipe"])

with tab1:
    st.subheader("État des Finances")
    c1, c2, c3 = st.columns(3)
    # Données simulées pour le design
    c1.metric("Revenus", "450,000 DZD", "+12%")
    c2.metric("Charges", "120,000 DZD", "-5%")
    c3.metric("Bénéfice Net", "330,000 DZD", "🔥")
    
    st.info("💡 Conseil IA : Les revenus sont stables, mais vous pourriez optimiser les frais de cantine.")

with tab2:
    st.subheader("Gestion des Inscriptions")
    df_p = pd.DataFrame([
        {"Enfant": "Yanis", "Parent": "Mme. Amraoui", "Tel": "213550000000", "Statut": "Payé", "DZD": 25000},
        {"Enfant": "Ines", "Parent": "Mr. Belkacem", "Tel": "213550000001", "Statut": "En attente", "DZD": 22000}
    ])
    st.data_editor(df_p, num_rows="dynamic", use_container_width=True)
    st.button("🔔 Envoyer les Rappels Automatiques")

with tab3:
    st.subheader("Gestion de l'Équipe")
    df_e = pd.DataFrame([
        {"Nom": "Khadidja", "Poste": "Éducatrice", "Salaire": 45000, "Statut": "Virement prêt"}
    ])
    st.table(df_e)
    st.button("💰 Valider les Salaires")
