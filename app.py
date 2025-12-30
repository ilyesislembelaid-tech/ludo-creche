import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime

# --- 1. UI SETUP ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a12; color: #ffffff; }
    .stMetric { border: 1px solid #d4af37; background-color: #0a1424; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; }
    .stButton>button { background-color: #d4af37 !important; color: black !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. CONNECTIONS ---
@st.cache_resource
def init_gsheet():
    try:
        client = gspread_client.get_client(st.secrets["gcp_service_account"])
        sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
        # Ensure this matches your tab name exactly
        return sh.worksheet("Feuille 1")
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

ws = init_gsheet()

# --- 3. APP LOGIC ---
if ws:
    # Load Data
    data = ws.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Family Management", "AI Financials"])

    if menu == "Dashboard":
        st.title("📈 Executive Dashboard")
        col1, col2, col3 = st.columns(3)
        
        total_revenue = df['Amount'].sum() if not df.empty else 0
        overdue_count = len(df[df['Status'] == 'Overdue']) if not df.empty else 0
        
        col1.metric("Projected Revenue", f"{total_revenue} €")
        col2.metric("Overdue Payments", overdue_count)
        col3.metric("Total Enrollment", len(df))
        
        st.subheader("Registry Overview")
        st.dataframe(df, use_container_width=True)

    elif menu == "Family Management":
        st.title("👨‍👩‍👧 Family Management")
        
        # Table Editor
        if not df.empty:
            st.subheader("Current Records")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Sync Changes to Cloud"):
                ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
                st.success("Database Updated!")

        # Add New Form
        st.markdown("---")
        st.subheader("➕ Register New Child")
        with st.form("add_new_child"):
            c1, c2 = st.columns(2)
            last_n = c1.text_input("Last Name")
            first_n = c1.text_input("First Name")
            age = c1.number_input("Age", 0, 10)
            
            phone = c2.text_input("WhatsApp (e.g., 33600000000)")
            amount = c2.number_input("Monthly Fee", min_value=0)
            date = st.date_input("Due Date")
            
            # THE FIXED LINE
            submit = st.form_submit_button("Add to System")
            
            if submit:
                if last_n and phone:
                    ws.append_row([last_n, first_n, age, "", "", phone, str(date), amount, "Pending", ""])
                    st.success(f"Registered {first_n} successfully!")
                    st.rerun()
                else:
                    st.warning("Last Name and Phone are required.")

    elif menu == "AI Financials":
        st.title("💰 AI Cost Analysis")
        genai.configure(api_key=st.secrets["api_keys"]["gemini"])
        model = genai.GenerativeModel('gemini-pro')
        
        expenses = st.text_area("Detail your costs (e.g., Rent 1000, Food 300, Elec 100)")
        if st.button("Analyze with Lumina AI"):
            if expenses:
                response = model.generate_content(f"Analyze nursery expenses and give 3 tips in English: {expenses}")
                st.info(response.text)
            else:
                st.warning("Please enter some cost data.")

st.sidebar.markdown("---")
st.sidebar.caption("Lumina Executive v1.3")
