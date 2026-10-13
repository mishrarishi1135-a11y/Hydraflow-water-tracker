import streamlit as st
import pandas as pd
import requests

# FastAPI Backend URL
API_BASE_URL = "http://127.0.0.1:8000"

# Page Configuration
st.set_page_config(
    page_title="HydraFlow AI - Smart Water Tracker",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Modern Glassmorphism & Animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }

    /* Main Container Gradient */
    .stApp {
        background: linear-gradient(135deg, #0b192c 0%, #102a43 50%, #000814 100%);
        color: #ffffff;
    }

    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 168, 255, 0.12);
        margin-bottom: 20px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .glass-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 35px 0 rgba(0, 210, 255, 0.22);
    }

    /* Glowing AI Insight Card */
    .ai-card {
        background: linear-gradient(135deg, rgba(0, 198, 255, 0.1) 0%, rgba(0, 114, 255, 0.12) 100%);
        border: 1px solid rgba(0, 198, 255, 0.35);
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 0 25px rgba(0, 198, 255, 0.2);
        animation: pulse-glow 3s infinite alternate;
        margin-bottom: 25px;
    }

    @keyframes pulse-glow {
        0% { box-shadow: 0 0 15px rgba(0, 198, 255, 0.2); }
        100% { box-shadow: 0 0 32px rgba(0, 198, 255, 0.45); }
    }

    /* Animated Water Droplet Icon */
    .water-badge {
        display: inline-block;
        font-size: 42px;
        animation: float 2.6s ease-in-out infinite;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        50% { transform: translateY(-10px) rotate(5deg); }
    }

    /* Metric Display */
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Custom Gradient Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #00c6ff 0%, #0072ff 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 24px;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(0, 114, 255, 0.35);
        transition: all 0.3s ease;
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
        box-shadow: 0 6px 20px rgba(0, 198, 255, 0.5);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "tracker_started" not in st.session_state:
    st.session_state.tracker_started = False
if "latest_analysis" not in st.session_state:
    st.session_state.latest_analysis = ""
if "selected_intake" not in st.session_state:
    st.session_state.selected_intake = 250

# ----------------- 1. WELCOME SCREEN -----------------
if not st.session_state.tracker_started:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2.6, 1])
    
    with col2:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 45px 30px;">
            <div class="water-badge">💧</div>
            <h1 style="background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.8rem; margin-bottom: 10px;">
                HydraFlow AI
            </h1>
            <p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 25px;">
                Intelligent Daily Hydration Companion powered by Gemini AI
            </p>
            <p style="color: #cbd5e1; font-size: 0.95rem; line-height: 1.6; margin-bottom: 30px;">
                Monitor every sip in real time, analyze your body hydration trends, and receive smart clinical feedback instantly via our FastAPI backend.
            </p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Start Tracking Hydration", use_container_width=True):
            st.session_state.tracker_started = True
            st.rerun()

# ----------------- 2. MAIN TRACKER DASHBOARD -----------------
else:
    # Sidebar - Logging via FastAPI
    with st.sidebar:
        st.markdown("### 🌊 Log Water Intake")
        st.markdown("<p style='color: #94a3b8; font-size: 0.85rem;'>Sync intake directly with FastAPI backend.</p>", unsafe_allow_html=True)

        user_id = st.text_input("👤 User ID", value="user_123", placeholder="e.g. user_123")
        
        # Preset Quick Buttons
        st.write("⚡ Quick Presets:")
        col_p1, col_p2, col_p3 = st.columns(3)
        if col_p1.button("+250 ml"): st.session_state.selected_intake = 250
        if col_p2.button("+500 ml"): st.session_state.selected_intake = 500
        if col_p3.button("+750 ml"): st.session_state.selected_intake = 750

        intake_ml = st.number_input(
            "💧 Intake Amount (mL)",
            min_value=50,
            max_value=5000,
            value=st.session_state.selected_intake,
            step=50
        )

        submit_btn = st.button("➕ Log to Database", use_container_width=True)

        if submit_btn:
            if not user_id.strip():
                st.error("Please enter a valid User ID.")
            else:
                with st.spinner("Calling FastAPI (/log-intake) & Gemini Agent..."):
                    payload = {"user_id": user_id, "intake_ml": int(intake_ml)}
                    try:
                        res = requests.post(f"{API_BASE_URL}/log-intake", json=payload, timeout=60)
                        if res.status_code == 200:
                            data = res.json()
                            st.session_state.latest_analysis = data.get("analysis", "")
                            st.success(f"{intake_ml} mL logged successfully via API!")
                        else:
                            st.error(f"API Error ({res.status_code}): {res.text}")
                    except requests.exceptions.ConnectionError:
                        st.error("Backend Server Offline! Please run 'uvicorn src.api:app --reload' in terminal.")
                    except Exception as err:
                        st.error(f"Request Error: {err}")

        st.markdown("---")
        if st.button("🔄 Change User / Reset View", use_container_width=True):
            st.session_state.tracker_started = False
            st.session_state.latest_analysis = ""
            st.rerun()

    # Dashboard Header
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div>
            <h2 style="margin: 0; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                HydraFlow Activity Dashboard
            </h2>
            <p style="color: #94a3b8; margin: 4px 0 0 0;">Active Profile: <b>{user_id}</b> | Backend: <code>{API_BASE_URL}</code></p>
        </div>
        <div class="water-badge" style="font-size: 34px;">💧</div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch History from FastAPI Route (/history/{user_id})
    records = []
    try:
        history_res = requests.get(f"{API_BASE_URL}/history/{user_id}", timeout=10)
        if history_res.status_code == 200:
            records = history_res.json().get("history", [])
    except requests.exceptions.ConnectionError:
        st.warning("⚠️ FastAPI Backend connect nahi ho paya. Make sure uvicorn chal raha hai.")

    total_consumed = sum([r[0] for r in records]) if records else 0
    daily_goal = 2500  # Target intake in mL
    progress_percentage = min(int((total_consumed / daily_goal) * 100), 100)

    # Row 1: Key Performance Metrics
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
        <div class="glass-card">
            <span style="color: #94a3b8; font-size: 0.9rem;">Total Daily Intake</span>
            <div class="metric-value">{total_consumed} <span style="font-size: 1.1rem; color: #cbd5e1;">mL</span></div>
            <span style="color: #38bdf8; font-size: 0.8rem;">Goal: {daily_goal} mL</span>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        st.markdown(f"""
        <div class="glass-card">
            <span style="color: #94a3b8; font-size: 0.9rem;">Hydration Goal Progress</span>
            <div class="metric-value">{progress_percentage}%</div>
            <span style="color: {'#4ade80' if progress_percentage >= 80 else '#fbbf24'}; font-size: 0.8rem;">
                {'Goal Reached! 🌟' if progress_percentage >= 100 else 'Drink more water 🥤'}
            </span>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        st.markdown(f"""
        <div class="glass-card">
            <span style="color: #94a3b8; font-size: 0.9rem;">Logs Recorded</span>
            <div class="metric-value">{len(records)}</div>
            <span style="color: #94a3b8; font-size: 0.8rem;">Sessions in Database</span>
        </div>
        """, unsafe_allow_html=True)

    # Progress Bar
    st.progress(progress_percentage / 100)
    st.markdown("<br>", unsafe_allow_html=True)

    # Row 2: AI Coach Feedback (Gemini Agent Output)
    if st.session_state.latest_analysis:
        st.markdown(f"""
        <div class="ai-card">
            <div style="display: flex; align-items: center; margin-bottom: 8px;">
                <span style="font-size: 22px; margin-right: 10px;">🤖</span>
                <b style="font-size: 1.1rem; color: #38bdf8;">HydraFlow AI Analysis</b>
            </div>
            <p style="color: #f1f5f9; font-size: 0.96rem; line-height: 1.6; margin: 0;">
                {st.session_state.latest_analysis}
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Row 3: Graphs & Data Table
    col_chart, col_table = st.columns([1.5, 1])

    with col_chart:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📈 Hydration Timeline")
        if records:
            df = pd.DataFrame(records, columns=["Intake_mL", "Date"])
            df["Log_Entry"] = [f"Entry #{i+1}" for i in range(len(df))]
            st.line_chart(df.set_index("Log_Entry")["Intake_mL"])
        else:
            st.info("No intake history recorded yet for this user. Log an entry from the sidebar!")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_table:
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        st.subheader("📋 Log Details (SQLite)")
        if records:
            df_display = pd.DataFrame(records, columns=["Intake (mL)", "Date"])
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        else:
            st.write("Awaiting logs from backend...")
        st.markdown("</div>", unsafe_allow_html=True)