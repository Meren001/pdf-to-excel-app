import streamlit as st
import pdfplumber
import pandas as pd

st.title("PDF to Excel Converter")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    with pdfplumber.open(uploaded_file) as pdf:
        table_data = []
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                table_data.extend(tables)
    
    df = pd.DataFrame(table_data)
    
    if not df.empty:
        excel_file = "output.xlsx"
        df.to_excel(excel_file, index=False)
        st.success("Conversion successful!")
        st.download_button("Download Excel file", open(excel_file, "rb"), file_name="converted.xlsx")
    else:
        st.warning("No tables found in PDF.")