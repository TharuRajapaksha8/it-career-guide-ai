"""
Career Guide AI - Streamlit App
Simple interface for career guidance
"""

import streamlit as st
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Setup page
st.set_page_config(
    page_title="Career Guide AI",
    page_icon="💼",
    layout="wide"
)

st.title("💼 IT Career Guide AI")
st.write("Ask me about IT careers!")

# Check API key
if not os.getenv("GROQ_API_KEY"):
    st.error("⚠️ Please set GROQ_API_KEY in .env file")
    st.stop()

# Initialize
if 'orchestrator' not in st.session_state:
    from src.main import get_orchestrator
    with st.spinner("Loading..."):
        st.session_state.orchestrator = get_orchestrator()


with st.sidebar:
    st.header("⚙️ Settings")
    
    pattern = st.selectbox(
        "Agent Pattern",
        ["single", "sequential", "parallel"],
        help="Single: One agent handles everything\nSequential: Agents work in order\nParallel: Agents research simultaneously"
    )
    
    st.markdown("---")
   
    st.header("🔍 Quick Questions")
    questions = [
        "What does a DevOps engineer do?",
        "How to become a cybersecurity professional?",
        "Compare cloud vs AI/ML careers",
        "What certifications for developer?",
        "Tell me about data engineering"
    ]
    
    for q in questions:
        if st.button(q, key=f"q_{q[:10]}"):
            st.session_state.messages.append({"role": "user", "content": q})
            st.rerun()

if 'messages' not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about IT careers..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.write(prompt)
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = st.session_state.orchestrator.run(prompt, pattern)
                
                # Get answer based on pattern
                if pattern == "single":
                    answer = result.get('final_answer', 'No answer')
                elif pattern == "sequential":
                    answer = result.get('final_roadmap', 'No roadmap')
                elif pattern == "parallel":
                    answer = result.get('final_comparison', 'No comparison')
                else:
                    answer = "No answer"
                
                st.write(answer)
                st.caption(f"Pattern: {pattern}")
                
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Please check your API key and try again.")

# Footer
st.divider()
st.caption("Built with LangGraph, Groq, and Streamlit")