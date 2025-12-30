import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime

# --- SETTINGS & UI ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

# Futuristic Gold & Dark Theme
st.markdown("""
    <style>
    .main { background-color: #050a12; color: #ffffff; }
    .stMetric { border: 1px solid #d4af37; background-color: #0a1424; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; letter-spacing: 2px; }
    .stButton>button { background-color: #d4af37 !important; color: black !important; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNECTIONS ---
def init_gsheet():
    try:
        client = gspread_client.get_client(st.secrets["gcp_service_account"])
        # Your specific spreadsheet URL
        sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
        # Change "Feuille 1" to "Parents" if you renamed the tab
        return sh.worksheet("Feuille 1")
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

ws = init_gsheet()

# --- WHATSAPP ENGINE ---
def send_whatsapp(phone, parent, child, amount, date):
    id_ins = st.secrets["api_keys"]["green_api_id"]
    token = st.secrets["api_keys"]["green_api_token"]
    url = f"https://api.green-api.com/waInstance{id_ins}/sendMessage/{token}"
    
    text = f"Hello {parent},\n\nPayment reminder for {child}.\nDue Date: {date}\nAmount: {amount}€.\n\nThank you, Lumina Nursery."
    payload = {"chatId": f"{phone}@c.us", "message": text}
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except:
        return False

# --- MAIN APP LOGIC ---
if ws:
    data = ws.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    choice = st.sidebar.radio("Navigation", ["Dashboard", "Families", "AI Financials"])

    if choice == "Dashboard":
        st.title("📈 Executive Overview")
        c1, c2, c3 = st.columns(3)
        
        rev = df['Amount'].sum() if not df.empty and 'Amount' in df.columns else 0
        overdue = len(df[df['Status'] == 'Overdue']) if not df.empty and 'Status' in df.columns else 0
        
        c1.metric("Projected Revenue", f"{rev} €")
        c2.metric("Overdue Payments", overdue)
        c3.metric("Total Kids", len(df))
        
        st.subheader("Current Registry")
        st.dataframe(df, use_container_width=True)

    elif choice == "Families":
        st.title("👨‍👩‍👧 Family Management")
        
        # Interactive Editor
        if not df.empty:
            edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
            if st.button("Sync Changes to Google Sheets"):
                ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
                st.success("Database Synchronized!")
        
        # Add New Entry
        st.markdown("---")
        st.subheader("➕ Register New Child")
        with st.form("add_child_form"):
            col1, col2 = st.columns(2)
            ln = col1.text_input("Last Name")
            fn = col1.text_input("First Name")
            age = col1.number_input("Age", 0, 10)
            ph = col2.text_input("WhatsApp (e.g. 33612345678)")
            am = col2.number_input("Monthly Fee (€)", min_value=0)
            dt = st.date_input("Due Date")
            
            if st.form_submit_button("Add to System"):
                if ln and ph:
                    ws.append_row([ln, fn, age, "", "", ph, str(dt), am, "Pending", ""])
                    st.success(f"Successfully added {fn}!")
                    st.rerun()
                else:
                    st.error("Please provide at least a Name and Phone Number.")

    elif choice == "AI Financials":
        st.title("💰 AI Cost Analyzer")
        genai.configure(api_key=st.secrets["api_keys"]["gemini"])
        model = genai.GenerativeModel('gemini-pro')
        
        user_input = st.text_area("Detail your expenses (e.g., Food 400, Rent 1200, Electricity 150)")
        if st.button("Run Financial Audit"):
            if user_input:
                response = model.generate_content(f"Analyze these costs for a nursery and suggest 3 tips in English: {user_input}")
                st.info(response.text)

# Sidebar footer
st.sidebar.markdown("---")
st.sidebar.caption("Lumina Executive v1.2")
