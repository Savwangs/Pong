import streamlit as st
from src.memory import Memory
from src.llm import LLM

class Frontend:
    def __init__(self, memory, llm):
        self.memory = memory
        self.llm = llm

    def run(self):
        st.title("OpenAI GPT-4o-mini Chatbot")
        st.write("Interact with the GPT-4 chatbot by entering your prompt below.")

        if "conversation" not in st.session_state:
            st.session_state.conversation = self.memory.load_conversation()

        user_input = st.text_input("Enter your prompt:")

        if st.button("Get Response"):
            if user_input:
                st.session_state.conversation.append(("user", user_input))
                response = self.llm.get_response(st.session_state.conversation)
                st.session_state.conversation.append(("assistant", response))
                self.memory.save_conversation(st.session_state.conversation)
            else:
                st.write("Please enter a prompt.")

        for role, msg in st.session_state.conversation:
            if role == "user":
                st.write(f"**You:** {msg}")
            else:
                st.write(f"**Bot:** {msg}")
