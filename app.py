import streamlit as st
import pandas as pd
import requests
import time

# 1. ELITE UI CONFIG
st.set_page_config(page_title="AI SALES WAR-ROOM PRO", layout="wide")

# --- 2. VIBRANT THEME ---
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] {
        background: #1a202c !important;
        border: 2px solid #2d3748 !important;
        border-radius: 12px !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
    }
    .stButton>button { background: #2b6cb0; color: white; border-radius: 8px; font-weight: 600; width: 100%; }
    .badge-aplus { background: #c53030; color: white; padding: 4px 12px; border-radius: 20px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. ACCESS KEYS ---
USER_DATABASE = {"ahmad123": "Ahmad - CEO", "pro_user_2026": "Enterprise Partner"}
API_KEY = "b940832ef990aa072bc43da75530e0ef4aa2d8a12e53b0103e37b022154872bc"
HOSTINGER_AFFILIATE = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

if "authenticated" not in st.session_state: st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.title("💎 AI SALES WAR-ROOM")
    key = st.text_input("Enter License Key", type="password").strip()
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
        st.markdown("### ⚙️ SCAN SETTINGS")
        # --- NEW: QUANTITY SELECTOR ---
        lead_limit = st.slider("Number of leads to fetch", 20, 100, 40, step=20)
        st.info(f"The tool will perform {lead_limit//20} deep scans to find hidden targets.")
        
        st.divider()
        my_name = st.text_input("Your Name", "Senior Partner")
        avg_order = st.number_input("Avg Sale ($)", 100, 5000, 500)
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

    st.markdown("### 📡 Deep-Scan Targets")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. Roofers")
    with c2: location = st.text_input("Target City", placeholder="e.g. Miami")

    if st.button("🚀 INITIATE UNLIMITED SCAN"):
        if niche and location:
            all_leads = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # --- LOOP FOR MULTIPLE PAGES ---
            for offset in range(0, lead_limit, 20):
                status_text.text(f"Scanning Page {offset//20 + 1}...")
                try:
                    params = {
                        "engine": "google_maps",
                        "q": f"{niche} in {location}",
                        "api_key": API_KEY,
                        "start": offset # This is the magic "turn the page" code
                    }
                    response = requests.get("https://serpapi.com/search", params=params).json()
                    page_results = response.get("local_results", [])
                    
                    if not page_results:
                        break # No more leads to find
                    
                    all_leads.extend(page_results)
                    progress_bar.progress(min((offset + 20) / lead_limit, 1.0))
                    time.sleep(0.5) # Prevent API blocking
                except:
                    st.error("Connection interrupted.")
                    break
            
            # Filter for High Value (No Website)
            high_value_leads = [l for l in all_leads if not l.get("website")]
            
            st.success(f"Scan Complete. Found {len(all_leads)} total leads. {len(high_value_leads)} are High-Value Opportunities!")
            
            # Display Results
            for i, lead in enumerate(all_leads):
                name, site, rating = lead.get("title"), lead.get("website"), lead.get("rating", 0)
                score, badge = ("A+", "badge-aplus") if not site else ("B", "")

                with st.expander(f"[{score}] {name}"):
                    cl, cr = st.columns([1, 1.2])
                    with cl:
                        st.markdown("<h4 style='color:#58a6ff;'>🧠 Strategy</h4>", unsafe_allow_html=True)
                        if not site:
                            loss = avg_order * 10
                            st.error("FATAL: No Website Found.")
                            st.markdown(f"**Potential Monthly Loss: ${loss:,}**")
                            pitch = f"Hi {name}, I noticed your {rating} rating on Google but you have NO website. You are losing about ${loss:,}/mo. I can build a Hostinger site for you today: {HOSTINGER_AFFILIATE}"
                        else:
                            st.info("STATUS: Website Detected.")
                            pitch = f"Hi {name}, your site needs an AI speed boost. Move to Hostinger here: {HOSTINGER_AFFILIATE}"
                        st.text_area("Pitch:", pitch, height=150, key=f"p_{i}")
                    with cr:
                        st.markdown("<h4 style='color:#58a6ff;'>👁️ Preview</h4>", unsafe_allow_html=True)
                        if site: st.components.v1.iframe(site, height=350)
                        else: st.warning("No site found. Record Loom video now.")
        else:
            st.warning("Enter Niche and City.")
