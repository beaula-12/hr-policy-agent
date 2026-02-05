import streamlit as st
from orchestrator import handle_query
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError

st.set_page_config(page_title="HR Policy Agent", layout="wide")
st.title("🧑‍💼 HR Policy Assistant")

# ---- UI chat history (display only) ----
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Chat input ----
user_query = st.chat_input("Ask an HR policy question...")

if user_query:
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Thinking..."):
                data = handle_query(user_query)

            # Decision
            st.markdown("### 📌 Decision")
            st.markdown(data["decision"])

            # Confidence
            st.markdown("### 📊 Confidence")
            st.metric(
                "Confidence Score",
                data["confidence"]["confidence_score"]
            )

            for note in data["confidence"]["risk_notes"]:
                st.markdown(f"- {note}")

            # Sources
            st.markdown("### 📚 Sources")
            if not data["sources"]:
                st.info("No sources found")
            else:
                seen = set()
                for s in data["sources"]:
                    key = (s["source"], s["page"])
                    if key not in seen:
                        seen.add(key)
                        st.markdown(f"- `{s['source']}` (page {s['page']})")

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": data["decision"]
            })

        except ChatGoogleGenerativeAIError as e:
            if "RESOURCE_EXHAUSTED" in str(e):
                st.error(
                    "😕 **Oh no! Resource exhausted**\n\n"
                    "You’ve reached the free usage limit for today.\n\n"
                    "👉 Please try again after **24 hours**."
                )
            else:
                st.error("⚠️ Something went wrong while generating the response.")

            st.stop()
