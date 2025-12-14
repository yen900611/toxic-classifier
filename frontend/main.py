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
# Create Tabs
tab1, tab2 = st.tabs(["💬 Single Comment", "📂 Batch Analysis"])

# --- TAB 1: SINGLE MODE (Keep your old logic here) ---
with tab1:
    st.markdown("Enter a comment below to check if it's toxic.")
    user_input = st.text_area("Comment Text:", placeholder="Type something here...")

    if st.button("Analyze Single"):
        if user_input.strip():
            try:
                headers = {"X-API-Key": api_key}
                payload = {"text": user_input}
                response = requests.post(f"{API_URL}/predict", json=payload, headers=headers)

                # ... (Keep your existing single result display logic here) ...
                # Note: Ensure API_URL in requests.post doesn't double the /predict path if you changed config
                # Easier way: Just hardcode or adjust os.getenv to base url
                if response.status_code == 200:
                    data = response.json()
                    results = data["results"]
                    st.write("---")
                    for label, score in results.items():
                        col1, col2 = st.columns([1, 3])
                        with col1: st.markdown(f"**{label.title()}**")
                        with col2: st.progress(score); st.caption(f"{score:.2%}")
                else:
                    st.error(f"Error: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: BATCH MODE (New!) ---
with tab2:
    st.markdown("Upload a CSV file containing a column named `text`.")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        import pandas as pd

        df = pd.read_csv(uploaded_file)

        # Check if 'text' column exists
        if "comment_text" in df.columns:
            st.write(f"Loaded {len(df)} comments.")

            if st.button("Analyze Batch"):
                # Prepare the batch payload
                texts = df["comment_text"].tolist()
                # Limit to 50 for demo purposes (so we don't crash browser)
                if len(texts) > 50:
                    st.warning("Truncating to first 50 rows for demo performance.")
                    texts = texts[:50]

                headers = {"X-API-Key": api_key}
                payload = {"texts": texts}

                with st.spinner("Analyzing..."):
                    try:
                        # Change Endpoint to /predict-batch
                        # NOTE: Depending on your API_URL config, you might need to adjust the path string
                        # If API_URL is "http://.../predict", strip it to base or just hardcode for now
                        batch_url = API_URL.replace("/predict", "/predict-batch")

                        response = requests.post(batch_url, json=payload, headers=headers)

                        if response.status_code == 200:
                            results = response.json()["results"]

                            # Create a nice DataFrame for display
                            result_df = pd.DataFrame(results)
                            # Combine with original text
                            final_df = pd.concat([pd.Series(texts, name="Comment"), result_df], axis=1)

                            st.success("Analysis Complete!")
                            st.dataframe(final_df.style.background_gradient(cmap="Reds", subset=result_df.columns))

                        else:
                            st.error(f"Error: {response.status_code}")

                    except Exception as e:
                        st.error(f"Connection Error: {e}")
        else:
            st.error("CSV must have a column named 'text'")