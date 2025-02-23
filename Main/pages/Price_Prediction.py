import streamlit as st
import pickle
import numpy as np
from pathlib import Path

def load_model():
    try:
        model_path = Path(__file__).parent.parent.parent / 'banglore_home_prices_model.pickle'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None

def get_location_map():
    return {
        0: "Whitefield", 10: "HSR Layout", 20: "Electronic City", 
        30: "Marathahalli", 40: "Koramangala", 50: "Indiranagar", 
        60: "JP Nagar", 70: "Bannerghatta Road", 80: "Sarjapur Road", 
        90: "Hebbal", 100: "Banashankari", 110: "BTM Layout", 
        120: "Jayanagar", 130: "Bellandur", 140: "CV Raman Nagar",
        150: "Malleswaram", 160: "Old Airport Road", 170: "Rajaji Nagar", 
        180: "Yelahanka", 190: "KR Puram", 200: "Mahadevapura", 
        210: "Thanisandra", 220: "Kengeri", 230: "Hoodi"
    }

def format_price(price):
    """Format price in lakhs with Indian number system"""
    price_in_lakhs = abs(price)
    formatted_price = f"{price_in_lakhs:.2f}"
    whole, decimal = formatted_price.split('.')
    
    s = whole
    l = len(s)
    if l > 3:
        formatted = s[-3:]
        s = s[:-3]
        while s:
            formatted = s[-2:] + ',' + formatted if s[-2:] else s[-1] + ',' + formatted
            s = s[:-2]
    else:
        formatted = s
    
    final_price = f"{formatted}.{decimal}"
    return f"₹{final_price} Lakhs"

def app():
    st.title("🏠 House Price Prediction")
    
    # Create columns for input fields
    col1 = st.container()
    
    with col1:
        with st.expander("📐 Basic Details", expanded=True):
            area = st.number_input(
                "Area (square feet)",
                min_value=100.0,
                max_value=10000.0,
                value=1000.0,
                step=100.0
            )
            
            col_bhk, col_bath = st.columns(2)
            with col_bhk:
                bhk = st.number_input(
                    "Number of Bedrooms (BHK)",
                    min_value=1,
                    max_value=10,
                    value=2
                )
            with col_bath:
                bath = st.number_input(
                    "Number of Bathrooms",
                    min_value=1,
                    max_value=10,
                    value=2
                )
        
        with st.expander("🏢 Property Details", expanded=True):
            property_age = st.slider(
                "Property Age (years)",
                min_value=0,
                max_value=50,
                value=5
            )
            
            col_floor, col_total = st.columns(2)
            with col_floor:
                floor_num = st.number_input(
                    "Floor Number",
                    min_value=0,
                    max_value=50,
                    value=2
                )
            with col_total:
                total_floors = st.number_input(
                    "Total Floors",
                    min_value=1,
                    max_value=50,
                    value=5
                )
            
            furnishing = st.selectbox(
                "Furnishing Status",
                ["Unfurnished", "Semi-furnished", "Fully Furnished"]
            )
            
            parking = st.selectbox(
                "Car Parking Available",
                ["Yes", "No"]
            )
            
            facing = st.selectbox(
                "Property Facing",
                ["North", "South", "East", "West", "North East", "North West", "South East", "South West"]
            )
        
        with st.expander("📍 Location Details", expanded=True):
            locations = sorted(get_location_map().values())
            location = st.selectbox(
                "Location",
                locations
            )
            
            amenities = st.multiselect(
                "Nearby Amenities",
                ["Metro Station", "Bus Stop", "School", "Hospital", "Shopping Mall", "Park"],
                default=["Metro Station"]
            )
    
    # Predict Button
    if st.button("Calculate Price", type="primary", use_container_width=True):
        try:
            model = load_model()
            if model is None:
                return
            
            # Prepare input features
            x = np.zeros(244)  # Model expects 244 features
            
            # Set basic features
            x[0] = area
            x[1] = bath
            x[2] = bhk
            
            # Set location feature
            location_map_inv = {v: k for k, v in get_location_map().items()}
            loc_index = location_map_inv[location]
            x[3 + loc_index] = 1
            
            # Make prediction
            predicted_price = model.predict([x])[0]
            
            # Display result in a nice card
            st.markdown("---")
            col_result_left, col_result_right = st.columns([2, 1])
            
            with col_result_left:
                st.markdown("### 📊 Prediction Results")
                st.markdown(f"**Location:** {location}")
                st.markdown(f"**Area:** {area} sq ft")
                st.markdown(f"**Configuration:** {bhk} BHK, {bath} Baths")
                if len(amenities) > 0:
                    st.markdown(f"**Nearby:** {', '.join(amenities)}")
            
            with col_result_right:
                st.markdown("### Estimated Price")
                st.markdown(f"<h2 style='color: #1E88E5;'>{format_price(predicted_price)}</h2>", 
                          unsafe_allow_html=True)
            
            # Additional price insights
            st.markdown("### 💡 Price Insights")
            col_insights1, col_insights2 = st.columns(2)
            
            with col_insights1:
                price_per_sqft = predicted_price * 100000 / area  # Convert lakhs to rupees
                st.metric("Price per sq ft", f"₹{price_per_sqft:,.2f}")
            
            with col_insights2:
                avg_price = 6000  # This should be calculated from your data
                price_diff = ((price_per_sqft - avg_price) / avg_price) * 100
                st.metric("Comparison to Area Average", 
                         f"{abs(price_diff):.1f}% {'above' if price_diff > 0 else 'below'} average")
            
            st.info("Note: This is an estimated price based on historical data and may vary from actual market prices.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app()
