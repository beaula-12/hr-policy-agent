from llm_factory import get_llm
llm = get_llm()

def reason(case_data, documents):
    policies_text = "\n\n".join(
        f"- {d.page_content}" for d in documents
    )

    prompt = f"""
You are an HR policy decision agent.

Use ONLY the policies below.

Return:
- Short final decision (2–3 lines)
- Brief explanation paragraph

Case:
{case_data}

Policies:
{policies_text}
"""

    return llm.invoke(prompt).content.strip()
