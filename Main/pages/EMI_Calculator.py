import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def calculate_emi(principal, rate, tenure):
    """Calculate EMI for given principal, interest rate and tenure"""
    rate = rate / (12 * 100)  # monthly interest rate
    tenure_months = tenure * 12  # tenure in months
    
    # EMI formula
    emi = principal * rate * (1 + rate)**tenure_months / ((1 + rate)**tenure_months - 1)
    return emi

def format_currency(amount):
    """Format amount in Indian currency format"""
    s = str(int(amount))
    l = len(s)
    if l > 3:
        formatted = s[-3:]
        s = s[:-3]
        while s:
            formatted = s[-2:] + ',' + formatted if s[-2:] else s[-1] + ',' + formatted
            s = s[:-2]
    else:
        formatted = s
    return f"₹{formatted}"

def app():
    st.title("💰 Home Loan EMI Calculator")
    
    # Create a form for input
    with st.form("emi_calculator"):
        col1, col2 = st.columns(2)
        
        with col1:
            loan_amount = st.number_input(
                "Loan Amount (₹)",
                min_value=100000,
                max_value=100000000,
                value=5000000,
                step=100000,
                help="Enter the loan amount you want to borrow"
            )
            
            interest_rate = st.number_input(
                "Interest Rate (%)",
                min_value=5.0,
                max_value=20.0,
                value=8.5,
                step=0.1,
                help="Enter the annual interest rate"
            )
        
        with col2:
            loan_tenure = st.number_input(
                "Loan Tenure (Years)",
                min_value=1,
                max_value=30,
                value=20,
                step=1,
                help="Enter the loan tenure in years"
            )
            
            down_payment_percent = st.number_input(
                "Down Payment (%)",
                min_value=0,
                max_value=90,
                value=20,
                step=5,
                help="Enter the down payment percentage"
            )
        
        calculate_button = st.form_submit_button("Calculate EMI", use_container_width=True)
    
    if calculate_button:
        # Calculate down payment and actual loan amount
        down_payment = loan_amount * (down_payment_percent / 100)
        actual_loan = loan_amount - down_payment
        
        # Calculate EMI
        monthly_emi = calculate_emi(actual_loan, interest_rate, loan_tenure)
        
        # Calculate other loan details
        total_payment = monthly_emi * loan_tenure * 12
        total_interest = total_payment - actual_loan
        
        # Display Results
        st.markdown("### 📊 Loan Summary")
        
        # Key metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Monthly EMI", format_currency(monthly_emi))
        
        with col2:
            st.metric("Total Interest", format_currency(total_interest))
        
        with col3:
            st.metric("Total Payment", format_currency(total_payment))
        
        # Detailed Breakdown
        st.markdown("### 📈 Payment Breakdown")
        
        # Create pie chart for payment breakdown
        fig_pie = go.Figure(data=[
            go.Pie(
                labels=['Principal', 'Interest'],
                values=[actual_loan, total_interest],
                hole=0.5,
                marker_colors=['#1E88E5', '#FFC107']
            )
        ])
        
        fig_pie.update_layout(
            title="Principal vs Interest Distribution",
            showlegend=True
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Year-wise payment schedule
        st.markdown("### 📅 Year-wise Payment Schedule")
        
        # Calculate year-wise data
        years = np.arange(1, loan_tenure + 1)
        yearly_payment = monthly_emi * 12
        balance = np.zeros(loan_tenure)
        
        remaining_balance = actual_loan
        for i in range(loan_tenure):
            interest_yearly = remaining_balance * (interest_rate / 100)
            principal_yearly = yearly_payment - interest_yearly
            remaining_balance -= principal_yearly
            balance[i] = remaining_balance
        
        # Create amortization schedule chart
        fig_schedule = go.Figure()
        
        fig_schedule.add_trace(go.Scatter(
            x=years,
            y=balance,
            name='Outstanding Balance',
            line=dict(color='#1E88E5')
        ))
        
        fig_schedule.update_layout(
            title='Outstanding Loan Balance Over Time',
            xaxis_title='Year',
            yaxis_title='Outstanding Balance (₹)',
            showlegend=True
        )
        
        st.plotly_chart(fig_schedule, use_container_width=True)
        
        # Additional Information
        with st.expander("💡 Additional Details"):
            st.markdown(f"""
            - **Loan Amount:** {format_currency(actual_loan)}
            - **Down Payment:** {format_currency(down_payment)}
            - **Interest Rate:** {interest_rate}% per annum
            - **Loan Tenure:** {loan_tenure} years
            - **Monthly EMI:** {format_currency(monthly_emi)}
            - **Total Interest:** {format_currency(total_interest)}
            - **Total Payment:** {format_currency(total_payment)}
            """)
        
        # EMI Tips
        st.info("""
        **Tips to reduce your EMI:**
        - Make a larger down payment
        - Opt for a longer loan tenure
        - Look for lower interest rates
        - Consider pre-payment options
        """)

if __name__ == "__main__":
    app()
