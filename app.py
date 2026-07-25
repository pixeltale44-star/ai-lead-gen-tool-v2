import streamlit as st
import pandas as pd
import requests
import time
import urllib.parse

# ============================================================
# 1. PAGE CONFIG
# ============================================================
st.set_page_config(page_title="AI Website Closer Pro", page_icon="🎯", layout="wide")

# ============================================================
# 2. DESIGN SYSTEM
#    Palette:  ink #0b1220 (cards) / slate #0f172a (deep bg accents)
#              canvas #eef2f7 → #dfe6ee (app background gradient)
#              electric #2563eb (primary actions)
#              signal #f59e0b (amber — "high value" / scarcity cue)
#              verified #10b981 (green — success states)
#    Type:     Space Grotesk (display) + Inter (body)
# ============================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;600;700&display=swap');

    /* Total white-label mode */
    #MainMenu, footer, header {visibility: hidden; display: none !important;}
    .viewerBadge_79elG, .stDeployButton, div[data-testid="stStatusWidget"] {display: none !important;}

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; font-weight: 700 !important; }

    .stApp {
        background: linear-gradient(160deg, #eef2f7 0%, #dfe6ee 100%);
        background-attachment: fixed;
    }

    /* --- Hero --- */
    .hero-wrap {
        background: linear-gradient(135deg, #0b1220 0%, #16213a 100%);
        border-radius: 20px;
        padding: 40px 44px;
        margin-bottom: 28px;
        box-shadow: 0 20px 40px -12px rgba(11, 18, 32, 0.35);
    }
    .hero-eyebrow {
        display: inline-block;
        color: #f59e0b;
        font-weight: 700;
        font-size: 13px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .hero-title {
        color: #f8fafc;
        font-size: 34px;
        font-weight: 700;
        margin: 0 0 8px 0;
        line-height: 1.15;
    }
    .hero-sub {
        color: #94a3b8;
        font-size: 16px;
        font-weight: 400;
        margin: 0;
    }

    /* --- Metric chips --- */
    .metric-chip {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 14px;
        padding: 16px 20px;
        text-align: left;
    }
    .metric-chip .num { font-family: 'Space Grotesk', sans-serif; font-size: 26px; font-weight: 700; color: #0b1220; }
    .metric-chip .lbl { font-size: 13px; color: #64748b; font-weight: 600; }

    /* --- Lead card --- */
    .lead-card {
        background: #0b1220;
        border: 1px solid #1e293b;
        border-radius: 18px;
        padding: 22px 24px;
        margin-bottom: 20px;
        box-shadow: 0 16px 30px -10px rgba(0,0,0,0.3);
    }
    .lead-badge {
        display: inline-block;
        background: rgba(245, 158, 11, 0.15);
        color: #f59e0b;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        padding: 4px 10px;
        border-radius: 999px;
        margin-bottom: 10px;
    }
    .lead-name { color: #f8fafc; font-family: 'Space Grotesk', sans-serif; font-size: 20px; font-weight: 700; margin: 0 0 4px 0; }
    .lead-meta { color: #94a3b8; font-size: 14px; margin: 0; }
    .vision-box {
        background: #16213a;
        padding: 16px 18px;
        border-radius: 12px;
        border-left: 4px solid #2563eb;
        color: #cbd5e1;
        font-size: 14px;
        margin: 14px 0;
    }

    /* --- Buttons --- */
    .stButton>button {
        background: #2563eb;
        color: white !important;
        border-radius: 12px;
        font-weight: 700;
        border: none;
        height: 52px;
        transition: 0.2s ease;
    }
    .stButton>button:hover { background: #1d4ed8; transform: translateY(-2px); box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.45); }

    .cta-link {
        text-decoration: none; display: block; background: #2563eb; color: white;
        padding: 14px; border-radius: 12px; text-align: center; font-weight: 700; margin-top: 10px;
    }
    .cta-link:hover { background: #1d4ed8; }
    </style>
    """, unsafe_allow_html=True)

# ============================================================
# 3. SECRETS  (set these in Streamlit Cloud → App settings → Secrets,
#    or locally in .streamlit/secrets.toml — NEVER commit real values)
#
#    [general]
#    api_key = "your-serpapi-key"
#    hostinger_link = "https://www.hostinger.com/in?REFERRALCODE=..."
#
#    [licenses]
#    ahmad123 = "Ahmad - Executive Director"
#    pro_user_2026 = "Premium Partner"
#    MEMUNA_VIP = "Master Admin"
# ============================================================
API_KEY = st.secrets.get("general", {}).get("api_key", "")
HOSTINGER_LINK = st.secrets.get("general", {}).get("hostinger_link", "")
USER_DATABASE = dict(st.secrets.get("licenses", {}))

PROPOSED_DESIGN_URL = "https://preview.themeforest.net/item/skylark-creative-one-page-business-template/full_screen_preview/21683050"

if "auth" not in st.session_state:
    st.session_state["auth"] = False

# ============================================================
# 4. LOGIN SCREEN
# ============================================================
if not st.session_state["auth"]:
    _, mid, _ = st.columns([1, 1.2, 1])
    with mid:
        st.markdown("""
            <div class="hero-wrap" style="text-align:center; margin-top: 80px;">
                <span class="hero-eyebrow">🎯 Closer Access</span>
                <p class="hero-title">AI Website Closer Pro</p>
                <p class="hero-sub">Closing high-ticket web clients with instant visual ROI.</p>
            </div>
        """, unsafe_allow_html=True)
        key = st.text_input("License Key", type="password", placeholder="Enter your access key...").strip()
        if st.button("Unlock Closer Dashboard", use_container_width=True):
            if not API_KEY or not USER_DATABASE:
                st.error("App secrets aren't configured yet — add api_key, hostinger_link and licenses in Streamlit Cloud → Settings → Secrets.")
            elif key in USER_DATABASE:
                st.session_state["auth"] = True
                st.session_state["user"] = USER_DATABASE[key]
                st.rerun()
            else:
                st.error("Access key invalid.")

# ============================================================
# 5. DASHBOARD
# ============================================================
else:
    with st.sidebar:
        st.markdown(f"### 🛡️ Welcome, {st.session_state['user']}")
        st.success("Mode: AGGRESSIVE CLOSER")
        my_agency = st.text_input("My Agency Name", "Senior Web Partner")
        batch_size = st.select_slider("Lead Batch Size", options=[20, 40, 60, 100], value=20)
        if st.button("Secure Logout"):
            st.session_state["auth"] = False
            st.rerun()

    st.markdown("""
        <div class="hero-wrap">
            <span class="hero-eyebrow">🎯 Prospect Radar</span>
            <p class="hero-title">Find businesses with no website</p>
            <p class="hero-sub">Scan a niche and city — we surface the ones with the biggest gap to close.</p>
        </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        niche = st.text_input("Industry (e.g. Lawyers, Roofers, Dentists)", placeholder="Enter niche...")
    with c2:
        city = st.text_input("City (e.g. London, Miami)", placeholder="Enter location...")

    scan = st.button("🚀 SCAN FOR HIGH-VALUE PROSPECTS", use_container_width=True)

    if scan:
        if not API_KEY:
            st.error("No API key configured — add it in Streamlit Cloud → Settings → Secrets.")
        elif niche and city:
            leads = []
            with st.spinner("Extracting hidden opportunities from Google Maps..."):
                try:
                    for start in range(0, batch_size, 20):
                        params = {"engine": "google_maps", "q": f"{niche} in {city}", "api_key": API_KEY, "start": start}
                        data = requests.get("https://serpapi.com/search", params=params).json().get("local_results", [])
                        if not data:
                            break
                        leads.extend(data)
                except Exception:
                    st.error("Database connection busy. Try again.")

            high_value_leads = [l for l in leads if not l.get("website")]

            if high_value_leads:
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f'<div class="metric-chip"><div class="num">{len(leads)}</div><div class="lbl">Businesses scanned</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-chip"><div class="num">{len(high_value_leads)}</div><div class="lbl">No website found</div></div>', unsafe_allow_html=True)
                with m3:
                    pct = round(100 * len(high_value_leads) / max(len(leads), 1))
                    st.markdown(f'<div class="metric-chip"><div class="num">{pct}%</div><div class="lbl">Open opportunity rate</div></div>', unsafe_allow_html=True)

                st.write("")

                for i, lead in enumerate(high_value_leads):
                    name = lead.get("title", "Unknown business")
                    phone = lead.get("phone", "N/A")
                    rating = lead.get("rating", 0)
                    stars = "⭐" * int(round(rating)) if rating else "No rating yet"

                    st.markdown(f"""
                        <div class="lead-card">
                            <span class="lead-badge">🔥 No website found</span>
                            <p class="lead-name">{name}</p>
                            <p class="lead-meta">{stars} &nbsp;•&nbsp; 📞 {phone}</p>
                        </div>
                    """, unsafe_allow_html=True)

                    l_col, r_col = st.columns([1, 1.2])
                    with l_col:
                        pitch = (
                            f"Hi {name} Team,\n\n"
                            f"I was researching {niche} in {city} and noticed your impressive {rating}-star reputation on Google. "
                            f"However, I found a major gap: you have no active website link. This means you're invisible to 70% of modern customers.\n\n"
                            f"I've already designed a 'Proposed Website' for your business (see the live preview alongside this). "
                            f"I can have this exact design live for you in 48 hours using our Hostinger AI engine.\n\n"
                            f"Claim your vision here to start: {HOSTINGER_LINK}\n\n"
                            f"Best, {my_agency}"
                        )
                        st.markdown('<div class="vision-box">Target is missing a website. Show them the vision to close the sale.</div>', unsafe_allow_html=True)
                        st.text_area("Live Pitch Script", pitch, height=180, key=f"pitch_{i}")

                        subj = urllib.parse.quote(f"Proposed Website Preview for {name}")
                        body = urllib.parse.quote(pitch)
                        mailto = f"mailto:?subject={subj}&body={body}"
                        st.markdown(f'<a href="{mailto}" target="_blank" class="cta-link">📧 Send Preview to Owner</a>', unsafe_allow_html=True)

                    with r_col:
                        st.markdown("**👁️ Proposed Website Design**")
                        st.caption("Record your video pitch with this preview in the background.")
                        st.components.v1.iframe(PROPOSED_DESIGN_URL, height=440, scrolling=True)

                    st.divider()
            else:
                st.info("No businesses without websites found in this area. Try another city!")
        else:
            st.warning("Please provide both Niche and City.")
