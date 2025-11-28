"""
FinanceBot - Main Streamlit Application
AI-powered financial advisory platform
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from streamlit_app.components.auth import show_login_page
from streamlit_app.components.dashboard import show_dashboard
from streamlit_app.utils.session import init_session, is_authenticated
from database.db import init_db

# Page configuration
st.set_page_config(
    page_title="FinanceBot - AI Financial Advisor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize database
init_db()

# Initialize session state
init_session()

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Main application logic
def main():
    """Main application entry point"""
    
    # Check if user is authenticated
    if not is_authenticated():
        # Show login page
        show_login_page()
    else:
        # Show sidebar
        with st.sidebar:
            st.title("💰 FinanceBot")
            st.write(f"**Logged in as:** {st.session_state.user.get('phone', 'User')}")
            
            st.divider()
            
            # Navigation
            st.subheader("Navigation")
            page = st.radio(
                "Go to",
                ["📊 Dashboard", "🧮 Calculators", "📄 Reports", "👤 Profile"],
                label_visibility="collapsed"
            )
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()
        
        # Show selected page
        if "Dashboard" in page:
            show_dashboard()
        elif "Calculators" in page:
            from streamlit_app.pages.calculators import show_calculators_page
            show_calculators_page()
        elif "Reports" in page:
            from streamlit_app.pages.reports import show_reports_page
            show_reports_page()
        elif "Profile" in page:
            from streamlit_app.pages.profile import show_profile_page
            show_profile_page()

if __name__ == "__main__":
    main()

