import os
from dotenv import load_dotenv
from langchain.agents import tool
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_openai import ChatOpenAI
from src.config import DB_PATH, EMBEDDING_MODEL
from src.data_ingestion import fetch_disruption_news

load_dotenv()

# --- Define Tools ---

@tool
def news_scanner_tool(query: str) -> str:
    """
    Scans for recent news articles related to a general query about supply chain disruptions.
    Use this as your first step to get a lay of the land. The input query should be a
    simple search term like 'factory fire' or 'port congestion'.
    Returns a formatted string of article titles and URLs.
    """
    print(f"--- AGENT ACTION: Calling News Scanner Tool with query: '{query}' ---")
    # We will re-use our function from Week 1
    articles = fetch_disruption_news(query) 
    if articles:
        # Format the output to be clean and simple for the agent
        return "\n".join([f"Title: {a['title']}, URL: {a['url']}" for a in articles])
    return "No relevant news articles found."

@tool
def supply_chain_retriever_tool(query: str) -> str:
    """
    Queries the company's internal supply chain vector database. Use this tool to check
    if a specific location (city, country), company name, or material mentioned in a news
    article is relevant to our supply chain. The input should be the specific entity
    to search for.
    """
    print(f"--- AGENT ACTION: Calling Supply Chain Retriever with query: '{query}' ---")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    results = vectordb.similarity_search(query, k=3) # Get top 3 results
    
    if results:
        # Format the results into a single string for the LLM
        return "\n\n".join([doc.page_content for doc in results])
    return "No relevant information found in the supply chain database."