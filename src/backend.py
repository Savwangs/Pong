import sqlite3
import random
from src.llm import LLM
from src.memory import Memory

class Backend:
    def __init__(self):
        self.llm = LLM()
        self.memory = Memory()
        self.db_connection = None
        self.db_cursor = None
        self.connect_to_database()

    def connect_to_database(self):
        try:
            self.db_connection = sqlite3.connect('messages.db')
            self.db_cursor = self.db_connection.cursor()
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")

    def get_response(self, name, user_text):
        sanitized_name = name.strip().lower()
        conversation = self.get_messages_for_name(sanitized_name)

        if not conversation:
            return f"Sorry, I don't have any message history with {name}. Let's start a new conversation!"

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
        WHERE chat_session = ? OR sender_name = ?
        ORDER BY message_date ASC
        LIMIT 100
        """
        try:
            self.db_cursor.execute(query, (name, name))
            messages = self.db_cursor.fetchall()

            return [{
                "direction": "inbound" if m[0] == name else "outbound",
                "content": m[1],
                "timestamp": m[2]
            } for m in messages]
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return []

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()