# Daily Options Trade Filter – Mid/Short-Term Execution Scanner

This tool scans for high-probability call options with contract cost <$1.50 using real-time market data and sentiment feeds.

## Features:
- Filters options based on price, POP, sentiment, and expiry.
- Validates data from Reddit, Google Trends, UOA feeds, and Xynth.
- Streamlit dashboard for live review and manual validation uploads.
- Output: Ranked trade list by POP and expiry.

## Setup
1. Add your API keys to `.env`.
2. Install requirements: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`