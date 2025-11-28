"""
Session management utilities for Streamlit
"""

import streamlit as st


def init_session():
    """Initialize session state variables"""
    
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'phone_number' not in st.session_state:
        st.session_state.phone_number = None
    
    if 'otp_sent' not in st.session_state:
        st.session_state.otp_sent = False
    
    if 'call_in_progress' not in st.session_state:
        st.session_state.call_in_progress = False
    
    if 'current_call_id' not in st.session_state:
        st.session_state.current_call_id = None


def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)


def set_authenticated(user_data):
    """Set user as authenticated"""
    st.session_state.authenticated = True
    st.session_state.user = user_data


def logout():
    """Logout user"""
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_session()

