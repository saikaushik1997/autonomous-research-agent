from fastapi import FastAPI
from app.api.routes.research import router
from app.agent.tools import warmup_rag_api
from contextlib import asynccontextmanager
import logging

logging.basicConfig(level=logging.INFO)

# lifespan function - everything before yield runs on startup
# everything after that runs just before shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # warm up RAG API on startup - so we're ready to send the RAG requests
    # since it has a cold start problem
    try:
        warmup_rag_api()
    except Exception as e:
        logging.warning(f"RAG API warmup failed: {e}")
    yield

app = FastAPI(
    title="Autonomous Research Agent",
    description="LangGraph-powered research agent with web search and RAG",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}