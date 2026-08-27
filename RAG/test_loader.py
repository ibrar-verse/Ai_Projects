from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Load the PDF document
loader = PyPDFLoader("sample.pdf")
docs = loader.load()

# 2. Configure the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# 3. Split the document pages into smaller text chunks
chunks = text_splitter.split_documents(docs)

# 4. Inspect results
print(f"Total Pages Loaded: {len(docs)}")
print(f"Total Chunks Created: {len(chunks)}")
print("\n--- First Chunk Preview ---")
print(chunks[0].page_content)
print(chunks)
