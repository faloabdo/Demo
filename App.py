import streamlit as st
import numpy as np
import time

# Show loading progress immediately
st.title("Diabetes Risk Prediction Tool")
progress_bar = st.progress(0)
status_text = st.empty()

# Simulate model loading (remove in production)
for i in range(100):
    progress_bar.progress(i + 1)
    status_text.text(f"Loading... {i+1}%")
    time.sleep(0.02)  # Remove this in production

# Minimal working example
def predict_diabetes(bmi, age, gen_hlth, high_bp):
    """Mock prediction function"""
    risk = (bmi * 0.08 + age * 0.05 + gen_hlth * 0.07 + high_bp * 0.06)
    return min(max(risk, 0), 1)

# Input widgets
with st.form("prediction_form"):
    bmi = st.slider("BMI", 12.0, 50.0, 25.0)
    age = st.slider("Age Group", 1, 13, 7)
    gen_hlth = st.selectbox("General Health (1-5)", options=[1,2,3,4,5], index=2)
    high_bp = st.radio("High Blood Pressure", options=[0, 1], format_func=lambda x: "Yes" if x else "No")
    
    if st.form_submit_button("Predict"):
        try:
            risk = predict_diabetes(bmi, age, gen_hlth, high_bp)
            st.success(f"Predicted Risk: {risk*100:.1f}%")
            
            if risk > 0.7:
                st.error("High risk - Please consult a doctor")
            elif risk > 0.3:
                st.warning("Moderate risk")
            else:
                st.success("Low risk")
                
        except Exception as e:
            st.error(f"Error in prediction: {str(e)}")

progress_bar.empty()
status_text.empty()
