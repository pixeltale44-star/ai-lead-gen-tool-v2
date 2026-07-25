import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse

# 1. ENTERPRISE CONFIG
st.set_page_config(page_title="WebDev Intelligence Pro", page_icon="🚀", layout="wide")

# --- 2. SUPER-STEALTH CSS (Hides ALL Streamlit Branding) ---
st.markdown("""
    <style>
    /* Hides Top Bar, Menu, and Footer */
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    
    /* Hides the 'Manage app' button and floating badges */
    .viewerBadge_79elG, .stDeployButton, div[data-testid="stStatusWidget"] {
        display: none !important;
        visibility: hidden !important;
    }
    
    /* Vibrant Professional Background */
    .stApp { 
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); 
        background-attachment: fixed; 
    }
    
    /* Deep Charcoal Prospect Cards */
    div[data-testid="stExpander"] {
        background: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Force Light Text inside Dark Cards */
    div[data-testid="stExpander"] * { color: #f8fafc !important; }
    
    /* Professional Header & Labels */
    h1, h2, h3 { color: #0f172a !important; font-weight: 700; }
    p, label { color: #334155 !important; font-weight: 600; }

    /* Premium Action Buttons */
    .stButton>button {
        background: #2563eb;
        color: white !important;
        border-radius: 8px;
        font-weight: 700;
        border: none;
        height: 50px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE REVENUE DATABASE ---
USER_DATABASE = {
    "ahmad123": "Ahmad - Global Director",
    "pro_user_2026": "Enterprise Partner",
    "MEMUNA_VIP": "Master Admin"
}

# --- 4. ENGINE KEYS & LINKS ---
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

if "auth" not in st.session_state: st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:80px;'>", unsafe_allow_html=True)
    st.markdown("<h1>🚀 WebDev Intelligence Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p>Exclusive Access for High-Ticket Web Development Partners</p>", unsafe_allow_html=True)
    key = st.text_input("License Key", type="password", placeholder="Enter your key...").strip()
    if st.button("Unlock Prospect Database"):
        if key in USER_DATABASE:
            st.session_state["auth"] = True
            st.session_state["user"] = USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Key Invalid.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- 5. THE PROSPECTOR DASHBOARD ---
    with st.sidebar:
        st.markdown(f"### 🛡️ Welcome, {st.session_state['user']}")
        my_agency = st.text_input("Agency Identity", "Senior Web Partner")
        limit = st.select_slider("Lead Batch Size", options=[20, 40, 60, 100], value=20)
        if st.button("Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.markdown("## 🎯 New Prospect Acquisition")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry", placeholder="Enter niche...")
    with c2: city = st.text_input("City", placeholder="Enter location...")

    if st.button("🚀 INITIATE GLOBAL LEAD SCAN"):
        if niche and city:
            leads = []
            with st.spinner("Accessing Real-Time Maps Data..."):
                try:
                    for start in range(0, limit, 20):
                        params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY, "start": start}
                        data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                        if not data: break
                        leads.extend(data)
                except: st.error("Connection busy. Try again.")
            
            if leads:
                st.success(f"Scanning Complete. {len(leads)} Prospects Identified.")
                for i, lead in enumerate(leads):
                    name, site = lead.get("title"), lead.get("website")
                    rating = lead.get("rating", 0)
                    
                    with st.expander(f"{'⚠️ SITE MISSING' if not site else '🌐 SITE DETECTED'} | {name}"):
                        l_col, r_col = st.columns([1, 1.2])
                        with l_col:
                            st.markdown("### 🧠 Intelligence")
                            if not site:
                                pitch = f"Hi {name} Team, I noticed your {rating}-star rating but no website. I can build you an elite AI site on Hostinger in 48 hours. Link: {HOSTINGER_LINK}"
                            else:
                                pitch = f"Hi {name} Team, your site at {site} needs an upgrade. Moving to Hostinger AI will boost your rank. Link: {HOSTINGER_LINK}"
                            st.text_area("Pitch Script", pitch, height=180, key=f"pitch_{i}")
                            
                            subj = urllib.parse.quote(f"Revenue Growth for {name}")
                            body = urllib.parse.quote(pitch)
                            st.markdown(f'<a href="mailto:?subject={subj}&body={body}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:700;">📧 Reach Out to Lead</div></a>', unsafe_allow_html=True)

                        with r_col:
                            st.markdown("### 👁️ Live Preview")
                            if site: st.components.v1.iframe(site, height=400, scrolling=True)
                            else: st.warning("No website found—High Priority Lead!")
        else: st.warning("Enter Niche and City.")
