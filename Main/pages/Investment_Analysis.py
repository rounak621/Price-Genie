import streamlit as st
import numpy as np
import pandas as pd

def calculate_roi(purchase_price, current_value, rental_income, years):
    """Calculate ROI for real estate investment"""
    total_return = current_value - purchase_price + (rental_income * 12 * years)
    roi = (total_return / purchase_price) * 100
    return roi

def calculate_rental_yield(property_value, monthly_rent):
    """Calculate annual rental yield"""
    annual_rent = monthly_rent * 12
    rental_yield = (annual_rent / property_value) * 100
    return rental_yield

def format_currency(amount):
    """Format amount in Indian currency"""
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

def main():
    st.title("💸 Investment Analysis")
    
    # Simple ROI Calculator
    st.header("Return on Investment Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        purchase_price = st.number_input(
            "Purchase Price (₹)",
            min_value=100000,
            max_value=100000000,
            value=5000000,
            step=100000
        )
        
        current_value = st.number_input(
            "Expected Value (₹)",
            min_value=100000,
            max_value=150000000,
            value=6000000,
            step=100000
        )
    
    with col2:
        monthly_rent = st.number_input(
            "Monthly Rent (₹)",
            min_value=0,
            max_value=1000000,
            value=25000,
            step=1000
        )
        
        investment_period = st.number_input(
            "Period (Years)",
            min_value=1,
            max_value=30,
            value=5,
            step=1
        )
    
    if st.button("Calculate Returns", use_container_width=True):
        roi = calculate_roi(purchase_price, current_value, monthly_rent, investment_period)
        rental_yield = calculate_rental_yield(purchase_price, monthly_rent)
        total_return = current_value - purchase_price + (monthly_rent * 12 * investment_period)
        
        # Display results
        st.markdown("### Investment Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total ROI", f"{roi:.1f}%", f"{roi/investment_period:.1f}% per year")
        with col2:
            st.metric("Total Returns", format_currency(total_return))
        with col3:
            st.metric("Rental Yield", f"{rental_yield:.1f}%")
        
        # Breakdown
        st.markdown("### Returns Breakdown")
        appreciation = current_value - purchase_price
        rental_returns = monthly_rent * 12 * investment_period
        
        st.info(f"""
        🏠 **Property Value Appreciation:** {format_currency(appreciation)}
        💰 **Rental Income:** {format_currency(rental_returns)}
        """)
    
    # Investment Options
    st.markdown("---")
    st.header("Investment Comparison")
    
    investment_amount = st.number_input(
        "Investment Amount (₹)",
        min_value=500000,
        max_value=10000000,
        value=2000000,
        step=100000
    )
    
    # Simplified comparison table
    comparison_data = {
        'Investment Type': ['Real Estate', 'Fixed Deposit', 'Mutual Funds', 'Gold'],
        'Expected Returns': ['8-12%', '6-7%', '12-15%', '8-10%'],
        'Risk Level': ['Medium', 'Low', 'Medium-High', 'Medium'],
        'Liquidity': ['Low', 'Medium', 'High', 'High']
    }
    
    df = pd.DataFrame(comparison_data)
    st.table(df)
    
    # Investment Tips
    with st.expander("💡 Investment Tips"):
        st.markdown("""
        1. **Diversify Investments**
           - Mix different investment types
           - Don't invest everything in one place
           - Balance risk and returns
        
        2. **Research Thoroughly**
           - Check location growth potential
           - Verify all legal documents
           - Understand market trends
        
        3. **Plan Finances**
           - Calculate all costs involved
           - Consider tax implications
           - Keep emergency funds
        """)

if __name__ == "__main__":
    main()
