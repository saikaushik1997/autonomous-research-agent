from pydantic import BaseModel

class ResearchRequest(BaseModel):
    topic: str
    namespace: str = "gibbs-2.pdf"

class ResearchResponse(BaseModel):
    topic: str
    report: str
    messages_count: int