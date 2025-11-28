"""
Dashboard Components
"""

import streamlit as st
import sys
from pathlib import Path
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from database.db import get_user_reports, get_user_financial_data, save_call, get_call_by_tracking_id
from services.pixpoc_client import PixpocClient


def show_dashboard():
    """Show main dashboard"""
    
    # Header
    st.title(f"👋 Welcome, {st.session_state.user.get('name', 'User')}!")
    st.write("Your personalized financial dashboard")
    
    st.divider()
    
    # Financial summary
    show_financial_summary()
    
    st.divider()
    
    # Call to action
    show_call_to_action()
    
    st.divider()
    
    # Recent reports
    show_recent_reports()


def show_financial_summary():
    """Show financial summary cards"""
    
    st.subheader("📊 Financial Summary")
    
    phone = st.session_state.user.get('phone')
    financial_data = get_user_financial_data(phone)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Monthly Income",
            value=f"₹{financial_data.get('income', 0):,}",
            delta="+5.2%",
            help="Your total monthly income"
        )
    
    with col2:
        st.metric(
            label="💵 Savings",
            value=f"₹{financial_data.get('savings', 0):,}",
            delta="+10,000",
            help="Current savings balance"
        )
    
    with col3:
        st.metric(
            label="💸 Expenses",
            value=f"₹{financial_data.get('expenses', 0):,}",
            delta="-5,000",
            delta_color="inverse",
            help="Total monthly expenses"
        )
    
    with col4:
        savings_rate = (financial_data.get('savings', 0) / financial_data.get('income', 1)) * 100 if financial_data.get('income', 0) > 0 else 0
        st.metric(
            label="📈 Savings Rate",
            value=f"{savings_rate:.1f}%",
            delta="+2.5%",
            help="Percentage of income saved"
        )


def show_call_to_action():
    """Show call initiation section"""
    
    st.subheader("🎯 Get Personalized Financial Advice")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        Talk to our AI financial advisor and receive:
        - 📊 Comprehensive financial analysis
        - 💡 Personalized recommendations
        - 📄 Professional PDF report
        - 🎯 Goal-based financial planning
        """)
    
    with col2:
        st.write("")
        st.write("")
        if st.button("📞 Start AI Call", type="primary", use_container_width=True, key="start_call"):
            initiate_call()


def initiate_call():
    """Initiate Pixpoc call"""
    
    phone = st.session_state.user.get('phone')
    user_name = st.session_state.user.get('name', 'User')
    
    with st.spinner("📞 Initiating call..."):
        try:
            # Initialize Pixpoc client
            client = PixpocClient(
                base_url=os.getenv("PIXPOC_API_BASE_URL", "https://app.pixpoc.ai"),
                api_key=os.getenv("PIXPOC_API_KEY", "")
            )
            
            agent_id = os.getenv("PIXPOC_AGENT_ID")
            from_number_id = os.getenv("PIXPOC_FROM_NUMBER_ID")
            
            if not agent_id:
                st.error("❌ PIXPOC_AGENT_ID not configured in .env file")
                return
            
            # Use the proper Pixpoc client method with user's actual name
            result = client.initiate_call_sync(
                phone_number=phone,
                agent_id=agent_id,
                contact_name=user_name,  # Use actual user name from login
                from_number_id=from_number_id  # Use configured from number
            )
            
            # Extract all relevant IDs from Pixpoc response
            call_id = result['call']['id']
            tracking_id = result['call'].get('trackingId')
            call_status = result['call']['status']
            contact_id = result['contact']['id']
            campaign_id = result['campaign']['id']
            
            # Save to database with all Pixpoc response data
            save_call(
                phone_number=phone,
                call_id=call_id,
                contact_id=contact_id,
                tracking_id=tracking_id,
                campaign_id=campaign_id
            )
            
            st.session_state.call_in_progress = True
            st.session_state.current_call_id = call_id
            
            st.success("✅ Call initiated successfully!")
            
            # Show call details
            st.info(f"""
            📞 **Call Details:**
            - Contact: **{user_name}**
            - Call ID: `{call_id}`
            - Status: `{call_status}`
            - Number: `{phone}`
            
            You will receive a call shortly from our AI financial advisor.
            
            **The AI will:**
            - Greet you by name ({user_name})
            - Ask about your income and expenses
            - Understand your financial goals
            - Assess your risk tolerance
            - Collect other relevant financial information
            
            After the call completes, we'll automatically generate a personalized financial report for you.
            """)
            
            # Add auto-refresh message
            st.warning("🔄 Dashboard will auto-refresh when your report is ready...")
        
        except Exception as e:
            st.error(f"❌ Error initiating call: {str(e)}")
            
            # Show helpful debug info
            with st.expander("🔍 Debug Information"):
                st.code(f"""
API Base URL: {os.getenv('PIXPOC_API_BASE_URL', 'https://app.pixpoc.ai')}
Agent ID: {os.getenv('PIXPOC_AGENT_ID', 'Not configured')}
From Number ID: {os.getenv('PIXPOC_FROM_NUMBER_ID', 'Not configured')}
API Key: {'Configured' if os.getenv('PIXPOC_API_KEY') else 'Not configured'}
Phone: {phone}
User Name: {user_name}
Error: {str(e)}
                """)
            
            st.info("💡 **Next Steps:**\n1. Check that all Pixpoc credentials are configured in .env\n2. Ensure webhook server is running\n3. Verify agent ID is correct")


def show_recent_reports():
    """Show recent reports"""
    
    st.subheader("📄 Recent Reports")
    
    phone = st.session_state.user.get('phone')
    reports = get_user_reports(phone)
    
    if not reports:
        st.info("📭 No reports yet. Generate your first report by starting an AI call!")
    else:
        # Show latest 3 reports
        for report in reports[:3]:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                
                with col1:
                    st.write(f"**📊 {report['title']}**")
                
                with col2:
                    st.caption(f"📅 {report['date'][:10]}")
                
                with col3:
                    st.caption(f"🏷️ {report['type'].replace('_', ' ').title()}")
                
                with col4:
                    try:
                        with open(report['path'], 'rb') as f:
                            st.download_button(
                                label="⬇️",
                                data=f,
                                file_name=report['filename'],
                                mime="application/pdf",
                                key=f"dash_download_{report['id']}",
                                help="Download report"
                            )
                    except FileNotFoundError:
                        st.error("❌")
                
                st.divider()
        
        if len(reports) > 3:
            if st.button("📄 View All Reports", use_container_width=True):
                st.session_state.page = "Reports"
                st.rerun()
    
    # Auto-refresh if call in progress
    if st.session_state.get('call_in_progress'):
        import time
        time.sleep(5)
        st.rerun()

