import streamlit as st
import numpy as np
import pickle
import logging
logger=logging.getLogger(__name__)
def run_loan_prediction():
    st.title("Loan Prediction & Eligibility")
    model=load_loan_model_internal()
    if model:
        marks_10th=st.number_input("10th Grade Marks (%)",min_value=0,max_value=100,step=1)
        marks_12th=st.number_input("12th Grade Marks (%)",min_value=0,max_value=100,step=1)
        cgpa=st.number_input("CGPA",min_value=0.0,max_value=10.0,step=0.1)
        parents_credit_score=st.number_input("Parents' Credit Score",min_value=300,max_value=900,step=1)
        student_credit_score=st.number_input("Student's Credit Score",min_value=300,max_value=900,step=1)
        total_assets=st.number_input("Total Assets (INR)",min_value=0)
        fixed_deposits=st.number_input("Fixed Deposits (INR)",min_value=0)
        exam_choice=st.selectbox("Select Exam",["JEE","SAT","CAT","NEET"])
        selected_exam_rank=st.number_input(f"Enter {exam_choice} Rank",min_value=0)
        if st.button("Predict Loan Eligibility"):
            data_input=[marks_10th,marks_12th,cgpa,parents_credit_score,student_credit_score,total_assets,fixed_deposits,selected_exam_rank]
            res=predict_loan_eligibility_internal(model,data_input)
            if res["status"]=="Approved":
                st.success(f"Loan Approved! Amount: ₹{res['amount']} lakh")
                st.write("Recommended Loan Schemes:")
                for ln in res["loans"]:
                    st.write(f"- {ln}")
            elif res["status"]=="Rejected":
                st.error("Loan Rejected. No loan available.")
            else:
                st.error("Error during prediction")
    else:
        st.error("Model not loaded")
def load_loan_model_internal():
    try:
        mdl=pickle.load(open("models/loan_approval_model.pkl","rb"))
        return mdl
    except:
        return None
def predict_loan_eligibility_internal(mdl,arr):
    try:
        arr_np=np.array(arr).reshape(1,-1)
        pred=mdl.predict(arr_np)[0]
        if pred==1:
            amt=calculate_loan_amount_internal(*arr)
            schemes=find_suitable_loan_internal(amt)
            return {"status":"Approved","amount":amt,"loans":schemes}
        else:
            return {"status":"Rejected","amount":0,"loans":[]}
    except:
        return {"status":"Error","amount":0,"loans":[]}
def calculate_loan_amount_internal(m10,m12,cg,pc,sc,ta,fd,er):
    base=5
    if cg>=9:base+=10
    elif cg>=8:base+=7
    elif cg>=7:base+=4
    avg=(m10+m12)/2
    if avg>90:base+=5
    elif avg>75:base+=3
    if pc>700:base+=3
    if sc>650:base+=2
    if ta>2000000:base+=10
    if fd>1000000:base+=5
    if er<1000:base+=5
    return min(base,100)
def find_suitable_loan_internal(amt):
    data={
        "SBI Student Loan Scheme":(0,10),
        "HDFC Bank Education Loan":(0,20),
        "ICICI Bank Education Loan":(0,100),
        "Avanse Education Loan":(1,500)
    }
    found=[]
    for k,v in data.items():
        if v[0]<=amt<=v[1]:
            found.append(k)
    if not found:
        found.append("No suitable loan found")
    return found
def advanced_loan_analytics(mdl,arr):
    arr_np=np.array(arr).reshape(1,-1)
    proba=mdl.predict_proba(arr_np)
    return proba
def run_loan_analytics():
    st.title("Loan Analytics")
    model=load_loan_model_internal()
    if model:
        m10=st.slider("10th %",0,100,50)
        m12=st.slider("12th %",0,100,60)
        cg=st.slider("CGPA",0.0,10.0,6.5,0.1)
        pc=st.slider("Parent Credit Score",300,900,600)
        sc=st.slider("Student Credit Score",300,900,600)
        ta=st.slider("Total Assets",0,10000000,500000)
        fd=st.slider("Fixed Deposits",0,5000000,100000)
        er=st.slider("Exam Rank",0,100000,500)
        arr_input=[m10,m12,cg,pc,sc,ta,fd,er]
        if st.button("Compute Probability"):
            prob=advanced_loan_analytics(model,arr_input)
            st.write("Probability:",prob)