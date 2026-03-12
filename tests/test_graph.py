from app.agent.graph import agent
from app.agent.tools import warmup_rag_api
from langchain_core.messages import HumanMessage

print("Warming up RAG API...")
warmup_rag_api()

print("Running agent...")
result = agent.invoke({
    "messages": [HumanMessage(content="Start researching")],
    "research_topic": "Gibbs sampling in bioinformatics",
    "final_report": ""
})

print("\n=== FINAL MESSAGES ===")
for message in result["messages"]:
    print(f"\n{message.type}:")
    if hasattr(message, "tool_calls") and message.tool_calls:
        print(f"  tool calls: {[t['name'] for t in message.tool_calls]}")
    else:
        print(message.content[:500])