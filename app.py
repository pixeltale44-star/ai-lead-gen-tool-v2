import streamlit as st
import pandas as pd
import requests
import time

# 1. BRANDED PAGE CONFIG (Controls Tab Title & Icon)
st.set_page_config(
    page_title="AI SALES WAR-ROOM PRO", 
    page_icon="💎", 
    layout="wide"
)

# --- 2. STEALTH & BRAND THEME ---
st.markdown("""
    <style>
    /* Hides Streamlit Branding */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Vibrant Background & Dark Target Cards */
    .stApp { 
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); 
        background-attachment: fixed; 
    }
    div[data-testid="stExpander"] {
        background: #1a202c !important;
        border: 2px solid #2b6cb0 !important;
        border-radius: 12px !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    /* Branded Primary Buttons */
    .stButton>button { 
        background: #2b6cb0; 
        color: white; 
        border-radius: 8px; 
        font-weight: 600; 
        width: 100%; 
        border: none;
    }
    .badge-aplus { background: #c53030; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCESS DATABASE ---
USER_DATABASE = {
    "ahmad123": "Ahmad - CEO", 
    "pro_user_2026": "Enterprise Partner",
    "VIP_ACCESS": "Lifetime Member"
}

# --- 4. ENGINE KEYS ---
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align:center;'>💎 AI SALES WAR-ROOM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Elite Lead Acquisition & ROI Closing Engine</p>", unsafe_allow_html=True)
    key = st.text_input("Enter Private License Key", type="password").strip()
    if st.button("Unlock Enterprise Dashboard"):
        if key in USER_DATABASE:
            st.session_state["authenticated"] = True
            st.session_state["user_info"] = USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Denied.")
else:
    # --- 5. THE COMMANDER DASHBOARD ---
    st.title(f"🎖️ Commander: {st.session_state['user_info']}")
    
    with st.sidebar:
        st.markdown("### ⚙️ DEEP-SCAN SETTINGS")
        lead_limit = st.slider("Leads to Fetch", 20, 100, 40, step=20)
        st.divider()
        my_name = st.text_input("Identity", "Senior AI Partner")
        avg_order = st.number_input("Prospect Avg Sale ($)", 100, 5000, 500)
        if st.button("End Session"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.markdown("### 📡 Initiate Global Intelligence Scan")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. Roofers")
    with c2: location = st.text_input("Target City", placeholder="e.g. Dubai")

    if st.button("🚀 EXECUTE GLOBAL SEARCH"):
        if niche and location:
            all_leads = []
            progress = st.progress(0)
            status = st.empty()
            
            for offset in range(0, lead_limit, 20):
                status.text(f"Scanning Database Page {offset//20 + 1}...")
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {location}", "api_key": API_KEY, "start": offset}
                    page = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                    if not page: break
                    all_leads.extend(page)
                    progress.progress(min((offset + 20) / lead_limit, 1.0))
                    time.sleep(0.4)
                except: break
            
            st.success(f"Scan Successful. Found {len(all_leads)} leads.")
            
            for i, lead in enumerate(all_leads):
                name, site, rating = lead.get("title"), lead.get("website"), lead.get("rating", 0)
                score, badge = ("A+", "badge-aplus") if not site else ("B", "")

                with st.expander(f"[{score}] TARGET: {name}"):
                    cl, cr = st.columns([1, 1.2])
                    with cl:
                        st.markdown("<h4 style='color:#58a6ff;'>🧠 AI Intelligence</h4>", unsafe_allow_html=True)
                        if not site:
                            loss = avg_order * 12
                            st.error("STATUS: No Website Detected.")
                            st.markdown(f"**Potential Annual Loss: ${loss:,}**")
                            pitch = f"Hi {name}, I noticed your {rating} rating on Google but you have NO website. You are losing about ${loss:,}/year. I can build a Hostinger site for you today: {HOSTINGER_AFFILIATE}"
                        else:
                            st.info("STATUS: Website Live (Weak Infrastructure).")
                            pitch = f"Hi {name}, your website needs an AI speed boost. Move to Hostinger's backbone here: {HOSTINGER_AFFILIATE}"
                        st.text_area("Pitch Script:", pitch, height=150, key=f"p_{i}")
                    with cr:
                        st.markdown("<h4 style='color:#58a6ff;'>👁️ Visual Preview</h4>", unsafe_allow_html=True)
                        if site: st.components.v1.iframe(site, height=350)
                        else: st.markdown(f'<div style="height:350px; display:flex; align-items:center; justify-content:center; background:#1a202c; border:2px dashed #4a5568; border-radius:8px; color:white; text-align:center;"><div><h2>🚫 MISSING SITE</h2><p>High Probability Conversion</p></div></div>', unsafe_allow_html=True)
        else:
            st.warning("Enter Niche and City.")
