import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse

# 1. ELITE UI CONFIG (Hiding Streamlit Branding)
st.set_page_config(page_title="AI Website Closer Pro", page_icon="💎", layout="wide")
st.markdown('<style>#MainMenu, footer, header {visibility: hidden; display: none !important;} .viewerBadge_79elG {display: none !important;}</style>', unsafe_allow_html=True)

# --- 2. THE SECRET SAFE (Zero Hardcoded Keys) ---
try:
    USER_DATABASE = {
        st.secrets["AHMAD_KEY"]: "Ahmad - CEO",
        st.secrets["PRO_USER_KEY"]: "Enterprise Partner"
    }
    REAL_API_KEY = st.secrets["SERPAPI_KEY"]
except Exception as e:
    st.error("Security Error: Secrets not found in Streamlit Dashboard. Please check your 'Secrets' settings.")
    st.stop()

HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"
PREVIEW_TEMPLATE = "https://demo.athemes.com/sydney/"

# --- 3. LOGIN SYSTEM ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>💎 AI Website Closer Pro</h1><p>Enterprise Lead Acquisition & ROI Closing Engine</p></div>", unsafe_allow_html=True)
    key = st.text_input("Enter License Key", type="password").strip()
    if st.button("Unlock Dashboard"):
        if key in USER_DATABASE:
            st.session_state["auth"] = True
            st.session_state["user"] = USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Key Invalid.")
else:
    # --- 4. THE COMMANDER DASHBOARD ---
    with st.sidebar:
        st.markdown(f"### 🛡️ Welcome, {st.session_state['user']}")
        my_agency = st.text_input("My Agency Name", "Senior Web Partner")
        if st.button("Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.markdown("## 🎯 Targeting Businesses with NO Website")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry", placeholder="e.g. Lawyers, Roofers...")
    with c2: city = st.text_input("Location", placeholder="e.g. London, Miami...")

    if st.button("🚀 EXECUTE SEARCH"):
        if niche and city:
            with st.spinner("Accessing High-Frequency Database..."):
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY}
                    data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                    leads = [l for l in data if not l.get("website")]
                    
                    if leads:
                        st.success(f"Success. Found {len(leads)} Prospects with NO website!")
                        # Data Export
                        csv = pd.DataFrame(leads)[['title', 'phone', 'address']].to_csv(index=False).encode('utf-8')
                        st.download_button("📥 Export Prospect List (CSV)", data=csv, file_name=f"{niche}_leads.csv")
                        
                        for i, lead in enumerate(leads):
                            name = lead.get("title")
                            with st.expander(f"🔥 OPPORTUNITY: {name}"):
                                col1, col2 = st.columns([1, 1.2])
                                with col1:
                                    pitch = f"Hi {name} Team, I noticed you have an impressive reputation but no website link on Google. This is costing you revenue. I can build you a professional Hostinger site today: {HOSTINGER_LINK}"
                                    st.text_area("Live Pitch Script", pitch, height=180, key=f"p_{i}")
                                    subj = urllib.parse.quote(f"Proposal for {name}")
                                    st.markdown(f'<a href="mailto:?subject={subj}&body={urllib.parse.quote(pitch)}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:700;">📧 Reach Out via Email</div></a>', unsafe_allow_html=True)
                                with col2:
                                    st.components.v1.iframe(PREVIEW_TEMPLATE, height=400, scrolling=True)
                    else: st.info("No businesses without websites found.")
                except: st.error("Connection busy. Try again.")
