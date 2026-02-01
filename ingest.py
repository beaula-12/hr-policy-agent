# # import os
# # from langchain_community.document_loaders import PyPDFLoader
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_chroma import Chroma
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from config import CHROMA_PATH


# # def ingest_policies(folder="data/pdfs"):
# #     documents = []

# #     for file in os.listdir(folder):
# #         if file.endswith(".pdf"):
# #             loader = PyPDFLoader(os.path.join(folder, file))
# #             documents.extend(loader.load())

# #     splitter = RecursiveCharacterTextSplitter(
# #         chunk_size=800,
# #         chunk_overlap=150
# #     )

# #     chunks = splitter.split_documents(documents)

# #     embeddings = HuggingFaceEmbeddings(
# #         model_name="all-MiniLM-L6-v2"
# #     )

# #     # ✅ Chroma auto-persists when persist_directory is set
# #     Chroma.from_documents(
# #         documents=chunks,
# #         embedding=embeddings,
# #         persist_directory=CHROMA_PATH
# #     )

# #     print("✅ Policy ingestion completed successfully")


# # if __name__ == "__main__":
# #     ingest_policies()


# from langchain_chroma import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_core.documents import Document

# import os

# # -------- Embeddings --------
# embeddings = HuggingFaceEmbeddings(
#     model_name="all-MiniLM-L6-v2"
# )

# # -------- Vector DB --------
# vectordb = Chroma(
#     collection_name="hr_policy_collection",
#     embedding_function=embeddings,
#     persist_directory="data/embeddings",
# )

# # -------- Load HR policy text files --------
# def load_documents():
#     docs = []
#     policies_dir = "data/policies"

#     for filename in os.listdir(policies_dir):
#         if filename.endswith(".txt"):
#             path = os.path.join(policies_dir, filename)

#             with open(path, "r", encoding="utf-8") as f:
#                 text = f.read()

#             docs.append(
#                 Document(
#                     page_content=text,
#                     metadata={
#                         "source": filename,
#                         "page": "N/A"
#                     }
#                 )
#             )

#     return docs


# if __name__ == "__main__":
#     documents = load_documents()

#     vectordb.add_documents(documents)
#     vectordb.persist()

#     print(f"✅ Ingested {len(documents)} documents with metadata")

import os
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ---------------- EMBEDDINGS ----------------
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# ---------------- VECTOR DB ----------------
vectordb = Chroma(
    collection_name="hr_policy_collection",
    embedding_function=embeddings,
    persist_directory="data/embeddings",
)

# ---------------- LOAD DOCUMENTS ----------------
def load_documents():
    policies_dir = "data/policies"
    documents = []

    print("📂 Reading from:", os.path.abspath(policies_dir))

    if not os.path.exists(policies_dir):
        raise FileNotFoundError("❌ data/policies folder not found")

    for filename in os.listdir(policies_dir):
        file_path = os.path.join(policies_dir, filename)
        print("📄 Found:", filename)

        # ---------- PDF ----------
        if filename.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            pdf_docs = loader.load()

            for doc in pdf_docs:
                doc.metadata["source"] = filename
                documents.append(doc)

        # ---------- TXT ----------
        elif filename.lower().endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read().strip()
                if text:
                    documents.append(
                        Document(
                            page_content=text,
                            metadata={"source": filename}
                        )
                    )

    if not documents:
        raise ValueError("❌ No documents loaded. PDFs or TXTs required.")

    return documents

# ---------------- INGEST ----------------
def ingest():
    print("🔹 Loading documents...")
    documents = load_documents()

    print(f"✅ Loaded {len(documents)} pages")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    print("🔹 Splitting documents...")
    chunks = splitter.split_documents(documents)

    print(f"🔹 Creating embeddings for {len(chunks)} chunks...")
    vectordb.add_documents(chunks)

    print("✅ Ingestion completed successfully!")


# ---------------- RUN ----------------
if __name__ == "__main__":
    ingest()
