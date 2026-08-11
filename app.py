import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Career Guide AI", page_icon="💼", layout="wide")

st.title("💼 IT Career Guide AI")
st.write("Ask me about IT careers!")

try:
    groq_key = st.secrets.get("GROQ_API_KEY")
except:
    groq_key = os.getenv("GROQ_API_KEY")

if not groq_key:
    st.error("❌ GROQ_API_KEY not found!")
    st.info("For local: Add to .env file\nFor Streamlit Cloud: Add in Secrets")
    st.stop()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize orchestrator
if 'orchestrator' not in st.session_state:
    from src.main import get_orchestrator
    with st.spinner("Loading agents..."):
        try:
            st.session_state.orchestrator = get_orchestrator()
            st.success("✅ Agents loaded!")
        except Exception as e:
            st.error(f"Error loading agents: {e}")
            st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    pattern = st.selectbox(
        "Agent Pattern",
        ["single", "sequential", "parallel"],
        help="Single: One agent handles everything\nSequential: Agents work in order\nParallel: Agents research simultaneously"
    )
    
    model_type = st.selectbox(
        "AI Model",
        ["groq", "openrouter"],
        help="Groq: Fast, cheap\nOpenRouter: Better quality, slower"
    )
    
    if model_type == "openrouter":
        try:
            has_openrouter = st.secrets.get("OPENROUTER_API_KEY") is not None
        except:
            has_openrouter = os.getenv("OPENROUTER_API_KEY") is not None
        if not has_openrouter:
            st.warning("⚠️ OPENROUTER_API_KEY not set. Switch to Groq.")
    
    st.markdown("---")
    st.header("📌 Quick Questions")
    questions = [
        "What does a DevOps engineer do?",
        "How to become a cybersecurity professional?",
        "Compare cloud vs AI/ML",
        "What certifications for developer?",
        "Tell me about data engineering"
    ]
    for q in questions:
        if st.button(q, use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()
    
    st.markdown("---")
    st.caption(f"Model: {model_type} | Pattern: {pattern}")

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about IT careers..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Run orchestrator with selected pattern
                result = st.session_state.orchestrator.run(prompt, pattern)
                
                # Extract answer based on pattern
                if pattern == "single":
                    answer = result.get('final_answer', 'No answer generated')
                elif pattern == "sequential":
                    answer = result.get('final_roadmap', 'No roadmap generated')
                elif pattern == "parallel":
                    answer = result.get('final_comparison', 'No comparison generated')
                else:
                    answer = "No answer"
                
                st.write(answer)
                st.caption(f"Pattern: {pattern} | Model: {model_type}")
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.divider()
st.caption("Built with LangGraph, Groq, and Streamlit")