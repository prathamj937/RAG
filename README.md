# RAG

1. llm_lcel_app: Built using React frontend, RAG architecture, ChromaDB, Gemini/Groq keys, Redis for caching.

2. text_summarizer: Built using Chainlit UI, supports .pdf, .txt, .docx, uses recursive text splitting.

🧠 RAG-Based Multi-Tool AI Platform
This repository contains two core applications:

llm_lcel_app: A React + FastAPI-based RAG (Retrieval-Augmented Generation) app using Gemini/Groq and ChromaDB.

text_summarizer: A document summarization tool with Chainlit UI, supporting PDF, DOCX, and TXT input.

📁 Project Structure
bash
Copy
Edit
.
├── llm_lcel_app/
│   ├── backend/        # FastAPI + Redis + ChromaDB + LLM
│   └── frontend/       # React-based user interface
│
├── text_summarizer/
│   ├── main.py         # Chainlit interface
│   ├── summary.py      # Summarization logic
│   └── utils/          # Text splitting & file extraction
│
├── README.md
└── requirements.txt
🚀 Features
📚 1. LLM_LCEL_APP (React + FastAPI)
🔍 RAG pipeline with:

ChromaDB for vector storage

Gemini Pro or Groq LLM for responses

Redis for fast caching of embeddings and API responses

⚛️ Frontend: React-based UI with clean interaction flow

⚡ Backend:

FastAPI for scalable APIs

RecursiveTextSplitter for robust document chunking

📝 2. Text Summarizer (Chainlit)
🧾 Upload .pdf, .docx, or .txt

🧠 Uses recursive text splitting

🦜 LLM-backed summarization via Gemini or Groq

🖼️ UI powered by Chainlit – chat-like experience

🛠️ Tech Stack
Category	Stack/Tool
LLMs	Gemini Pro / Groq
Embedding Store	ChromaDB
Cache Layer	Redis
Text Splitting	RecursiveTextSplitter
Frontend	React (for LCEL App)
Summarizer UI	Chainlit
Backend	FastAPI

🔧 Setup Instructions
🧠 llm_lcel_app

cd llm_lcel_app/backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set your keys in .env
GROQ_API_KEY=...
GEMINI_API_KEY=...

uvicorn main:app --reload
React Frontend

cd llm_lcel_app/frontend
npm install
npm run dev
📝 text_summarizer

cd text_summarizer
pip install -r requirements.txt

# Environment variables
GEMINI_API_KEY=...
GROQ_API_KEY=...

chainlit run main.py -w
