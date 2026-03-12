# Langgraph Nodes defined here
from langchain_openai import ChatOpenAI
from app.agent.state import AgentState
from app.agent.tools import search_web, search_documents
from app.config import settings

llm = ChatOpenAI(
    model=settings.model_name,
    api_key=settings.openai_api_key
)

tools = [search_web, search_documents]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: AgentState) -> dict:
    """Main agent node — LLM decides what to do next."""
    system_prompt = f"""You are an expert research assistant who can read and write reports exceptionally. Your goal is to research the following topic thoroughly:

{state['research_topic']}

You have access to two tools:
- search_web: for current information, recent developments, and general knowledge
- search_documents: for specific technical details from the research knowledge base

Use both tools to gather comprehensive information before writing your final report.
Your final report should be structured with clear sections: Overview, Key Concepts, Current Developments, and Conclusion."""

    messages = [
        {"role": "system", "content": system_prompt},
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: AgentState) -> str:
    """Decide whether to continue to tools or end."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return "end"