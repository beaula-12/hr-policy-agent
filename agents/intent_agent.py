# from llm_factory import get_llm
# llm = get_llm()

# def classify(query: str):
#     prompt = f"""
# Classify HR query intent:
# lookup | decision | exception | insufficient_info

# Query: {query}
# Return only the label.
# """
#     return llm.invoke(prompt).content.strip()
from llm_factory import get_llm

def classify(query: str):
    llm = get_llm()
    prompt = f"""
Classify HR query intent:
lookup | decision | exception | insufficient_info

Query: {query}
Return only the label.
"""
    return llm.invoke(prompt).content.strip()

