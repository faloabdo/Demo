import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load model (simplified version - in production, use a trained model)
@st.cache_resource
def load_model():
    model = LogisticRegression()
    # Mock coefficients based on your analysis (BMI, Age, GenHlth, HighBP)
    model.coef_ = np.array([[0.8, 0.5, 0.7, 0.6]])
    model.intercept_ = np.array([-5.0])
    return model

# Load scaler (in production, use your actual scaler)
@st.cache_resource
def load_scaler():
    scaler = StandardScaler()
    # Mock parameters (mean and scale for BMI, Age, GenHlth, HighBP)
    scaler.mean_ = np.array([29.0, 8.0, 2.8, 0.5])
    scaler.scale_ = np.array([7.0, 2.8, 1.1, 0.5])
    return scaler

def main():
    st.title("Diabetes Risk Prediction Tool")
    st.markdown("""
    This app predicts your likelihood of having diabetes based on key health indicators.
    """)
    
    # Load model and scaler
    model = load_model()
    scaler = load_scaler()
    
    # Input section
    st.sidebar.header("User Input Parameters")
    
    def user_input_features():
        bmi = st.sidebar.slider("BMI", 12.0, 50.0, 25.0)
        age = st.sidebar.slider("Age Group", 1, 13, 7,
                              help="1: 18-24, 2: 25-29, ..., 13: 80+")
        gen_hlth = st.sidebar.slider("General Health (1-5 scale)", 1, 5, 3,
                                    help="1: Excellent, 5: Poor")
        high_bp = st.sidebar.radio("High Blood Pressure", ["No", "Yes"])
        
        return {
            'BMI': bmi,
            'Age': age,
            'GenHlth': gen_hlth,
            'HighBP': 1 if high_bp == "Yes" else 0
        }
    
    input_data = user_input_features()
    input_df = pd.DataFrame(input_data, index=[0])
    
    # Display user input
    st.subheader("Your Input Values")
    st.write(input_df)
    
    # Preprocess and predict
    input_scaled = scaler.transform(input_df)
    prediction_proba = model.predict_proba(input_scaled)
    risk_percentage = prediction_proba[0][1] * 100
    
    # Show results
    st.subheader("Prediction Result")
    st.metric(label="Diabetes Risk Probability", value=f"{risk_percentage:.1f}%")
    
    # Risk interpretation
    st.subheader("Risk Interpretation")
    if risk_percentage < 30:
        st.success("Low risk of diabetes")
    elif risk_percentage < 70:
        st.warning("Moderate risk of diabetes")
    else:
        st.error("High risk of diabetes")
    
    # Feature importance
    st.subheader("How Each Factor Affects Your Risk")
    features = ['BMI', 'Age', 'General Health', 'High BP']
    importance = pd.DataFrame({
        'Feature': features,
        'Impact': np.abs(model.coef_[0])
    }).sort_values('Impact', ascending=False)
    
    st.bar_chart(importance.set_index('Feature'))
    
    # Recommendations
    st.subheader("Health Recommendations")
    if input_data['BMI'] > 30:
        st.write("- 🏋️ Consider weight management (your BMI indicates obesity)")
    if input_data['GenHlth'] >= 4:
        st.write("- 🩺 Schedule a health check-up (your self-reported health is fair/poor)")
    if input_data['HighBP'] == 1:
        st.write("- ❤️ Monitor your blood pressure regularly")
    if input_data['Age'] >= 7:  # About 45+ years
        st.write("- 🩺 Regular diabetes screening recommended for your age group")
    
    st.info("Note: This is a simplified prediction tool. Consult a healthcare professional for accurate diagnosis.")

if __name__ == "__main__":
    main()
