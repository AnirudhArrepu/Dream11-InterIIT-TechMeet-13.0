import os
import json
import shutil
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

folder_path = "../data/raw/cricksheet/cricsheet-raw"
destination_folder = "../data/interim/cricksheet-interim"

# Create the destination directory if it doesn't exist
os.makedirs(destination_folder, exist_ok=True)

# Function to process each file
def process_file(file_name):
    if file_name.endswith(".json"):
        file_path = os.path.join(folder_path, file_name)
        print(f"Reading {file_name}...")

        # Open and read the JSON file
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
        
        # Process the data after closing the file
        match_date = data['info']['dates'][0]
        check_date = "2014-01-01"

        # Parse the dates using the correct format
        date1 = datetime.strptime(match_date, "%Y-%m-%d")
        date2 = datetime.strptime(check_date, "%Y-%m-%d")

        # Move the file if the match date is after the check date
        if date1 > date2:
            destination_path = os.path.join(destination_folder, file_name)
            try:
                shutil.move(file_path, destination_path)
                print(f"Moved {file_name} to {destination_folder}")
            except PermissionError:
                print(f"Failed to move {file_name}. The file is locked or being used by another process.")

        # Print the JSON data
        print(json.dumps(data, indent=2))

# Get the list of files
file_list = os.listdir(folder_path)

# Use ThreadPoolExecutor to process files in parallel
with ThreadPoolExecutor() as executor:
    executor.map(process_file, file_list)

print("All JSON files have been processed successfully.")
