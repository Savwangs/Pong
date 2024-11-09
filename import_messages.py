import sqlite3
import csv
from datetime import datetime
import os

def create_table():
    """Create the messages table if it doesn't exist and clear existing data"""
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
    
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    print("Database initialized and cleared")

def safe_get(row, key, default=None):
    try:
        return row[key] if row[key] is not None else default
    except KeyError:
        print(f"Warning: Column '{key}' not found in CSV. Using default value.")
        return default

def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        print(f"Warning: Could not parse date '{date_str}'. Using None.")
        return None

def import_messages(csv_file_path):
    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file not found at {csv_file_path}")
        return

    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    try:
        chat_session = os.path.basename(csv_file_path).replace('_messages.csv', '')
        print(f"Importing messages for chat session: {chat_session}")

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            
            row_count = 0
            for row in csv_reader:
                try:
                    message_date = parse_date(safe_get(row, 'Message Date'))
                    delivered_date = parse_date(safe_get(row, 'Delivered Date'))
                    read_date = parse_date(safe_get(row, 'Read Date'))
                    service = safe_get(row, 'Service', '')
                    type_ = safe_get(row, 'Type', '')
                    sender_id = safe_get(row, 'Sender ID', '').strip()
                    sender_name = safe_get(row, 'Sender Name', '').strip()
                    status = safe_get(row, 'Status', '')
                    replying_to = safe_get(row, 'Replying to', '')
                    subject = safe_get(row, 'Subject', '')
                    content = safe_get(row, 'Text', '')
                    attachment = safe_get(row, 'Attachment', '')
                    attachment_type = safe_get(row, 'Attachment Type', '')

                    if not message_date:
                        print(f"Skipping row {row_count + 1}: Missing message date")
                        continue

                    cursor.execute("""
                    INSERT INTO messages (
                        chat_session, message_date, delivered_date, read_date,
                        edited_date, service, type, sender_id, sender_name,
                        status, replying_to, subject, content, attachment,
                        attachment_type
                    ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        chat_session, message_date, delivered_date, read_date,
                        service, type_, sender_id, sender_name, status,
                        replying_to, subject, content, attachment, attachment_type
                    ))
                    
                    row_count += 1
                    if row_count % 100 == 0:
                        print(f"Processed {row_count} messages...")
                
                except Exception as e:
                    print(f"Warning: Error processing row {row_count + 1}: {str(e)}")
                    continue

            conn.commit()
            print(f"\nSuccessfully imported {row_count} messages for {chat_session}")

    except Exception as e:
        print(f"Error during import process: {str(e)}")
        conn.rollback()
    finally:
        try:
            cursor.execute("SELECT chat_session, COUNT(*) FROM messages GROUP BY chat_session")
            results = cursor.fetchall()
            print("\nCurrent database status:")
            for chat_session, count in results:
                print(f"{chat_session}: {count} messages")
        except:
            pass
        conn.close()