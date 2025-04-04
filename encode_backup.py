import zipfile
import base64
import argparse

def encode_and_compress_backup(input_file='decoded_backup.json', output_file='backup.daylio'):
    try:
        # Read the JSON content
        with open(input_file, 'r', encoding='utf-8') as f:
            json_content = f.read()
        
        # Step 1: Encode to Base64
        encoded_bytes = base64.b64encode(json_content.encode('utf-8'))
        
        # Step 2: Create a ZIP file with the encoded content
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            # Add the encoded content to the ZIP file
            zip_ref.writestr('backup.daylio', encoded_bytes)
        
        print(f"Successfully encoded and compressed backup to {output_file}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Encode and compress Daylio backup file')
    parser.add_argument('input_file', help='Path to the input JSON file (default: decoded_backup.json)')
    parser.add_argument('-o', '--output', help='Path to the output backup file (default: backup.daylio)')
    
    args = parser.parse_args()
    output_file = args.output if args.output else 'backup.daylio'
    encode_and_compress_backup(args.input_file, output_file) 