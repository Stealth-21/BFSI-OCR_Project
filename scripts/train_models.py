import streamlit as st
import pandas as pd
import numpy as np
import logging
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
logger = logging.getLogger(__name__)

def run_train_models():
    st.title("Train Models")
    st.write("Train or retrain BFSI models here")
    data_file = st.file_uploader("Upload CSV data for training", type=["csv"])
    if data_file:
        df = pd.read_csv(data_file)
        if st.button("Train Loan Model"):
            result = train_loan_model(df)
            st.write("Training completed:", result)

def train_loan_model(df):
    selected_features = [
        "Marks_10th",
        "Marks_12th",
        "CGPA",
        "Parents_Credit_Score",
        "Student_Credit_Score",
        "Total_Assets",
        "Fixed_Deposit",
        "Selected_Exam_Rank"
    ]
    df["Selected_Exam_Rank"] = df[["JEE_Rank", "SAT_Score", "CAT_Rank", "NEET_Rank"]].max(axis=1)
    X = df[selected_features]
    y = df["Loan_Approved"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    param_grid = {
        "n_estimators": [100, 200],
        "max_depth": [None, 10, 20]
    }
    rf = RandomForestClassifier(random_state=42)
    gs = GridSearchCV(rf, param_grid, cv=3, n_jobs=-1, scoring="accuracy")
    gs.fit(X_train, y_train)
    best = gs.best_estimator_
    acc = best.score(X_test, y_test)
    with open("models/loan_approval_model.pkl","wb") as f:
        pickle.dump(best,f)
    return {"best_params":gs.best_params_,"accuracy":acc}

def advanced_model_training(df):
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC
    data = df.dropna()
    X = data.drop("Loan_Approved", axis=1)
    y = data["Loan_Approved"]
    sc = StandardScaler()
    X_scaled = sc.fit_transform(X)
    model = SVC(probability=True)
    model.fit(X_scaled, y)
    return model

def run_svc_training():
    st.title("SVC Loan Model Training")
    uploaded = st.file_uploader("Upload training data", type=["csv"])
    if uploaded:
        data = pd.read_csv(uploaded)
        if st.button("Train SVC Model"):
            mdl = advanced_model_training(data)
            with open("models/svc_loan.pkl","wb") as f:
                pickle.dump(mdl,f)
            st.success("SVC Model trained and saved")

def run_model_evaluation():
    st.title("Evaluate Models")
    model_type = st.selectbox("Select Model to Evaluate",["RandomForest","SVC"])
    test_file = st.file_uploader("Upload Test CSV", type=["csv"])
    if test_file:
        df = pd.read_csv(test_file)
        if st.button("Evaluate"):
            if model_type=="RandomForest":
                path="models/loan_approval_model.pkl"
            else:
                path="models/svc_loan.pkl"
            try:
                loaded=pickle.load(open(path,"rb"))
                X = df.drop("Loan_Approved", axis=1)
                y = df["Loan_Approved"]
                from sklearn.metrics import accuracy_score
                preds=loaded.predict(X)
                acc=accuracy_score(y,preds)
                st.write(f"Accuracy: {acc:.2f}")
            except:
                st.error("Error evaluating model")

def advanced_feature_importance(mdl, columns):
    imp = mdl.feature_importances_
    df = pd.DataFrame({"feature":columns,"importance":imp}).sort_values("importance",ascending=False)
    return df

def run_importance_check():
    st.title("Feature Importance Check")
    try:
        loaded=pickle.load(open("models/loan_approval_model.pkl","rb"))
        feats=["Marks_10th","Marks_12th","CGPA","Parents_Credit_Score","Student_Credit_Score","Total_Assets","Fixed_Deposit","Selected_Exam_Rank"]
        imp=advanced_feature_importance(loaded,feats)
        st.dataframe(imp)
    except:
        st.error("Error loading model")