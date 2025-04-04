import base64
import argparse
import zipfile

def decode_backup(input_file='backup.daylio', output_file='decoded_backup.json'):
    try:
        # First unzip the .daylio file
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            # Get the first (and only) file in the zip
            file_list = zip_ref.namelist()
            if not file_list:
                raise ValueError("No files found in the zip archive")
            
            # Read the Base64 content from the unzipped file
            base64_content = zip_ref.read(file_list[0]).decode('utf-8').strip()
        
        # Decode the Base64 string
        decoded_bytes = base64.b64decode(base64_content)
        decoded_string = decoded_bytes.decode('utf-8')
        
        # Write the decoded content to a JSON file
        with open(output_file, 'w') as f:
            f.write(decoded_string)
        
        print(f"Successfully decoded and saved to {output_file}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Decode Daylio backup file')
    parser.add_argument('input_file', help='Path to the input backup file (default: backup.daylio)')
    parser.add_argument('-o', '--output', help='Path to the output JSON file (default: decoded_backup.json)')
    
    args = parser.parse_args()
    output_file = args.output if args.output else 'decoded_backup.json'
    decode_backup(args.input_file, output_file) 