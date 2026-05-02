import streamlit as st
import pandas as pd
import joblib

# -------------------------
# PAGE CONFIG
# -------------------------
st.set_page_config(page_title="Churn AI", layout="wide")

# -------------------------
# LOAD MODEL
# -------------------------
model = joblib.load("random.pkl")
columns = joblib.load("columns.pkl")

# -------------------------
# AMC STYLE CSS 🎬
# -------------------------
st.markdown("""
<style>

body {
    background-color: #0e1117;
    color: white;
}

/* Title */
.title {
    font-size: 42px;
    font-weight: bold;
    color: #ff4b4b;
    text-align: center;
}

/* Subtitle */
.subtitle {
    text-align: center;
    color: #aaa;
}

/* Glass Card */
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow: 0px 0px 20px rgba(255, 75, 75, 0.2);
    margin-top: 20px;
}

/* Button */
.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff0000);
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="title">🎬 Churn Prediction AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Smart customer behavior analysis system</div>', unsafe_allow_html=True)

# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("🎛️ Controls")

tenure = st.sidebar.slider("Tenure", 0, 72, 12)
monthly_charges = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 50.0)
total_charges = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 500.0)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
partner = st.sidebar.selectbox("Partner", ["Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", ["Yes", "No"])

phone_service = st.sidebar.selectbox("Phone Service", ["Yes", "No"])
multiple_lines = st.sidebar.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])

internet_service = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment_method = st.sidebar.selectbox("Payment Method", [
    "Electronic check", "Mailed check", 
    "Bank transfer (automatic)", "Credit card (automatic)"
])

# -------------------------
# DATA PREP
# -------------------------
input_data = {
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges
}

input_df = pd.DataFrame([input_data])

for col in columns:
    if col not in input_df.columns:
        input_df[col] = 0

def set_dummy(col, val):
    name = f"{col}_{val}"
    if name in input_df.columns:
        input_df[name] = 1

set_dummy("gender", gender)
set_dummy("Partner", partner)
set_dummy("Dependents", dependents)
set_dummy("PhoneService", phone_service)
set_dummy("MultipleLines", multiple_lines)
set_dummy("InternetService", internet_service)
set_dummy("Contract", contract)
set_dummy("PaymentMethod", payment_method)

input_df = input_df[columns]

# -------------------------
# PREDICTION DISPLAY
# -------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)

st.subheader("🎯 Prediction Result")

if st.button("🚀 Run Prediction"):
    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error("⚠️ HIGH RISK: Customer will churn")
    else:
        st.success("✅ SAFE: Customer will stay")

    st.write("### 📊 Confidence Level")
    st.progress(int(prob * 100))

    st.metric("Churn Probability", f"{prob*100:.2f}%")

st.markdown('</div>', unsafe_allow_html=True)











# import streamlit as st
# import pandas as pd
# import joblib

# # ===============================
# # Load Model & Columns
# # ===============================
# model = joblib.load("random.pkl")
# columns = joblib.load("columns.pkl")

# # ===============================
# # Page Config (AMC Style)
# # ===============================
# st.set_page_config(page_title="Customer Churn Predictor", layout="wide")

# # Custom CSS (Modern UI)
# st.markdown("""
#     <style>
#     .main {
#         background-color: #0f172a;
#         color: white;
#     }
#     .stButton>button {
#         background: linear-gradient(90deg, #06b6d4, #3b82f6);
#         color: white;
#         border-radius: 10px;
#         height: 50px;
#         width: 100%;
#         font-size: 18px;
#     }
#     .stTextInput>div>div>input {
#         border-radius: 10px;
#     }
#     </style>
# """, unsafe_allow_html=True)

# # ===============================
# # Title
# # ===============================
# st.title("📊 Customer Churn Prediction App")
# st.write("Predict whether a customer will churn or not using ML model")

# # ===============================
# # Input Section
# # ===============================
# st.subheader("Enter Customer Details")

# col1, col2, col3 = st.columns(3)

# with col1:
#     tenure = st.number_input("Tenure", 0, 100)
#     MonthlyCharges = st.number_input("Monthly Charges", 0.0, 10000.0)

# with col2:
#     TotalCharges = st.number_input("Total Charges", 0.0, 100000.0)
#     gender = st.selectbox("Gender", ["Male", "Female"])

# with col3:
#     Partner = st.selectbox("Partner", ["Yes", "No"])
#     Dependents = st.selectbox("Dependents", ["Yes", "No"])

# # ===============================
# # Convert Input to DataFrame
# # ===============================
# input_dict = {
#     "tenure": tenure,
#     "MonthlyCharges": MonthlyCharges,
#     "TotalCharges": TotalCharges
# }

# # Convert categorical to dummy manually
# def encode_input(input_dict):
#     df = pd.DataFrame(columns=columns)
#     df.loc[0] = 0

#     # Numerical
#     for key in input_dict:
#         if key in df.columns:
#             df[key] = input_dict[key]

#     # Example categorical encoding
#     if f"gender_{gender}" in df.columns:
#         df[f"gender_{gender}"] = 1

#     if f"Partner_{Partner}" in df.columns:
#         df[f"Partner_{Partner}"] = 1

#     if f"Dependents_{Dependents}" in df.columns:
#         df[f"Dependents_{Dependents}"] = 1

#     return df

# # ===============================
# # Prediction
# # ===============================
# if st.button("🚀 Predict Churn"):

#     input_df = encode_input(input_dict)

#     prediction = model.predict(input_df)[0]
#     prob = model.predict_proba(input_df)[0][1]

#     st.subheader("Result")

#     if prediction == 1:
#         st.error(f"⚠️ Customer is likely to CHURN\n\nProbability: {prob:.2f}")
#     else:
#         st.success(f"✅ Customer will STAY\n\nProbability: {prob:.2f}")
