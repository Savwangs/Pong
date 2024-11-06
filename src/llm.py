import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

class LLM:
    def __init__(self):
        try:
            api_key = st.secrets["OPENAI_API_KEY"]
        except Exception:
            load_dotenv()
            api_key = os.getenv('OPENAI_API_KEY')
            
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables or Streamlit secrets")
            
        self.client = OpenAI(api_key=api_key)

    def get_response(self, context):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Savir's personal chatbot. Your responses should exactly "
                                 "match Savir's texting style based on the conversation history provided. "
                                 "Keep responses casual and natural, matching the tone and length of "
                                 "Savir's previous messages."
                    },
                    {"role": "user", "content": context}
                ],
                max_tokens=150,
                temperature=0.7,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error getting LLM response: {e}")
            return "Sorry, I'm having trouble generating a response right now. Can you try again?"