import streamlit as st
import io
import pdf2image
import pytesseract
import numpy as np
import logging
from PIL import Image
from googletrans import Translator
import langdetect
logger=logging.getLogger(__name__)
def run_multi_lang_ocr():
    st.title("Multi-Language OCR")
    st.write("Extract and translate text from images, PDFs, or docx")
    file_obj=st.file_uploader("Upload File",type=["pdf","jpg","jpeg","png","docx"])
    if file_obj:
        text,lang=perform_multi_lang_ocr(file_obj)
        st.text_area("Extracted Text",text,height=200)
        st.write(f"Detected Language: {lang}")
        translator=Translator()
        if text and lang!="unknown":
            translated=translator.translate(text,dest="en")
            st.text_area("Translated Text",translated.text,height=200)
def perform_multi_lang_ocr(file_obj):
    ft=file_obj.type
    raw=""
    try:
        if "image" in ft:
            im=Image.open(file_obj)
            raw=pytesseract.image_to_string(im,lang='eng+hin+tam+kan+tel')
        elif ft=="application/pdf":
            pages=pdf2image.convert_from_bytes(file_obj.read())
            result=[]
            for p in pages:
                txt=pytesseract.image_to_string(p,lang='eng+hin+tam+kan+tel')
                result.append(txt)
            raw="\n".join(result)
        elif ft=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            import docx
            doc=docx.Document(file_obj)
            lines=[]
            for para in doc.paragraphs:
                lines.append(para.text)
            raw="\n".join(lines)
        else:
            raw="Unsupported format"
    except Exception as e:
        raw="Error in OCR"
    detected="unknown"
    if raw and raw not in ["Unsupported format","Error in OCR"]:
        try:
            detected=langdetect.detect(raw)
        except:
            detected="unknown"
    return raw,detected
def multi_lang_preprocessing(text):
    lines=text.split("\n")
    cleaned=[]
    for line in lines:
        if line.strip():
            cleaned.append(line.strip())
    return " ".join(cleaned)
def advanced_language_segmentation(text):
    from googletrans import Translator
    translator=Translator()
    segments=text.split(".")
    results=[]
    for seg in segments:
        seg=seg.strip()
        if seg:
            detected=langdetect.detect(seg)
            trans=translator.translate(seg,dest="en")
            results.append({"original":seg,"lang":detected,"translated":trans.text})
    return results
def run_multi_lang_advanced():
    st.title("Multi-Language Advanced OCR")
    file_obj=st.file_uploader("Upload File",type=["pdf","jpg","jpeg","png","docx"])
    if file_obj:
        text,lang=perform_multi_lang_ocr(file_obj)
        st.write(f"Detected Language: {lang}")
        if text not in ["Unsupported format","Error in OCR"]:
            segs=advanced_language_segmentation(text)
            for i,s in enumerate(segs):
                st.write(f"Segment {i+1}: {s['original']}")
                st.write(f"Detected: {s['lang']} -> {s['translated']}")