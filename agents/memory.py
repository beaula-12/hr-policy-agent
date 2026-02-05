from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    k=2,                      # 👈 remember last 2 turns
    return_messages=True
)
