from twilio.rest import Client
from src.llm import LLM
from src.memory import Memory
import json
import os
import random

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
                return {name.strip().lower(): phone for name, phone in json.load(f).items()}
        except FileNotFoundError:
            return {}

    def get_response(self, name, user_text):
        sanitized_name = name.strip().lower()
        
        if sanitized_name not in self.name_to_phone:
            return f"Sorry, I don't have a contact named {sanitized_name.capitalize()}."

        phone_number = self.name_to_phone[sanitized_name]
        conversation = self.get_messages_for_name(sanitized_name, phone_number)

        if not conversation:
            return f"I don't have any message history with {sanitized_name.capitalize()}."

        # Use 15 recent messages
        sample_messages = random.sample(conversation, min(15, len(conversation)))
        sample_messages.sort(key=lambda m: m['date'])

        # Prepare context
        context = self.memory.prepare_context(sanitized_name, self.twilio_number, sample_messages, user_text)

        # Get LLM response
        response = self.llm.get_response(context)
        self.memory.save_interaction(sanitized_name, user_text, response)
        return response

    def get_messages_for_name(self, name, phone_number):
        try:
            inbound_msgs = self.twilio_client.messages.list(to=self.twilio_number, from_=phone_number)
            outbound_msgs = self.twilio_client.messages.list(from_=self.twilio_number, to=phone_number)
        except Exception as e:
            print(f"Error retrieving Twilio messages: {e}")
            return []

        messages = inbound_msgs + outbound_msgs
        messages.sort(key=lambda m: m.date_sent)

        # Build conversation history
        return [{"direction": "inbound" if m.from_ == phone_number else "outbound",
                 "content": m.body,
                 "date": m.date_sent} for m in messages]