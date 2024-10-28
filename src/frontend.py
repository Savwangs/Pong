import streamlit as st
from src.backend import Backend

class Frontend:
    def __init__(self):
        self.backend = Backend()

    def run(self):
        st.title("Savir Bot")

        # Initialize session state
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "user_name" not in st.session_state:
            st.session_state.user_name = ""

        # User name input
        if not st.session_state.user_name:
            user_name = st.text_input("Enter contact name:")
            if st.button("Start Chat"):
                st.session_state.user_name = user_name.strip()
                st.rerun()

        # Chat interface
        if st.session_state.user_name:
            st.write(f"Chatting with {st.session_state.user_name}")

            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Chat input
            if prompt := st.chat_input("Type your message..."):
                # Add user message to chat
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Get bot response
                response = self.backend.get_response(st.session_state.user_name, prompt)
                
                # Add bot response to chat
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                st.rerun()