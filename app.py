import hashlib
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import plotly.express as px
import time
from PIL import Image
import pytesseract
import requests
from bs4 import BeautifulSoup
import numpy as np
import pdf2image
from googletrans import Translator
import io
import yfinance as yf
import seaborn as sns

# -------------------------------
# Custom CSS for animations and styling
st.markdown("""
<style>
@keyframes float {
    0% { transform: translateY(0px); }
    50% { transform: translateY(-20px); }
    100% { transform: translateY(0px); }
}
@keyframes gradientBackground {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
body {
    background: linear-gradient(-45deg, #ff7e5f, #feb47b, #ff6a6a, #ffcc5c);
    background-size: 400% 400%;
    animation: gradientBackground 15s ease infinite;
}
.hero {
    text-align: center;
    padding: 4rem 0;
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border-radius: 15px;
    animation: float 6s ease-in-out infinite;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
.feature-card {
    padding: 1.5rem;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    margin: 1rem 0;
    transition: transform 0.3s, box-shadow 0.3s;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.3);
}
.feature-card:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}
.section-title {
    border-left: 5px solid #ff6f61;
    padding-left: 1rem;
    margin: 2rem 0;
    color: white;
}
.stButton>button {
    background: linear-gradient(45deg, #ff6f61, #ffcc5c);
    color: white;
    border: none;
    border-radius: 25px;
    padding: 0.75rem 2rem;
    font-size: 1rem;
    transition: transform 0.3s, box-shadow 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
}
.stTextInput>div>div>input {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}
.stTextInput>div>div>input::placeholder {
    color: rgba(255, 255, 255, 0.5);
}
.stSelectbox>div>div>select {
    background: rgba(255, 255, 255, 0.2);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}
.stRadio>div>label {
    color: white;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: white;
}
.animation-3d {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    background: url('https://www.transparenttextures.com/patterns/diamond-upholstery.png');
    animation: rotate3D 60s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Session state initialization for user management
if 'users' not in st.session_state:
    st.session_state['users'] = {}
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'current_user' not in st.session_state:
    st.session_state['current_user'] = None

# -------------------------------
# Password Hashing Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# -------------------------------
# Signup Page
def signup_page():
    st.title("Sign Up for Finsight 💼")
    st.markdown("Create your account to access AI-powered financial insights.")
    with st.form("signup_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        if st.form_submit_button("Sign Up"):
            if username in st.session_state['users']:
                st.error("Username already exists. Please choose a different username.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                st.session_state['users'][username] = hash_password(password)
                st.success("Account created successfully! Please log in.")
                time.sleep(1)
                st.session_state['current_page'] = "login"
                st.rerun()

# -------------------------------
# Login Page
def login_page():
    st.title("Login to Finsight 💼")
    st.markdown("Welcome back! Please log in to continue.")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if username in st.session_state['users'] and st.session_state['users'][username] == hash_password(password):
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = username
                st.success("Logged in successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Invalid username or password.")

# -------------------------------
# Logout Function
def logout():
    st.session_state['logged_in'] = False
    st.session_state['current_user'] = None
    st.success("Logged out successfully!")
    time.sleep(1)
    st.rerun()

# -------------------------------
# Sidebar Navigation (Expanded to include new features)
def sidebar():
    st.sidebar.title("Navigation")
    options = [
        "Home", 
        "Smart Document Analysis", 
        "Multi-Language OCR", 
        "Education Loan Eligibility"
    ]
    selection = st.sidebar.radio("Go to", options)
    if st.session_state['logged_in']:
        if st.sidebar.button("Logout"):
            logout()
    return selection

# -------------------------------
# Home Page
def home_page():
    st.markdown("""
    <div class="hero">
        <h1 style="font-size:3.5rem; margin-bottom:1rem; background: linear-gradient(45deg, #fff, #ff6f61); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Finsight 💼</h1>
        <h3 style="font-weight:300;">AI-Powered Financial Intelligence Platform</h3>
    </div>
    <div style="text-align: center; margin: 3rem 0;">
        <h2>Transform Your Financial Future</h2>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 2rem;">
            <div class="feature-card">
                <h4>📚 Smart Analysis</h4>
                <p>Advanced document processing powered by AI</p>
            </div>
            <div class="feature-card">
                <h4>🎓 Education Loans</h4>
                <p>Personalized loan eligibility assessment</p>
            </div>
            <div class="feature-card">
                <h4>📈 Financial Insights</h4>
                <p>Data-driven recommendations for success</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------
# Document Analysis Functions
def process_unstructured_data():
    st.header("📑 Unstructured Data Analysis (CSV)")
    uploaded_file = st.file_uploader("Upload Unstructured CSV File", type=["csv"])
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### Uploaded Data:")
            st.write(df)
            if "Frequency" in df.columns and "Price range" in df.columns:
                st.subheader("K-Means Clustering Analysis")
                process_kmeans_clustering(df)
            else:
                st.error("CSV file must contain 'Frequency' and 'Price range' columns.")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def process_kmeans_clustering(df):
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[["Frequency", "Price range"]])
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df["cluster"] = kmeans.fit_predict(scaled_data)
    st.subheader("Updated Dataset with Clusters:")
    st.write(df)
    st.subheader("Cluster Interpretations")
    cluster_info = {
        0: "Cluster 0: Low Frequency, Low Price Range",
        1: "Cluster 1: High Frequency, High Price Range",
        2: "Cluster 2: Medium Frequency, Medium Price Range"
    }
    for cluster, meaning in cluster_info.items():
        st.write(f"{meaning}")
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df["Frequency"], df["Price range"], c=df["cluster"], cmap="viridis", edgecolors="k")
    plt.colorbar(scatter, label="Cluster")
    plt.xlabel("Frequency of Purchases")
    plt.ylabel("Price Range")
    plt.title("K-Means Clustering of Items")
    st.pyplot(plt)
    st.markdown("""
    **Clustering Visualization Analysis:**
    - Each point represents an item's purchasing pattern
    - **X-Axis:** Frequency of purchases (normalized scale)
    - **Y-Axis:** Price range of items (normalized scale)
    - **Color Mapping:** 
      - Purple: Cluster 0 (Low frequency, low price)
      - Yellow: Cluster 1 (High frequency, high price)
      - Green: Cluster 2 (Medium frequency, medium price)
    - **Business Insight:** Identify high-value frequent purchase items for inventory optimization
    """)

def process_structured_data():
    st.header("📑 Structured Data Analysis")
    file_type = st.selectbox("Select Data Type", ["Cash Flow", "Payslips", "Bank Statements", "Profit and Loss", "Invoices"])
    uploaded_file = st.file_uploader("Upload Structured Document", type=["jpg", "png"])
    if uploaded_file:
        try:
            img = Image.open(uploaded_file)
            st.image(img, caption="Uploaded Document", use_container_width=True)
            with st.spinner("🔍 Extracting Text..."):
                extracted_text = pytesseract.image_to_string(img)
                time.sleep(1)
            if extracted_text.strip():
                with st.expander("📄 View Extracted Text"):
                    st.code(extracted_text, language="text")
                process_structured_analysis(file_type, extracted_text)
            else:
                st.warning("No text found in the document")
        except Exception as e:
            st.error(f"Error: {str(e)}")

def process_structured_analysis(file_type, extracted_text):
    st.subheader("Structured Data Analysis Example")
    st.write(f"Processing {file_type} data...")
    if file_type == "Cash Flow":
        data = {
            "Month": ["January", "February", "March", "April"],
            "Income": [5000, 5500, 6000, 6500],
            "Expenses": [3000, 3500, 4000, 4500]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x='Month', y=['Income', 'Expenses'], title="Cash Flow Analysis", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig)
        fig_pie = px.pie(df, names='Month', values='Income', title="Income Distribution by Month", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
    elif file_type == "Bank Statements":
        data = {
            "Date": ["01/01", "02/01", "03/01", "04/01"],
            "Debit": [200, 300, 250, 350],
            "Credit": [1000, 1200, 1100, 1300]
        }
        df = pd.DataFrame(data)
        fig_bar = px.bar(df, x='Date', y=['Debit', 'Credit'], title="Bank Statement Overview", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)
        fig_pie = px.pie(df, names='Date', values='Credit', title="Credit Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
    elif file_type == "Payslips":
        data = {
            "Month": ["Jan", "Feb", "Mar", "Apr"],
            "Basic Salary": [30000, 31000, 32000, 33000],
            "Deductions": [5000, 5200, 5400, 5600]
        }
        df = pd.DataFrame(data)
        fig = px.bar(df, x="Month", y=["Basic Salary", "Deductions"], title="Salary Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig)
        fig_pie = px.pie(df, names="Month", values="Basic Salary", title="Salary Distribution by Month", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
    elif file_type == "Profit and Loss":
        data = {
            "Category": ["Revenue", "COGS", "Operating Expenses", "Net Profit"],
            "Amount": [100000, 40000, 30000, 30000]
        }
        df = pd.DataFrame(data)
        fig_pie = px.pie(df, names="Category", values="Amount", title="Profit & Loss Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)
        fig_bar = px.bar(df, x="Category", y="Amount", title="Profit & Loss Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)
    elif file_type == "Invoices":
        data = {
            "Item": ["Hourly Car Rental", "Weekly Car Rent", "Monthly Car Rental"],
            "Amount": [88.00, 328.00, 1410.00]
        }
        df = pd.DataFrame(data)
        fig_bar = px.bar(df, x='Item', y='Amount', title="Invoice Amount Breakdown", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_bar)
        fig_pie = px.pie(df, names='Item', values='Amount', title="Invoice Amount Distribution", color_discrete_sequence=px.colors.qualitative.Dark24)
        st.plotly_chart(fig_pie)

# -------------------------------
# NEW: Multi-Language OCR Function (from ex.txt)
def extract_and_translate(file):
    file_type = file.type
    translator = Translator()
    if "image" in file_type:
        image = Image.open(file)
        extracted_text = pytesseract.image_to_string(image, lang='eng+hin+tam+kan+tel')
    elif file_type == "application/pdf":
        images = pdf2image.convert_from_bytes(file.read())
        extracted_text = "\n".join([pytesseract.image_to_string(img, lang='eng+hin+tam+kan+tel') for img in images])
    else:
        extracted_text = "Unsupported file format"
    translated_text = translator.translate(extracted_text, dest='en').text
    return extracted_text, translated_text

# -------------------------------
# NEW: Stock Market Analyzer for Semi-Structured Data (from ex.txt)
def compare_stocks():
    st.header("📈 Live Stock Market Analyzer")
    time_periods = {
        "1 Week": "7d",
        "1 Month": "1mo",
        "3 Months": "3mo",
        "6 Months": "6mo",
        "1 Year": "1y",
        "5 Years": "5y",
        "All Time": "max"
    }
    stock1 = st.text_input("🔹 Enter First Stock Symbol (e.g., AAPL for Apple)", "AAPL").upper()
    stock2 = st.text_input("🔹 Enter Second Stock Symbol (e.g., TSLA for Tesla)", "TSLA").upper()
    time_period = st.selectbox("📊 Select Time Period", list(time_periods.keys()))
    if st.button("Compare Stocks"):
        try:
            period = time_periods[time_period]
            stock1_data = yf.download(stock1, period=period, interval="1d")["Close"]
            stock2_data = yf.download(stock2, period=period, interval="1d")["Close"]
            if stock1_data.empty or stock2_data.empty:
                st.error("⚠️ No stock data available. Try selecting another stock or period.")
                return
            df = pd.DataFrame({
                stock1: stock1_data.squeeze(),
                stock2: stock2_data.squeeze()
            })
            df.index = pd.to_datetime(df.index)
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df, linewidth=2.5)
            plt.title(f"Stock Comparison: {stock1} vs {stock2}")
            plt.xlabel("Date")
            plt.ylabel("Stock Price (USD)")
            plt.legend([stock1, stock2])
            st.pyplot(plt)
        except Exception as e:
            st.error(f"⚠️ Error fetching stock data: {e}")

# -------------------------------
# NEW: Unsupervised Analysis using DBSCAN (from ex1.txt)
def process_unsupervised_data():
    st.header("🔍 Unsupervised Analysis")
    uploaded_file = st.file_uploader("Upload CSV for Unsupervised Analysis", type=["csv"], key="unsupervised")
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("### Original Data:")
            st.write(df)
            # Check for specific columns to decide which clustering to run
            if "Frequency" in df.columns and "Price range" in df.columns:
                st.subheader("K-Means Clustering Analysis")
                process_kmeans_clustering(df)
            else:
                # Proceed with DBSCAN clustering on all numeric columns (silhouette score removed)
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                if len(numeric_cols) < 2:
                    st.error("At least two numeric columns are required for unsupervised analysis.")
                    return
                X = df[numeric_cols]
                from sklearn.cluster import DBSCAN
                dbscan = DBSCAN(eps=0.5, min_samples=5)
                clusters = dbscan.fit_predict(X)
                df['DBSCAN_Cluster'] = clusters
                st.write("### Data with DBSCAN Clusters:")
                st.write(df)
                plt.figure(figsize=(8, 5))
                import seaborn as sns
                sns.scatterplot(data=df, x=numeric_cols[0], y=numeric_cols[1], hue='DBSCAN_Cluster', palette="viridis", s=100)
                plt.title("DBSCAN Clustering")
                st.pyplot(plt)
        except Exception as e:
            st.error(f"Error: {e}")

# -------------------------------
def show_student_loan_page():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🎓 Student Loan Recommendation</h1>", unsafe_allow_html=True)
    with st.form("loan_form"):
        name, age, tenth_score, twelfth_score, family_income, category, exam_score = get_loan_inputs()
        submitted = st.form_submit_button("Check Eligibility")
        if submitted:
            eligibility, reasons = check_eligibility(name, age, tenth_score, twelfth_score, family_income, category, exam_score)
            st.session_state.loan_result = {
                "name": name,
                "category": category,
                "eligible": eligibility,
                "reasons": reasons
            }
    # Outside the form: display results if available
    if "loan_result" in st.session_state:
        result = st.session_state.loan_result
        if result["eligible"]:
            display_loan_offers(result["name"], result["category"])
        else:
            st.error(f"Sorry {result['name']}, you are not eligible due to:")
            for reason in result["reasons"]:
                st.error(f"- {reason}")

def get_loan_inputs():
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Name", key="loan_name")
        age = st.number_input("Age", min_value=16, max_value=60, key="loan_age")
        tenth_score = st.number_input("10th Grade Score (%)", min_value=0.0, max_value=100.0, key="tenth_score")
    with col2:
        twelfth_score = st.number_input("12th Grade Score (%)", min_value=0.0, max_value=100.0, key="twelfth_score")
        family_income = st.number_input("Family Income (INR)", min_value=0, key="family_income")
        category = st.selectbox("Category", ["Undergraduate", "Postgraduate", "Abroad Studies"], key="loan_category")
    # Additional input: Standardized Exam Score
    exam_score = st.number_input("Standardized Exam Score (%)", min_value=0.0, max_value=100.0, key="exam_score")
    return name, age, tenth_score, twelfth_score, family_income, category, exam_score

def check_eligibility(name, age, tenth, twelfth, income, category, exam_score):
    eligibility = True
    reasons = []
    
    if tenth < 75:
        eligibility = False
        reasons.append("10th score below 75%")
    if twelfth < 75:
        eligibility = False
        reasons.append("12th score below 75%")
    if exam_score < 60:
        eligibility = False
        reasons.append("Standardized Exam Score below 60%")
        
    income_limits = {
        "Undergraduate": 1500000,
        "Postgraduate": 2000000,
        "Abroad Studies": 2500000
    }
    if income > income_limits.get(category, 1500000):
        eligibility = False
        reasons.append(f"Family income exceeds limit for {category}")
        
    age_limits = {
        "Undergraduate": 25,
        "Postgraduate": 30,
        "Abroad Studies": 35
    }
    if age > age_limits.get(category, 25):
        eligibility = False
        reasons.append(f"Age exceeds limit for {category}")
    
    return eligibility, reasons

def display_loan_offers(name, category):
    st.success(f"🎉 Congratulations {name}, you are eligible for a {category} education loan!")
    st.markdown("### 📜 Bank Offers")
    
    loan_offers = {
        "Undergraduate": [
            {"Bank": "SBI Bank", "Interest Rate": "8.5%", "Max Loan": "15 Lakh", "Tenure": "7 Years"},
            {"Bank": "HDFC Bank", "Interest Rate": "9.0%", "Max Loan": "20 Lakh", "Tenure": "10 Years"},
            {"Bank": "Axis Bank", "Interest Rate": "9.5%", "Max Loan": "25 Lakh", "Tenure": "12 Years"}
        ],
        "Postgraduate": [
            {"Bank": "ICICI Bank", "Interest Rate": "8.0%", "Max Loan": "30 Lakh", "Tenure": "12 Years"},
            {"Bank": "Kotak Bank", "Interest Rate": "8.2%", "Max Loan": "35 Lakh", "Tenure": "15 Years"},
            {"Bank": "Bank of Baroda", "Interest Rate": "8.7%", "Max Loan": "40 Lakh", "Tenure": "15 Years"}
        ],
        "Abroad Studies": [
            {"Bank": "Axis Bank", "Interest Rate": "7.5%", "Max Loan": "1.5 Crore", "Tenure": "20 Years"},
            {"Bank": "IDFC First Bank", "Interest Rate": "7.8%", "Max Loan": "2 Crore", "Tenure": "20 Years"},
            {"Bank": "Yes Bank", "Interest Rate": "8.2%", "Max Loan": "1.75 Crore", "Tenure": "18 Years"}
        ]
    }
    
    for offer in loan_offers.get(category, []):
        with st.expander(f"{offer['Bank']} Offer"):
            st.markdown(f"**Interest Rate**: {offer['Interest Rate']}")
            st.markdown(f"**Maximum Loan Amount**: {offer['Max Loan']}")
            st.markdown(f"**Repayment Tenure**: {offer['Tenure']}")
            st.markdown(f"**Special Features**: {get_special_features(offer['Bank'])}")
    
    # EMI Calculator Section (displayed outside any form)
    st.markdown("### 🧮 EMI Calculator")
    col1, col2, col3 = st.columns(3)
    with col1:
        principal = st.number_input("Loan Amount (₹)", min_value=0, key="emi_principal")
    with col2:
        rate_of_interest = st.number_input("Annual Interest Rate (%)", min_value=0.0, key="emi_rate")
    with col3:
        tenure_years = st.number_input("Tenure (Years)", min_value=0, key="emi_tenure")
    if st.button("Calculate EMI", key="emi_calc"):
        if principal > 0 and rate_of_interest > 0 and tenure_years > 0:
            monthly_interest = rate_of_interest / (12 * 100)
            tenure_months = tenure_years * 12
            emi = (principal * monthly_interest * (1 + monthly_interest) ** tenure_months) / ((1 + monthly_interest) ** tenure_months - 1)
            st.success(f"✅ Your EMI is ₹ {emi:.2f} per month")
        else:
            st.warning("⚠️ Please enter valid values to calculate EMI.")

def get_special_features(bank):
    features = {
        "SBI Bank": "No collateral required for loans up to 15 Lakh",
        "HDFC Bank": "Flexible repayment options after 1 year moratorium",
        "ICICI Bank": "Interest-only payments during study period",
        "Axis Bank": "Free forex card with international transactions",
        "Kotak Bank": "Career counseling services included",
        "Bank of Baroda": "Low processing fee of 0.5%",
        "IDFC First Bank": "Currency hedging options available",
        "Yes Bank": "Airport pickup service for international students"
    }
    return features.get(bank, "Contact bank for special features")
# -------------------------------
# Main Function
def main():
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = "login"
    if not st.session_state['logged_in']:
        if st.session_state['current_page'] == "login":
            login_page()
            if st.button("Don't have an account? Sign Up"):
                st.session_state['current_page'] = "signup"
                st.rerun()
        elif st.session_state['current_page'] == "signup":
            signup_page()
            if st.button("Already have an account? Log In"):
                st.session_state['current_page'] = "login"
                st.rerun()
    else:
        selection = sidebar()
        if selection == "Home":
            home_page()
        elif selection == "Smart Document Analysis":
            data_type = st.selectbox("Choose Data Type", ["Structured", "Semi-Structured", "Unstructured"])
            if data_type == "Structured":
                process_structured_data()
            elif data_type == "Semi-Structured":
                compare_stocks()
            elif data_type == "Unstructured":
                process_unsupervised_data()
        elif selection == "Multi-Language OCR":
            st.header("🌍 Extract & Translate Text")
            uploaded_file = st.file_uploader("📂 Upload a file", type=["png", "jpg", "jpeg", "tiff", "pdf", "docx"])
            if uploaded_file is not None:
                extracted_text, translated_text = extract_and_translate(uploaded_file)
                st.text_area("📝 Original Text:", extracted_text, height=150)
                st.text_area("🌐 Translated Text:", translated_text, height=150)
        elif selection == "Education Loan Eligibility":
            show_student_loan_page()

if __name__ == "__main__":
    main()
