import os
import json
import string
import math
import numpy as np
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
    Recursively processes the tree to gather fine-grained topology metrics,
    counting absolute cumulative nested structures down the tree lines.
    """
    exclusive_files_size = 0
    total_folders_underneath = 0
    max_depth_underneath = 0
    denied_tree = []

    if not isinstance(contents, list):
        return 0, 0, 0, "ACCESS_DENIED"

    for item in contents:
        if not isinstance(item, dict):
            continue
            
        for name, value in item.items():
            # Scenario A: It's a folder
            if isinstance(value, list):
                stats["levels"][current_depth]["folders"] += 1
                new_prefix = f"{path_prefix}/{name}" if path_prefix else name

                # Recurse down
                sub_size, sub_folders, sub_depth, sub_denied = analyze_hierarchy(
                    value, current_depth + 1, new_prefix, stats, now
                )
                
                # Accumulate the geometric properties
                total_folders_underneath += 1 + sub_folders
                max_depth_underneath = max(max_depth_underneath, 1 + sub_depth)
                
                if sub_denied:
                    denied_tree.append({name: sub_denied})

            # Scenario B: Explicitly flagged as ACCESS_DENIED
            elif value == "ACCESS_DENIED":
                denied_tree.append({name: "ACCESS_DENIED"})

            # Scenario C: It's a file
            elif isinstance(value, dict) and "size_bytes" in value:
                file_size = value["size_bytes"]
                exclusive_files_size += file_size
                
                stats["levels"][current_depth]["files"] += 1
                stats["levels"][current_depth]["total_size_bytes"] += file_size
                
                # Track Extensions
                _, ext = os.path.splitext(name.lower())
                ext_key = ext or "no_extension"
                stats["extensions"][ext_key]["size"] += file_size
                stats["extensions"][ext_key]["count"] += 1
                
                # Track Modification Time Clusters
                mod_time = parse_iso_time(value.get("modification_time"))
                if mod_time:
                    days_old = (now - mod_time).total_seconds() / 86400.0
                    if days_old < 0: 
                        days_old = 0 
                    stats["time_clusters"][get_log_time_cluster(days_old)] += 1

    # Store the raw total structural volume count for this directory path node
    if total_folders_underneath > 0 and path_prefix:
        stats["raw_folder_counts"][path_prefix] = total_folders_underneath

    stats["levels"][current_depth]["total_size_bytes"] += exclusive_files_size
    return (exclusive_files_size), total_folders_underneath, max_depth_underneath, (denied_tree if denied_tree else None)

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
        "raw_folder_counts": {},
        "levels": defaultdict(lambda: {"folders": 0, "files": 0, "total_size_bytes": 0})
    }
    
    final_denied_tree = {}
    
    for drive_letter, root_contents in data.items():
        stats["levels"][1]["folders"] += 1
        _, _, _, drive_denied_structure = analyze_hierarchy(root_contents, current_depth=1, path_prefix="", stats=stats, now=now)
        final_denied_tree[drive_letter] = drive_denied_structure if drive_denied_structure else []

    # ==========================================
    # SECTION 1: String Formatted Ratios
    # ==========================================
    formatted_extensions = {}
    sorted_raw_ext = sorted(stats["extensions"].items(), key=lambda x: x[1]["size"], reverse=True)
    
    for ext, payload in sorted_raw_ext:
        size = payload["size"]
        count = payload["count"]
        ratio = size / count if count > 0 else 0.0
        formatted_extensions[ext] = f"{size} bytes / {count} files = {ratio:6.4f} bytes/file"

    # ==========================================
    # SECTION 3: Statistical Filtering & Branch Lineage Pruning
    # ==========================================
    filtered_branching = {}
    if stats["raw_folder_counts"]:
        counts_array = list(stats["raw_folder_counts"].values())
        mean_val = np.mean(counts_array)
        std_val = np.std(counts_array)
        
        dynamic_threshold = mean_val + (1.5 * std_val)
        print(f"Calculated Folder Count Stats -> Average: {mean_val:.2f}, Cutoff Threshold: {dynamic_threshold:.2f}")
        
        # Initial pass: get everything that qualifies above the outlier bar
        qualified_paths = {path: count for path, count in stats["raw_folder_counts"].items() if count >= dynamic_threshold}
        
        # Lineage Pruning: Remove ancestral conduits to isolate the deep specific root of the thicket
        pruned_paths = {}
        for path, count in qualified_paths.items():
            # Check if this folder has a subfolder that is ALSO in our qualified list
            has_heavy_subfolder = False
            for other_path in qualified_paths.keys():
                if other_path.startswith(path + "/"):
                    # If a subfolder accounts for almost the entire volume (e.g., within 100 subfolders difference), 
                    # it means this current folder path is just a redundant parent conduit line.
                    if qualified_paths[other_path] >= (count - 100):
                        has_heavy_subfolder = True
                        break
            
            if not has_heavy_subfolder:
                pruned_paths[path] = f"{count} nested subfolders"
                
        sorted_branching = dict(sorted(pruned_paths.items(), key=lambda x: int(x[1].split()[0]), reverse=True))
    else:
        sorted_branching = {}

    # ==========================================
    # SECTION 5: Generational Mapping
    # ==========================================
    formatted_levels = {}
    for level_idx in sorted(stats["levels"].keys()):
        formatted_levels[f"level_{level_idx}"] = dict(stats["levels"][level_idx])

    # Sort Time Clusters
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

    # Assemble output object
    output_filename = f"analytics_{os.path.basename(file_path)}"
    final_output = {
        "1_extension_analytics": formatted_extensions,
        "2_time_clusters_file_counts": sorted_time_clusters,
        "3_heaviest_branching_directories_volume": sorted_branching,
        "4_access_denied_hierarchy": final_denied_tree,
        "5_generational_level_topology": formatted_levels
    }
    
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=4)
        
    print(f"\nAnalysis complete! Topological output written to: {output_filename}")

if __name__ == "__main__":
    main()