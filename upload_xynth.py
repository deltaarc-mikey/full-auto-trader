# upload_xynth.py
import streamlit as st
import os
from openai import OpenAI
from google.generativeai import GenerativeModel

openai.api_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

openai_client = OpenAI()
gemini = GenerativeModel("gemini-pro")

def call_gpt(prompt):
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

def call_gemini(prompt):
    return gemini.generate_content(prompt).text.strip()

def run_tab():
    st.subheader("📄 Upload XYNTH Output for Final Analysis")

    uploaded_file = st.file_uploader("Upload XYNTH .txt or .md output", type=["txt", "md"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")

        gemini_response = call_gemini(f"Summarize the following trade data and provide execution-ready instructions:\n{content}")
        gpt_response = call_gpt(f"Summarize the following trade data and provide execution-ready instructions:\n{content}")

        st.success("✅ Summarization complete.")
        st.markdown("### 🧠 Gemini Summary")
        st.write(gemini_response)
        st.markdown("### 🤖 GPT Summary")
        st.write(gpt_response)