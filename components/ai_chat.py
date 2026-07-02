import streamlit as st
from services.gemini_service import GeminiService
from utils.prompts import AI_CHAT_SYSTEM_INSTRUCTION

def render(gemini_service: GeminiService):
    """
    Renders the AI Chat Assistant page for DhanushaBuddy.
    Acts as a conversational placement prep mentor.
    """
    st.markdown(
        '<h1>💬 AI <span class="gradient-text">Chat Mentor</span></h1>', 
        unsafe_allow_html=True
    )
    st.write(
        "Ask programming doubts, review code snippets, practice HR questions, "
        "or request career and resume advice from your DhanushaBuddy mentor."
    )
    st.markdown("---")

    # Initialize chat history in session state
    if "buddy_chat_history" not in st.session_state:
        st.session_state.buddy_chat_history = [
            {
                "role": "assistant", 
                "content": (
                    "Hello! I am DhanushaBuddy, your placement mentor. How can I assist you today?\n\n"
                    "Feel free to ask technical questions, check coding logic, request resume guidance, "
                    "or explore corporate interview prep tips."
                )
            }
        ]

    # Predefined quick prompts layout
    st.subheader("💡 Quick Prompts")
    quick_prompts = [
        "Explain Java OOP.",
        "Ask me an HR interview question.",
        "Give me an aptitude question.",
        "Explain SQL JOIN.",
        "Help me improve my resume."
    ]

    cols = st.columns(len(quick_prompts))
    selected_prompt = None
    for idx, prompt_text in enumerate(quick_prompts):
        if cols[idx].button(prompt_text, use_container_width=True, key=f"quick_prompt_{idx}"):
            selected_prompt = prompt_text

    # Top control bar (e.g., Clear Chat)
    col_chat, col_clear = st.columns([6, 1])
    with col_clear:
        if st.button("Clear Chat", help="Clear conversation history", type="secondary", use_container_width=True):
            st.session_state.buddy_chat_history = [
                {
                    "role": "assistant", 
                    "content": (
                        "Hello! I am DhanushaBuddy, your placement mentor. How can I assist you today?\n\n"
                        "Feel free to ask technical questions, check coding logic, request resume guidance, "
                        "or explore corporate interview prep tips."
                    )
                }
            ]
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Render all chat messages from session state
    for message in st.session_state.buddy_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Check if the last message was sent by the user (meaning we need to generate response)
    if st.session_state.buddy_chat_history[-1]["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("DhanushaBuddy is typing..."):
                response = gemini_service.get_chat_response(
                    messages=st.session_state.buddy_chat_history,
                    system_instruction=AI_CHAT_SYSTEM_INSTRUCTION
                )
                st.markdown(response)
                
        # Append the assistant's response to history and rerun to refresh
        st.session_state.buddy_chat_history.append({"role": "assistant", "content": response})
        st.rerun()

    # Capture User Inputs (from Chat Input bar or Quick Prompt buttons)
    user_input = st.chat_input("Ask DhanushaBuddy anything (e.g. 'How does a BST differ from an AVL tree?')")
    
    prompt_to_send = None
    if user_input:
        prompt_to_send = user_input.strip()
    elif selected_prompt:
        prompt_to_send = selected_prompt

    # Process and append user input
    if prompt_to_send:
        st.session_state.buddy_chat_history.append({"role": "user", "content": prompt_to_send})
        st.rerun()
