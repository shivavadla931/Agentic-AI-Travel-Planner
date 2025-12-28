import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(__file__))

from agent.travel_agent import run_travel_agent

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------
st.set_page_config(
    page_title="AI Travel Planner",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------
# CUSTOM CSS (Professional Dark Theme)
# ---------------------------------------
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #e6e6e6;
    }
    .stApp {
        background-color: #0e1117;
    }
    .card {
        background: linear-gradient(180deg, #14181d, #0f1317);
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #222831;
        margin-bottom: 20px;
    }
    .title {
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .subtitle {
        color: #9aa0a6;
        font-size: 16px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------
# HEADER
# ---------------------------------------
st.markdown("<div class='title'> Agentic AI Travel Planner</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>Plan a complete trip with flights, hotels, weather & budget — Powered by AI</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ---------------------------------------
# INPUT CARD
# ---------------------------------------

st.subheader("📍 Trip Details")

CITIES = [
    "Hyderabad",
    "Delhi",
    "Kolkata",
    "Chennai",
    "Bangalore",
    "Mumbai",
    "Goa",
    "Jaipur"
]

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox("Source City", CITIES, index=0)

with col2:
    destination = st.selectbox("Destination City", CITIES, index=1)

days = st.number_input(
    "Number of Days",
    min_value=1,
    max_value=10,
    value=1,
    help="Select the total number of days for your trip"
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------
# VALIDATION
# ---------------------------------------
if source == destination:
    st.warning("⚠️ Source and Destination cannot be the same.")

# ---------------------------------------
# ACTION BUTTON
# ---------------------------------------
st.markdown("<br>", unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns([1, 2, 1])

with button_col2:
    plan_clicked = st.button("✈️ Plan My Trip", use_container_width=True)

# ---------------------------------------
# OUTPUT
# ---------------------------------------
if plan_clicked and source != destination:
    with st.spinner("✨ Planning your perfect trip..."):
        output = run_travel_agent(source, destination, days)

    st.success("✅ Your professional AI-powered travel plan is ready!")
    st.subheader("🧳 Your Travel Plan")
    st.text(output)
    st.markdown("</div>", unsafe_allow_html=True)

 # DOWNLOAD BUTTON
    st.download_button(
        label="📥 Download Trip Plan",
        data=output,
        file_name="travel_plan.txt",
        mime="text/plain",
        use_container_width=True
    )

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("-------")
st.caption("© 2025 • AI Travel Planner • Built with Streamlit & Open-Meteo")
st.caption("Developed by Vadla Shiva Kumar")
