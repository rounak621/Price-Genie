# import pickle
# import numpy as np
# import pandas as pd
# from pathlib import Path

# def load_model():
#     """Load the pre-trained model and analyze its structure"""
#     model_path = Path(__file__).parent.parent / 'banglore_home_prices_model.pickle'
#     try:
#         with open(model_path, 'rb') as f:
#             model = pickle.load(f)
#             if hasattr(model, 'coef_'):
#                 print("Model coefficients shape:", model.coef_.shape)
#                 print("Model intercept:", model.intercept_)
#                 return model, len(model.coef_)
#             else:
#                 raise ValueError("Loaded model does not appear to be a valid LinearRegression model")
#     except Exception as e:
#         print(f"Error loading model: {str(e)}")
#         raise

# def get_location_map():
#     """Map location indices to readable names"""
#     return {
#         0: "Whitefield", 10: "HSR Layout", 20: "Electronic City", 
#         30: "Marathahalli", 40: "Koramangala", 50: "Indiranagar", 
#         60: "JP Nagar", 70: "Bannerghatta Road", 80: "Sarjapur Road", 
#         90: "Hebbal", 100: "Banashankari", 110: "BTM Layout", 
#         120: "Jayanagar", 130: "Bellandur", 140: "CV Raman Nagar",
#         150: "Malleswaram", 160: "Old Airport Road", 170: "Rajaji Nagar", 
#         180: "Yelahanka", 190: "KR Puram", 200: "Mahadevapura", 
#         210: "Thanisandra", 220: "Kengeri", 230: "Hoodi"
#     }

# def get_data_columns(n_features):
#     """Return data columns with the exact number of features"""
#     columns = ['area', 'bath', 'bhk']
#     for i in range(n_features - 3):  # -3 for area, bath, bhk
#         columns.append(f'location_{i}')
#     return columns

# def format_price_in_lakhs(price):
#     """Format price in Lakhs with proper formatting"""
#     # Model's output is already in lakhs
#     price_in_lakhs = abs(price)  # Handle negative predictions by taking absolute value
    
#     # Format with two decimal places
#     formatted_price = f"{price_in_lakhs:.2f}"
    
#     # Split into whole and decimal parts
#     whole, decimal = formatted_price.split('.')
    
#     # Format whole part with commas (Indian system)
#     s = whole
#     l = len(s)
#     if l > 3:
#         formatted = s[-3:]
#         s = s[:-3]
#         while s:
#             formatted = s[-2:] + ',' + formatted if s[-2:] else s[-1] + ',' + formatted
#             s = s[:-2]
#     else:
#         formatted = s
        
#     # Add decimal part back
#     final_price = f"{formatted}.{decimal}"
    
#     return f"₹{final_price} Lakhs"

# def predict_home_price():
#     print("\n=== Bangalore House Price Predictor ===\n")
    
#     # Load the model and get data columns
#     print("Loading model...")
#     model, n_features = load_model()
#     data_columns = get_data_columns(n_features)
#     location_map = get_location_map()
    
#     # Get locations from data columns
#     location_columns = [col for col in data_columns if col.startswith('location_')]
#     locations = [loc.replace('location_', '') for loc in location_columns]
    
#     # Get user inputs
#     try:
#         # Get area
#         while True:
#             try:
#                 area = float(input("Enter Area (in square feet): "))
#                 if area <= 0:
#                     print("Area must be a positive number")
#                     continue
#                 break
#             except ValueError:
#                 print("Please enter a valid number")
        
#         # Get BHK
#         while True:
#             try:
#                 bhk = int(input("Enter number of BHK: "))
#                 if bhk <= 0:
#                     print("BHK must be a positive number")
#                     continue
#                 break
#             except ValueError:
#                 print("Please enter a valid number")
        
#         # Get bathrooms
#         while True:
#             try:
#                 bath = int(input("Enter number of bathrooms: "))
#                 if bath <= 0:
#                     print("Number of bathrooms must be a positive number")
#                     continue
#                 break
#             except ValueError:
#                 print("Please enter a valid number")
        
#         # Print available locations
#         print("\nAvailable locations:")
#         locations = sorted(location_map.items(), key=lambda x: x[1])
#         for i, (loc_index, loc_name) in enumerate(locations, 1):
#             print(f"{i}. {loc_name}")
        
#         # Get location
#         while True:
#             try:
#                 loc_index = int(input("\nEnter location number from the above list: ")) - 1
#                 if 0 <= loc_index < len(locations):
#                     location_index, location = sorted(location_map.items(), key=lambda x: x[1])[loc_index]
#                     break
#                 else:
#                     print("Please enter a valid location number")
#             except ValueError:
#                 print("Please enter a valid number")
        
#         # Prepare input data with exact number of features and scale appropriately
#         x = np.zeros(len(data_columns))
#         # Scale area to match model's expectations
#         x[0] = area / 1000  # Convert to 1000 sq ft units
#         x[1] = bath
#         x[2] = bhk
#         # Add location using the correct index
#         loc_feature_index = 3 + location_index
#         x[loc_feature_index] = 1
        
#         print("\nDebug Information:")
#         print(f"Input vector shape: {x.shape}")
#         print(f"Location '{location}' set at index: {loc_feature_index}")
#         print(f"Input vector preview: area={x[0]}, bath={x[1]}, bhk={x[2]}")
#         non_zero = np.nonzero(x)[0]
#         print(f"Non-zero feature indices: {non_zero}")
        
#         # Make prediction
#         predicted_price = model.predict([x])[0]
        
#         # Display result
#         print("\n" + "="*50)
#         print("Prediction Results:")
#         print(f"Area: {area} sq ft")
#         print(f"BHK: {bhk}")
#         print(f"Bathrooms: {bath}")
#         print(f"Location: {location}")
#         print(f"\nEstimated Price: {format_price_in_lakhs(predicted_price)}")
#         print("="*50)
        
#     except Exception as e:
#         print(f"\nAn error occurred: {str(e)}")
#         print("Please try again")

# if __name__ == "__main__":
#     predict_home_price()
