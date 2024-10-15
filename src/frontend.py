import streamlit as st
from backend import Backend

class Frontend:
    def __init__(self):
        self.backend = Backend()

    def run(self):
        st.title("Savir Chatbot")

        # Ask for user's name if not already provided
        if "user_name" not in st.session_state:
            st.session_state.user_name = st.text_input("Please enter your name:")

        if st.session_state.user_name:
            st.write(f"Hello, {st.session_state.user_name}!")

            # Initialize conversation history
            if "conversation" not in st.session_state:
                st.session_state.conversation = []

            # Text input for user message
            user_message = st.text_input("Enter your message:")

            if st.button("Send") and user_message:
                # Get response from backend
                response = self.backend.get_most_relevant_given_text(st.session_state.user_name, user_message)

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