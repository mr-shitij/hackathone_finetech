"""
Reports Page
"""

import streamlit as st
from database.db import get_user_reports
from pathlib import Path


def show_reports_page():
    """Show reports page"""
    
    st.title("📄 Your Financial Reports")
    st.write("Download and view your personalized financial reports")
    
    st.divider()
    
    # Get user's reports
    phone = st.session_state.user.get('phone')
    reports = get_user_reports(phone)
    
    if not reports:
        st.info("📭 No reports yet. Generate your first report from the Dashboard!")
        
        if st.button("Go to Dashboard", type="primary"):
            st.session_state.page = "Dashboard"
            st.rerun()
    else:
        # Group reports by type
        financial_reports = [r for r in reports if 'financial' in r['type']]
        tax_reports = [r for r in reports if 'tax' in r['type']]
        
        # Financial Planning Reports
        if financial_reports:
            st.subheader("💼 Financial Planning Reports")
            for report in financial_reports:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                    
                    with col1:
                        st.write(f"**{report['title']}**")
                    
                    with col2:
                        st.caption(f"📅 {report['date'][:10]}")
                    
                    with col3:
                        file_size = Path(report['path']).stat().st_size / 1024
                        st.caption(f"📊 {file_size:.0f} KB")
                    
                    with col4:
                        try:
                            with open(report['path'], 'rb') as f:
                                st.download_button(
                                    label="⬇️ Download",
                                    data=f,
                                    file_name=report['filename'],
                                    mime="application/pdf",
                                    key=f"download_{report['id']}"
                                )
                        except FileNotFoundError:
                            st.error("File not found")
                
                st.divider()
        
        # Tax Planning Reports
        if tax_reports:
            st.subheader("💰 Tax Planning Reports")
            for report in tax_reports:
                with st.container():
                    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
                    
                    with col1:
                        st.write(f"**{report['title']}**")
                    
                    with col2:
                        st.caption(f"📅 {report['date'][:10]}")
                    
                    with col3:
                        file_size = Path(report['path']).stat().st_size / 1024
                        st.caption(f"📊 {file_size:.0f} KB")
                    
                    with col4:
                        try:
                            with open(report['path'], 'rb') as f:
                                st.download_button(
                                    label="⬇️ Download",
                                    data=f,
                                    file_name=report['filename'],
                                    mime="application/pdf",
                                    key=f"download_{report['id']}"
                                )
                        except FileNotFoundError:
                            st.error("File not found")
                
                st.divider()
        
        # Stats
        st.subheader("📊 Report Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Reports", len(reports))
        
        with col2:
            st.metric("Financial Plans", len(financial_reports))
        
        with col3:
            st.metric("Tax Plans", len(tax_reports))

