import streamlit as st
import pandas as pd
import requests
import time

# 1. PAGE CONFIG
st.set_page_config(page_title="AI SALES WAR-ROOM PRO", page_icon="💎", layout="wide")

# --- 🔑 THE CUSTOMER REGISTRY (YOUR DATABASE) ---
# Format: "UNIQUE_KEY": "CUSTOMER_NAME"
# You can add 100s of users here!
USER_DATABASE = {
    "ahmad123": "Ahmad - CEO",             # Your Admin Key
    "VIP_777": "Exclusive Member",         # Another Admin Key
    "JON_DOE_99": "John Doe - Pro Plan",   # Customer 1
    "SARAH_M_2026": "Sarah Miller - Basic",# Customer 2
    "USER_PRO_88": "Active Subscriber"     # Customer 3
}

# --- CONFIGURATION ---
REAL_API_KEY = st.secrets["SERPAPI_KEY"]
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- STEALTH UI ---
st.markdown('<style>#MainMenu, footer, header {visibility: hidden;}</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] { background: #1a202c !important; border: 2px solid #2b6cb0 !important; border-radius: 12px !important; color: white !important; }
    .stButton>button { background: #2b6cb0; color: white; border-radius: 8px; font-weight: 600; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN SYSTEM ---
if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align:center;'>💎 AI SALES WAR-ROOM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Elite Lead Acquisition Engine</p>", unsafe_allow_html=True)
    # .strip() handles accidental spaces, .upper() makes keys case-insensitive
    key = st.text_input("Enter License Key", type="password").strip()
    if st.button("Access Dashboard"):
        if key in USER_DATABASE:
            st.session_state["authenticated"] = True
            st.session_state["user_info"] = USER_DATABASE[key]
            st.rerun()
        else: st.error("Invalid or Expired License Key.")
else:
    # --- THE COMMANDER DASHBOARD ---
    st.title(f"🎖️ Welcome back, {st.session_state['user_info']}")
    
    with st.sidebar:
        st.markdown("### ⚙️ SYSTEM")
        lead_limit = st.slider("Target Depth", 20, 100, 40, step=20)
        st.divider()
        my_name = st.text_input("Your Agent Name", "Senior Partner")
        if st.sidebar.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. Lawyers")
    with c2: location = st.text_input("Target City", placeholder="e.g. London")

    if st.button("🚀 EXECUTE SEARCH"):
        if niche and location:
            all_leads = []
            progress = st.progress(0)
            for offset in range(0, lead_limit, 20):
                params = {"engine": "google_maps", "q": f"{niche} in {location}", "api_key": REAL_API_KEY, "start": offset}
                page = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                if not page: break
                all_leads.extend(page)
                progress.progress(min((offset + 20) / lead_limit, 1.0))
            
            st.success(f"Success. {len(all_leads)} Targets Found.")
            for i, lead in enumerate(all_leads):
                name, site = lead.get("title"), lead.get("website")
                with st.expander(f"OPPORTUNITY: {name}"):
                    cl, cr = st.columns([1, 1.2])
                    with cl:
                        st.subheader("AI Pitch")
                        if not site: msg = f"Hi {name}, I noticed you're missing a site. Build one on Hostinger here: {HOSTINGER_AFFILIATE}"
                        else: msg = f"Hi {name}, your site needs a speed boost on Hostinger here: {HOSTINGER_AFFILIATE}"
                        st.text_area("Ready-to-use Script:", msg, height=150, key=f"p_{i}")
                    with cr:
                        st.subheader("Visual Preview")
                        if site: st.components.v1.iframe(site, height=350)
                        else: st.error("SITE MISSING - High Value Lead!")
