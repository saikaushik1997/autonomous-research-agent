import sys
sys.path.append("..")

from dotenv import load_dotenv
load_dotenv()

from app.agent.tools import search_web, search_documents, warmup_rag_api

# Test 1 — web search
print("Testing web search...")
result = search_web.invoke("What is retrieval augmented generation?")
print(result[:500])
print("\n---\n")

# Test 2 — RAG (warm up first)
print("Warming up RAG API...")
warmup_rag_api()
print("Testing document search...")
result = search_documents.invoke("What is the Gibbs sampling algorithm?")
print(result[:500])