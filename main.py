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
    Your mission is to act as a world-class Supply Chain Risk Analyst.
    Your goal is to be a resilient and resourceful researcher.

    First, use the news_scanner_tool to find potential disruption events.
    **CRITICAL INSTRUCTION: If your initial search query returns no results, DO NOT give up. You MUST try again with a different, broader, or simpler query. Break the problem down. For example, if 'factory fire OR port congestion' fails, try searching for just 'factory fire', and then separately for 'port congestion'. Continue this process until you find relevant information.**

    For each relevant news headline you find, you must use the supply_chain_retriever_tool to check if the mentioned location or company affects our supply chain. The tool will return a 'Criticality Level' for any match it finds.

    Finally, provide a consolidated final answer. Your answer MUST be a prioritized list, ordered from most critical to least critical. For each identified risk, you MUST begin the line with a priority score tag:
    - [P0 - CRITICAL] for 'High' criticality events.
    - [P1 - WARNING] for 'Medium' criticality events.
    - [P2 - INFO] for 'Low' criticality events.

    If after several different search attempts you still find no risks, then and only then should you state that clearly. Begin your analysis.
    """

    
    print("\n--- Running Supply Chain Agent ---")
    agent_executor.invoke({
        "input": master_task
    })