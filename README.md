# autonomous-research-agent

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![LangGraph](https://img.shields.io/badge/LangGraph-1.x-orange)
![LangChain](https://img.shields.io/badge/LangChain-1.x-yellow)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

An autonomous research agent that independently researches any topic by orchestrating web search and document retrieval — powered by LangGraph, Tavily, and a live RAG microservice.

**GitHub:** https://github.com/saikaushik1997/autonomous-research-agent

---

## Demo

> TODO: Add Loom demo GIF here

---

## Architecture

```
User enters research topic
        ↓
FastAPI receives POST /api/v1/research
        ↓
LangGraph agent invoked
        ↓
─────────────────────────────────────────
AGENT LOOP (ReAct pattern)

Agent (GPT-4o-mini) reads topic
        ↓
Decides which tools to call
        ↓
search_web ──────────────── Tavily API
search_documents ─────────── RAG Microservice (Project 1)
        ↓
Agent observes both results
        ↓
Decides: enough information → generate report
        ↓
Structured research report generated

AGENT LOOP ENDS
─────────────────────────────────────────
        ↓
FastAPI returns report + message count
        ↓
Streamlit renders report
```

**LangGraph graph:**
```
START → agent node → should_continue?
                         ↙           ↘
                      tools          END
                         ↓
                    tool node
                         ↓
                   back to agent
```

---

## Key Engineering Decisions

**RAG pipeline as a microservice**
Rather than duplicating the RAG logic from Project 1, the agent calls the live document Q&A API over HTTP. The agent doesn't need to know how retrieval works internally — it just calls an endpoint and gets an answer back. This keeps the two projects independently deployable and reflects how production AI systems are actually composed — as a set of specialized services rather than one monolithic application.

**Warmup call before agent invocation**
Both the RAG API and the research agent API run on Render's free tier, which spins down services after inactivity. A warmup loop polls the RAG API health endpoint before invoking the agent, preventing mid-run cold start failures that would otherwise cause the agent to error out mid-loop.

**Over-fetching in tools**
The `search_web` tool fetches 5 results from Tavily before passing to the agent. More candidates give the LLM better material to synthesize from — similar to the over-fetch before rerank pattern in Project 1's retrieval pipeline.

**Explicit synthesis instruction in system prompt**
Without explicit instruction, the agent tended to rely on web search results alone and underutilize the document knowledge base. Adding an explicit instruction to synthesize both sources in the final report significantly improved retrieval utilization across both tools.

**Namespace-scoped document search**
The document namespace is passed as a request parameter rather than hardcoded, allowing the agent to search any document that has been ingested into the RAG service. This makes the research agent general-purpose — not tied to a single document.

---

## Running Locally

**Prerequisites:** Python 3.11, Project 1 RAG API running locally or on Render

```bash
# 1. clone the repo
git clone https://github.com/saikaushik1997/autonomous-research-agent
cd autonomous-research-agent

# 2. install dependencies
pip install -r requirements.txt

# 3. set up environment variables
cp .env.example .env
# fill in your API keys in .env

# 4. start the API
python -m uvicorn app.main:app --reload

# 5. start the UI (separate terminal)
streamlit run streamlit_app.py
```

API available at `http://localhost:8000/docs`  
UI available at `http://localhost:8501`

**With Docker:**
```bash
docker compose up
```

---

## What I Would Do Next

**RAGAS evaluation**
Add an evaluation notebook measuring faithfulness, context precision, and answer relevancy across a testset of research questions. Compare retrieval quality with and without the document search tool to quantify its contribution to report quality.

**Streaming responses**
The agent currently waits for the full report before returning. Implementing SSE (Server-Sent Events) through FastAPI would allow token-by-token streaming, making the UI feel significantly more responsive for longer research tasks.

**Query reformulation**
Add a preprocessing step where a separate LLM call reformulates the user's topic into a more specific research question before passing it to the agent. Vague topics produce vague retrieval — a reformulation step improves retrieval quality without requiring the user to be precise.

**Multi-document research**
Currently the agent searches a single document namespace. A cross-namespace query mode would let the agent search across all ingested documents simultaneously, making it more useful for research tasks that span multiple sources.

**Persistent research history**
Research results are not stored — each run is stateless. Adding a database layer would allow users to revisit previous research sessions and compare reports across runs.

**Agent memory across sessions**
The agent has no memory of previous research runs. Adding long-term memory via a vector store would allow the agent to reference prior findings when researching related topics.
