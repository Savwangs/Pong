from src.memory import Memory
from src.llm import LLM
from src.frontend import Frontend
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variables
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

# Instantiate the classes
memory = Memory()
llm = LLM(api_key=OPENAI_API_KEY)
frontend = Frontend(memory=memory, llm=llm)

# Run the frontend to start the chatbot
if __name__ == "__main__":
    frontend.run()



        
