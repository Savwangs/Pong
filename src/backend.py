import sqlite3
import random
from src.llm import LLM
from src.memory import Memory
from import_messages import create_table

class Backend:
    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()
        self.db_connection = sqlite3.connect('messages.db')
        self.db_cursor = self.db_connection.cursor()
        create_table()

    def get_response(self, name, user_text):
        sanitized_name = name.strip().lower()
        conversation = self.get_messages_for_name(sanitized_name)

        if not conversation:
            return f"Sorry, I don't have any message history with {name}."

        sample_messages = random.sample(conversation, min(15, len(conversation)))
        sample_messages.sort(key=lambda m: m['timestamp'])

        context = self.memory.prepare_context(name, sample_messages, user_text)
        response = self.llm.get_response(context)
        self.memory.save_interaction(name, user_text, response)
        return response

    def get_messages_for_name(self, name):
        query = """
        SELECT sender_name, content, message_date
        FROM messages
        WHERE chat_session = ?
        ORDER BY message_date ASC
        LIMIT 100
        """
        # Execute the query where the chat_session is 'Bro'
        self.db_cursor.execute(query, (name,))
        messages = self.db_cursor.fetchall()

        # Now process the messages
        return [{
            # If the sender_name is empty, it's an outbound message from 'Savir'
            "direction": "inbound" if m[0] else "outbound",
            "content": m[1],  # Message content
            "timestamp": m[2]  # Message timestamp
        } for m in messages]
    
    def __del__(self):
        self.db_connection.close()