
import joblib
import pandas as pd
import streamlit as st

# -------------------- PAGE SETUP --------------------

st.set_page_config(
    page_title="ChurnIQ | Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

model = joblib.load("churn_model.joblib")

# -------------------- CUSTOM STYLING --------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    [data-testid="stSidebar"] {
        background-color: #101A2C;
        border-right: 1px solid #243249;
    }

    .hero {
        background: linear-gradient(120deg, #15263E, #123A45);
        border: 1px solid #28505B;
        padding: 28px 30px;
        border-radius: 18px;
        margin-bottom: 24px;
    }

    .hero-tag {
        color: #5EEAD4;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    .hero h1 {
        color: #F8FAFC;
        font-size: 34px;
        margin: 10px 0 8px 0;
        line-height: 1.2;
    }

    .hero p {
        color: #C0CFDF;
        font-size: 15px;
        margin-bottom: 0;
    }

    .section-heading {
        font-size: 19px;
        font-weight: 700;
        color: #F1F5F9;
        margin: 8px 0 14px 0;
    }

    .info-card {
        background: #151F32;
        border: 1px solid #29374D;
        padding: 18px;
        border-radius: 14px;
        min-height: 110px;
    }

    .info-label {
        color: #9CAFC5;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .info-value {
        color: #F8FAFC;
        font-size: 25px;
        font-weight: 700;
        margin-top: 8px;
    }

    .result-card {
        background: linear-gradient(135deg, #142A3D, #15263A);
        border: 1px solid #31516A;
        border-radius: 18px;
        padding: 24px;
        margin: 10px 0 18px 0;
    }

    .result-label {
        color: #9CAFC5;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1.5px;
    }

    .result-value {
        color: #5EEAD4;
        font-size: 30px;
        font-weight: 750;
        margin: 8px 0;
    }

    .result-description {
        color: #C0CFDF;
        font-size: 14px;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #0D9488, #14B8A6);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        min-height: 48px;
        font-weight: 700;
        width: 100%;
        transition: 0.2s ease;
    }

    div.stButton > button:hover {
        background: linear-gradient(90deg, #0F766E, #0D9488);
        border: none;
        color: #FFFFFF;
    }

    div[data-testid="stMetric"] {
        background: #151F32;
        border: 1px solid #29374D;
        padding: 15px;
        border-radius: 12px;
    }

    hr {
        border-color: #29374D;
    }

    .footer {
        color: #8294AA;
        font-size: 12px;
        text-align: center;
        padding-top: 24px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div class="hero-tag">AI · CUSTOMER INTELLIGENCE</div>
    <h1>Customer Churn Analytics</h1>
    <p>
        Understand customer retention risk using a trained
        machine learning model. Enter customer details to
        generate an individual churn prediction.
    </p>
</div>
""", unsafe_allow_html=True)


# -------------------- SIDEBAR INPUTS --------------------

with st.sidebar:
    st.markdown("## ⚙️ Customer Profile")
    st.caption("Configure the customer's information below.")

    with st.expander("👤 Personal Details", expanded=True):
        gender = st.selectbox("Gender", ["Female", "Male"])
        senior_citizen = st.selectbox(
            "Senior citizen",
            [0, 1],
            format_func=lambda x: "Yes" if x == 1 else "No"
        )
        partner = st.selectbox("Has a partner?", ["Yes", "No"])
        dependents = st.selectbox("Has dependents?", ["Yes", "No"])

    with st.expander("📡 Services", expanded=True):
        phone_service = st.selectbox("Phone service", ["Yes", "No"])
        multiple_lines = st.selectbox(
            "Multiple lines",
            ["No phone service", "No", "Yes"]
        )
        internet_service = st.selectbox(
            "Internet service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online security",
            ["No internet service", "No", "Yes"]
        )
        online_backup = st.selectbox(
            "Online backup",
            ["No internet service", "No", "Yes"]
        )
        device_protection = st.selectbox(
            "Device protection",
            ["No internet service", "No", "Yes"]
        )
        tech_support = st.selectbox(
            "Tech support",
            ["No internet service", "No", "Yes"]
        )
        streaming_tv = st.selectbox(
            "Streaming TV",
            ["No internet service", "No", "Yes"]
        )
        streaming_movies = st.selectbox(
            "Streaming movies",
            ["No internet service", "No", "Yes"]
        )

    with st.expander("💳 Billing & Contract", expanded=True):
        contract = st.selectbox(
            "Contract type",
            ["Month-to-month", "One year", "Two year"]
        )
        paperless_billing = st.selectbox(
            "Paperless billing",
            ["Yes", "No"]
        )
        payment_method = st.selectbox(
            "Payment method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    with st.expander("💰 Charges & Tenure", expanded=True):
        tenure = st.number_input(
            "Tenure (months)", 0, 100, 12
        )
        monthly_charges = st.number_input(
            "Monthly charges ($)", 0.0, 200.0, 70.0, step=5.0
        )
        total_charges = st.number_input(
            "Total charges ($)", 0.0, 100000.0, 840.0, step=50.0
        )

    predict_clicked = st.button("✦ Analyze Customer", use_container_width=True)


# -------------------- TOP OVERVIEW --------------------

st.markdown('<div class="section-heading">Model Overview</div>',
            unsafe_allow_html=True)

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric("Test Accuracy", "80.55%")

with metric2:
    st.metric("Churn Recall", "55.9%")

with metric3:
    st.metric("Model", "Logistic Regression")

st.caption(
    "Evaluation results from the held-out test set. "
    "Churn recall measures the proportion of actual churners detected."
)

st.divider()


# -------------------- MAIN CONTENT --------------------

left_col, right_col = st.columns([1.15, 0.85], gap="large")

with left_col:
    st.markdown(
        '<div class="section-heading">Customer Snapshot</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="info-card">
            <div class="info-label">Customer tenure</div>
            <div class="info-value">{tenure} months</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    charge1, charge2 = st.columns(2)

    with charge1:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Monthly charges</div>
                <div class="info-value">${monthly_charges:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with charge2:
        st.markdown(
            f"""
            <div class="info-card">
                <div class="info-label">Total charges</div>
                <div class="info-value">${total_charges:,.2f}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")
    st.markdown("**Selected contract**")
    st.write(f"{contract}")

    st.markdown("**Internet service**")
    st.write(f"{internet_service}")

with right_col:
    st.markdown(
        '<div class="section-heading">Prediction Center</div>',
        unsafe_allow_html=True
    )

    if predict_clicked:
        customer = pd.DataFrame([{
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges
        }])

        prediction = model.predict(customer)[0]
        probabilities = model.predict_proba(customer)[0]
        churn_index = list(model.classes_).index("Yes")
        churn_probability = float(probabilities[churn_index])

        if prediction == "Yes":
            result_text = "Potential Churn"
            description = "The model predicts that this customer may leave."
        else:
            result_text = "Likely to Stay"
            description = "The model predicts that this customer may remain."

        st.markdown(
            f"""
            <div class="result-card">
                <div class="result-label">Model assessment</div>
                <div class="result-value">{result_text}</div>
                <div class="result-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("**Estimated churn probability**")
        st.progress(churn_probability)
        st.markdown(f"### {churn_probability:.1%}")

        if churn_probability >= 0.5:
            st.warning(
                "The estimated churn probability is at least 50%. "
                "Consider reviewing this customer's experience."
            )
        else:
            st.info(
                "The estimated churn probability is below 50%. "
                "This does not guarantee that the customer will stay."
            )

    else:
        st.markdown(
            """
            <div class="result-card">
                <div class="result-label">Ready for analysis</div>
                <div class="result-value">Awaiting input</div>
                <div class="result-description">
                    Configure the customer profile in the sidebar,
                    then select Analyze Customer to view the result.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "The model uses customer details, service selections, "
            "contract information and billing data."
        )

st.divider()

with st.expander("📘 How to interpret this dashboard"):
    st.write(
        "- **Test accuracy:** The proportion of all test records "
        "classified correctly.\n"
        "- **Churn recall:** The proportion of actual churners "
        "identified by the model.\n"
        "- **Churn probability:** The model's estimated probability, "
        "not a guarantee or proof of future behavior.\n"
        "- **Prediction threshold:** The classifier normally predicts "
        "'Yes' at a probability threshold of 50%, unless configured otherwise."
    )

st.markdown(
    '<div class="footer">'
    'CHURNIQ · MACHINE LEARNING PROJECT · FOR DEMONSTRATION PURPOSES'
    '</div>',
    unsafe_allow_html=True
)
