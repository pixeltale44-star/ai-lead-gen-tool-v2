import streamlit as st
import pandas as pd
import requests
import urllib.parse
import streamlit.components.v1 as components

# --- 1. ELITE UI & STEALTH CONFIG (MUST BE FIRST) ---
st.set_page_config(page_title="WebDev Intelligence Pro", page_icon="💎", layout="wide")

# Total White-Label Mode: Hides 'Manage app', Pencil, and Footer
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    .viewerBadge_79elG, .stDeployButton, div[data-testid="stStatusWidget"] {display: none !important;}
    .stApp { background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%); background-attachment: fixed; }
    
    /* Dark Prospect Cards */
    div[data-testid="stExpander"] {
        background: #0f172a !important;
        border: 2px solid #1e293b !important;
        border-radius: 15px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
    }
    div[data-testid="stExpander"] * { color: #f1f5f9 !important; }
    
    /* Professional Blue Buttons */
    .stButton>button {
        background: #2563eb; color: white !important; border-radius: 10px; font-weight: 700; height: 50px; border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SECURE DATABASE (LOAD FROM YOUR SECRETS BOX) ---
try:
    REAL_API_KEY = st.secrets["SERPAPI_KEY"]
    USER_DATABASE = {
        st.secrets["AHMAD_KEY"]: "Ahmad - CEO",
        st.secrets["PRO_USER_KEY"]: "Enterprise Partner"
    }
except:
    st.error("⚠️ Security Error: Please ensure your AHMAD_KEY, PRO_USER_KEY, and SERPAPI_KEY are entered in the Streamlit Secrets box.")
    st.stop()

HOSTINGER_LINK = "https://www.hostinger.com/in?REFERRALCODE=QWKAAMIRHS43"

# --- 3. THE "V1 WEBSITE" GENERATOR (THE HEAVY LIFTING) ---
def generate_v1_site_html(name, phone, city, niche):
    return f"""
    <div style="font-family: 'Inter', sans-serif; background: #fff; color: #1a202c; border-radius: 10px; overflow: hidden;">
        <nav style="background: #1e293b; color: #fff; padding: 20px; display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 20px; font-weight: 800;">{name}</span>
            <span style="font-weight: 600;">📞 {phone}</span>
        </nav>
        <div style="padding: 60px 20px; text-align: center; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?q=80&w=1000'); background-size: cover; color: white;">
            <h1 style="font-size: 42px; margin-bottom: 10px; text-transform: uppercase;">{niche} Experts in {city}</h1>
            <p style="font-size: 18px; margin-bottom: 30px;">Premium quality service you can trust. Now serving {city} and surrounding areas.</p>
            <div style="background: #2563eb; color: white; padding: 15px 30px; display: inline-block; border-radius: 5px; font-weight: bold;">REQUEST A FREE QUOTE</div>
        </div>
        <div style="padding: 40px; background: #f80px; background: #f8fafc; text-align: center;">
            <h2 style="color: #1e293b;">Why choose {name}?</h2>
            <p style="color: #64748b;">We specialize in professional {niche} solutions with a focus on speed, reliability, and 5-star customer service.</p>
        </div>
        <footer style="background: #0f172a; color: #94a3b8; padding: 30px; text-align: center; font-size: 12px;">
            <p>© 2026 {name} | {city}, USA</p>
            <p>Built with AI Intelligence & Hostinger Pro</p>
        </footer>
    </div>
    """

# --- 4. LOGIN SYSTEM ---
if "auth_status" not in st.session_state: st.session_state["auth_status"] = False
if not st.session_state["auth_status"]:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1>💎 WebDev Intelligence Pro</h1><p>The Exact Tool from the '1-Person Business' Strategy</p></div>", unsafe_allow_html=True)
    key = st.text_input("Enter License Key", type="password").strip()
    if st.button("Unlock Dashboard"):
        if key in USER_DATABASE:
            st.session_state["auth_status"], st.session_state["user_name"] = True, USER_DATABASE[key]
            st.rerun()
        else: st.error("Access Denied.")
else:
    # --- 5. THE PRO DASHBOARD ---
    st.sidebar.success(f"Connected: {st.session_state['user_name']}")
    my_agency = st.sidebar.text_input("Your Agency Name", "Senior Partner")
    if st.sidebar.button("Secure Logout"): st.session_state["auth_status"] = False; st.rerun()

    st.title("🎯 Value-First Prospect Acquisition")
    st.info("Searching Google Maps for businesses with NO website to offer them a completed 'Version 1' design.")

    c1, c2 = st.columns(2)
    with c1: niche = st.text_input("Target Industry (e.g. Plumbers)", placeholder="Who are we targeting?")
    with c2: city = st.text_input("Target City (e.g. Dallas, TX)", placeholder="Where are we targeting?")

    if st.button("🚀 EXECUTE DEEP SCAN"):
        if niche and city:
            with st.spinner("Accessing Real-Time Maps Data..."):
                p = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": REAL_API_KEY}
                data = requests.get("https://serpapi.com/search", params=p).json().get("local_results", [])
                targets = [l for l in data if not l.get("website")]
            
            if targets:
                st.success(f"Scanning Complete. {len(targets)} Businesses with NO Website Identified.")
                for i, lead in enumerate(targets):
                    name, phone = lead.get("title"), lead.get("phone", "No Phone Listed")
                    with st.expander(f"🔥 HIGH-VALUE TARGET: {name}"):
                        l_col, r_col = st.columns([1, 1.4])
                        with l_col:
                            st.markdown("### ✉️ The Sales Script")
                            script = f"Hey {name} Team,\n\nI was looking for {niche} in {city} and found your business, but I noticed you don't have a website link on Google yet. \n\nI actually went ahead and built a professional 'Version 1' website for you (see the preview on the right).\n\nWould you like to see it live? I can have this exact design active on your own domain in 48 hours.\n\nCLAIM YOUR SITE HERE: {HOSTINGER_LINK}\n\n*BONUS: I can also add an AI Chat Bot to handle your bookings automatically!*"
                            st.text_area("Ready-to-use Script:", script, height=220, key=f"p_{i}")
                            
                            subj = urllib.parse.quote(f"I built a website for {name}")
                            st.markdown(f'<a href="mailto:?subject={subj}&body={urllib.parse.quote(script)}" target="_blank" style="text-decoration:none;"><div style="background:#2563eb; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:700;">📧 Send Preview to Owner</div></a>', unsafe_allow_html=True)
                            st.write(f"📞 Direct Line: {phone}")
                        
                        with r_col:
                            st.markdown("### 👁️ Your Proposed Design (V1)")
                            st.caption("Record your screen showing this design to the owner!")
                            html_content = generate_v1_site_html(name, phone, city, niche)
                            components.html(html_content, height=500, scrolling=True)
            else: st.info("No 'Ghost' businesses found in this area. Try another city!")
