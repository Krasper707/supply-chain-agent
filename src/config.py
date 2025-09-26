
"""
Centralized configuration file for the Supply Chain Agent.
"""

#Data Paths
DATA_PATH = "data/"
DB_PATH = "db/"

#Embedding Model 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# LLM Configuration (via OpenRouter) 
# Other good options: "mistralai/mistral-7b-instruct:free", "huggingfaceh4/zephyr-7b-beta:free"
LLM_MODEL_NAME = "mistralai/mistral-7b-instruct:free"