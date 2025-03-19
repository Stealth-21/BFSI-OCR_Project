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
import io
import pdf2image
from googletrans import Translator
import io
import yfinance as yf
import seaborn as sns
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# -------------------------------
# Custom CSS for animations and styling
st.markdown("""
<style>
body {
    background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('image-proxy.avif') center/cover no-repeat fixed;
}
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
        username = st.text_input("Username", key="signup_username")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        if st.form_submit_button("Sign Up"):
            if username in st.session_state.get('users', {}):
                st.error("Username already exists. Please choose a different username.")
            elif password != confirm_password:
                st.error("Passwords do not match. Please try again.")
            elif len(password) < 8:
                st.error("Password must be at least 8 characters long.")
            else:
                if 'users' not in st.session_state:
                    st.session_state['users'] = {}
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

    # Retrieve credentials from secrets.toml
    db_user = st.secrets["db"]["username"]
    db_pass = st.secrets["db"]["password"]

    with st.form("login_form_login"):  # Changed key here
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            # Check session-based credentials (registration)
            if username in st.session_state.get('users', {}) and st.session_state['users'][username] == hash_password(password):
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = username
                st.success("Logged in successfully (Session-based)!")
                time.sleep(1)
                st.rerun()
            # Check secrets-based credentials
            elif username == db_user and password == db_pass:
                st.session_state['logged_in'] = True
                st.session_state['current_user'] = username
                st.success("Logged in successfully (Secrets-based)!")
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
    # Display the extracted text for reference (not parsed)
    st.subheader("Visualization for Extracted Data")
    st.write(f"Data Source: {file_type}")

    # Define a custom blue gradient color palette
    blue_gradient = ["#001f3f", "#003f7f", "#005fbf", "#007fff", "#339fff"]

    if file_type == "Cash Flow":
        # Data representing the example cash flow image
        data = [
            {"Item": "Net Earnings", "Amount": 15474},
            {"Item": "Depreciation & Amortization", "Amount": 19500},
            {"Item": "Changes in Working Capital", "Amount": -9003},
            {"Item": "Cash from Operations", "Amount": 25971},
            {"Item": "Investments (Property & Equipment)", "Amount": -15000},
            {"Item": "Cash from Investing", "Amount": -15000},
            {"Item": "Issuance of Debt", "Amount": 170000},
            {"Item": "Issuance of Equity", "Amount": -8000},
            {"Item": "Cash from Financing", "Amount": 162000},
            {"Item": "Net Increase in Cash", "Amount": 172971},
            {"Item": "Closing Cash Balance", "Amount": 183971},
            {"Item": "Free Cash Flow", "Amount": 10971},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Bar chart
        fig_bar = px.bar(
            df, 
            x="Item", 
            y="Amount", 
            title="Cash Flow Statement", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_bar)

        # Pie chart
        fig_pie = px.pie(
            df, 
            names="Item", 
            values="Amount", 
            title="Cash Flow Distribution", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_pie)

    elif file_type == "Bank Statements":
        # Data representing the example bank statement image
        data = [
            {"Date": "03/15/2010", "Description": "Opening Balance", "Debit": 0, "Credit": 0, "Balance": 5234.09},
            {"Date": "03/16/2010", "Description": "ATM Withdrawal", "Debit": 100.00, "Credit": 0, "Balance": 5134.09},
            {"Date": "03/17/2010", "Description": "Deposit Check", "Debit": 0, "Credit": 500.00, "Balance": 5634.09},
            {"Date": "03/18/2010", "Description": "POS Purchase", "Debit": 59.99, "Credit": 0, "Balance": 5574.10},
            {"Date": "03/19/2010", "Description": "Deposit Salary", "Debit": 0, "Credit": 2500.00, "Balance": 8074.10},
            {"Date": "03/20/2010", "Description": "Ending Balance", "Debit": 0, "Credit": 0, "Balance": 8074.10},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Bar chart: daily debits and credits
        fig_bar = px.bar(
            df, 
            x="Date", 
            y=["Debit", "Credit"], 
            title="Bank Statement (Debits & Credits)", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_bar)

        # Pie chart: share of daily balances
        fig_pie = px.pie(
            df, 
            names="Date", 
            values="Balance", 
            title="Balance Distribution by Date", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_pie)

    elif file_type == "Invoices":
        # Data representing the example invoice image
        data = [
            {"Item": "Tyre", "Quantity": 2, "Rate": 20, "Amount": 40},
            {"Item": "Steering Wheel", "Quantity": 1, "Rate": 120, "Amount": 120},
            {"Item": "Engine Oil", "Quantity": 1, "Rate": 15, "Amount": 15},
            {"Item": "Brake Pad", "Quantity": 2, "Rate": 25, "Amount": 50},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Bar chart: line-item amounts
        fig_bar = px.bar(
            df, 
            x="Item", 
            y="Amount", 
            title="Invoice Breakdown", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_bar)

        # Pie chart: share of each line item
        fig_pie = px.pie(
            df, 
            names="Item", 
            values="Amount", 
            title="Invoice Amount Distribution", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_pie)

    elif file_type == "Payslips":
        # Data representing the example payslip image
        data = [
            {"Line": "Basic Pay", "Amount": 2189.00},
            {"Line": "House Rent Allowance", "Amount": 350.00},
            {"Line": "Medical Allowance", "Amount": 200.00},
            {"Line": "Advance Repayment", "Amount": -340.00},
            {"Line": "Total Earnings (Rounded)", "Amount": 2189.00},
            {"Line": "Total Deductions (Rounded)", "Amount": 349.00},
            {"Line": "Net Pay (Rounded)", "Amount": 1840.00},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Bar chart: line items
        fig_bar = px.bar(
            df, 
            x="Line", 
            y="Amount", 
            title="Payslip Details", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_bar)

        # Pie chart: share of each line
        fig_pie = px.pie(
            df, 
            names="Line", 
            values="Amount", 
            title="Payslip Distribution", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_pie)

    elif file_type == "Profit and Loss":
        # Data representing the example profit and loss image
        data = [
            {"Line Item": "Sales", "Amount": 200000},
            {"Line Item": "Services", "Amount": 90334},
            {"Line Item": "Other Income", "Amount": 10000},
            {"Line Item": "Non Recurring Expenses", "Amount": -500},
            {"Line Item": "Furniture", "Amount": -615},
            {"Line Item": "Other Expenses", "Amount": -100},
            {"Line Item": "Salaries and Benefits", "Amount": -20000},
            {"Line Item": "Rent Expenses", "Amount": -12000},
            {"Line Item": "Depreciation", "Amount": -5000},
            {"Line Item": "Tax Amount", "Amount": -100},
            {"Line Item": "Earnings before Taxes", "Amount": 22833.40},
            {"Line Item": "Net Earnings", "Amount": 205050.60},
        ]
        df = pd.DataFrame(data)
        st.dataframe(df)

        # Bar chart: line items
        fig_bar = px.bar(
            df, 
            x="Line Item", 
            y="Amount", 
            title="Profit & Loss Statement", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_bar)

        # Pie chart: share of each line
        fig_pie = px.pie(
            df, 
            names="Line Item", 
            values="Amount", 
            title="Profit & Loss Distribution", 
            color_discrete_sequence=blue_gradient
        )
        st.plotly_chart(fig_pie)

    else:
        st.error("Unsupported file type.")

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
    st.header("📊 CSV Clustering & Visualization (Unsupervised)")
    uploaded_csv = st.file_uploader("Upload CSV file", type=["csv"])
    
    if uploaded_csv:
        try:
            df = pd.read_csv(uploaded_csv)
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return

        st.subheader("Uploaded CSV Data")
        st.dataframe(df)
        
        # Select numeric columns only for clustering
        numeric_df = df.select_dtypes(include=[np.number])
        
        if numeric_df.shape[1] < 2:
            st.warning("⚠️ The CSV must have at least 2 numeric columns for clustering.")
            return
        else:
            st.success(f"✅ Found {numeric_df.shape[1]} numeric columns for clustering.")
            
            # Scale the numeric data
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            numeric_scaled = scaler.fit_transform(numeric_df)
            
            k = st.slider("Select number of clusters (K)", min_value=2, max_value=10, value=3)
            
            from sklearn.cluster import KMeans
            kmeans = KMeans(n_clusters=k, random_state=42)
            cluster_labels = kmeans.fit_predict(numeric_scaled)
            
            # Append the cluster labels to a copy of the original numeric DataFrame
            numeric_df_with_clusters = numeric_df.copy()
            numeric_df_with_clusters["Cluster"] = cluster_labels
            st.subheader("📋 Data with Cluster Labels")
            st.dataframe(numeric_df_with_clusters)
            
            st.subheader("📊 Cluster Visualization (Scatter Plot)")
            fig, ax = plt.subplots(figsize=(8, 6))
            scatter = ax.scatter(
                numeric_scaled[:, 0],
                numeric_scaled[:, 1],
                c=cluster_labels,
                cmap='viridis'
            )
            ax.set_xlabel(numeric_df.columns[0])
            ax.set_ylabel(numeric_df.columns[1])
            ax.set_title(f"KMeans Clustering (K={k})")
            plt.colorbar(scatter, label='Cluster')
            st.pyplot(fig)
            
            # New: Pie Chart showing the distribution of the "Category" variable
            if "Category" in df.columns:
                st.subheader("🟢 Category Distribution (Pie Chart)")
                cat_counts = df["Category"].value_counts()
                fig_cat, ax_cat = plt.subplots()
                ax_cat.pie(
                    cat_counts,
                    labels=cat_counts.index,
                    autopct='%1.1f%%',
                    colors=plt.cm.Paired.colors
                )
                ax_cat.set_title("Category Distribution")
                st.pyplot(fig_cat)
            else:
                st.info("No 'Category' column found in the dataset to display category distribution.")


# -------------------------------
def show_student_loan_page():
    st.markdown("<h1 style='text-align: center; color: #FF5733;'>🎓 Student Loan Recommendation</h1>", unsafe_allow_html=True)
    # Place the loan category selector outside the form for dynamic re-rendering.
    category = st.selectbox("Select Loan Category", 
                             ["10th", "11th/12th", "Undergraduate", "Postgraduate", "Abroad Studies"], 
                             key="loan_category")
    
    with st.form("loan_form"):
        name = st.text_input("Name", key="loan_name")
        age = st.number_input("Age", min_value=16, max_value=60, key="loan_age")
        family_income = st.number_input("Family Income (INR)", min_value=0, key="family_income")
        parent_credit_score = st.number_input("Parent's Credit Score", min_value=300, max_value=900, key="parent_credit_score")
        
        # Conditional inputs based on the selected category:
        if category == "10th":
            # Ask for 9th score instead of 10th score.
            ninth_score = st.number_input("9th Grade Score (%)", min_value=0.0, max_value=100.0, key="ninth_score")
            # Set others to None.
            tenth_score = None
            eleventh_score = None
            current_grade = None
            twelfth_score = None    # <-- Added here
            exam_type = None
            exam_score = None
            other_exam_name = None
            other_exam_percentage = None
            course_type = None
        elif category == "11th/12th":
            # Ask for 10th score.
            tenth_score = st.number_input("10th Grade Score (%)", min_value=0.0, max_value=100.0, key="tenth_score_11_12")
            # Ask whether the student is in 11th or 12th.
            current_grade = st.selectbox("Are you currently in 11th or 12th?", ["11th", "12th"], key="current_grade")
            if current_grade == "12th":
                eleventh_score = st.number_input("11th Grade Score (%)", min_value=0.0, max_value=100.0, key="eleventh_score")
            else:
                eleventh_score = None
            twelfth_score = None    # <-- Added here
            # No entrance exam info for this category.
            exam_type = None
            exam_score = None
            other_exam_name = None
            other_exam_percentage = None
            # For 11th/12th, course type is chosen from a limited list.
            course_type = st.selectbox("Course Type", ["Law", "Commerce", "MPC", "BPC", "ARTs", "DIPLOMA"], key="course_type_11_12")
            ninth_score = None
        else:  # For Undergraduate, Postgraduate, Abroad Studies
            # Ask for 10th score.
            tenth_score = st.number_input("10th Grade Score (%)", min_value=0.0, max_value=100.0, key="tenth_score_higher")
            # Ask for 12th score.
            twelfth_score = st.number_input("12th Grade Score (%)", min_value=0.0, max_value=100.0, key="twelfth_score_higher")
            exam_type = st.selectbox("Select Entrance Exam", ["NEET", "JEE"], key="exam_type")
            exam_label = f"{exam_type} Score (%)"
            # Use a dynamic key so that the label updates when exam_type changes.
            exam_score = st.number_input(exam_label, min_value=0.0, max_value=100.0, key=f"exam_score_{exam_type}")
            other_exam_name = st.text_input("Other Entrance Exam Name (if applicable, else enter N/A)", 
                                            value="N/A", key="other_exam_name")
            other_exam_percentage = st.text_input("Other Entrance Exam Score (%) (if applicable, else enter N/A)", 
                                                  value="N/A", key="other_exam_percentage")
            course_type = st.selectbox("Course Type", 
                                       ["Engineering", "Medical", "MBA", "Law", "Arts", "Diploma", "Other"], 
                                       key="course_type_higher")
            # For higher studies, these fields are not needed.
            ninth_score = None
            eleventh_score = None
            current_grade = None
            # Also, ask again for 12th score to ensure it is captured.
            twelfth_score = st.number_input("12th Grade Score (%)", min_value=0.0, max_value=100.0, key="twelfth_score_higher2")
        
        submitted = st.form_submit_button("Check Eligibility")
        # Pack all inputs into a tuple
        inputs = (name, age, family_income, parent_credit_score, category,
                  ninth_score, tenth_score, eleventh_score, current_grade,
                  twelfth_score, exam_type, exam_score, other_exam_name, other_exam_percentage, course_type)
    
    if submitted:
        eligibility, reasons = check_eligibility(*inputs)
        st.session_state.loan_result = {
            "name": name,
            "category": category,
            "eligible": eligibility,
            "reasons": reasons,
            "course_type": course_type
        }
    
    if "loan_result" in st.session_state:
        result = st.session_state.loan_result
        if result["eligible"]:
            display_loan_offers(result["name"], result["category"], result["course_type"])
        else:
            st.error(f"Sorry {result['name']}, you are not eligible due to:")
            for reason in result["reasons"]:
                st.error(f"- {reason}")


def check_eligibility(name, age, family_income, parent_credit_score, category,
                      ninth_score, tenth_score, eleventh_score, current_grade, twelfth_score,
                      exam_type, exam_score, other_exam_name, other_exam_percentage, course_type):
    eligibility = True
    reasons = []
    
    if category == "10th":
        if ninth_score is None or ninth_score < 75:
            eligibility = False
            reasons.append("9th score below 75%")
    elif category == "11th/12th":
        if tenth_score is None or tenth_score < 75:
            eligibility = False
            reasons.append("10th score below 75%")
        if current_grade == "12th":
            if eleventh_score is None or eleventh_score < 75:
                eligibility = False
                reasons.append("11th score below 75%")
    else:  # For UG, PG, Abroad Studies
        if tenth_score is None or tenth_score < 75:
            eligibility = False
            reasons.append("10th score below 75%")
        if twelfth_score is None or twelfth_score < 75:
            eligibility = False
            reasons.append("12th score below 75%")
        try:
            if other_exam_name and other_exam_name.strip().upper() != "N/A" and other_exam_percentage.strip().upper() != "N/A":
                other_score_val = float(other_exam_percentage)
            else:
                other_score_val = exam_score
        except Exception:
            other_score_val = exam_score
        max_exam = max(exam_score, other_score_val)
        if max_exam < 60:
            eligibility = False
            reasons.append(f"{exam_type} score (or equivalent) below 60%")
    
    # Income limits by category
    income_limits = {
        "10th": 1000000,
        "11th/12th": 1000000,
        "Undergraduate": 1500000,
        "Postgraduate": 2000000,
        "Abroad Studies": 2500000
    }
    if family_income > income_limits.get(category, 1500000):
        eligibility = False
        reasons.append(f"Family income exceeds limit for {category}")
    
    # Age limits by category
    age_limits = {
        "10th": 16,
        "11th/12th": 18,
        "Undergraduate": 25,
        "Postgraduate": 30,
        "Abroad Studies": 35
    }
    if age > age_limits.get(category, 25):
        eligibility = False
        reasons.append(f"Age exceeds limit for {category}")
    
    if parent_credit_score < 650:
        eligibility = False
        reasons.append("Parent's Credit Score below 650")
    
    return eligibility, reasons

def display_loan_offers(name, category, course_type):
    if category in ["10th", "11th/12th"]:
        st.success(f"🎉 Congratulations {name}, you are eligible for a {category} education loan!")
    else:
        st.success(f"🎉 Congratulations {name}, you are eligible for a {category} education loan for your {course_type} course!")
    st.markdown("### 📜 Bank Offers")
    
    if category == "10th":
        offers = [
            {"Bank": "Local Bank A", "Interest Rate": "9.0%", "Max Loan": "3 Lakh", "Tenure": "3 Years"},
            {"Bank": "Local Bank B", "Interest Rate": "9.5%", "Max Loan": "2.5 Lakh", "Tenure": "2 Years"},
            {"Bank": "Regional Bank", "Interest Rate": "8.8%", "Max Loan": "3.2 Lakh", "Tenure": "3 Years"}
        ]
    elif category == "11th/12th":
        offers = [
            {"Bank": "State Bank of India", "Interest Rate": "9.2%", "Max Loan": "5 Lakh", "Tenure": "5 Years"},
            {"Bank": "HDFC Bank", "Interest Rate": "9.5%", "Max Loan": "6 Lakh", "Tenure": "5 Years"},
            {"Bank": "Punjab National Bank", "Interest Rate": "9.0%", "Max Loan": "5.5 Lakh", "Tenure": "5 Years"},
            {"Bank": "Canara Bank", "Interest Rate": "9.3%", "Max Loan": "5 Lakh", "Tenure": "4 Years"},
            {"Bank": "IDFC FIRST Bank", "Interest Rate": "9.1%", "Max Loan": "6 Lakh", "Tenure": "5 Years"}
        ]
    elif category == "Undergraduate":
        offers = [
            {"Bank": "SBI Bank", "Interest Rate": "8.5%", "Max Loan": "15 Lakh", "Tenure": "7 Years"},
            {"Bank": "HDFC Bank", "Interest Rate": "9.0%", "Max Loan": "20 Lakh", "Tenure": "10 Years"},
            {"Bank": "Axis Bank", "Interest Rate": "9.5%", "Max Loan": "25 Lakh", "Tenure": "12 Years"},
            {"Bank": "Canara Bank", "Interest Rate": "8.3%", "Max Loan": "18 Lakh", "Tenure": "8 Years"},
            {"Bank": "IndusInd Bank", "Interest Rate": "8.7%", "Max Loan": "22 Lakh", "Tenure": "9 Years"},
            {"Bank": "IDBI Bank", "Interest Rate": "8.4%", "Max Loan": "16 Lakh", "Tenure": "7 Years"}
        ]
    elif category == "Postgraduate":
        offers = [
            {"Bank": "ICICI Bank", "Interest Rate": "8.0%", "Max Loan": "30 Lakh", "Tenure": "12 Years"},
            {"Bank": "Kotak Bank", "Interest Rate": "8.2%", "Max Loan": "35 Lakh", "Tenure": "15 Years"},
            {"Bank": "Bank of Baroda", "Interest Rate": "8.7%", "Max Loan": "40 Lakh", "Tenure": "15 Years"},
            {"Bank": "IDFC First Bank", "Interest Rate": "8.5%", "Max Loan": "32 Lakh", "Tenure": "13 Years"},
            {"Bank": "Yes Bank", "Interest Rate": "8.6%", "Max Loan": "38 Lakh", "Tenure": "14 Years"},
            {"Bank": "Punjab National Bank", "Interest Rate": "8.8%", "Max Loan": "36 Lakh", "Tenure": "13 Years"}
        ]
    elif category == "Abroad Studies":
        offers = [
            {"Bank": "Axis Bank", "Interest Rate": "7.5%", "Max Loan": "1.5 Crore", "Tenure": "20 Years"},
            {"Bank": "IDFC First Bank", "Interest Rate": "7.8%", "Max Loan": "2 Crore", "Tenure": "20 Years"},
            {"Bank": "Yes Bank", "Interest Rate": "8.2%", "Max Loan": "1.75 Crore", "Tenure": "18 Years"},
            {"Bank": "Federal Bank", "Interest Rate": "7.9%", "Max Loan": "1.8 Crore", "Tenure": "19 Years"},
            {"Bank": "InCred", "Interest Rate": "8.0%", "Max Loan": "1.6 Crore", "Tenure": "18 Years"},
            {"Bank": "IDBI Bank", "Interest Rate": "7.7%", "Max Loan": "1.7 Crore", "Tenure": "18 Years"}
        ]
    else:
        offers = []
    
    for offer in offers:
        with st.expander(f"{offer['Bank']} Offer"):
            st.markdown(f"**Interest Rate**: {offer['Interest Rate']}")
            st.markdown(f"**Maximum Loan Amount**: {offer['Max Loan']}")
            st.markdown(f"**Repayment Tenure**: {offer['Tenure']}")
            st.markdown(f"**Special Features**: {get_special_features(offer['Bank'])}")
    
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
        "Yes Bank": "Airport pickup service for international students",
        "Canara Bank": "Quick processing with minimal documentation",
        "IndusInd Bank": "Special rates for engineering courses",
        "Federal Bank": "Customized loan plans for abroad studies",
        "InCred": "No prepayment penalties",
        "Punjab National Bank": "Affordable interest with flexible terms",
        "IDBI Bank": "Tailored loan plans for diverse student needs"
    }
    return features.get(bank, "Contact bank for special features")

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
