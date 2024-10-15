import json

class Memory:
    def __init__(self, file_name="conversation_log.json"):
        self.file_name = file_name

    def save_interaction(self, name, user_text, response):
        try:
            # Load existing data
            try:
                with open(self.file_name, 'r') as f:
                    data = json.load(f)
            except FileNotFoundError:
                data = {}

            # Append new interaction
            if name not in data:
                data[name] = []
            data[name].append({
                "user_text": user_text,
                "response": response
            })

            # Save updated data
            with open(self.file_name, 'w') as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error in saving interaction: {e}")

    def load_interactions(self, name):
        try:
            with open(self.file_name, 'r') as f:
                data = json.load(f)
            return data.get(name, [])
        except FileNotFoundError:
          

  return []
        except Exception as e:
            print(f"Error in loading interactions: {e}")
            return []