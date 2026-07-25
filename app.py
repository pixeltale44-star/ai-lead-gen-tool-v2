import streamlit as st
import pandas as pd
import requests
import urllib.parse

# 1. PAGE SETUP
st.set_page_config(page_title="AI Website Visionary", page_icon="🎯", layout="wide")

# --- 2. ELITE WHITE-LABEL CSS ---
st.markdown('<style>#MainMenu, footer, header {visibility: hidden;} .viewerBadge_79elG {display: none !important;}</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] { background: #0f172a !important; border-radius: 15px !important; box-shadow: 0 10px 15px rgba(0,0,0,0.3) !important; color: white !important; }
    div[data-testid="stExpander"] * { color: #f1f5f9 !important; }
    .stButton>button { background: #2563eb; color: white !important; border-radius: 10px; font-weight: 700; height: 50px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. THE SAFE (Secrets) ---
try:
    REAL_API_KEY = st.secrets["SERPAPI_KEY"]
    USER_DB = {st.secrets["AHMAD_KEY"]: "Ahmad (Director)", st.secrets["PRO_USER_KEY"]: "Elite Partner"}
except:
    st.error("Setup Error: Please enter your keys in the Streamlit Secrets box.")
    st.stop()

HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"
# A high-end, responsive business template that allows embedding
DEMO_SITE = "https://demo.athemes.com/sydney/"

# --- 4. LOGIN ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>🎯 AI Website Visionary</h1><p>Solving the 'Invisible Business' Problem with AI</p></div>", unsafe_allow_html=True)
    key = st.text_input("Enter Private License Key", type="password").strip()
    if st.button("Unlock Closer Dashboard"):
        if key in USER_DB:
            st.session_state["auth"], st.session_state["user"] = True, USER_DB[key]
            st.rerun()
        else: st.error("Access Denied.")
else:
    # --- 5. THE DASHBOARD ---
    st.sidebar.markdown(f"### 👤 {st.session_state['user']}")
    if st.sidebar.button("Logout"): st.session_state["auth"] = False; st.rerun()
    
    st.title("🎯 Identify & Close Ghost Businesses")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Business Industry", placeholder="e.g. Plumbers")
    with c2: city = st.text_input("Location", placeholder="e.g. London")

    if st.button("🚀 SCAN FOR NO-WEBSITE OPPORTUNITIES"):
        if niche and city:
            with st.spinner("Analyzing Google Maps Database..."):
                p = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY}
                data = requests.get("https://serpapi.com/search", params=p).json().get("local_results", [])
                leads = [l for l in data if not l.get("website")]
            
            if leads:
                st.success(f"Success! Found {len(leads)} Businesses without websites in {city}.")
                for i, lead in enumerate(leads):
                    name, rating = lead.get("title"), lead.get("rating", 0)
                    with st.expander(f"🔥 OPPORTUNITY: {name} ({rating}⭐)"):
                        col1, col2 = st.columns([1, 1.2])
                        with col1:
                            st.markdown("### 🧠 The Solution Pitch")
                            pitch = f"Hi {name} Team, I noticed your amazing {rating}-star reputation on Google. However, you don't have a website link. You are effectively 'invisible' to new customers. I've designed a proposed site for you (see right). We can launch this on Hostinger's AI engine today.\n\nStart here: {HOSTINGER_LINK}"
                            st.text_area("Pitch Script:", pitch, height=180, key=f"p_{i}")
                            
                            subj = urllib.parse.quote(f"Website Vision for {name}")
                            mailto = f"mailto:?subject={subj}&body={urllib.parse.quote(pitch)}"
                            st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:10px; border-radius:8px; text-align:center; font-weight:700;">📧 Send Vision to Owner</div></a>', unsafe_allow_html=True)
                            st.write(f"📞 Phone: {lead.get('phone', 'N/A')}")
                        with col2:
                            st.markdown("### 👁️ Your Proposed Design")
                            st.info("Record a Loom video showing them this professional design!")
                            st.components.v1.iframe(DEMO_SITE, height=450, scrolling=True)
            else: st.info("All businesses in this search already have websites. Try a different city!")
