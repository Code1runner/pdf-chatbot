import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def main():
    load_dotenv()
    st.set_page_config(page_title="Analyze and ask about multiple PDFs", page_icon=":books:")

    st.header("Analyze multiple PDFs :books:")
    st.text_input("Ask a question about your documents:")

    with st.sidebar:
        st.subheader("Your PDFs")
        pdf_docs = st.file_uploader(
            "Upload your file", accept_multiple_files=True)
        if st.button("Upload"):
            with st.spinner("Uploading"):
                raw_text = get_pdf_text(pdf_docs)
                st.write(raw_text)

if __name__ == '__main__':
    main()