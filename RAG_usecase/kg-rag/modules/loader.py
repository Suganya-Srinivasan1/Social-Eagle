import json
import glob
import os
from pprint import pprint

directory_path = r"C:\Users\Hp\My_AI_works\kg-rag\data"

def load_json_files(directory_path):
    all_data = []
    
    # Path pattern to find all .json files
    search_pattern = os.path.join(directory_path, "*.json")
    file_list = glob.glob(search_pattern)
    
    if not file_list:
        print(f"No JSON files found in {directory_path}")
        return []

    for file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle both single objects and lists of objects
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
                print(f"Successfully loaded: {os.path.basename(file_path)}")
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

           
    return all_data

#all_data = load_json_files(directory_path)
#pprint(all_data, indent=4, depth=3, compact=False)
# Usage
# data = load_json_files('./data/knowledge_base')        