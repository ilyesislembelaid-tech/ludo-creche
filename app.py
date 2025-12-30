import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime

# --- UI CONFIGURATION ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a12; color: #ffffff; }
    .stMetric { border: 1px solid #d4af37; background-color: #0a1424; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; letter-spacing: 1px; }
    .stButton>button { background-color: #d4af37 !important; color: black !important; font-weight: bold; border-radius: 5px; }
    .stDataFrame { border: 1px solid #d4af37; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS CONNECTION ---
def init_gsheet():
    try:
        client = gspread_client.get_client(st.secrets["gcp_service_account"])
        # Connect via your specific URL
        sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
        # Ensure the tab name matches your Sheet (Feuille 1 or Parents)
        return sh.worksheet("Feuille 1") 
    except Exception as e:
        st.error(f"Spreadsheet Connection Failed: {e}")
        return None

ws = init_gsheet()

# --- APP NAVIGATION ---
if ws:
    data = ws.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Family Management", "AI Financials"])

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.title("📈 Executive Dashboard")
        
        c1, c2, c3 = st.columns(3)
        total_rev = df['Amount'].sum() if not df.empty and 'Amount' in df.columns else 0
        overdue_count = len(df[df['Status'] == 'Overdue']) if not df.empty and 'Status' in df.columns else 0
        
        c1.metric("Projected Revenue", f"{total_rev} €")
        c2.metric("Overdue Cases", overdue_count)
        c3.metric("Total Enrollment", len(df))
        
        st.subheader("📋 Enrollment Registry")
        st.dataframe(df, use_container_width=True)

    # --- FAMILY MANAGEMENT ---
    elif menu == "Family Management":
        st.title("👨‍👩‍👧 Family Management")
        
        # CRUD: Inline Editing
        if not df.empty:
            st.subheader("Edit Records")
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Save Changes to Cloud"):
                ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
                st.success("Database Synchronized Successfully!")
        
        # CRUD: Add New Child
        st.markdown("---")
        st.subheader("➕ Register New Entry")
        with st.form("entry_form"):
            col1, col2 = st.columns(2)
            ln = col1.text_input("Last Name")
            fn = col1.text_input("First Name")
            age = col1.number_input("Age", 0, 10)
            
            ph = col2.text_input("WhatsApp Number (e.g. 33612345678)")
            am = col2.number_input("Monthly Fee (€)", min_value=0)
            dt = st.date_input("Payment Due Date")
            
            # FIXED SYNTAX HERE
            submitted = st.form_submit_button("Add to System")
            if submitted:
                if ln and ph:
                    # Append to Sheet: [Last_Name, First_Name, Age, Father, Mother, Phone, Due_Date, Amount, Status, Last_Reminder]
                    ws.append_row([ln, fn, age, "", "", ph, str(dt), am, "Pending", ""])
                    st.success(f"Successfully registered {fn} {ln}!")
                    st.rerun()
                else:
                    st.error("Missing Data: Please enter at least Last Name and WhatsApp Number.")

    # --- AI FINANCIALS ---
    elif menu == "AI Financials":
        st.title("💰 AI Cost Analyzer")
        
        if "api_keys" in st.secrets and "gemini" in st.secrets["api_keys"]:
            genai.configure(api_key=st.secrets["api_keys"]["gemini"])
            model = genai.GenerativeModel('gemini-pro')
            
            expenses = st.text_area("Detail your monthly expenses (e.g., Food 500, Rent 1500, Electricity 200)", height=150)
            
            if st.button("Generate Executive Analysis"):
                if expenses:
                    with st.spinner("Lumina AI is analyzing financial data..."):
                        response = model.generate_content(f"Act as a nursery financial consultant. Analyze these expenses and provide 3 optimization tips in English: {expenses}")
                        st.markdown("### 🤖 Lumina AI Insights")
                        st.info(response.text)
                else:
                    st.warning("Please input expense details for analysis.")
        else:
            st.error("Gemini API Key missing in secrets.")

# Footer
st.sidebar.markdown("---")
st.sidebar.caption("Lumina Executive Manager v1.3")
