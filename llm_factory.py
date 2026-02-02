from langchain_google_genai import ChatGoogleGenerativeAI
import os

_llm = None  # cache

def get_llm():
    global _llm
    if _llm is None:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY not set")

        _llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_retries=2,
            google_api_key=api_key
        )
    return _llm
