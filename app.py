import streamlit as st
from orchestrator import handle_query

st.set_page_config(page_title="HR Policy Agent", layout="wide")
st.title("🧑‍💼 HR Policy Assistant")

query = st.text_area(
    "Ask an HR policy question",
    placeholder="e.g. How many casual leaves are allowed per year?"
)

if st.button("Submit") and query.strip():
    with st.spinner("Thinking..."):
        data = handle_query(query)

    st.subheader("📌 Decision")
    st.markdown(data["decision"])

    st.subheader("📊 Confidence")
    st.metric("Confidence Score", data["confidence"]["confidence_score"])

    for note in data["confidence"]["risk_notes"]:
        st.markdown(f"- {note}")

    st.subheader("📚 Sources")
    if not data["sources"]:
        st.info("No sources found")

    for s in data["sources"]:
        st.markdown(f"- `{s['source']}` (page {s['page']})")
