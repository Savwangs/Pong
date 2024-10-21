import sqlite3
import csv
from datetime import datetime
import os

def create_table():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_session TEXT,
        message_date DATETIME,
        delivered_date DATETIME,
        read_date DATETIME,
        edited_date DATETIME,
        service TEXT,
        type TEXT,
        sender_id TEXT,
        sender_name TEXT,
        status TEXT,
        replying_to TEXT,
        subject TEXT,
        content TEXT,
        attachment TEXT,
        attachment_type TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def import_messages(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"Warning: CSV file not found at {csv_file_path}")
        return

    create_table()
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)

            for row in csv_reader:
                chat_session = row['Chat Session']
                message_date = datetime.strptime(row['Message Date'], '%Y-%m-%d %H:%M:%S')
                delivered_date = datetime.strptime(row['Delivered Date'], '%Y-%m-%d %H:%M:%S') if row['Delivered Date'] else None
                read_date = datetime.strptime(row['Read Date'], '%Y-%m-%d %H:%M:%S') if row['Read Date'] else None
                edited_date = None  # As mentioned, this field is empty
                service = row['Service']
                type = row['Type']
                sender_id = row['Sender ID']
                sender_name = row['Sender Name'] if row['Sender Name'] else 'Savir'  # If empty, it's Savir
                status = row['Status']
                replying_to = row['Replying To']
                subject = row['Subject']
                content = row['Text']
                attachment = row['Attachment']
                attachment_type = row['Attachment Type']

                cursor.execute("""
                INSERT INTO messages (chat_session, message_date, delivered_date, read_date, edited_date, 
                                      service, type, sender_id, sender_name, status, replying_to, subject, 
                                      content, attachment, attachment_type)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (chat_session, message_date, delivered_date, read_date, edited_date, service, type, 
                      sender_id, sender_name, status, replying_to, subject, content, attachment, attachment_type))

        conn.commit()
        print("Messages imported successfully")
    except Exception as e:
        print(f"Error importing messages: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, 'messages.csv')
    import_messages(csv_file_path)