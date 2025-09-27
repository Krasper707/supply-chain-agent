import pandas as pd
import chromadb
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from src.config import DATA_PATH, DB_PATH, EMBEDDING_MODEL
# Define the paths to your data and the persistent database directory
def create_vector_db():
    """
    Creates and persists a vector database from the company's supply chain data.
    This new version enriches each document with critical metadata.
    """
    # 1. LOAD AND PREPROCESS THE DATA
    print("Step 1: Loading and preprocessing data...")
    
    suppliers_df = pd.read_csv(DATA_PATH + "suppliers.csv")
    materials_df = pd.read_csv(DATA_PATH + "materials.csv")

    merged_df = pd.merge(
        materials_df,
        suppliers_df,
        how="left",
        left_on="supplied_by_id",
        right_on="supplier_id"
    )
    print("Successfully loaded and merged CSV data.")


    # 2. CREATE LANGCHAIN DOCUMENTS WITH METADATA
    print("\nStep 2: Creating LangChain documents with metadata...")
    
    documents = []
    for index, row in merged_df.iterrows():
        page_content = f"Material '{row['material_name']}' (ID: {row['material_id']}) is a " \
                       f"{row['criticality_level']} criticality component. It is supplied by " \
                       f"'{row['supplier_name']}' (ID: {row['supplier_id']}) from {row['city']}, " \
                       f"{row['country']}, which is in the {row['industry_type']} industry."
        
        metadata = {
            "source": f"materials.csv:{row['material_id']}",
            "supplier_name": row['supplier_name'],
            "material_name": row['material_name'],
            "criticality_level": row['criticality_level']
        }
        
        documents.append(Document(page_content=page_content, metadata=metadata))

    print(f"Successfully created {len(documents)} documents with rich metadata.")
    
    # 3. SPLIT DOCUMENTS INTO CHUNKS
    print("\nStep 3: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Split documents into {len(texts)} chunks.")

    # 4. CREATE EMBEDDINGS
    print("\nStep 4: Creating embeddings...")
    embeddings = SentenceTransformerEmbeddings(model_name=EMBEDDING_MODEL)
    print("Embeddings model loaded.")

    # 5. CREATE AND PERSIST THE VECTOR DATABASE
    print("\nStep 5: Creating and persisting the vector database...")
    vectordb = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    vectordb.persist()
    print(f"\nVector database created and persisted at: {DB_PATH}")

if __name__ == "__main__":
    create_vector_db()
