import json
import sys
import argparse

def format_json(input_file, output_file=None):
    try:
        # Read the input JSON file
        with open(input_file, 'r') as f:
            data = json.load(f)
        
        # If no output file specified, use input filename with '_formatted' suffix
        if output_file is None:
            output_file = input_file.rsplit('.', 1)[0] + '_formatted.json'
        
        # Write the formatted JSON to the output file
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4, sort_keys=True)
        
        print(f"Successfully formatted JSON. Output written to: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in file '{input_file}'.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Format a JSON file for better readability')
    parser.add_argument('input_file', help='Path to the input JSON file')
    parser.add_argument('-o', '--output', help='Path to the output JSON file (optional)')
    
    args = parser.parse_args()
    format_json(args.input_file, args.output)

if __name__ == '__main__':
    main() 