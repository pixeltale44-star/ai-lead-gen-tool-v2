import streamlit as st
import pandas as pd
import requests

# 1. ELITE UI CONFIG
st.set_page_config(page_title="AI SALES WAR-ROOM PRO", layout="wide", initial_sidebar_state="expanded")

# --- 2. LUXURY THEMEING ---
st.markdown("""
    <style>
    .main { background: #0E1117; }
    .stApp { background-image: radial-gradient(circle at 2px 2px, #1d2129 1px, transparent 0); background-size: 40px 40px; }
    div[data-testid="stExpander"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; margin-bottom: 1rem; }
    .stButton>button { background: linear-gradient(90deg, #3E7096 0%, #6F8854 100%); color: white; border: none; font-weight: bold; border-radius: 5px; width: 100%; transition: 0.3s; }
    .stButton>button:hover { transform: scale(1.02); filter: brightness(1.2); }
    h1, h2, h3 { color: #58a6ff !important; font-family: 'Inter', sans-serif; }
    .metric-box { background: #161b22; padding: 20px; border-radius: 10px; border-top: 4px solid #3E7096; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ENTERPRISE ACCESS ---
USER_DATABASE = {
    "ahmad123": "Ahmad - CEO",
    "pro_user_2026": "Enterprise Partner",
    "VIP_ACCESS": "Lifetime Member"
}

# --- 4. ENGINE ---
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown("<h1 style='text-align:center;'>💎 AI SALES WAR-ROOM</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#8b949e;'>Enterprise Grade Lead Acquisition & Closing Engine</p>", unsafe_allow_html=True)
    with st.container():
        key = st.text_input("Enter License Key", type="password", help="Contact Ahmad for Private Access").strip()
        if st.button("Unlock Enterprise Access"):
            if key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[key]
                st.rerun()
            else: st.error("Access Denied.")
else:
    # --- 5. THE WAR-ROOM DASHBOARD ---
    st.title(f"🎖️ Global Commander: {st.session_state['user_info']}")
    
    with st.sidebar:
        st.markdown("### 🛠️ COMMAND CENTER")
        my_name = st.text_input("Consultant Identity", "Senior AI Partner")
        avg_order_value = st.number_input("Prospect Avg Order ($)", 100, 5000, 250)
        st.markdown("---")
        if st.button("End Session"):
            st.session_state["authenticated"] = False
            st.rerun()

    # Metrics Row
    m1, m2, m3 = st.columns(3)
    with m1: st.markdown(f'<div class="metric-box"><h3>Targeted</h3><p style="font-size:24px;">Global</p></div>', unsafe_allow_html=True)
    with m2: st.markdown(f'<div class="metric-box"><h3>Intelligence</h3><p style="font-size:24px;">Real-Time</p></div>', unsafe_allow_html=True)
    with m3: st.markdown(f'<div class="metric-box"><h3>Provider</h3><p style="font-size:24px;">Hostinger Pro</p></div>', unsafe_allow_html=True)

    st.markdown("### 📡 Deep-Scan Target Search")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. High-End Real Estate")
    with c2: location = st.text_input("Target Location", placeholder="e.g. Beverly Hills, CA")

    if st.button("🚀 INITIATE DEEP SCAN"):
        if niche and location:
            with st.spinner("Extracting hidden opportunities..."):
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {location}", "api_key": API_KEY}
                    results = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                    
                    if results:
                        st.success(f"Scanning Complete. {len(results)} Targets Identified.")
                        for i, lead in enumerate(results):
                            name, site, rating = lead.get("title"), lead.get("website"), lead.get("rating", 0)
                            
                            # LOGIC: SCORE THE OPPORTUNITY
                            score = "B"
                            if not site: score = "A+"
                            elif rating < 4.2: score = "A"

                            with st.expander(f"[{score}] TARGET: {name} | Rating: {rating}⭐"):
                                col_left, col_right = st.columns([1, 1.2])
                                
                                with col_left:
                                    st.markdown("#### 🧠 AI Opportunity Report")
                                    if not site:
                                        lost_revenue = avg_order_value * 12 # Estimated monthly loss
                                        st.error(f"FATAL ERROR: No Digital Presence found.")
                                        st.warning(f"ESTIMATED REVENUE LOSS: ${lost_revenue:,}/month")
                                        pitch = f"Hi {name}, I'm looking at your Beverly Hills listing. You have a {rating} rating but NO website. You are losing approx ${lost_revenue:,} every month to competitors. I can stop the bleed with a Hostinger Pro site today: {HOSTINGER_AFFILIATE}"
                                    else:
                                        st.info("STATUS: Weak Digital Presence. High Migration Probability.")
                                        pitch = f"Hi {name}, your {rating}-star rating is impressive, but your website is bottlenecking your growth. Moving to Hostinger's AI backbone will increase your Google Rank. Link: {HOSTINGER_AFFILIATE}"
                                    
                                    st.text_area("Elite Sales Pitch:", pitch, height=180, key=f"p_{i}")
                                    st.button(f"Copy Pitch for {name}", on_click=lambda: st.toast("Copied!"), key=f"c_{i}")

                                with col_right:
                                    st.markdown("#### 👁️ Target Visual Intelligence")
                                    if site:
                                        st.components.v1.iframe(site, height=450, scrolling=True)
                                    else:
                                        st.markdown(f'<div style="height:450px; display:flex; align-items:center; justify-content:center; background:#161b22; border:1px dashed #58a6ff; border-radius:8px;"><div><h2 style="text-align:center;">🚫 SITE MISSING</h2><p style="text-align:center;">Opportunity identified. Record Loom video now.</p></div></div>', unsafe_allow_html=True)
                except: st.error("Global Satellite connection timed out. Retry.")
        else: st.warning("Awaiting target coordinates (Niche + Location).")
