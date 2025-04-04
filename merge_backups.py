import json
import time
import csv
from datetime import datetime as dt

def load_tag_mappings(mapping_file='tag_mappings.csv'):
    """Load tag mappings from CSV file"""
    tag_mappings = {}
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tag_mappings[row['pixels_tag']] = row['daylio_tag']
    except (FileNotFoundError, csv.Error):
        return {}
    return tag_mappings

def load_keyword_mappings(mapping_file='keyword_mappings.csv'):
    """Load keyword to tag mappings from CSV file"""
    keyword_mappings = {}
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                keyword = row['keyword'].lower()
                if keyword not in keyword_mappings:
                    keyword_mappings[keyword] = []
                keyword_mappings[keyword].append(row['daylio_tag'])
    except (FileNotFoundError, csv.Error):
        return {}
    return keyword_mappings

def find_tags_from_keywords(note, keyword_mappings, daylio_tags, daylio_tag_groups, existing_tag_ids=None):
    """Find Daylio tags based on keywords in the note"""
    tag_ids = []
    if not note or not keyword_mappings:
        return tag_ids
        
    note_lower = note.lower()
    existing_tag_ids = existing_tag_ids or []
    
    for keyword, tag_names in keyword_mappings.items():
        if keyword in note_lower:
            for tag_name in tag_names:
                # Find the tag in Daylio tags
                tag = next((t for t in daylio_tags if t["name"] == tag_name), None)
                if tag and tag["id"] not in existing_tag_ids and tag["id"] not in tag_ids:
                    tag_ids.append(tag["id"])
    
    return tag_ids

def parse_pixels_date(date_str):
    """Convert Pixels date string to Daylio datetime components"""
    date = dt.strptime(date_str, "%Y-%m-%d")
    return {
        "year": date.year,
        "month": date.month - 1,  # Convert to 0-based month (0-11)
        "day": date.day,
        "hour": 22,  # Default to 10 PM as per Daylio example
        "minute": 0,
        "datetime": int(time.mktime(date.replace(hour=22, minute=0).timetuple()) * 1000),
        "timeZoneOffset": -14400000  # Default timezone offset
    }

def convert_pixels_tags(pixels_tags, daylio_tags, daylio_tag_groups, tag_mappings=None):
    """Convert Pixels tags to Daylio tag IDs"""
    tag_ids = []
    if tag_mappings is None:
        tag_mappings = {}
    
    for tag_group in pixels_tags:
        group_name = tag_group["type"]
        # Find matching tag group in Daylio
        group = next((g for g in daylio_tag_groups if g["name"] == group_name), None)
        if not group:
            continue
            
        for tag_name in tag_group["entries"]:
            # Check if there's a mapping for this tag
            mapped_name = tag_mappings.get(tag_name, tag_name)
            
            # Find matching tag in Daylio
            tag = next((t for t in daylio_tags if t["name"] == mapped_name and t["id_tag_group"] == group["id"]), None)
            if tag:
                tag_ids.append(tag["id"])
    
    return tag_ids

def merge_backups(pixels_file, daylio_file, output_file):
    try:
        # Load mappings
        tag_mappings = load_tag_mappings()
        keyword_mappings = load_keyword_mappings()
        
        # Read Pixels backup
        with open(pixels_file, 'r', encoding='utf-8') as f:
            pixels_data = json.load(f)
            
        # Read Daylio backup
        with open(daylio_file, 'r', encoding='utf-8') as f:
            daylio_data = json.load(f)
            
        # Get the next available entry ID
        next_entry_id = max(entry["id"] for entry in daylio_data["dayEntries"]) + 1 if daylio_data["dayEntries"] else 1
        
        # Convert Pixels entries to Daylio format
        for entry in pixels_data:
            if entry["type"] != "Mood":
                continue
                
            # Parse date
            date_info = parse_pixels_date(entry["date"])
            
            # Convert tags from Pixels tags
            tag_ids = convert_pixels_tags(
                entry["tags"],
                daylio_data["tags"],
                daylio_data["tag_groups"],
                tag_mappings
            )
            
            # Add tags from keywords in the note
            if entry["notes"]:
                keyword_tag_ids = find_tags_from_keywords(
                    entry["notes"],
                    keyword_mappings,
                    daylio_data["tags"],
                    daylio_data["tag_groups"],
                    tag_ids  # Pass existing tag IDs to prevent duplicates
                )
                tag_ids.extend(keyword_tag_ids)
            
            # Create Daylio entry
            daylio_entry = {
                "assets": [],
                "datetime": date_info["datetime"],
                "day": date_info["day"],
                "hour": date_info["hour"],
                "id": next_entry_id,
                "isFavorite": False,
                "minute": date_info["minute"],
                "month": date_info["month"],
                "mood": 6 - entry["scores"][0],  # Invert mood scale (1-5 -> 5-1)
                "note": entry["notes"].replace("\n", "<br>") if entry["notes"] else "",  # Replace \n with <br>
                "note_title": "",
                "tags": tag_ids,
                "timeZoneOffset": date_info["timeZoneOffset"],
                "year": date_info["year"]
            }
            
            # Add to Daylio entries
            daylio_data["dayEntries"].append(daylio_entry)
            next_entry_id += 1
            
        # Update metadata
        daylio_data["metadata"]["number_of_entries"] = len(daylio_data["dayEntries"])
        daylio_data["metadata"]["created_at"] = int(time.time() * 1000)
        
        # Save merged backup
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(daylio_data, f, indent=4)
            
        print(f"Successfully merged backups. Output written to: {output_file}")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge Pixels backup into Daylio backup')
    parser.add_argument('pixels_file', help='Path to Pixels backup JSON file')
    parser.add_argument('daylio_file', help='Path to Daylio backup JSON file')
    parser.add_argument('-o', '--output', help='Path to output merged JSON file (optional)')
    
    args = parser.parse_args()
    
    # If no output file specified, use input filename with '_merged' suffix
    output_file = args.output or args.daylio_file.rsplit('.', 1)[0] + '_merged.json'
    
    merge_backups(args.pixels_file, args.daylio_file, output_file) 