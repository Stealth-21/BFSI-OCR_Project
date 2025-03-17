import streamlit as st
import logging
import pdfplumber
import pytesseract
import numpy as np
import pandas as pd
import re
import os
from PIL import Image
logger = logging.getLogger(__name__)

def run_document_processing():
    st.title("Advanced Document Processing")
    choice = st.selectbox("Select Document Type", ["Balance Sheet", "Profit & Loss", "Cash Flow", "Invoice", "Misc"])
    file_obj = st.file_uploader("Upload Document", type=["pdf", "png", "jpg", "jpeg"])
    if file_obj:
        if choice == "Balance Sheet":
            res = process_balance_sheet(file_obj)
            st.json(res)
        elif choice == "Profit & Loss":
            res = process_profit_loss(file_obj)
            st.json(res)
        elif choice == "Cash Flow":
            res = process_cash_flow(file_obj)
            st.json(res)
        elif choice == "Invoice":
            res = process_invoice(file_obj)
            st.json(res)
        else:
            res = process_misc_doc(file_obj)
            st.json(res)

def process_balance_sheet(file_obj):
    text = extract_text_advanced(file_obj)
    data = parse_balance_sheet_data(text)
    return data

def process_profit_loss(file_obj):
    text = extract_text_advanced(file_obj)
    data = parse_profit_loss_data(text)
    return data

def process_cash_flow(file_obj):
    text = extract_text_advanced(file_obj)
    data = parse_cash_flow_data(text)
    return data

def process_invoice(file_obj):
    text = extract_text_advanced(file_obj)
    data = parse_invoice_data(text)
    return data

def process_misc_doc(file_obj):
    text = extract_text_advanced(file_obj)
    result = {}
    result["content"] = text[:500]
    result["insights"] = analyze_unstructured_text(text)
    return result

def extract_text_advanced(file_obj):
    ext = os.path.splitext(file_obj.name)[1].lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_obj)
    else:
        return extract_text_from_image(file_obj)

def extract_text_from_pdf(file_obj):
    all_text = []
    try:
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    all_text.append(t)
        return "\n".join(all_text)
    except:
        return "Error reading PDF"

def extract_text_from_image(file_obj):
    try:
        im = Image.open(file_obj)
        txt = pytesseract.image_to_string(im)
        return txt
    except:
        return "Error reading image"

def parse_balance_sheet_data(text):
    total_assets = find_value_in_text(text, r"Total Assets\s*:\s*(\d[\d,\.]*)")
    total_liabilities = find_value_in_text(text, r"Total Liabilities\s*:\s*(\d[\d,\.]*)")
    equity = find_value_in_text(text, r"Shareholder\s*Equity\s*:\s*(\d[\d,\.]*)")
    return {
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "equity": equity
    }

def parse_profit_loss_data(text):
    revenue = find_value_in_text(text, r"Revenue\s*:\s*(\d[\d,\.]*)")
    expenses = find_value_in_text(text, r"Expenses\s*:\s*(\d[\d,\.]*)")
    profit = find_value_in_text(text, r"Net\s*Profit\s*:\s*(\d[\d,\.]*)")
    return {
        "revenue": revenue,
        "expenses": expenses,
        "profit": profit
    }

def parse_cash_flow_data(text):
    operating = find_value_in_text(text, r"Net\s*Cash\s*Flow\s*\(Operating\)\s*:\s*(\d[\d,\.]*)")
    investing = find_value_in_text(text, r"Net\s*Cash\s*Flow\s*\(Investing\)\s*:\s*(\d[\d,\.]*)")
    financing = find_value_in_text(text, r"Net\s*Cash\s*Flow\s*\(Financing\)\s*:\s*(\d[\d,\.]*)")
    return {
        "operating_cash_flow": operating,
        "investing_cash_flow": investing,
        "financing_cash_flow": financing
    }

def parse_invoice_data(text):
    invoice_number = find_match_in_text(text, r"Invoice\s*Number\s*:\s*([A-Z0-9\-]+)")
    total_amount = find_value_in_text(text, r"Total\s*Amount\s*:\s*(\d[\d,\.]*)")
    tax_amount = find_value_in_text(text, r"Tax\s*Amount\s*:\s*(\d[\d,\.]*)")
    return {
        "invoice_number": invoice_number,
        "total_amount": total_amount,
        "tax_amount": tax_amount
    }

def analyze_unstructured_text(text):
    words = text.split()
    wc = len(words)
    numeric_values = find_all_values(text)
    top_terms = find_top_terms(words)
    return {
        "word_count": wc,
        "numeric_values": numeric_values[:10],
        "top_terms": top_terms
    }

def find_value_in_text(text, pattern):
    import re
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        raw = match.group(1)
        val = raw.replace(",", "")
        try:
            return float(val)
        except:
            return val
    return 0

def find_match_in_text(text, pattern):
    import re
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "N/A"

def find_all_values(text):
    import re
    pat = r"\b\d[\d,\.]*\b"
    matches = re.findall(pat, text)
    cleaned = []
    for m in matches:
        c = m.replace(",", "")
        try:
            v = float(c)
            cleaned.append(v)
        except:
            pass
    return cleaned

def find_top_terms(words):
    from collections import Counter
    freq = Counter([w.lower() for w in words if len(w) > 3])
    return freq.most_common(5)

def advanced_doc_clustering(docs):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.cluster import KMeans
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(docs)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans.fit(X)
    return kmeans.labels_

def advanced_pdf_splitter(pdf_file):
    import PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    total_pages = len(pdf_reader.pages)
    half = total_pages // 2
    parts = []
    for i in range(2):
        writer = PyPDF2.PdfWriter()
        start = i * half
        end = (i + 1) * half if i < 1 else total_pages
        for page_num in range(start, end):
            writer.add_page(pdf_reader.pages[page_num])
        buffer = open(f"processed_data/part_{i}.pdf", "wb")
        writer.write(buffer)
        buffer.close()
        parts.append(f"processed_data/part_{i}.pdf")
    return parts

def advanced_image_enhancement(image):
    arr = np.array(image.convert("L"))
    mean_val = np.mean(arr)
    thr = (mean_val + arr.min()) / 2
    bin_img = (arr > thr).astype(np.uint8) * 255
    return Image.fromarray(bin_img)

def advanced_doc_parser(text):
    lines = text.split("\n")
    data = []
    for ln in lines:
        if ":" in ln:
            sp = ln.split(":")
            if len(sp) == 2:
                k = sp[0].strip()
                v = sp[1].strip()
                data.append((k, v))
    return dict(data)

def run_advanced_doc_features():
    st.title("Advanced Document Features")
    file_obj = st.file_uploader("Upload Document", type=["pdf", "png", "jpg", "jpeg"])
    if file_obj:
        text = extract_text_advanced(file_obj)
        st.text_area("Extracted Text", text, height=200)
        doc_dict = advanced_doc_parser(text)
        st.json(doc_dict)
        numeric_vals = find_all_values(text)
        st.write("Numeric Values Found:", numeric_vals)