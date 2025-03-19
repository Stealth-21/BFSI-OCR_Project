****BFSI-OCR: AI-Powered Financial Intelligence Platform****

BFSI-OCR is an AI-powered platform designed for the banking and financial services industry. It integrates Optical Character Recognition (OCR), document analysis, unsupervised data clustering, stock market analysis, and education loan eligibility—all within a single, interactive Streamlit application. With BFSI-OCR, users can extract and analyze data from various financial documents, generate visual insights, and make informed decisions.

****Features****

**OCR Extraction & Multi-Language Support**

Extract text from images and PDFs in multiple languages (English, Hindi, Tamil, Kannada, Telugu) using Tesseract OCR.

**Structured Document Analysis**

Process and visualize financial documents such as bank statements, cash flow statements, profit and loss reports, invoices, and payslips with interactive charts.

**Unstructured Data Clustering**

Perform unsupervised clustering on CSV data to reveal hidden patterns and trends using advanced machine learning techniques.

**Stock Market Analyzer**

Compare live stock data from Yahoo Finance over various time periods with dynamic, interactive visualizations.

**Education Loan Eligibility Checker**

Assess your eligibility for education loans by inputting your academic and financial details, and view personalized loan offers.

**Advanced Visualizations**

Enjoy interactive bar charts, pie charts, and line graphs—all styled with a modern blue gradient color scheme.

**Secure Authentication**

Register and log in securely using either session-based credentials or via secrets stored in your environment.

**Installation**

**Clone the Repository**

git clone https://github.com/Stealth-21/BFSI-OCR_Project.git

cd BFSI-OCR_Project

**Create and Activate a Virtual Environment (optional but recommended)**

python -m venv venv
venv\Scripts\activate

**Install Dependencies**

pip install -r requirements.txt

**Install Tesseract OCR**

Ensure that Tesseract OCR is installed on your system and its path is set correctly in the code (e.g., on Windows, update pytesseract.pytesseract.tesseract_cmd).

**Configuration**

Create a folder called .streamlit in the root directory.

Inside .streamlit, create a file named secrets.toml with your sensitive credentials. For example:

secrets.toml
[db]
username = "my_secret_user"
password = "my_secret_password"

**Running the Application**

**Run the application with the following command:**
streamlit run app.py

Your default web browser will open, displaying the BFSI-OCR application.

**Usage**

Home: View an overview and introduction to the platform.

Smart Document Analysis: Upload your structured financial documents to extract text and visualize the data interactively.

Multi-Language OCR: Upload images or PDFs to extract and translate text.

Education Loan Eligibility: Enter your academic and financial details to check your eligibility and explore personalized loan offers.

Unstructured Data Analysis: Upload CSV files to perform clustering and visualize the data.

Stock Market Analyzer: Compare live stock data with dynamic charts.

Contributions are welcome! Feel free to fork the repository, make improvements, and submit pull requests. If you encounter any issues or have suggestions, please open an issue on GitHub.
