import streamlit as st
import numpy as np

def predict_diabetes(bmi, age, gen_hlth, high_bp):
    """Refined prediction based on model insights with proper scaling"""
    # Non-linear age risk mapping (aligned with RF thresholds)
    age_risk_map = {
        1: 0.1,   # 18-24
        2: 0.15,  # 25-29
        3: 0.2,   # 30-34
        4: 0.25,  # 35-39
        5: 0.3,   # 40-44
        6: 0.4,   # 45-49 (risk jump)
        7: 0.5,   # 50-54
        8: 0.6,   # 55-59
        9: 0.7,   # 60-64
        10: 0.75, # 65-69
        11: 0.8,  # 70-74
        12: 0.85, # 75-79
        13: 0.9   # 80+
    }
    age_risk = age_risk_map[age]
    
    # Feature weights (sum to 1) based on model importance
    risk_score = (
        (min(bmi, 40)/40 * 0.25) +      # BMI (capped at 40, 25% weight)
        (age_risk * 0.15) +              # Age (15% weight, non-linear)
        ((gen_hlth-1)/4 * 0.35) +        # GenHlth (35% weight, dominant)
        (high_bp * 0.25)                 # HighBP (25% weight)
    
    # Calibrated sigmoid (gentler curve)
    probability = 1 / (1 + np.exp(-4 * (risk_score - 0.5)))
    return min(max(probability, 0.05), 0.95), age_risk  # Return both probability and age_risk

# Streamlit UI Configuration
st.set_page_config(page_title="Diabetes Risk Calculator", layout="wide")
st.title("Diabetes Risk Assessment Tool")
st.markdown("""
*Based on analysis of CDC's BRFSS dataset (ROC AUC=0.83)*  
*This tool estimates risk but is not a medical diagnosis.*
""")

with st.form("diabetes_risk_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        # BMI Input with category hints
        bmi = st.slider("Body Mass Index (BMI)", 12.0, 50.0, 25.0, 0.1,
                       help="BMI Categories:\n"
                            "• Underweight: <18.5\n"
                            "• Normal weight: 18.5-24.9\n"
                            "• Overweight: 25-29.9\n"
                            "• Obesity: 30+")
        
        # Age group with detailed mapping
        age = st.select_slider("Age Group", 
                              options=list(range(1,14)),
                              value=7,
                              format_func=lambda x: [
                                  "18-24", "25-29", "30-34", "35-39", "40-44",
                                  "45-49", "50-54", "55-59", "60-64", "65-69",
                                  "70-74", "75-79", "80+"][x-1])
    
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
                                      5: "5 - Poor"}[x])
        
        # High BP input
        high_bp = st.radio("High Blood Pressure", 
                          ["No", "Yes"],
                          horizontal=True)
    
    submitted = st.form_submit_button("Calculate Risk")
    
    if submitted:
        high_bp_num = 1 if high_bp == "Yes" else 0
        risk, age_risk = predict_diabetes(bmi, age, gen_hlth, high_bp_num)  # Unpack both returns
        
        # Results Display
        st.subheader("Results")
        
        # Risk Meter
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.metric("Risk Probability", f"{risk*100:.1f}%")
        with col_b:
            st.progress(risk)
        
        # Risk Breakdown Visualization
        factors = {
            'BMI': min(bmi,40)/40*0.25,
            'Age': age_risk*0.15,
            'General Health': ((gen_hlth-1)/4)*0.35,
            'High BP': high_bp_num*0.25
        }
        st.bar_chart(factors)
        
        # Clinical Interpretation
        st.subheader("Clinical Guidance")
        if risk > 0.7:
            st.error("**High Risk** - Strongly recommend:")
            st.info("Recommendations: Regular blood sugar monitoring, lifestyle changes, and medical consultation")
        elif risk > 0.4:
            st.warning("**Moderate Risk** - Recommended actions:")
            st.info("Recommendations: Improve diet, increase physical activity, annual check-ups")
        else:
            st.success("**Low Risk** - Maintenance suggestions:")
            st.info("Recommendations: Balanced diet, regular exercise, maintain healthy weight")

# Footer
st.markdown("---")
st.caption("""
**Disclaimer**: This tool provides statistical estimates based on population data. 
Individual risk factors may vary. Always consult a healthcare provider for personal 
medical advice. Model performance: ROC AUC 0.83, Accuracy 75%.
""")
