import streamlit as st
import pandas as pd
import joblib

# ===============================
# Load Model & Columns
# ===============================
model = joblib.load("random.pkl")
columns = joblib.load("columns.pkl")

# ===============================
# Page Config (AMC Style)
# ===============================
st.set_page_config(page_title="Customer Churn Predictor", layout="wide")

# Custom CSS (Modern UI)
st.markdown("""
    <style>
    .main {
        background-color: #0f172a;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        color: white;
        border-radius: 10px;
        height: 50px;
        width: 100%;
        font-size: 18px;
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# Title
# ===============================
st.title("📊 Customer Churn Prediction App")
st.write("Predict whether a customer will churn or not using ML model")

# ===============================
# Input Section
# ===============================
st.subheader("Enter Customer Details")

col1, col2, col3 = st.columns(3)

with col1:
    tenure = st.number_input("Tenure", 0, 100)
    MonthlyCharges = st.number_input("Monthly Charges", 0.0, 10000.0)

with col2:
    TotalCharges = st.number_input("Total Charges", 0.0, 100000.0)
    gender = st.selectbox("Gender", ["Male", "Female"])

with col3:
    Partner = st.selectbox("Partner", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["Yes", "No"])

# ===============================
# Convert Input to DataFrame
# ===============================
input_dict = {
    "tenure": tenure,
    "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges
}

# Convert categorical to dummy manually
def encode_input(input_dict):
    df = pd.DataFrame(columns=columns)
    df.loc[0] = 0

    # Numerical
    for key in input_dict:
        if key in df.columns:
            df[key] = input_dict[key]

    # Example categorical encoding
    if f"gender_{gender}" in df.columns:
        df[f"gender_{gender}"] = 1

    if f"Partner_{Partner}" in df.columns:
        df[f"Partner_{Partner}"] = 1

    if f"Dependents_{Dependents}" in df.columns:
        df[f"Dependents_{Dependents}"] = 1

    return df

# ===============================
# Prediction
# ===============================
if st.button("🚀 Predict Churn"):

    input_df = encode_input(input_dict)

    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    st.subheader("Result")

    if prediction == 1:
        st.error(f"⚠️ Customer is likely to CHURN\n\nProbability: {prob:.2f}")
    else:
        st.success(f"✅ Customer will STAY\n\nProbability: {prob:.2f}")
