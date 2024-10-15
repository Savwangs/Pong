import json
import os
from twilio.rest import Client
from src.llm import LLM
from src.memory import Memory

class Backend:
    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()
        self.twilio_client = Client(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])
        self.twilio_number = os.environ['TWILIO_PHONE_NUMBER']
        self.name_to_phone = self.load_name_to_phone()

    def load_name_to_phone(self):
        try:
            with open('name_to_phone.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def find_messages_for_name(self, name):
        phone_number = self.name_to_phone.get(name)
        if not phone_number:
            return {"Savir": [], "User": []}

        # Fetch messages from Twilio
        messages = self.twilio_client.messages.list(to=self.twilio_number, from_=phone_number)
        conversation = {"Savir": [], "User": []}
        
        for message in messages[:15]:  # Limit to last 15 messages
            if message.direction == 'inbound':
                conversation["User"].append(message.body)
            else:
                conversation["Savir"].append(message.body)

        # Save to conversation_history.json
        with open('conversation_history.json', 'w') as f:
            json.dump(conversation, f)

        return conversation

    def get_most_relevant_given_text(self, name, user_text):
        # Load conversation history
        conversation = self.find_messages_for_name(name)

        # Prepare context for LLM
        context = f"Previous conversation with {name}:\n"
        for i in range(min(len(conversation['Savir']), len(conversation['User']))):
            context += f"{name}: {conversation['User'][i]}\n"
            context += f"Savir: {conversation['Savir'][i]}\n"
        
        context += f"\n{name}: {user_text}\nSavir:"

        # Get response from LLM
        response = self.llm.get_response(context)

        # Save the new interaction
        self.memory.save_interaction(name, user_text, response)

        return response