import os
import base64
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

def initialize_database():
    """Initialize database with messages from CSV files"""
    data_dir = './data'
    os.makedirs(data_dir, exist_ok=True)
    
    create_table()
    
    @st.cache_resource
    def load_database():
        import sqlite3
        conn = sqlite3.connect('messages.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM messages")
        count = cursor.fetchone()[0]
        conn.close()
        
        if count == 0:
            print("Database empty, importing messages...")
            
            csv_mappings = {
                'bro_messages.csv': 'BRO_MESSAGES',
                'mom_messages.csv': 'MOM_MESSAGES',
                'dad_messages.csv': 'DAD_MESSAGES',
                'pranav_messages.csv': 'PRANAV_MESSAGES',
                'adan_messages.csv': 'ADAN_MESSAGES',
                'aryan_messages.csv': 'ARYAN_MESSAGES'
            }
            
            for filename, secret_key in csv_mappings.items():
                try:
                    if secret_key in st.secrets:
                        print(f"Found encoded content for {filename}")
                        if decode_and_save_csv(st.secrets[secret_key], filename, data_dir):
                            csv_path = os.path.join(data_dir, filename)
                            import_messages(csv_path)
                            os.remove(csv_path)
                    else:
                        print(f"Warning: No encoded content found for {filename}")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")
        else:
            print(f"Database already contains {count} messages. Skipping import.")
    
    load_database()

def main():
    st.set_page_config(page_title="Savir Bot", page_icon="🤖")
    initialize_database()
    frontend = Frontend()
    frontend.run()

if __name__ == "__main__":
    main()