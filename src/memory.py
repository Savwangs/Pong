import json
import os

class Memory:
    def __init__(self, file_name="conversation_log.json"):
        self.file_name = file_name

    def prepare_context(self, name, sample_messages, user_text):
        context = f"You are Savir, responding to a message from {name}. Mimic Savir's personal communication style with {name} based on these recent messages:\n\n"
        
        for msg in sample_messages:
            if msg['direction'] == 'inbound':
                context += f"{name}: {msg['content']}\n"
            else:
                context += f"You (Savir): {msg['content']}\n"
        
        context += f"\nNow, {name} has sent this new message: '{user_text}'\n"
        context += f"Respond to this message as Savir would, maintaining your personal style of communication with {name}: "
        
        return context

    def save_interaction(self, name, user_text, response):
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
            else:
                data = {}

            if name not in data:
                data[name] = []
            data[name].append({
                "user_text": user_text,
                "response": response
            })

            with open(self.file_name, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving interaction: {e}")

    def load_interactions(self, name):
        try:
            if os.path.exists(self.file_name):
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
                return data.get(name, [])
            else:
                return []
        except Exception as e:
            print(f"Error loading interactions: {e}")
            return []