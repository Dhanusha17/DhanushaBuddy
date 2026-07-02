import streamlit as st
import os
from services.gemini_service import GeminiService
from components import home, learn_concepts, ai_chat, aptitude_quiz, hr_interview, coding_practice

# Page config configuration
st.set_page_config(
    page_title="DhanushaBuddy - AI Placement Preparation Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to inject custom CSS styles
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Inject custom layout stylesheet
load_css("assets/style.css")

# Initialize GeminiService in Streamlit session state

if "gemini_service" not in st.session_state:
    st.session_state.gemini_service = GeminiService()

# Sidebar Navigation Panel
st.sidebar.markdown(
    '<h2>🎯 Dhanusha<span class="gradient-text">Buddy</span></h2>', 
    unsafe_allow_html=True
)
st.sidebar.markdown("**Your Personal AI Placement Preparation Assistant**")
st.sidebar.markdown("---")

# Navigation Routing Dictionary
pages = {
    "🏡 Home": home,
    "📚 Learn Concepts": learn_concepts,
    "💬 AI Chat": ai_chat,
    "💻 Coding Practice": coding_practice,
    "🧠 Aptitude Quiz": aptitude_quiz,
    "💼 HR Mock Interview": hr_interview
}

selected_page_name = st.sidebar.radio(
    "Navigation Menu:",
    options=list(pages.keys())
)

st.sidebar.markdown("---")

# API Connection status widget using the new GeminiService configuration check
if st.session_state.gemini_service.is_configured():
    st.sidebar.caption("🟢 **Connection Status:** Gemini API Active")
else:
    st.sidebar.caption("🔴 **Connection Status:** Gemini Key Missing")
    st.sidebar.info(
        "To enable AI responses, set the `GEMINI_API_KEY` environment variable "
        "locally or add it to Streamlit Secrets."
    )

# Footer credits
st.sidebar.markdown(
    '<div class="footer-text">DhanushaBuddy V1<br>Infosys Pragati Cohort 9 Capstone</div>', 
    unsafe_allow_html=True
)

# Render selected component page
selected_module = pages[selected_page_name]
if selected_page_name == "🏡 Home":
    selected_module.render()
else:
    selected_module.render(st.session_state.gemini_service)
