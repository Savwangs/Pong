import os
from src.frontend import Frontend
from import_messages import create_table, import_messages

def initialize_database():
    create_table()
    csv_files = [
        'bro_messages.csv',
        'mom_messages.csv',
        'dad_messages.csv',
        'pranav_messages.csv',
        'adan_messages.csv',
        'aryan_messages.csv'
    ]
    for csv_file in csv_files:
        csv_file_path = os.path.join(os.path.dirname(__file__), csv_file)
        if os.path.exists(csv_file_path):
            print(f"Importing {csv_file}...")
            import_messages(csv_file_path)
        else:
            print("Warning: messages.csv not found. Starting with an empty database.")

def main():
    initialize_database()
    frontend = Frontend()
    frontend.run()

if __name__ == "__main__":
    main()