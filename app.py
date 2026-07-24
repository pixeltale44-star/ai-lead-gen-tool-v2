import streamlit as st
import pandas as pd
import requests

# --- CONFIGURATION ---
REAL_API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- SUBSCRIPTION GATE ---
def check_password():
    def password_entered():
        if st.session_state["password"] == "pro_user_2026":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.title("🔒 Pro Lead Gen Login")
        st.text_input("Enter Access Key", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Enter Access Key", type="password", on_change=password_entered, key="password")
        st.error("😕 Access Key incorrect.")
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
            results = response.json().get("local_results", [])
            self.leads = results
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- APP ---
if check_password():
    st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")
    st.title("🚀 AI Lead Gen PRO (with Site Preview)")
    
    agent_name = st.sidebar.text_input("Your Name", "Pro Consultant")
    niche = st.text_input("Niche (e.g. Dentists)")
    location = st.text_input("City (e.g. New York)")

    if st.button("🔥 Generate Leads with Previews"):
        tool = AILeadGenTool(location, niche)
        tool.scrape_leads()
        
        if tool.leads:
            st.success(f"Found {len(tool.leads)} Leads")
            for i, lead in enumerate(tool.leads):
                site_url = lead.get("website")
                name = lead.get("title")
                
                with st.expander(f"🔍 PREVIEW: {name}"):
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("### AI Pitch")
                        if not site_url:
                            pitch = f"Hi {name} Team, I noticed you're missing a website on Google. I can build you one on Hostinger in 48 hours. Register here: {HOSTINGER_AFFILIATE}"
                        else:
                            pitch = f"Hi {name} Team, I saw your site at {site_url}. It needs a speed boost. Moving to Hostinger's AI hosting will help. Link: {HOSTINGER_AFFILIATE}"
                        st.text_area("Pitch:", pitch, height=150, key=f"p_{i}")
                        st.info(f"Phone: {lead.get('phone', 'N/A')}")
                    
                    with col2:
                        st.markdown("### Live Prospect Preview")
                        if site_url:
                            st.write(f"Displaying: {site_url}")
                            st.components.v1.iframe(site_url, height=400, scrolling=True)
                        else:
                            st.warning("No website found. Showing Google Maps position instead.")
                            # Fallback to showing their business name on a map-like frame
                            st.write(f"Target: {name}")
                            st.write(f"Address: {lead.get('address', 'Check Google Maps')}")
        else:
            st.info("No leads found. Check your API key or search terms.")
