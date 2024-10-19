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
            return f"Sorry, I don't have a contact named {name}."
    
        phone_number = self.name_to_phone[sanitized_name]
        conversation = self.get_messages_for_name(sanitized_name, phone_number)
    
        if not conversation:
            return f"I don't have any message history with {name}."
    
        sample_messages = random.sample(conversation, min(15, len(conversation)))
        sample_messages.sort(key=lambda m: m['date'])
    
        context = self.memory.prepare_context(name, self.twilio_number, sample_messages, user_text)
        response = self.llm.get_response(context)
        self.memory.save_interaction(name, user_text, response)
        return response

    def get_messages_for_name(self, name, phone_number):
        try:
        # Fetch messages between the twilio number and the user's phone number
            messages = self.twilio_client.messages.list(
                to=self.twilio_number, from_=phone_number
            ) + self.twilio_client.messages.list(
                from_=self.twilio_number, to=phone_number
            )

            for m in messages:
                print(f"Message from {m.from_} to {m.to}: {m.body} at {m.date_sent}")

            if not messages:
                print("No messages found")
        
            # Sort by date
            messages.sort(key=lambda m: m.date_sent)

            # Return messages in a format your system understands
            return [{
                "direction": "inbound" if m.from_ == phone_number else "outbound",
                "content": m.body,
                "date": m.date_sent
            } for m in messages]
        
        except Exception as e:
            print(f"Error fetching messages for {name}: {e}")
            return []