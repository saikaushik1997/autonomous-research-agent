from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    
    # Tavily
    tavily_api_key: str
    
    # RAG API
    rag_api_url: str = "https://document-qna-rag.onrender.com"
    rag_namespace: str = "gibbs-2.pdf"
    
    # Agent
    max_iterations: int = 10
    model_name: str = "gpt-4o-mini"
    
    # LangSmith
    langsmith_api_key: str = ""
    langsmith_tracing: bool = False
    langsmith_project: str = "autonomous-research-agent"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()