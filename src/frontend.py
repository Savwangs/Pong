import streamlit as st
from src.memory import Memory
from src.llm import LLM
from twilio.rest import Client   # Import the Twilio client

class Frontend:
    def __init__(self, memory, llm, twilio_client):
        self.memory = memory
        self.llm = llm
        self.twilio_client = twilio_client

        if "conversation" not in st.session_state:
            st.session_state.conversation = self.memory.load_conversation()

    def get_messages_with_contact(self, contact_name):
        """Retrieve previous text messages from a specific contact."""
        try:
            messages = self.twilio_client.messages.list()
            contact_messages = []

            for message in messages:
                # Check if contact_name is part of the from or to field
                if contact_name in message.from_ or contact_name in message.to:
                    contact_messages.append((message.direction, message.body))

            return contact_messages
        except Exception as e:
            st.error(f"Error retrieving messages: {e}")
            return []

    def run(self):
        st.title("Chatbot Simulation with Contacts")
        st.write("Enter the name of a contact to simulate a conversation.")

        if "conversation" not in st.session_state:
            st.session_state.conversation = []  # Initialize conversation history

        contact_name = st.text_input("Enter the contact name:")

        if st.button("Get Messages") and contact_name:
            # Retrieve messages from the contact
            messages = self.get_messages_with_contact(contact_name)

            # Add messages to conversation history
            for direction, msg in messages:
                role = "user" if direction == "incoming" else contact_name
                if (role, msg) not in st.session_state.conversation:
                    st.session_state.conversation.append((role, msg))

            if messages:
                st.success("Messages retrieved. You can now simulate a response.")
            else:
                st.warning("No messages found for this contact.")

            user_message = st.text_input("What message would this contact send?")

            if st.button("Get Response") and user_message:
                # Generate a response based on the user's message
                response = self.llm.get_response(st.session_state.conversation, user_message)
                st.write(f"**Chatbot Response:** {response}")
                # Append the new user message and bot response to the conversation history
                st.session_state.conversation.append(("user", user_message))
                st.session_state.conversation.append((contact_name, response))
                self.memory.save_conversation(st.session_state.conversation)
        else:
            st.write("Please enter a contact name and retrieve messages.")
