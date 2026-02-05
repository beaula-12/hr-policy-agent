from agents.intent_agent import classify
from agents.case_agent import analyze
from agents.reasoning_agent import reason
from agents.confidence_agent import score
from agents.rag_agent import rag_agent

# def handle_query(query: str):
def handle_query(query: str, history=None):
    intent = classify(query)

    documents = rag_agent(query)

    case_data = analyze(query)

    # decision = reason(case_data, documents)
    decision = reason(case_data, documents, history)

    confidence = score(decision)

    # Extract sources safely
    sources = []
    for d in documents:
        if d.metadata:
            sources.append({
                "source": d.metadata.get("source", "Unknown"),
                "page": d.metadata.get("page", "N/A")
            })

    return {
        "decision": decision,
        "confidence": confidence,
        "sources": sources
    }

