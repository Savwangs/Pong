import streamlit as st
from src.backend import Backend

class Frontend:
    def __init__(self):
        self.backend = Backend()

    def run(self):
        st.title("Personalized Chatbot")

        if "user_name" not in st.session_state:
            st.session_state.user_name = ""
        if "conversation" not in st.session_state:
            st.session_state.conversation = []

        if not st.session_state.user_name:
            user_name = st.text_input("Please enter your name:")
            if st.button("Submit Name"):
                st.session_state.user_name = user_name.lower()
                st.rerun()  # Use st.rerun() instead of st.experimental_rerun()

        if st.session_state.user_name:
            st.write(f"Hello, {st.session_state.user_name}!")

            user_message = st.text_input("Enter your message:")

            if st.button("Send") and user_message:
                try:
                    response = self.backend.get_response(st.session_state.user_name, user_message)
                    st.session_state.conversation.append(("User", user_message))
                    st.session_state.conversation.append(("Savir", response))
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")

            st.write("Conversation History:")
            for speaker, message in st.session_state.conversation:
                st.write(f"{speaker}: {message}")

if __name__ == "__main__":
    frontend = Frontend()
    frontend.run()