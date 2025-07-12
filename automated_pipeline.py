# automated_pipeline.py

import os
from datetime import datetime
import pandas as pd
from openai import OpenAI
from google.generativeai import GenerativeModel

# ⬇️ Import your finalized prompts
from prompts import (
    GEMINI_SENTIMENT,
    GEMINI_TRADES,
    GPT_TRADES,
    COMBINE_PROMPT,
    VALIDATE_GEMINI,
    VALIDATE_GPT
)

# ⬇️ Set up API clients
openai.api_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")
openai_client = OpenAI()
gemini = GenerativeModel("gemini-pro")

# ⬇️ Prompt call helpers
def call_gemini(prompt: str) -> str:
    return gemini.generate_content(prompt).text.strip()

def call_gpt(prompt: str) -> str:
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

# ⬇️ Run the full pipeline
def run_daily_pipeline():
    print("🚀 Running automated pipeline...")

    # 1. Gemini sentiment
    sentiment_output = call_gemini(GEMINI_SENTIMENT)

    # 2. Gemini + GPT trade suggestions (based on sentiment)
    gemini_trades = call_gemini(GEMINI_TRADES.format(sentiment=sentiment_output))
    gpt_trades = call_gpt(GPT_TRADES.format(sentiment=sentiment_output))

    # 3. Combine
    combined_output = call_gpt(COMBINE_PROMPT.format(gemini=gemini_trades, gpt=gpt_trades))

    # 4. Validate output with both models
    gemini_validated = call_gemini(VALIDATE_GEMINI.format(combined=combined_output))
    gpt_validated = call_gpt(VALIDATE_GPT.format(combined=combined_output))

    # 5. Output to CSV
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

# Entry point
if __name__ == "__main__":
    run_daily_pipeline()
