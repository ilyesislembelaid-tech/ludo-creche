import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

# Futuristic Gold & Dark Theme
st.markdown("""
    <style>
    .main { background-color: #050a12; color: #e0e0e0; }
    .stMetric { border: 1px solid #d4af37; padding: 20px; border-radius: 10px; background: #0a1424; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { background-color: #d4af37; color: black; width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
def get_worksheet():
    try:
        client = gspread_client.get_client(st.secrets["gcp_service_account"])
        # Use your specific sheet URL
        sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
        return sh.worksheet("Feuille 1")
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

ws = get_worksheet()

# --- WHATSAPP SENDING FUNCTION ---
def send_whatsapp(phone, parent, child, amount, date):
    url = f"https://api.green-api.com/waInstance{st.secrets['api_keys']['green_api_id']}/sendMessage/{st.secrets['api_keys']['green_api_token']}"
    message = f"Dear Mr/Ms {parent},\n\nPayment for {child} is due on {date}.\nAmount: {amount} €.\n\nThank you,\nLumina Nursery"
    payload = {"chatId": f"{phone}@c.us", "message": message}
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except:
        return False

# --- MAIN APP ---
if ws:
    data = ws.get_all_records()
    df = pd.DataFrame(data)
    
    st.sidebar.title("🏛️ LUMINA ADMIN")
    menu = st.sidebar.selectbox("Navigation", ["Dashboard", "Family Management", "AI Finance"])

    if menu == "Dashboard":
        st.title("📊 Executive Dashboard")
        c1, c2, c3 = st.columns(3)
        
        # Safe calculation of metrics
        total = df['Amount'].sum() if not df.empty and 'Amount' in df.columns else 0
        overdue = len(df[df['Status'] == 'Overdue']) if not df.empty and 'Status' in df.columns else 0
        
        c1.metric("Total Revenue", f"{total} €")
        c2.metric("Overdue Payments", overdue)
        c3.metric("Total Children", len(df))
        
        st.subheader("📋 Registry Overview")
        st.dataframe(df, use_container_width=True)

    elif menu == "Family Management":
        st.title("👨‍👩‍👧 Family Management")
        
        # Edit existing data
        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Sync with Google Sheets"):
                ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
                st.success("Database Updated!")
        
        # Add new family
        with st.expander("➕ Register New Child"):
            with st.form("add_form"):
                col1, col2 = st.columns(2)
                ln = col1.text_input("Last Name")
                fn = col1.text_input("First Name")
                ph = col2.text_input("Phone (e.g. 33612345678)")
                am = col2.number_input("Monthly Fee", min_value=0)
                dt = st.date_input("Due Date")
                
                if st.form_submit_button("Add
