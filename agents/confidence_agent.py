# from llm_factory import get_llm
import json

def score(decision: str):
    llm = get_llm()
    prompt = f"""
Give confidence score between 0 and 1.
Give 1–3 risk notes.

Return STRICT JSON:
{{
  "confidence_score": 0.9,
  "risk_notes": ["..."]
}}

Decision:
{decision}
"""
    try:
        return json.loads(llm.invoke(prompt).content)
    except:
        return {
            "confidence_score": 0.75,
            "risk_notes": ["Confidence parsing fallback"]
        }
