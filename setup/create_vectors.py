import os
from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from pdf_utils import process_pdfs_in_directory

# Retrieve environment variables for sensitive information
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("The OPENAI_API_KEY environment variable is not set.")

ATLAS_CONNECTION_STRING = os.getenv('ATLAS_CONNECTION_STRING')
if not ATLAS_CONNECTION_STRING:
    raise ValueError("The ATLAS_CONNECTION_STRING environment variable is not set.")

# Connect to MongoDB Atlas cluster using the connection string
cluster = MongoClient(ATLAS_CONNECTION_STRING)

def create_vectors(directory_name, db_name, collection_name):
    docs = process_pdfs_in_directory(directory_name)
    MONGODB_COLLECTION = cluster[db_name][collection_name]

    vector_search = MongoDBAtlasVectorSearch.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
        collection=MONGODB_COLLECTION,
        index_name="embeddings"  # Use a predefined index name
    )
# print(os.getcwd())
print("MONGO CONNECTION SUCCESFUL...")
print("Embedding PT Context...")
# create_vectors("data/pt_context", "langchain", "pt")
print("Embedding Nutrition Context...")
create_vectors("data/nutrition_context", "langchain", "nutrition")
print("Embedding Process Complete!")