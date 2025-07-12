# upload_xynth.py

import streamlit as st
import os
import google.generativeai as genai
from openai import OpenAI

# 🔐 Authenticate Gemini (Gemini 2.5 Pro)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel(model_name="gemini-2.5-pro")

# 🔐 Authenticate OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def call_gpt(prompt: str) -> str:
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

def call_gemini(prompt: str) -> str:
    response = gemini.generate_content(prompt)
    return response.text.strip()

def run_tab():
    st.subheader("📄 Upload XYNTH Output for Final Analysis")

    uploaded_file = st.file_uploader("Upload XYNTH .txt or .md output", type=["txt", "md"])
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")

        gemini_summary = call_gemini(f"Summarize the following XYNTH output and convert to clear trades:\n{content}")
        gpt_summary = call_gpt(f"Summarize the following XYNTH output and convert to clear trades:\n{content}")

        st.success("✅ Analysis Complete")
        st.markdown("### 🧠 Gemini Summary")
        st.write(gemini_summary)
        st.markdown("### 🤖 GPT Summary")
        st.write(gpt_summary)
