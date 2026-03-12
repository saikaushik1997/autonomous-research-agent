from fastapi import APIRouter, HTTPException
from app.models.schemas import ResearchRequest, ResearchResponse
from app.agent.graph import agent
from app.config import settings
from langchain_core.messages import HumanMessage
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    try:
        # update namespace from request
        settings.rag_namespace = request.namespace

        result = agent.invoke({
            "messages": [HumanMessage(content="Start researching")],
            "research_topic": request.topic,
            "final_report": ""
        })

        # last ai message is the final report, intermediate ai messages are meant for the tools.
        # searching from the end to ensure we hit the last one first and then stop.
        final_message = next(
            m for m in reversed(result["messages"])
            if m.type == "ai" and m.content
        )

        return ResearchResponse(
            topic=request.topic,
            report=final_message.content,
            messages_count=len(result["messages"])
        )

    except Exception as e:
        logger.error(f"Research failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))