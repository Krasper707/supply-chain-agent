import pandas as pd
import chromadb
from langchain_community.document_loaders import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Define the paths to your data and the persistent database directory
DATA_PATH = "data/"
DB_PATH = "db/"

def create_vector_db():
    """
    Creates and persists a vector database from the company's supply chain data.
    """
    print("Step 1: Loading and preprocessing data...")
    
    # Load the CSV files into pandas DataFrames
    suppliers_df = pd.read_csv(DATA_PATH + "suppliers.csv")
    materials_df = pd.read_csv(DATA_PATH + "materials.csv")

    # Merge the dataframes to create rich, contextual information for each material
    # This combines supplier info with the materials they supply.
    merged_df = pd.merge(
        materials_df,
        suppliers_df,
        how="left",
        left_on="supplied_by_id",
        right_on="supplier_id"
    )

    # Create a descriptive text column that the LLM can understand.
    # This is a key step in making the data useful for retrieval.
    merged_df['combined_text'] = merged_df.apply(
        lambda row: f"Material '{row['material_name']}' (ID: {row['material_id']}) is a "
                    f"{row['criticality_level']} criticality component. It is supplied by "
                    f"'{row['supplier_name']}' (ID: {row['supplier_id']}) from {row['city']}, "
                    f"{row['country']}, which is in the {row['industry_type']} industry.",
        axis=1
    )

    # Use LangChain's DataFrameLoader to prepare the documents
    loader = DataFrameLoader(merged_df, page_content_column="combined_text")
    documents = loader.load()
    
    print(f"Successfully loaded and combined data into {len(documents)} documents.")
    
    # 2. SPLIT DOCUMENTS INTO CHUNKS
    print("\nStep 2: Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Split documents into {len(texts)} chunks.")

    # 3. CREATE EMBEDDINGS
    print("\nStep 3: Creating embeddings...")
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    print("Embeddings model loaded.")

    # 4. CREATE AND PERSIST THE VECTOR DATABASE
    print("\nStep 4: Creating and persisting the vector database...")
    # It uses the embeddings to convert text chunks into vectors and stores them.
    vectordb = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_PATH
    )
    
    vectordb.persist() #Saves the database in disk.
    print(f"Vector database created and persisted at: {DB_PATH}")

if __name__ == "__main__":
    create_vector_db()