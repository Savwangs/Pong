import sqlite3
import csv
from datetime import datetime

def import_messages(csv_file_path):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    with open(csv_file_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            sender = row['From']
            recipient = row['To']
            content = row['Text']
            timestamp = datetime.strptime(row['Date'], '%Y-%m-%d %H:%M:%S')
            
            cursor.execute("""
            INSERT INTO messages (sender, recipient, content, timestamp)
            VALUES (?, ?, ?, ?)
            """, (sender, recipient, content, timestamp))

    conn.commit()
    conn.close()

# Replace with the actual path to your exported CSV file
import_messages('/Users/savirwangoo/Documents/Introduction/Messages/Messages - 25 chat sessions.csv') 