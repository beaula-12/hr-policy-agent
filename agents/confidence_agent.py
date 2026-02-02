# from llm_factory import get_llm
import json
import re

def score(decision: str):
    llm = get_llm()

    prompt = f"""
You MUST return ONLY valid JSON.
No text. No markdown. No explanation.

JSON format:
{{
  "confidence_score": number between 0 and 1,
  "risk_notes": array of strings
}}

Decision:
{decision}
"""

    response = llm.invoke(prompt).content.strip()

    # Extract JSON safely
    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        return json.loads(match.group())

    return {
        "confidence_score": 0.75,
        "risk_notes": ["Confidence parsing fallback"]
    }