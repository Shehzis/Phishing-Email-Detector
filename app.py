import streamlit as st
import joblib
import csv
from datetime import datetime


# Load model and vectorizer
model = joblib.load("svm_model_final.pkl")
vectorizer = joblib.load("tfidf_vectorizer_5000.pkl")

# Streamlit App
st.set_page_config(page_title="Phishing Email Detector", page_icon="📧")
st.title("📧 Real-Time Phishing Email Detection")

st.markdown("Enter an email content below to check if it's **phishing** or **legitimate**:")

# Input text area
email = st.text_area("Email content:", height=200)

prediction = None
label = None



if st.button("🔍 Detect"):
    if email.strip() == "":
        st.warning("Please enter some email content.")
    else:
        # Preprocess and predict
        X_input = vectorizer.transform([email])
        prediction = model.predict(X_input)[0]
        label = "Phishing" if prediction == 1 else "Legitimate"

        # Result display
        if label == "Phishing":
            st.error(f"⚠️ This email is **{label}**.")
        else:
            st.success(f"✅ This email is **{label}**.")
            

#  Feedback section
if 'label' in st.session_state:
    st.markdown("### ❓ Was this prediction correct?")
    feedback = st.radio("Your feedback:", ["Yes", "No"], key="feedback_radio")

    if feedback == "No":
        correct_label = st.selectbox("What should it be?", ["Phishing", "Legitimate"], key="label_correct")

        if st.button("Submit Feedback"):
            feedback_entry = {
                "timestamp": datetime.now().isoformat(),
                "email": st.session_state['email'],
                "model_prediction": "Phishing" if st.session_state['prediction'] == 1 else "Legitimate",
                "user_label": correct_label
            }

            # Append feedback to CSV
            with open("feedback_log.csv", mode="a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=feedback_entry.keys())
                if f.tell() == 0:
                    writer.writeheader()
                writer.writerow(feedback_entry)

            st.success("✅ Thank you! Your feedback has been recorded.")
