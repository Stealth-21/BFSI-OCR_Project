import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pdfplumber
import os
import re
import logging
logger=logging.getLogger(__name__)
def run_bank_analysis():
    st.title("Bank Statement Analysis")
    uploaded=st.file_uploader("Upload CSV or PDF",type=["csv","pdf"])
    if uploaded:
        if uploaded.name.endswith(".pdf"):
            path=convert_pdf_to_csv_advanced(uploaded)
            if path:
                df=pd.read_csv(path)
                analyze_statement_advanced(df)
        else:
            df=pd.read_csv(uploaded)
            analyze_statement_advanced(df)
def convert_pdf_to_csv_advanced(pdf_file):
    out="processed_data/bank_statement_advanced.csv"
    os.makedirs("processed_data",exist_ok=True)
    transactions=[]
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                text=page.extract_text()
                if text:
                    lines=text.split("\n")
                    for line in lines:
                        match=re.search(r"(\d{2}-\d{2}-\d{4})\s+(.*?)\s+(\d{1,3}(?:,\d{3})*\.\d{2})\((Dr|Cr)\)",line)
                        if match:
                            date,narration,amount,txn=match.groups()
                            try:
                                val=float(amount.replace(",",""))
                                typ="Credit" if txn=="Cr" else "Debit"
                                transactions.append([date,narration.strip(),typ,val])
                            except:
                                pass
        if transactions:
            df=pd.DataFrame(transactions,columns=["Date","Narration","Transaction Type","Amount"])
            df.to_csv(out,index=False)
            return out
        else:
            st.error("No valid transactions found in PDF")
            return None
    except:
        st.error("Error converting PDF to CSV")
        return None
def analyze_statement_advanced(df):
    st.subheader("Advanced Bank Statement Analysis")
    total_dep=df[df["Transaction Type"]=="Credit"]["Amount"].sum()
    total_wdr=df[df["Transaction Type"]=="Debit"]["Amount"].sum()
    highest_dep=df[df["Transaction Type"]=="Credit"]["Amount"].max()
    highest_wdr=df[df["Transaction Type"]=="Debit"]["Amount"].max()
    summary={
        "Total Deposits":total_dep,
        "Total Withdrawals":total_wdr,
        "Highest Deposit":highest_dep,
        "Highest Withdrawal":highest_wdr
    }
    st.json(summary)
    visualize_statement_advanced(df)
def visualize_statement_advanced(df):
    st.subheader("Visualizations")
    fig,ax=plt.subplots(figsize=(5,4))
    dep=df[df["Transaction Type"]=="Credit"]["Amount"].sum()
    wdr=df[df["Transaction Type"]=="Debit"]["Amount"].sum()
    ax.bar(["Deposits","Withdrawals"],[dep,wdr],color=["green","red"])
    ax.set_title("Deposits vs Withdrawals")
    st.pyplot(fig)
    plt.figure(figsize=(6,4))
    count_types=df["Transaction Type"].value_counts()
    plt.pie(count_types,labels=count_types.index,autopct="%1.1f%%",startangle=90)
    plt.title("Transaction Distribution")
    st.pyplot(plt)
    df["Date"]=pd.to_datetime(df["Date"],errors="coerce")
    df.sort_values("Date",inplace=True)
    plt.figure(figsize=(8,4))
    for ttype in df["Transaction Type"].unique():
        subset=df[df["Transaction Type"]==ttype]
        plt.plot(subset["Date"],subset["Amount"],marker="o",label=ttype)
    plt.legend()
    plt.title("Transactions Over Time")
    st.pyplot(plt)
def advanced_spending_patterns(df):
    categories={}
    for i,row in df.iterrows():
        cat="Misc"
        narr=row["Narration"].lower()
        if "food" in narr or "restaurant" in narr:
            cat="Food"
        elif "fuel" in narr or "petrol" in narr:
            cat="Fuel"
        elif "bill" in narr or "recharge" in narr:
            cat="Utilities"
        elif "shopping" in narr:
            cat="Shopping"
        if cat not in categories:
            categories[cat]=0
        categories[cat]+=row["Amount"] if row["Transaction Type"]=="Debit" else 0
    return categories
def run_spending_pattern():
    st.title("Spending Pattern Analysis")
    uploaded=st.file_uploader("Upload CSV",type=["csv"])
    if uploaded:
        df=pd.read_csv(uploaded)
        cats=advanced_spending_patterns(df)
        st.json(cats)
        labels=list(cats.keys())
        values=list(cats.values())
        fig,ax=plt.subplots()
        ax.pie(values,labels=labels,autopct="%1.1f%%",startangle=90)
        ax.set_title("Spending Categories")
        st.pyplot(fig)