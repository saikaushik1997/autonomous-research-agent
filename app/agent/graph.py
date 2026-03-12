from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from app.agent.state import AgentState
from app.agent.nodes import agent_node, should_continue
from app.agent.tools import search_web, search_documents

tools = [search_web, search_documents]

def build_graph():
    graph = StateGraph(AgentState)

    # nodes
    graph.add_node("agent", agent_node)
    graph.add_node("tools", ToolNode(tools))

    # edges
    graph.set_entry_point("agent")
    graph.add_conditional_edges(
        "agent",
        should_continue,
        {"tools": "tools", "end": END}
    )
    graph.add_edge("tools", "agent")

    return graph.compile()

agent = build_graph()