import streamlit as st
import pandas as pd
from gspread_streamlit import gspread_client
import google.generativeai as genai
import requests
from datetime import datetime, timedelta

# --- SETTINGS & UI ---
st.set_page_config(page_title="LUMINA EXECUTIVE", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #050a12; color: #ffffff; }
    .stMetric { border: 1px solid #d4af37; background-color: #0a1424; padding: 20px; border-radius: 10px; }
    h1, h2, h3 { color: #d4af37 !important; text-transform: uppercase; }
    .stButton>button { background-color: #d4af37; color: black; font-weight: bold; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONNECTIONS ---
def init_gsheet():
    client = gspread_client.get_client(st.secrets["gcp_service_account"])
    sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
    return sh.worksheet("Feuille 1")

ws = init_gsheet()
df = pd.DataFrame(ws.get_all_records())

# --- WHATSAPP ENGINE ---
def send_reminder(phone, parent, child, amount, date):
    id_ins = st.secrets["api_keys"]["green_api_id"]
    token = st.secrets["api_keys"]["green_api_token"]
    url = f"https://api.green-api.com/waInstance{id_ins}/sendMessage/{token}"
    
    text = f"Hello {parent},\n\nThis is a reminder for {child}'s nursery payment.\nDate: {date}\nAmount: {amount}€.\n\nThank you, Lumina Nursery."
    payload = {"chatId": f"{phone}@c.us", "message": text}
    try:
        res = requests.post(url, json=payload)
        return res.status_code == 200
    except:
        return False

# --- APP MENU ---
st.sidebar.title("🏛️ LUMINA ADMIN")
choice = st.sidebar.radio("Navigation", ["Dashboard", "Families", "AI Financials"])

if choice == "Dashboard":
    st.title("📈 Executive Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Expected Revenue", f"{df['Amount'].sum() if not df.empty else 0} €")
    c2.metric("Overdue", len(df[df['Status'] == 'Overdue']) if not df.empty else 0)
    c3.metric("Total Kids", len(df))
    
    st.subheader("WhatsApp Automation")
    if st.button("🚀 Send Reminders for Payments in 3 days"):
        today = datetime.now()
        count = 0
        for i, row in df.iterrows():
            due_date = datetime.strptime(str(row['Due_Date']), '%Y-%m-%d')
            # Check 3 days before and if not already sent
            if (due_date - today).days <= 3 and row['Status'] != 'Paid' and not row['Last_Reminder']:
                if send_reminder(row['Phone'], row['Father_Name'], row['First_Name'], row['Amount'], row['Due_Date']):
                    ws.update_cell(i + 2, 10, today.strftime('%Y-%m-%d'))
                    count += 1
        st.success(f"Sent {count} reminders successfully.")

elif choice == "Families":
    st.title("👨‍👩‍👧 Family Management")
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    if st.button("Sync Database"):
        ws.update([edited_df.columns.values.tolist()] + edited_df.values.tolist())
        st.toast("Saved!")

elif choice == "AI Financials":
    st.title("💰 AI Cost Analyzer")
    genai.configure(api_key=st.secrets["api_keys"]["gemini"])
    model = genai.GenerativeModel('gemini-pro')
    
    costs = st.text_area("Enter monthly expenses (e.g. Electricity 200, Food 500)")
    if st.button("Analyze with Gemini"):
        resp = model.generate_content(f"Analyze these expenses and give 3 tips in English: {costs}")
        st.markdown(resp.text)
