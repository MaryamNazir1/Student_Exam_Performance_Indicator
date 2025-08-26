import streamlit as st
import requests

st.set_page_config(page_title="Student Score Predictor", layout="centered")

st.title("📘 Student Performance Prediction")

# Form for user input
with st.form("prediction_form"):
    gender = st.selectbox("Gender", ["male", "female"])
    ethnicity = st.selectbox(
        "Race/Ethnicity", ["group A", "group B", "group C", "group D", "group E"]
    )
    parental_edu = st.selectbox(
        "Parental Education",
        [
            "some high school",
            "high school",
            "some college",
            "associate's degree",
            "bachelor's degree",
            "master's degree",
        ],
    )
    lunch = st.selectbox("Lunch", ["standard", "free/reduced"])
    prep_course = st.selectbox("Test Preparation Course", ["none", "completed"])
    reading_score = st.number_input(
        "Reading Score", min_value=0, max_value=100, value=50
    )
    writing_score = st.number_input(
        "Writing Score", min_value=0, max_value=100, value=50
    )

    submitted = st.form_submit_button("Predict")

if submitted:
    input_data = {
        "gender": gender,
        "race_ethnicity": ethnicity,
        "parental_level_of_education": parental_edu,
        "lunch": lunch,
        "test_preparation_course": prep_course,
        "reading_score": reading_score,
        "writing_score": writing_score,
    }

    response = requests.post("http://127.0.0.1:8000/predict", json=input_data)

    if response.status_code == 200:
        result = response.json()
        st.success(f"✅ Predicted Score: {result['prediction']:.2f}")
    else:
        st.error("❌ Something went wrong with prediction.")
