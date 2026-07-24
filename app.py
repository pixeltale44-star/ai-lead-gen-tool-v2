import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION (YOUR PRIVATE DETAILS) ---
REAL_API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- SUBSCRIPTION GATE ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "pro_user_2026": # YOUR CUSTOMER PASSWORD
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Pro Lead Gen Login")
        st.text_input("Enter Access Key", type="password", on_change=password_entered, key="password")
        st.info("Contact the owner to purchase a subscription.")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Access Key", type="password", on_change=password_entered, key="password")
        st.error("😕 Access Key incorrect.")
        return False
    else:
        return True

# --- LOGIC ---
class AILeadGenTool:
    def __init__(self, location, niche):
        self.location = location
        self.niche = niche
        self.leads = []

    def scrape_leads(self):
        try:
            params = {"engine": "google_maps", "q": f"{self.niche} in {self.location}", "api_key": REAL_API_KEY, "type": "search"}
            response = requests.get("https://serpapi.com/search", params=params)
            results = response.json().get("local_results", [])
            self.leads = [{"name": res.get("title"), "rating": res.get("rating", 0), "website": res.get("website"), "phone": res.get("phone")} for res in results]
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- APP ---
if check_password():
    st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")
    st.title("🚀 AI Lead Gen Pro Dashboard")
    agent_name = st.sidebar.text_input("Your Name", "Pro Consultant")
    
    niche = st.text_input("Niche (e.g. Dentists)")
    location = st.text_input("City (e.g. New York)")

    if st.button("🔥 Generate Paid Leads"):
        tool = AILeadGenTool(location, niche)
        tool.scrape_leads()
        leads = [l for l in tool.leads if not l.get("website")]
        if leads:
            st.success(f"Found {len(leads)} Opportunities")
            for i, lead in enumerate(leads):
                with st.expander(f"Lead: {lead['name']}"):
                    pitch = f"Hi {lead['name']} Team, I noticed you don't have a website on Google. I can build you one on Hostinger in 48 hours. Register here: {HOSTINGER_AFFILIATE}\n\nBest, {agent_name}"
                    st.text_area("Pitch:", pitch, height=150, key=f"p_{i}")
        else:
            st.info("No leads found.")
