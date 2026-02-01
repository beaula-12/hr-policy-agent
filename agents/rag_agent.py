from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

vectordb = Chroma(
    collection_name="hr_policy_collection",
    embedding_function=embeddings,
    persist_directory="data/embeddings",
)

def rag_agent(query: str, k: int = 5):
    return vectordb.similarity_search(query, k=k)
