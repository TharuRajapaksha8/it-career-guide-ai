import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Career Guide AI", page_icon="💼", layout="wide")

st.title("💼 IT Career Guide AI")
st.write("Ask me about IT careers!")

if not os.getenv("GROQ_API_KEY"):
    st.error("Please set GROQ_API_KEY in .env file")
    st.stop()

if 'orchestrator' not in st.session_state:
    from src.main import get_orchestrator
    with st.spinner("Loading agents..."):
        st.session_state.orchestrator = get_orchestrator()

with st.sidebar:
    st.header("Settings")
    
    pattern = st.selectbox(
        "Agent Pattern",
        ["single", "sequential", "parallel"],
        help="Single: One agent\nSequential: Assembly line\nParallel: Simultaneous research"
    )
    
    model_type = st.selectbox(
        "AI Model",
        ["groq", "openrouter"],
        help="Groq: Fast, cheap\nOpenRouter: Better quality, slower"
    )
    
    if model_type == "openrouter" and not os.getenv("OPENROUTER_API_KEY"):
        st.warning("OPENROUTER_API_KEY not set. Add to .env file.")
    
    st.markdown("---")
    st.header("Quick Questions")
    questions = [
        "What does a DevOps engineer do?",
        "How to become a cybersecurity professional?",
        "Compare cloud vs AI/ML",
        "What certifications for developer?"
    ]
    for q in questions:
        if st.button(q):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
    
    st.markdown("---")
    st.caption(f"Model: {model_type}")

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about IT careers..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                if model_type == "openrouter" and not os.getenv("OPENROUTER_API_KEY"):
                    st.error("OPENROUTER_API_KEY not set. Please add to .env file or switch to Groq.")
                else:
                    st.session_state.orchestrator = get_orchestrator(model_type)
                    result = st.session_state.orchestrator.run(prompt, pattern)
                    
                    if pattern == "single":
                        answer = result.get('final_answer', 'No answer')
                    elif pattern == "sequential":
                        answer = result.get('final_roadmap', 'No roadmap')
                    elif pattern == "parallel":
                        answer = result.get('final_comparison', 'No comparison')
                    else:
                        answer = "No answer"
                    
                    st.write(answer)
                    st.caption(f"Pattern: {pattern} | Model: {model_type}")
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Built with LangGraph, Groq, and Streamlit")