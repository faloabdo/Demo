import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

# Load and prepare the model (this would normally be trained separately)
@st.cache_resource
def load_model():
    # This is a simplified version - in practice you would train and save your model
    # Here we'll create a mock model based on typical coefficients
    model = LogisticRegression()
    
    # Mock coefficients based on typical importance
    # (In a real app, you would load your trained model)
    model.coef_ = np.array([[0.8, 0.5, 0.7, 0.6]])  # BMI, Age, GenHlth, HighBP
    model.intercept_ = np.array([-5.0])  # Intercept
    model.classes_ = np.array([0, 1])
    
    return model

# Create scaler (in practice, fit this on your training data)
@st.cache_resource
def load_scaler():
    scaler = StandardScaler()
    # Mock scaler parameters (in practice, use your training data stats)
    scaler.mean_ = np.array([29.0, 8.0, 2.8, 0.5])  # BMI, Age, GenHlth, HighBP means
    scaler.scale_ = np.array([7.0, 2.8, 1.1, 0.5])  # Standard deviations
    return scaler

def main():
    st.title("Diabetes Risk Prediction Tool")
    st.write("""
    This app predicts the likelihood of having diabetes based on key health indicators.
    """)
    
    # Load model and scaler
    model = load_model()
    scaler = load_scaler()
    
    # User input
    st.sidebar.header('User Input Parameters')
    
    def user_input_features():
        bmi = st.sidebar.slider('BMI', 12.0, 50.0, 25.0)
        age = st.sidebar.slider('Age Group', 1, 13, 7,
                               help="1: 18-24, 2: 25-29, ..., 13: 80+")
        gen_hlth = st.sidebar.slider('General Health (1-5)', 1, 5, 3,
                                    help="1: Excellent, 2: Very good, 3: Good, 4: Fair, 5: Poor")
        high_bp = st.sidebar.radio('High Blood Pressure', ['No', 'Yes'])
        
        high_bp = 1 if high_bp == 'Yes' else 0
        
        data = {
            'BMI': bmi,
            'Age': age,
            'GenHlth': gen_hlth,
            'HighBP': high_bp
        }
        
        features = pd.DataFrame(data, index=[0])
        return features
    
    input_df = user_input_features()
    
    # Display user input
    st.subheader('User Input Parameters')
    st.write(input_df)
    
    # Preprocess input
    input_scaled = scaler.transform(input_df)
    
    # Make prediction
    prediction = model.predict_proba(input_scaled)
    
    # Display results
    st.subheader('Prediction')
    st.write(f"Probability of having diabetes: {prediction[0][1]*100:.1f}%")
    
    # Interpretation
    st.subheader('Risk Interpretation')
    if prediction[0][1] < 0.3:
        st.success('Low risk of diabetes')
    elif prediction[0][1] < 0.7:
        st.warning('Moderate risk of diabetes')
    else:
        st.error('High risk of diabetes')
    
    # Feature importance visualization
    st.subheader('How Each Factor Affects Your Risk')
    feature_importance = pd.DataFrame({
        'Feature': input_df.columns,
        'Coefficient': model.coef_[0],
        'Impact': np.abs(model.coef_[0])
    }).sort_values('Impact', ascending=False)
    
    st.bar_chart(feature_importance.set_index('Feature')['Impact'])
    
    # Health recommendations
    st.subheader('Health Recommendations')
    if input_df['BMI'].values[0] > 30:
        st.write("- Your BMI indicates obesity. Losing 5-10% of your body weight can significantly reduce diabetes risk.")
    if input_df['GenHlth'].values[0] >= 4:
        st.write("- Your self-reported health is fair/poor. Consider consulting a healthcare provider.")
    if input_df['HighBP'].values[0] == 1:
        st.write("- You have high blood pressure, which is associated with higher diabetes risk.")
    if input_df['Age'].values[0] >= 7:  # About 45+ years
        st.write("- As you're over 45, regular diabetes screening is recommended.")

if __name__ == '__main__':
    main()