import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import requests
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION API ---
# Remarque : Les clés sont ici en dur pour ton test, mais utilise st.secrets en prod.
GOOGLE_AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"
GREEN_API_ID = "41e4cb90444f42a8"
GREEN_API_TOKEN = "b2ef21886432f2286ad973eefb1e45f3a8"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PaX2JKScxAwnEVXUiKrB5fxvRdaxjjJFWa-kJ-i_e7g/edit"

# Configuration Gemini
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

# --- DESIGN & STYLE ---
st.set_page_config(page_title="Lumina Nursery Manager", layout="wide", page_icon="🏛️")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    [data-testid="stSidebar"] { background-color: #1A1C23; border-right:
