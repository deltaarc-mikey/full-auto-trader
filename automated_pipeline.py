# automated_pipeline.py

import os
import pandas as pd
from datetime import datetime
from openai import OpenAI
import google.generativeai as genai

# 🔐 Authenticate Gemini (Gemini 2.5 Pro)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
gemini = genai.GenerativeModel(model_name="gemini-2.5-pro")

# 🔐 Authenticate OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ⬇️ Import prompt templates
from prompts import (
    GEMINI_SENTIMENT,
    GEMINI_TRADES,
    GPT_TRADES,
    COMBINE_PROMPT,
    VALIDATE_GEMINI,
    VALIDATE_GPT
)

def call_gemini(prompt: str) -> str:
    response = gemini.generate_content(prompt)
    return response.text.strip()

def call_gpt(prompt: str) -> str:
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

def run_daily_pipeline():
    print("🚀 Running automated pipeline...")

    # 1. Sentiment analysis from Gemini
    sentiment_output = call_gemini(GEMINI_SENTIMENT)

    # 2. Trade recommendations
    gemini_trades = call_gemini(GEMINI_TRADES.format(sentiment=sentiment_output))
    gpt_trades = call_gpt(GPT_TRADES.format(sentiment=sentiment_output))

    # 3. Combine both outputs
    combined_output = call_gpt(COMBINE_PROMPT.format(gemini=gemini_trades, gpt=gpt_trades))

    # 4. Validate the trade list
    gemini_validated = call_gemini(VALIDATE_GEMINI.format(combined=combined_output))
    gpt_validated = call_gpt(VALIDATE_GPT.format(combined=combined_output))

    # 5. Save to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.DataFrame([{
        "Timestamp": timestamp,
        "Gemini Sentiment": sentiment_output,
        "Gemini Trades": gemini_trades,
        "GPT Trades": gpt_trades,
        "Combined Summary": combined_output,
        "Gemini Validation": gemini_validated,
        "GPT Validation": gpt_validated
    }])

    df.to_csv("pre_xynth_trades.csv", index=False)
    print("✅ pre_xynth_trades.csv saved.")

if __name__ == "__main__":
    run_daily_pipeline()
