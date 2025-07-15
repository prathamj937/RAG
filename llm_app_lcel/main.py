from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load Groq API key
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
assert groq_api_key, "Missing GROQ_API_KEY in .env"

# FastAPI app
app = FastAPI(title="LCEL Groq Translator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class ChainInput(BaseModel):
    language: str
    text: str

# Define LCEL components
prompt = ChatPromptTemplate.from_messages([
    ("system", "Translate English to {language}."),
    ("user", "{text}")
])

model = ChatGroq(model="gemma2-9b-it", groq_api_key=groq_api_key)
parser = StrOutputParser()

# LCEL input mapper (RunnableLambda)
def map_input(input: dict):
    return {"language": input["language"], "text": input["text"]}

input_mapper = RunnableLambda(map_input)

# LCEL chain
chain = input_mapper | prompt | model | parser

# POST endpoint using LCEL
@app.post("/translate")
async def translate(input_data: ChainInput):
    try:
        result = await chain.ainvoke(input_data.dict())
        return {"translation": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))  # Render injects PORT env var
    uvicorn.run("main:app", host="0.0.0.0", port=port)
