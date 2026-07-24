import streamlit as st
import pandas as pd
import requests

# --- 🔑 CUSTOMER DATABASE (YOUR REVENUE CENTER) ---
# Add your customers here. Format: "AccessKey": "Customer Name/Plan"
USER_DATABASE = {
    "admin123": "Master Admin",        # Your personal key
    "user_alex_pro": "Alex - Pro Plan", # Customer 1
    "user_sarah_basic": "Sarah - Basic", # Customer 2
}

# --- CONFIGURATION ---
REAL_API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- SUBSCRIPTION GATE ---
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🛡️ Partner Portal Login")
        access_key = st.text_input("Enter your unique License Key", type="password")
        if st.button("Login"):
            if access_key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[access_key]
                st.rerun()
            else:
                st.error("Invalid License Key. Contact support to renew.")
        return False
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
            self.leads = response.json().get("local_results", [])
        except Exception as e:
            st.error(f"Search temporary unavailable.")

# --- APP ---
if check_password():
    st.set_page_config(page_title="LeadGen SaaS PRO", layout="wide")
    
    # Dashboard Header
    st.title(f"🚀 Welcome, {st.session_state['user_info']}")
    st.sidebar.success(f"License: ACTIVE")
    
    if st.sidebar.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

    niche = st.text_input("Industry (e.g. Roofers)")
    location = st.text_input("City (e.g. London)")

    if st.button("🔥 Scan for Leads"):
        tool = AILeadGenTool(location, niche)
        tool.scrape_leads()
        
        if tool.leads:
            for i, lead in enumerate(tool.leads):
                site_url = lead.get("website")
                name = lead.get("title")
                
                with st.expander(f"Opportunity: {name}"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.subheader("AI Pitch")
                        pitch = f"Hi {name}, I noticed your Google ranking. I can build you a better site on Hostinger here: {HOSTINGER_AFFILIATE}"
                        st.text_area("Copy Pitch:", pitch, height=150, key=f"p_{i}")
                    with c2:
                        st.subheader("Site Preview")
                        if site_url:
                            st.components.v1.iframe(site_url, height=300)
                        else:
                            st.warning("No website found—Perfect for a new sale!")
