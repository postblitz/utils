import os
import json
import string
import math
from collections import defaultdict
from datetime import datetime

def load_json_data(file_path):
    print(f"Loading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_iso_time(time_str):
    try:
        return datetime.fromisoformat(time_str)
    except (ValueError, TypeError):
        return None

def get_log_time_cluster(days_old):
    if days_old <= 1:
        return "0 to 1 day old"
    lower_power = int(math.log2(days_old))
    upper_power = lower_power + 1
    start_days = 2 ** lower_power
    end_days = 2 ** upper_power
    
    if start_days >= 365:
        return f"{start_days//365} to {end_days//365} years old"
    elif start_days >= 30:
        return f"{start_days//30} to {end_days//30} months old"
    else:
        return f"{start_days} to {end_days} days old"

def analyze_hierarchy(contents, current_depth, path_prefix, stats, now):
    """
    Recursively processes the JSON structure, fixes the mathematical size bubble-up,
    and accurately preserves the access-denied tracking tree.
    """
    exclusive_files_size = 0
    total_subfolders_size = 0
    denied_tree = []

    if not isinstance(contents, list):
        return 0, "ACCESS_DENIED"

    for item in contents:
        if not isinstance(item, dict):
            continue
            
        for name, value in item.items():
            # Scenario A: It's a folder
            if isinstance(value, list):
                target_depth = current_depth
                
                # Apply the WinSxS flattening optimization
                if path_prefix == "Windows/WinSxS" and "_" in name:
                    prefix_part, rest_part = name.split("_", 1)
                    virtual_prefix = f"Windows/WinSxS/{prefix_part}"
                    target_depth = current_depth + 1
                    new_prefix = f"{virtual_prefix}/{rest_part}" if target_depth <= 3 else virtual_prefix
                else:
                    if current_depth <= 3:
                        new_prefix = f"{path_prefix}/{name}" if path_prefix else name
                    else:
                        new_prefix = path_prefix

                # Recurse down and capture the absolute total size of this child folder
                sub_total_size, sub_denied = analyze_hierarchy(value, current_depth + 1, new_prefix, stats, now)
                total_subfolders_size += sub_total_size
                
                # Attribute the sizes safely to the reporting buckets up to level 3
                if path_prefix == "Windows/WinSxS" and "_" in name:
                    virtual_prefix = f"Windows/WinSxS/{name.split('_', 1)[0]}"
                    stats["folder_sizes"][virtual_prefix] += sub_total_size
                elif current_depth <= 3 and new_prefix:
                    stats["folder_sizes"][new_prefix] += sub_total_size
                
                if sub_denied:
                    denied_tree.append({name: sub_denied})

            # Scenario B: Explicitly flagged as ACCESS_DENIED
            elif value == "ACCESS_DENIED":
                denied_tree.append({name: "ACCESS_DENIED"})

            # Scenario C: It's a file with metadata
            elif isinstance(value, dict) and "size_bytes" in value:
                file_size = value["size_bytes"]
                exclusive_files_size += file_size
                
                # 1. Track Extensions
                _, ext = os.path.splitext(name.lower())
                ext_key = ext or "no_extension"
                stats["extensions"][ext_key]["size"] += file_size
                stats["extensions"][ext_key]["count"] += 1
                
                # 2. Track Modification Time Clusters
                mod_time = parse_iso_time(value.get("modification_time"))
                if mod_time:
                    days_old = (now - mod_time).total_seconds() / 86400.0
                    if days_old < 0: 
                        days_old = 0 
                    stats["time_clusters"][get_log_time_cluster(days_old)] += 1

    # Add this folder's immediate flat files to its own level 3 bucket summary
    if current_depth <= 3 and path_prefix:
        stats["folder_sizes"][path_prefix] += exclusive_files_size

    # FIX: Return the absolute combined sum up the recursive stack
    true_total_folder_size = exclusive_files_size + total_subfolders_size
    return true_total_folder_size, (denied_tree if denied_tree else None)

def main():
    file_path = input("Enter the path of the drive JSON file to analyze (e.g., drive_c.json): ").strip()
    
    if not os.path.exists(file_path):
        print("File not found!")
        return
        
    data = load_json_data(file_path)
    now = datetime.now()
    
    stats = {
        "extensions": defaultdict(lambda: {"size": 0, "count": 0}),
        "time_clusters": defaultdict(int),
        "folder_sizes": defaultdict(int)
    }
    
    final_denied_tree = {}
    
    for drive_letter, root_contents in data.items():
        # Initialize drive base container size tracking
        stats["folder_sizes"][drive_letter] = 0
        drive_total, drive_denied_structure = analyze_hierarchy(root_contents, current_depth=1, path_prefix="", stats=stats, now=now)
        stats["folder_sizes"][drive_letter] = drive_total
        final_denied_tree[drive_letter] = drive_denied_structure if drive_denied_structure else []

    # Sorting
    sorted_extensions = dict(sorted(stats["extensions"].items(), key=lambda x: x[1]["size"], reverse=True))
    final_extensions_tuple = {ext: [d["size"], d["count"]] for ext, d in sorted_extensions.items()}
    sorted_folders = dict(sorted(stats["folder_sizes"].items(), key=lambda x: x[1], reverse=True))
    
    def cluster_sort_key(item):
        label = item[0]
        if "0 to 1" in label: return 0
        try:
            num = int(label.split()[0])
            if "year" in label: return num * 365
            if "month" in label: return num * 30
            return num
        except:
            return 99999
            
    sorted_time_clusters = dict(sorted(stats["time_clusters"].items(), key=cluster_sort_key))

    # Save outputs
    output_filename = f"analytics_{os.path.basename(file_path)}"
    final_output = {
        "1_extension_totals_[bytes, count]": final_extensions_tuple,
        "2_time_clusters_file_counts": sorted_time_clusters,
        "3_top_level_folder_sizes_bytes": sorted_folders,
        "4_access_denied_hierarchy": final_denied_tree
    }
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4)
        
    print(f"\nAnalysis complete! Cleaned results written to: {output_filename}")

if __name__ == "__main__":
    main()