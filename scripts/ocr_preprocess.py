import streamlit as st
import pdf2image
import pytesseract
import io
import numpy as np
import pandas as pd
import logging
import os
import re
from PIL import Image
logger=logging.getLogger(__name__)
def run_ocr_extraction():
    st.title("OCR Extraction")
    st.write("Extract text from images or PDFs")
    choice=st.selectbox("Select Input Type",["Image","PDF"])
    uploaded_file=st.file_uploader("Upload File",type=["jpg","jpeg","png","pdf"])
    if uploaded_file:
        if choice=="Image":
            try:
                image=Image.open(uploaded_file)
                text=pytesseract.image_to_string(image)
                st.text_area("Extracted Text",text,height=300)
            except Exception as e:
                st.error("Error extracting text from image")
        else:
            try:
                images=pdf2image.convert_from_bytes(uploaded_file.read())
                extracted=[]
                for im in images:
                    t=pytesseract.image_to_string(im)
                    extracted.append(t)
                final="\n".join(extracted)
                st.text_area("Extracted Text",final,height=300)
            except Exception as e:
                st.error("Error extracting text from PDF")
def advanced_preprocess_image(image):
    arr=np.array(image.convert("L"))
    mean_val=np.mean(arr)
    thresh=(mean_val+arr.min())/2
    arr=(arr>thresh).astype(np.uint8)*255
    processed=Image.fromarray(arr)
    return processed
def advanced_extract_data(image):
    text=pytesseract.image_to_string(image)
    lines=text.split("\n")
    result=[]
    for line in lines:
        if line.strip():
            result.append(line.strip())
    return result
def advanced_pdf_to_images(pdf_bytes,dpi=300):
    pages=pdf2image.convert_from_bytes(pdf_bytes,dpi=dpi)
    return pages
def advanced_process_text(text):
    text=text.replace("\n"," ").strip()
    words=text.split(" ")
    words=[w for w in words if w]
    return words
def detect_language(text):
    import langdetect
    try:
        lang=langdetect.detect(text)
        return lang
    except:
        return "unknown"
def extract_tables_from_pdf(pdf_file):
    import pdfplumber
    data_frames=[]
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                tables=page.extract_tables()
                for tbl in tables:
                    df=pd.DataFrame(tbl[1:],columns=tbl[0])
                    data_frames.append(df)
    except:
        pass
    return data_frames
def parse_numeric_data(text):
    pattern=r"\b\d{1,3}(?:,\d{3})*\.\d{2}\b"
    matches=re.findall(pattern,text)
    cleaned=[float(x.replace(",","")) for x in matches]
    return cleaned
def remove_stopwords(text):
    from nltk.corpus import stopwords
    sw=set(stopwords.words("english"))
    tokens=text.split()
    filtered=[t for t in tokens if t.lower() not in sw]
    return " ".join(filtered)
def summarize_text(text):
    from gensim.summarization import summarize
    try:
        summary=summarize(text,ratio=0.2)
        return summary
    except:
        return text
def advanced_ocr_pipeline(file_obj):
    ext=os.path.splitext(file_obj.name)[1].lower()
    if ext in [".jpg",".jpeg",".png"]:
        image=Image.open(file_obj)
        processed=advanced_preprocess_image(image)
        lines=advanced_extract_data(processed)
        text=" ".join(lines)
        return text
    elif ext==".pdf":
        pages=advanced_pdf_to_images(file_obj.read())
        all_text=[]
        for p in pages:
            proc=advanced_preprocess_image(p)
            lines=advanced_extract_data(proc)
            joined=" ".join(lines)
            all_text.append(joined)
        return " ".join(all_text)
    else:
        return "Unsupported format"
def generate_advanced_insights(text):
    lang=detect_language(text)
    numeric=parse_numeric_data(text)
    short=remove_stopwords(text)
    summarized=summarize_text(short)
    return {"language":lang,"numeric_values":numeric,"summary":summarized}
def run_advanced_ocr():
    st.title("Advanced OCR Pipeline")
    uploaded=st.file_uploader("Upload File",type=["pdf","jpg","jpeg","png"])
    if uploaded:
        raw_text=advanced_ocr_pipeline(uploaded)
        st.text_area("Extracted Text",raw_text,height=200)
        if raw_text and raw_text!="Unsupported format":
            insights=generate_advanced_insights(raw_text)
            st.json(insights)