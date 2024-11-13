import os
import json
import shutil
from datetime import datetime

folder_path = "../data/raw/cricsheet-raw"

destination_folder = "../data/processed/cricsheet-processed"

os.makedirs(destination_folder, exist_ok=True)

file_list = os.listdir(folder_path)

for file_name in file_list:
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        print(f"Reading {file_name}...")

        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            match_date = data['info']['dates'][0]
            check_date = "01-01-2014"
            date1 = datetime.strptime(match_date, "%d-%m-%Y")
            date2 = datetime.strptime(check_date, "%d-%m-%Y")

            if date1>date2:
                destination_path = os.path.join(destination_folder, file_name)
                shutil.move(file_path, destination_path)
                print(f"Moved {file_name} to {destination_folder}")

            print(json.dumps(data, indent=2)) 

print("All JSON files have been read successfully.")
