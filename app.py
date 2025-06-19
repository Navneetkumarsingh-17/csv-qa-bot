import streamlit as st
import pandas as pd
import openai
import os

# Set API Key securely from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="CSV-QA Bot", layout="wide")
st.title("📊 Ask Your CSV - AI Bot")

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    user_query = st.text_input("Ask a question about your data:")

    if user_query:
        sample_data = df.head(20).to_string(index=False)
        prompt = (
            "You are a data analyst. The user will ask questions about the following data.\\n\\n"
            + sample_data +
            "\\n\\nQuestion: " + user_query +
            "\\nAnswer in detail using the data only."
        )

        with st.spinner("Thinking..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=500
                )
                st.success(response['choices'][0]['message']['content'])
            except Exception as e:
                st.error(f"Error: {str(e)}")
else:
    st.info("Upload a CSV file to get started.")
