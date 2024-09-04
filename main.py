from src.memory import Memory
from src.llm import LLM
from src.frontend import Frontend
import os
from dotenv import load_dotenv
import requests

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

try:
    response = requests.get("https://api.openai.com")
    if response.status_code == 200:
        print("API is accessible")
    else:
        print("Failed to access API")
except requests.ConnectionError:
    print("Network issue: Unable to connect to OpenAI API")

# Instantiate the classes
memory = Memory()
llm = LLM(api_key=OPENAI_API_KEY)
frontend = Frontend(memory=memory, llm=llm)

# Run the frontend to start the chatbot
if __name__ == "__main__":
    frontend.run()



        
