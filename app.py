# import streamlit as st
# from orchestrator import handle_query

# st.set_page_config(page_title="HR Policy Agent", layout="wide")
# st.title("🧑‍💼 HR Policy Assistant")

# query = st.text_area(
#     "Ask an HR policy question",
#     placeholder="e.g. How many casual leaves are allowed per year?"
# )

# if st.button("Submit") and query.strip():
#     with st.spinner("Thinking..."):
#         data = handle_query(query)

#     st.subheader("📌 Decision")
#     st.markdown(data["decision"])

#     st.subheader("📊 Confidence")
#     st.metric("Confidence Score", data["confidence"]["confidence_score"])

#     for note in data["confidence"]["risk_notes"]:
#         st.markdown(f"- {note}")

#     st.subheader("📚 Sources")
#     if not data["sources"]:
#         st.info("No sources found")

#     for s in data["sources"]:
#         st.markdown(f"- `{s['source']}` (page {s['page']})")

import streamlit as st
from orchestrator import handle_query

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
    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_query
    })
    with st.chat_message("user"):
        st.markdown(user_query)

    # Assistant response
    with st.chat_message("assistant"):
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

    # Save assistant response (for UI only)
    st.session_state.messages.append({
        "role": "assistant",
        "content": data["decision"]
    })
