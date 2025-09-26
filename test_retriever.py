from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

DB_PATH = "db/"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def test_query(query: str):
    """
    Loads the persisted vector database and performs a similarity search.
    """
    print(f"\n--- Testing query: '{query}' ---")
    
    # Load the embedding function
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    
    # Load the  database
    vectordb = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
    
    #Perform a similarity search
    results = vectordb.similarity_search(query, k=2) 
    
    if results:
        print("Found relevant documents:")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(doc.page_content)
    else:
        print("No relevant documents found.")

if __name__ == "__main__":
    test_query("What materials are supplied from Taiwan?")
    test_query("Do we have any high criticality microchips?")