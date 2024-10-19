import os
from openai import OpenAI
class LLM:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

    def get_response(self, context):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or another appropriate model
                messages=[
                    {"role": "system", "content": "You are Savir. Respond to the message based on the conversation history provided, mimicking Savir's communication style."},
                    {"role": "user", "content": context}
                ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in getting LLM response: {e}")
            return "I'm sorry, I couldn't generate a response at the moment. Error: " + str(e)