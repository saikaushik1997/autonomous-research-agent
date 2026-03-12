from app.agent.state import AgentState
from app.agent.nodes import agent_node, should_continue
from langchain_core.messages import HumanMessage

# Test 1 — agent node makes a decision
print("Testing agent node...")
state = AgentState(
    messages=[HumanMessage(content="Start researching")],
    research_topic="Gibbs sampling in bioinformatics",
    final_report=""
)

result = agent_node(state)
last_message = result["messages"][-1]
print(f"Message type: {last_message.type}")
print(f"Tool calls: {last_message.tool_calls}")

# Test 2 — should_continue routes correctly
print("\nTesting should_continue...")
state["messages"].append(last_message)
decision = should_continue(state)
print(f"Decision: {decision}")