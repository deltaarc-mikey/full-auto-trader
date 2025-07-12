# scanner_task.py
import pandas as pd
import yfinance as yf
from utils import fetch_sentiment_data
from filters import option_filter
import scanners
import configparser
import datetime

def run_scanner_task():
    """
    This is the main backend task. It runs scanners to find tickers,
    analyzes them, scores them, filters for opportunities, and saves the results.
    """
    print(f"[{datetime.datetime.now()}] Running scanner task...")
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    
    uw_api_key = config['API_KEYS']['UNUSUAL_WHALES_API_KEY']
    barchart_api_key = config['API_KEYS']['BARCHART_API_KEY']
    finviz_url = config['API_KEYS']['FINVIZ_SCREENER_URL']

    print("Gathering candidate tickers from data sources...")
    uoa_tickers = scanners.get_unusual_whales_flow(uw_api_key)
    finviz_tickers = scanners.run_finviz_screener(finviz_url)
    
    candidate_tickers = list(set(uoa_tickers) | set(finviz_tickers))
    
    if not candidate_tickers:
        print("No candidate tickers found from initial scans.")
        return

    print(f"Found {len(candidate_tickers)} candidates: {candidate_tickers}")
    all_valid_options = []

    for ticker_symbol in candidate_tickers:
        try:
            # --- UPDATED: Weighted Scoring Logic ---
            catalyst_score = 0
            if ticker_symbol in uoa_tickers:
                catalyst_score += 4  # High score for important UOA signal
            if ticker_symbol in finviz_tickers:
                catalyst_score += 2  # Moderate score for technical setup
            if scanners.get_barchart_data(ticker_symbol, barchart_api_key):
                catalyst_score += 2  # Moderate score for analyst rating

            # Only proceed with tickers that have a meaningful score
            if catalyst_score < 4:
                continue

            ticker = yf.Ticker(ticker_symbol)
            next_expiry = ticker.options[0]
            opt = ticker.option_chain(next_expiry)
            calls = opt.calls

            calls['ticker'] = ticker_symbol
            calls['expiry'] = next_expiry
            calls['pop_score'] = catalyst_score
            calls['type'] = 'call'
            calls['price'] = calls['lastPrice']

            for _, row in calls.iterrows():
                option_data = row.to_dict()
                if option_filter(option_data):
                    sentiment = fetch_sentiment_data(ticker_symbol)
                    option_data['summary'] = (
                        f"Strike: {option_data['strike']} | Price: ${option_data['price']:.2f} | "
                        f"Catalyst Score: {option_data['pop_score']}/10 | News: {sentiment['news_catalyst']}"
                    )
                    all_valid_options.append(option_data)

        except Exception as e:
            print(f"Could not process ticker {ticker_symbol}: {e}")

    if all_valid_options:
        results_df = pd.DataFrame(all_valid_options)
        results_df = results_df.sort_values(by='pop_score', ascending=False)
        results_df.to_csv("results.csv", index=False)
        print(f"Scan complete. Found {len(results_df)} valid trades. Results saved to results.csv.")
    else:
        pd.DataFrame([]).to_csv("results.csv", index=False)
        print("Scan complete. No options met the filter criteria.")

if __name__ == '__main__':
    run_scanner_task()
