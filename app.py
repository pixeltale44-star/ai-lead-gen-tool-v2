import streamlit as st
import pandas as pd
import requests

# 1. Page Config (MUST BE FIRST)
st.set_page_config(page_title="AI Lead Gen PRO", layout="wide")

# 2. DEFINITIVE KEYS (NO SPACES, ALL LOWERCASE)
USER_DATABASE = {
    "ahmad123": "Ahmad",
    "pro_user_2026": "Premium Subscriber",
    "memuna123": "Master Admin"
}

# 3. GLOBAL CONFIG
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
AFFILIATE_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# 4. LOGIN SYSTEM
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.title("🛡️ Pro SaaS Login")
    # .strip() handles accidental spaces at the end
    user_key = st.text_input("Enter License Key", type="password").strip()
    
    if st.button("Access Dashboard"):
        if user_key in USER_DATABASE:
            st.session_state["logged_in"] = True
            st.session_state["user_name"] = USER_DATABASE[user_key]
            st.rerun() # Refresh to show the dashboard
        else:
            st.error(f"Invalid Key. You entered: '{user_key}'")
else:
    # 5. THE MAIN APP
    st.title(f"🚀 Welcome, {st.session_state['user_name']}")
    
    with st.sidebar:
        st.header("Control Panel")
        my_name = st.text_input("Your Agency Name", "Expert")
        if st.button("Log Out"):
            st.session_state["logged_in"] = False
            st.rerun()

    niche = st.text_input("Niche (e.g. Dentists)")
    city = st.text_input("City (e.g. New York)")

    if st.button("🔥 Scan for Leads"):
        if niche and city:
            with st.spinner("Searching Google Maps..."):
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY}
                    response = requests.get("https://serpapi.com/search", params=params)
                    leads = response.json().get("local_results", [])
                    
                    if leads:
                        st.success(f"Found {len(leads)} Opportunities!")
                        for i, lead in enumerate(leads):
                            name = lead.get("title")
                            site = lead.get("website")
                            with st.expander(f"Lead: {name}"):
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.subheader("✉️ AI Pitch")
                                    if not site:
                                        msg = f"Hi {name}, I noticed you're missing a site. I can build one on Hostinger: {AFFILIATE_LINK}"
                                    else:
                                        msg = f"Hi {name}, your site at {site} needs a speed boost on Hostinger: {AFFILIATE_LINK}"
                                    st.text_area("Ready Pitch:", msg, height=150, key=f"p_{i}")
                                with col2:
                                    st.subheader("🌐 Preview")
                                    if site:
                                        st.components.v1.iframe(site, height=350)
                                    else:
                                        st.warning("No site found—High Value Opportunity!")
                except Exception as e:
                    st.error(f"Search failed. Please try again.")
        else:
            st.warning("Please fill in both fields.")
