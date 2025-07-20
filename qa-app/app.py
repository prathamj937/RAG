import os
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

# ✅ Fix incorrect use of os.getenv
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")  # NOT os.getenv[]
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "QA CHATBOT"

## PROMPT
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to the user queries."),
        ("human", "Question: {question}")
    ]
)

def generate_response(question, api_key, model="gemma-7b-it", temperature=0.7):
    try:
        llm = ChatGroq(groq_api_key=api_key, model=model, temperature=temperature)
        output_parser = StrOutputParser()
        chain = prompt | llm | output_parser

        # ✅ Tracing via LangSmith
        config = RunnableConfig(
            config={
                "run_name": "QA Chain",
                "tags": ["qa", "groq"],
                "metadata": {"model": model}
            }
        )

        answer = chain.invoke({'question': question}, config=config)
        return answer
    except Exception as e:
        return f"Error: {str(e)}"   

# Streamlit UI
st.title("QA Chatbot")

st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your key:", type="password")

model = st.sidebar.selectbox(
    "Select Groq model",
    ["Llama3-8b-8192", "mixtral-8x7b-32768", "llama2-70b-4096"]
)

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7)

st.write("Go ahead and ask any question")
user_input = st.text_input("You:")

if user_input and api_key:
    response = generate_response(user_input, api_key, model, temperature)
    st.write("Assistant:", response)
elif user_input:
    st.warning("Please enter the Groq API Key in the sidebar")
else:
    st.write("Please provide your question")
