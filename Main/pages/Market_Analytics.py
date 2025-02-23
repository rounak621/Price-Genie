import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path

def format_price_lakhs(price):
    return f"₹{price:.2f} L"

def generate_sample_data():
    # Generate sample data for visualizations
    locations = [
        "Whitefield", "HSR Layout", "Electronic City", "Marathahalli",
        "Koramangala", "Indiranagar", "JP Nagar", "Bannerghatta Road"
    ]
    
    np.random.seed(42)
    n_samples = 100
    
    data = {
        'location': np.random.choice(locations, n_samples),
        'area': np.random.uniform(600, 3000, n_samples),
        'bhk': np.random.choice([1, 2, 3, 4], n_samples),
        'price': np.random.uniform(30, 200, n_samples),  # in lakhs
        'price_per_sqft': np.random.uniform(4000, 8000, n_samples),
        'month': pd.date_range(start='2023-01-01', periods=n_samples, freq='D')
    }
    
    return pd.DataFrame(data)

def app():
    st.title("📊 Market Analytics")
    
    # Generate sample data
    df = generate_sample_data()
    
    # Sidebar for filters
    st.sidebar.title("Filters")
    selected_locations = st.sidebar.multiselect(
        "Select Locations",
        options=sorted(df['location'].unique()),
        default=sorted(df['location'].unique())[:5]
    )
    
    min_area, max_area = st.sidebar.slider(
        "Area Range (sq ft)",
        float(df['area'].min()),
        float(df['area'].max()),
        (800.0, 2000.0)
    )
    
    # Filter data
    filtered_df = df[
        (df['location'].isin(selected_locations)) &
        (df['area'] >= min_area) &
        (df['area'] <= max_area)
    ]
    
    # Create tabs for different analyses
    tab1, tab2, tab3 = st.tabs(["Price Trends", "Location Analysis", "Configuration Analysis"])
    
    with tab1:
        st.subheader("Price Trends Over Time")
        
        # Monthly average price trend
        monthly_avg = filtered_df.groupby(filtered_df['month'].dt.to_period('M'))['price'].mean().reset_index()
        monthly_avg['month'] = monthly_avg['month'].astype(str)
        
        fig_trend = px.line(
            monthly_avg,
            x='month',
            y='price',
            title='Average Property Prices Over Time',
            labels={'price': 'Price (Lakhs)', 'month': 'Month'}
        )
        fig_trend.update_traces(line_color='#1E88E5')
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Price Distribution
        fig_dist = px.histogram(
            filtered_df,
            x='price',
            nbins=30,
            title='Price Distribution',
            labels={'price': 'Price (Lakhs)', 'count': 'Number of Properties'}
        )
        fig_dist.update_traces(marker_color='#1E88E5')
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with tab2:
        st.subheader("Location-wise Analysis")
        
        # Average price by location
        location_avg = filtered_df.groupby('location')['price'].agg(['mean', 'count']).reset_index()
        location_avg = location_avg.sort_values('mean', ascending=True)
        
        fig_location = go.Figure()
        fig_location.add_trace(go.Bar(
            y=location_avg['location'],
            x=location_avg['mean'],
            orientation='h',
            marker_color='#1E88E5',
            name='Average Price'
        ))
        
        fig_location.update_layout(
            title='Average Property Prices by Location',
            xaxis_title='Price (Lakhs)',
            yaxis_title='Location',
            height=400 + len(location_avg) * 20
        )
        st.plotly_chart(fig_location, use_container_width=True)
        
        # Price per sq ft by location
        st.subheader("Price per Square Foot Analysis")
        location_price_per_sqft = filtered_df.groupby('location')['price_per_sqft'].mean().sort_values(ascending=True)
        
        fig_price_sqft = px.bar(
            location_price_per_sqft,
            orientation='h',
            title='Average Price per Square Foot by Location',
            labels={'value': 'Price per sq ft (₹)', 'location': 'Location'}
        )
        fig_price_sqft.update_traces(marker_color='#1E88E5')
        st.plotly_chart(fig_price_sqft, use_container_width=True)
    
    with tab3:
        st.subheader("Configuration Analysis")
        
        # Average price by BHK
        bhk_avg = filtered_df.groupby('bhk')['price'].mean().reset_index()
        
        fig_bhk = px.bar(
            bhk_avg,
            x='bhk',
            y='price',
            title='Average Price by BHK',
            labels={'price': 'Price (Lakhs)', 'bhk': 'Number of Bedrooms'}
        )
        fig_bhk.update_traces(marker_color='#1E88E5')
        st.plotly_chart(fig_bhk, use_container_width=True)
        
        # Area vs Price Scatter Plot
        fig_scatter = px.scatter(
            filtered_df,
            x='area',
            y='price',
            color='bhk',
            title='Price vs Area by BHK',
            labels={'price': 'Price (Lakhs)', 'area': 'Area (sq ft)', 'bhk': 'BHK'}
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Key Insights
    st.subheader("💡 Key Market Insights")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_price = filtered_df['price'].mean()
        st.metric("Average Price", format_price_lakhs(avg_price))
        
    with col2:
        avg_price_sqft = filtered_df['price_per_sqft'].mean()
        st.metric("Avg Price/Sq ft", f"₹{avg_price_sqft:,.2f}")
        
    with col3:
        mom_change = 5.2  # This should be calculated from your data
        st.metric("Month-over-Month Change", f"{mom_change}%", delta=mom_change)
    
    # Market Summary
    st.info("""
    **Market Summary:**
    - Prices have shown an upward trend in premium locations
    - 3 BHK configurations remain the most popular
    - Properties in the 1000-1500 sq ft range have the highest demand
    """)

if __name__ == "__main__":
    app()
