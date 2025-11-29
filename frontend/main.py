import streamlit as st
import requests
import os

# 1. Configuration
# If we are in Docker, use the environment variable. If not, default to localhost.
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

st.set_page_config(page_title="Toxic Comment Classifier", page_icon="🤬")

# 2. UI Layout
st.title("🤬 Toxic Comment Classifier")
st.markdown("Enter a comment below to check if it's toxic.")

# Input area
user_input = st.text_area("Comment Text:", placeholder="Type something here...")

if st.button("Analyze"):
    if user_input.strip():
        try:
            # 3. Call the API
            payload = {"text": user_input}
            response = requests.post(API_URL, json=payload)

            # Check if request was successful
            if response.status_code == 200:
                result = response.json()
                is_toxic = result["is_toxic"]
                confidence = result["confidence"]

                # 4. Display Results
                st.write("---")
                if is_toxic:
                    st.error(f"🚨 **Toxic!** (Confidence: {confidence:.2%})")
                else:
                    st.success(f"✅ **Safe** (Confidence: {1 - confidence:.2%})")

                # Show raw JSON for debugging/demo purposes
                with st.expander("See Raw API Response"):
                    st.json(result)
            else:
                st.error(f"Error: API returned status code {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the backend. Is FastAPI running on port 8000?")
    else:
        st.warning("Please enter some text first.")