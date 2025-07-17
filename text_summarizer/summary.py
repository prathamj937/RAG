import os
import hashlib
import redis
import fitz  # PyMuPDF
import docx
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# Load environment
load_dotenv()
# Redis Setup
redis_client = redis.Redis(host="localhost", port=6379, db=0)
# redis_client.flushdb()
# Chroma Vector DB Setup
CHROMA_DIR = "chroma_db"
os.makedirs(CHROMA_DIR, exist_ok=True)
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = Chroma(persist_directory=CHROMA_DIR, embedding_function=embedding)

# Gemini API Setup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Hash for Redis Keying
def hash_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def get_cached_summary(text: str):
    key = hash_text(text)
    result = redis_client.get(key)
    return result.decode() if result else None

def cache_summary(text: str, summary: str):
    key = hash_text(text)
    redis_client.set(key, summary)

# ✨ Gemini Summarization
def summarize_with_gemini(text: str):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(f"Summarize the following text:\n\n{text}")
        return response.text
    except Exception as e:
        print("❌ Failed to summarize with Gemini:", e)
        return "⚠️ Gemini failed to generate summary."

# Split Text into Chunks
def split_text(text: str):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_text(text)

# Store Embeddings
def embed_and_store(chunks):
    ids = [hash_text(chunk) for chunk in chunks]
    vector_db.add_texts(texts=chunks, ids=ids)

# File Parser
def extract_text_from_file(file_path: str):
    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            return "\n".join(page.get_text() for page in doc)
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    elif file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    else:
        raise ValueError("Unsupported file format")

# Full Summarization Pipeline
def summarize_text(text: str):
    cached = get_cached_summary(text)
    if cached:
        print("📦 Using cached summary.")
        return cached

    print("🔍 Splitting text into chunks...")
    chunks = split_text(text)
    embed_and_store(chunks)

    print(f"📑 Summarizing {len(chunks)} chunks...")
    chunk_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"➡️ Summarizing chunk {i + 1}/{len(chunks)}...")
        summary = summarize_with_gemini(chunk)
        print(f"✅ Chunk {i + 1} summary: {summary[:100]}...\n")
        chunk_summaries.append(summary)

    final_input = " ".join(chunk_summaries)
    final_summary = summarize_with_gemini(final_input)
    cache_summary(text, final_summary)

    print("✅ Final summary ready and cached.")
    return final_summary

# # Optional: Test
# if __name__ == "__main__":
#     sample = """In Q2 2025, the global technology consulting market witnessed moderate growth amid economic uncertainties and shifting digital priorities. Enterprises continued investing in AI and automation, though many slowed spending on large-scale transformation projects. EY’s consulting practice adapted by emphasizing value-driven advisory services and scalable digital strategies tailored to sector-specific needs.

# The Financial Services sector showed the strongest resilience, driven by regulatory changes and increased focus on cybersecurity. Meanwhile, the Consumer Products and Retail segments experienced a decline in consulting demand due to reduced consumer spending and supply chain disruptions.

# Talent retention remained a key challenge, with attrition rates stabilizing but not declining significantly. EY’s “Future-Ready Workforce” program—launched earlier this year—has started showing positive results in upskilling employees in data analytics, cloud services, and agile delivery models. The initiative has been especially impactful in the Asia-Pacific region.

# Operationally, the consulting division introduced an AI-powered delivery excellence framework. This framework leverages internal data, client KPIs, and project outcomes to provide real-time quality insights and improve delivery consistency. Internal adoption of the tool has reached 62%, with a target of 85% by Q4.

# From a financial perspective, revenue grew 4.7% YoY, with the EMEA region showing the highest increase (7.9%), driven by strong demand in digital risk and regulatory compliance. However, North America saw a marginal decline (–1.1%) due to client budget tightening in the TMT (Technology, Media, Telecom) sector.

# In terms of sustainability consulting, EY expanded its Net Zero advisory services. Collaborations with three major energy providers are underway to build transparent ESG dashboards using satellite data and AI modeling. The aim is to provide predictive insights into emissions and compliance trajectories.

# Looking ahead to Q3 and Q4, the firm plans to further integrate GenAI into client delivery, focusing on document intelligence and code review automation. This shift is expected to streamline 12–15% of manual tasks in large transformation programs.

# Overall, the consulting practice remains focused on agility, sector relevance, and AI-powered value delivery."""
#     summary = summarize_text(sample)
#     print("\n🧠 Final Summary:\n", summary)
