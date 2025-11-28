"""
Authentication Components
"""

import streamlit as st
from streamlit_app.utils.helpers import validate_phone_number, normalize_phone_number


def show_login_page():
    """Show login/OTP page"""
    
    # Header
    st.markdown('<h1 class="main-header">🏦 FinanceBot</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p style="text-align: center; font-size: 1.2rem; color: #666;">Your AI-Powered Financial Advisor</p>',
        unsafe_allow_html=True
    )
    
    st.divider()
    
    # Two-step authentication
    if not st.session_state.get('otp_sent'):
        # Step 1: Phone number input
        show_phone_input()
    else:
        # Step 2: OTP verification
        show_otp_verification()


def show_phone_input():
    """Show phone number input form"""
    
    st.subheader("📱 Login with Phone Number")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        phone = st.text_input(
            "Enter your mobile number",
            placeholder="+919876543210 or 9876543210",
            max_chars=15,
            help="Enter in format: +91xxxxxxxxxx or 10-digit mobile number"
        )
        
        if st.button("📨 Send OTP", type="primary", use_container_width=True):
            if validate_phone_number(phone):
                # Normalize phone number to E.164 format
                normalized_phone = normalize_phone_number(phone)
                
                st.session_state.phone_number = normalized_phone
                st.session_state.otp_sent = True
                
                st.success(f"✅ OTP sent to {normalized_phone}!")
                st.info("💡 For testing, use OTP: **222222**")
                st.rerun()
            else:
                st.error("❌ Please enter a valid phone number (e.g., +919876543210 or 9876543210)")


def show_otp_verification():
    """Show OTP verification form"""
    
    st.subheader("🔐 Verify OTP")
    st.write(f"OTP sent to **{st.session_state.phone_number}**")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        otp = st.text_input(
            "Enter 6-digit OTP",
            max_chars=6,
            type="password",
            help="Check your SMS for the OTP"
        )
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("✅ Verify", type="primary", use_container_width=True):
                if otp == "222222":  # Static OTP for development
                    # Set authenticated
                    st.session_state.authenticated = True
                    st.session_state.user = {
                        "phone": st.session_state.phone_number,
                        "name": st.session_state.phone_number.split("+91")[1][:4] + "****"
                    }
                    
                    st.success("🎉 Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Please try again.")
        
        with col_b:
            if st.button("◀️ Back", use_container_width=True):
                st.session_state.otp_sent = False
                st.rerun()
        
        st.info("💡 **Test OTP:** 222222")

