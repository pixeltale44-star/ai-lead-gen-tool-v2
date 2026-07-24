import streamlit as st
import pandas as pd
import requests

# 1. ELITE UI CONFIG
st.set_page_config(page_title="AI SALES WAR-ROOM PRO", layout="wide")

# --- 2. VIBRANT LIGHT BACKGROUND & DARK CARDS THEME ---
st.markdown("""
    <style>
    /* Vibrant Light Background */
    .stApp {
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
        background-attachment: fixed;
    }
    
    /* Deep Dark Intelligence Cards */
    div[data-testid="stExpander"] {
        background: #1a202c !important;
        border: 2px solid #2d3748 !important;
        border-radius: 12px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
        margin-bottom: 1.5rem !important;
        color: white !important;
    }
    
    /* White Input Boxes for Contrast */
    .stTextInput>div>div>input, .stNumberInput>div>div>input {
        background-color: white !important;
        color: #1a202c !important;
        border: 1px solid #cbd5e0 !important;
    }

    /* Buttons */
    .stButton>button {
        background: #2b6cb0;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background: #2c5282;
        transform: translateY(-1px);
    }

    /* Text Colors */
    h1, h2, h3 { color: #2d3748 !important; }
    p, label { color: #4a5568 !important; font-weight: 500; }
    
    /* Opportunity Badges */
    .badge-aplus { background: #c53030; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
    .badge-a { background: #2b6cb0; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCESS KEYS ---
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
    st.markdown("<p style='text-align:center;'>Elite Client Acquisition Engine</p>", unsafe_allow_html=True)
    with st.container():
        key = st.text_input("Enter Private License Key", type="password").strip()
        if st.button("Unlock Dashboard"):
            if key in USER_DATABASE:
                st.session_state["authenticated"] = True
                st.session_state["user_info"] = USER_DATABASE[key]
                st.rerun()
            else: st.error("Access Denied.")
else:
    # --- 5. THE DASHBOARD ---
    st.title(f"🎖️ Commander: {st.session_state['user_info']}")
    
    with st.sidebar:
        st.markdown("### 🛠️ TOOLS")
        my_name = st.text_input("Identity", "Senior AI Partner")
        avg_order = st.number_input("Prospect Avg Sale ($)", 100, 5000, 500)
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

    # Inputs on Vibrant Background
    st.markdown("### 📡 Deep-Scan Targets")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. Luxury Hotels")
    with c2: location = st.text_input("Target City", placeholder="e.g. Dubai")

    if st.button("🚀 INITIATE GLOBAL SCAN"):
        if niche and location:
            with st.spinner("Analyzing Market Intelligence..."):
                try:
                    params = {"engine": "google_maps", "q": f"{niche} in {location}", "api_key": API_KEY}
                    results = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                    
                    if results:
                        st.success(f"Scan Successful. {len(results)} Opportunities Found.")
                        for i, lead in enumerate(results):
                            name, site, rating = lead.get("title"), lead.get("website"), lead.get("rating", 0)
                            
                            # LOGIC: SCORE THE OPPORTUNITY
                            score, badge_class = ("A+", "badge-aplus") if not site else ("A", "badge-a")

                            # DARK LEAD CARD
                            with st.expander(f"Opportunity: {name}"):
                                st.markdown(f"**Score:** <span class='{badge_class}'>{score}</span> | **Rating:** {rating}⭐", unsafe_allow_html=True)
                                col_left, col_right = st.columns([1, 1.2])
                                
                                with col_left:
                                    st.markdown("<h4 style='color:#58a6ff;'>🧠 Strategy</h4>", unsafe_allow_html=True)
                                    if not site:
                                        loss = avg_order * 10
                                        st.error(f"FATAL: Missing Website.")
                                        st.markdown(f"**Est. Revenue Loss: ${loss:,}/mo**")
                                        pitch = f"Hi {name}, I'm an AI Partner in {location}. You have a {rating} rating but no website. You are losing approx ${loss:,} monthly. I can build a Hostinger site for you today: {HOSTINGER_AFFILIATE}"
                                    else:
                                        st.info("STATUS: Weak Infrastructure detected.")
                                        pitch = f"Hi {name}, your {rating}-star rating is great, but your site is slow. Moving to Hostinger's AI hosting will boost your rank. Link: {HOSTINGER_AFFILIATE}"
                                    
                                    st.text_area("Copy Pitch:", pitch, height=180, key=f"p_{i}")

                                with col_right:
                                    st.markdown("<h4 style='color:#58a6ff;'>👁️ Preview</h4>", unsafe_allow_html=True)
                                    if site:
                                        st.components.v1.iframe(site, height=400, scrolling=True)
                                    else:
                                        st.markdown(f'<div style="height:400px; display:flex; align-items:center; justify-content:center; background:#2d3748; border:2px dashed #4a5568; border-radius:8px; color:white;"><div><h2 style="text-align:center;">🚫 NO SITE</h2><p style="text-align:center;">Ideal for Website Build Sale.</p></div></div>', unsafe_allow_html=True)
                except: st.error("Scan Failed. Try again.")
        else: st.warning("Enter Niche and City.")
