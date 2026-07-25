import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse

# 1. ENTERPRISE CONFIG (TAB TITLE & ICON)
st.set_page_config(page_title="WebDev Intelligence Pro", page_icon="🚀", layout="wide")

# --- 2. ELITE UI THEME (Vibrant Background + Dark Prospect Cards) ---
st.markdown("""
    <style>
    /* Total Stealth Mode */
    #MainMenu, footer, header {visibility: hidden;}
    
    /* Vibrant Professional Background */
    .stApp { 
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); 
        background-attachment: fixed; 
    }
    
    /* Deep Charcoal Prospect Cards (High Visibility) */
    div[data-testid="stExpander"] {
        background: #1e293b !important;
        border: 2px solid #334155 !important;
        border-radius: 12px !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3) !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* Force Light Text inside Dark Cards */
    div[data-testid="stExpander"] * {
        color: #f8fafc !important;
    }
    
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
        transition: 0.3s;
    }
    .stButton>button:hover { background: #1d4ed8; transform: scale(1.02); }
    
    /* AI Report Style */
    .report-box { background: #334155; padding: 15px; border-radius: 8px; border-left: 5px solid #2563eb; }
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
        st.success("Connection: SECURE")
        my_agency = st.text_input("Agency Identity", "Senior Web Partner")
        limit = st.select_slider("Lead Batch Size", options=[20, 40, 60, 100], value=20)
        if st.button("Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.markdown("## 🎯 New Prospect Acquisition")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry (e.g. Lawyers, Roofers)", placeholder="Enter niche...")
    with c2: city = st.text_input("City (e.g. New York, London)", placeholder="Enter location...")

    if st.button("🚀 INITIATE GLOBAL LEAD SCAN"):
        if niche and city:
            leads = []
            with st.spinner("Accessing Real-Time Maps Data..."):
                for start in range(0, limit, 20):
                    params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY, "start": start}
                    data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                    if not data: break
                    leads.extend(data)
            
            st.success(f"Scanning Complete. {len(leads)} Prospects Identified.")
            
            for i, lead in enumerate(leads):
                name, site, phone = lead.get("title"), lead.get("website"), lead.get("phone", "N/A")
                rating = lead.get("rating", 0)
                
                # DARK PROSPECT CARD
                with st.expander(f"{'⚠️ SITE MISSING' if not site else '🌐 SITE DETECTED'} | {name}"):
                    l_col, r_col = st.columns([1, 1.2])
                    
                    with l_col:
                        st.markdown("### 🧠 Prospect Intelligence")
                        if not site:
                            status_label = "🔥 HIGH VALUE: Business is invisible online."
                            pitch = f"Hi {name} Team,\n\nI was researching {niche} in {city} and noticed your business has a {rating}-star rating but no active website link. This is a massive 'hidden' loss for your brand. I can build you an elite, AI-powered site on Hostinger in 48 hours.\n\nRegister your hosting here to start: {HOSTINGER_LINK}\n\nBest, {my_agency}"
                        else:
                            status_label = "💡 OPPORTUNITY: Site lacks speed optimization."
                            pitch = f"Hi {name} Team,\n\nI checked your site at {site}. Your {rating}-star reputation deserves a faster engine. Moving to Hostinger's AI hosting will boost your Google rank instantly.\n\nStart here: {HOSTINGER_LINK}\n\nBest, {my_agency}"
                        
                        st.markdown(f"<div class='report-box'>{status_label}</div>", unsafe_allow_html=True)
                        st.text_area("Live AI Pitch Script", pitch, height=180, key=f"pitch_{i}")
                        
                        # DRAFT EMAIL BUTTON
                        subject = urllib.parse.quote(f"Boosting {name}'s Revenue")
                        body = urllib.parse.quote(pitch)
                        mailto = f"mailto:?subject={subject}&body={body}"
                        st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:700;">📧 Reach Out to Lead</div></a>', unsafe_allow_html=True)
                        st.write(f"📞 Contact: {phone}")

                    with r_col:
                        st.markdown("### 👁️ Live Preview")
                        if site:
                            st.components.v1.iframe(site, height=450, scrolling=True)
                        else:
                            st.markdown(f'<div style="height:450px; display:flex; align-items:center; justify-content:center; background:#0f172a; border:2px dashed #334155; border-radius:12px; text-align:center; padding:20px; color:white;"><div><h2 style="color:#64748b;">🚫 NO FOOTPRINT</h2><p style="color:#64748b;">This prospect has no active website.<br>Click the email button to close the deal.</p></div></div>', unsafe_allow_html=True)
        else:
            st.warning("Please provide both Niche and City.")
