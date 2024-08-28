import os
import json

class Memory:
    def __init__(self, conversation_file="conversation_history.json"):
        self.conversation_file = conversation_file

    def save_conversation(self, conversation):
        """Save the conversation to a JSON file."""
        with open(self.conversation_file, "w") as file:
            json.dump(conversation, file)

    def load_conversation(self):
        """Load the conversation from a JSON file, if it exists and is not empty."""
        if os.path.exists(self.conversation_file):
            try:
                with open(self.conversation_file, "r") as file:
                    if os.path.getsize(self.conversation_file) > 0:
                        return json.load(file)
            except json.JSONDecodeError:
                return []
        return []
