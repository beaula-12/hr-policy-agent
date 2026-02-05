
# from llm_factory import get_llm

# def reason(case_data, documents):
#     llm = get_llm()
#     policies_text = "\n\n".join(
#         f"- {d.page_content}" for d in documents
#     )

#     prompt = f"""
# You are an HR policy decision agent.

# Use ONLY the policies below.

# Return:
# - Short final decision (2–3 lines)
# - Brief explanation paragraph

# Case:
# {case_data}

# Policies:
# {policies_text}
# """
#     return llm.invoke(prompt).content.strip()

from llm_factory import get_llm

def reason(case_data, documents, history=None):
    llm = get_llm()

    policies_text = "\n\n".join(
        f"- {d.page_content}" for d in documents
    )

    conversation = ""
    if history:
        conversation = "\n".join(
            f"{m['role']}: {m['content']}" for m in history
        )

    prompt = f"""
You are an HR policy assistant.

Conversation so far:
{conversation}

Use ONLY the policies below.

Return:
- Short final decision (2–3 lines)
- Brief explanation paragraph

Current Case:
{case_data}

Policies:
{policies_text}
"""

    return llm.invoke(prompt).content.strip()
