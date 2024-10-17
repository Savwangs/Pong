import json

class Memory:
    def __init__(self, file_name="conversation_log.json"):
        self.file_name = file_name

    def prepare_context(self, name, twilio_number, sample_messages, user_text):
        context = f"You are an AI assistant named Savir, helping the owner of the phone number {twilio_number} respond to a message from {name}. Here are some random messages from their actual phone conversation:\n\n"
        
        for msg in sample_messages:
            if msg['direction'] == 'inbound':
                context += f"{name}: {msg['content']}\n"
            else:
                context += f"You: {msg['content']}\n"
        
        context += f"\nNow, {name} has sent this new message: '{user_text}'\n"
        context += "Based on these actual phone messages and this new message, compose a response as if you were the owner of the phone number: "

        return context

    def save_interaction(self, name, user_text, response):
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        if name not in data:
            data[name] = []
        
        data[name].append({
            "user_text": user_text,
            "response": response
        })

        with open(self.file_name, 'w') as f:
            json.dump(data, f, indent=2)

    def load_interactions(self, name):
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
            return data.get(name, [])
        except FileNotFoundError:
            return []