import os
import streamlit as st
from src.frontend import Frontend
from import_messages import create_table, import_messages

def initialize_database():
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    create_table()
    csv_files = [
        'bro_messages.csv',
        'mom_messages.csv',
        'dad_messages.csv',
        'pranav_messages.csv',
        'adan_messages.csv',
        'aryan_messages.csv'
    ]
    
    @st.cache_resource
    def load_database():
        for csv_file in csv_files:
            csv_file_path = os.path.join(data_dir, csv_file)
            if os.path.exists(csv_file_path):
                print(f"Importing {csv_file}...")
                import_messages(csv_file_path)
            else:
                print(f"Warning: {csv_file} not found. Skipping...")
    
    load_database()

def main():
    st.set_page_config(page_title="Savir Bot", page_icon="🤖")
    initialize_database()
    frontend = Frontend()
    frontend.run()

if __name__ == "__main__":
    main()