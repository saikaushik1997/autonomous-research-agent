import requests
from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from app.config import settings
import time

# ── Web Search Tool ──────────────────────────────────────────
tavily = TavilySearch(
    max_results=5,
    api_key=settings.tavily_api_key
)

# web search tool using Tavily API
@tool
def search_web(query: str) -> str:
    """Search the web for current information on a topic. 
    Use this for recent developments, news, and general knowledge."""
    response = tavily.invoke(query)
    results = response["results"]
    return "\n\n".join([
        f"Source: {r['url']}\n{r['content']}"
        for r in results
    ])

# ── RAG Tool ─────────────────────────────────────────────────
# Since I'm using the free version of Render, it suffers from a cold start problem, 
# this is to combat that.
def warmup_rag_api(retries: int = 5, wait: int = 10) -> bool:
    """Wake up the RAG API before running the agent."""
    url = f"{settings.rag_api_url}/health"
    for attempt in range(retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print("RAG API is ready")
                return True
        except requests.exceptions.RequestException:
            pass
        print(f"RAG API warming up... attempt {attempt + 1}/{retries}")
        time.sleep(wait)
    raise Exception("RAG API failed to warm up after max retries")

# actual RAG API call
@tool
def search_documents(query: str) -> str:
    """Search the research document knowledge base for relevant information.
    Use this for specific technical details, paper content, and domain knowledge."""
    response = requests.post(
        f"{settings.rag_api_url}/api/v1/query",
        json={
            "question": query,
            "namespace": settings.rag_namespace
        },
        timeout=30
    )
    response.raise_for_status()
    return response.json()["answer"]