import streamlit as st
import pandas as pd
import requests
import urllib.parse
import base64

# 1. PAGE SETUP
st.set_page_config(page_title="AI Sales War-Room: Heavy Lifter", page_icon="💎", layout="wide")

# --- 2. STEALTH WHITE-LABEL ---
st.markdown('<style>#MainMenu, footer, header {visibility: hidden;} .viewerBadge_79elG {display: none !important;}</style>', unsafe_allow_html=True)
st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%); background-attachment: fixed; }
    div[data-testid="stExpander"] { background: #0f172a !important; border-radius: 15px; box-shadow: 0 10px 15px rgba(0,0,0,0.3) !important; color: white !important; }
    div[data-testid="stExpander"] * { color: #f1f5f9 !important; }
    .stButton>button { background: #2563eb; color: white !important; border-radius: 10px; font-weight: 700; height: 50px; border: none; }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-2px); }
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATABASE & REVENUE ---
USER_DB = {
    st.secrets["AHMAD_KEY"]: "Ahmad - CEO",
    st.secrets["PRO_USER_KEY"]: "Enterprise Partner"
}
REAL_API_KEY = st.secrets["SERPAPI_KEY"]
HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- 4. DYNAMIC WEBSITE GENERATOR (THE MAGIC) ---
def generate_v1_site(name, phone, address, niche, city):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
        <style> .hero {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://source.unsplash.com/1600x900/?{niche}'); background-size: cover; }} </style>
    </head>
    <body class="bg-gray-50">
        <nav class="p-6 bg-white shadow-md flex justify-between items-center">
            <h1 class="text-2xl font-bold text-blue-600">{name}</h1>
            <p class="text-gray-600">📞 {phone}</p>
        </nav>
        <div class="hero h-96 flex flex-col items-center justify-center text-white text-center px-4">
            <h2 class="text-5xl font-extrabold mb-4">Elite {niche} in {city}</h2>
            <p class="text-xl mb-8">Professional service you can trust. Serving the {city} area with excellence.</p>
            <button class="bg-blue-600 px-8 py-3 rounded-full font-bold text-lg">Book Service Now</button>
        </div>
        <div class="p-12 text-center">
            <h3 class="text-3xl font-bold mb-6">Why Choose {name}?</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="p-6 bg-white rounded-xl shadow">✨ Quality Work</div>
                <div class="p-6 bg-white rounded-xl shadow">🕒 Fast Response</div>
                <div class="p-6 bg-white rounded-xl shadow">⭐ Top Rated in {city}</div>
            </div>
        </div>
        <footer class="bg-gray-900 text-white p-12 text-center">
            <p class="mb-2">{name} | {address}</p>
            <p class="text-gray-400">Powered by AI Web Solutions</p>
        </footer>
    </body>
    </html>
    """
    return base64.b64encode(html.encode()).decode()

# --- 5. LOGIN ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1>💎 AI SALES WAR-ROOM</h1><p>The 'Heavy Lifter' Edition</p></div>", unsafe_allow_html=True)
    key = st.text_input("License Key", type="password").strip()
    if st.button("Access Command Center"):
        if key in USER_DB:
            st.session_state["auth"], st.session_state["user"] = True, USER_DB[key]
            st.rerun()
        else: st.error("Access Denied.")
else:
    # --- 6. THE DASHBOARD ---
    st.sidebar.markdown(f"### 🎖️ Welcome, {st.session_state['user']}")
    if st.sidebar.button("Secure Logout"): st.session_state["auth"] = False; st.rerun()
    
    st.title("🎯 Value-First Prospecting")
    st.info("Finding businesses with NO website to offer them a completed 'Version 1' design.")
    
    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Niche", placeholder="e.g. Plumbers")
    with c2: city = st.text_input("Target City", placeholder="e.g. Dallas, TX")

    if st.button("🚀 EXECUTE DEEP SCAN"):
        if niche and city:
            with st.spinner("Analyzing Google Maps database..."):
                p = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY}
                data = requests.get("https://serpapi.com/search", params=p).json().get("local_results", [])
                leads = [l for l in data if not l.get("website")]
            
            if leads:
                st.success(f"Scanning Complete. {len(leads)} High-Value targets identified.")
                for i, lead in enumerate(leads):
                    name, phone, addr = lead.get("title"), lead.get("phone", "No Phone"), lead.get("address", "Local Area")
                    
                    with st.expander(f"🔥 TARGET: {name}"):
                        l, r = st.columns([1, 1.3])
                        with l:
                            st.markdown("### 🧠 The Value-First Script")
                            script = f"Hey {name} Team,\n\nI was looking for {niche} in {city} and found you, but I noticed you don't have a website yet. \n\nI actually went ahead and built a professional 'Version 1' website for you (see the preview on the right). \n\nWould you like to see it live? I can have this exact design active on your own domain in 48 hours.\n\nCLAIM YOUR SITE HERE: {HOSTINGER_LINK}\n\n*BONUS: I can also add an AI Chat Bot to handle your bookings automatically!*"
                            st.text_area("Copy/Paste Script:", script, height=250, key=f"p_{i}")
                            
                            subj = urllib.parse.quote(f"I built a website for {name}")
                            mailto = f"mailto:?subject={subj}&body={urllib.parse.quote(script)}"
                            st.markdown(f'<a href="{mailto}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:8px; text-align:center; font-weight:700;">📧 Send Preview to Owner</div></a>', unsafe_allow_html=True)
                            st.write(f"📞 Direct Call: {phone}")

                        with r:
                            st.markdown("### 👁️ Your Finished 'Version 1' Design")
                            st.caption("Record your screen showing this design to the owner!")
                            b64_site = generate_v1_site(name, phone, addr, niche, city)
                            st.markdown(f'<iframe src="data:text/html;base64,{b64_site}" height="500" width="100%" style="border-radius:10px; border:2px solid #334155;"></iframe>', unsafe_allow_html=True)
            else: st.info("No 'ghost' businesses found. Try a different city!")
