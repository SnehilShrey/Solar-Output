import streamlit as st
import pickle
import numpy as np
import base64

# Load the trained model
model_filename = 'solar_output_model.sav'
with open(model_filename, 'rb') as file:
    model = pickle.load(file)

# Function to set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded_string}");
        background-size: cover;
    }}
    .cloud-box {{
        background-color: rgba(221, 243, 254, 0.6);
        padding: 15px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
        text-align: center;
        font-size: 36px;
        font-weight: bold;
        margin-bottom: 10px; 
    }}
    .subheading-box {{
        background-color: rgba(254, 249, 215, 0.6);
        padding: 10px;
        border-radius: 10px;
        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.1);
        text-align: left;
        font-size: 16px;
        font-weight: bold;
        margin-bottom: 35px; 
    }}
    .input-container {{
        display: flex;
        flex-direction: column;
        margin-top: -5px;
        margin-bottom: -45px;
    }}
    .input-block, .output-block {{
        background-color: rgba(255, 255, 255, 0.8);
        padding: 8px; 
        border-radius: 10px;
        text-align: left;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

# Set background image
set_background("background.jpg")

# Streamlit UI
st.markdown('<div class="cloud-box">Solar Output Tracker</div>', unsafe_allow_html=True)
st.markdown('<div class="subheading-box">Enter the environmental parameters to predict solar power output.</div>', unsafe_allow_html=True)

# User inputs
parameters = [
    "Temperature (°C)", "Relative Humidity (%)", "Mean Sea Level Pressure (hPa)", "Total Precipitation (mm)",
    "Snowfall Amount (mm)", "Total Cloud Cover (%)", "High Cloud Cover (%)", "Medium Cloud Cover (%)",
    "Low Cloud Cover (%)", "Shortwave Radiation Backwards (W/m²)", "Wind Speed at 10m (m/s)",
    "Wind Direction at 10m (°)", "Wind Speed at 80m (m/s)", "Wind Direction at 80m (°)",
    "Wind Speed at 900mb (m/s)", "Wind Direction at 900mb (°)", "Wind Gust at 10m (m/s)",
    "Angle of Incidence (°)", "Zenith Angle (°)", "Azimuth Angle (°)"
]

inputs = []
for param in parameters:
    with st.container():
        st.markdown(f'<div class="input-container"><div class="input-block">{param}</div>', unsafe_allow_html=True)
        value = st.number_input("", key=param)
        st.markdown('</div>', unsafe_allow_html=True)
        inputs.append(value)

def predict_output():
    input_data = np.array([inputs])
    prediction = model.predict(input_data)
    return prediction[0]

if st.button("Predict Output"):
    output = predict_output()
    st.markdown(f'<div class="output-block">Predicted Solar Output: {output:.2f} kWh</div>', unsafe_allow_html=True)
