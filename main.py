import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load .env file's variables into os.environ
load_dotenv()

# get our api key from os.environ
OPENAI_API_KEY=os.environ.get("OPENAI_API_KEY", "")

# create a client with our api key
client = OpenAI(api_key=OPENAI_API_KEY)

# Set your OpenAI API key directly in the code

def get_openai_response(prompt):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return completion.choices[0].message.content

# Streamlit app
st.title("OpenAI GPT-4o-mini Chatbot")
st.write("Interact with the GPT-4 chatbot by entering your prompt below.")


if "conversation" not in st.session_state:
    st.session_state.conversation = []

user_input = st.text_input("Enter your prompt:")

if st.button("Get Response"):
    if user_input:
        response = get_openai_response(user_input)
        st.session_state.conversation.append(("user", user_input))
        st.session_state.conversation.append(("bot", response))
    else:
        st.write("Please enter a prompt.")

for role, msg in st.session_state.conversation:
    if role == "user":
        st.write(f"**You:** {msg}")
    else:
        st.write(f"**Bot:** {msg}")

        
