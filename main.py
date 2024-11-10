import os
import base64
import sqlite3
import streamlit as st
from src.frontend import Frontend
from import_messages import create_table, import_messages

def decode_and_save_csv(encoded_content, filename, data_dir):
    """Decode base64 content and save as CSV"""
    try:
        decoded_content = base64.b64decode(encoded_content).decode('utf-8')
        filepath = os.path.join(data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(decoded_content)
        return True
    except Exception as e:
        print(f"Error saving {filename}: {e}")
        return False

@st.cache_resource
def initialize_database():
    """Initialize database with messages from CSV files"""
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Check if database exists and has data
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    create_table()
    
    # Check if database is empty
    cursor.execute("SELECT COUNT(*) FROM messages")
    count = cursor.fetchone()[0]
    
    if count == 0:
        st.write("Initializing database...")
        
        # Map CSV filenames to their secret keys
        csv_mappings = {
            'bro_messages.csv': ('Bro', 'BRO_MESSAGES'),
            'mom_messages.csv': ('Mom', 'MOM_MESSAGES'),
            'dad_messages.csv': ('Dad', 'DAD_MESSAGES'),
            'pranav_messages.csv': ('Pranav', 'PRANAV_MESSAGES'),
            'adan_messages.csv': ('Adan', 'ADAN_MESSAGES'),
            'aryan_messages.csv': ('Aryan', 'ARYAN_MESSAGES')
        }
        
        imported_files = []
        
        for filename, (chat_name, secret_key) in csv_mappings.items():
            try:
                if secret_key in st.secrets:
                    csv_path = decode_and_save_csv(st.secrets[secret_key], filename, data_dir)
                    if csv_path:
                        import_messages(csv_path)
                        imported_files.append(chat_name)
                        os.remove(csv_path)  # Clean up the temp file
            except Exception as e:
                st.error(f"Error processing {filename}: {e}")
        
        if imported_files:
            st.success(f"Successfully imported messages for: {', '.join(imported_files)}")
        
        # Verify imports
        cursor.execute("SELECT chat_session, COUNT(*) FROM messages GROUP BY chat_session")
        results = cursor.fetchall()
        for chat_session, msg_count in results:
            print(f"Imported {msg_count} messages for {chat_session}")
    
    conn.close()


def main():
    st.set_page_config(
        page_title="Savir Bot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize database before creating Frontend
    initialize_database()
    
    # Create and run frontend
    frontend = Frontend()
    frontend.run()

if __name__ == "__main__":
    main()