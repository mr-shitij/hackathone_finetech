"""
Financial Calculators Page
"""

import streamlit as st
from streamlit_app.utils.helpers import calculate_sip, calculate_emi, format_currency


def show_calculators_page():
    """Show financial calculators page"""
    
    st.title("🧮 Financial Calculators")
    st.write("Calculate your investments, loans, and tax estimates")
    
    st.divider()
    
    # Calculator tabs
    tab1, tab2, tab3 = st.tabs(["📈 SIP Calculator", "🏦 EMI Calculator", "💼 Tax Calculator"])
    
    # SIP Calculator
    with tab1:
        st.header("SIP Calculator")
        st.write("Calculate returns on your Systematic Investment Plan")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input")
            monthly_amount = st.number_input(
                "Monthly Investment (₹)",
                min_value=500,
                max_value=1000000,
                value=5000,
                step=500
            )
            expected_return = st.slider(
                "Expected Annual Return (%)",
                min_value=1,
                max_value=30,
                value=12,
                step=1
            )
            time_period = st.slider(
                "Investment Period (Years)",
                min_value=1,
                max_value=30,
                value=10,
                step=1
            )
        
        with col2:
            st.subheader("Results")
            result = calculate_sip(monthly_amount, expected_return, time_period)
            
            st.metric(
                "💰 Total Investment",
                format_currency(result['total_investment'])
            )
            st.metric(
                "📈 Estimated Returns",
                format_currency(result['estimated_returns']),
                delta=f"+{result['estimated_returns']/result['total_investment']*100:.1f}%"
            )
            st.metric(
                "🎯 Maturity Value",
                format_currency(result['maturity_value'])
            )
            
            # Show chart
            import plotly.graph_objects as go
            
            fig = go.Figure(data=[
                go.Pie(
                    labels=['Investment', 'Returns'],
                    values=[result['total_investment'], result['estimated_returns']],
                    hole=.3
                )
            ])
            fig.update_layout(title="Investment Breakdown")
            st.plotly_chart(fig, use_container_width=True)
    
    # EMI Calculator
    with tab2:
        st.header("EMI Calculator")
        st.write("Calculate your Equated Monthly Installment for loans")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input")
            loan_amount = st.number_input(
                "Loan Amount (₹)",
                min_value=10000,
                max_value=100000000,
                value=1000000,
                step=50000
            )
            interest_rate = st.slider(
                "Interest Rate (% per annum)",
                min_value=1.0,
                max_value=20.0,
                value=8.5,
                step=0.1
            )
            tenure = st.slider(
                "Loan Tenure (Years)",
                min_value=1,
                max_value=30,
                value=20,
                step=1
            )
        
        with col2:
            st.subheader("Results")
            result = calculate_emi(loan_amount, interest_rate, tenure * 12)
            
            st.metric(
                "💳 Monthly EMI",
                format_currency(result['emi'])
            )
            st.metric(
                "💸 Total Interest",
                format_currency(result['total_interest'])
            )
            st.metric(
                "💰 Total Amount Payable",
                format_currency(result['total_amount'])
            )
            
            # Show chart
            fig = go.Figure(data=[
                go.Pie(
                    labels=['Principal', 'Interest'],
                    values=[loan_amount, result['total_interest']],
                    hole=.3
                )
            ])
            fig.update_layout(title="Payment Breakdown")
            st.plotly_chart(fig, use_container_width=True)
    
    # Tax Calculator
    with tab3:
        st.header("Income Tax Calculator")
        st.write("Compare Old vs New tax regimes")
        
        st.info("🚧 Advanced tax calculator coming soon! For now, use our AI agent to get personalized tax advice.")
        
        if st.button("📞 Talk to Tax Planning Agent", type="primary"):
            st.session_state.page = "Dashboard"
            st.rerun()

