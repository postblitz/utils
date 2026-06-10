import os
import json
import string
from datetime import datetime
from ctypes import windll

def get_drives():
    """Returns a list of active drive letters in Windows."""
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_lowercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives

def get_file_properties(file_entry):
    """Fetches size and modification time for a file, handling permission issues."""
    try:
        stat = file_entry.stat(follow_symlinks=False)
        return {
            "size_bytes": stat.st_size,
            "modification_time": datetime.fromtimestamp(stat.st_mtime).isoformat()
        }
    except PermissionError:
        return "ACCESS_DENIED"

def scan_directory(path):
    """
    Recursively scans a directory and builds a hierarchical list 
    of its contents with file metadata and error handling.
    """
    folder_contents = []
    
    try:
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir(follow_symlinks=False):
                    try:
                        # Recursively scan the subfolder
                        sub_content = scan_directory(entry.path)
                        folder_contents.append({entry.name: sub_content})
                    except PermissionError:
                        folder_contents.append({entry.name: "ACCESS_DENIED"})
                
                elif entry.is_file(follow_symlinks=False):
                    # Fetch file properties or assign ACCESS_DENIED if restricted
                    properties = get_file_properties(entry)
                    folder_contents.append({entry.name: properties})
                    
    except PermissionError:
        # If the parent directory itself cannot be opened
        return "ACCESS_DENIED"
    
    return folder_contents

def main():
    print("Detecting system drives...")
    drives = get_drives()
    print(f"Found drives: {', '.join(drives)}")
    
    for drive in drives:
        drive_letter = drive[0].lower() # e.g., "c"
        output_file = f"drive_{drive_letter}.json"
        
        print(f"\nScanning drive {drive_letter.upper()}:... (Writing to {output_file})")
        
        # Scan the drive root
        drive_data = {drive_letter: scan_directory(drive)}
        
        # Save this specific drive's JSON immediately to save memory
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(drive_data, f, indent=4, ensure_ascii=False)
            
    print("\nAll drives scanned successfully!")

if __name__ == "__main__":
    main()