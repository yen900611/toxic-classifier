import streamlit as st
import requests
import os

# 1. Configuration
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/predict")

st.set_page_config(page_title="Toxic Comment Classifier", page_icon="🤬")

# --- MISSING PART: SIDEBAR CONFIGURATION ---
st.sidebar.title("🔒 API Security")
# This creates the variable 'api_key' that was missing
api_key = st.sidebar.text_input("Enter API Key", type="password", value="frontend-dev-key")
st.sidebar.info("Default key: frontend-dev-key")

# 2. Main UI Layout
st.title("🤬 Toxic Comment Classifier")
st.markdown("Enter a comment below to check if it's toxic.")

# Input area
user_input = st.text_area("Comment Text:", placeholder="Type something here...")

if st.button("Analyze"):
    if user_input.strip():
        try:
            # 3. Call the API
            # Now 'api_key' exists because we defined it in the sidebar above
            headers = {"X-API-Key": api_key}
            payload = {"text": user_input}

            response = requests.post(API_URL, json=payload, headers=headers)

            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                results = data["results"]

                # 4. Display Results
                st.write("---")
                st.subheader("Analysis Results:")

                for label, score in results.items():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        st.markdown(f"**{label.title()}**")
                    with col2:
                        st.progress(score)
                        st.caption(f"{score:.2%}")

                with st.expander("See Raw API Response"):
                    st.json(results)

            # Handle specific security errors
            elif response.status_code == 403:
                st.error("⛔ **403 Forbidden**: Invalid API Key. Check the sidebar.")
            elif response.status_code == 429:
                st.error("⏳ **429 Too Many Requests**: Slow down!")
            else:
                st.error(f"Error: API returned status code {response.status_code}")

        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the backend. Is FastAPI running on port 8000?")
    else:
        st.warning("Please enter some text first.")