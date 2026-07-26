import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse
import streamlit.components.v1 as components

# 1. PAGE SETUP
st.set_page_config(page_title="WebDev Intelligence Pro", page_icon="💎", layout="wide")

# --- 2. THE STEALTH THEME ---
st.markdown('<style>#MainMenu, footer, header {visibility: hidden;} .viewerBadge_79elG {display: none !important;}</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] { background: #0f172a !important; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white !important; }
    div[data-testid="stExpander"] * { color: #f1f5f9 !important; }
    .stButton>button { background: #2563eb; color: white !important; border-radius: 10px; font-weight: 700; height: 50px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. REVENUE SECRETS ---
try:
    REAL_API_KEY = st.secrets["SERPAPI_KEY"]
    USER_DATABASE = {st.secrets["AHMAD_KEY"]: "Ahmad (Director)", st.secrets["PRO_USER_KEY"]: "Enterprise Partner"}
except:
    st.error("⚠️ Setup Error: Please ensure your keys are in the Streamlit Secrets box.")
    st.stop()

HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- 4. THE V1 SITE GENERATOR ---
def create_v1_html(name, phone, city, niche):
    return f"""
    <div style="font-family: sans-serif; background: #fff; color: #333; padding: 0; margin: 0; border-radius: 10px; overflow: hidden;">
        <nav style="background: #1e293b; color: #fff; padding: 20px; display: flex; justify-content: space-between;">
            <span style="font-weight: bold;">{name}</span>
            <span>📞 {phone}</span>
        </nav>
        <div style="padding: 50px 20px; text-align: center; background: #2563eb; color: white;">
            <h1>Elite {niche} in {city}</h1>
            <p>Quality service you can trust. Serving {city} area.</p>
        </div>
        <div style="padding: 30px; text-align: center;">
            <h3>Why choose us?</h3>
            <p>Top Rated in {city} • Fast Response • Professional Work</p>
        </div>
    </div>
    """

# --- 5. LOGIN ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>💎 WebDev Intelligence Pro</h1><p>Find businesses with NO website and close them instantly.</p></div>", unsafe_allow_html=True)
    key = st.text_input("License Key", type="password").strip()
    if st.button("Unlock Dashboard"):
        if key in USER_DATABASE:
            st.session_state["auth"], st.session_state["user"] = True, USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Denied.")
else:
    # --- 6. THE DASHBOARD ---
    st.sidebar.success(f"Connected: {st.session_state['user']}")
    # NEW: ADDED DEPTH SLIDER
    depth = st.sidebar.slider("Scan Depth (Number of results to check)", 20, 200, 60, step=20)
    if st.sidebar.button("Logout"): st.session_state["auth"] = False; st.rerun()

    st.title("🎯 Value-First Prospect Acquisition")
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry (e.g. Plumbers)", value="plumber")
    with c2: city = st.text_input("City (e.g. Dallas, TX)", value="Dallas, TX")

    if st.button("🚀 EXECUTE DEEP SCAN"):
        all_leads = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        # DEEP SCAN LOOP (This is the fix!)
        with st.spinner("Digging deep into Google Maps..."):
            for start in range(0, depth, 20):
                status_text.text(f"Scanning Page {start//20 + 1}...")
                params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY, "start": start}
                data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                if not data: break
                all_leads.extend(data)
                progress_bar.progress(min((start + 20) / depth, 1.0))
                time.sleep(0.5)

        # Filter for NO Website
        targets = [l for l in all_leads if not l.get("website")]

        if targets:
            st.success(f"Scanning Complete! Checked {len(all_leads)} businesses and found {len(targets)} GHOSTS (No Website).")
            for i, lead in enumerate(targets):
                name, phone = lead.get("title"), lead.get("phone", "No Phone Listed")
                with st.expander(f"🔥 HIGH-VALUE TARGET: {name}"):
                    cl, cr = st.columns([1, 1.4])
                    with cl:
                        st.markdown("### ✉️ The Sales Script")
                        script = f"Hey {name} Team, I noticed you have a great reputation but no website link on Google. I actually went ahead and built a 'Version 1' site for you (see right). Would you like to see it? Link: {HOSTINGER_LINK}"
                        st.text_area("Pitch Script:", script, height=180, key=f"p_{i}")
                        subj = urllib.parse.quote(f"I built a website for {name}")
                        mailto = f"mailto:?subject={subj}&body={urllib.parse.quote(script)}"
                        st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:700;">📧 Send Preview to Owner</div></a>', unsafe_allow_html=True)
                    with cr:
                        st.markdown("### 👁️ Your Proposed Design (V1)")
                        components.html(create_v1_html(name, phone, city, niche), height=400, scrolling=True)
        else:
            st.warning("Still no Ghost businesses found. Try a different city or increase the 'Scan Depth' in the sidebar!")
