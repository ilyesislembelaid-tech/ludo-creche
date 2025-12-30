import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime

# --- SETTINGS & UI ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a12; color: #ffffff; }
    .stMetric { border: 1px solid #d4af37; background-color: #0a1424; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; }
    .stButton>button { background-color: #d4af37 !important; color: black !important; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNECTIONS ---
def init_gsheet():
    try:
        client = gspread_client.get_client(st.secrets["gcp_service_account"])
        sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
        return sh.worksheet("Feuille 1")
    except Exception as e:
        st.error(f"Spreadsheet Error: {e}")
        return None

ws = init_gsheet()

# --- MAIN LOGIC ---
if ws:
    # Load data
    data = ws.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    choice = st.sidebar.radio("Navigation", ["Dashboard", "Families", "AI Financials"])

    if choice == "Dashboard":
        st.title("📈 Executive Overview")
        c1, c2, c3 = st.columns(3)
        
        rev = df['Amount'].sum() if not df.empty and 'Amount' in df.columns else 0
        overdue = len(df[df['Status'] == 'Overdue']) if not df.empty and 'Status' in df.columns else 0
        
        c1.metric("Expected Revenue", f"{rev} €")
        c2.metric("Overdue Payments", overdue)
        c3.metric("Total Children", len(df))
        
        st.subheader("Live Registry")
        st.dataframe(df, use_container_width=True)

    elif choice == "Families":
        st.title("👨‍👩‍👧 Family Management")
        
        # Table Editor
        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Save Changes to Cloud"):
                ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
                st.success("Database Synchronized!")
        
        # Add New Entry Form
        st.markdown("---")
        st.subheader("➕ Register New Child")
        with st.form("registration_form"):
            col1, col2 = st.columns(2)
            ln = col1.text_input("Last Name")
            fn = col1.text_input("First Name")
            age = col1.number_input("Age", 0, 10)
            ph = col2.text_input("WhatsApp (e.g. 33612345678)")
            am = col2.number_input("Monthly Fee (€)", min_value=0)
            dt = st.date_input("Due Date")
            
            if st.form_submit_button("Add to System"):
                if ln and fn and ph:
                    new_row = [ln, fn, age, "", "", ph, str(dt), am, "Pending", ""]
                    ws.append_row(new_row)
                    st.success(f"Successfully added {fn}!")
                    st.rerun()
                else:
                    st.error("Please fill in Name and Phone Number.")

    elif choice == "AI Financials":
        st.title("💰 AI Cost Analyzer")
        genai
