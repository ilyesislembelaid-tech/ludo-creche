import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import requests
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
GOOGLE_AI_KEY = "AIzaSyBfhCp3ZHcrajcfYDbzCqoIlv898iPLiKQ"
GREEN_API_ID = "41e4cb90444f42a8"
GREEN_API_TOKEN = "b2ef21886432f2286ad973eefb1e45f3a8"
SHEET_URL = "https://docs.google.com/spreadsheets/d/1PaX2JKScxAwnEVXUiKrB5fxvRdaxjjJFWa-kJ-i_e7g/edit"

# Init Gemini AI
genai.configure(api_key=GOOGLE_AI_KEY)
ai_model = genai.GenerativeModel('gemini-1.5-flash')

# --- CONNEXION GOOGLE SHEETS ---
def get_worksheet():
    # ... connexion ...
    sh = client.open_by_url("https://docs.google.com/spreadsheets/d/1lYRd8k2Mv4_zmFruzCpepZJnhrqRvEm11bhulzHPibY/edit")
    return sh.worksheet("Feuille 1") # Utilise le nom détecté dans votre Drive

# --- DESIGN FUTURISTE ---
st.set_page_config(page_title="Lumina Executive", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    [data-testid="stSidebar"] { background-color: #1A1C23; border-right: 1px solid #D4AF37; }
    .stMetric { border: 1px solid #D4AF37; padding: 15px; border-radius: 10px; background: #1A1C23; }
    h1, h2, h3 { color: #D4AF37 !important; }
    .stButton>button { border: 1px solid #D4AF37; background: transparent; color: #D4AF37; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background: #D4AF37 !important; color: black !important; box-shadow: 0 0 15px #D4AF37; }
    </style>
""", unsafe_allow_html=True)

try:
    worksheet = get_worksheet()
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)

    st.sidebar.title("🏛️ LUMINA ADMIN")
    menu = st.sidebar.radio("Navigation", ["Dashboard", "Family Management", "Financial Analysis IA"])

    if menu == "Dashboard":
        st.title("✨ Executive Dashboard")
        col1, col2, col3 = st.columns(3)
        
        # Calculs basés sur vos colonnes exactes
        total_revenue = df['Montant'].sum() if 'Montant' in df.columns else 0
        lates = len(df[df['Statut'] == 'En retard']) if 'Statut' in df.columns else 0
        
        col1.metric("TOTAL REVENUE", f"{total_revenue} €")
        col2.metric("TOTAL CHILDREN", len(df))
        col3.metric("LATE PAYMENTS", lates)

        st.write("### 📊 Revenue Breakdown")
        if 'Statut' in df.columns:
            fig = px.pie(df, names='Statut', values='Montant', hole=0.5,
                         color_discrete_map={'Payé':'#D4AF37', 'En attente':'#E5E4E2', 'En retard':'#FF4B4B'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    elif menu == "Family Management":
        st.title("👨‍👩‍👧 Family Database")
        # Édition directe du tableau
        edited_df = st.data_editor(df, num_rows="dynamic", key="family_editor")
        
        if st.button("💾 Sync with Google Sheets"):
            clean_df = edited_df.fillna("")
            worksheet.update([clean_df.columns.values.tolist()] + clean_df.values.tolist())
            st.success("Google Sheets successfully updated!")

        st.divider()
        st.subheader("📲 WhatsApp Automated Reminders")
        if st.button("🚀 Run Reminder Campaign (J-3)"):
            today = datetime.now().date()
            sent_count = 0
            
            for _, row in edited_df.iterrows():
                try:
                    due_date = pd.to_datetime(row['Date_Paiement']).date()
                    # Si la date est dans moins de 3 jours et non payé
                    if 0 <= (due_date - today).days <= 3 and row['Statut'] != "Payé":
                        phone = str(row['Tel']).replace("+", "").strip()
                        parent = row['Papa'] if row['Papa'] else row['Maman']
                        
                        message = (f"Hello Mr/Ms {parent},\n\n"
                                   f"This is a reminder that the payment for *{row['Prénom']}* is due on *{due_date}*.\n"
                                   f"Amount: *{row['Montant']} €*.\n\n"
                                   f"Thank you for your trust.\nLumina Nursery ✨")
                        
                        url = f"https://api.green-api.com/waInstance{GREEN_API_ID}/sendMessage/{GREEN_API_TOKEN}"
                        requests.post(url, json={"chatId": f"{phone}@c.us", "message": message})
                        sent_count += 1
                        st.write(f"✅ Reminder sent to {parent} ({row['Prénom']})")
                except:
                    continue
            st.success(f"Campaign finished: {sent_count} messages sent.")

    elif menu == "Financial Analysis IA":
        st.title("💎 AI Expense Auditor")
        col_a, col_b = st.columns(2)
        elec = col_a.number_input("Electricity", 0)
        food = col_a.number_input("Food & Nutrition", 0)
        gas = col_b.number_input("Gas", 0)
        staff = col_b.number_input("Staff Salaries", 0)
        
        if st.button("Generate AI Insight"):
            prompt = (f"Act as a professional financial auditor for a luxury nursery. "
                      f"Analyze these expenses: Electricity {elec}, Food {food}, Gas {gas}, Staff {staff}. "
                      f"Provide a brief summary and 3 tips to reduce costs in English.")
            response = ai_model.generate_content(prompt)
            st.info(response.text)

except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.info("Ensure your Google Sheet headers match: Nom, Prénom, Age, Papa, Maman, Tel, Date_Paiement, Montant, Statut")
