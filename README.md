# 🚀 AI Developer Projects Hub

A comprehensive collection of end-to-end Artificial Intelligence applications, featuring **Retrieval-Augmented Generation (RAG)**, **Multimodal Voice Assistants**, **Semantic Vector Search**, and **Computer Vision Pipelines**.

---

## 📂 Projects Overview

| Directory | Project | Key Technologies | Description |
| :--- | :--- | :--- | :--- |
| **`RAG/`** | **Document RAG Assistant** | LangChain, ChromaDB, Gemini 3.6 Flash, Google Embeddings | Full-stack conversational RAG application allowing users to upload PDFs, chunk & embed contents, and query the document via vector similarity search. |
| **`Voice_Assistant/`** | **AI Voice Assistant** | Gemini Multimodal API, gTTS, Web Speech API, Flask | Interactive voice-to-voice personal assistant that transcribes spoken audio, reasons with LLMs, and responds with synthetic speech. |
| **`image_captioning/`** | **Vision Caption Generator** | Google GenAI Vision, Python, Pillow | Multimodal pipeline that analyzes image semantics, generates descriptive captions, and extracts key contextual metadata. |
| **`CHATBOTS/`** | **Conversational Agents** | LangChain Core, Prompt Engineering, Memory Systems | Specialized dialogue agents featuring context window memory, system persona controls, and prompt chaining. |
| **`chatapp-with-voice-and-openai/`** | **Hybrid Voice Chat** | OpenAI / Gemini API, gTTS, Flask-CORS | Full-stack web chat interface supporting both textual and real-time audio input/output streaming. |

---

## 🛠️ Tech Stack & Frameworks

* **Languages:** Python 3.11+, JavaScript (ES6+), HTML5/CSS3
* **AI & LLM Orchestration:** LangChain, Google GenAI SDK (`gemini-3.6-flash`), OpenAI API
* **Vector Databases & Embeddings:** ChromaDB, `gemini-embedding-2-preview`, Hugging Face `sentence-transformers`
* **Speech & Vision:** Google Text-to-Speech (`gTTS`), Web Audio API, Gemini Vision Multimodal
* **Backend & Web:** Flask, Flask-CORS, RESTful APIs

---

## ⚡ Getting Started

### 1. Clone the Repository
```bash
git clone [https://github.com/](https://github.com/)<YOUR-USERNAME>/Ai_developer_projects.git
cd Ai_developer_projects
2. Set Up Virtual Environment
Bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory (or respective project folders):

Code snippet
GEMINI_API_KEY=your_google_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
🚀 Running a Project Example (RAG Assistant)
Bash
cd RAG
python server.py
Open your browser and navigate to http://127.0.0.1:8000 to upload documents and begin asking questions.

🔒 Security & Best Practices
Sensitive credentials and API keys are managed through .env files and excluded from version control via .gitignore.

Document embeddings use chunking heuristics (chunk_size=2500, chunk_overlap=200) to maximize retrieval precision while adhering to strict cloud rate limits.

👤 Author
Developer: Abrar Ahmad

GitHub: @ibrar-verse