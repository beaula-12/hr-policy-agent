
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
from agents.memory import memory

def reason(case_data, documents):
    llm = get_llm()

    policies_text = "\n\n".join(
        f"- {d.page_content}" for d in documents
    )

    chat_history = memory.load_memory_variables({}).get("chat_history", [])

    prompt = f"""
You are an HR policy assistant.

Conversation so far:
{chat_history}

Use ONLY the policies below.

Return:
- Short final decision (2–3 lines)
- Brief explanation paragraph

Current Case:
{case_data}

Policies:
{policies_text}
"""

    response = llm.invoke(prompt).content.strip()

    memory.save_context(
        {"input": case_data},
        {"output": response}
    )

    return response
