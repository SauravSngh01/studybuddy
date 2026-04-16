import streamlit as st
from src.agent import get_agent

# --- CONFIGURATION ---
# Keep this True for the presentation to trigger the pre-recorded response
USE_DUMMY_LLM = True 

# --- PAGE SETUP ---
st.set_page_config(page_title="StudyBuddy AI", layout="centered")
st.title("📚 StudyBuddy: AI Planner")

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- INITIALIZE AGENT (Once) ---
if "agent" not in st.session_state:
    st.session_state.agent = get_agent(use_dummy_llm=USE_DUMMY_LLM)
    # The UI warnings have been completely removed for a stealthy presentation.

# --- DISPLAY CHAT ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- HANDLE INPUT ---
if prompt := st.chat_input("Ask me to plan your study..."):
    # 1. User Message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.agent.run(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {e}")