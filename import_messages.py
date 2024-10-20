import sqlite3
import csv
from datetime import datetime

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
        service TEXT,
        type TEXT,
        sender_id TEXT,
        sender_name TEXT,
        status TEXT,
        content TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def import_messages(csv_file_path):
    create_table()
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)

        for row in csv_reader:
            chat_session = row['Chat Session']
            message_date = datetime.strptime(row['Message Date'], '%Y-%m-%d %H:%M:%S')
            delivered_date = datetime.strptime(row['Delivered Date'], '%Y-%m-%d %H:%M:%S') if row['Delivered Date'] else None
            read_date = datetime.strptime(row['Read Date'], '%Y-%m-%d %H:%M:%S') if row['Read Date'] else None
            service = row['Service']
            type = row['Type']
            sender_id = row['Sender ID']
            sender_name = row['Sender Name']
            status = row['Status']
            content = row['Text']

            cursor.execute("""
            INSERT INTO messages (chat_session, message_date, delivered_date, read_date, service, type, sender_id, sender_name, status, content)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (chat_session, message_date, delivered_date, read_date, service, type, sender_id, sender_name, status, content))

    conn.commit()
    conn.close()

# Replace with the actual path to your exported CSV file
import_messages('/Users/savirwangoo/Documents/Introduction/messages.csv')