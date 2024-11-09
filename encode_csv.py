import base64
import os

def encode_file(filepath):
    """Encode a file as base64"""
    with open(filepath, 'rb') as file:
        return base64.b64encode(file.read()).decode('utf-8')

def main():
    # Get all CSV files in the current directory
    csv_files = [f for f in os.listdir('.') if f.endswith('_messages.csv')]
    
    print("Copy the following into your Streamlit secrets:")
    print("\n```toml")
    
    # Encode and print each file
    for filename in csv_files:
        try:
            encoded = encode_file(filename)
            secret_key = filename.upper().replace('.CSV', '').replace('-', '_')
            print(f'{secret_key} = "{encoded}"')
        except Exception as e:
            print(f"Error encoding {filename}: {e}")
    
    print("```")

if __name__ == "__main__":
    main()