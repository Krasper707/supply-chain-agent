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
    Queries the company's internal supply chain vector database to find information
    about suppliers, materials, and locations. Crucially, this tool now returns
    both the retrieved information AND its 'Criticality Level'.
    """
    print(f"--- AGENT ACTION: Calling Upgraded Supply Chain Retriever with query: '{query}' ---")
    
    # Load the embedding function and the vector database from disk
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    vectordb = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    # Perform a similarity search. We ask for the single best match (k=1) for clarity.
    results = vectordb.similarity_search(query, k=1)
    
    if results:
        # Get the first and best document match
        doc = results[0]
        page_content = doc.page_content
        
        # --- THIS IS THE KEY UPGRADE ---
        # We access the document's metadata and get the criticality level.
        # .get() is a safe way to do this; it returns 'Unknown' if the key doesn't exist.
        criticality = doc.metadata.get('criticality_level', 'Unknown')
        
        # We return a structured string that the agent's LLM can easily understand.
        return f"Found Match: {page_content}\nCriticality Level: {criticality}"
        
    return "No relevant information found in the supply chain database."

if __name__ == '__main__':
    print("--- Testing the upgraded retriever tool ---")
    # We will simulate a query the agent might make
    test_query = "What suppliers do we have in Taiwan?"
    tool_output = supply_chain_retriever_tool.invoke(test_query)
    
    print(f"\nQuery: '{test_query}'")
    print("Tool Output:")
    print(tool_output)
    print("\n--- Test complete ---")
