import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Streamlit UI config
st.set_page_config(page_title="LangChain: Summarize YT or Website", page_icon="🦜")
st.title("🦜 LangChain: Summarize YT or Website")
st.subheader("Summarize content from YouTube or any URL")

# Sidebar: API key input
with st.sidebar:
    groq_api_key = st.text_input("🔑 Groq API Key", value="", type="password")

# Main input: URL
generic_url = st.text_input("Paste YouTube or Website URL", label_visibility="collapsed")

# Load LLM (Groq)
llm = ChatGroq(model="gemma-9b-it", groq_api_key=groq_api_key)

map_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Summarize the following part of the content clearly and concisely:
{text}
"""
)

combine_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Using the following partial summaries, write a single, complete summary in under 300 words:
{text}
"""
)

# Handle Button Click
if st.button("Summarize the Content"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide both a valid URL and Groq API key.")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL (YouTube or webpage).")
    else:
        try:
            with st.spinner("Loading and processing content..."):
                # Load content
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                docs = loader.load()

                if not docs:
                    st.warning("No content could be loaded from the given URL.")
                else:
                    # Split large content into manageable chunks
                    splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=200
                    )
                    split_docs = splitter.split_documents(docs)

                    # Run summarization with map-reduce chain
                    chain = load_summarize_chain(
                        llm=llm,
                        chain_type="map_reduce",
                        map_prompt=map_prompt,
                        combine_prompt=combine_prompt
                    )
                    summary = chain.run(split_docs)

                    st.success("✅ Summary generated:")
                    st.write(summary)

        except Exception as e:
            st.exception(f"Exception: {e}")

