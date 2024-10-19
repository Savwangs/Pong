import json

class Memory:
    def __init__(self, file_name="conversation_log.json"):
        self.file_name = file_name

    def prepare_context(self, name, twilio_number, sample_messages, user_text):
        context = f"You are Savir, responding to a message from {name}. Here are some recent messages from your conversation:\n\n"
        
        # This part builds the conversation history from sample_messages
        for msg in sample_messages:
            if msg['direction'] == 'inbound':
                context += f"{name}: {msg['content']}\n"
            else:
                context += f"You (Savir): {msg['content']}\n"
        
        # This adds the new message from the user
        context += f"\nNow, {name} has sent this new message: '{user_text}'\n"
        
        # This is the instruction for the AI to respond
        context += "Respond to this message as Savir would, based on the conversation history shown above: "
        
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