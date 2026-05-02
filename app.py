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
# 🎬 ANC CINEMATIC CSS
# -------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f172a, #020617);
    color: white;
}
.title {
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    background: linear-gradient(90deg, #ff4b4b, #dc2626);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.subtitle {
    text-align: center;
    color: #9ca3af;
}
.card {
    background: rgba(255, 255, 255, 0.05);
    padding: 25px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0px 0px 30px rgba(255,0,0,0.2);
    margin-top: 20px;
}
.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #dc2626);
    color: white;
    border-radius: 12px;
    height: 55px;
    font-size: 18px;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0px 0px 20px red;
}
section[data-testid="stSidebar"] {
    background: #020617;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# HEADER
# -------------------------
st.markdown('<div class="title"> 🎬 Customer Churn Prediction</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">AI Powered Customer Risk Analysis</div>', unsafe_allow_html=True)

# -------------------------
# SIDEBAR INPUT
# -------------------------
st.sidebar.header("🎛️ Customer Controls")

tenure = st.sidebar.slider("Tenure", 0, 72, 12)
monthly = st.sidebar.number_input("Monthly Charges", 0.0, 200.0, 50.0)
total = st.sidebar.number_input("Total Charges", 0.0, 10000.0, 500.0)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
partner = st.sidebar.selectbox("Partner", ["Yes", "No"])
dependents = st.sidebar.selectbox("Dependents", ["Yes", "No"])

phone = st.sidebar.selectbox("Phone Service", ["Yes", "No"])
multi = st.sidebar.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
internet = st.sidebar.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

contract = st.sidebar.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
payment = st.sidebar.selectbox("Payment Method", [
    "Electronic check", "Mailed check",
    "Bank transfer (automatic)", "Credit card (automatic)"
])

# -------------------------
# DATA PREP
# -------------------------
input_data = {
    "tenure": tenure,
    "MonthlyCharges": monthly,
    "TotalCharges": total
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
set_dummy("PhoneService", phone)
set_dummy("MultipleLines", multi)
set_dummy("InternetService", internet)
set_dummy("Contract", contract)
set_dummy("PaymentMethod", payment)

input_df = input_df[columns]

# -------------------------
# MAIN DASHBOARD
# -------------------------
col1, col2 = st.columns([2,1])

# -------------------------
# LEFT PANEL
# -------------------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📊 Customer Overview")

    st.write(f"**Tenure:** {tenure} months")
    st.write(f"**Monthly Charges:** ₹{monthly}")
    st.write(f"**Total Charges:** ₹{total}")
    st.write(f"**Internet Service:** {internet}")
    st.write(f"**Contract Type:** {contract}")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# RIGHT PANEL (PREDICTION)
# -------------------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎯 Risk Prediction")

    if st.button("🚀 Analyze Customer"):

        prob = model.predict_proba(input_df)[0][1]

        # -------------------------
        # 🎯 Risk Levels
        # -------------------------
        if prob < 0.30:
            level = "🟢 LOW RISK"
            msg = "Customer is safe. Very low chance of churn."
            st.success(level)

        elif prob < 0.60:
            level = "🟡 MODERATE RISK"
            msg = "Customer may churn. Needs attention."
            st.warning(level)

        elif prob < 0.80:
            level = "🟠 HIGH RISK"
            msg = "Customer likely to churn. Take action soon."
            st.warning(level)

        else:
            level = "🔴 CRITICAL RISK"
            msg = "Customer is very likely to churn! Immediate action required."
            st.error(level)

        # -------------------------
        # 📊 Output
        # -------------------------
        st.write(f"**Insight:** {msg}")
        st.progress(int(prob * 100))
        st.metric("Churn Probability", f"{prob*100:.2f}%")

        # -------------------------
        # 💡 Business Suggestions
        # -------------------------
        st.markdown("### 💡 Recommended Actions")

        if prob < 0.30:
            st.write("✔ Maintain service quality")
            st.write("✔ Offer loyalty rewards")

        elif prob < 0.60:
            st.write("✔ Send promotional offers")
            st.write("✔ Improve engagement")

        elif prob < 0.80:
            st.write("✔ Provide discounts")
            st.write("✔ Customer support follow-up")

        else:
            st.write("✔ Immediate retention call 🚨")
            st.write("✔ Heavy discount offer")
            st.write("✔ Escalate to retention team")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------------
# FOOTER
# -------------------------
st.markdown("---")
st.caption("⚡ Built by Manish | AI Project | Streamlit UI")
