import os
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI

from agent import news_scanner_tool, supply_chain_retriever_tool
from src.config import LLM_MODEL_NAME
# Load environment variables
load_dotenv()




llm = ChatOpenAI(
    model=LLM_MODEL_NAME,
    temperature=0,
    openai_api_base=os.getenv("OPENROUTER_API_BASE"),
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
)

print(f"LLM Initialized with model: {LLM_MODEL_NAME}")

tools = [news_scanner_tool, supply_chain_retriever_tool]

# --- 3. Get the Agent's Prompt Template ---
prompt = hub.pull("hwchase17/react")

# --- 4. Create the Agent ---
agent = create_react_agent(llm, tools, prompt)

# --- 5. Create the Agent Executor ---
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

# --- 6. Define the Master Task and Run the Agent ---
if __name__ == '__main__':
    master_task = """
    Your mission is to act as a Supply Chain Risk Analyst.
    First, use the news_scanner_tool with a query like "Taiwan semiconductor"
    to find potential disruption events.

    For each relevant news headline, identify the key location or company. Then, use the
    supply_chain_retriever_tool with that key entity to check if it affects our
    internal supply chain.

    Finally, provide a consolidated final answer summarizing any identified risks.
    If no risks are found, state that clearly.

    """
    
    print("\n--- Running Supply Chain Agent ---")
    agent_executor.invoke({
        "input": master_task
    })