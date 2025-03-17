import streamlit as st
import logging
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from pymongo import MongoClient
logger=logging.getLogger(__name__)

def run_csv_clustering():
    st.title("CSV Clustering & Analysis")
    file_obj=st.file_uploader("Upload CSV",type=["csv"])
    if file_obj:
        df=pd.read_csv(file_obj)
        if df.empty:
            st.error("Uploaded CSV is empty.")
            return
        numeric=df.select_dtypes(include=[np.number]).columns
        if len(numeric)<2:
            st.error("Not enough numeric columns for clustering.")
            return
        x_col=st.selectbox("Select X-axis Feature",numeric)
        y_col=st.selectbox("Select Y-axis Feature",numeric)
        if x_col==y_col:
            st.error("Choose different columns.")
            return
        kmeans=KMeans(n_clusters=3,random_state=42,n_init=10)
        df["Cluster"]=kmeans.fit_predict(df[[x_col,y_col]])
        st.dataframe(df.head())
        import matplotlib.pyplot as plt
        import seaborn as sns
        fig,ax=plt.subplots(figsize=(8,5))
        sns.scatterplot(data=df,x=x_col,y=y_col,hue="Cluster",palette="viridis",s=100,ax=ax)
        ax.set_title("K-Means Clustering")
        st.pyplot(fig)

def run_login():
    st.title("Secure Login")
    username=st.text_input("Username")
    password=st.text_input("Password",type="password")
    if st.button("Login"):
        auth=authenticate_user(username,password)
        if auth:
            st.success("Login successful.")
        else:
            st.error("Invalid credentials.")

def authenticate_user(user,passwd):
    try:
        client=get_mongo_client_internal()
        db=client["mydatabase"]
        found=db.users.find_one({"username":user,"password":passwd})
        return found is not None
    except:
        return False

def get_mongo_client_internal():
    try:
        cl=MongoClient("mongodb://localhost:27017")
        return cl
    except:
        return None

def advanced_csv_analysis(df):
    desc=df.describe()
    corr=df.corr()
    return desc,corr

def run_advanced_csv_analysis():
    st.title("Advanced CSV Analysis")
    file_obj=st.file_uploader("Upload CSV",type=["csv"])
    if file_obj:
        df=pd.read_csv(file_obj)
        desc,corr=advanced_csv_analysis(df)
        st.subheader("Descriptive Statistics")
        st.dataframe(desc)
        st.subheader("Correlation Matrix")
        st.dataframe(corr)

def run_data_cleaning():
    st.title("Data Cleaning")
    file_obj=st.file_uploader("Upload CSV",type=["csv"])
    if file_obj:
        df=pd.read_csv(file_obj)
        st.write("Initial Shape:",df.shape)
        cleaned=drop_nulls_and_duplicates(df)
        st.write("Cleaned Shape:",cleaned.shape)
        st.dataframe(cleaned.head())

def drop_nulls_and_duplicates(df):
    df=df.dropna()
    df=df.drop_duplicates()
    return df

def run_data_enrichment():
    st.title("Data Enrichment")
    file_obj=st.file_uploader("Upload CSV",type=["csv"])
    if file_obj:
        df=pd.read_csv(file_obj)
        col=st.selectbox("Select Column to Enrich",df.columns)
        if st.button("Enrich"):
            df[col+"_Flag"]=df[col].apply(lambda x:1 if x else 0)
            st.dataframe(df.head())