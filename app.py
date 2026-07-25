import streamlit as st
import pandas as pd
import requests
import urllib.parse
import streamlit.components.v1 as components

# 1. ELITE UI CONFIG
st.set_page_config(page_title="WebDev Intelligence Pro", page_icon="💎", layout="wide")

# --- 2. THE NUCLEAR STEALTH CSS ---
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    .viewerBadge_79elG, .stDeployButton, div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] { background: #0f172a !important; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.4); color: white !important; }
    div[data-testid="stExpander"] * { color: #f1f5f9 !important; }
    .stButton>button { background: #2563eb; color: white !important; border-radius: 10px; font-weight: 700; height: 50px; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE & REVENUE ---
USER_DATABASE = {
    "ahmad123": "Ahmad - CEO",
    "pro_user_2026": "Enterprise Partner",
    "memuna123": "Master Admin"
}
REAL_API_KEY = st.secrets["SERPAPI_KEY"]
HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- 4. THE MAGIC "V1 WEBSITE" GENERATOR ---
def create_personalized_html(name, phone, city, niche):
    return f"""
    <div style="font-family: sans-serif; background: #fff; color: #333; margin: 0; padding: 0;">
        <nav style="background: #1a202c; color: #fff; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 24px; font-weight: bold;">{name}</span>
            <span style="font-size: 18px;">📞 {phone}</span>
        </nav>
        <div style="padding: 60px 20px; text-align: center; background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1581094794329-c8112a89af12?q=80&w=1000&auto=format&fit=crop'); background-size: cover; color: white;">
            <h1 style="font-size: 48px; margin-bottom: 10px;">Elite {niche} in {city}</h1>
            <p style="font-size: 20px; margin-bottom: 30px;">The most trusted service in the {city} area. Dedicated to quality and customer satisfaction.</p>
            <a href="#" style="background: #2563eb; color: white; padding: 15px 40px; text-decoration: none; border-radius: 50px; font-weight: bold; font-size: 18px;">GET A FREE QUOTE</a>
        </div>
        <div style="padding: 50px 20px; text-align: center; background: #f8fafc;">
            <h2 style="font-size: 32px; color: #1e293b;">Why {name}?</h2>
            <div style="display: flex; justify-content: space-around; margin-top: 30px; flex-wrap: wrap;">
                <div style="padding: 20px; width: 250px; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h3>⭐ Top Rated</h3>
                    <p>Highest rated {niche} service in {city}.</p>
                </div>
                <div style="padding: 20px; width: 250px; background: white; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    <h3>🕒 Fast Support</h3>
                    <p>We respond to all calls within minutes.</p>
                </div>
            </div>
        </div>
        <footer style="background: #111827; color: #9ca3af; padding: 40px; text-align: center;">
            <p>© 2026 {name} | Serving {city} and surrounding areas.</p>
            <p style="font-size: 12px; margin-top: 10px;">Powered by AI Web Solutions & Hostinger</p>
        </footer>
    </div>
    """

# --- 5. LOGIN ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>💎 WebDev Intelligence Pro</h1><p>The Exact Tool from the '1-Person Business' Strategy</p></div>", unsafe_allow_html=True)
    key = st.text_input("Enter License Key", type="password").strip()
    if st.button("Access Dashboard"):
        if key in USER_DATABASE:
            st.session_state["auth"], st.session_state["user"] = True, USER_DATABASE[key]
            st.rerun()
        else: st.error("Key Invalid.")
else:
    # --- 6. THE DASHBOARD ---
    st.sidebar.success(f"Connected: {st.session_state['user']}")
    my_agency = st.sidebar.text_input("Agency Name", "Senior Web Partner")
    if st.sidebar.button("Logout"): st.session_state["auth"] = False; st.rerun()

    st.title("🎯 Value-First Client Acquisition")
    st.markdown("Finding businesses with NO website to offer them a completed 'Version 1' design.")

    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Industry (e.g. Plumbers)", placeholder="Target niche...")
    with c2: city = st.text_input("City (e.g. Dallas, TX)", placeholder="Target city...")

    if st.button("🚀 EXECUTE DEEP SCAN"):
        if niche and city:
            with st.spinner("Accessing Google Maps Database..."):
                p = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY}
                leads = requests.get("https://serpapi.com/search", params=p).json().get("local_results", [])
                targets = [l for l in leads if not l.get("website")]
            
            if targets:
                st.success(f"Identified {len(targets)} Prospects with NO website!")
                for i, lead in enumerate(targets):
                    name, phone = lead.get("title"), lead.get("phone", "No Phone Listed")
                    with st.expander(f"🔥 HIGH-VALUE TARGET: {name}"):
                        l, r = st.columns([1, 1.4])
                        with l:
                            st.markdown("### ✉️ The Sales Script")
                            script = f"Hey {name} Team,\n\nI was looking for {niche} in {city} and found you, but I noticed you don't have a website yet. \n\nI actually went ahead and built a professional 'Version 1' website for you (see the preview on the right). \n\nWould you like to see it live? I can have this exact design active on your own domain in 48 hours.\n\nCLAIM YOUR SITE HERE: {HOSTINGER_LINK}"
                            st.text_area("Live Pitch Script", script, height=250, key=f"p_{i}")
                            
                            subj = urllib.parse.quote(f"I built a website for {name}")
                            mailto = f"mailto:?subject={subj}&body={urllib.parse.quote(script)}"
                            st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:15px; border-radius:12px; text-align:center; font-weight:700;">📧 Send Preview to Owner</div></a>', unsafe_allow_html=True)
                        
                        with r:
                            st.markdown("### 👁️ Your Proposed Design (V1)")
                            st.info("Record your screen showing this design to the owner!")
                            html_content = create_personalized_html(name, phone, city, niche)
                            components.html(html_content, height=500, scrolling=True)
            else: st.info("No businesses without websites found in this city.")
