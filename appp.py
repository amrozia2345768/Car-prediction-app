import streamlit as st
import pickle
import numpy as np
import os

# Page configuration
st.set_page_config(page_title="Car Price Predictor", page_icon="🚗")

# Title
st.title("🚗 Car Price Prediction App")

# Show current working directory
st.write("📁 Working directory:", os.getcwd())

# Load the model
model_path = 'car_price_model.pkl'

if not os.path.exists(model_path):
    st.error(f"❌ Model file not found at: {os.path.abspath(model_path)}")
    st.stop()
else:
    st.success(f"✅ Model file found at: {os.path.abspath(model_path)}")

# Load model
try:
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    st.success("🎉 Model loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

# Input fields
st.subheader("🚗 Enter Car Details")

present_price = st.number_input("Present Price (in lakhs)", min_value=0.0, value=5.0, step=0.5)
driven_kms = st.number_input("Kilometers Driven", value=50000)
owner = st.selectbox("Number of Previous Owners", [0, 1, 2, 3])
year = st.number_input("Year of Purchase", min_value=1990, max_value=2025, value=2015)
car_age = 2025 - year

fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
fuel_type_petrol = 1 if fuel_type == "Petrol" else 0
fuel_type_diesel = 1 if fuel_type == "Diesel" else 0

selling_type = st.selectbox("Seller Type", ["Individual", "Dealer"])
selling_type_individual = 1 if selling_type == "Individual" else 0

transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
transmission_manual = 1 if transmission == "Manual" else 0

# Predict button
if st.button("Predict Price"):
    input_data = np.array([[present_price, driven_kms, owner, car_age,
                            fuel_type_diesel, fuel_type_petrol,
                            selling_type_individual, transmission_manual]])
    
    try:
        prediction = model.predict(input_data)
        st.success(f"💰 Predicted Car Price: ₹ {prediction[0]:,.2f} lakhs")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
