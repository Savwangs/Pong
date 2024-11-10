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
        """Establish database connection"""
        try:
            self.db_connection = sqlite3.connect('messages.db', check_same_thread=False)
            self.db_cursor = self.db_connection.cursor()
            
            # Verify database connection and content
            self.db_cursor.execute("SELECT DISTINCT chat_session FROM messages")
            available_sessions = self.db_cursor.fetchall()
            print(f"Available chat sessions: {[session[0] for session in available_sessions]}")
            
        except sqlite3.Error as e:
            print(f"Database connection error: {e}")
            raise

    def standardize_name(self, name):
        """Convert input name to standardized format"""
        lookup_name = name.strip().lower()
        return self.name_mapping.get(lookup_name, name.strip())

    def get_response(self, name, user_text):
        """Generate response based on chat history"""
        standardized_name = self.standardize_name(name)
        print(f"Getting response for user: {standardized_name}")
        
        # Get conversation history
        conversation = self.get_messages_for_name(standardized_name)
        print(f"Found {len(conversation)} messages in history")

        if not conversation:
            return f"Sorry, I don't have any message history with {standardized_name}. Let's start a new conversation!"

        # Sample messages for context
        sample_size = min(15, len(conversation))
        sample_indices = sorted(random.sample(range(len(conversation)), sample_size))
        sample_messages = [conversation[i] for i in sample_indices]
        sample_messages.sort(key=lambda m: m['timestamp'])

        # Generate and return response
        context = self.memory.prepare_context(standardized_name, sample_messages, user_text)
        response = self.llm.get_response(context)
        self.memory.save_interaction(standardized_name, user_text, response)
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
        """Clean up database connection"""
        if self.db_connection:
            try:
                self.db_connection.close()
            except:
                pass