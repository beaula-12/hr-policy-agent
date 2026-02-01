from llm_factory import get_llm
llm = get_llm()

def analyze(query: str):
    prompt = f"""
Extract:
- employee facts
- scenario
- missing info
- ambiguity

Query: {query}
"""
    return llm.invoke(prompt).content.strip()
