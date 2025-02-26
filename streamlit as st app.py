import streamlit as st
import pdfplumber
import pandas as pd
from io import BytesIO

def extract_tables_from_pdf(pdf_file):
    tables = []
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_tables = page.extract_tables()
            for table in extracted_tables:
                tables.append(pd.DataFrame(table))
    
    if not tables:
        return None

    # Combine all tables into one Excel file (multiple sheets)
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        for idx, df in enumerate(tables):
            df.to_excel(writer, sheet_name=f"Table_{idx+1}", index=False, header=False)
    
    excel_buffer.seek(0)
    return excel_buffer

# Streamlit UI
st.title("PDF to Excel Converter 📄➡️📊")
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file:
    excel_data = extract_tables_from_pdf(uploaded_file)
    if excel_data:
        st.download_button(label="📥 Download Excel File",
                           data=excel_data,
                           file_name="extracted_tables.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.error("No tables found in the PDF.")
