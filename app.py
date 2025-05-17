import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("svm_model_final.pkl")
vectorizer = joblib.load("tfidf_vectorizer_5000.pkl")

# Streamlit App
st.set_page_config(page_title="Phishing Email Detector", page_icon="📧")
st.title("📧 Real-Time Phishing Email Detection")

st.markdown("Enter an email content below to check if it's **phishing** or **legitimate**:")

# Input text area
email = st.text_area("Email content:", height=200)

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
