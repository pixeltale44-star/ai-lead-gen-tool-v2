import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse

# 1. ELITE UI CONFIG
st.set_page_config(page_title="AI Website Closer Pro", page_icon="🚀", layout="wide")

# --- 2. SUPER-STEALTH & ELITE UI THEME ---
st.markdown("""
    <style>
    /* Total White-Label Mode */
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    .viewerBadge_79elG, .stDeployButton, div[data-testid="stStatusWidget"] {display: none !important;}
    
    /* Vibrant Professional Background */
    .stApp { 
        background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); 
        background-attachment: fixed; 
    }
    
    /* Deep Charcoal Prospect Cards (High Contrast) */
    div[data-testid="stExpander"] {
        background: #0f172a !important;
        border: 1px solid #1e293b !important;
        border-radius: 16px !important;
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Force White Text inside Cards */
    div[data-testid="stExpander"] * { color: #f8fafc !important; }
    
    /* Professional Typography */
    h1, h2, h3 { color: #0f172a !important; font-weight: 800; }
    p, label { color: #1e293b !important; font-weight: 600; }

    /* Premium Blue Buttons */
    .stButton>button {
        background: #2563eb;
        color: white !important;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        height: 55px;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.4); }
    
    /* Info Box Styling */
    .vision-box { background: #1e293b; padding: 20px; border-radius: 12px; border-left: 6px solid #2563eb; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. REVENUE & LICENSE DATABASE ---
USER_DATABASE = {
    "ahmad123": "Ahmad - Executive Director",
    "pro_user_2026": "Premium Partner",
    "MEMUNA_VIP": "Master Admin"
}

# --- 4. ENGINE KEYS & GLOBAL VISION ---
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# This is a world-class business template used as the "Proposed Design"
PROPOSED_DESIGN_URL = "https://preview.themeforest.net/item/skylark-creative-one-page-business-template/full_screen_preview/21683050"

if "auth" not in st.session_state: st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'>", unsafe_allow_html=True)
    st.markdown("<h1>💎 AI Website Closer Pro</h1>", unsafe_allow_html=True)
    st.markdown("<p>Closing High-Ticket Web Clients with Instant Visual ROI</p>", unsafe_allow_html=True)
    key = st.text_input("License Key", type="password", placeholder="Enter your access key...").strip()
    if st.button("Unlock Closer Dashboard"):
        if key in USER_DATABASE:
            st.session_state["auth"] = True
            st.session_state["user"] = USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Key Invalid.")
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # --- 5. THE CLOSER DASHBOARD ---
    with st.sidebar:
        st.markdown(f"### 🛡️ Welcome, {st.session_state['user']}")
        st.success("Mode: AGGRESSIVE CLOSER")
        my_agency = st.text_input("My Agency Name", "Senior Web Partner")
        batch_size = st.select_slider("Lead Batch Size", options=[20, 40, 60, 100], value=20)
        if st.button("Secure Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.markdown("## 🎯 Targeting Businesses with NO Website")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry (e.g. Lawyers, Roofers, Dentists)", placeholder="Enter niche...")
    with c2: city = st.text_input("City (e.g. London, Miami)", placeholder="Enter location...")

    if st.button("🚀 SCAN FOR HIGH-VALUE PROSPECTS"):
        if niche and city:
            leads = []
            with st.spinner("Extracting hidden opportunities from Google Maps..."):
                try:
                    for start in range(0, batch_size, 20):
                        params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY, "start": start}
                        data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                        if not data: break
                        leads.extend(data)
                except: st.error("Database connection busy. Try again.")
            
            # CRITICAL FILTER: ONLY SHOW PROSPECTS WITHOUT A WEBSITE
            high_value_leads = [l for l in leads if not l.get("website")]
            
            if high_value_leads:
                st.success(f"Successfully identified {len(high_value_leads)} Prospects with NO digital footprint!")
                for i, lead in enumerate(high_value_leads):
                    name, phone = lead.get("title"), lead.get("phone", "N/A")
                    rating = lead.get("rating", 0)
                    
                    # DEEP DARK PROSPECT CARD
                    with st.expander(f"🔥 HIGH-VALUE LEAD: {name}"):
                        l_col, r_col = st.columns([1, 1.2])
                        
                        with l_col:
                            st.markdown("### 🧠 AI Strategic Pitch")
                            pitch = f"Hi {name} Team,\n\nI was researching {niche} in {city} and noticed your impressive {rating}-star reputation on Google. However, I found a major gap: you have no active website link. This means you're invisible to 70% of modern customers.\n\nI’ve already designed a 'Proposed Website' for your business (see the live preview on the right). I can have this exact design live for you in 48 hours using our Hostinger AI engine.\n\nClaim your vision here to start: {HOSTINGER_LINK}\n\nBest, {my_agency}"
                            
                            st.markdown(f"<div class='vision-box'>Target is missing a website. Show them the vision to close the sale.</div>", unsafe_allow_html=True)
                            st.text_area("Live Pitch Script", pitch, height=200, key=f"pitch_{i}")
                            
                            # ONE-CLICK REACH OUT
                            subj = urllib.parse.quote(f"Proposed Website Preview for {name}")
                            body = urllib.parse.quote(pitch)
                            mailto = f"mailto:?subject={subj}&body={body}"
                            st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:700; font-size:18px;">📧 Send Preview to Owner</div></a>', unsafe_allow_html=True)
                            st.write(f"📞 Direct Line: {phone}")

                        with r_col:
                            st.markdown("### 👁️ Proposed Website Design")
                            st.info("Record your video pitch with this preview in the background.")
                            # Show a professional template as the "proposed design"
                            st.components.v1.iframe(PROPOSED_DESIGN_URL, height=500, scrolling=True)
            else:
                st.info("No businesses without websites found in this area. Try another city!")
        else:
            st.warning("Please provide both Niche and City.")
