import streamlit as st

# Page config
st.set_page_config(
    page_title="PriceGenie - Bangalore House Price Predictor",
    page_icon="🏠",
    layout="wide"
)

# Simple custom CSS for minimal styling
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        color: #1E88E5;
    }
    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .card {
        padding: 1rem;
        border-radius: 8px;
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1 class='main-title'>🏠 PriceGenie</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Your Smart Bangalore Real Estate Assistant</p>", unsafe_allow_html=True)

# Main Features
st.subheader("📱 Quick Access")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container():
        st.markdown("### 🎯 Price Prediction")
        st.write("Get instant house price estimates based on location and features")
        st.link_button("Predict Price", "Price_Prediction", use_container_width=True)

with col2:
    with st.container():
        st.markdown("### 📊 Market Analysis")
        st.write("Explore price trends and compare different locations")
        st.link_button("View Analytics", "Market_Analytics", use_container_width=True)

with col3:
    with st.container():
        st.markdown("### 💰 EMI Calculator")
        st.write("Plan your home loan and calculate monthly payments")
        st.link_button("Calculate EMI", "EMI_Calculator", use_container_width=True)

with col4:
    with st.container():
        st.markdown("### 💸 Investment")
        st.write("Analyze ROI, rental yields, and investment options,Commodities")
        st.link_button("Investment Analysis", "Investment_Analysis", use_container_width=True)

# Key Features Section
st.markdown("---")
st.subheader("✨ Key Features")

features_col1, features_col2 = st.columns(2)

with features_col1:
    st.markdown("""
    ### Input Details
    - Enter property size and location
    - Specify number of bedrooms & bathrooms
    - Add amenity information
    """)
    
    st.markdown("""
    ### Get Results
    - Instant price predictions
    - Market comparisons
    - Price trends analysis
    """)

with features_col2:
    st.markdown("""
    ### Smart Analytics
    - Location-wise price trends
    - Property size analysis
    - Investment projections
    """)
    
    st.markdown("""
    ### Financial Planning
    - EMI calculations
    - ROI analysis
    - Investment comparison
    """)

# Benefits
st.markdown("---")
st.subheader("💡 Benefits")

benefit_cols = st.columns(4)

with benefit_cols[0]:
    st.markdown("#### Accurate")
    st.write("ML-powered predictions")

with benefit_cols[1]:
    st.markdown("#### Fast")
    st.write("Instant results")

with benefit_cols[2]:
    st.markdown("#### Reliable")
    st.write("Verified data")

with benefit_cols[3]:
    st.markdown("#### Free")
    st.write("No hidden costs")

# Quick Tips
st.markdown("---")
with st.expander("📌 Quick Tips for Home Buyers"):
    tip_col1, tip_col2 = st.columns(2)
    
    with tip_col1:
        st.markdown("""
        **Location Research**
        - Check connectivity
        - Nearby amenities
        - Future development
        
        **Price Analysis**
        - Compare similar properties
        - Check historical trends
        - Evaluate per sq ft cost
        """)
    
    with tip_col2:
        st.markdown("""
        **Documentation**
        - Verify property papers
        - Check builder reputation
        - Confirm approvals
        
        **Financial Planning**
        - Plan down payment
        - Compare loan options
        - Analyze investment returns
        """)

# Footer
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div style='text-align: center;'>
        <p>Made with ❤️ by PriceGenie</p>
        <p style='font-size: 0.8rem; color: #666;'>Using AI for smarter real estate decisions</p>
    </div>
    """, unsafe_allow_html=True)
