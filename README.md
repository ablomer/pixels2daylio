# Pixels to Daylio Backup Merge

A Python tool to merge Pixels app backup file into existing Daylio backup file.

## Features

- Merge Pixels backup file into Daylio backup file
- Support for tag mapping between Pixels and Daylio

## Prerequisites

- Python 3.x
- Required Python packages:
  - None (uses standard library only)

## Usage

### 1. Decode Daylio Backup

First, decode your Daylio backup file into a readable JSON format:

```bash
python decode_backup.py your_backup.daylio -o decoded_daylio.json
```

### 2. Merge Pixels Backup

Merge your Pixels backup into the decoded Daylio backup:

```bash
python merge_backups.py pixels_backup.json decoded_daylio.json -o merged_backup.json
```

### 3. Encode Back to Daylio Format

Encode the merged backup back into Daylio format:

```bash
python encode_backup.py merged_backup.json -o final_backup.daylio
```

### Optional: Format JSON Files

To make the JSON files more readable, you can use the format script:

```bash
python format_json.py input.json -o formatted.json
```

## Tag Mapping

The tool supports mapping Pixels tags to Daylio tags using a CSV file (`tag_mappings.csv`). The format should be:

```csv
pixels_tag,daylio_tag
```

For example:
```csv
pixels_tag,daylio_tag
Work,Job
Exercise,Sports
```

### Keyword Mappings

Create a `keyword_mappings.csv` file to automatically add tags based on note content:
```csv
keyword,daylio_tag
work,Work
gym,Exercise
```

## File Structure

- `decode_backup.py`: Decodes Daylio backup files
- `merge_backups.py`: Merges Pixels backup into Daylio format
- `encode_backup.py`: Encodes JSON back into Daylio backup format
- `format_json.py`: Formats JSON files for better readability
- `tag_mappings.csv`: Maps Pixels tags to Daylio tags

## Notes

- The tool preserves mood ratings, notes, and tags
- Newline characters in notes are converted to HTML line breaks
- All entries are set to 10 PM by default (Daylio's example time)
- The tool maintains the original Daylio backup structure while adding new entries
