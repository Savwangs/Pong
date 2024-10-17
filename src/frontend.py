import streamlit as st
from src.backend import Backend

class Frontend:
    def __init__(self):
        self.backend = Backend()

    def run(self):
        st.title("Savir's Chatbot")

        # Initialize session state
        if "user_name" not in st.session_state:
            st.session_state.user_name = ""
        if "conversation" not in st.session_state:
            st.session_state.conversation = []

        # Ask for user's name if not already provided
        if not st.session_state.user_name:
            user_name = st.text_input("Please enter your name:")
            if st.button("Submit Name"):
                st.session_state.user_name = user_name
                st.rerun()

        if st.session_state.user_name:
            st.write(f"Hello, {st.session_state.user_name}!")

            # Text input for user message
            user_message = st.text_input("Enter your message:")

            if st.button("Send") and user_message:
                # Get response from backend using the new get_response method
                response = self.backend.get_response(st.session_state.user_name, user_message)

                # Display the response
                st.write(f"Savir: {response}")

                # Update conversation history
                st.session_state.conversation.append(("User", user_message))
                st.session_state.conversation.append(("Savir", response))

            # Display conversation history
            st.write("Conversation History:")
            for speaker, message in st.session_state.conversation:
                st.write(f"{speaker}: {message}")

if __name__ == "__main__":
    frontend = Frontend()
    frontend.run()