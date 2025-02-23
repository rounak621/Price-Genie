import pickle
import numpy as np
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

class BangaloreHousePricePredictor:
    def __init__(self, root):
        self.root = root
        self.root.title("Bangalore House Price Predictor")
        self.root.geometry("800x800")
        
        # Configure style
        self.configure_styles()
        
        # Create gradient background
        self.create_gradient_background()
        
        # Create card-like main frame
        main_frame = ttk.Frame(root, style='Card.TFrame', padding="30")
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title with decorative elements
        title_frame = ttk.Frame(main_frame, style='Card.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        title_label = ttk.Label(title_frame, 
                              text="🏠 Bangalore House Price Predictor",
                              style='Title.TLabel')
        title_label.pack()
        
        # Separator below title
        ttk.Separator(main_frame, orient='horizontal').grid(row=1, column=0, 
                                                          columnspan=2, sticky='ew', pady=(0, 20))
        
        # Input section
        input_frame = ttk.Frame(main_frame, style='Card.TFrame')
        input_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=20)
        
        # Initialize variables
        self.area_var = tk.StringVar()
        self.bhk_var = tk.StringVar()
        self.bath_var = tk.StringVar()
        
        # Area input with icon
        self.create_input_field(input_frame, "📏 Area (square feet):", 0, self.area_var)
        
        # BHK input
        self.create_input_field(input_frame, "🛏️ BHK (number of bedrooms):", 1, self.bhk_var)
        
        # Bathrooms input
        self.create_input_field(input_frame, "🚿 Number of bathrooms:", 2, self.bath_var)
        
        # Location dropdown
        location_label = ttk.Label(input_frame, text="📍 Location:", style='Input.TLabel')
        location_label.grid(row=3, column=0, padx=5, pady=15, sticky=tk.W)
        
        self.location_var = tk.StringVar()
        locations = sorted(self.get_location_map().values())
        location_dropdown = ttk.Combobox(input_frame, textvariable=self.location_var,
                                       values=locations, width=30, style='Combo.TCombobox',
                                       state='readonly')
        location_dropdown.grid(row=3, column=1, padx=5, pady=15, sticky=tk.W)
        
        # Predict button
        predict_btn = ttk.Button(main_frame, text="Calculate Price 🔍",
                               command=self.predict_price, style='Predict.TButton')
        predict_btn.grid(row=3, column=0, columnspan=2, pady=30)
        
        # Result section
        result_frame = ttk.LabelFrame(main_frame, text="Prediction Result",
                                    padding="20", style='Result.TLabelframe')
        result_frame.grid(row=4, column=0, columnspan=2, pady=(0, 20), sticky='ew')
        
        self.result_var = tk.StringVar()
        result_label = ttk.Label(result_frame, textvariable=self.result_var,
                               style='Result.TLabel')
        result_label.pack(expand=True)
        
        # Load model
        self.load_model()

    def configure_styles(self):
        style = ttk.Style()
        
        # Configure colors
        bg_color = '#f5f5f5'
        accent_color = '#1e88e5'
        text_color = '#212121'
        
        style.configure('Card.TFrame', background=bg_color)
        
        # Title style
        style.configure('Title.TLabel',
                       font=('Helvetica', 24, 'bold'),
                       foreground=text_color,
                       background=bg_color)
        
        # Input label style
        style.configure('Input.TLabel',
                       font=('Helvetica', 12),
                       foreground=text_color,
                       background=bg_color)
        
        # Entry style
        style.configure('Custom.TEntry',
                       fieldbackground='white',
                       borderwidth=1)
        
        # Button style
        style.configure('Predict.TButton',
                       font=('Helvetica', 14),
                       padding=10)
        
        # Result frame style
        style.configure('Result.TLabelframe',
                       background=bg_color)
        style.configure('Result.TLabelframe.Label',
                       font=('Helvetica', 12, 'bold'),
                       background=bg_color,
                       foreground=text_color)
        
        # Result label style
        style.configure('Result.TLabel',
                       font=('Helvetica', 18, 'bold'),
                       foreground=accent_color,
                       background=bg_color)

    def create_gradient_background(self):
        canvas = tk.Canvas(self.root, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create gradient effect
        colors = ['#e3f2fd', '#bbdefb', '#90caf9']
        height = 800
        width = 800
        
        for i in range(len(colors) - 1):
            canvas.create_rectangle(0, i * height / len(colors),
                                 width, (i + 1) * height / len(colors),
                                 fill=colors[i], outline=colors[i])

    def create_input_field(self, parent, label_text, row, variable):
        label = ttk.Label(parent, text=label_text, style='Input.TLabel')
        label.grid(row=row, column=0, padx=5, pady=15, sticky=tk.W)
        
        entry = ttk.Entry(parent, textvariable=variable, width=30, style='Custom.TEntry')
        entry.grid(row=row, column=1, padx=5, pady=15, sticky=tk.W)
        return entry

    def load_model(self):
        """Load the pre-trained model"""
        try:
            model_path = Path(__file__).parent.parent / 'banglore_home_prices_model.pickle'
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {str(e)}")
            self.root.quit()

    def get_location_map(self):
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

    def format_price(self, price):
        """Format price in lakhs with Indian number system"""
        price_in_lakhs = abs(price)
        
        # Format with two decimal places
        formatted_price = f"{price_in_lakhs:.2f}"
        
        # Split into whole and decimal parts
        whole, decimal = formatted_price.split('.')
        
        # Format whole part with commas (Indian system)
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

    def predict_price(self):
        """Make price prediction based on user inputs"""
        try:
            # Validate inputs
            try:
                area = float(self.area_var.get())
                bhk = int(self.bhk_var.get())
                bath = int(self.bath_var.get())
                location = self.location_var.get()
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numeric values for area, BHK, and bathrooms")
                return
            
            if not location:
                messagebox.showerror("Error", "Please select a location")
                return
            
            if area <= 0 or bhk <= 0 or bath <= 0:
                messagebox.showerror("Error", "Please enter positive values")
                return
            
            # Prepare input features
            x = np.zeros(244)  # Model expects 244 features
            
            # Set basic features
            x[0] = area
            x[1] = bath
            x[2] = bhk
            
            # Set location feature
            location_map_inv = {v: k for k, v in self.get_location_map().items()}
            loc_index = location_map_inv[location]
            x[3 + loc_index] = 1
            
            # Make prediction
            predicted_price = self.model.predict([x])[0]
            
            # Display result
            self.result_var.set(f"Estimated Price: {self.format_price(predicted_price)}")
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = BangaloreHousePricePredictor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
