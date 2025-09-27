# Proactive Supply Chain Resilience Agent

This project is a proof-of-concept AI agent designed to proactively identify, analyze, and report on potential supply chain disruptions. It mirrors the mission of Kavida.ai by using integrated data (real-time news and an internal knowledge base) to manage supply chain risks.

The agent autonomously scans for news events, cross-references them against a company's simulated supply chain data, and provides a concise risk analysis, demonstrating an end-to-end RAG (Retrieval-Augmented Generation) and Agentic workflow.

## Core Features

- **Resilient & Autonomous Agent:** Uses a LangChain ReAct agent to reason, plan, and use custom tools. It can now recover from failed searches and adapt its strategy.
- **Prioritized Risk Scoring:** Automatically scores risks (P0-Critical, P1-Warning, P2-Info) by enriching the RAG pipeline with material criticality metadata.
- **Real-time News Ingestion:** Fetches the latest articles related to supply chain disruptions using the GNews API.
- **Internal Knowledge Base:** Uses a vector database (ChromaDB) to store and retrieve information about a company's suppliers and materials.
- **RAG Pipeline:** Employs a Retrieval-Augmented Generation architecture to provide the LLM with relevant, private context before making decisions.
- **Autonomous Agent:** Uses a LangChain ReAct agent to reason, plan, and use custom tools (`news_scanner_tool` and `supply_chain_retriever_tool`).
- **Flexible LLM Integration:** Powered by a model from OpenRouter (`mistral-ai/mistral-7b-instruct`), allowing for easy model swapping.
- **Containerized & Reproducible:** Fully containerized with Docker, ensuring easy setup and execution with a single command.

## Tech Stack

- **Programming Language:** Python 3.11
- **Core Frameworks:** LangChain
- **Key Libraries:** `langchain-openai`, `langchain-community`, `chromadb`, `sentence-transformers`
- **LLM Provider:** OpenRouter
- **Data Sources:** GNews API
- **Containerization:** Docker

---

## Getting Started

### Prerequisites

- Docker Desktop installed and running.
- Git installed.
- API keys from [GNews](https://gnews.io/) and [OpenRouter](https://openrouter.ai/).

### Installation & Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/Krasper707/supply-chain-agent.git
    cd supply-chain-agent
    ```

2.  **Create the environment file:**
    Create a file named `.env` in the root of the project and add your API keys:

    ```
    GNEWS_API_KEY="YOUR_GNEWS_KEY_HERE"
    OPENROUTER_API_KEY="YOUR_OPENROUTER_KEY_HERE"
    OPENROUTER_API_BASE="https://openrouter.ai/api/v1"
    ```

3.  **Build the Vector Database (First-time setup):**
    Before running the agent, you must create the vector database from the mock data. This command only needs to be run once.
    ```bash
    python vector_db.py
    ```
    This will create a `db/` folder in your project directory containing the knowledge base.

### Running the Agent

**Option 1: Run with Docker (Recommended)**

1.  **Build the Docker image:**

    ```bash
    docker build -t supply-chain-agent .
    ```

2.  **Run the container:**
    This command securely passes your API keys from the `.env` file into the container.
    ```bash
    docker run --rm --env-file .env supply-chain-agent
    ```

**Option 2: Run Locally (with a Virtual Environment)**

1.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the main application:**
    ```bash
    python main.py
    ```

---

## Example Agent Workflow

The agent now follows a resilient, multi-step research process and delivers a prioritized, decision-ready report.

```
> Entering new AgentExecutor chain...

Thought: My first broad query failed. I should not give up. I will try a more specific query.
Action: news_scanner_tool
Action Input: "factory fire"
Observation: [List of news articles about factory fires...]

Thought: I have found several articles. I will now check each location against our database to see if we have a supplier there and what their criticality is.
Action: supply_chain_retriever_tool
Action Input: "Mattress Factory in Kapurthala"
Observation: Found Match: ...Flame-Retardant Polyurethane Foam... Criticality Level: High
...

Final Answer:
- [P0 - CRITICAL] A factory fire in Kapurthala may affect the supply of 'Flame-Retardant Polyurethane Foam', a High criticality component from a supplier in Bangalore.
- [P0 - CRITICAL] A factory blaze in Senai may affect the supply of 'TECH-427-B Motor Stator', a High criticality component from a supplier in Saitama.
- [P2 - INFO] A furniture factory fire in Kathmandu has a potential link to our supply of 'Thermal Cotton Fabric', a Low criticality component.

> Finished chain.
```
