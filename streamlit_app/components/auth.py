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
    """Show phone number and name input form"""
    
    st.subheader("📱 Login to FinanceBot")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Name input
        user_name = st.text_input(
            "Your Full Name",
            placeholder="Enter your full name",
            help="This will be used for personalization in calls and reports"
        )
        
        st.write("")  # Add spacing
        
        # Add info about format requirement
        st.info("📱 **Format**: +91XXXXXXXXXX (10 digits after +91)")
        
        phone = st.text_input(
            "Mobile Number",
            placeholder="+919876543210",
            max_chars=13,
            help="Must start with + and country code. Example: +919876543210",
            value="+91"  # Pre-fill with country code
        )
        
        # Real-time validation feedback
        if phone and phone != "+91":
            if not phone.startswith("+"):
                st.error("❌ Number must start with + (country code required)")
            elif phone.startswith("+91"):
                digits = phone[3:]
                if len(digits) < 10:
                    st.warning(f"⚠️  Need {10 - len(digits)} more digit(s)")
                elif len(digits) > 10:
                    st.error(f"❌ Too many digits (remove {len(digits) - 10})")
                elif not digits.isdigit():
                    st.error("❌ Only numbers allowed after +91")
                else:
                    st.success("✅ Valid format")
        
        if st.button("📨 Send OTP", type="primary", use_container_width=True):
            # Validate name
            if not user_name or len(user_name.strip()) < 2:
                st.error("❌ Please enter your full name")
            # Validate phone
            elif not phone.startswith("+"):
                st.error("❌ Phone number must start with + (e.g., +919876543210)")
            elif not validate_phone_number(phone):
                st.error("❌ Invalid phone number format. Use: +91XXXXXXXXXX (10 digits)")
            else:
                # Save both phone and name
                st.session_state.phone_number = phone
                st.session_state.user_name = user_name.strip()
                st.session_state.otp_sent = True
                
                st.success(f"✅ OTP sent to {phone}!")
                st.info("💡 For testing, use OTP: **222222**")
                st.rerun()


def show_otp_verification():
    """Show OTP verification form"""
    
    st.subheader("🔐 Verify OTP")
    
    # Show user info
    user_name = st.session_state.get('user_name', 'User')
    st.write(f"**Name:** {user_name}")
    st.write(f"**Mobile:** {st.session_state.phone_number}")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.write("")  # Spacing
        
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
                        "name": user_name
                    }
                    
                    st.success(f"🎉 Welcome, {user_name}!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid OTP. Please try again.")
        
        with col_b:
            if st.button("◀️ Back", use_container_width=True):
                st.session_state.otp_sent = False
                del st.session_state.user_name
                st.rerun()
        
        st.info("💡 **Test OTP:** 222222")

