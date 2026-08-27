import os
from dotenv import load_dotenv
from google import genai
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

# Global State
gemini_client = None
embeddings = None
retriever = None
chat_history = []

def init_llm():
    global gemini_client, embeddings
    load_dotenv()
    gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    # Google Cloud Embedding Model
    embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

def process_document(document_path):
    global retriever
    # 1. Load document
    loader = PyPDFLoader(document_path)
    docs = loader.load()

    # 2. Optimized chunking: larger chunks keep API request count well under rate limits
    splitter = RecursiveCharacterTextSplitter(chunk_size=2500, chunk_overlap=200)
    chunks = splitter.split_documents(docs)

    # 3. Create Chroma vector database & retriever
    vector_db = Chroma.from_documents(documents=chunks, embedding=embeddings)
    retriever = vector_db.as_retriever(search_kwargs={"k": 3})
    return f"Successfully processed {len(chunks)} chunks from {document_path}"

def process_prompt(prompt):
    global chat_history
    if retriever is None:
        return "Please upload and process a document first."

    # 1. Retrieve relevant chunks
    docs = retriever.invoke(prompt)
    context = "\n\n".join([doc.page_content for doc in docs])

    # 2. Build conversational history context
    history_context = "\n".join([f"User: {q}\nAI: {a}" for q, a in chat_history[-3:]])

    # 3. Prompt for Gemini
    full_prompt = f"""
You are a helpful and precise assistant answering questions about an uploaded document.
Answer the user's question based strictly on the provided context. If the answer is not in the context, say you cannot find it in the document.

<Document Context>
{context}
</Document Context>

<Chat History>
{history_context}
</Chat History>

User Question: {prompt}
Answer:"""

    response = gemini_client.models.generate_content(
        model="gemini-3.6-flash",
        contents=full_prompt
    )
    answer = response.text.strip()

    # 4. Save to memory
    chat_history.append((prompt, answer))
    return answer

# Initialize on startup
init_llm()

# --- Direct Test Block ---
if __name__ == "__main__":
    print(process_document("sample.pdf"))
    print("\nQ: What are the main benefits of the Transformer over RNNs?")
    print("A:", process_prompt("What are the main benefits of the Transformer over RNNs?"))