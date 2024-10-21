import os
from src.frontend import Frontend
from import_messages import create_table, import_messages

def initialize_database():
    create_table()
    csv_file_path = os.path.join(os.path.dirname(__file__), 'messages.csv')
    if os.path.exists(csv_file_path):
        import_messages(csv_file_path)
    else:
        print("Warning: messages.csv not found. Starting with an empty database.")

def main():
    initialize_database()
    frontend = Frontend()
    frontend.run()

if __name__ == "__main__":
    main()