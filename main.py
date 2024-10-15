from src.memory import Memory
from src.llm import LLM
from src.frontend import Frontend
import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID","")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN","")
TWILIO_PHONE_NUMBER = os.environ.get("TWILIO_PHONE_NUMBER","")

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Instantiate the classes
memory = Memory()
llm = LLM(api_key=OPENAI_API_KEY)
frontend = Frontend(memory=memory, llm=llm, twilio_client = twilio_client)

# Run the frontend to start the chatbot
if __name__ == "__main__":
    frontend.run()


        
