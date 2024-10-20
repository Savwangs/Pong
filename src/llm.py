import os
from openai import OpenAI
from dotenv import load_dotenv

class LLM:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def get_response(self, context):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Savir. Respond to the message based on the conversation history provided, precisely mimicking Savir's personal communication style with this specific contact."},
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
            return "I'm having trouble generating a response right now. Can you try again?"