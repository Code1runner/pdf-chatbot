import huggingface_hub
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS 
from langchain.embeddings import HuggingFaceInstructEmbeddings

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 1000,
        chunk_overlap = 200,
        length_function = len 
    )
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    embeddings = HuggingFaceInstructEmbeddings(model_name = "hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(text_chunks, embeddings)
    return vectorstore

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
                
                text_chunks = get_text_chunks(raw_text)

                vectorstore = get_vectorstore(text_chunks)

                #st.write(text_chunks)
if __name__ == '__main__':
    main()