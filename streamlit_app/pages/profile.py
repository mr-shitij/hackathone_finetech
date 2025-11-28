"""
User Profile Page
"""

import streamlit as st


def show_profile_page():
    """Show user profile page"""
    
    st.title("👤 Profile")
    st.write("Manage your account and preferences")
    
    st.divider()
    
    # User info
    st.subheader("📱 Account Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.text_input("Phone Number", value=st.session_state.user.get('phone', ''), disabled=True)
        st.text_input("Name", value=st.session_state.user.get('name', 'User'))
    
    with col2:
        st.text_input("Email", value=st.session_state.user.get('email', ''))
        st.selectbox("Preferred Language", ["English", "Hindi"])
    
    if st.button("💾 Save Changes", type="primary"):
        st.success("Profile updated successfully!")
    
    st.divider()
    
    # Preferences
    st.subheader("⚙️ Preferences")
    
    st.checkbox("📧 Email notifications", value=True)
    st.checkbox("💬 WhatsApp updates", value=True)
    st.checkbox("📊 Weekly financial summary", value=False)
    
    st.divider()
    
    # About
    st.subheader("ℹ️ About FinanceBot")
    st.info("""
    **FinanceBot** is an AI-powered financial advisory platform designed to provide 
    personalized financial planning, tax optimization, and investment guidance.
    
    - 🤖 Powered by advanced AI agents
    - 📞 Voice-based data collection
    - 📄 Personalized PDF reports
    - 🔒 Secure and private
    
    Version: 1.0.0
    """)

