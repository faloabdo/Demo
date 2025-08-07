import streamlit as st
import numpy as np

# Improved prediction function
def predict_diabetes(bmi, age, gen_hlth, high_bp):
    """Realistic mock prediction with proper scaling"""
    # Normalized coefficients (sum < 1)
    bmi_coef = 0.3
    age_coef = 0.2
    health_coef = 0.3
    bp_coef = 0.2
    
    # Normalize inputs
    scaled_bmi = (bmi - 12) / (50 - 12)  # 0-1 range
    scaled_age = (age - 1) / (13 - 1)     # 0-1 range
    scaled_health = (gen_hlth - 1) / 4    # 0-1 range
    
    # Calculate risk (0-1 range)
    risk = (
        scaled_bmi * bmi_coef +
        scaled_age * age_coef +
        scaled_health * health_coef +
        high_bp * bp_coef
    )
    
    # Apply sigmoid to get probability between 0-1
    probability = 1 / (1 + np.exp(-(risk - 0.5) * 10))
    return min(max(probability, 0.01), 0.99)  # Cap between 1%-99%

# Streamlit UI
st.title("Diabetes Risk Prediction Tool")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        bmi = st.slider("BMI", 12.0, 50.0, 25.0, step=0.1,
                       help="Normal range: 18.5-24.9")
        age = st.slider("Age Group", 1, 13, 7,
                       help="1: 18-24, 2: 25-29, ..., 13: 80+")
        
    with col2:
        gen_hlth = st.select_slider("General Health", 
                                   options=[1, 2, 3, 4, 5],
                                   value=3,
                                   help="1=Excellent, 5=Poor")
        high_bp = st.radio("High Blood Pressure", 
                          options=["No", "Yes"],
                          index=0)
    
    if st.form_submit_button("Calculate Risk"):
        high_bp_num = 1 if high_bp == "Yes" else 0
        risk = predict_diabetes(bmi, age, gen_hlth, high_bp_num)
        
        # Display results
        st.subheader("Results")
        st.metric("Diabetes Risk Probability", f"{risk*100:.1f}%")
        
        # Visual indicator
        st.progress(risk)
        
        # Interpretation
        if risk > 0.7:
            st.error("High risk - Please consult a healthcare provider")
        elif risk > 0.4:
            st.warning("Moderate risk - Consider lifestyle changes")
        else:
            st.success("Low risk - Maintain healthy habits")

st.caption("Note: This is a simplified screening tool, not a medical diagnosis")
