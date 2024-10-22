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
            raise

    def get_response(self, name, user_text):
        sanitized_name = name.strip().lower()
        print(f"Getting response for user: {sanitized_name}")
        
        conversation = self.get_messages_for_name(sanitized_name)
        print(f"Found {len(conversation)} messages in history")

        if not conversation:
            return f"Sorry, I don't have any message history with {name}. Let's start a new conversation!"

        # Get a random sample of messages, but ensure we keep chronological order
        sample_size = min(15, len(conversation))
        sample_indices = sorted(random.sample(range(len(conversation)), sample_size))
        sample_messages = [conversation[i] for i in sample_indices]
        sample_messages.sort(key=lambda m: m['timestamp'])

        context = self.memory.prepare_context(name, sample_messages, user_text)
        response = self.llm.get_response(context)
        self.memory.save_interaction(name, user_text, response)
        return response

    def get_messages_for_name(self, name):
        query = """
        SELECT 
            COALESCE(sender_name, 'Savir') as sender_name,
            content,
            message_date,
            CASE 
                WHEN sender_name IS NULL OR sender_name = '' THEN 'outbound'
                ELSE 'inbound'
            END as direction
        FROM messages
        WHERE LOWER(chat_session) = ?
        ORDER BY message_date ASC
        """
        
        try:
            self.db_cursor.execute(query, (name,))
            messages = self.db_cursor.fetchall()
            
            print(f"Query returned {len(messages)} messages for {name}")
            
            return [{
                "direction": m[3],
                "content": m[1],
                "timestamp": m[2],
                "sender": m[0]
            } for m in messages]
        except sqlite3.Error as e:
            print(f"Database query error: {e}")
            return []

    def __del__(self):
        if self.db_connection:
            self.db_connection.close()