import streamlit as st
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain_community.utilities import SQLDatabase  # Changed from langchain.sql_database
from langchain.agents.agent_types import AgentType    # Changed from langchain_agents
from langchain.callbacks import StreamlitCallbackHandler
import sqlite3
from langchain_groq import ChatGroq
from sqlalchemy import create_engine
from langchain.agents.agent_toolkits import SQLDatabaseToolkit  

st.set_page_config(page_title="SQL Agent with Streamlit")
st.title("Langchain: Chat with SQL DB")

LOCALDB="USE_LOCALDB"
MYSQL="USE_MYSQL"

radio_opt=["Use SQLLite 3 Database- Student.db","Connect to you MySQL Database"]

selected_opt=st.sidebar.radio(label="Choose the DB which you want to chat",options=radio_opt)


if radio_opt.index(selected_opt)==1:
    db_uri=MYSQL
    mysql_host=st.sidebar.text_input("Provide MySQL Host")
    mysql_user=st.sidebar.text_input("MYSQL User")
    mysql_password=st.sidebar.text_input("MYSQL password",type="password")
    mysql_db=st.sidebar.text_input("MySQL database")
else:
    db_uri=LOCALDB

api_key=st.sidebar.text_input(label="GRoq API Key",type="password")

if not db_uri:
    st.info("Please enter the database information and uri")

if not api_key:
    st.info("Please add the groq api key")

## LLM model
llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)

@st.cache_resource(ttl="2h")
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_password=None,mysql_db=None):
    if db_uri==LOCALDB:
        dbfilepath=(Path(__file__).parent/"chatbot.db").absolute()
        print(dbfilepath)
        creator = lambda: sqlite3.connect(f"file:{dbfilepath}?mode=ro", uri=True)
        return SQLDatabase(create_engine("sqlite:///", creator=creator))
    elif db_uri==MYSQL:
        if not (mysql_host and mysql_user and mysql_password and mysql_db):
            st.error("Please provide all MySQL connection details.")
            st.stop()
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_db}"))   
    
if db_uri==MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_password,mysql_db)
else:
    db=configure_db(db_uri)

toolkit = SQLDatabaseToolkit(db=db, llm=llm) # Create a toolkit for the SQL database

agent = create_sql_agent(
    toolkit=toolkit,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, # Use zero-shot reasoning it is used for tasks where the agent has no prior knowledge
    verbose=True
)

if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot who can answer questions about the database. How can I help you?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

user_query = st.chat_input(placeholder="Ask anything from the database")
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    st.chat_message("user").write(user_query)

    with st.chat_message("assistant"):
        st_cb = StreamlitCallbackHandler(st.container()) # creates a callback handler for Streamlit
        response = agent.run(st.session_state.messages, callbacks=[st_cb]) # runs the agent with the chat history
        st.session_state.messages.append({'role': 'assistant', "content": response}) # saves in chat history
        st.write(response)