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
        bmi = st.slider("Body Mass Index (BMI)", 12.0, 50.0, 25.0, step=0.1,
                       help="BMI Categories:\n"
                            "• Underweight: <18.5\n"
                            "• Normal weight: 18.5-24.9\n"
                            "• Overweight: 25-29.9\n"
                            "• Obesity: 30+")
        
        # Age group with detailed mapping
        age = st.slider("Age Group", 1, 13, 7,
                       help="Age Group Mapping:\n"
                            "1: 18-24 years\n"
                            "2: 25-29 years\n"
                            "3: 30-34 years\n"
                            "4: 35-39 years\n"
                            "5: 40-44 years\n"
                            "6: 45-49 years\n"
                            "7: 50-54 years\n"
                            "8: 55-59 years\n"
                            "9: 60-64 years\n"
                            "10: 65-69 years\n"
                            "11: 70-74 years\n"
                            "12: 75-79 years\n"
                            "13: 80+ years")
    
    with col2:
        # General health with clear labels
        gen_hlth = st.select_slider("General Health", 
                                  options=[1, 2, 3, 4, 5],
                                  value=3,
                                  format_func=lambda x: {
                                      1: "1 - Excellent",
                                      2: "2 - Very Good",
                                      3: "3 - Good",
                                      4: "4 - Fair",
                                      5: "5 - Poor"
                                  }[x],
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
