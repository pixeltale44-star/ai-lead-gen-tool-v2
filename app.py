import streamlit as st
import pandas as pd
import requests

# --- REAL AI LEAD GEN LOGIC ---
class AILeadGenTool:
    def __init__(self, location, niche, api_key=None):
        self.location = location
        self.niche = niche
        self.api_key = api_key
        self.leads = []

    def scrape_leads(self):
        if self.api_key and len(self.api_key) > 5:
            # REAL DATA MODE - Connecting to SerpApi
            try:
                params = {
                    "engine": "google_maps",
                    "q": f"{self.niche} in {self.location}",
                    "api_key": self.api_key,
                    "type": "search"
                }
                response = requests.get("https://serpapi.com/search", params=params)
                data = response.json()
                results = data.get("local_results", [])
                
                if not results and "error" in data:
                    st.error(f"SerpApi Error: {data['error']}")
                    return

                self.leads = []
                for res in results:
                    self.leads.append({
                        "name": res.get("title", "Unknown"),
                        "rating": res.get("rating", 0),
                        "reviews": res.get("reviews", 0),
                        "website": res.get("website"),
                        "phone": res.get("phone")
                    })
            except Exception as e:
                st.error(f"Connection Error: {str(e)}")
        else:
            # DEMO MODE
            self.leads = [
                {"name": "Demo: Quick Fix Plumbers", "rating": 4.2, "reviews": 15, "website": None},
                {"name": "Demo: Slow Site Expert", "rating": 3.5, "reviews": 5, "website": "http://slow.com"}
            ]

    def analyze_leads(self):
        return [l for l in self.leads if not l.get("website") or "slow" in str(l.get("website"))]

    def generate_pitch(self, lead, your_name):
        name = lead["name"]
        if not lead.get("website"):
            offer = "I noticed you don't have a website link on Google. I can build you a professional Hostinger site in 48 hours."
        else:
            offer = "I noticed your website could be faster. Moving to Hostinger's AI hosting will boost your local ranking."
        return f"Hi {name} Team,\n\n{offer}\n\nBest, {your_name}"

# --- APP INTERFACE ---
st.set_page_config(page_title="AI Lead Gen", layout="wide")
st.title("🚀 Real-Time AI Lead Gen")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("SerpApi Key", type="password")
    your_name = st.text_input("Your Agency Name", "AI Solutions")

niche = st.text_input("Niche (e.g. Plumbers)")
location = st.text_input("City (e.g. Austin, TX)")

if st.button("🔍 Find Real Leads"):
    if niche and location:
        with st.spinner("Searching Google Maps..."):
            tool = AILeadGenTool(location, niche, api_key)
            tool.scrape_leads()
            leads = tool.analyze_leads()
            if leads:
                st.success(f"Found {len(leads)} Opportunities!")
                for i, lead in enumerate(leads):
                    with st.expander(f"Lead: {lead['name']}"):
                        st.write(f"Website: {lead.get('website', 'NONE')}")
                        pitch = tool.generate_pitch(lead, your_name)
                        st.text_area("Pitch:", pitch, height=150, key=f"p_{i}")
            else:
                st.info("No leads matching criteria found.")
    else:
        st.warning("Enter Niche and City.")
