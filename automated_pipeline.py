# automated_pipeline.py
import os
import json
from datetime import datetime
from openai import OpenAI
from google.generativeai import GenerativeModel
import pandas as pd

# Load keys
OpenAi.api_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

# Set up models
openai_client = OpenAI()
gemini = GenerativeModel("gemini-pro")

def call_gemini(prompt):
    return gemini.generate_content(prompt).text.strip()

def call_gpt(prompt):
    return openai_client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content.strip()

def run_daily_pipeline():
    # 1. Prompt Gemini for sentiment
    sentiment_prompt = "Analyze today's market sentiment and major trends..."
    sentiment_output = call_gemini(sentiment_prompt)

    # 2. Prompt Gemini and GPT for trade suggestions
    gemini_trade_prompt = f"Based on the following sentiment, suggest trades:\n\n{sentiment_output}"
    gpt_trade_prompt = gemini_trade_prompt

    gemini_trades = call_gemini(gemini_trade_prompt)
    gpt_trades = call_gpt(gpt_trade_prompt)

    # 3. Combine
    combined_prompt = f"""Compare and combine these trade suggestions:

    Gemini:
    {gemini_trades}

    GPT:
    {gpt_trades}

    Return a unified list with ticker, strategy, POP, and trade type."""
    combined_summary = call_gpt(combined_prompt)

    # 4. Validate again via Gemini and GPT
    gemini_validation = call_gemini(f"Validate these trades for POP and clarity:\n{combined_summary}")
    gpt_validation = call_gpt(f"Validate these trades for POP and clarity:\n{combined_summary}")

    # 5. Output CSV
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    df = pd.DataFrame([{
        "Run Timestamp": timestamp,
        "Gemini Trades": gemini_trades,
        "GPT Trades": gpt_trades,
        "Combined Summary": combined_summary,
        "Gemini Validation": gemini_validation,
        "GPT Validation": gpt_validation
    }])

    df.to_csv("pre_xynth_trades.csv", index=False)
    print("✅ pre_xynth_trades.csv saved.")

if __name__ == "__main__":
    run_daily_pipeline()
