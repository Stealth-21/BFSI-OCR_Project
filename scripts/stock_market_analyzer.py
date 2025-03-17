import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
logger = logging.getLogger(__name__)

def run_stock_analysis():
    st.title("Advanced Stock Market Analysis")
    stock1 = st.text_input("First Stock Symbol", "AAPL").upper()
    stock2 = st.text_input("Second Stock Symbol", "TSLA").upper()
    period_options = {
        "1 Week": "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "Max": "max"
    }
    chosen_period = st.selectbox("Select Period", list(period_options.keys()))
    if st.button("Compare Stocks"):
        p = period_options[chosen_period]
        data1 = fetch_stock_data(stock1, p)
        data2 = fetch_stock_data(stock2, p)
        if data1 is None or data2 is None:
            st.error("Unable to fetch data. Check symbols or period.")
            return
        plot_stock_comparison(data1, data2, stock1, stock2, chosen_period)
        advanced_insights(data1, data2, stock1, stock2)

def fetch_stock_data(symbol, period):
    try:
        df = yf.download(symbol, period=period, interval="1d")["Close"]
        if df.empty:
            return None
        return df
    except:
        return None

def plot_stock_comparison(series1, series2, s1, s2, period_name):
    df = pd.DataFrame({s1: series1, s2: series2}).dropna()
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df.index, df[s1], label=s1, linewidth=2)
    ax.plot(df.index, df[s2], label=s2, linewidth=2)
    ax.set_title(f"{s1} vs {s2} - {period_name}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend()
    st.pyplot(fig)

def advanced_insights(data1, data2, s1, s2):
    diff = data2.iloc[-1] - data1.iloc[-1]
    st.write(f"Price difference on last day: {diff}")
    returns1 = (data1.iloc[-1] - data1.iloc[0]) / data1.iloc[0] * 100
    returns2 = (data2.iloc[-1] - data2.iloc[0]) / data2.iloc[0] * 100
    st.write(f"{s1} returns: {returns1:.2f}%")
    st.write(f"{s2} returns: {returns2:.2f}%")
    fig, ax = plt.subplots(figsize=(5,4))
    ax.bar([s1, s2], [returns1, returns2], color=["blue","green"])
    ax.set_title("Percentage Returns")
    st.pyplot(fig)

def advanced_volatility_analysis(symbol, period="1y"):
    data = yf.download(symbol, period=period, interval="1d")["Close"]
    daily_returns = data.pct_change().dropna()
    vol = daily_returns.std() * (252 ** 0.5)
    return vol

def run_stock_volatility():
    st.title("Stock Volatility Analysis")
    sym = st.text_input("Stock Symbol", "AAPL").upper()
    if st.button("Analyze Volatility"):
        vol = advanced_volatility_analysis(sym)
        st.write(f"Annualized Volatility for {sym}: {vol:.2f}")

def correlation_analysis(symbols, period="1y"):
    frames = {}
    for s in symbols:
        d = yf.download(s, period=period, interval="1d")["Close"]
        frames[s] = d
    df = pd.DataFrame(frames).dropna()
    corr = df.corr()
    return corr

def run_correlation():
    st.title("Stock Correlation Analysis")
    user_syms = st.text_input("Enter Stock Symbols (comma-separated)", "AAPL,TSLA,MSFT")
    if st.button("Compute Correlation"):
        syms = [x.strip().upper() for x in user_syms.split(",") if x.strip()]
        c = correlation_analysis(syms)
        st.dataframe(c)
        fig, ax = plt.subplots(figsize=(5,4))
        sns.heatmap(c, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

def advanced_moving_averages(symbol, period="1y"):
    data = yf.download(symbol, period=period, interval="1d")["Close"]
    df = pd.DataFrame(data)
    df["MA_20"] = df["Close"].rolling(window=20).mean()
    df["MA_50"] = df["Close"].rolling(window=50).mean()
    return df

def run_moving_average_analysis():
    st.title("Moving Average Analysis")
    sym = st.text_input("Symbol", "AAPL").upper()
    if st.button("Compute MAs"):
        df = advanced_moving_averages(sym)
        fig, ax = plt.subplots(figsize=(10,5))
        ax.plot(df.index, df["Close"], label="Close", linewidth=1)
        ax.plot(df.index, df["MA_20"], label="MA 20", linewidth=2)
        ax.plot(df.index, df["MA_50"], label="MA 50", linewidth=2)
        ax.legend()
        ax.set_title(f"{sym} Moving Averages")
        st.pyplot(fig)