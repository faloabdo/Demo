import streamlit as st
import numpy as np

def predict_diabetes(bmi, age, gen_hlth, high_bp):
    """Realistic prediction with proper scaling"""
    # Normalize inputs (0-1 range)
    scaled_bmi = min(bmi, 40) / 40  # Cap BMI at 40 for calculation
    scaled_age = (age - 1) / 12      # Age groups 1-13 → 0-1
    scaled_health = (gen_hlth - 1) / 4  # General health from 1 to 5 → 0 to 1
    
    # Weighted factors with balanced coefficients
    risk_score = (
        (scaled_bmi * 0.3) + 
        (scaled_age * 0.25) + 
        (scaled_health * 0.25) + 
        (high_bp * 0.2)
    )
    
    # Adjusted sigmoid with gentler curve
    probability = 1 / (1 + np.exp(-6 * (risk_score - 0.6)))
    
    # Ensure reasonable bounds (5%-95%)
    return min(max(probability, 0.05), 0.95)

# Streamlit UI
st.title("Diabetes Risk Assessment Tool")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        bmi = st.slider("BMI", 12.0, 50.0, 25.0, step=0.1)
        age = st.slider("Age Group", 1, 13, 7,
                       help="1: 18-24, 2: 25-29, 3: 30-34, 4: 35-39, 5: 40-44, 6: 45-49, 7: 50-54, 8: 55-59, 9: 60-64, 10: 65-69, 11: 70-74, 12: 75-79, 13: 80+")
    
    with col2:
        gen_hlth = st.select_slider("General Health", 
                                  options=[1, 2, 3, 4, 5],
                                  value=3,
                                  help="1 = Excellent, 2 = Very Good, 3 = Good, 4 = Fair, 5 = Poor")
        high_bp = st.radio("High Blood Pressure", ["No", "Yes"])
    
    submitted = st.form_submit_button("Calculate Risk")
    
    if submitted:
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
            st.info("Recommendations: Regular blood sugar monitoring, lifestyle changes, and medical consultation")
        elif risk > 0.4:
            st.warning("Moderate risk - Monitor your health regularly")
            st.info("Recommendations: Improve diet, increase physical activity, annual check-ups")
        else:
            st.success("Low risk - Maintain healthy habits")
            st.info("Recommendations: Balanced diet, regular exercise, maintain healthy weight")

st.caption("Note: This is a screening tool, not a medical diagnosis. Always consult a healthcare professional for personalized advice.")
