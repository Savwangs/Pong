import os
import openai

class LLM:
    def __init__(self):
        openai.api_key = os.environ['OPENAI_API_KEY']

    def get_response(self, context):
        try:
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=context,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error in getting LLM response: {e}")
            return "I'm sorry, I couldn't generate a response at the moment."