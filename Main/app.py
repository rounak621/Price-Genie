import streamlit as st
import pickle
import numpy as np
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Bangalore House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    .stApp {
        max-width: 800px;
        margin: 0 auto;
    }
    .st-emotion-cache-16txtl3 {
        padding: 2rem;
    }
    .prediction-result {
        padding: 20px;
        border-radius: 10px;
        background: #f0f8ff;
        margin: 20px 0;
        text-align: center;
    }
    .title {
        text-align: center;
        color: #1E88E5;
        margin-bottom: 2rem;
    }
    .input-container {
        margin: 1rem auto;
        max-width: 500px;
    }
    .stButton {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def load_model():
    """Load the pre-trained model"""
    try:
        model_path = Path(__file__).parent.parent / 'banglore_home_prices_model.pickle'
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except Exception as e:
        st.error(f"Failed to load model: {str(e)}")
        return None

def get_location_map():
    """Map location indices to readable names"""
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

def main():
    # Title
    st.markdown("<h1 class='title'>🏠 Bangalore House Price Predictor</h1>", unsafe_allow_html=True)
    
    # Load model
    model = load_model()
    if model is None:
        return
    
    # Container for inputs with better spacing
    with st.container():
        st.markdown("<div class='input-container'>", unsafe_allow_html=True)
        
        # Area input with validation
        area = st.number_input(
            "📏 Area (square feet)",
            min_value=100.0,
            max_value=10000.0,
            value=1000.0,
            step=100.0,
            help="Enter the total area in square feet"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # BHK input
        bhk = st.number_input(
            "🛏️ Number of Bedrooms (BHK)",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
            help="Enter the number of bedrooms"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Bathrooms input
        bath = st.number_input(
            "🚿 Number of Bathrooms",
            min_value=1,
            max_value=10,
            value=2,
            step=1,
            help="Enter the number of bathrooms"
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Location dropdown
        locations = sorted(get_location_map().values())
        location = st.selectbox(
            "📍 Location",
            options=locations,
            help="Select the location in Bangalore"
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Add some spacing
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Center the predict button
    predict_button = st.button("🔍 Predict Price", use_container_width=True)
    
    if predict_button:
        try:
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
            
            # Display result with animation
            with st.markdown("<div class='prediction-result'>", unsafe_allow_html=True):
                st.markdown("### Prediction Results")
                st.markdown("---")
                
                # Display inputs for confirmation
                st.markdown(f"**Area:** {area} sq ft")
                st.markdown(f"**BHK:** {bhk}")
                st.markdown(f"**Bathrooms:** {bath}")
                st.markdown(f"**Location:** {location}")
                st.markdown("---")
                
                # Display predicted price with larger font
                st.markdown(f"<h2 style='color: #1E88E5; margin-top: 1rem;'>Estimated Price: {format_price(predicted_price)}</h2>", 
                          unsafe_allow_html=True)
            
            # Add disclaimer
            st.info("Note: This is an estimated price based on historical data and may vary from actual market prices.")
            
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
