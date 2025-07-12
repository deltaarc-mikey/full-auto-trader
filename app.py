# app.py
import streamlit as st
import pandas as pd
from upload_xynth import run_tab as run_upload_xynth

st.set_page_config(page_title="AI Trading Hub", layout="wide")
st.title("📊 Delta Ghost AI Trading Dashboard")

tabs = ["📅 Daily Market Report", "📤 Upload XYNTH Result"]
selected_tab = st.sidebar.radio("Select Section", tabs)

if selected_tab == tabs[0]:
    st.subheader("Automated Daily Market Summary")

    try:
        df = pd.read_csv("pre_xynth_trades.csv")
        st.write(df.iloc[-1])  # Show most recent row
    except Exception:
        st.warning("No market data available yet.")

elif selected_tab == tabs[1]:
    run_upload_xynth()