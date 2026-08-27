import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# 1. Load API Keys from .env
load_dotenv()

# 2. Ingest & Chunk the PDF
loader = PyPDFLoader("sample.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(docs)

# 3. Cloud Embeddings (0 MB Local Model Download)
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")
vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)

# 4. Perform Similarity Search
query = "What is the Transformer architecture based on?"
matched_docs = vector_db.similarity_search(query, k=2)

# 5. Print the Retrieved Context Chunks
print("\n--- Retrieved Context from PDF ---")
for i, doc in enumerate(matched_docs, 1):
    print(f"\n[Match {i}] (Page {doc.metadata.get('page', 'Unknown')}):")
    print(doc.page_content)