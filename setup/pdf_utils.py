import os
from pymongo import MongoClient
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch

def process_pdf_from_file(pdf_file):
    loader = PyPDFLoader(pdf_file)  # Initialize the PDF loader with the file path
    data = loader.load()  # Load the PDF document's data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)  # Initialize the text splitter
    docs = text_splitter.split_documents(data)  # Split the document into manageable segments
    return docs

def process_pdfs_in_directory(directory):
    all_docs = []
    pdf_files = [filename for filename in os.listdir(directory) if filename.endswith(".pdf")]
    total_files = len(pdf_files)
    print(f"Found {total_files} PDF files in directory '{directory}'")
    for i, filename in enumerate(pdf_files, start=1):
        pdf_file = os.path.join(directory, filename)
        print(f"Processing PDF file {i} of {total_files}: {pdf_file}")
        docs = process_pdf_from_file(pdf_file)
        all_docs.extend(docs)
    print(f"All PDF files processed in directory '{directory}'. {len(all_docs)} docs have been created.")

    return all_docs