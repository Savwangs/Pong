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

def safe_get(row, key, default=None):
    """Safely get a value from the row with a default if the key doesn't exist"""
    try:
        return row[key] if row[key] is not None else default
    except KeyError:
        print(f"Warning: Column '{key}' not found in CSV. Using default value.")
        return default

def parse_date(date_str):
    """Safely parse a date string, returning None if invalid"""
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

    create_table()
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()

    try:
        # First, clear existing messages to avoid duplicates
        cursor.execute("DELETE FROM messages")
        conn.commit()
        print("Cleared existing messages from database")

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            # Read the first line to get column names
            first_line = file.readline().strip()
            columns = [col.strip() for col in first_line.split(',')]
            print(f"Found columns: {columns}")
            
            # Reset file pointer
            file.seek(0)
            csv_reader = csv.DictReader(file)
            
            row_count = 0
            for row in csv_reader:
                try:
                    # Get values with safe defaults
                    chat_session = safe_get(row, 'Chat Session', '').strip()
                    message_date = parse_date(safe_get(row, 'Message Date'))
                    delivered_date = parse_date(safe_get(row, 'Delivered Date'))
                    read_date = parse_date(safe_get(row, 'Read Date'))
                    service = safe_get(row, 'Service', '')
                    type_ = safe_get(row, 'Type', '')
                    sender_id = safe_get(row, 'Sender ID', '').strip()
                    sender_name = safe_get(row, 'Sender Name', '').strip()
                    status = safe_get(row, 'Status', '')
                    replying_to = safe_get(row, 'Replying to', '')  # Note: Changed from 'Replying To'
                    subject = safe_get(row, 'Subject', '')
                    content = safe_get(row, 'Text', '')
                    attachment = safe_get(row, 'Attachment', '')
                    attachment_type = safe_get(row, 'Attachment Type', '')

                    if not message_date:
                        print(f"Skipping row {row_count + 1}: Missing message date")
                        continue

                    cursor.execute("""
                    INSERT INTO messages (
                        chat_session, message_date, delivered_date, read_date, edited_date,
                        service, type, sender_id, sender_name, status, replying_to,
                        subject, content, attachment, attachment_type
                    ) VALUES (?, ?, ?, ?, NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        chat_session, message_date, delivered_date, read_date,
                        service, type_, sender_id, sender_name, status, replying_to,
                        subject, content, attachment, attachment_type
                    ))
                    
                    row_count += 1
                    if row_count % 100 == 0:  # Progress update every 100 rows
                        print(f"Processed {row_count} messages...")
                
                except Exception as e:
                    print(f"Warning: Error processing row {row_count + 1}: {str(e)}")
                    continue

            conn.commit()
            
            # Verify import
            cursor.execute("SELECT COUNT(*) FROM messages")
            final_count = cursor.fetchone()[0]
            print(f"\nImport completed successfully:")
            print(f"Total messages imported: {final_count}")
            
            # Show sample message
            cursor.execute("""
                SELECT chat_session, sender_name, content 
                FROM messages 
                LIMIT 1
            """)
            sample = cursor.fetchone()
            if sample:
                print("\nSample message:")
                print(f"Chat: {sample[0]}")
                print(f"Sender: {sample[1] or 'Savir'}")
                print(f"Content: {sample[2][:50]}...")

    except Exception as e:
        print(f"Error during import process: {str(e)}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_files = [
        'bro_messages.csv',
        'mom_messages.csv',
        'dad_messages.csv',
        'pranav_messages.csv',
        'adan_messages.csv',
        'aryan_messages.csv'
    ]
    for csv_file in csv_files:
        csv_file_path = os.path.join(script_dir, csv_file)
        print(f"Importing {csv_file}...")
        import_messages(csv_file_path)