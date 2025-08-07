import streamlit as st
import numpy as np

def predict_diabetes(bmi, age, gen_hlth, high_bp):
    """Realistic prediction with proper scaling"""
    # Normalize inputs (0-1 range)
    scaled_bmi = min(bmi, 40) / 40  # Cap BMI at 40 for calculation
    scaled_age = (age - 1) / 12      # Age groups 1-13 → 0-1
    scaled_health = (gen_hlth - 1) / 4
    
    # Debugging: Print normalized values
    print(f"Scaled BMI: {scaled_bmi}, Scaled Age: {scaled_age}, Scaled Health: {scaled_health}, High BP: {high_bp}")

    # Weighted factors (sum < 1)
    risk_score = (
        (scaled_bmi * 0.4) + 
        (scaled_age * 0.3) + 
        (scaled_health * 0.2) + 
        (high_bp * 0.1)
    )
    
    # Debugging: Print risk score before sigmoid
    print(f"Risk Score (before sigmoid): {risk_score}")

    # Adjusted sigmoid to prevent extremes
    probability = 1 / (1 + np.exp(-10 * (risk_score - 0.5)))
    
    # Ensure reasonable bounds (5%-95%)
    return min(max(probability, 0.05), 0.95)

# Streamlit UI
st.title("Realistic Diabetes Risk Assessment")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        bmi = st.slider("BMI", 12.0, 50.0, 22.0, step=0.1)
        age = st.slider("Age Group", 1, 13, 3,
                       help="1:18-24, 2:25-29, ..., 13:80+")
    
    with col2:
        gen_hlth = st.select_slider("General Health", 
                                  options=[1,2,3,4,5],
                                  value=2,
                                  help="1=Excellent, 5=Poor")
        high_bp = st.radio("High BP", ["No", "Yes"])
    
    if st.form_submit_button("Calculate"):
        high_bp_num = 1 if high_bp == "Yes" else 0
        risk = predict_diabetes(bmi, age, gen_hlth, high_bp_num)
        
        # Display
        st.subheader("Results")
        st.metric("Risk Probability", f"{risk*100:.1f}%")
        
        # Visual indicator
        st.progress(risk)
        
        # Interpretation
        if risk > 0.7:
            st.error("High risk - Consult a doctor")
        elif risk > 0.4:
            st.warning("Moderate risk - Monitor regularly")
        else:
            st.success("Low risk - Maintain healthy habits")

st.caption("Note: This screening tool is not a medical diagnosis")
